/**
 * 要求仕様ID: TRN.1-ATT.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_SKL_Skill_スキル管理画面.md
 * 実装内容: 資格情報入力フォーム
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Certification, CertificationFormData } from '@/types/skills';

interface CertificationFormProps {
  certification?: Certification | null;
  onSave: (data: CertificationFormData) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
}

export function CertificationForm({
  certification,
  onSave,
  onCancel,
  isLoading = false
}: CertificationFormProps) {
  const [formData, setFormData] = useState<CertificationFormData>({
    certificationName: '',
    organizationName: '',
    acquiredDate: '',
    expiryDate: '',
    score: '',
    remarks: ''
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  // 編集時の初期値設定
  useEffect(() => {
    if (certification) {
      setFormData({
        certificationName: certification.certificationName,
        organizationName: certification.organizationName || '',
        acquiredDate: certification.acquiredDate,
        expiryDate: certification.expiryDate || '',
        score: certification.score || '',
        remarks: certification.remarks || ''
      });
    }
  }, [certification]);

  // フォーム値更新
  const handleInputChange = (field: keyof CertificationFormData, value: string | undefined) => {
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

  // バリデーション
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.certificationName.trim()) {
      newErrors.certificationName = '資格名は必須です';
    }

    if (!formData.acquiredDate) {
      newErrors.acquiredDate = '取得日は必須です';
    }

    // 取得日の妥当性チェック
    if (formData.acquiredDate) {
      const acquiredDate = new Date(formData.acquiredDate);
      const today = new Date();
      if (acquiredDate > today) {
        newErrors.acquiredDate = '取得日は今日以前の日付を入力してください';
      }
    }

    // 有効期限の妥当性チェック
    if (formData.expiryDate && formData.acquiredDate) {
      const acquiredDate = new Date(formData.acquiredDate);
      const expiryDate = new Date(formData.expiryDate);
      if (expiryDate <= acquiredDate) {
        newErrors.expiryDate = '有効期限は取得日より後の日付を入力してください';
      }
    }

    // スコアの妥当性チェック
    if (formData.score !== undefined && formData.score !== '') {
      const scoreNum = parseInt(formData.score, 10);
      if (isNaN(scoreNum) || scoreNum < 0 || scoreNum > 1000) {
        newErrors.score = 'スコアは0から1000の範囲で入力してください';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // 保存処理
  const handleSave = async () => {
    if (!validateForm()) {
      return;
    }

    try {
      await onSave(formData);
    } catch (error) {
      console.error('資格情報保存エラー:', error);
    }
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-medium text-gray-900">
          {certification ? '資格情報編集' : '新規資格追加'}
        </h2>
        <p className="text-sm text-gray-600">
          {certification ? '資格情報を編集してください' : '新しい資格情報を入力してください'}
        </p>
      </div>

      <div className="p-4 space-y-4">
        {/* 資格名 */}
        <div>
          <label htmlFor="certificationName" className="block text-sm font-medium text-gray-700 mb-1">
            資格名 <span className="text-red-500">*</span>
          </label>
          <Input
            id="certificationName"
            type="text"
            value={formData.certificationName}
            onChange={(e) => handleInputChange('certificationName', e.target.value)}
            placeholder="例: AWS Certified Solutions Architect"
            error={errors.certificationName}
          />
        </div>

        {/* 認定機関 */}
        <div>
          <label htmlFor="organizationName" className="block text-sm font-medium text-gray-700 mb-1">
            認定機関
          </label>
          <Input
            id="organizationName"
            type="text"
            value={formData.organizationName}
            onChange={(e) => handleInputChange('organizationName', e.target.value)}
            placeholder="例: Amazon Web Services"
          />
        </div>

        {/* 取得日 */}
        <div>
          <label htmlFor="acquiredDate" className="block text-sm font-medium text-gray-700 mb-1">
            取得日 <span className="text-red-500">*</span>
          </label>
          <Input
            id="acquiredDate"
            type="date"
            value={formData.acquiredDate}
            onChange={(e) => handleInputChange('acquiredDate', e.target.value)}
            error={errors.acquiredDate}
          />
        </div>

        {/* 有効期限 */}
        <div>
          <label htmlFor="expiryDate" className="block text-sm font-medium text-gray-700 mb-1">
            有効期限
          </label>
          <Input
            id="expiryDate"
            type="date"
            value={formData.expiryDate}
            onChange={(e) => handleInputChange('expiryDate', e.target.value)}
            error={errors.expiryDate}
          />
          <p className="text-xs text-gray-500 mt-1">
            有効期限がない場合は空欄にしてください
          </p>
        </div>

        {/* スコア */}
        <div>
          <label htmlFor="score" className="block text-sm font-medium text-gray-700 mb-1">
            スコア
          </label>
          <Input
            id="score"
            type="number"
            min="0"
            max="1000"
            value={formData.score?.toString() || ''}
            onChange={(e) => {
              const value = e.target.value;
              handleInputChange('score', value || '');
            }}
            placeholder="例: 850"
            error={errors.score}
          />
          <p className="text-xs text-gray-500 mt-1">
            スコアがない場合は空欄にしてください
          </p>
        </div>

        {/* 備考 */}
        <div>
          <label htmlFor="remarks" className="block text-sm font-medium text-gray-700 mb-1">
            備考
          </label>
          <textarea
            id="remarks"
            rows={3}
            value={formData.remarks}
            onChange={(e) => handleInputChange('remarks', e.target.value)}
            placeholder="資格に関する補足情報があれば入力してください"
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>

      {/* フォームアクション */}
      <div className="p-4 border-t border-gray-200 flex justify-end space-x-3">
        <Button
          variant="secondary"
          onClick={onCancel}
          disabled={isLoading}
        >
          キャンセル
        </Button>
        <Button
          onClick={handleSave}
          disabled={isLoading}
        >
          {isLoading ? '保存中...' : '保存'}
        </Button>
      </div>
    </div>
  );
}
