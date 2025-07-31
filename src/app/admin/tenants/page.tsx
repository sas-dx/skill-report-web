/**
 * 要求仕様ID: TNT.1-MGMT
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_TNT_Admin_テナント管理画面.md
 * 実装内容: テナント管理画面（管理者専用）
 */

'use client';

import React, { useState } from 'react';
import { TenantManagement } from '@/components/admin/TenantManagement';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { Sidebar } from '@/components/dashboard/Sidebar';

export default function TenantAdminPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ダッシュボードヘッダー */}
      <DashboardHeader 
        onMenuClick={() => setSidebarOpen(true)}
        title="テナント管理"
      />

      {/* サイドバー */}
      <Sidebar 
        isOpen={sidebarOpen} 
        onClose={() => setSidebarOpen(false)} 
      />

      {/* メインコンテンツ */}
      <div className="pt-16 lg:pl-64">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* ページタイトル */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">テナント管理</h1>
            <p className="mt-2 text-lg text-gray-600">
              システム内のテナント（組織）を管理します
            </p>
          </div>

          {/* テナント管理コンポーネント */}
          <TenantManagement />
        </div>
      </div>
    </div>
  );
}
