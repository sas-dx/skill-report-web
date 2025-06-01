// RPT.1-EXCEL.1: レポート画面
'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { Sidebar } from '@/components/dashboard/Sidebar';
import { ReportContent } from '@/components/reports/ReportContent';

export default function ReportsPage() {
  const router = useRouter();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

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
        title="レポート"
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
          <ReportContent />
        </div>
      </div>
    </div>
  );
}
