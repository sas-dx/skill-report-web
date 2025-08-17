// PLT.1-WEB.1: ダッシュボード画面
'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { DashboardContent } from '@/components/dashboard/DashboardContent';
import { Sidebar } from '@/components/dashboard/Sidebar';

export default function DashboardPage() {
  const router = useRouter();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  // TODO: 実際の認証状態とユーザー情報を取得
  const userName = 'テストユーザー';

  const handleLogout = () => {
    // ログアウト処理
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    localStorage.removeItem('tenant');
    router.push('/');
  };

  const handleMenuClick = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleSidebarClose = () => {
    setIsSidebarOpen(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ヘッダー - 最上部に固定 */}
      <DashboardHeader 
        onMenuClick={handleMenuClick}
        title="ダッシュボード"
      />

      {/* メインレイアウト - ヘッダーの下 */}
      <div className="flex pt-16">
        {/* サイドバー */}
        <Sidebar 
          isOpen={isSidebarOpen}
          onClose={handleSidebarClose}
        />

        {/* メインコンテンツエリア */}
        <div className="flex-1 lg:ml-64">
          {/* コンテンツ */}
          <DashboardContent 
            userName={userName}
          />
        </div>
      </div>
    </div>
  );
}
