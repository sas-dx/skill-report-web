/**
 * 要求仕様ID: SKL.1-EVAL.1, SKL.1-MAINT.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_SKL_Skill_スキル管理画面.md
 * 実装内容: スキル詳細表示・編集フォーム
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { SkillHierarchy, UserSkill, SkillFormData, SKILL_LEVELS, Certification } from '@/types/skills';

interface SkillDetailFormProps {
  selectedSkill: SkillHierarchy | null;
  userSkill: UserSkill | null;
  relatedCertifications: Certification[];
  onSave: (formData: SkillFormData) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
  isNewSkillMode?: boolean;
  customSkillName?: string;
  customSkillCategory?: string;
}

export const SkillDetailForm: React.FC<SkillDetailFormProps> = ({
  selectedSkill,
  userSkill,
  relatedCertifications,
  onSave,
  onCancel,
  isLoading = false,
  isNewSkillMode = false,
  customSkillName = '',
  customSkillCategory = 'technical'
}) => {
  const [formData, setFormData] = useState<SkillFormData>({
    skillId: '',
    level: 1,
    acquiredDate: undefined,
    experienceYears: undefined,
    lastUsed: undefined,
    remarks: undefined
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isEditing, setIsEditing] = useState(false);

  // フォームデータの初期化
  useEffect(() => {
    if (selectedSkill || isNewSkillMode) {
      setFormData({
        skillId: selectedSkill?.id || 'new-skill',
        level: userSkill?.level || 1,
        acquiredDate: userSkill?.acquiredDate || undefined,
        experienceYears: userSkill?.experienceYears || undefined,
        lastUsed: userSkill?.lastUsed || undefined,
        remarks: userSkill?.remarks || undefined
      });
      setIsEditing(!!userSkill);
    }
  }, [selectedSkill, userSkill, isNewSkillMode]);

  // バリデーション
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.skillId) {
      newErrors.skillId = 'スキルが選択されていません';
    }

    if (formData.level < 1 || formData.level > 4) {
      newErrors.level = 'スキルレベルは1から4の範囲で選択してください';
    }

    if (formData.experienceYears !== undefined && formData.experienceYears < 0) {
      newErrors.experienceYears = '経験年数は0以上で入力してください';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // フォーム送信
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    try {
      await onSave(formData);
    } catch (error) {
      console.error('スキル保存エラー:', error);
    }
  };

  // フォームフィールドの更新
  const updateField = (field: keyof SkillFormData, value: any) => {
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

  if (!selectedSkill && !isNewSkillMode) {
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6 h-full flex items-center justify-center">
        <div className="text-center text-gray-500">
          <p className="text-sm">スキルを選択してください</p>
          <p className="text-xs mt-1">左側のツリーからスキル項目を選択するか、新規スキル追加ボタンをクリックしてください</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 h-full overflow-y-auto">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900">
          {isNewSkillMode ? customSkillName || '新規スキル' : selectedSkill?.name}
        </h3>
        <p className="text-sm text-gray-600 mt-1">
          {isNewSkillMode 
            ? `${customSkillCategory} (新規作成)`
            : `${selectedSkill?.category} ${selectedSkill?.subcategory && `> ${selectedSkill.subcategory}`}`
          }
        </p>
        {selectedSkill?.description && !isNewSkillMode && (
          <p className="text-sm text-gray-500 mt-2">{selectedSkill.description}</p>
        )}
        {isNewSkillMode && (
          <p className="text-sm text-gray-500 mt-2">新規スキルとして登録されます</p>
        )}
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* スキルレベル */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            スキルレベル <span className="text-red-500">*</span>
          </label>
          <div className="grid grid-cols-2 gap-2">
            {Object.entries(SKILL_LEVELS).map(([level, info]) => (
              <label
                key={level}
                className={`
                  flex items-center p-3 border rounded-lg cursor-pointer transition-colors
                  ${formData.level === parseInt(level) 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-200 hover:border-gray-300'
                  }
                `}
              >
                <input
                  type="radio"
                  name="level"
                  value={level}
                  checked={formData.level === parseInt(level)}
                  onChange={(e) => updateField('level', parseInt(e.target.value))}
                  className="sr-only"
                />
                <span className={`text-lg font-bold mr-2 ${info.color.split(' ')[0]}`}>
                  {info.symbol}
                </span>
                <span className="text-sm font-medium">{info.label}</span>
              </label>
            ))}
          </div>
          {errors.level && (
            <p className="text-red-500 text-xs mt-1">{errors.level}</p>
          )}
        </div>

        {/* 習得日 */}
        <div>
          <label htmlFor="acquiredDate" className="block text-sm font-medium text-gray-700 mb-2">
            習得日
          </label>
          <Input
            id="acquiredDate"
            type="date"
            value={formData.acquiredDate || ''}
            onChange={(e) => updateField('acquiredDate', e.target.value || undefined)}
            className="w-full"
          />
          {errors.acquiredDate && (
            <p className="text-red-500 text-xs mt-1">{errors.acquiredDate}</p>
          )}
        </div>

        {/* 経験年数 */}
        <div>
          <label htmlFor="experienceYears" className="block text-sm font-medium text-gray-700 mb-2">
            経験年数
          </label>
          <div className="flex items-center space-x-2">
            <Input
              id="experienceYears"
              type="number"
              min="0"
              step="0.5"
              value={formData.experienceYears || ''}
              onChange={(e) => updateField('experienceYears', e.target.value ? parseFloat(e.target.value) : undefined)}
              className="w-24"
              placeholder="0"
            />
            <span className="text-sm text-gray-500">年</span>
          </div>
          {errors.experienceYears && (
            <p className="text-red-500 text-xs mt-1">{errors.experienceYears}</p>
          )}
        </div>

        {/* 最終使用日 */}
        <div>
          <label htmlFor="lastUsed" className="block text-sm font-medium text-gray-700 mb-2">
            最終使用日
          </label>
          <Input
            id="lastUsed"
            type="date"
            value={formData.lastUsed || ''}
            onChange={(e) => updateField('lastUsed', e.target.value || undefined)}
            className="w-full"
          />
          {errors.lastUsed && (
            <p className="text-red-500 text-xs mt-1">{errors.lastUsed}</p>
          )}
        </div>

        {/* 備考 */}
        <div>
          <label htmlFor="remarks" className="block text-sm font-medium text-gray-700 mb-2">
            備考
          </label>
          <textarea
            id="remarks"
            rows={3}
            value={formData.remarks || ''}
            onChange={(e) => updateField('remarks', e.target.value || undefined)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="スキルに関する補足情報があれば入力してください"
          />
          {errors.remarks && (
            <p className="text-red-500 text-xs mt-1">{errors.remarks}</p>
          )}
        </div>

        {/* 関連資格 */}
        {relatedCertifications.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-2">関連資格</h4>
            <div className="space-y-2">
              {relatedCertifications.map((cert) => (
                <div key={cert.id} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                  <div>
                    <p className="text-sm font-medium">{cert.certificationName}</p>
                    <p className="text-xs text-gray-500">
                      取得日: {cert.acquiredDate}
                      {cert.expiryDate && ` | 有効期限: ${cert.expiryDate}`}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ボタン */}
        <div className="flex justify-end space-x-3 pt-4 border-t">
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
            disabled={isLoading}
          >
            {isLoading ? '保存中...' : isEditing ? '更新' : '登録'}
          </Button>
        </div>
      </form>
    </div>
  );
};
