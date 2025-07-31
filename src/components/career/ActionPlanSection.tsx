/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: アクションプランセクションコンポーネント
 */

'use client';

import React, { useState, useEffect, useMemo } from 'react';
import { Button } from '@/components/ui/Button';
import { 
  PlusIcon, 
  PencilIcon, 
  TrashIcon, 
  CheckCircleIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  CalendarIcon
} from '@/components/ui/Icons';
import { ActionPlanItem, CareerGoalData } from '@/types/career';

/**
 * アクションプランセクションのプロパティ
 */
interface ActionPlanSectionProps {
  careerGoal: CareerGoalData | null;
  year: number;
  isLoading?: boolean;
}

/**
 * ステータス表示用の設定
 */
const STATUS_CONFIG = {
  '未着手': {
    color: 'bg-gray-100 text-gray-800',
    icon: ClockIcon,
  },
  '進行中': {
    color: 'bg-blue-100 text-blue-800',
    icon: ClockIcon,
  },
  '完了': {
    color: 'bg-green-100 text-green-800',
    icon: CheckCircleIcon,
  },
} as const;

/**
 * アクションプランセクションコンポーネント
 * 
 * 機能:
 * - アクションプランの一覧表示
 * - 新規追加・編集・削除
 * - ステータス変更
 * - 期限管理
 */
export function ActionPlanSection({ 
  careerGoal, 
  year,
  isLoading = false 
}: ActionPlanSectionProps) {
  const [filterStatus, setFilterStatus] = useState<ActionPlanItem['status'] | 'all'>('all');

  // careerGoalからアクションプランデータを生成
  const actionPlans: ActionPlanItem[] = useMemo(() => {
    if (!careerGoal) return [];

    // キャリア目標に基づいてアクションプランを動的生成
    const generateActionPlans = (): ActionPlanItem[] => {
      // careerGoalがnullの場合は空配列を返す
      if (!careerGoal) return [];
      
      // 型安全性を確保した値の取得
      const targetPosition: string = careerGoal?.target_position || 'キャリア目標';
      const targetDate: string = careerGoal?.target_date || '';
      const progressPercentage: number = careerGoal?.progress_percentage || 0;
      
      // 目標ポジションに基づく基本アクションプラン
      const baseActions = [
        {
          item: '研修受講',
          skill: 'リーダーシップ',
          description: 'リーダーシップスキルを習得するための研修を受講する',
          priority: 1
        },
        {
          item: 'プロジェクト管理経験の積み重ね',
          skill: 'プロジェクト管理',
          description: '実際のプロジェクトでリーダー役を担い、管理経験を積む',
          priority: 2
        },
        {
          item: 'チームマネジメント実践',
          skill: 'チームマネジメント',
          description: 'チームメンバーの指導・育成を通じてマネジメントスキルを向上させる',
          priority: 1
        },
        {
          item: '業界知識の習得',
          skill: '専門知識',
          description: '担当領域の専門知識を深め、業界トレンドをキャッチアップする',
          priority: 3
        },
        {
          item: 'ネットワーキング活動',
          skill: 'コミュニケーション',
          description: '社内外のネットワークを構築し、情報収集・協力関係を築く',
          priority: 2
        }
      ];

      // 進捗に基づいてステータスを決定
      const getStatusByProgress = (index: number): ActionPlanItem['status'] => {
        const progressThreshold = (index + 1) * (100 / baseActions.length);
        if (progressPercentage >= progressThreshold) return '完了';
        if (progressPercentage >= progressThreshold - 20) return '進行中';
        return '未着手';
      };

      // 期限を計算（目標日から逆算）
      const calculateDeadline = (index: number): string => {
        if (!targetDate) {
          // デフォルトの期限設定（今から3-12ヶ月後）
          const months = 3 + (index * 2);
          const deadline = new Date();
          deadline.setMonth(deadline.getMonth() + months);
          return deadline.toISOString().split('T')[0] || '';
        }
        
        // 目標日から逆算して期限を設定
        const targetDateObj = new Date(targetDate);
        const monthsBeforeTarget = baseActions.length - index;
        const deadline = new Date(targetDateObj);
        deadline.setMonth(deadline.getMonth() - monthsBeforeTarget);
        return deadline.toISOString().split('T')[0] || '';
      };

      return baseActions.map((action, index) => ({
        id: `action_${index + 1}`,
        item: action.item,
        skill: action.skill,
        description: action.description,
        deadline: calculateDeadline(index),
        status: getStatusByProgress(index),
        priority: action.priority
      }));
    };

    return generateActionPlans();
  }, [careerGoal, year]);

  // フィルタリング（安全にハンドリング）
  const filteredPlans = useMemo(() => 
    actionPlans.filter(plan => 
      filterStatus === 'all' || plan.status === filterStatus
    ), [actionPlans, filterStatus]
  );

  // ハンドラー関数（モック）
  const handleAdd = () => {
    console.log('アクションプラン追加');
  };

  const handleEdit = (plan: ActionPlanItem) => {
    console.log('アクションプラン編集:', plan);
  };

  const handleDelete = (plan: ActionPlanItem) => {
    console.log('アクションプラン削除:', plan);
  };

  const handleStatusChange = (planId: string, status: ActionPlanItem['status']) => {
    console.log('ステータス変更:', planId, status);
  };

  /**
   * 期限までの日数を計算
   */
  const getDaysUntilDeadline = (deadline: string) => {
    const today = new Date();
    const deadlineDate = new Date(deadline);
    const diffTime = deadlineDate.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };

  /**
   * 期限表示の色を取得
   */
  const getDeadlineColor = (days: number) => {
    if (days < 0) return 'text-red-600';
    if (days <= 3) return 'text-orange-600';
    if (days <= 7) return 'text-yellow-600';
    return 'text-green-600';
  };

  // ローディング表示
  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, index) => (
          <div key={index} className="animate-pulse">
            <div className="bg-gray-200 rounded-lg h-24"></div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* ヘッダー */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium text-gray-900">アクションプラン</h3>
        <Button
          onClick={handleAdd}
          className="flex items-center space-x-2"
        >
          <PlusIcon className="h-4 w-4" />
          <span>新規追加</span>
        </Button>
      </div>

      {/* フィルター */}
      <div className="flex items-center space-x-4">
        <label htmlFor="status-filter" className="text-sm font-medium text-gray-700">
          ステータス:
        </label>
        <select
          id="status-filter"
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value as ActionPlanItem['status'] | 'all')}
          className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="all">すべて</option>
          <option value="未着手">未着手</option>
          <option value="進行中">進行中</option>
          <option value="完了">完了</option>
        </select>
      </div>

      {/* アクションプラン一覧 */}
      {filteredPlans.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            {filterStatus === 'all' ? 'アクションプランがありません' : `${filterStatus}のプランがありません`}
          </h3>
          <p className="text-sm text-gray-500">
            新しいアクションプランを追加して、目標達成に向けた具体的な行動を計画しましょう。
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredPlans.map((plan) => {
            const StatusIcon = STATUS_CONFIG[plan.status]?.icon || ClockIcon;
            const daysUntilDeadline = getDaysUntilDeadline(plan.deadline);

            return (
              <div
                key={plan.id}
                className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    {/* タイトルとステータス */}
                    <div className="flex items-center space-x-3 mb-2">
                      <h4 className="text-base font-medium text-gray-900 truncate">
                        {plan.item}
                      </h4>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${STATUS_CONFIG[plan.status]?.color}`}>
                        <StatusIcon className="h-3 w-3 mr-1" />
                        {plan.status}
                      </span>
                    </div>

                    {/* スキル */}
                    <div className="text-sm text-gray-600 mb-2">
                      <span className="font-medium">関連スキル:</span> {plan.skill}
                    </div>

                    {/* 説明 */}
                    {plan.description && (
                      <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                        {plan.description}
                      </p>
                    )}

                    {/* 期限情報 */}
                    <div className="flex items-center space-x-4 text-sm">
                      <div className="flex items-center space-x-1">
                        <CalendarIcon className="h-4 w-4 text-gray-400" />
                        <span className="text-gray-600">
                          期限: {new Date(plan.deadline).toLocaleDateString('ja-JP')}
                        </span>
                      </div>
                      <span className={`font-medium ${getDeadlineColor(daysUntilDeadline)}`}>
                        {daysUntilDeadline > 0 
                          ? `あと${daysUntilDeadline}日`
                          : daysUntilDeadline === 0
                          ? '今日が期限'
                          : `${Math.abs(daysUntilDeadline)}日経過`
                        }
                      </span>
                    </div>
                  </div>

                  {/* アクションボタン */}
                  <div className="flex items-center space-x-2 ml-4">
                    {/* ステータス変更ボタン */}
                    {plan.status !== '完了' && (
                      <select
                        value={plan.status}
                        onChange={(e) => handleStatusChange(plan.id, e.target.value as ActionPlanItem['status'])}
                        className="border border-gray-300 rounded-md px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="未着手">未着手</option>
                        <option value="進行中">進行中</option>
                        <option value="完了">完了</option>
                      </select>
                    )}
                    
                    <Button
                      variant="secondary"
                      size="sm"
                      onClick={() => handleEdit(plan)}
                      className="flex items-center space-x-1"
                    >
                      <PencilIcon className="h-4 w-4" />
                      <span>編集</span>
                    </Button>
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => handleDelete(plan)}
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
      )}

      {/* 統計情報 */}
      {actionPlans.length > 0 && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-900 mb-3">進捗統計</h4>
          <div className="grid grid-cols-3 gap-4">
            {Object.keys(STATUS_CONFIG).map((status) => {
              const count = actionPlans.filter(plan => plan.status === status).length;
              const percentage = actionPlans.length > 0 ? Math.round((count / actionPlans.length) * 100) : 0;
              return (
                <div key={status} className="text-center">
                  <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${STATUS_CONFIG[status as keyof typeof STATUS_CONFIG].color} mb-1`}>
                    {status}
                  </div>
                  <div className="text-lg font-semibold text-gray-900">{count}</div>
                  <div className="text-xs text-gray-500">{percentage}%</div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
