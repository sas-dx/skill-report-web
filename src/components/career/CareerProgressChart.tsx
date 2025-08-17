/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: キャリア進捗チャートコンポーネント
 */

'use client';

import React, { useMemo } from 'react';
import { CareerGoal } from '@/types/career';
import { 
  CheckCircleIcon, 
  ClockIcon, 
  ExclamationTriangleIcon,
  XCircleIcon,
  FlagIcon
} from '@/components/ui/Icons';

interface CareerProgressChartProps {
  goals: CareerGoal[];
  year: number;
}

/**
 * キャリア進捗チャートコンポーネント
 * 年度の全目標を集計し、個別の進捗も表示
 */
export function CareerProgressChart({ goals, year }: CareerProgressChartProps) {
  // 全体の進捗率を計算
  const overallProgress = useMemo(() => {
    if (goals.length === 0) return 0;
    
    const totalProgress = goals.reduce((sum, goal) => {
      return sum + (goal.progress_percentage || 0);
    }, 0);
    
    return Math.round(totalProgress / goals.length);
  }, [goals]);

  // ステータス別の目標数を集計
  const statusCounts = useMemo(() => {
    return goals.reduce((counts, goal) => {
      const status = goal.status || 'not_started';
      counts[status] = (counts[status] || 0) + 1;
      return counts;
    }, {} as Record<string, number>);
  }, [goals]);

  // ステータスごとの表示設定
  const statusConfig: Record<string, { label: string; color: string; icon: any }> = {
    not_started: { label: '未着手', color: 'bg-gray-200', icon: ClockIcon },
    NOT_STARTED: { label: '未着手', color: 'bg-gray-200', icon: ClockIcon },
    in_progress: { label: '進行中', color: 'bg-blue-500', icon: ClockIcon },
    IN_PROGRESS: { label: '進行中', color: 'bg-blue-500', icon: ClockIcon },
    completed: { label: '完了', color: 'bg-green-500', icon: CheckCircleIcon },
    COMPLETED: { label: '完了', color: 'bg-green-500', icon: CheckCircleIcon },
    postponed: { label: '延期', color: 'bg-yellow-500', icon: ExclamationTriangleIcon },
    POSTPONED: { label: '延期', color: 'bg-yellow-500', icon: ExclamationTriangleIcon },
    cancelled: { label: '中止', color: 'bg-red-500', icon: XCircleIcon },
    CANCELLED: { label: '中止', color: 'bg-red-500', icon: XCircleIcon }
  };

  // 進捗バーの色を決定
  const getProgressBarColor = (percentage: number) => {
    if (percentage >= 80) return 'bg-green-500';
    if (percentage >= 60) return 'bg-blue-500';
    if (percentage >= 40) return 'bg-yellow-500';
    if (percentage >= 20) return 'bg-orange-500';
    return 'bg-red-500';
  };

  // 個別目標の進捗バーの色
  const getGoalProgressColor = (goal: CareerGoal) => {
    const status = goal.status?.toLowerCase();
    if (status === 'completed') return 'bg-green-500';
    if (status === 'cancelled') return 'bg-gray-400';
    if (status === 'postponed') return 'bg-yellow-500';
    return getProgressBarColor(goal.progress_percentage || 0);
  };

  if (goals.length === 0) {
    return (
      <div className="text-center py-12">
        <FlagIcon className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">
          {year}年度の目標がありません
        </h3>
        <p className="mt-1 text-sm text-gray-500">
          新しい目標を追加して、進捗管理を始めましょう。
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* ヘッダー */}
      <div className="text-center">
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          {year}年度 キャリア進捗状況
        </h3>
        <p className="text-sm text-gray-600">
          {goals.length}個の目標の進捗を管理中
        </p>
      </div>

      {/* 全体進捗 */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h4 className="text-lg font-semibold text-gray-900 mb-4">全体進捗率</h4>
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-gray-600">平均進捗率</span>
            <span className="font-bold text-lg">{overallProgress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-4">
            <div 
              className={`h-4 rounded-full transition-all duration-500 ${getProgressBarColor(overallProgress)}`}
              style={{ width: `${overallProgress}%` }}
            />
          </div>
        </div>

        {/* ステータス別サマリー */}
        <div className="mt-6 grid grid-cols-2 md:grid-cols-5 gap-4">
          {Object.entries(statusConfig)
            .filter(([status]) => status === status.toLowerCase()) // 小文字のキーのみ表示
            .map(([status, config]) => {
            const count = (statusCounts[status] || 0) + (statusCounts[status.toUpperCase()] || 0);
            const Icon = config.icon;
            return (
              <div key={status} className="text-center">
                <div className={`inline-flex items-center justify-center w-10 h-10 rounded-full ${config.color} bg-opacity-20 mb-2`}>
                  <Icon className={`h-5 w-5 ${config.color.replace('bg-', 'text-')}`} />
                </div>
                <div className="text-2xl font-bold text-gray-900">{count}</div>
                <div className="text-xs text-gray-600">{config.label}</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 個別目標の進捗 */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h4 className="text-lg font-semibold text-gray-900 mb-4">個別目標の進捗</h4>
        <div className="space-y-4">
          {goals.map((goal, index) => (
            <div key={goal.id || index} className="border-b border-gray-100 last:border-b-0 pb-4 last:pb-0">
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <h5 className="font-medium text-gray-900">{goal.title}</h5>
                  <div className="flex items-center space-x-4 mt-1">
                    <span className="text-xs text-gray-500">
                      タイプ: {goal.goal_type === 'short_term' ? '短期' : 
                              goal.goal_type === 'mid_term' ? '中期' : '長期'}
                    </span>
                    {goal.target_date && (
                      <span className="text-xs text-gray-500">
                        期限: {new Date(goal.target_date).toLocaleDateString('ja-JP')}
                      </span>
                    )}
                    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium
                      ${goal.status === 'completed' || goal.status === 'COMPLETED' ? 'bg-green-100 text-green-800' :
                        goal.status === 'in_progress' || goal.status === 'IN_PROGRESS' ? 'bg-blue-100 text-blue-800' :
                        goal.status === 'postponed' || goal.status === 'POSTPONED' ? 'bg-yellow-100 text-yellow-800' :
                        goal.status === 'cancelled' || goal.status === 'CANCELLED' ? 'bg-red-100 text-red-800' :
                        'bg-gray-100 text-gray-800'}`}>
                      {(statusConfig[goal.status || 'not_started'] || statusConfig['not_started']).label}
                    </span>
                  </div>
                </div>
                <div className="text-right ml-4">
                  <div className="text-2xl font-bold text-gray-900">
                    {goal.progress_percentage || 0}%
                  </div>
                </div>
              </div>
              
              {/* 個別進捗バー */}
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full transition-all duration-300 ${getGoalProgressColor(goal)}`}
                  style={{ width: `${goal.progress_percentage || 0}%` }}
                />
              </div>

              {/* 説明がある場合は表示 */}
              {goal.description && (
                <p className="mt-2 text-sm text-gray-600">{goal.description}</p>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* 進捗分析 */}
      <div className="bg-blue-50 rounded-lg p-4">
        <h4 className="text-sm font-semibold text-blue-900 mb-2">進捗分析</h4>
        <ul className="space-y-1 text-sm text-blue-800">
          {statusCounts.completed > 0 && (
            <li>✓ {statusCounts.completed}個の目標が完了しています</li>
          )}
          {statusCounts.in_progress > 0 && (
            <li>→ {statusCounts.in_progress}個の目標が進行中です</li>
          )}
          {statusCounts.not_started > 0 && (
            <li>○ {statusCounts.not_started}個の目標が未着手です</li>
          )}
          {overallProgress >= 70 && (
            <li>★ 全体の進捗は順調です！このペースを維持しましょう</li>
          )}
          {overallProgress < 30 && goals.length > 0 && (
            <li>⚠ 進捗が遅れています。計画の見直しを検討してください</li>
          )}
        </ul>
      </div>
    </div>
  );
}