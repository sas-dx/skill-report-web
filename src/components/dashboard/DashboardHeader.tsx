// PLT.1-WEB.1: ダッシュボードヘッダーコンポーネント
'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { NotificationIcon } from '../ui/NotificationIcon';
import { UserDropdown } from '../ui/UserDropdown';

interface DashboardHeaderProps {
  onMenuClick: () => void;
  title?: string;
}

export const DashboardHeader: React.FC<DashboardHeaderProps> = ({ 
  onMenuClick, 
  title = 'ダッシュボード' 
}) => {
  const router = useRouter();

  const handleLogout = () => {
    // ログアウト処理
    // TODO: 実際のログアウトAPI呼び出しを実装
    console.log('ログアウト処理');
    
    // ルートページ（トップページ）に遷移
    router.push('/');
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-30 bg-white shadow-sm border-b border-gray-200">
      <div className="flex items-center justify-between h-16 px-4 lg:px-6">
        {/* 左側: メニューボタン + ロゴ + システム名 */}
        <div className="flex items-center">
          {/* モバイル用メニューボタン */}
          <button
            onClick={onMenuClick}
            className="lg:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 transition-colors duration-150"
            aria-label="メニューを開く"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          {/* ロゴ + システム名 */}
          <div className="flex items-center ml-4 lg:ml-0">
            {/* ロゴ */}
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center mr-3">
              <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            
            {/* システム名 */}
            <h1 className="text-xl font-semibold text-gray-900">
              年間スキル報告書システム
            </h1>
          </div>
        </div>

        {/* 右側: 通知 + ユーザーメニュー */}
        <div className="flex items-center space-x-4">
          {/* 通知アイコン */}
          <NotificationIcon
            onNotificationClick={(notification) => {
              console.log('通知クリック:', notification);
            }}
            onMarkAllRead={() => {
              console.log('すべて既読にする');
            }}
          />

          {/* ユーザードロップダウン */}
          <UserDropdown onLogout={handleLogout} />
        </div>
      </div>
    </header>
  );
};
