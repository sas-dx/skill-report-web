/**
 * 要求仕様ID: PLT.1-WEB.1
 * 対応設計書: docs/design/screens/specs/画面設計書_SCR-DASHBOARD_ダッシュボード画面.md
 * 実装内容: ダッシュボードメインコンテンツ（実データ対応）
 */

'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { Spinner } from '@/components/ui/Spinner';
import { 
  useDashboard, 
  getSkillLevelName, 
  getPriorityLevelName, 
  getAchievementStatusName,
  getNotificationPriorityClass 
} from '@/hooks/useDashboard';

export function DashboardContent() {
  const router = useRouter();
  const { data, loading, error, refetch } = useDashboard();

  // ナビゲーションハンドラー
  const handleSkillManagement = () => {
    router.push('/skills');
  };

  const handleProfileEdit = () => {
    router.push('/profile');
  };

  const handleGoalSetting = () => {
    router.push('/career');
  };

  const handleReportView = () => {
    router.push('/reports');
  };

  if (loading) {
    return (
      <div className="p-6 flex items-center justify-center min-h-96">
        <div className="text-center">
          <Spinner size="lg" />
          <p className="mt-4 text-gray-600">ダッシュボードデータを読み込み中...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
          <div className="text-red-600 mb-4">
            <svg className="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 15.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-red-800 mb-2">データの読み込みに失敗しました</h3>
          <p className="text-red-600 mb-4">{error}</p>
          <Button onClick={refetch} variant="outline">
            再試行
          </Button>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="p-6">
        <div className="text-center text-gray-500">
          <p>データが見つかりません</p>
        </div>
      </div>
    );
  }

  const { user, profile, skillSummary, recentTraining, goalProgress, notifications } = data;

  return (
    <main className="p-6 space-y-6">
      {/* ウェルカムセクション */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">
          おかえりなさい、{user.fullName}さん
        </h1>
        <p className="text-blue-100">
          今日も一日お疲れさまです。スキルアップの進捗を確認しましょう。
        </p>
        <div className="mt-4 text-sm text-blue-100">
          最終更新: {new Date(data.lastUpdated).toLocaleString('ja-JP')}
        </div>
      </div>

      {/* 統計情報カード */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* 登録スキル数 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">登録スキル数</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{skillSummary.levelCounts.total}</p>
              <p className="text-sm text-blue-600 mt-1">
                レベル4: {skillSummary.levelCounts.level4}件
              </p>
            </div>
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>

        {/* 進行中の目標 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">進行中の目標</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{goalProgress.length}</p>
              <p className="text-sm text-green-600 mt-1">
                {goalProgress.filter(g => g.achievement_status === 'IN_PROGRESS').length}件 進行中
              </p>
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
              <p className="text-3xl font-bold text-gray-900 mt-2">{recentTraining.length}</p>
              <p className="text-sm text-purple-600 mt-1">
                {recentTraining.filter(t => t.certificate_obtained).length}件 修了証取得
              </p>
            </div>
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
          </div>
        </div>

        {/* 未読通知 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">未読通知</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{notifications.length}</p>
              <p className="text-sm text-orange-600 mt-1">
                {notifications.filter(n => n.priority_level === 'HIGH').length}件 重要
              </p>
            </div>
            <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-5 5v-5zM4 19h6v-2H4v2zM4 15h8v-2H4v2zM4 11h8V9H4v2z" />
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
              <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors cursor-pointer" onClick={handleSkillManagement}>
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
                <Button size="sm" className="w-full" onClick={handleSkillManagement}>
                  スキル管理へ
                </Button>
              </div>

              {/* プロフィール管理 */}
              <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors cursor-pointer" onClick={handleProfileEdit}>
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
                <Button variant="outline" size="sm" className="w-full" onClick={handleProfileEdit}>
                  プロフィール編集
                </Button>
              </div>

              {/* 目標管理 */}
              <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors cursor-pointer" onClick={handleGoalSetting}>
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
                <Button variant="outline" size="sm" className="w-full" onClick={handleGoalSetting}>
                  目標設定
                </Button>
              </div>

              {/* レポート */}
              <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors cursor-pointer" onClick={handleReportView}>
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
                <Button variant="outline" size="sm" className="w-full" onClick={handleReportView}>
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
            {notifications.length > 0 && (
              <span className="bg-red-100 text-red-800 text-xs font-medium px-2 py-1 rounded-full">
                {notifications.length}件
              </span>
            )}
          </div>
          <div className="space-y-4">
            {notifications.length === 0 ? (
              <div className="text-center text-gray-500 py-8">
                <svg className="w-12 h-12 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                </svg>
                <p>新しい通知はありません</p>
              </div>
            ) : (
              notifications.slice(0, 5).map((notification, index) => (
                <div key={notification.notification_id || index} 
                     className={`flex items-start p-3 rounded-lg border-l-4 ${getNotificationPriorityClass(notification.priority_level || 'LOW')}`}>
                  <div className="w-2 h-2 bg-current rounded-full mt-2 mr-3 flex-shrink-0"></div>
                  <div className="flex-1">
                    <p className="text-sm font-medium">
                      {notification.title || '通知'}
                    </p>
                    {notification.message && (
                      <p className="text-xs text-gray-600 mt-1">
                        {notification.message}
                      </p>
                    )}
                    <p className="text-xs text-gray-500 mt-1">
                      {notification.created_at.toLocaleString('ja-JP')}
                    </p>
                  </div>
                </div>
              ))
            )}
          </div>
          {notifications.length > 0 && (
            <Button variant="outline" size="sm" className="w-full mt-4">
              すべての通知を見る
            </Button>
          )}
        </div>
      </div>

      {/* 最近の活動・進捗状況 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 最近のスキル更新 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            最近のスキル更新
          </h2>
          <div className="space-y-4">
            {skillSummary.recentSkills.length === 0 ? (
              <div className="text-center text-gray-500 py-4">
                <p>最近のスキル更新はありません</p>
              </div>
            ) : (
              skillSummary.recentSkills.map((skill, index) => (
                <div key={skill.skill_item_id || index} className="flex items-center p-3 bg-gray-50 rounded-lg">
                  <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                    <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div className="ml-3 flex-1">
                    <p className="text-sm font-medium text-gray-900">
                      スキルレベル {getSkillLevelName(skill.skill_level || 1)} に更新
                    </p>
                    <p className="text-xs text-gray-500">
                      {skill.updated_at.toLocaleString('ja-JP')}
                    </p>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* 目標進捗 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            目標進捗
          </h2>
          <div className="space-y-6">
            {goalProgress.length === 0 ? (
              <div className="text-center text-gray-500 py-4">
                <p>進行中の目標はありません</p>
              </div>
            ) : (
              goalProgress.slice(0, 3).map((goal, index) => (
                <div key={index}>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-900">
                      {goal.goal_title || '目標'}
                    </span>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm font-semibold text-blue-600">
                        {goal.progress_rate || 0}%
                      </span>
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        goal.priority_level === 'HIGH' ? 'bg-red-100 text-red-800' :
                        goal.priority_level === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-blue-100 text-blue-800'
                      }`}>
                        {getPriorityLevelName(goal.priority_level || 'LOW')}
                      </span>
                    </div>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div 
                      className="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full transition-all duration-300" 
                      style={{ width: `${goal.progress_rate || 0}%` }}
                    ></div>
                  </div>
                  <div className="flex justify-between items-center mt-1">
                    <p className="text-xs text-gray-500">
                      {getAchievementStatusName(goal.achievement_status || 'PENDING')}
                    </p>
                    {goal.target_date && (
                      <p className="text-xs text-gray-500">
                        期限: {goal.target_date.toLocaleDateString('ja-JP')}
                      </p>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* スキルレベル分布 */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">
            スキルレベル分布
          </h2>
          <Button variant="outline" size="sm">
            詳細を見る
          </Button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600 mb-1">{skillSummary.levelCounts.level1}</div>
            <div className="text-sm text-gray-600">基礎レベル</div>
          </div>
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600 mb-1">{skillSummary.levelCounts.level2}</div>
            <div className="text-sm text-gray-600">応用レベル</div>
          </div>
          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <div className="text-2xl font-bold text-purple-600 mb-1">{skillSummary.levelCounts.level3}</div>
            <div className="text-sm text-gray-600">熟練レベル</div>
          </div>
          <div className="text-center p-4 bg-orange-50 rounded-lg">
            <div className="text-2xl font-bold text-orange-600 mb-1">{skillSummary.levelCounts.level4}</div>
            <div className="text-sm text-gray-600">専門レベル</div>
          </div>
        </div>
      </div>
    </main>
  );
}
