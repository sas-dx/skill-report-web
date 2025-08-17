/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: キャリアパスタイムラインコンポーネント
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { RefreshCw, MapPin, Calendar, CheckCircle, Clock, AlertCircle, Plus, Edit2, Trash2, X } from 'lucide-react';
import { CareerPathForm, CareerPathStep as FormCareerPathStep } from './CareerPathForm';
import { PlusIcon, PencilIcon, TrashIcon, XIcon } from '@/components/ui/Icons';

// 型定義
interface RequiredSkill {
  skill_id: string;
  skill_name: string;
  required_level: number;
  current_level: number;
  is_achieved: boolean;
}

interface CareerPathStep {
  step_id: string;
  position_name?: string;
  position_level?: number;
  step_name?: string;
  step_description?: string;
  description?: string;
  target_date?: string;
  estimated_duration?: string;
  completion_date?: string;
  status?: 'not_started' | 'in_progress' | 'completed' | 'overdue';
  required_skills?: RequiredSkill[];
  prerequisites?: string[];
  milestones?: string[];
  progress_percentage?: number;
  is_current?: boolean;
  is_completed?: boolean;
}

interface CareerPathTimelineProps {
  userId?: string;
  className?: string;
}

/**
 * キャリアパスタイムラインコンポーネント
 */
export function CareerPathTimeline({ userId, className }: CareerPathTimelineProps) {
  const [careerPath, setCareerPath] = useState<CareerPathStep[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingStep, setEditingStep] = useState<CareerPathStep | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  /**
   * キャリアパスデータを取得
   */
  const fetchCareerPath = async () => {
    try {
      setIsLoading(true);
      setError(null);

      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      if (userId) {
        headers['x-user-id'] = userId;
      }

      const response = await fetch('/api/career/path', {
        method: 'GET',
        headers,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('キャリアパスAPIレスポンス:', data);

      if (data.success && data.data) {
        const steps = data.data.career_path?.steps || [];
        console.log('キャリアパスステップ:', steps);
        // 各ステップのstep_idを確認
        steps.forEach((step: CareerPathStep, index: number) => {
          console.log(`ステップ${index + 1}: step_id=${step.step_id}, position_name=${step.position_name}`);
        });
        setCareerPath(steps);
      } else {
        throw new Error(data.error?.message || 'キャリアパスデータの取得に失敗しました');
      }

    } catch (err) {
      console.error('キャリアパスデータ取得エラー:', err);
      setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCareerPath();
  }, [userId]);

  /**
   * ステップ編集ハンドラー
   */
  const handleEditStep = (step: CareerPathStep) => {
    console.log('編集するステップ:', step);
    // step_idが文字列として存在し、空文字でないかチェック
    if (!step.step_id || step.step_id === '') {
      console.error('ステップIDが存在しません:', step);
      setError('このステップは編集できません（IDが不明です）');
      return;
    }
    setEditingStep(step);
    setIsDialogOpen(true);
  };

  /**
   * ステップ削除ハンドラー
   */
  const handleDeleteStep = async (stepId: string) => {
    if (!stepId || stepId === '') {
      console.error('ステップIDが指定されていません');
      return;
    }
    if (!window.confirm('このキャリアパスステップを削除してもよろしいですか？')) {
      return;
    }

    try {
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      if (userId) {
        headers['x-user-id'] = userId;
      }

      const response = await fetch(`/api/career/path/${stepId}`, {
        method: 'DELETE',
        headers,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      await fetchCareerPath();
    } catch (err) {
      console.error('キャリアパス削除エラー:', err);
      setError(err instanceof Error ? err.message : '削除に失敗しました');
    }
  };

  /**
   * フォーム送信ハンドラー
   */
  const handleSubmit = async (formData: FormCareerPathStep) => {
    try {
      setIsSubmitting(true);
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      if (userId) {
        headers['x-user-id'] = userId;
      }

      // デバッグログ追加
      console.log('編集中のステップ:', editingStep);
      console.log('送信データ:', formData);
      
      // 編集時は、step_idがあるか確認
      const stepId = editingStep?.step_id || formData.step_id;
      
      const url = editingStep && stepId
        ? `/api/career/path/${stepId}`
        : '/api/career/path';
      
      const method = editingStep && stepId ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers,
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      setIsDialogOpen(false);
      setEditingStep(null);
      await fetchCareerPath();
    } catch (err) {
      console.error('キャリアパス保存エラー:', err);
      setError(err instanceof Error ? err.message : '保存に失敗しました');
    } finally {
      setIsSubmitting(false);
    }
  };

  /**
   * ステータスに応じたアイコンを取得
   */
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'in_progress':
        return <Clock className="h-5 w-5 text-blue-500" />;
      case 'overdue':
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      default:
        return <MapPin className="h-5 w-5 text-gray-400" />;
    }
  };

  /**
   * ステータスに応じたバッジバリアントを取得
   */
  const getStatusVariant = (status: string): "default" | "secondary" | "destructive" | "outline" => {
    switch (status) {
      case 'completed':
        return 'secondary';
      case 'in_progress':
        return 'default';
      case 'overdue':
        return 'destructive';
      default:
        return 'outline';
    }
  };

  /**
   * ステータスの日本語表示を取得
   */
  const getStatusText = (status: string) => {
    switch (status) {
      case 'completed':
        return '完了';
      case 'in_progress':
        return '進行中';
      case 'overdue':
        return '遅延';
      case 'not_started':
        return '未開始';
      default:
        return '不明';
    }
  };

  /**
   * 日付をフォーマット
   */
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ja-JP', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  if (isLoading) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <MapPin className="h-5 w-5" />
            キャリアパス
          </CardTitle>
          <CardDescription>
            目標達成までのステップを段階的に表示
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center h-64">
            <RefreshCw className="h-8 w-8 animate-spin text-gray-400" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <AlertCircle className="h-5 w-5 text-red-500" />
            キャリアパス
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <p className="text-red-600 mb-4">{error}</p>
            <Button onClick={fetchCareerPath} variant="outline">
              <RefreshCw className="h-4 w-4 mr-2" />
              再試行
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (careerPath.length === 0) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <MapPin className="h-5 w-5" />
            キャリアパス
          </CardTitle>
          <CardDescription>
            目標達成までのステップを段階的に表示
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <p className="text-gray-500 mb-4">キャリアパスが設定されていません</p>
            <Button onClick={() => { setEditingStep(null); setIsDialogOpen(true); }}>
              <PlusIcon className="h-4 w-4 mr-2" />
              キャリアパスを作成
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <MapPin className="h-5 w-5" />
              キャリアパス
            </CardTitle>
            <CardDescription>
              目標達成までのステップを段階的に表示
            </CardDescription>
          </div>
          <div className="flex items-center space-x-2">
            <Button onClick={() => { setEditingStep(null); setIsDialogOpen(true); }} variant="secondary" size="sm">
              <PlusIcon className="h-4 w-4 mr-1" />
              追加
            </Button>
            <Button onClick={fetchCareerPath} variant="outline" size="sm">
              <RefreshCw className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* タイムライン */}
          <div className="relative">
            {careerPath.map((step, index) => (
              <div key={step.step_id} className="relative flex items-start space-x-4 pb-8">
                {/* タイムライン線 */}
                {index < careerPath.length - 1 && (
                  <div className="absolute left-6 top-12 w-0.5 h-full bg-gray-200" />
                )}
                
                {/* ステップアイコン */}
                <div className="flex-shrink-0 w-12 h-12 bg-white border-2 border-gray-200 rounded-full flex items-center justify-center relative z-10">
                  {getStatusIcon(step.status)}
                </div>

                {/* ステップ内容 */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <h4 className="text-lg font-semibold text-gray-900">
                        {step.position_name || step.step_name || ''}
                      </h4>
                      {step.status && (
                        <Badge variant={getStatusVariant(step.status)}>
                          {getStatusText(step.status)}
                        </Badge>
                      )}
                    </div>
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => handleEditStep(step)}
                        className="text-gray-400 hover:text-blue-600 transition-colors"
                      >
                        <PencilIcon className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => step.step_id && handleDeleteStep(step.step_id)}
                        className="text-gray-400 hover:text-red-600 transition-colors"
                        disabled={!step.step_id}
                      >
                        <TrashIcon className="h-4 w-4" />
                      </button>
                    </div>
                  </div>

                  <p className="text-sm text-gray-600 mb-3">
                    {step.description || step.step_description || ''}
                  </p>

                  {/* 日付情報 */}
                  {(step.estimated_duration || step.target_date || step.completion_date) && (
                    <div className="flex items-center gap-4 mb-3 text-sm text-gray-500">
                      {step.estimated_duration && (
                        <div className="flex items-center gap-1">
                          <Calendar className="h-4 w-4" />
                          <span>期間: {step.estimated_duration}</span>
                        </div>
                      )}
                      {step.completion_date && (
                        <div className="flex items-center gap-1">
                          <CheckCircle className="h-4 w-4" />
                          <span>完了: {formatDate(step.completion_date)}</span>
                        </div>
                      )}
                    </div>
                  )}

                  {/* 進捗バー */}
                  {step.progress_percentage !== undefined && (
                    <div className="mb-3">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-medium text-gray-700">進捗</span>
                        <span className="text-sm text-gray-500">{step.progress_percentage || 0}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${step.progress_percentage || 0}%` }}
                        />
                      </div>
                    </div>
                  )}

                  {/* 必要スキル */}
                  {step.required_skills && step.required_skills.length > 0 && (
                    <div className="mb-3">
                      <h5 className="text-sm font-medium text-gray-700 mb-2">必要スキル</h5>
                      <div className="flex flex-wrap gap-1">
                        {step.required_skills.map((skill, skillIndex) => (
                          <Badge 
                            key={skillIndex} 
                            variant={skill.is_achieved ? "secondary" : "outline"} 
                            className="text-xs"
                          >
                            {skill.skill_name} (Lv.{skill.current_level}/{skill.required_level})
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* 前提条件 */}
                  {step.prerequisites && step.prerequisites.length > 0 && (
                    <div>
                      <h5 className="text-sm font-medium text-gray-700 mb-2">前提条件</h5>
                      <ul className="text-sm text-gray-600 space-y-1">
                        {step.prerequisites.map((prerequisite, index) => (
                          <li key={index} className="flex items-start gap-2">
                            <span className="text-gray-400 mt-1">•</span>
                            <span>{prerequisite}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* 統計情報 */}
          <div className="grid grid-cols-4 gap-4 pt-4 border-t">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {careerPath.length}
              </div>
              <div className="text-xs text-gray-500">総ステップ数</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {careerPath.filter(step => step.is_completed === true).length}
              </div>
              <div className="text-xs text-gray-500">完了</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {careerPath.filter(step => step.is_current === true).length}
              </div>
              <div className="text-xs text-gray-500">現在</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-600">
                {careerPath.filter(step => !step.is_completed && !step.is_current).length}
              </div>
              <div className="text-xs text-gray-500">未着手</div>
            </div>
          </div>
        </div>
      </CardContent>

      {/* キャリアパス作成・編集ダイアログ */}
      {isDialogOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex min-h-screen items-center justify-center p-4">
            {/* オーバーレイ */}
            <div 
              className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
              onClick={() => setIsDialogOpen(false)}
            />
            
            {/* ダイアログコンテンツ */}
            <div className="relative bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
              {/* ヘッダー */}
              <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-medium text-gray-900">
                  {editingStep ? 'キャリアパスを編集' : '新しいキャリアパスを作成'}
                </h2>
                <button
                  onClick={() => setIsDialogOpen(false)}
                  className="text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-md p-1"
                >
                  <XIcon className="h-5 w-5" />
                </button>
              </div>
              
              {/* フォーム */}
              <div className="px-6 py-4">
                <CareerPathForm
                  step={editingStep as FormCareerPathStep}
                  onSubmit={handleSubmit}
                  onCancel={() => setIsDialogOpen(false)}
                  isLoading={isSubmitting}
                />
              </div>
            </div>
          </div>
        </div>
      )}
    </Card>
  );
}

export default CareerPathTimeline;
