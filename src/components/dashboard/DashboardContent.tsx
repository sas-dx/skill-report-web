// PLT.1-WEB.1: ダッシュボードメインコンテンツコンポーネント（DB連携版）
'use client';

import React from 'react';
import { Button } from '@/components/ui/Button';
import { SubordinatesSection } from '@/components/profile/SubordinatesSection';
import { useDashboard } from '@/hooks/useDashboard';
import { useRouter } from 'next/navigation';

interface DashboardContentProps {
  userName: string;
}

export const DashboardContent: React.FC<DashboardContentProps> = ({
  userName
}) => {
  const router = useRouter();
  const { data, isLoading, error, refresh } = useDashboard();
  const [subordinates, setSubordinates] = React.useState<any[]>([]);

  const handleAddSubordinate = () => {
    console.log('部下追加');
  };

  const handleEditSubordinate = (subordinate: any) => {
    console.log('部下編集:', subordinate);
  };

  const handleRemoveSubordinate = async (employeeId: string) => {
    console.log('部下削除:', employeeId);
  };

  // ローディング中の表示
  if (isLoading) {
    return (
      <main className="p-6 space-y-6">
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg p-6 text-white animate-pulse">
          <div className="h-8 bg-white/20 rounded w-1/3 mb-2"></div>
          <div className="h-4 bg-white/20 rounded w-2/3"></div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 animate-pulse">
              <div className="h-12 bg-gray-200 rounded mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      </main>
    );
  }

  // エラー時の表示
  if (error) {
    return (
      <main className="p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <Button onClick={refresh}>再読み込み</Button>
        </div>
      </main>
    );
  }

  // データが取得できなかった場合
  if (!data) {
    return (
      <main className="p-6">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
          <p className="text-yellow-600 mb-4">データを取得できませんでした</p>
          <Button onClick={refresh}>再読み込み</Button>
        </div>
      </main>
    );
  }

  // 通知の色を決定する関数
  const getNotificationColor = (type: string) => {
    switch(type) {
      case 'error': return 'red';
      case 'warning': return 'yellow';
      case 'success': return 'green';
      default: return 'blue';
    }
  };

  // タスクの優先度の色を決定する関数
  const getTaskPriorityColor = (priority: string) => {
    switch(priority) {
      case 'high': return 'red';
      case 'medium': return 'yellow';
      default: return 'green';
    }
  };

  return (
    <main className="p-6 space-y-6">
      {/* ウェルカムセクション */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">
          おかえりなさい、{data.user_info.name}さん
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
              <p className="text-3xl font-bold text-gray-900 mt-2">{data.skill_summary.total_skills}</p>
              <p className="text-sm text-green-600 mt-1">+{data.skill_summary.recent_updates.length} 最近更新</p>
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
              <p className="text-3xl font-bold text-gray-900 mt-2">{data.goal_summary.overall_progress}%</p>
              <p className="text-sm text-blue-600 mt-1">{data.goal_summary.current_goals}個の進行中</p>
            </div>
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
          </div>
        </div>

        {/* 資格取得数 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">資格取得数</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{data.certification_summary.total_certifications}</p>
              <p className="text-sm text-purple-600 mt-1">{data.certification_summary.active_certifications}個が有効</p>
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
              <p className="text-sm font-medium text-gray-600">今月の作業時間</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{data.work_summary.monthly_hours.total}</p>
              <p className="text-sm text-orange-600 mt-1">時間</p>
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
                <Button size="sm" className="w-full" onClick={() => router.push('/skills')}>
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
                <Button variant="outline" size="sm" className="w-full" onClick={() => router.push('/profile')}>
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
                <Button variant="outline" size="sm" className="w-full" onClick={() => router.push('/career')}>
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
                <Button variant="outline" size="sm" className="w-full" onClick={() => router.push('/reports')}>
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
              {data.notifications.filter(n => !n.is_read).length}件
            </span>
          </div>
          <div className="space-y-4">
            {data.notifications.slice(0, 3).map((notification) => {
              const color = getNotificationColor(notification.type);
              return (
                <div key={notification.notification_id} className={`flex items-start p-3 bg-${color}-50 rounded-lg border-l-4 border-${color}-400`}>
                  <div className={`w-2 h-2 bg-${color}-500 rounded-full mt-2 mr-3 flex-shrink-0`}></div>
                  <div className="flex-1">
                    <p className="text-sm text-gray-900 font-medium">
                      {notification.title}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      {new Date(notification.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              );
            })}
            {data.notifications.length === 0 && (
              <p className="text-sm text-gray-500 text-center py-4">新しい通知はありません</p>
            )}
          </div>
          <Button variant="outline" size="sm" className="w-full mt-4" onClick={() => router.push('/notifications')}>
            すべての通知を見る
          </Button>
        </div>
      </div>

      {/* 最近の活動・進捗状況 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 最近の活動 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            最近のタスク
          </h2>
          <div className="space-y-4">
            {data.tasks.slice(0, 3).map((task) => {
              const color = getTaskPriorityColor(task.priority);
              return (
                <div key={task.task_id} className="flex items-center p-3 bg-gray-50 rounded-lg">
                  <div className={`w-10 h-10 bg-${color}-100 rounded-full flex items-center justify-center`}>
                    <svg className={`w-5 h-5 text-${color}-600`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                  </div>
                  <div className="ml-3 flex-1">
                    <p className="text-sm font-medium text-gray-900">{task.title}</p>
                    <p className="text-xs text-gray-500">
                      {task.due_date ? `期限: ${new Date(task.due_date).toLocaleDateString()}` : 'タスク'}
                    </p>
                  </div>
                </div>
              );
            })}
            {data.tasks.length === 0 && (
              <p className="text-sm text-gray-500 text-center py-4">未完了のタスクはありません</p>
            )}
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
                <span className="text-sm font-semibold text-blue-600">{data.goal_summary.overall_progress}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div className="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full transition-all duration-300" style={{ width: `${data.goal_summary.overall_progress}%` }}></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">目標まであと{100 - data.goal_summary.overall_progress}%</p>
            </div>

            {/* スキル習得進捗 */}
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-900">スキル習得</span>
                <span className="text-sm font-semibold text-green-600">
                  {data.skill_summary.total_skills > 0 
                    ? Math.round((data.skill_summary.skills_by_level.intermediate + data.skill_summary.skills_by_level.advanced) / data.skill_summary.total_skills * 100)
                    : 0}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div className="bg-gradient-to-r from-green-500 to-green-600 h-3 rounded-full transition-all duration-300" style={{ 
                  width: `${data.skill_summary.total_skills > 0 
                    ? Math.round((data.skill_summary.skills_by_level.intermediate + data.skill_summary.skills_by_level.advanced) / data.skill_summary.total_skills * 100)
                    : 0}%` 
                }}></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">
                {data.skill_summary.skills_by_level.intermediate + data.skill_summary.skills_by_level.advanced}/{data.skill_summary.total_skills} スキル習得済み
              </p>
            </div>

            {/* 資格取得進捗 */}
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-900">有効資格</span>
                <span className="text-sm font-semibold text-purple-600">
                  {data.certification_summary.active_certifications}/{data.certification_summary.total_certifications}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div className="bg-gradient-to-r from-purple-500 to-purple-600 h-3 rounded-full transition-all duration-300" style={{ 
                  width: `${data.certification_summary.total_certifications > 0 ? 
                    (data.certification_summary.active_certifications / data.certification_summary.total_certifications * 100) : 0}%` 
                }}></div>
              </div>
              {data.certification_summary.expiring_soon.length > 0 && (
                <p className="text-xs text-gray-500 mt-1">
                  {data.certification_summary.expiring_soon.length}個が期限切れ間近
                </p>
              )}
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
          <Button variant="outline" size="sm" onClick={() => router.push('/skills')}>
            詳細を見る
          </Button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {data.skill_summary.skills_by_category.slice(0, 3).map((category, index) => {
            const colors = ['blue', 'green', 'purple'];
            const color = colors[index % colors.length];
            return (
              <div key={category.category_id} className={`text-center p-4 bg-${color}-50 rounded-lg`}>
                <div className={`text-2xl font-bold text-${color}-600 mb-1`}>{category.count}</div>
                <div className="text-sm text-gray-600">{category.category_name}</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 部下情報セクション */}
      {data.team_summary && (
        <SubordinatesSection
          subordinates={subordinates}
          isManager={true}
          onAddSubordinate={handleAddSubordinate}
          onEditSubordinate={handleEditSubordinate}
          onRemoveSubordinate={handleRemoveSubordinate}
        />
      )}

      {/* 推奨事項セクション */}
      {data.recommendations.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            推奨アクション
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.recommendations.map((rec, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-medium text-gray-900 mb-1">{rec.title}</h3>
                    <p className="text-sm text-gray-600 mb-3">{rec.description}</p>
                  </div>
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                    rec.priority === 'high' ? 'bg-red-100 text-red-800' :
                    rec.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {rec.priority === 'high' ? '高' : rec.priority === 'medium' ? '中' : '低'}
                  </span>
                </div>
                <Button 
                  size="sm" 
                  variant="outline" 
                  className="w-full"
                  onClick={() => router.push(rec.action_url)}
                >
                  {rec.action_label}
                </Button>
              </div>
            ))}
          </div>
        </div>
      )}
    </main>
  );
};