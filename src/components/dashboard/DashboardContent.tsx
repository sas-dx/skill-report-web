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
    <main className="p-6 space-y-6">
      {/* ウェルカムセクション */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">
          おかえりなさい、{userName}さん
        </h1>
        <p className="text-blue-100">
          今日も一日お疲れさまです。スキルアップの進捗を確認しましょう。
        </p>
      </div>

      {/* 統計情報カード */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* 登録スキル数 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">登録スキル数</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">24</p>
              <p className="text-sm text-green-600 mt-1">+3 今月</p>
            </div>
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>

        {/* 目標達成率 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">目標達成率</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">75%</p>
              <p className="text-sm text-green-600 mt-1">+5% 先月比</p>
            </div>
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
          </div>
        </div>

        {/* 研修受講数 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">研修受講数</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">8</p>
              <p className="text-sm text-blue-600 mt-1">今年度</p>
            </div>
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
          </div>
        </div>

        {/* 作業実績 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">作業実績</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">12</p>
              <p className="text-sm text-orange-600 mt-1">プロジェクト</p>
            </div>
            <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* クイックアクション */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-gray-900">
                クイックアクション
              </h2>
              <span className="text-sm text-gray-500">よく使う機能</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* スキル情報管理 */}
              <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors cursor-pointer">
                <div className="flex items-center mb-3">
                  <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                    <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <h3 className="ml-3 font-medium text-gray-900">スキル管理</h3>
                </div>
                <p className="text-sm text-gray-600 mb-4">
                  スキル情報を登録・更新して、あなたの成長を記録しましょう
                </p>
                <Button size="sm" className="w-full">
                  スキル管理へ
                </Button>
              </div>

              {/* プロフィール管理 */}
              <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors cursor-pointer">
                <div className="flex items-center mb-3">
                  <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                    <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <h3 className="ml-3 font-medium text-gray-900">プロフィール</h3>
                </div>
                <p className="text-sm text-gray-600 mb-4">
                  基本情報・目標を設定して、キャリアプランを明確にしましょう
                </p>
                <Button variant="outline" size="sm" className="w-full">
                  プロフィール編集
                </Button>
              </div>

              {/* 目標管理 */}
              <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors cursor-pointer">
                <div className="flex items-center mb-3">
                  <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                    <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                  </div>
                  <h3 className="ml-3 font-medium text-gray-900">目標管理</h3>
                </div>
                <p className="text-sm text-gray-600 mb-4">
                  キャリア目標を設定し、進捗を管理しましょう
                </p>
                <Button variant="outline" size="sm" className="w-full">
                  目標設定
                </Button>
              </div>

              {/* レポート */}
              <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors cursor-pointer">
                <div className="flex items-center mb-3">
                  <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
                    <svg className="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h3 className="ml-3 font-medium text-gray-900">レポート</h3>
                </div>
                <p className="text-sm text-gray-600 mb-4">
                  スキル分析・レポートを確認して成長を可視化しましょう
                </p>
                <Button variant="outline" size="sm" className="w-full">
                  レポート表示
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* 通知・お知らせ */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">
              通知・お知らせ
            </h2>
            <span className="bg-red-100 text-red-800 text-xs font-medium px-2 py-1 rounded-full">
              3件
            </span>
          </div>
          <div className="space-y-4">
            <div className="flex items-start p-3 bg-blue-50 rounded-lg border-l-4 border-blue-400">
              <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
              <div className="flex-1">
                <p className="text-sm text-gray-900 font-medium">
                  スキル評価の更新をお願いします
                </p>
                <p className="text-xs text-gray-500 mt-1">2時間前</p>
              </div>
            </div>
            <div className="flex items-start p-3 bg-green-50 rounded-lg border-l-4 border-green-400">
              <div className="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
              <div className="flex-1">
                <p className="text-sm text-gray-900 font-medium">
                  新しい研修「React基礎」が追加されました
                </p>
                <p className="text-xs text-gray-500 mt-1">1日前</p>
              </div>
            </div>
            <div className="flex items-start p-3 bg-yellow-50 rounded-lg border-l-4 border-yellow-400">
              <div className="w-2 h-2 bg-yellow-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
              <div className="flex-1">
                <p className="text-sm text-gray-900 font-medium">
                  目標設定の期限が近づいています
                </p>
                <p className="text-xs text-gray-500 mt-1">3日前</p>
              </div>
            </div>
          </div>
          <Button variant="outline" size="sm" className="w-full mt-4">
            すべての通知を見る
          </Button>
        </div>
      </div>

      {/* 最近の活動・進捗状況 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 最近の活動 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            最近の活動
          </h2>
          <div className="space-y-4">
            <div className="flex items-center p-3 bg-gray-50 rounded-lg">
              <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                </svg>
              </div>
              <div className="ml-3 flex-1">
                <p className="text-sm font-medium text-gray-900">システムにログイン</p>
                <p className="text-xs text-gray-500">たった今</p>
              </div>
            </div>
            <div className="flex items-center p-3 bg-gray-50 rounded-lg">
              <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-3 flex-1">
                <p className="text-sm font-medium text-gray-900">JavaScript スキルを更新</p>
                <p className="text-xs text-gray-500">2時間前</p>
              </div>
            </div>
            <div className="flex items-center p-3 bg-gray-50 rounded-lg">
              <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
                <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div className="ml-3 flex-1">
                <p className="text-sm font-medium text-gray-900">React基礎研修を受講</p>
                <p className="text-xs text-gray-500">1日前</p>
              </div>
            </div>
          </div>
        </div>

        {/* 進捗状況 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            進捗状況
          </h2>
          <div className="space-y-6">
            {/* 年間目標進捗 */}
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-900">年間目標達成</span>
                <span className="text-sm font-semibold text-blue-600">75%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div className="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full transition-all duration-300" style={{ width: '75%' }}></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">目標まであと25%</p>
            </div>

            {/* スキル習得進捗 */}
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-900">スキル習得</span>
                <span className="text-sm font-semibold text-green-600">60%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div className="bg-gradient-to-r from-green-500 to-green-600 h-3 rounded-full transition-all duration-300" style={{ width: '60%' }}></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">24/40 スキル習得済み</p>
            </div>

            {/* 研修受講進捗 */}
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-900">研修受講</span>
                <span className="text-sm font-semibold text-purple-600">80%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div className="bg-gradient-to-r from-purple-500 to-purple-600 h-3 rounded-full transition-all duration-300" style={{ width: '80%' }}></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">8/10 研修完了</p>
            </div>
          </div>
        </div>
      </div>

      {/* スキルマップ概要 */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">
            スキルマップ概要
          </h2>
          <Button variant="outline" size="sm">
            詳細を見る
          </Button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600 mb-1">8</div>
            <div className="text-sm text-gray-600">フロントエンド</div>
          </div>
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600 mb-1">6</div>
            <div className="text-sm text-gray-600">バックエンド</div>
          </div>
          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <div className="text-2xl font-bold text-purple-600 mb-1">10</div>
            <div className="text-sm text-gray-600">その他</div>
          </div>
        </div>
      </div>
    </main>
  );
};
