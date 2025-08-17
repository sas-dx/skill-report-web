/**
 * 研修記録フォームコンポーネント
 */

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { X, Save, Calendar, Clock, Users, MapPin, DollarSign, Award } from 'lucide-react';

interface TrainingRecord {
  id?: string;
  trainingName: string;
  trainingType: string;
  trainingCategory: string;
  providerName: string;
  instructorName?: string;
  startDate: string;
  endDate: string;
  durationHours: number;
  location?: string;
  cost?: number;
  attendanceStatus: string;
  completionRate: number;
  testScore?: number;
  certificateObtained: boolean;
  satisfactionScore?: number;
}

interface TrainingFormProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (record: TrainingRecord) => Promise<void>;
  editingRecord?: TrainingRecord | null;
}

export default function TrainingForm({
  isOpen,
  onClose,
  onSave,
  editingRecord
}: TrainingFormProps) {
  const [formData, setFormData] = useState<TrainingRecord>({
    trainingName: '',
    trainingType: 'EXTERNAL',
    trainingCategory: '技術研修',
    providerName: '',
    instructorName: '',
    startDate: '',
    endDate: '',
    durationHours: 0,
    location: '',
    cost: 0,
    attendanceStatus: 'REGISTERED',
    completionRate: 0,
    testScore: 0,
    certificateObtained: false,
    satisfactionScore: 0
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  // 編集時のデータ設定
  useEffect(() => {
    if (editingRecord) {
      setFormData(editingRecord);
    } else {
      setFormData({
        trainingName: '',
        trainingType: 'EXTERNAL',
        trainingCategory: '技術研修',
        providerName: '',
        instructorName: '',
        startDate: '',
        endDate: '',
        durationHours: 0,
        location: '',
        cost: 0,
        attendanceStatus: 'REGISTERED',
        completionRate: 0,
        testScore: 0,
        certificateObtained: false,
        satisfactionScore: 0
      });
    }
    setErrors({});
  }, [editingRecord, isOpen]);

  // バリデーション
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.trainingName.trim()) {
      newErrors.trainingName = '研修名は必須です';
    }

    if (!formData.providerName.trim()) {
      newErrors.providerName = '提供元は必須です';
    }

    if (!formData.startDate) {
      newErrors.startDate = '開始日は必須です';
    }

    if (!formData.endDate) {
      newErrors.endDate = '終了日は必須です';
    }

    if (formData.startDate && formData.endDate && formData.startDate > formData.endDate) {
      newErrors.endDate = '終了日は開始日以降である必要があります';
    }

    if (formData.durationHours <= 0) {
      newErrors.durationHours = '研修時間は1時間以上である必要があります';
    }

    if (formData.completionRate < 0 || formData.completionRate > 100) {
      newErrors.completionRate = '完了率は0-100%の範囲で入力してください';
    }

    if (formData.testScore !== undefined && (formData.testScore < 0 || formData.testScore > 100)) {
      newErrors.testScore = 'テストスコアは0-100点の範囲で入力してください';
    }

    if (formData.satisfactionScore !== undefined && (formData.satisfactionScore < 0 || formData.satisfactionScore > 5)) {
      newErrors.satisfactionScore = '満足度は0-5の範囲で入力してください';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // フォーム送信
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setIsSubmitting(true);
    try {
      await onSave(formData);
      onClose();
    } catch (error) {
      console.error('研修記録保存エラー:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  // 入力値更新
  const updateField = (field: keyof TrainingRecord, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // エラーをクリア
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <Card className="border-0 shadow-none">
          <CardHeader className="border-b">
            <div className="flex items-center justify-between">
              <CardTitle className="text-xl">
                {editingRecord ? '研修記録を編集' : '新しい研修記録を追加'}
              </CardTitle>
              <Button
                variant="outline"
                size="sm"
                onClick={onClose}
                disabled={isSubmitting}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          </CardHeader>

          <CardContent className="p-6">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* 基本情報 */}
              <div>
                <h3 className="text-lg font-semibold mb-4 flex items-center">
                  <Users className="h-5 w-5 mr-2" />
                  基本情報
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      研修名 <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      value={formData.trainingName}
                      onChange={(e) => updateField('trainingName', e.target.value)}
                      className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                        errors.trainingName ? 'border-red-500' : 'border-gray-300'
                      }`}
                      placeholder="研修名を入力"
                    />
                    {errors.trainingName && <p className="text-red-500 text-sm mt-1">{errors.trainingName}</p>}
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">研修タイプ</label>
                    <select
                      value={formData.trainingType}
                      onChange={(e) => updateField('trainingType', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="EXTERNAL">外部研修</option>
                      <option value="INTERNAL">社内研修</option>
                      <option value="ONLINE">オンライン研修</option>
                      <option value="SELF_STUDY">自己学習</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">カテゴリ</label>
                    <select
                      value={formData.trainingCategory}
                      onChange={(e) => updateField('trainingCategory', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="技術研修">技術研修</option>
                      <option value="ビジネススキル">ビジネススキル</option>
                      <option value="マネジメント">マネジメント</option>
                      <option value="コンプライアンス">コンプライアンス</option>
                      <option value="資格取得">資格取得</option>
                      <option value="その他">その他</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">
                      提供元 <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      value={formData.providerName}
                      onChange={(e) => updateField('providerName', e.target.value)}
                      className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                        errors.providerName ? 'border-red-500' : 'border-gray-300'
                      }`}
                      placeholder="研修提供元を入力"
                    />
                    {errors.providerName && <p className="text-red-500 text-sm mt-1">{errors.providerName}</p>}
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">講師名</label>
                    <input
                      type="text"
                      value={formData.instructorName || ''}
                      onChange={(e) => updateField('instructorName', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="講師名を入力（任意）"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">場所</label>
                    <input
                      type="text"
                      value={formData.location || ''}
                      onChange={(e) => updateField('location', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="研修場所を入力（任意）"
                    />
                  </div>
                </div>
              </div>

              {/* 日程・時間 */}
              <div>
                <h3 className="text-lg font-semibold mb-4 flex items-center">
                  <Calendar className="h-5 w-5 mr-2" />
                  日程・時間
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      開始日 <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="date"
                      value={formData.startDate}
                      onChange={(e) => updateField('startDate', e.target.value)}
                      className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                        errors.startDate ? 'border-red-500' : 'border-gray-300'
                      }`}
                    />
                    {errors.startDate && <p className="text-red-500 text-sm mt-1">{errors.startDate}</p>}
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">
                      終了日 <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="date"
                      value={formData.endDate}
                      onChange={(e) => updateField('endDate', e.target.value)}
                      className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                        errors.endDate ? 'border-red-500' : 'border-gray-300'
                      }`}
                    />
                    {errors.endDate && <p className="text-red-500 text-sm mt-1">{errors.endDate}</p>}
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">
                      研修時間（時間） <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="number"
                      min="0"
                      step="0.5"
                      value={formData.durationHours}
                      onChange={(e) => updateField('durationHours', parseFloat(e.target.value) || 0)}
                      className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                        errors.durationHours ? 'border-red-500' : 'border-gray-300'
                      }`}
                    />
                    {errors.durationHours && <p className="text-red-500 text-sm mt-1">{errors.durationHours}</p>}
                  </div>
                </div>
              </div>

              {/* 進捗・評価 */}
              <div>
                <h3 className="text-lg font-semibold mb-4 flex items-center">
                  <Award className="h-5 w-5 mr-2" />
                  進捗・評価
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">受講状況</label>
                    <select
                      value={formData.attendanceStatus}
                      onChange={(e) => updateField('attendanceStatus', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="REGISTERED">申込済</option>
                      <option value="IN_PROGRESS">受講中</option>
                      <option value="COMPLETED">完了</option>
                      <option value="CANCELLED">キャンセル</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">完了率（%）</label>
                    <input
                      type="number"
                      min="0"
                      max="100"
                      value={formData.completionRate}
                      onChange={(e) => updateField('completionRate', parseInt(e.target.value) || 0)}
                      className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                        errors.completionRate ? 'border-red-500' : 'border-gray-300'
                      }`}
                    />
                    {errors.completionRate && <p className="text-red-500 text-sm mt-1">{errors.completionRate}</p>}
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">テストスコア（点）</label>
                    <input
                      type="number"
                      min="0"
                      max="100"
                      value={formData.testScore || ''}
                      onChange={(e) => updateField('testScore', e.target.value ? parseInt(e.target.value) : undefined)}
                      className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                        errors.testScore ? 'border-red-500' : 'border-gray-300'
                      }`}
                      placeholder="テストスコア（任意）"
                    />
                    {errors.testScore && <p className="text-red-500 text-sm mt-1">{errors.testScore}</p>}
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">満足度（1-5）</label>
                    <input
                      type="number"
                      min="0"
                      max="5"
                      value={formData.satisfactionScore || ''}
                      onChange={(e) => updateField('satisfactionScore', e.target.value ? parseInt(e.target.value) : undefined)}
                      className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                        errors.satisfactionScore ? 'border-red-500' : 'border-gray-300'
                      }`}
                      placeholder="満足度（任意）"
                    />
                    {errors.satisfactionScore && <p className="text-red-500 text-sm mt-1">{errors.satisfactionScore}</p>}
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">費用（円）</label>
                    <input
                      type="number"
                      min="0"
                      value={formData.cost || ''}
                      onChange={(e) => updateField('cost', e.target.value ? parseInt(e.target.value) : undefined)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="研修費用（任意）"
                    />
                  </div>

                  <div className="flex items-center">
                    <label className="flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={formData.certificateObtained}
                        onChange={(e) => updateField('certificateObtained', e.target.checked)}
                        className="mr-2"
                      />
                      <span className="text-sm font-medium">資格・証明書を取得</span>
                    </label>
                  </div>
                </div>
              </div>

              {/* アクションボタン */}
              <div className="flex justify-end space-x-4 pt-4 border-t">
                <Button
                  type="button"
                  variant="outline"
                  onClick={onClose}
                  disabled={isSubmitting}
                >
                  キャンセル
                </Button>
                <Button
                  type="submit"
                  disabled={isSubmitting}
                  className="min-w-[120px]"
                >
                  {isSubmitting ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      保存中...
                    </>
                  ) : (
                    <>
                      <Save className="h-4 w-4 mr-2" />
                      {editingRecord ? '更新' : '保存'}
                    </>
                  )}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}