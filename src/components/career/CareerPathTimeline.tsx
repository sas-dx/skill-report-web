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
import { RefreshCw, MapPin, Calendar, CheckCircle, Clock, AlertCircle } from 'lucide-react';

// 型定義
interface CareerPathStep {
  step_id: string;
  step_name: string;
  step_description: string;
  target_date: string;
  completion_date?: string;
  status: 'not_started' | 'in_progress' | 'completed' | 'overdue';
  required_skills: string[];
  milestones: string[];
  progress_percentage: number;
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

      if (data.success && data.data) {
        setCareerPath(data.data.career_path_steps);
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
            <p className="text-gray-500">キャリアパスが設定されていません</p>
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
          <Button onClick={fetchCareerPath} variant="outline" size="sm">
            <RefreshCw className="h-4 w-4" />
          </Button>
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
                    <h4 className="text-lg font-semibold text-gray-900">
                      {step.step_name}
                    </h4>
                    <Badge variant={getStatusVariant(step.status)}>
                      {getStatusText(step.status)}
                    </Badge>
                  </div>

                  <p className="text-sm text-gray-600 mb-3">
                    {step.step_description}
                  </p>

                  {/* 日付情報 */}
                  <div className="flex items-center gap-4 mb-3 text-sm text-gray-500">
                    <div className="flex items-center gap-1">
                      <Calendar className="h-4 w-4" />
                      <span>目標: {formatDate(step.target_date)}</span>
                    </div>
                    {step.completion_date && (
                      <div className="flex items-center gap-1">
                        <CheckCircle className="h-4 w-4" />
                        <span>完了: {formatDate(step.completion_date)}</span>
                      </div>
                    )}
                  </div>

                  {/* 進捗バー */}
                  <div className="mb-3">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-medium text-gray-700">進捗</span>
                      <span className="text-sm text-gray-500">{step.progress_percentage}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${step.progress_percentage}%` }}
                      />
                    </div>
                  </div>

                  {/* 必要スキル */}
                  {step.required_skills.length > 0 && (
                    <div className="mb-3">
                      <h5 className="text-sm font-medium text-gray-700 mb-2">必要スキル</h5>
                      <div className="flex flex-wrap gap-1">
                        {step.required_skills.map((skill, skillIndex) => (
                          <Badge key={skillIndex} variant="outline" className="text-xs">
                            {skill}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* マイルストーン */}
                  {step.milestones.length > 0 && (
                    <div>
                      <h5 className="text-sm font-medium text-gray-700 mb-2">マイルストーン</h5>
                      <ul className="text-sm text-gray-600 space-y-1">
                        {step.milestones.map((milestone, milestoneIndex) => (
                          <li key={milestoneIndex} className="flex items-start gap-2">
                            <span className="text-gray-400 mt-1">•</span>
                            <span>{milestone}</span>
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
                {careerPath.filter(step => step.status === 'completed').length}
              </div>
              <div className="text-xs text-gray-500">完了</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {careerPath.filter(step => step.status === 'in_progress').length}
              </div>
              <div className="text-xs text-gray-500">進行中</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-red-600">
                {careerPath.filter(step => step.status === 'overdue').length}
              </div>
              <div className="text-xs text-gray-500">遅延</div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default CareerPathTimeline;
