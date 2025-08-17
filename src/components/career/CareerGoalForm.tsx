/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: キャリア目標フォームコンポーネント
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Spinner } from '@/components/ui/Spinner';
import { 
  CareerGoal, 
  CareerGoalData,
  SkillCategory, 
  Position,
  CareerGoalStatus,
  CareerGoalPriority,
  CareerGoalType
} from '@/types/career';

/**
 * キャリア目標フォームのプロパティ
 */
interface CareerGoalFormProps {
  goal?: CareerGoalData | null;
  skillCategories: SkillCategory[];
  positions: Position[];
  userId: string;
  onSubmit: (goal: CareerGoal) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
}

/**
 * フォームデータの型定義
 */
interface FormData {
  title: string;
  description: string;
  goal_type: CareerGoalType;
  target_date: string;
  status: string;
  priority: string;
  progress_percentage: number;
}

/**
 * フォームエラーの型定義
 */
interface FormErrors extends Partial<FormData> {
  _general?: string; // 全般的なエラーメッセージ用
}

/**
 * キャリア目標フォームコンポーネント
 * 
 * 機能:
 * - 新規目標の作成
 * - 既存目標の編集
 * - バリデーション
 * - フォーム送信
 */
export function CareerGoalForm({
  goal,
  skillCategories,
  positions,
  userId,
  onSubmit,
  onCancel,
  isLoading = false
}: CareerGoalFormProps) {
  // フォーム状態
  const [formData, setFormData] = useState<FormData>({
    title: '',
    description: '',
    goal_type: 'short_term',
    target_date: '',
    status: 'not_started',
    priority: '2',
    progress_percentage: 0
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // 編集モードの場合、初期値を設定
  useEffect(() => {
    if (goal) {
      // 型安全な値の取得
      const title = (goal.target_position ?? '') as string;
      const description = (goal.target_description ?? '') as string;
      const targetDate = (goal.target_date ? goal.target_date.split('T')[0] : '') as string;
      const progressPercentage = (goal.progress_percentage ?? 0) as number;
      
      // 目標タイプの型安全な設定
      const rawGoalType = goal.goal_type ?? 'short_term';
      const goalType = isValidGoalType(rawGoalType) ? rawGoalType : 'short_term';
      
      setFormData({
        title,
        description,
        goal_type: goalType,
        target_date: targetDate,
        status: goal.plan_status === 'ACTIVE' ? 'in_progress' : 
                goal.plan_status === 'COMPLETED' ? 'completed' : 
                goal.plan_status === 'INACTIVE' ? 'not_started' : 'not_started',
        priority: '2',
        progress_percentage: progressPercentage
      });
    } else {
      // 新規作成の場合、デフォルト値を設定
      const nextYear = new Date();
      nextYear.setFullYear(nextYear.getFullYear() + 1);
      
      setFormData({
        title: '',
        description: '',
        goal_type: 'short_term',
        target_date: nextYear.toISOString().split('T')[0] as string,
        status: 'not_started',
        priority: '2',
        progress_percentage: 0
      });
    }
  }, [goal]);

  /**
   * 入力値変更ハンドラー
   */
  const handleInputChange = (
    field: keyof FormData,
    value: string | number
  ) => {
    // 目標タイプの場合は型安全な処理
    if (field === 'goal_type' && typeof value === 'string') {
      const goalType = isValidGoalType(value) ? value : 'short_term';
      setFormData(prev => ({
        ...prev,
        [field]: goalType
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [field]: value
      }));
    }

    // エラーをクリア
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: undefined
      }));
    }
  };

  /**
   * 型ガード関数：有効な目標タイプかチェック
   */
  const isValidGoalType = (value: string): value is CareerGoalType => {
    return ['short_term', 'mid_term', 'long_term'].includes(value);
  };

  /**
   * バリデーション
   */
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    // タイトル
    if (!formData.title.trim()) {
      newErrors.title = 'タイトルを入力してください';
    }

    // 目標タイプ - 型安全なバリデーション
    if (!formData.goal_type) {
      newErrors.goal_type = '目標タイプを選択してください';
    } else if (!isValidGoalType(formData.goal_type)) {
      newErrors.goal_type = '無効な目標タイプです';
    }

    // 目標達成日
    if (!formData.target_date) {
      newErrors.target_date = '目標達成日を入力してください';
    } else {
      const targetDate = new Date(formData.target_date);
      const today = new Date();
      if (targetDate <= today) {
        newErrors.target_date = '目標達成日は未来の日付を入力してください';
      }
    }

    // 説明
    if (!formData.description.trim()) {
      newErrors.description = '説明を入力してください';
    } else if (formData.description.length > 500) {
      newErrors.description = '説明は500文字以内で入力してください';
    }

    // 進捗率
    if (formData.progress_percentage < 0 || formData.progress_percentage > 100) {
      newErrors.progress_percentage = '進捗率は0-100の範囲で入力してください';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  /**
   * フォーム送信ハンドラー
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      // 優先度を確実に数値に変換
      const priorityNumber = parseInt(formData.priority, 10);
      if (isNaN(priorityNumber) || priorityNumber < 1 || priorityNumber > 3) {
        throw new Error('優先度は1-3の範囲で指定してください');
      }

      const goalData: CareerGoal = {
        id: goal?.id || crypto.randomUUID(),
        user_id: userId,
        goal_type: formData.goal_type,
        title: formData.title,
        description: formData.description,
        status: formData.status as CareerGoalStatus,
        priority: priorityNumber as CareerGoalPriority,
        target_date: formData.target_date,
        progress_percentage: formData.progress_percentage,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };

      // デバッグ用ログ追加
      console.log('=== フォーム送信データ デバッグ ===');
      console.log('formData:', formData);
      console.log('formData.priority (string):', formData.priority, 'typeof:', typeof formData.priority);
      console.log('priorityNumber (converted):', priorityNumber, 'typeof:', typeof priorityNumber);
      console.log('goalData:', goalData);
      console.log('goalData.priority:', goalData.priority, 'typeof:', typeof goalData.priority);
      console.log('goal_type:', goalData.goal_type, 'typeof:', typeof goalData.goal_type);

      // エラーをクリア
      setErrors({});

      await onSubmit(goalData);
    } catch (error) {
      console.error('フォーム送信エラー:', error);
      
      // ユーザーフレンドリーなエラーメッセージ表示
      let userMessage = 'キャリア目標の保存に失敗しました。';
      if (error instanceof Error) {
        if (error.message.includes('優先度')) {
          userMessage = '優先度の設定に問題があります。再度お試しください。';
        } else if (error.message.includes('目標タイプ')) {
          userMessage = '目標タイプの選択に問題があります。再度お試しください。';
        } else if (error.message.includes('必須')) {
          userMessage = '必須項目が不足しています。入力内容をご確認ください。';
        } else if (error.message.includes('詳細:')) {
          userMessage = error.message; // APIからの詳細エラーメッセージを表示
        }
      }
      
      // エラー表示のため、setErrors を使用してユーザーに通知
      setErrors(prev => ({
        ...prev,
        _general: userMessage
      }));
    } finally {
      setIsSubmitting(false);
    }
  };

  /**
   * レベル選択肢を生成
   */
  const generateLevelOptions = () => {
    return [
      { value: '1', label: 'レベル1 - 初級' },
      { value: '2', label: 'レベル2 - 中級' },
      { value: '3', label: 'レベル3 - 上級' },
      { value: '4', label: 'レベル4 - エキスパート' }
    ];
  };

  /**
   * ステータス選択肢を生成
   */
  const generateStatusOptions = () => {
    return [
      { value: 'not_started', label: '未着手' },
      { value: 'in_progress', label: '進行中' },
      { value: 'completed', label: '完了' },
      { value: 'postponed', label: '延期' },
      { value: 'cancelled', label: '中止' }
    ];
  };

  /**
   * 目標タイプ選択肢を生成
   */
  const generateGoalTypeOptions = () => {
    return [
      { value: 'short_term', label: '短期目標（1年以内）' },
      { value: 'mid_term', label: '中期目標（1-3年）' },
      { value: 'long_term', label: '長期目標（3年以上）' }
    ];
  };

  return (
    <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
      <div className="mb-6">
        <h3 className="text-lg font-medium text-gray-900">
          {goal ? 'キャリア目標を編集' : '新しいキャリア目標を作成'}
        </h3>
        <p className="mt-1 text-sm text-gray-600">
          目標設定により、キャリアアップの道筋を明確にしましょう
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* 全般エラーメッセージ表示 */}
        {errors._general && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">
                  エラーが発生しました
                </h3>
                <div className="mt-2 text-sm text-red-700">
                  <pre className="whitespace-pre-wrap">{errors._general}</pre>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* タイトル */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              タイトル <span className="text-red-500">*</span>
            </label>
            <Input
              type="text"
              value={formData.title}
              onChange={(e) => handleInputChange('title', e.target.value)}
              error={errors.title}
              placeholder="目標のタイトルを入力してください"
              className="w-full"
            />
          </div>

          {/* 目標タイプ */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              目標タイプ <span className="text-red-500">*</span>
            </label>
            <select
              value={formData.goal_type}
              onChange={(e) => handleInputChange('goal_type', e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {generateGoalTypeOptions().map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-1 gap-6">
          {/* 目標達成日 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              目標達成日 <span className="text-red-500">*</span>
            </label>
            <Input
              type="date"
              value={formData.target_date}
              onChange={(e) => handleInputChange('target_date', e.target.value)}
              error={errors.target_date}
              className="w-full"
            />
          </div>
        </div>

        {/* 説明 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            説明 <span className="text-red-500">*</span>
          </label>
          <textarea
            value={formData.description}
            onChange={(e) => handleInputChange('description', e.target.value)}
            rows={4}
            maxLength={500}
            placeholder="具体的な目標内容や達成したいことを記述してください"
            className={`w-full border rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              errors.description ? 'border-red-300' : 'border-gray-300'
            }`}
          />
          <div className="mt-1 flex justify-between">
            {errors.description && (
              <p className="text-sm text-red-600">{errors.description}</p>
            )}
            <p className="text-sm text-gray-500">
              {formData.description.length}/500文字
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* 優先度 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              優先度
            </label>
            <select
              value={formData.priority}
              onChange={(e) => handleInputChange('priority', e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="1">高</option>
              <option value="2">中</option>
              <option value="3">低</option>
            </select>
          </div>

          {/* ステータス */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              ステータス
            </label>
            <select
              value={formData.status}
              onChange={(e) => handleInputChange('status', e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {generateStatusOptions().map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          {/* 進捗率 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              進捗率 (%)
            </label>
            <Input
              type="number"
              min="0"
              max="100"
              value={String(formData.progress_percentage)}
              onChange={(e) => handleInputChange('progress_percentage', parseInt(e.target.value) || 0)}
              error={errors.progress_percentage ? String(errors.progress_percentage) : undefined}
              className="w-full"
            />
          </div>
        </div>

        {/* ボタン */}
        <div className="flex justify-end space-x-3 pt-6 border-t border-gray-200">
          <Button
            type="button"
            variant="secondary"
            onClick={onCancel}
            disabled={isSubmitting || isLoading}
          >
            キャンセル
          </Button>
          <Button
            type="submit"
            disabled={isSubmitting || isLoading}
            className="flex items-center space-x-2"
          >
            {(isSubmitting || isLoading) && <Spinner size="sm" />}
            <span>{goal ? '更新' : '作成'}</span>
          </Button>
        </div>
      </form>
    </div>
  );
}
