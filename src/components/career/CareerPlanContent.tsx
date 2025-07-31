/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: キャリアプラン画面メインコンテンツ
 */

'use client';

import React, { useState, useEffect } from 'react';
import { useCareerInit } from '@/hooks/useCareerInit';
import { useCareerGoals } from '@/hooks/useCareerGoals';
import { CareerGoalForm } from './CareerGoalForm';
import { CareerGoalList } from './CareerGoalList';
import { CareerProgressChart } from './CareerProgressChart';
import { ActionPlanSection } from './ActionPlanSection';
import { SkillGapRadarChart } from './SkillGapRadarChart';
import { CareerPathTimeline } from './CareerPathTimeline';
import { ManagerFeedbackSection } from './ManagerFeedbackSection';
import { Button } from '@/components/ui/Button';
import { Spinner } from '@/components/ui/Spinner';
import { 
  PlusIcon, 
  ChartBarIcon, 
  DocumentTextIcon,
  CalendarIcon 
} from '@/components/ui/Icons';
import { CareerGoal, CareerGoalData } from '@/types/career';

/**
 * キャリアプラン画面のプロパティ
 */
interface CareerPlanContentProps {
  userId?: string;
  year?: number;
}

/**
 * キャリアプラン画面メインコンテンツコンポーネント
 * 
 * 機能:
 * - キャリア目標の表示・編集・削除
 * - 進捗状況の可視化
 * - アクションプランの管理
 * - 年度切り替え
 */
export function CareerPlanContent({ userId, year }: CareerPlanContentProps) {
  // 状態管理
  const [selectedYear, setSelectedYear] = useState(year || new Date().getFullYear());
  const [showGoalForm, setShowGoalForm] = useState(false);
  const [editingGoal, setEditingGoal] = useState<CareerGoalData | null>(null);
  const [activeTab, setActiveTab] = useState<'goals' | 'progress' | 'actions' | 'skillgap' | 'path' | 'feedback'>('goals');

  // カスタムフック
  const { 
    careerGoal, 
    skillCategories, 
    positions, 
    isLoading: initLoading, 
    error: initError,
    refetch 
  } = useCareerInit(userId, selectedYear);

  const {
    addCareerGoal,
    updateCareerGoal,
    deleteCareerGoal,
    isLoading: goalLoading,
    error: goalError,
    isSuccess
  } = useCareerGoals(userId);

  // 年度変更時の処理
  useEffect(() => {
    if (year !== selectedYear) {
      refetch();
    }
  }, [selectedYear, year, refetch]);

  // 目標操作成功時の処理
  useEffect(() => {
    if (isSuccess) {
      setShowGoalForm(false);
      setEditingGoal(null);
      refetch();
    }
  }, [isSuccess, refetch]);

  /**
   * 新規目標追加ハンドラー
   */
  const handleAddGoal = () => {
    setEditingGoal(null);
    setShowGoalForm(true);
  };

  /**
   * 目標編集ハンドラー
   */
  const handleEditGoal = (goal: CareerGoal) => {
    // CareerGoalをCareerGoalData形式に変換
    const goalData: CareerGoalData = {
      id: goal.id,
      goal_type: goal.goal_type,
      target_position: goal.title,
      target_description: goal.description || '',
      target_date: goal.target_date || '',
      plan_status: goal.status === 'in_progress' ? 'ACTIVE' : 
                   goal.status === 'completed' ? 'COMPLETED' : 
                   goal.status === 'not_started' ? 'INACTIVE' : 'INACTIVE',
      progress_percentage: goal.progress_percentage || 0
    };
    
    setEditingGoal(goalData);
    setShowGoalForm(true);
  };

  /**
   * 目標削除ハンドラー
   */
  const handleDeleteGoal = async (goal: CareerGoal) => {
    if (window.confirm('この目標を削除してもよろしいですか？')) {
      await deleteCareerGoal(goal, selectedYear);
    }
  };

  /**
   * フォーム送信ハンドラー
   */
  const handleFormSubmit = async (goal: CareerGoal) => {
    if (editingGoal) {
      await updateCareerGoal(goal, selectedYear);
    } else {
      await addCareerGoal(goal, selectedYear);
    }
  };

  /**
   * フォームキャンセルハンドラー
   */
  const handleFormCancel = () => {
    setShowGoalForm(false);
    setEditingGoal(null);
  };

  /**
   * 年度選択肢を生成
   */
  const generateYearOptions = () => {
    const currentYear = new Date().getFullYear();
    const years = [];
    for (let i = currentYear - 2; i <= currentYear + 3; i++) {
      years.push(i);
    }
    return years;
  };

  // ローディング表示
  if (initLoading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <Spinner size="lg" />
        <span className="ml-3 text-gray-600">キャリアデータを読み込み中...</span>
      </div>
    );
  }

  // エラー表示
  if (initError) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">
              データの読み込みに失敗しました
            </h3>
            <div className="mt-2 text-sm text-red-700">
              <p>{initError}</p>
            </div>
            <div className="mt-4">
              <Button
                variant="secondary"
                size="sm"
                onClick={refetch}
              >
                再試行
              </Button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* ヘッダー部分 */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                キャリアプラン
              </h1>
              <p className="mt-1 text-sm text-gray-600">
                目標設定と進捗管理でキャリアアップを支援します
              </p>
            </div>
            <div className="flex items-center space-x-4">
              {/* 年度選択 */}
              <div className="flex items-center space-x-2">
                <CalendarIcon className="h-5 w-5 text-gray-400" />
                <select
                  value={selectedYear}
                  onChange={(e) => setSelectedYear(Number(e.target.value))}
                  className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  {generateYearOptions().map(year => (
                    <option key={year} value={year}>
                      {year}年度
                    </option>
                  ))}
                </select>
              </div>
              {/* 新規目標追加ボタン */}
              <Button
                onClick={handleAddGoal}
                disabled={goalLoading}
                className="flex items-center space-x-2"
              >
                <PlusIcon className="h-4 w-4" />
                <span>新規目標</span>
              </Button>
            </div>
          </div>
        </div>

        {/* タブナビゲーション */}
        <div className="px-6">
          <nav className="flex space-x-8" aria-label="Tabs">
            <button
              onClick={() => setActiveTab('goals')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'goals'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <DocumentTextIcon className="h-4 w-4" />
                <span>目標管理</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('progress')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'progress'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <ChartBarIcon className="h-4 w-4" />
                <span>進捗状況</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('actions')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'actions'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <DocumentTextIcon className="h-4 w-4" />
                <span>アクションプラン</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('skillgap')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'skillgap'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <ChartBarIcon className="h-4 w-4" />
                <span>スキルギャップ</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('path')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'path'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <DocumentTextIcon className="h-4 w-4" />
                <span>キャリアパス</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('feedback')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'feedback'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <DocumentTextIcon className="h-4 w-4" />
                <span>フィードバック</span>
              </div>
            </button>
          </nav>
        </div>
      </div>

      {/* エラー表示 */}
      {goalError && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{goalError}</p>
            </div>
          </div>
        </div>
      )}

      {/* メインコンテンツ */}
      <div className="bg-white shadow rounded-lg">
        <div className="p-6">
          {/* 目標フォーム */}
          {showGoalForm && (
            <div className="mb-6">
              <CareerGoalForm
                goal={editingGoal}
                skillCategories={skillCategories}
                positions={positions}
                userId={userId || 'emp_001'}
                onSubmit={handleFormSubmit}
                onCancel={handleFormCancel}
                isLoading={goalLoading}
              />
            </div>
          )}

          {/* タブコンテンツ */}
          {activeTab === 'goals' && (
            <CareerGoalList
              careerGoal={careerGoal}
              onEdit={handleEditGoal}
              onDelete={handleDeleteGoal}
              isLoading={goalLoading}
            />
          )}

          {activeTab === 'progress' && (
            <CareerProgressChart
              careerGoal={careerGoal}
              year={selectedYear}
            />
          )}

          {activeTab === 'actions' && (
            <ActionPlanSection
              careerGoal={careerGoal}
              year={selectedYear}
            />
          )}

          {activeTab === 'skillgap' && (
            <SkillGapRadarChart
              userId={userId || 'emp_001'}
              className="w-full"
            />
          )}

          {activeTab === 'path' && (
            <CareerPathTimeline
              userId={userId || 'emp_001'}
              className="w-full"
            />
          )}

          {activeTab === 'feedback' && (
            <ManagerFeedbackSection
              userId={userId || 'emp_001'}
              className="w-full"
            />
          )}
        </div>
      </div>
    </div>
  );
}
