// PLT.1-WEB.1: ダッシュボード画面
'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { DashboardContent } from '@/components/dashboard/DashboardContent';

export default function DashboardPage() {
  const router = useRouter();

  // TODO: 実際の認証状態とユーザー情報を取得
  const userName = 'テストユーザー';

  const handleLogout = () => {
    // TODO: 実際のログアウト処理を実装
    console.log('ログアウト処理');
    router.push('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardHeader 
        userName={userName}
        onLogout={handleLogout}
      />
      <DashboardContent 
        userName={userName}
      />
    </div>
  );
}
