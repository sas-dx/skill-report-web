/**
 * 要求仕様ID: TRN.1-ATT.1
 * 対応設計書: docs/design/screens/specs/画面設計書_SCR-TRAINING_研修管理画面.md
 * 実装内容: 新規研修記録登録フォーム
 */
'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';

interface TrainingRecordFormData {
  trainingName: string;
  category: string;
  startDate: string;
  endDate: string;
  hours: number;
  pduPoints: number;
  description: string;
  skills: string[];
}

interface TrainingRecordFormProps {
  onSave: (data: TrainingRecordFormData) => void;
  onCancel: () => void;
  isLoading: boolean;
  initialData?: any; // 編集時の初期データ
}

export function TrainingRecordForm({ onSave, onCancel, isLoading, initialData }: TrainingRecordFormProps) {
  const [formData, setFormData] = useState<TrainingRecordFormData>({
    trainingName: initialData?.trainingName || '',
    category: initialData?.category || 'フロントエンド',
    startDate: initialData?.startDate || '',
    endDate: initialData?.endDate || '',
    hours: initialData?.hours || 0,
    pduPoints: initialData?.pduPoints || 0,
    description: initialData?.description || '',
    skills: initialData?.skills || []
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [skillInput, setSkillInput] = useState('');

  // カテゴリ選択肢
  const categories = [
    { value: 'フロントエンド', label: 'フロントエンド' },
    { value: 'バックエンド', label: 'バックエンド' },
    { value: 'データベース', label: 'データベース' },
    { value: 'クラウド', label: 'クラウド' },
    { value: 'AI・機械学習', label: 'AI・機械学習' },
    { value: 'プロジェクト管理', label: 'プロジェクト管理' },
    { value: 'セキュリティ', label: 'セキュリティ' },
    { value: 'その他', label: 'その他' }
  ];

  // 日付の妥当性チェック関数
  const validateDate = (dateString: string): boolean => {
    if (!dateString) return false;
    
    // YYYY-MM-DD形式の正規表現チェック
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(dateString)) return false;
    
    // 年の範囲チェック（1900-9999）
    const year = parseInt(dateString.substring(0, 4));
    if (year < 1900 || year > 9999) return false;
    
    // 日付の妥当性チェック
    const date = new Date(dateString);
    return date instanceof Date && !isNaN(date.getTime()) && 
           date.toISOString().substring(0, 10) === dateString;
  };

  // バリデーション関数
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    // 研修名チェック
    if (!formData.trainingName.trim()) {
      newErrors.trainingName = '研修名は必須です';
    } else if (formData.trainingName.length > 100) {
      newErrors.trainingName = '研修名は100文字以内で入力してください';
    }

    // カテゴリチェック
    if (!formData.category) {
      newErrors.category = 'カテゴリは必須です';
    }

    // 開始日チェック
    if (!formData.startDate) {
      newErrors.startDate = '開始日は必須です';
    } else if (!validateDate(formData.startDate)) {
      newErrors.startDate = '正しい日付形式で入力してください（1900-9999年）';
    }

    // 終了日チェック
    if (!formData.endDate) {
      newErrors.endDate = '終了日は必須です';
    } else if (!validateDate(formData.endDate)) {
      newErrors.endDate = '正しい日付形式で入力してください（1900-9999年）';
    }

    // 日付の整合性チェック
    if (formData.startDate && formData.endDate && 
        validateDate(formData.startDate) && validateDate(formData.endDate)) {
      if (new Date(formData.startDate) > new Date(formData.endDate)) {
        newErrors.endDate = '終了日は開始日以降の日付を入力してください';
      }
    }

    // 時間数チェック
    if (formData.hours <= 0) {
      newErrors.hours = '時間数は1以上の数値を入力してください';
    } else if (formData.hours > 999) {
      newErrors.hours = '時間数は999時間以内で入力してください';
    }

    // PDUポイントチェック
    if (formData.pduPoints < 0) {
      newErrors.pduPoints = 'PDUポイントは0以上の数値を入力してください';
    } else if (formData.pduPoints > 999) {
      newErrors.pduPoints = 'PDUポイントは999ポイント以内で入力してください';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // フォーム送信処理
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    try {
      // 編集時はIDを含めて送信
      const dataToSave = initialData?.id 
        ? { ...formData, id: initialData.id }
        : formData;
      await onSave(dataToSave);
    } catch (error) {
      console.error('研修記録保存エラー:', error);
    }
  };

  // 入力値変更処理
  const handleInputChange = (field: keyof TrainingRecordFormData, value: string | number) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));

    // エラーをクリア
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: ''
      }));
    }
  };

  // スキル追加処理
  const handleAddSkill = () => {
    if (skillInput.trim() && !formData.skills.includes(skillInput.trim())) {
      setFormData(prev => ({
        ...prev,
        skills: [...prev.skills, skillInput.trim()]
      }));
      setSkillInput('');
    }
  };

  // スキル削除処理
  const handleRemoveSkill = (skillToRemove: string) => {
    setFormData(prev => ({
      ...prev,
      skills: prev.skills.filter(skill => skill !== skillToRemove)
    }));
  };

  // Enterキーでスキル追加
  const handleSkillInputKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddSkill();
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          {/* ヘッダー */}
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-gray-900">
              {initialData?.id ? '研修記録編集' : '新規研修記録'}
            </h2>
            <button
              onClick={onCancel}
              className="text-gray-400 hover:text-gray-600"
              disabled={isLoading}
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* フォーム */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* 研修名 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                研修名 <span className="text-red-500">*</span>
              </label>
              <Input
                type="text"
                value={formData.trainingName}
                onChange={(e) => handleInputChange('trainingName', e.target.value)}
                placeholder="研修名を入力してください"
                error={errors.trainingName}
                disabled={isLoading}
              />
            </div>

            {/* カテゴリ */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                カテゴリ <span className="text-red-500">*</span>
              </label>
              <Select
                value={formData.category}
                onChange={(value) => handleInputChange('category', value)}
                options={categories}
                placeholder="カテゴリを選択してください"
                error={!!errors.category}
                disabled={isLoading}
              />
              {errors.category && (
                <p className="text-sm text-red-600 mt-1" role="alert">
                  {errors.category}
                </p>
              )}
            </div>

            {/* 日付 */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  開始日 <span className="text-red-500">*</span>
                </label>
                <Input
                  type="date"
                  value={formData.startDate}
                  onChange={(e) => handleInputChange('startDate', e.target.value)}
                  min="1900-01-01"
                  max="9999-12-31"
                  error={errors.startDate}
                  disabled={isLoading}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  終了日 <span className="text-red-500">*</span>
                </label>
                <Input
                  type="date"
                  value={formData.endDate}
                  onChange={(e) => handleInputChange('endDate', e.target.value)}
                  min="1900-01-01"
                  max="9999-12-31"
                  error={errors.endDate}
                  disabled={isLoading}
                />
              </div>
            </div>

            {/* 時間数・PDUポイント */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  時間数 <span className="text-red-500">*</span>
                </label>
                <Input
                  type="number"
                  value={formData.hours}
                  onChange={(e) => handleInputChange('hours', parseInt(e.target.value) || 0)}
                  placeholder="時間数"
                  min="1"
                  max="999"
                  error={errors.hours}
                  disabled={isLoading}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  PDUポイント
                </label>
                <Input
                  type="number"
                  value={formData.pduPoints}
                  onChange={(e) => handleInputChange('pduPoints', parseInt(e.target.value) || 0)}
                  placeholder="PDUポイント"
                  min="0"
                  max="999"
                  error={errors.pduPoints}
                  disabled={isLoading}
                />
              </div>
            </div>

            {/* 習得スキル */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                習得スキル
              </label>
              <div className="flex gap-2 mb-2">
                <Input
                  type="text"
                  value={skillInput}
                  onChange={(e) => setSkillInput(e.target.value)}
                  onKeyDown={handleSkillInputKeyPress}
                  placeholder="スキルを入力してEnterキーで追加"
                  disabled={isLoading}
                />
                <Button
                  type="button"
                  onClick={handleAddSkill}
                  variant="secondary"
                  disabled={!skillInput.trim() || isLoading}
                >
                  追加
                </Button>
              </div>
              {formData.skills.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {formData.skills.map((skill, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800"
                    >
                      {skill}
                      <button
                        type="button"
                        onClick={() => handleRemoveSkill(skill)}
                        className="ml-2 text-blue-600 hover:text-blue-800"
                        disabled={isLoading}
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>

            {/* 説明 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                説明
              </label>
              <textarea
                value={formData.description}
                onChange={(e) => handleInputChange('description', e.target.value)}
                placeholder="研修の内容や学習目標を入力してください"
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={isLoading}
              />
            </div>

            {/* ボタン */}
            <div className="flex justify-end space-x-3 pt-4">
              <Button
                type="button"
                onClick={onCancel}
                variant="secondary"
                disabled={isLoading}
              >
                キャンセル
              </Button>
              <Button
                type="submit"
                variant="primary"
                disabled={isLoading}
              >
                {isLoading ? '保存中...' : '保存'}
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
