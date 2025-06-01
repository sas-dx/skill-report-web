// PLT.1-WEB.1: ダッシュボードヘッダーコンポーネント
'use client';

import React from 'react';
import { Button } from '@/components/ui/Button';

interface DashboardHeaderProps {
  userName: string;
  onLogout: () => void;
}

export const DashboardHeader: React.FC<DashboardHeaderProps> = ({
  userName,
  onLogout
}) => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* ロゴ・タイトル */}
          <div className="flex items-center">
            <h1 className="text-xl font-semibold text-gray-900">
              スキル報告書システム
            </h1>
          </div>

          {/* ユーザー情報・ログアウト */}
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-700">
              ようこそ、<span className="font-medium">{userName}</span>さん
            </span>
            <Button
              variant="outline"
              size="sm"
              onClick={onLogout}
              className="text-gray-600 hover:text-gray-900"
            >
              ログアウト
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};
