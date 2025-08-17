/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: キャリアプラン画面
 */

'use client';

import React, { useState, useEffect } from 'react';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { Sidebar } from '@/components/dashboard/Sidebar';
import { CareerPlanContent } from '@/components/career/CareerPlanContent';

export default function CareerPage() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);

  const handleMenuClick = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleSidebarClose = () => {
    setIsSidebarOpen(false);
  };

  // ログインユーザーの情報を取得
  useEffect(() => {
    const user = localStorage.getItem('user');
    console.log('Career Page - User from localStorage:', user);
    
    if (user) {
      try {
        const userData = JSON.parse(user);
        console.log('Career Page - Parsed userData:', userData);
        
        // employeeIdまたはuserIdを使用
        const id = userData.employeeId || userData.userId;
        if (id) {
          console.log('Career Page - Setting userId:', id);
          setUserId(id);
        } else {
          console.error('ユーザーIDが見つかりません');
          // デフォルト値として000001を使用（テスト用）
          setUserId('000001');
        }
      } catch (error) {
        console.error('ユーザー情報の解析エラー:', error);
        // デフォルト値として000001を使用（テスト用）
        setUserId('000001');
      }
    } else {
      console.log('Career Page - No user info in localStorage, using default');
      // デフォルト値として000001を使用（テスト用）
      setUserId('000001');
    }
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ヘッダー */}
      <DashboardHeader 
        onMenuClick={handleMenuClick}
        title="年間スキル報告書システム"
      />

      {/* メインレイアウト */}
      <div className="flex pt-16">
        {/* サイドバー */}
        <Sidebar 
          isOpen={isSidebarOpen}
          onClose={handleSidebarClose}
        />

        {/* メインコンテンツエリア */}
        <div className="flex-1 lg:ml-64">
          <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
            {userId && <CareerPlanContent userId={userId} />}
          </div>
        </div>
      </div>
    </div>
  );
}
