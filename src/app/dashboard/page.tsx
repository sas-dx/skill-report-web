/**
 * 要求仕様ID: PLT.1-WEB.1
 * 対応設計書: docs/design/screens/specs/画面設計書_SCR-DASHBOARD_ダッシュボード画面.md
 * 実装内容: ダッシュボード画面（実データ対応）
 */

'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { DashboardContent } from '@/components/dashboard/DashboardContent';
import { Sidebar } from '@/components/dashboard/Sidebar';

export default function DashboardPage() {
  const router = useRouter();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const handleLogout = () => {
    // TODO: 実際のログアウト処理を実装
    console.log('ログアウト処理');
    router.push('/login');
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
          {/* コンテンツ - userNameプロパティを削除（useDashboardフックで取得） */}
          <DashboardContent />
        </div>
      </div>
    </div>
  );
}
