/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: キャリアパスステップ作成・編集フォーム
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Spinner } from '@/components/ui/Spinner';
import { XIcon, PlusIcon, TrashIcon } from '@/components/ui/Icons';

// 型定義
export interface CareerPathStep {
  step_id?: string;
  position_name: string;
  position_level: number;
  description: string;
  estimated_duration: string;
  target_date?: string;
  prerequisites: string[];
  required_skills: Array<{
    skill_id: string;
    skill_name: string;
    required_level: number;
  }>;
  milestones: string[];
  status?: 'not_started' | 'in_progress' | 'completed';
  progress_percentage?: number;
}

interface CareerPathFormProps {
  step?: CareerPathStep | null;
  onSubmit: (data: CareerPathStep) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
}

/**
 * キャリアパスステップフォームコンポーネント
 */
export function CareerPathForm({ 
  step, 
  onSubmit, 
  onCancel, 
  isLoading = false 
}: CareerPathFormProps) {
  const [formData, setFormData] = useState<CareerPathStep>({
    position_name: '',
    position_level: 1,
    description: '',
    estimated_duration: '',
    target_date: '',
    prerequisites: [],
    required_skills: [],
    milestones: [],
    status: 'not_started',
    progress_percentage: 0
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [newPrerequisite, setNewPrerequisite] = useState('');
  const [newMilestone, setNewMilestone] = useState('');
  const [newSkill, setNewSkill] = useState({ skill_name: '', required_level: 1 });

  // 編集時の初期値設定
  useEffect(() => {
    if (step) {
      setFormData({
        position_name: step.position_name || '',
        position_level: step.position_level || 1,
        description: step.description || '',
        estimated_duration: step.estimated_duration || '',
        target_date: step.target_date ? step.target_date.split('T')[0] : '',
        prerequisites: step.prerequisites || [],
        required_skills: step.required_skills || [],
        milestones: step.milestones || [],
        status: step.status || 'not_started',
        progress_percentage: step.progress_percentage || 0,
        step_id: step.step_id
      });
    }
  }, [step]);

  /**
   * 入力変更ハンドラー
   */
  const handleInputChange = (field: keyof CareerPathStep, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // エラーをクリア
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  /**
   * 前提条件追加
   */
  const addPrerequisite = () => {
    if (newPrerequisite.trim()) {
      setFormData(prev => ({
        ...prev,
        prerequisites: [...(prev.prerequisites || []), newPrerequisite.trim()]
      }));
      setNewPrerequisite('');
    }
  };

  /**
   * 前提条件削除
   */
  const removePrerequisite = (index: number) => {
    setFormData(prev => ({
      ...prev,
      prerequisites: (prev.prerequisites || []).filter((_, i) => i !== index)
    }));
  };

  /**
   * マイルストーン追加
   */
  const addMilestone = () => {
    if (newMilestone.trim()) {
      setFormData(prev => ({
        ...prev,
        milestones: [...(prev.milestones || []), newMilestone.trim()]
      }));
      setNewMilestone('');
    }
  };

  /**
   * マイルストーン削除
   */
  const removeMilestone = (index: number) => {
    setFormData(prev => ({
      ...prev,
      milestones: (prev.milestones || []).filter((_, i) => i !== index)
    }));
  };

  /**
   * 必要スキル追加
   */
  const addRequiredSkill = () => {
    if (newSkill.skill_name.trim()) {
      setFormData(prev => ({
        ...prev,
        required_skills: [...(prev.required_skills || []), {
          skill_id: `skill_${Date.now()}`,
          skill_name: newSkill.skill_name.trim(),
          required_level: newSkill.required_level
        }]
      }));
      setNewSkill({ skill_name: '', required_level: 1 });
    }
  };

  /**
   * 必要スキル削除
   */
  const removeRequiredSkill = (index: number) => {
    setFormData(prev => ({
      ...prev,
      required_skills: (prev.required_skills || []).filter((_, i) => i !== index)
    }));
  };

  /**
   * バリデーション
   */
  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.position_name.trim()) {
      newErrors.position_name = 'ポジション名は必須です';
    }

    if (formData.position_level < 1 || formData.position_level > 10) {
      newErrors.position_level = 'レベルは1〜10の範囲で入力してください';
    }

    if (!formData.description.trim()) {
      newErrors.description = '説明は必須です';
    }

    if (!formData.estimated_duration.trim()) {
      newErrors.estimated_duration = '想定期間は必須です';
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
      await onSubmit(formData);
    } catch (error) {
      console.error('フォーム送信エラー:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* ポジション名とレベル */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            ポジション名 <span className="text-red-500">*</span>
          </label>
          <Input
            value={formData.position_name}
            onChange={(e) => handleInputChange('position_name', e.target.value)}
            placeholder="例：シニアエンジニア"
            error={errors.position_name}
            disabled={isSubmitting || isLoading}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            レベル <span className="text-red-500">*</span>
          </label>
          <Input
            type="number"
            min="1"
            max="10"
            value={formData.position_level}
            onChange={(e) => handleInputChange('position_level', parseInt(e.target.value))}
            error={errors.position_level}
            disabled={isSubmitting || isLoading}
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
          rows={3}
          placeholder="このポジションの役割と責任について説明してください"
          className={`w-full border rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.description ? 'border-red-300' : 'border-gray-300'
          }`}
          disabled={isSubmitting || isLoading}
        />
        {errors.description && (
          <p className="mt-1 text-sm text-red-600">{errors.description}</p>
        )}
      </div>

      {/* 期間と目標日 */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            想定期間 <span className="text-red-500">*</span>
          </label>
          <Input
            value={formData.estimated_duration}
            onChange={(e) => handleInputChange('estimated_duration', e.target.value)}
            placeholder="例：1年〜2年"
            error={errors.estimated_duration}
            disabled={isSubmitting || isLoading}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            目標達成日
          </label>
          <Input
            type="date"
            value={formData.target_date}
            onChange={(e) => handleInputChange('target_date', e.target.value)}
            disabled={isSubmitting || isLoading}
          />
        </div>
      </div>

      {/* 前提条件 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          前提条件
        </label>
        <div className="space-y-2">
          <div className="flex gap-2">
            <Input
              value={newPrerequisite}
              onChange={(e) => setNewPrerequisite(e.target.value)}
              placeholder="新しい前提条件を入力"
              disabled={isSubmitting || isLoading}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  addPrerequisite();
                }
              }}
            />
            <Button
              type="button"
              onClick={addPrerequisite}
              disabled={isSubmitting || isLoading}
              variant="secondary"
            >
              <PlusIcon className="h-4 w-4" />
            </Button>
          </div>
          {(formData.prerequisites || []).map((prerequisite, index) => (
            <div key={index} className="flex items-center justify-between bg-gray-50 px-3 py-2 rounded">
              <span className="text-sm">{prerequisite}</span>
              <button
                type="button"
                onClick={() => removePrerequisite(index)}
                className="text-red-500 hover:text-red-700"
              >
                <TrashIcon className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* 必要スキル */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          必要スキル
        </label>
        <div className="space-y-2">
          <div className="flex gap-2">
            <Input
              value={newSkill.skill_name}
              onChange={(e) => setNewSkill(prev => ({ ...prev, skill_name: e.target.value }))}
              placeholder="スキル名"
              disabled={isSubmitting || isLoading}
            />
            <Input
              type="number"
              min="1"
              max="5"
              value={newSkill.required_level}
              onChange={(e) => setNewSkill(prev => ({ ...prev, required_level: parseInt(e.target.value) }))}
              placeholder="レベル"
              className="w-24"
              disabled={isSubmitting || isLoading}
            />
            <Button
              type="button"
              onClick={addRequiredSkill}
              disabled={isSubmitting || isLoading}
              variant="secondary"
            >
              <PlusIcon className="h-4 w-4" />
            </Button>
          </div>
          {(formData.required_skills || []).map((skill, index) => (
            <div key={index} className="flex items-center justify-between bg-gray-50 px-3 py-2 rounded">
              <span className="text-sm">{skill.skill_name} (Lv.{skill.required_level})</span>
              <button
                type="button"
                onClick={() => removeRequiredSkill(index)}
                className="text-red-500 hover:text-red-700"
              >
                <TrashIcon className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* マイルストーン */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          マイルストーン
        </label>
        <div className="space-y-2">
          <div className="flex gap-2">
            <Input
              value={newMilestone}
              onChange={(e) => setNewMilestone(e.target.value)}
              placeholder="新しいマイルストーンを入力"
              disabled={isSubmitting || isLoading}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  addMilestone();
                }
              }}
            />
            <Button
              type="button"
              onClick={addMilestone}
              disabled={isSubmitting || isLoading}
              variant="secondary"
            >
              <PlusIcon className="h-4 w-4" />
            </Button>
          </div>
          {(formData.milestones || []).map((milestone, index) => (
            <div key={index} className="flex items-center justify-between bg-gray-50 px-3 py-2 rounded">
              <span className="text-sm">{milestone}</span>
              <button
                type="button"
                onClick={() => removeMilestone(index)}
                className="text-red-500 hover:text-red-700"
              >
                <TrashIcon className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* ステータスと進捗 */}
      {step && (
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              ステータス
            </label>
            <select
              value={formData.status}
              onChange={(e) => handleInputChange('status', e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isSubmitting || isLoading}
            >
              <option value="not_started">未開始</option>
              <option value="in_progress">進行中</option>
              <option value="completed">完了</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              進捗率 (%)
            </label>
            <Input
              type="number"
              min="0"
              max="100"
              value={formData.progress_percentage}
              onChange={(e) => handleInputChange('progress_percentage', parseInt(e.target.value))}
              disabled={isSubmitting || isLoading}
            />
          </div>
        </div>
      )}

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
          <span>{step ? '更新' : '作成'}</span>
        </Button>
      </div>
    </form>
  );
}