/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: スキルギャップレーダーチャートコンポーネント
 */

'use client';

import React, { useState, useEffect } from 'react';
import { 
  Radar, 
  RadarChart, 
  PolarGrid, 
  PolarAngleAxis, 
  PolarRadiusAxis, 
  ResponsiveContainer,
  Legend,
  Tooltip
} from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { RefreshCw, TrendingUp, AlertTriangle } from 'lucide-react';

// 型定義
interface SkillGapData {
  skill: string;
  current: number;
  target: number;
  gap: number;
  category: string;
  priority: 'high' | 'medium' | 'low';
}

interface SkillGapRadarChartProps {
  userId?: string;
  className?: string;
}

/**
 * スキルギャップレーダーチャートコンポーネント
 */
export function SkillGapRadarChart({ userId, className }: SkillGapRadarChartProps) {
  const [skillGapData, setSkillGapData] = useState<SkillGapData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  /**
   * スキルギャップデータを取得
   */
  const fetchSkillGapData = async () => {
    try {
      setIsLoading(true);
      setError(null);

      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      if (userId) {
        headers['x-user-id'] = userId;
      }

      const response = await fetch('/api/career/skill-gap', {
        method: 'GET',
        headers,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.success && data.data && data.data.skill_gap_data) {
        // APIレスポンスをチャート用データに変換
        const skillGapData = data.data.skill_gap_data;
        const chartData: SkillGapData[] = [];
        
        // カテゴリごとのデータを展開
        if (skillGapData.skill_categories) {
          skillGapData.skill_categories.forEach((category: any) => {
            if (category.skills && Array.isArray(category.skills)) {
              category.skills.forEach((skill: any) => {
                chartData.push({
                  skill: skill.skill_name,
                  current: skill.current_level,
                  target: skill.target_level,
                  gap: skill.gap_score / 25, // gap_scoreを0-4スケールに変換
                  category: category.category_name,
                  priority: skill.priority.toLowerCase() as 'high' | 'medium' | 'low'
                });
              });
            } else {
              // カテゴリレベルのデータ
              chartData.push({
                skill: category.category_name,
                current: category.current_level,
                target: category.target_level,
                gap: category.gap_score / 25,
                category: category.category_name,
                priority: category.gap_score >= 75 ? 'high' : category.gap_score >= 50 ? 'medium' : 'low'
              });
            }
          });
        }

        setSkillGapData(chartData);
      } else {
        throw new Error(data.error?.message || 'スキルギャップデータの取得に失敗しました');
      }

    } catch (err) {
      console.error('スキルギャップデータ取得エラー:', err);
      setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchSkillGapData();
  }, [userId]);

  /**
   * 優先度に応じた色を取得
   */
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return '#EF4444'; // red-500
      case 'medium':
        return '#F59E0B'; // amber-500
      case 'low':
        return '#10B981'; // emerald-500
      default:
        return '#6B7280'; // gray-500
    }
  };

  /**
   * 優先度に応じたバッジバリアントを取得
   */
  const getPriorityVariant = (priority: string): "default" | "secondary" | "destructive" | "outline" => {
    switch (priority) {
      case 'high':
        return 'destructive';
      case 'medium':
        return 'default';
      case 'low':
        return 'secondary';
      default:
        return 'outline';
    }
  };

  /**
   * カスタムツールチップ
   */
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border rounded-lg shadow-lg">
          <p className="font-semibold">{label}</p>
          <p className="text-sm text-gray-600">カテゴリ: {data.category}</p>
          <p className="text-sm">
            <span className="text-blue-600">現在レベル: {data.current}</span>
          </p>
          <p className="text-sm">
            <span className="text-green-600">目標レベル: {data.target}</span>
          </p>
          <p className="text-sm">
            <span className="text-red-600">ギャップ: {data.gap}</span>
          </p>
          <Badge variant={getPriorityVariant(data.priority)} className="mt-1">
            {data.priority === 'high' ? '高優先度' : 
             data.priority === 'medium' ? '中優先度' : '低優先度'}
          </Badge>
        </div>
      );
    }
    return null;
  };

  if (isLoading) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            スキルギャップ分析
          </CardTitle>
          <CardDescription>
            現在のスキルレベルと目標レベルの差を可視化
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
            <AlertTriangle className="h-5 w-5 text-red-500" />
            スキルギャップ分析
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <p className="text-red-600 mb-4">{error}</p>
            <Button onClick={fetchSkillGapData} variant="outline">
              <RefreshCw className="h-4 w-4 mr-2" />
              再試行
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (skillGapData.length === 0) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            スキルギャップ分析
          </CardTitle>
          <CardDescription>
            現在のスキルレベルと目標レベルの差を可視化
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <p className="text-gray-500">スキルギャップデータがありません</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  // 高優先度のスキルギャップを抽出
  const highPriorityGaps = skillGapData.filter(item => item.priority === 'high');

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              スキルギャップ分析
            </CardTitle>
            <CardDescription>
              現在のスキルレベルと目標レベルの差を可視化
            </CardDescription>
          </div>
          <Button onClick={fetchSkillGapData} variant="outline" size="sm">
            <RefreshCw className="h-4 w-4" />
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* レーダーチャート */}
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={skillGapData}>
                <PolarGrid />
                <PolarAngleAxis 
                  dataKey="skill" 
                  tick={{ fontSize: 12 }}
                  className="text-xs"
                />
                <PolarRadiusAxis 
                  angle={90} 
                  domain={[0, 5]} 
                  tick={{ fontSize: 10 }}
                />
                <Radar
                  name="現在レベル"
                  dataKey="current"
                  stroke="#3B82F6"
                  fill="#3B82F6"
                  fillOpacity={0.2}
                  strokeWidth={2}
                />
                <Radar
                  name="目標レベル"
                  dataKey="target"
                  stroke="#10B981"
                  fill="#10B981"
                  fillOpacity={0.2}
                  strokeWidth={2}
                />
                <Legend />
                <Tooltip content={<CustomTooltip />} />
              </RadarChart>
            </ResponsiveContainer>
          </div>

          {/* 高優先度ギャップの表示 */}
          {highPriorityGaps.length > 0 && (
            <div>
              <h4 className="font-semibold text-sm mb-3 flex items-center gap-2">
                <AlertTriangle className="h-4 w-4 text-red-500" />
                優先的に改善が必要なスキル
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {highPriorityGaps.map((item, index) => (
                  <div key={index} className="p-3 border rounded-lg bg-red-50">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium text-sm">{item.skill}</span>
                      <Badge variant="destructive" className="text-xs">
                        ギャップ: {item.gap}
                      </Badge>
                    </div>
                    <div className="text-xs text-gray-600">
                      <span>現在: {item.current}</span>
                      <span className="mx-2">→</span>
                      <span>目標: {item.target}</span>
                    </div>
                    <div className="text-xs text-gray-500 mt-1">
                      {item.category}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 統計情報 */}
          <div className="grid grid-cols-3 gap-4 pt-4 border-t">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {skillGapData.length}
              </div>
              <div className="text-xs text-gray-500">評価スキル数</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-red-600">
                {highPriorityGaps.length}
              </div>
              <div className="text-xs text-gray-500">高優先度ギャップ</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {skillGapData.filter(item => item.gap === 0).length}
              </div>
              <div className="text-xs text-gray-500">目標達成済み</div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default SkillGapRadarChart;
