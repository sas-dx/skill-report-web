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
  CareerGoalPriority
} from '@/types/career';

/**
 * キャリア目標フォームのプロパティ
 */
interface CareerGoalFormProps {
  goal?: CareerGoalData | null;
  skillCategories: SkillCategory[];
  positions: Position[];
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
  target_date: string;
  status: string;
  priority: string;
  progress_percentage: number;
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
  onSubmit,
  onCancel,
  isLoading = false
}: CareerGoalFormProps) {
  // フォーム状態
  const [formData, setFormData] = useState<FormData>({
    title: '',
    description: '',
    target_date: '',
    status: 'not_started',
    priority: '2',
    progress_percentage: 0
  });

  const [errors, setErrors] = useState<Partial<FormData>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // 編集モードの場合、初期値を設定
  useEffect(() => {
    if (goal) {
      setFormData({
        title: goal.target_position,
        description: goal.target_description,
        target_date: goal.target_date ? goal.target_date.split('T')[0] : '',
        status: goal.plan_status || 'not_started',
        priority: '2',
        progress_percentage: goal.progress_percentage
      });
    } else {
      // 新規作成の場合、デフォルト値を設定
      const nextYear = new Date();
      nextYear.setFullYear(nextYear.getFullYear() + 1);
      
      setFormData({
        title: '',
        description: '',
        target_date: nextYear.toISOString().split('T')[0],
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
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));

    // エラーをクリア
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: undefined
      }));
    }
  };

  /**
   * バリデーション
   */
  const validateForm = (): boolean => {
    const newErrors: Partial<FormData> = {};

    // タイトル
    if (!formData.title.trim()) {
      newErrors.title = 'タイトルを入力してください';
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
      const goalData: CareerGoal = {
        id: goal?.id || crypto.randomUUID(),
        user_id: 'current-user', // TODO: 実際のユーザーIDを取得
        title: formData.title,
        description: formData.description,
        status: formData.status as CareerGoalStatus,
        priority: parseInt(formData.priority) as CareerGoalPriority,
        target_date: formData.target_date,
        progress_percentage: formData.progress_percentage,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };

      await onSubmit(goalData);
    } catch (error) {
      console.error('フォーム送信エラー:', error);
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
      { value: 'not_started', label: '未開始' },
      { value: 'in_progress', label: '進行中' },
      { value: 'completed', label: '完了' },
      { value: 'on_hold', label: '保留' },
      { value: 'cancelled', label: 'キャンセル' }
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
              value={formData.progress_percentage.toString()}
              onChange={(e) => handleInputChange('progress_percentage', parseInt(e.target.value) || 0)}
              error={errors.progress_percentage}
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
