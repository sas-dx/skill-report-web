/**
 * 要求仕様ID: TRN.1-ATT.1
 * 対応設計書: docs/design/screens/specs/画面設計書_SCR-TRAINING_研修管理画面.md
 * 実装内容: 資格情報登録フォーム
 */

'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';

interface CertificationFormData {
  certificationName: string;
  issuingOrganization: string;
  category: string;
  level: string;
  status: 'acquired' | 'expired' | 'planned';
  acquisitionDate?: string;
  expiryDate?: string;
  plannedDate?: string;
  certificationNumber?: string;
  score?: number;
  description: string;
}

interface CertificationFormProps {
  onSave: (data: any) => void;
  onCancel: () => void;
  isLoading: boolean;
  initialData?: any; // 編集時の初期データ
}

export function CertificationForm({ onSave, onCancel, isLoading, initialData }: CertificationFormProps) {
  const [formData, setFormData] = useState<CertificationFormData>({
    certificationName: initialData?.certificationName || '',
    issuingOrganization: initialData?.organization || '',
    category: initialData?.category || 'technical',
    level: initialData?.level || 'basic',
    status: initialData?.status || 'acquired',
    acquisitionDate: initialData?.acquiredDate || '',
    expiryDate: initialData?.expiryDate === '無期限' ? '' : initialData?.expiryDate || '',
    plannedDate: initialData?.plannedDate || '',
    certificationNumber: initialData?.score || '',
    description: initialData?.description || ''
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const categoryOptions = [
    { value: 'technical', label: '技術系' },
    { value: 'business', label: 'ビジネス系' },
    { value: 'language', label: '語学系' },
    { value: 'project', label: 'プロジェクト管理' },
    { value: 'security', label: 'セキュリティ' },
    { value: 'other', label: 'その他' }
  ];

  const levelOptions = [
    { value: 'basic', label: '基礎' },
    { value: 'intermediate', label: '中級' },
    { value: 'advanced', label: '上級' },
    { value: 'expert', label: 'エキスパート' }
  ];

  const statusOptions = [
    { value: 'acquired', label: '取得済み' },
    { value: 'planned', label: '取得予定' },
    { value: 'expired', label: '期限切れ' }
  ];

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.certificationName.trim()) {
      newErrors.certificationName = '資格名は必須です';
    }

    if (!formData.issuingOrganization.trim()) {
      newErrors.issuingOrganization = '発行機関は必須です';
    }

    if (formData.status === 'acquired' && !formData.acquisitionDate) {
      newErrors.acquisitionDate = '取得済みの場合、取得日は必須です';
    }

    if (formData.status === 'planned' && !formData.plannedDate) {
      newErrors.plannedDate = '取得予定の場合、予定日は必須です';
    }

    if (formData.score && (formData.score < 0 || formData.score > 1000)) {
      newErrors.score = 'スコアは0-1000の範囲で入力してください';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    try {
      // 編集時は既存のIDを含めてデータを送信
      const dataToSave = {
        ...formData,
        id: initialData?.id // 編集時のIDを含める
      };
      await onSave(dataToSave);
    } catch (error) {
      console.error('資格情報保存エラー:', error);
    }
  };

  const handleInputChange = (field: keyof CertificationFormData, value: string | number | undefined) => {
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

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-900">
              {initialData ? '資格情報編集' : '新規資格登録'}
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

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* 基本情報 */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Input
                  label="資格名"
                  value={formData.certificationName}
                  onChange={(e) => handleInputChange('certificationName', e.target.value)}
                  error={errors.certificationName}
                  required
                  placeholder="例: 基本情報技術者試験"
                />
              </div>
              <div>
                <Input
                  label="発行機関"
                  value={formData.issuingOrganization}
                  onChange={(e) => handleInputChange('issuingOrganization', e.target.value)}
                  error={errors.issuingOrganization}
                  required
                  placeholder="例: IPA（情報処理推進機構）"
                />
              </div>
            </div>

            {/* カテゴリ・レベル・ステータス */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  カテゴリ <span className="text-red-500">*</span>
                </label>
                <Select
                  value={formData.category}
                  onChange={(value) => handleInputChange('category', value)}
                  options={categoryOptions}
                  placeholder="カテゴリを選択"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  レベル <span className="text-red-500">*</span>
                </label>
                <Select
                  value={formData.level}
                  onChange={(value) => handleInputChange('level', value)}
                  options={levelOptions}
                  placeholder="レベルを選択"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  ステータス <span className="text-red-500">*</span>
                </label>
                <Select
                  value={formData.status}
                  onChange={(value) => handleInputChange('status', value as 'acquired' | 'expired' | 'planned')}
                  options={statusOptions}
                  placeholder="ステータスを選択"
                />
              </div>
            </div>

            {/* 日付情報 */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {formData.status === 'acquired' && (
                <div>
                  <Input
                    label="取得日"
                    type="date"
                    value={formData.acquisitionDate || ''}
                    onChange={(e) => handleInputChange('acquisitionDate', e.target.value)}
                    error={errors.acquisitionDate}
                    required
                    min="1990-01-01"
                    max="9999-12-31"
                  />
                </div>
              )}
              {formData.status === 'planned' && (
                <div>
                  <Input
                    label="取得予定日"
                    type="date"
                    value={formData.plannedDate || ''}
                    onChange={(e) => handleInputChange('plannedDate', e.target.value)}
                    error={errors.plannedDate}
                    required
                    min="2025-01-01"
                    max="9999-12-31"
                  />
                </div>
              )}
              {(formData.status === 'acquired' || formData.status === 'expired') && (
                <div>
                  <Input
                    label="有効期限"
                    type="date"
                    value={formData.expiryDate || ''}
                    onChange={(e) => handleInputChange('expiryDate', e.target.value)}
                    placeholder="無期限の場合は空欄"
                    min="2025-01-01"
                    max="9999-12-31"
                  />
                </div>
              )}
            </div>

            {/* 詳細情報 */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Input
                  label="認定番号"
                  value={formData.certificationNumber || ''}
                  onChange={(e) => handleInputChange('certificationNumber', e.target.value)}
                  placeholder="例: FE-2024-001234"
                />
              </div>
              <div>
                <Input
                  label="スコア"
                  type="number"
                  value={formData.score?.toString() || ''}
                  onChange={(e) => handleInputChange('score', e.target.value ? parseInt(e.target.value) : undefined)}
                  error={errors.score}
                  placeholder="例: 850"
                  min="0"
                  max="1000"
                />
              </div>
            </div>

            {/* 説明 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                説明・備考
              </label>
              <textarea
                value={formData.description}
                onChange={(e) => handleInputChange('description', e.target.value)}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="資格の詳細や取得の背景など"
              />
            </div>

            {/* アクションボタン */}
            <div className="flex justify-end space-x-3 pt-6 border-t">
              <Button
                type="button"
                variant="secondary"
                onClick={onCancel}
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
