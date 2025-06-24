/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: キャリアプラン画面のメインコンテンツ
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Target, Plus, Edit, Trash2, Calendar, TrendingUp, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select, SelectOption } from '@/components/ui/Select';
import { Spinner } from '@/components/ui/Spinner';
import { useCareerData } from '@/hooks/useCareerData';
import { useCareerGoals } from '@/hooks/useCareerGoals';
import { CareerGoal, CareerGoalStatus, CareerGoalPriority } from '@/types/career';

interface CareerPlanContentProps {
  userId: string;
}

/**
 * キャリアプラン画面のメインコンテンツコンポーネント
 */
export function CareerPlanContent({ userId }: CareerPlanContentProps) {
  const { careerGoal, skillCategories, positions, isLoading: careerLoading, error: careerError } = useCareerData(userId);
  const { 
    isLoading: goalsLoading, 
    error: goalsError, 
    addCareerGoal, 
    updateCareerGoal, 
    deleteCareerGoal 
  } = useCareerGoals(userId);

  const [goals, setGoals] = useState<CareerGoal[]>([]);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [editingGoal, setEditingGoal] = useState<CareerGoal | null>(null);
  const [filterStatus, setFilterStatus] = useState<CareerGoalStatus | 'all'>('all');
  const [filterPriority, setFilterPriority] = useState<CareerGoalPriority | 'all'>('all');

  // ローディング状態
  const isLoading = careerLoading || goalsLoading;

  // エラー状態
  const error = careerError || goalsError;

  // フィルタリングされた目標
  const filteredGoals = goals.filter(goal => {
    const statusMatch = filterStatus === 'all' || goal.status === filterStatus;
    const priorityMatch = filterPriority === 'all' || goal.priority === filterPriority;
    return statusMatch && priorityMatch;
  });

  // ステータス別の目標数
  const goalStats = {
    total: goals.length,
    not_started: goals.filter(g => g.status === 'not_started').length,
    in_progress: goals.filter(g => g.status === 'in_progress').length,
    completed: goals.filter(g => g.status === 'completed').length,
    postponed: goals.filter(g => g.status === 'postponed').length,
    cancelled: goals.filter(g => g.status === 'cancelled').length,
  };

  // 目標作成
  const handleCreateGoal = async (goalData: Omit<CareerGoal, 'id' | 'user_id' | 'created_at' | 'updated_at'>) => {
    try {
      const newGoal: CareerGoal = {
        id: Date.now().toString(),
        user_id: userId,
        ...goalData,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      
      const result = await addCareerGoal(newGoal, new Date().getFullYear());
      if (result) {
        setGoals(prev => [...prev, newGoal]);
        setIsCreateModalOpen(false);
      }
    } catch (error) {
      console.error('目標作成エラー:', error);
    }
  };

  // 目標更新
  const handleUpdateGoal = async (goalId: string, goalData: Partial<CareerGoal>) => {
    try {
      const existingGoal = goals.find(g => g.id === goalId);
      if (existingGoal) {
        const updatedGoal = { ...existingGoal, ...goalData, updated_at: new Date().toISOString() };
        const result = await updateCareerGoal(updatedGoal, new Date().getFullYear());
        if (result) {
          setGoals(prev => prev.map(g => g.id === goalId ? updatedGoal : g));
          setEditingGoal(null);
        }
      }
    } catch (error) {
      console.error('目標更新エラー:', error);
    }
  };

  // 目標削除
  const handleDeleteGoal = async (goalId: string) => {
    if (window.confirm('この目標を削除してもよろしいですか？')) {
      try {
        const existingGoal = goals.find(g => g.id === goalId);
        if (existingGoal) {
          const result = await deleteCareerGoal(existingGoal, new Date().getFullYear());
          if (result) {
            setGoals(prev => prev.filter(g => g.id !== goalId));
          }
        }
      } catch (error) {
        console.error('目標削除エラー:', error);
      }
    }
  };

  // ステータスオプション
  const statusOptions: SelectOption[] = [
    { value: 'all', label: 'すべて' },
    { value: 'not_started', label: '未開始' },
    { value: 'in_progress', label: '進行中' },
    { value: 'completed', label: '完了' },
    { value: 'postponed', label: '延期' },
    { value: 'cancelled', label: 'キャンセル' },
  ];

  // 優先度オプション
  const priorityOptions: SelectOption[] = [
    { value: 'all', label: 'すべて' },
    { value: '1', label: '高' },
    { value: '2', label: '中' },
    { value: '3', label: '低' },
  ];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Spinner size="lg" />
        <span className="ml-2 text-gray-600">キャリアプランを読み込み中...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">エラーが発生しました</h3>
          <p className="text-gray-600">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* ヘッダー */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center">
            <Target className="h-8 w-8 text-blue-600 mr-3" />
            キャリアプラン
          </h1>
          <p className="text-gray-600 mt-1">
            あなたのキャリア目標を設定し、進捗を管理しましょう
          </p>
        </div>
        <Button
          onClick={() => setIsCreateModalOpen(true)}
          className="flex items-center"
        >
          <Plus className="h-4 w-4 mr-2" />
          新しい目標を追加
        </Button>
      </div>

      {/* 統計カード */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-6 rounded-lg shadow border">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Target className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">総目標数</p>
              <p className="text-2xl font-bold text-gray-900">{goalStats.total}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <Calendar className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">未開始</p>
              <p className="text-2xl font-bold text-gray-900">{goalStats.not_started}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">進行中</p>
              <p className="text-2xl font-bold text-gray-900">{goalStats.in_progress}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Target className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">完了</p>
              <p className="text-2xl font-bold text-gray-900">{goalStats.completed}</p>
            </div>
          </div>
        </div>
      </div>

      {/* フィルター */}
      <div className="bg-white p-4 rounded-lg shadow border">
        <div className="flex flex-wrap gap-4">
          <div className="flex-1 min-w-48">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              ステータス
            </label>
            <Select
              options={statusOptions}
              value={filterStatus}
              onChange={(value) => setFilterStatus(value as CareerGoalStatus | 'all')}
              placeholder="ステータスを選択"
            />
          </div>
          <div className="flex-1 min-w-48">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              優先度
            </label>
            <Select
              options={priorityOptions}
              value={filterPriority === 'all' ? 'all' : filterPriority.toString()}
              onChange={(value) => setFilterPriority(value === 'all' ? 'all' : parseInt(value) as CareerGoalPriority)}
              placeholder="優先度を選択"
            />
          </div>
        </div>
      </div>

      {/* 目標一覧 */}
      <div className="bg-white rounded-lg shadow border">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">
            キャリア目標一覧 ({filteredGoals.length}件)
          </h2>
        </div>

        {filteredGoals.length === 0 ? (
          <div className="p-8 text-center">
            <Target className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">目標がありません</h3>
            <p className="text-gray-600 mb-4">
              新しいキャリア目標を追加して、成長を始めましょう
            </p>
            <Button onClick={() => setIsCreateModalOpen(true)}>
              <Plus className="h-4 w-4 mr-2" />
              最初の目標を追加
            </Button>
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {filteredGoals.map((goal) => (
              <GoalCard
                key={goal.id}
                goal={goal}
                onEdit={() => setEditingGoal(goal)}
                onDelete={() => handleDeleteGoal(goal.id)}
                onUpdateStatus={(status) => handleUpdateGoal(goal.id, { status })}
              />
            ))}
          </div>
        )}
      </div>

      {/* 目標作成モーダル */}
      {isCreateModalOpen && (
        <GoalModal
          title="新しい目標を追加"
          onClose={() => setIsCreateModalOpen(false)}
          onSubmit={handleCreateGoal}
        />
      )}

      {/* 目標編集モーダル */}
      {editingGoal && (
        <GoalModal
          title="目標を編集"
          goal={editingGoal}
          onClose={() => setEditingGoal(null)}
          onSubmit={(goalData) => handleUpdateGoal(editingGoal.id, goalData)}
        />
      )}
    </div>
  );
}

/**
 * 目標カードコンポーネント
 */
interface GoalCardProps {
  goal: CareerGoal;
  onEdit: () => void;
  onDelete: () => void;
  onUpdateStatus: (status: CareerGoalStatus) => void;
}

function GoalCard({ goal, onEdit, onDelete, onUpdateStatus }: GoalCardProps) {
  const getStatusColor = (status: CareerGoalStatus) => {
    switch (status) {
      case 'not_started': return 'bg-yellow-100 text-yellow-800';
      case 'in_progress': return 'bg-blue-100 text-blue-800';
      case 'completed': return 'bg-green-100 text-green-800';
      case 'postponed': return 'bg-orange-100 text-orange-800';
      case 'cancelled': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusLabel = (status: CareerGoalStatus) => {
    switch (status) {
      case 'not_started': return '未開始';
      case 'in_progress': return '進行中';
      case 'completed': return '完了';
      case 'postponed': return '延期';
      case 'cancelled': return 'キャンセル';
      default: return status;
    }
  };

  const getPriorityColor = (priority: CareerGoalPriority) => {
    switch (priority) {
      case 1: return 'text-red-600';
      case 2: return 'text-yellow-600';
      case 3: return 'text-green-600';
      default: return 'text-gray-600';
    }
  };

  const getPriorityLabel = (priority: CareerGoalPriority) => {
    switch (priority) {
      case 1: return '高';
      case 2: return '中';
      case 3: return '低';
      default: return '不明';
    }
  };

  return (
    <div className="p-6 hover:bg-gray-50 transition-colors duration-150">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-3 mb-2">
            <h3 className="text-lg font-medium text-gray-900">{goal.title}</h3>
            <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(goal.status)}`}>
              {getStatusLabel(goal.status)}
            </span>
            <span className={`text-sm font-medium ${getPriorityColor(goal.priority)}`}>
              優先度: {getPriorityLabel(goal.priority)}
            </span>
          </div>
          
          {goal.description && (
            <p className="text-gray-600 mb-3">{goal.description}</p>
          )}

          <div className="flex items-center space-x-4 text-sm text-gray-500">
            {goal.target_date && (
              <span className="flex items-center">
                <Calendar className="h-4 w-4 mr-1" />
                目標日: {new Date(goal.target_date).toLocaleDateString('ja-JP')}
              </span>
            )}
            {goal.progress_percentage !== undefined && (
              <span className="flex items-center">
                <TrendingUp className="h-4 w-4 mr-1" />
                進捗: {goal.progress_percentage}%
              </span>
            )}
          </div>

          {goal.progress_percentage !== undefined && (
            <div className="mt-3">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${goal.progress_percentage}%` }}
                />
              </div>
            </div>
          )}
        </div>

        <div className="flex items-center space-x-2 ml-4">
          <Button
            variant="outline"
            size="sm"
            onClick={onEdit}
            className="flex items-center"
          >
            <Edit className="h-4 w-4" />
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={onDelete}
            className="flex items-center text-red-600 hover:text-red-700"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}

/**
 * 目標作成・編集モーダルコンポーネント
 */
interface GoalModalProps {
  title: string;
  goal?: CareerGoal;
  onClose: () => void;
  onSubmit: (goalData: Omit<CareerGoal, 'id' | 'user_id' | 'created_at' | 'updated_at'>) => void;
}

function GoalModal({ title, goal, onClose, onSubmit }: GoalModalProps) {
  const [formData, setFormData] = useState({
    title: goal?.title || '',
    description: goal?.description || '',
    status: goal?.status || 'not_started' as CareerGoalStatus,
    priority: goal?.priority || 2 as CareerGoalPriority,
    target_date: goal?.target_date ? new Date(goal.target_date).toISOString().split('T')[0] : '',
    progress_percentage: goal?.progress_percentage || 0,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // バリデーション
    const newErrors: Record<string, string> = {};
    if (!formData.title.trim()) {
      newErrors.title = 'タイトルは必須です';
    }
    if (formData.progress_percentage < 0 || formData.progress_percentage > 100) {
      newErrors.progress_percentage = '進捗は0-100の範囲で入力してください';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    onSubmit({
      title: formData.title,
      description: formData.description.trim() || '',
      status: formData.status,
      priority: formData.priority,
      target_date: formData.target_date || '',
      progress_percentage: formData.progress_percentage,
    });
  };

  const statusOptions: SelectOption[] = [
    { value: 'not_started', label: '未開始' },
    { value: 'in_progress', label: '進行中' },
    { value: 'completed', label: '完了' },
    { value: 'postponed', label: '延期' },
    { value: 'cancelled', label: 'キャンセル' },
  ];

  const priorityOptions: SelectOption[] = [
    { value: '1', label: '高' },
    { value: '2', label: '中' },
    { value: '3', label: '低' },
  ];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">{title}</h2>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              タイトル *
            </label>
            <Input
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              error={errors.title}
              placeholder="目標のタイトルを入力"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              説明
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              rows={3}
              placeholder="目標の詳細説明を入力"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                ステータス
              </label>
              <Select
                options={statusOptions}
                value={formData.status}
                onChange={(value) => setFormData({ ...formData, status: value as CareerGoalStatus })}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                優先度
              </label>
              <Select
                options={priorityOptions}
                value={formData.priority.toString()}
                onChange={(value) => setFormData({ ...formData, priority: parseInt(value) as CareerGoalPriority })}
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              目標日
            </label>
            <Input
              type="date"
              value={formData.target_date}
              onChange={(e) => setFormData({ ...formData, target_date: e.target.value })}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              進捗 (%)
            </label>
            <Input
              type="number"
              min="0"
              max="100"
              value={formData.progress_percentage}
              onChange={(e) => setFormData({ ...formData, progress_percentage: parseInt(e.target.value) || 0 })}
              error={errors.progress_percentage}
            />
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={onClose}
            >
              キャンセル
            </Button>
            <Button type="submit">
              {goal ? '更新' : '作成'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
