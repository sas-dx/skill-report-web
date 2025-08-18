/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: アクションプラン作成・編集フォーム
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Spinner } from '@/components/ui/Spinner';
import { ActionPlan, ActionPlanCreateRequest } from '@/types/career';

interface ActionPlanFormProps {
  plan?: ActionPlan | null;
  onSubmit: (data: ActionPlanCreateRequest) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
}

/**
 * アクションプラン作成・編集フォーム
 */
export function ActionPlanForm({ 
  plan, 
  onSubmit, 
  onCancel, 
  isLoading = false 
}: ActionPlanFormProps) {
  // フォーム内部の状態管理用の型（statusとgoal_idを含む）
  interface InternalFormData extends Omit<ActionPlanCreateRequest, 'priority'> {
    priority: number;
    status: 'not_started' | 'in_progress' | 'completed';
    goal_id?: string;
  }

  const [formData, setFormData] = useState<InternalFormData>({
    title: '',
    description: '',
    goal_id: '',
    related_skill_id: '',
    due_date: '',
    priority: 2,
    status: 'not_started'
  });

  const [errors, setErrors] = useState<Partial<Record<keyof ActionPlanCreateRequest, string>>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // 編集時の初期値設定
  useEffect(() => {
    if (plan) {
      setFormData({
        title: plan.title,
        description: plan.description || '',
        goal_id: '',
        related_skill_id: plan.related_skill_id || '',
        due_date: plan.due_date,
        priority: plan.priority === 'high' ? 3 : plan.priority === 'medium' ? 2 : 1,
        status: plan.status
      });
    }
  }, [plan]);

  /**
   * 入力変更ハンドラー
   */
  const handleInputChange = (field: keyof InternalFormData, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // エラーをクリア
    if (errors[field as keyof ActionPlanCreateRequest]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  /**
   * バリデーション
   */
  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof ActionPlanCreateRequest, string>> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'タイトルは必須です';
    }

    if (!formData.due_date) {
      newErrors.due_date = '期限は必須です';
    } else {
      const dueDate = new Date(formData.due_date);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      if (dueDate < today) {
        newErrors.due_date = '期限は今日以降の日付を設定してください';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  /**
   * フォーム送信
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    try {
      setIsSubmitting(true);
      // priorityを文字列に変換してAPIに送信
      const submitData: any = {
        title: formData.title,
        due_date: formData.due_date,
        priority: formData.priority === 1 ? 'high' : formData.priority === 3 ? 'low' : 'medium',
      };
      
      if (formData.description) {
        submitData.description = formData.description;
      }
      
      if (formData.related_skill_id) {
        submitData.related_skill_id = formData.related_skill_id;
      }
      await onSubmit(submitData);
    } catch (error) {
      console.error('フォーム送信エラー:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* タイトル */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          タイトル <span className="text-red-500">*</span>
        </label>
        <Input
          value={formData.title}
          onChange={(e) => handleInputChange('title', e.target.value)}
          placeholder="例：React.js の学習"
          error={errors.title}
          disabled={isSubmitting || isLoading}
        />
      </div>

      {/* 説明 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          説明
        </label>
        <textarea
          value={formData.description}
          onChange={(e) => handleInputChange('description', e.target.value)}
          rows={3}
          placeholder="詳細な説明を入力してください"
          className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={isSubmitting || isLoading}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        {/* 期限 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            期限 <span className="text-red-500">*</span>
          </label>
          <Input
            type="date"
            value={formData.due_date}
            onChange={(e) => handleInputChange('due_date', e.target.value)}
            error={errors.due_date}
            disabled={isSubmitting || isLoading}
          />
        </div>

        {/* 優先度 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            優先度
          </label>
          <select
            value={formData.priority}
            onChange={(e) => handleInputChange('priority', parseInt(e.target.value))}
            className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isSubmitting || isLoading}
          >
            <option value={1}>高</option>
            <option value={2}>中</option>
            <option value={3}>低</option>
          </select>
        </div>
      </div>

      {/* ステータス */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          ステータス
        </label>
        <select
          value={formData.status}
          onChange={(e) => handleInputChange('status', e.target.value as 'not_started' | 'in_progress' | 'completed')}
          className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={isSubmitting || isLoading}
        >
          <option value="not_started">未着手</option>
          <option value="in_progress">進行中</option>
          <option value="completed">完了</option>
        </select>
      </div>

      {/* 関連スキル */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          関連スキル
        </label>
        <Input
          value={formData.related_skill_id}
          onChange={(e) => handleInputChange('related_skill_id', e.target.value)}
          placeholder="関連するスキルを入力"
          disabled={isSubmitting || isLoading}
        />
      </div>

      {/* ボタン */}
      <div className="flex justify-end space-x-3 pt-4 border-t border-gray-200">
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
          <span>{plan ? '更新' : '作成'}</span>
        </Button>
      </div>
    </form>
  );
}