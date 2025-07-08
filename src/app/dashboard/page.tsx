/**
 * 要求仕様ID: PLT.1-WEB.1
 * 対応設計書: docs/design/screens/specs/画面設計書_SCR-DASHBOARD_ダッシュボード画面.md
 * 実装内容: ダッシュボード画面（実データ対応）
 */

'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { DashboardContent } from '@/components/dashboard/DashboardContent';
import { Sidebar } from '@/components/dashboard/Sidebar';
import { useDashboard } from '@/hooks/useDashboard';

export default function DashboardPage() {
  const router = useRouter();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const { data, loading, error } = useDashboard();

  // 認証エラーの場合はログインページにリダイレクト
  useEffect(() => {
    if (error && error.includes('認証が必要です')) {
      console.log('認証エラーによりログインページにリダイレクト');
      router.push('/');
    }
  }, [error, router]);

  // ローディング中の表示
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">読み込み中...</p>
        </div>
      </div>
    );
  }

  // 認証エラーの場合は何も表示しない（リダイレクト処理中）
  if (error && error.includes('認証が必要です')) {
    return null;
  }

  const handleLogout = () => {
    // TODO: 実際のログアウト処理を実装
    console.log('ログアウト処理');
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
          {/* コンテンツ - userNameプロパティを削除（useDashboardフックで取得） */}
          <DashboardContent />
        </div>
      </div>
    </div>
  );
}
