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
  CalendarIcon,
  XIcon
} from '@/components/ui/Icons';
import { 
  ActionPlan, 
  ActionPlanCreateRequest, 
  ActionPlanUpdateRequest, 
  CareerGoalData 
} from '@/types/career';
import { ActionPlanForm } from './ActionPlanForm';

/**
 * アクションプランセクションのプロパティ
 */
interface ActionPlanSectionProps {
  careerGoal: CareerGoalData | null;
  year: number;
  isLoading?: boolean;
  userId?: string;
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
  isLoading = false,
  userId
}: ActionPlanSectionProps) {
  const [filterStatus, setFilterStatus] = useState<'not_started' | 'in_progress' | 'completed' | 'all'>('all');
  const [actionPlans, setActionPlans] = useState<ActionPlan[]>([]);
  const [apiLoading, setApiLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingPlan, setEditingPlan] = useState<ActionPlan | null>(null);

  /**
   * アクションプラン一覧を取得
   */
  const fetchActionPlans = async () => {
    try {
      setApiLoading(true);
      setError(null);

      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      if (userId) {
        headers['x-user-id'] = userId;
      }

      const response = await fetch('/api/career/action-plans', {
        method: 'GET',
        headers,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.success && data.data) {
        setActionPlans(data.data.action_plans || []);
      } else {
        throw new Error(data.error?.message || 'アクションプランの取得に失敗しました');
      }

    } catch (err) {
      console.error('アクションプラン取得エラー:', err);
      setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
    } finally {
      setApiLoading(false);
    }
  };

  useEffect(() => {
    fetchActionPlans();
  }, [userId, year]);

  // フィルタリング
  const filteredPlans = useMemo(() => 
    actionPlans.filter(plan => 
      filterStatus === 'all' || plan.status === filterStatus
    ), [actionPlans, filterStatus]
  );

  // ステータス表示マッピング
  const getStatusDisplay = (status: string): string => {
    switch (status) {
      case 'not_started': return '未着手';
      case 'in_progress': return '進行中';
      case 'completed': return '完了';
      default: return status;
    }
  };

  const getStatusColor = (status: string): string => {
    switch (status) {
      case 'not_started': return 'bg-gray-100 text-gray-800';
      case 'in_progress': return 'bg-blue-100 text-blue-800';
      case 'completed': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  /**
   * アクションプラン追加
   */
  const handleAdd = () => {
    setEditingPlan(null);
    setIsDialogOpen(true);
  };

  /**
   * アクションプラン編集
   */
  const handleEdit = (plan: ActionPlan) => {
    setEditingPlan(plan);
    setIsDialogOpen(true);
  };

  /**
   * アクションプラン削除
   */
  const handleDelete = async (plan: ActionPlan) => {
    if (!window.confirm('このアクションプランを削除してもよろしいですか？')) {
      return;
    }

    try {
      setApiLoading(true);
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      if (userId) {
        headers['x-user-id'] = userId;
      }

      const response = await fetch(`/api/career/action-plan/${plan.action_id}`, {
        method: 'DELETE',
        headers,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      if (data.success) {
        await fetchActionPlans(); // リストを再取得
      } else {
        throw new Error(data.error?.message || 'アクションプランの削除に失敗しました');
      }

    } catch (err) {
      console.error('アクションプラン削除エラー:', err);
      setError(err instanceof Error ? err.message : '削除に失敗しました');
    } finally {
      setApiLoading(false);
    }
  };

  /**
   * ステータス変更
   */
  const handleStatusChange = async (planId: string, status: 'not_started' | 'in_progress' | 'completed') => {
    try {
      setApiLoading(true);
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      if (userId) {
        headers['x-user-id'] = userId;
      }

      const updateData: ActionPlanUpdateRequest = {
        status,
        ...(status === 'completed' && { completed_date: new Date().toISOString().split('T')[0] })
      };

      const response = await fetch(`/api/career/action-plan/${planId}`, {
        method: 'PUT',
        headers,
        body: JSON.stringify(updateData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      if (data.success) {
        await fetchActionPlans(); // リストを再取得
      } else {
        throw new Error(data.error?.message || 'ステータスの更新に失敗しました');
      }

    } catch (err) {
      console.error('ステータス更新エラー:', err);
      setError(err instanceof Error ? err.message : 'ステータス更新に失敗しました');
    } finally {
      setApiLoading(false);
    }
  };

  /**
   * フォーム送信処理
   */
  const handleSubmit = async (formData: ActionPlanCreateRequest) => {
    try {
      setApiLoading(true);
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      if (userId) {
        headers['x-user-id'] = userId;
      }

      let response;
      if (editingPlan) {
        // 更新
        response = await fetch(`/api/career/action-plan/${editingPlan.action_id}`, {
          method: 'PUT',
          headers,
          body: JSON.stringify(formData),
        });
      } else {
        // 新規追加
        response = await fetch('/api/career/action-plans', {
          method: 'POST',
          headers,
          body: JSON.stringify(formData),
        });
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      if (data.success) {
        setIsDialogOpen(false);
        setEditingPlan(null);
        await fetchActionPlans(); // リストを再取得
      } else {
        throw new Error(data.error?.message || '保存に失敗しました');
      }

    } catch (err) {
      console.error('保存エラー:', err);
      setError(err instanceof Error ? err.message : '保存に失敗しました');
    } finally {
      setApiLoading(false);
    }
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
  if (isLoading || apiLoading) {
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

  // エラー表示
  if (error) {
    return (
      <div className="text-center py-8">
        <div className="text-red-500 mb-2">⚠️</div>
        <p className="text-red-600 mb-4">{error}</p>
        <Button onClick={fetchActionPlans} variant="outline">
          再試行
        </Button>
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
          onChange={(e) => setFilterStatus(e.target.value as 'not_started' | 'in_progress' | 'completed' | 'all')}
          className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="all">すべて</option>
          <option value="not_started">未着手</option>
          <option value="in_progress">進行中</option>
          <option value="completed">完了</option>
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
            {filterStatus === 'all' ? 'アクションプランがありません' : `${getStatusDisplay(filterStatus)}のプランがありません`}
          </h3>
          <p className="text-sm text-gray-500">
            新しいアクションプランを追加して、目標達成に向けた具体的な行動を計画しましょう。
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredPlans.map((plan) => {
            const statusDisplay = getStatusDisplay(plan.status);
            const StatusIcon = STATUS_CONFIG[statusDisplay as keyof typeof STATUS_CONFIG]?.icon || ClockIcon;
            const daysUntilDeadline = getDaysUntilDeadline(plan.due_date);

            return (
              <div
                key={plan.action_id}
                className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    {/* タイトルとステータス */}
                    <div className="flex items-center space-x-3 mb-2">
                      <h4 className="text-base font-medium text-gray-900 truncate">
                        {plan.title}
                      </h4>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(plan.status)}`}>
                        <StatusIcon className="h-3 w-3 mr-1" />
                        {statusDisplay}
                      </span>
                    </div>

                    {/* スキル */}
                    {plan.related_skill_id && (
                      <div className="text-sm text-gray-600 mb-2">
                        <span className="font-medium">関連スキル:</span> {plan.related_skill_id}
                      </div>
                    )}

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
                          期限: {new Date(plan.due_date).toLocaleDateString('ja-JP')}
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
                    {plan.status !== 'completed' && (
                      <select
                        value={plan.status}
                        onChange={(e) => handleStatusChange(plan.action_id!, e.target.value as 'not_started' | 'in_progress' | 'completed')}
                        className="border border-gray-300 rounded-md px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="not_started">未着手</option>
                        <option value="in_progress">進行中</option>
                        <option value="completed">完了</option>
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
            {['not_started', 'in_progress', 'completed'].map((status) => {
              const count = actionPlans.filter(plan => plan.status === status).length;
              const percentage = actionPlans.length > 0 ? Math.round((count / actionPlans.length) * 100) : 0;
              const statusDisplay = getStatusDisplay(status);
              return (
                <div key={status} className="text-center">
                  <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(status)} mb-1`}>
                    {statusDisplay}
                  </div>
                  <div className="text-lg font-semibold text-gray-900">{count}</div>
                  <div className="text-xs text-gray-500">{percentage}%</div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* アクションプラン作成・編集ダイアログ */}
      {isDialogOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex min-h-screen items-center justify-center p-4">
            {/* オーバーレイ */}
            <div 
              className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
              onClick={() => setIsDialogOpen(false)}
            />
            
            {/* ダイアログコンテンツ */}
            <div className="relative bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              {/* ヘッダー */}
              <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-medium text-gray-900">
                  {editingPlan ? 'アクションプランを編集' : '新しいアクションプランを作成'}
                </h2>
                <button
                  onClick={() => setIsDialogOpen(false)}
                  className="text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-md p-1"
                >
                  <XIcon className="h-5 w-5" />
                </button>
              </div>
              
              {/* フォーム */}
              <div className="px-6 py-4">
                <ActionPlanForm
                  plan={editingPlan}
                  onSubmit={handleSubmit}
                  onCancel={() => setIsDialogOpen(false)}
                  isLoading={apiLoading}
                />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
