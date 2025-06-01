// PLT.1-WEB.1: 通知アイコンコンポーネント
'use client';

import React, { useState, useRef, useEffect } from 'react';

interface Notification {
  id: string;
  title: string;
  message: string;
  type: 'system' | 'personal' | 'organization';
  isRead: boolean;
  timestamp: string;
}

interface NotificationIconProps {
  notifications?: Notification[];
  onNotificationClick?: (notification: Notification) => void;
  onMarkAllRead?: () => void;
}

// モックデータ
const mockNotifications: Notification[] = [
  {
    id: '1',
    title: 'スキル評価期限のお知らせ',
    message: '2025年6月15日までにスキル自己評価を完了してください。',
    type: 'system',
    isRead: false,
    timestamp: '2025-06-01T09:00:00Z',
  },
  {
    id: '2',
    title: '新しい研修コースが追加されました',
    message: 'React Advanced Patterns研修が利用可能になりました。',
    type: 'organization',
    isRead: false,
    timestamp: '2025-05-31T14:30:00Z',
  },
  {
    id: '3',
    title: 'プロフィール更新完了',
    message: 'プロフィール情報が正常に更新されました。',
    type: 'personal',
    isRead: true,
    timestamp: '2025-05-30T16:45:00Z',
  },
];

export const NotificationIcon: React.FC<NotificationIconProps> = ({
  notifications = mockNotifications,
  onNotificationClick,
  onMarkAllRead,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const unreadCount = notifications.filter(n => !n.isRead).length;

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
      case 'system':
        return (
          <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
            <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        );
      case 'personal':
        return (
          <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
            <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
        );
      case 'organization':
        return (
          <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center">
            <svg className="w-4 h-4 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
        );
      default:
        return null;
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
                onClick={() => {
                  onMarkAllRead?.();
                  setIsOpen(false);
                }}
                className="text-sm text-blue-600 hover:text-blue-800 font-medium"
              >
                すべて既読にする
              </button>
            )}
          </div>

          {/* 通知リスト */}
          <div className="max-h-96 overflow-y-auto">
            {notifications.length === 0 ? (
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
                    ${!notification.isRead ? 'bg-blue-50' : ''}
                  `}
                  onClick={() => {
                    onNotificationClick?.(notification);
                    setIsOpen(false);
                  }}
                >
                  <div className="flex items-start space-x-3">
                    {getNotificationIcon(notification.type)}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <p className={`text-sm font-medium ${!notification.isRead ? 'text-gray-900' : 'text-gray-600'}`}>
                          {notification.title}
                        </p>
                        {!notification.isRead && (
                          <div className="w-2 h-2 bg-blue-600 rounded-full flex-shrink-0"></div>
                        )}
                      </div>
                      <p className="text-sm text-gray-500 mt-1 line-clamp-2">
                        {notification.message}
                      </p>
                      <p className="text-xs text-gray-400 mt-1">
                        {formatTimestamp(notification.timestamp)}
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
