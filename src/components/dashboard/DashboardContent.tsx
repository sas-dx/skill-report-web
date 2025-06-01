// PLT.1-WEB.1: ダッシュボードメインコンテンツコンポーネント
'use client';

import React from 'react';
import { Button } from '@/components/ui/Button';

interface DashboardContentProps {
  userName: string;
}

export const DashboardContent: React.FC<DashboardContentProps> = ({
  userName
}) => {
  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* ウェルカムセクション */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          ダッシュボード
        </h2>
        <p className="text-gray-600">
          {userName}さん、お疲れ様です。今日も一日頑張りましょう！
        </p>
      </div>

      {/* クイックアクションカード */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {/* スキル情報管理 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center mb-4">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="ml-3 text-lg font-semibold text-gray-900">
              スキル情報
            </h3>
          </div>
          <p className="text-gray-600 mb-4">
            あなたのスキル情報を管理・更新できます
          </p>
          <Button className="w-full">
            スキル管理へ
          </Button>
        </div>

        {/* プロフィール管理 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center mb-4">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <h3 className="ml-3 text-lg font-semibold text-gray-900">
              プロフィール
            </h3>
          </div>
          <p className="text-gray-600 mb-4">
            基本情報やキャリア目標を設定できます
          </p>
          <Button variant="outline" className="w-full">
            プロフィール編集
          </Button>
        </div>

        {/* レポート・分析 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center mb-4">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 className="ml-3 text-lg font-semibold text-gray-900">
              レポート
            </h3>
          </div>
          <p className="text-gray-600 mb-4">
            スキル分析やレポートを確認できます
          </p>
          <Button variant="outline" className="w-full">
            レポート表示
          </Button>
        </div>
      </div>

      {/* 最近の活動 */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          最近の活動
        </h3>
        <div className="space-y-3">
          <div className="flex items-center text-sm text-gray-600">
            <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
            <span>システムにログインしました</span>
            <span className="ml-auto text-gray-400">たった今</span>
          </div>
          <div className="flex items-center text-sm text-gray-600">
            <div className="w-2 h-2 bg-gray-300 rounded-full mr-3"></div>
            <span>今後の活動がここに表示されます</span>
          </div>
        </div>
      </div>
    </main>
  );
};
