/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: キャリア目標一覧表示コンポーネント
 */

'use client';

import React, { useState, useMemo } from 'react';
import { Button } from '@/components/ui/Button';
import { 
  PencilIcon, 
  TrashIcon, 
  CalendarIcon,
  FlagIcon,
  CheckCircleIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  XCircleIcon
} from '@/components/ui/Icons';
import { 
  CareerGoal, 
  CareerGoalData, 
  CareerGoalStatus,
  CareerGoalPriority 
} from '@/types/career';

/**
 * キャリア目標一覧のプロパティ
 */
interface CareerGoalListProps {
  careerGoal: CareerGoalData | null;
  onEdit: (goal: CareerGoal) => void;
  onDelete: (goal: CareerGoal) => void;
  isLoading?: boolean;
}

/**
 * ステータス表示用の設定
 */
const STATUS_CONFIG = {
  not_started: {
    label: '未着手',
    color: 'bg-gray-100 text-gray-800',
    icon: ClockIcon,
  },
  in_progress: {
    label: '進行中',
    color: 'bg-blue-100 text-blue-800',
    icon: ClockIcon,
  },
  completed: {
    label: '完了',
    color: 'bg-green-100 text-green-800',
    icon: CheckCircleIcon,
  },
  postponed: {
    label: '延期',
    color: 'bg-yellow-100 text-yellow-800',
    icon: ExclamationTriangleIcon,
  },
  cancelled: {
    label: '中止',
    color: 'bg-red-100 text-red-800',
    icon: XCircleIcon,
  },
} as const;

/**
 * 優先度表示用の設定
 */
const PRIORITY_CONFIG = {
  1: { label: '高', color: 'text-red-600' },
  2: { label: '中', color: 'text-yellow-600' },
  3: { label: '低', color: 'text-green-600' },
} as const;

/**
 * キャリア目標一覧表示コンポーネント
 * 
 * 機能:
 * - 目標の一覧表示
 * - ステータス別フィルタリング
 * - 優先度別ソート
 * - 編集・削除アクション
 * - 進捗率の視覚的表示
 */
export function CareerGoalList({ 
  careerGoal, 
  onEdit, 
  onDelete, 
  isLoading = false 
}: CareerGoalListProps) {
  const [filterStatus, setFilterStatus] = useState<CareerGoalStatus | 'all'>('all');
  const [sortBy, setSortBy] = useState<'priority' | 'target_date' | 'created_at'>('priority');

  /**
   * plan_statusをCareerGoalStatusに変換
   */
  const mapPlanStatusToCareerStatus = (planStatus?: string): CareerGoalStatus => {
    switch (planStatus) {
      case 'ACTIVE':
        return 'in_progress';
      case 'COMPLETED':
        return 'completed';
      case 'INACTIVE':
        return 'postponed';
      default:
        return 'not_started';
    }
  };

  /**
   * 進捗率に基づく優先度の推定
   */
  const estimatePriority = (progressPercentage: number): CareerGoalPriority => {
    if (progressPercentage >= 80) return 1; // 高優先度（完了間近）
    if (progressPercentage >= 40) return 2; // 中優先度（進行中）
    return 3; // 低優先度（開始段階）
  };

  // CareerGoalDataからCareerGoal配列を生成
  const convertedGoals: CareerGoal[] = useMemo(() => {
    if (!careerGoal) return [];

    // CareerGoalDataからCareerGoalに変換
    const convertedGoal: CareerGoal = {
      id: careerGoal.id || `goal_${Date.now()}`,
      goal_id: careerGoal.id || `goal_${Date.now()}`, // goal_idを追加
      user_id: 'current_user', // 実際のユーザーIDは親コンポーネントから取得
      title: careerGoal.target_position || '',
      description: careerGoal.target_description || '',
      goal_type: careerGoal.goal_type || 'mid_term', // goal_typeを追加（デフォルト値設定）
      status: mapPlanStatusToCareerStatus(careerGoal.plan_status),
      priority: estimatePriority(careerGoal.progress_percentage || 0),
      progress_percentage: careerGoal.progress_percentage || 0,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      ...(careerGoal.target_date && { target_date: careerGoal.target_date }), // 条件付きでプロパティを追加
    };

    return [convertedGoal];
  }, [careerGoal]);

  // フィルタリングとソート
  const filteredAndSortedGoals = useMemo(() => {
    let filtered = convertedGoals;

    // ステータスフィルタリング
    if (filterStatus !== 'all') {
      filtered = filtered.filter((goal: CareerGoal) => goal.status === filterStatus);
    }

    // ソート
    filtered.sort((a: CareerGoal, b: CareerGoal) => {
      switch (sortBy) {
        case 'priority':
          return a.priority - b.priority;
        case 'target_date':
          return new Date(a.target_date || '').getTime() - new Date(b.target_date || '').getTime();
        case 'created_at':
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
        default:
          return 0;
      }
    });

    return filtered;
  }, [convertedGoals, filterStatus, sortBy]);

  /**
   * 進捗バーの色を取得
   */
  const getProgressColor = (percentage: number) => {
    if (percentage >= 80) return 'bg-green-500';
    if (percentage >= 50) return 'bg-blue-500';
    if (percentage >= 20) return 'bg-yellow-500';
    return 'bg-gray-300';
  };

  /**
   * 期限までの日数を計算
   */
  const getDaysUntilDeadline = (targetDate?: string) => {
    if (!targetDate) return null;
    const today = new Date();
    const deadline = new Date(targetDate);
    const diffTime = deadline.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };

  /**
   * 期限表示の色を取得
   */
  const getDeadlineColor = (days: number | null) => {
    if (days === null) return 'text-gray-500';
    if (days < 0) return 'text-red-600';
    if (days <= 7) return 'text-orange-600';
    if (days <= 30) return 'text-yellow-600';
    return 'text-green-600';
  };

  // ローディング表示
  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, index) => (
          <div key={index} className="animate-pulse">
            <div className="bg-gray-200 rounded-lg h-32"></div>
          </div>
        ))}
      </div>
    );
  }

  // 目標が存在しない場合
  if (filteredAndSortedGoals.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="mx-auto h-12 w-12 text-gray-400">
          <FlagIcon className="h-12 w-12" />
        </div>
        <h3 className="mt-2 text-sm font-medium text-gray-900">
          {filterStatus === 'all' ? 'キャリア目標がありません' : `${STATUS_CONFIG[filterStatus as keyof typeof STATUS_CONFIG]?.label}の目標がありません`}
        </h3>
        <p className="mt-1 text-sm text-gray-500">
          新しい目標を追加して、キャリアプランを始めましょう。
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* フィルター・ソートコントロール */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-3 sm:space-y-0">
        <div className="flex items-center space-x-4">
          {/* ステータスフィルター */}
          <div className="flex items-center space-x-2">
            <label htmlFor="status-filter" className="text-sm font-medium text-gray-700">
              ステータス:
            </label>
            <select
              id="status-filter"
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value as CareerGoalStatus | 'all')}
              className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">すべて</option>
              {Object.entries(STATUS_CONFIG).map(([status, config]) => (
                <option key={status} value={status}>
                  {config.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <label htmlFor="sort-by" className="text-sm font-medium text-gray-700">
            並び順:
          </label>
          <select
            id="sort-by"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as 'priority' | 'target_date' | 'created_at')}
            className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="priority">優先度順</option>
            <option value="target_date">期限順</option>
            <option value="created_at">作成日順</option>
          </select>
        </div>
      </div>

      {/* 目標一覧 */}
      <div className="space-y-4">
        {filteredAndSortedGoals.map((goal) => {
          const StatusIcon = STATUS_CONFIG[goal.status]?.icon || ClockIcon;
          const daysUntilDeadline = getDaysUntilDeadline(goal.target_date);

          return (
            <div
              key={goal.id}
              className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow duration-200"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  {/* タイトルとステータス */}
                  <div className="flex items-center space-x-3 mb-2">
                    <h3 className="text-lg font-medium text-gray-900 truncate">
                      {goal.title}
                    </h3>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${STATUS_CONFIG[goal.status]?.color}`}>
                      <StatusIcon className="h-3 w-3 mr-1" />
                      {STATUS_CONFIG[goal.status]?.label}
                    </span>
                    <span className={`inline-flex items-center text-xs font-medium ${PRIORITY_CONFIG[goal.priority]?.color}`}>
                      <FlagIcon className="h-3 w-3 mr-1" />
                      優先度: {PRIORITY_CONFIG[goal.priority]?.label}
                    </span>
                  </div>

                  {/* 説明 */}
                  {goal.description && (
                    <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                      {goal.description}
                    </p>
                  )}

                  {/* 進捗バー */}
                  <div className="mb-3">
                    <div className="flex items-center justify-between text-sm text-gray-600 mb-1">
                      <span>進捗状況</span>
                      <span>{goal.progress_percentage}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(goal.progress_percentage)}`}
                        style={{ width: `${goal.progress_percentage}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* 期限情報 */}
                  {goal.target_date && (
                    <div className="flex items-center space-x-4 text-sm">
                      <div className="flex items-center space-x-1">
                        <CalendarIcon className="h-4 w-4 text-gray-400" />
                        <span className="text-gray-600">
                          目標日: {goal.target_date ? new Date(goal.target_date).toLocaleDateString('ja-JP') : '未設定'}
                        </span>
                      </div>
                      {daysUntilDeadline !== null && (
                        <span className={`font-medium ${getDeadlineColor(daysUntilDeadline)}`}>
                          {daysUntilDeadline > 0 
                            ? `あと${daysUntilDeadline}日`
                            : daysUntilDeadline === 0
                            ? '今日が期限'
                            : `${Math.abs(daysUntilDeadline)}日経過`
                          }
                        </span>
                      )}
                    </div>
                  )}
                </div>

                {/* アクションボタン */}
                <div className="flex items-center space-x-2 ml-4">
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => onEdit(goal)}
                    className="flex items-center space-x-1"
                  >
                    <PencilIcon className="h-4 w-4" />
                    <span>編集</span>
                  </Button>
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => onDelete(goal)}
                    className="flex items-center space-x-1"
                  >
                    <TrashIcon className="h-4 w-4" />
                    <span>削除</span>
                  </Button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* 統計情報 */}
      <div className="bg-gray-50 rounded-lg p-4">
        <h4 className="text-sm font-medium text-gray-900 mb-3">目標統計</h4>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {Object.entries(STATUS_CONFIG).map(([status, config]) => {
            const count = convertedGoals.filter((goal: CareerGoal) => goal.status === status).length;
            return (
              <div key={status} className="text-center">
                <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${config.color} mb-1`}>
                  {config.label}
                </div>
                <div className="text-lg font-semibold text-gray-900">{count}</div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
