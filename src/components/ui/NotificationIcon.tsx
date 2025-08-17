// PLT.1-WEB.1: 通知アイコンコンポーネント
'use client';

import React, { useState, useRef, useEffect } from 'react';

interface Notification {
  id: string;
  title: string;
  message: string;
  type: 'info' | 'warning' | 'error' | 'success';
  is_read: boolean;
  created_at: string;
  action_url?: string | null;
  metadata?: any;
}

interface NotificationIconProps {
  onNotificationClick?: (notification: Notification) => void;
  onMarkAllRead?: () => void;
}

interface NotificationApiResponse {
  success: boolean;
  data?: {
    notifications: Notification[];
    summary: {
      total: number;
      unread: number;
      read: number;
    };
    pagination: {
      limit: number;
      offset: number;
      hasMore: boolean;
    };
  };
  error?: string;
}

export const NotificationIcon: React.FC<NotificationIconProps> = ({
  onNotificationClick,
  onMarkAllRead,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const unreadCount = notifications.filter(n => !n.is_read).length;

  // 通知を取得する関数
  const fetchNotifications = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // 認証トークンを取得
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('認証トークンが見つかりません');
      }
      
      const response = await fetch('/api/notifications/me', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result: NotificationApiResponse = await response.json();
      
      if (result.success && result.data) {
        setNotifications(result.data.notifications);
      } else {
        throw new Error(result.error || '通知の取得に失敗しました');
      }
    } catch (err) {
      console.error('通知取得エラー:', err);
      setError(err instanceof Error ? err.message : '通知の取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  // 通知を既読にする関数
  const markNotificationsAsRead = async (notificationIds: string[]) => {
    try {
      // 認証トークンを取得
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('認証トークンが見つかりません');
      }
      
      const response = await fetch('/api/notifications/me', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ notificationIds }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      if (result.success) {
        // ローカル状態を更新
        setNotifications(prev => 
          prev.map(notification => 
            notificationIds.includes(notification.id)
              ? { ...notification, is_read: true }
              : notification
          )
        );
      } else {
        throw new Error(result.error || '既読処理に失敗しました');
      }
    } catch (err) {
      console.error('既読処理エラー:', err);
      setError(err instanceof Error ? err.message : '既読処理に失敗しました');
    }
  };

  // すべての未読通知を既読にする関数
  const handleMarkAllRead = async () => {
    const unreadIds = notifications
      .filter(n => !n.is_read)
      .map(n => n.id);
    
    if (unreadIds.length > 0) {
      await markNotificationsAsRead(unreadIds);
      onMarkAllRead?.();
    }
  };

  // 通知クリック時の処理
  const handleNotificationClick = async (notification: Notification) => {
    if (!notification.is_read) {
      await markNotificationsAsRead([notification.id]);
    }
    onNotificationClick?.(notification);
  };

  // 初回データ取得とポーリング設定
  useEffect(() => {
    // 初回取得
    fetchNotifications();

    // 30秒間隔でポーリング
    const interval = setInterval(() => {
      fetchNotifications();
    }, 30000);

    return () => {
      clearInterval(interval);
    };
  }, []);

  // 外部クリックでドロップダウンを閉じる
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const getNotificationIcon = (type: Notification['type']) => {
    switch (type) {
      case 'info':
        return (
          <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
            <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        );
      case 'success':
        return (
          <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
            <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
        );
      case 'warning':
        return (
          <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center">
            <svg className="w-4 h-4 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-1.732-.833-2.464 0L5.35 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
        );
      case 'error':
        return (
          <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
            <svg className="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
        );
      default:
        return (
          <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">
            <svg className="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-5 5v-5zM11 19H7a2 2 0 01-2-2V7a2 2 0 012-2h4m0 14v-5a2 2 0 012-2h2a2 2 0 012 2v5m-6 0h6" />
            </svg>
          </div>
        );
    }
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));

    if (diffInHours < 1) {
      return 'たった今';
    } else if (diffInHours < 24) {
      return `${diffInHours}時間前`;
    } else {
      const diffInDays = Math.floor(diffInHours / 24);
      return `${diffInDays}日前`;
    }
  };

  return (
    <div className="relative" ref={dropdownRef}>
      {/* 通知アイコンボタン */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 text-gray-400 hover:text-gray-500 hover:bg-gray-100 rounded-full transition-colors duration-150"
        aria-label={`通知 ${unreadCount > 0 ? `(${unreadCount}件の未読)` : ''}`}
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-5 5v-5zM11 19H7a2 2 0 01-2-2V7a2 2 0 012-2h4m0 14v-5a2 2 0 012-2h2a2 2 0 012 2v5m-6 0h6" />
        </svg>
        
        {/* 未読バッジ */}
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white transform translate-x-1/2 -translate-y-1/2 bg-red-600 rounded-full">
            {unreadCount > 99 ? '99+' : unreadCount}
          </span>
        )}
      </button>

      {/* ドロップダウンメニュー */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
          {/* ヘッダー */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">通知</h3>
            {unreadCount > 0 && (
              <button
                onClick={async () => {
                  await handleMarkAllRead();
                  setIsOpen(false);
                }}
                className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                disabled={loading}
              >
                すべて既読にする
              </button>
            )}
          </div>

          {/* 通知リスト */}
          <div className="max-h-96 overflow-y-auto">
            {loading ? (
              <div className="px-4 py-8 text-center text-gray-500">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
                <p>読み込み中...</p>
              </div>
            ) : error ? (
              <div className="px-4 py-8 text-center text-red-500">
                <svg className="w-12 h-12 mx-auto mb-4 text-red-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-1.732-.833-2.464 0L5.35 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
                <p>{error}</p>
                <button
                  onClick={fetchNotifications}
                  className="mt-2 text-sm text-blue-600 hover:text-blue-800 font-medium"
                >
                  再試行
                </button>
              </div>
            ) : notifications.length === 0 ? (
              <div className="px-4 py-8 text-center text-gray-500">
                <svg className="w-12 h-12 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-5 5v-5zM11 19H7a2 2 0 01-2-2V7a2 2 0 012-2h4m0 14v-5a2 2 0 012-2h2a2 2 0 012 2v5m-6 0h6" />
                </svg>
                <p>通知はありません</p>
              </div>
            ) : (
              notifications.map((notification) => (
                <div
                  key={notification.id}
                  className={`
                    px-4 py-3 border-b border-gray-100 hover:bg-gray-50 cursor-pointer transition-colors duration-150
                    ${!notification.is_read ? 'bg-blue-50' : ''}
                  `}
                  onClick={() => {
                    handleNotificationClick(notification);
                    setIsOpen(false);
                  }}
                >
                  <div className="flex items-start space-x-3">
                    {getNotificationIcon(notification.type)}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <p className={`text-sm font-medium ${!notification.is_read ? 'text-gray-900' : 'text-gray-600'}`}>
                          {notification.title}
                        </p>
                        {!notification.is_read && (
                          <div className="w-2 h-2 bg-blue-600 rounded-full flex-shrink-0"></div>
                        )}
                      </div>
                      <p className="text-sm text-gray-500 mt-1 line-clamp-2">
                        {notification.message}
                      </p>
                      <p className="text-xs text-gray-400 mt-1">
                        {formatTimestamp(notification.created_at)}
                      </p>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* フッター */}
          {notifications.length > 0 && (
            <div className="px-4 py-3 border-t border-gray-200">
              <button
                onClick={() => setIsOpen(false)}
                className="w-full text-center text-sm text-blue-600 hover:text-blue-800 font-medium"
              >
                すべての通知を表示
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
