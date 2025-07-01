/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: キャリア進捗チャートコンポーネント
 */

'use client';

import React, { useMemo } from 'react';
import { ProgressData, CareerGoalData, SkillGapData, SkillProgress } from '@/types/career';

/**
 * キャリア進捗チャートのプロパティ
 */
interface CareerProgressChartProps {
  careerGoal: CareerGoalData | null;
  year: number;
  isLoading?: boolean;
}

/**
 * キャリア進捗チャートコンポーネント
 * 
 * 機能:
 * - 全体進捗の円グラフ表示
 * - スキル別進捗の棒グラフ表示
 * - アクションプラン進捗の表示
 */
export function CareerProgressChart({ 
  careerGoal, 
  year,
  isLoading = false 
}: CareerProgressChartProps) {
  
  // CareerGoalDataからProgressDataを生成
  const progressData = useMemo((): ProgressData | null => {
    if (!careerGoal) return null;

    // モックスキル進捗データを生成
    const skillProgress: SkillProgress[] = [
      {
        skill_name: 'リーダーシップ',
        current_level: parseInt(careerGoal.current_level) || 1,
        target_level: parseInt(careerGoal.target_level) || 4,
        progress_percentage: ((parseInt(careerGoal.current_level) || 1) / (parseInt(careerGoal.target_level) || 4)) * 100,
        category: 'management'
      },
      {
        skill_name: 'プロジェクト管理',
        current_level: 2,
        target_level: 4,
        progress_percentage: 50,
        category: 'management'
      },
      {
        skill_name: 'チームマネジメント',
        current_level: 1,
        target_level: 3,
        progress_percentage: 33,
        category: 'management'
      },
      {
        skill_name: '戦略立案',
        current_level: 2,
        target_level: 4,
        progress_percentage: 50,
        category: 'strategy'
      }
    ];

    return {
      overall_progress: careerGoal.progress_percentage || 0,
      skill_progress: skillProgress,
      action_plan_progress: {
        total_count: 8,
        completed_count: 3,
        in_progress_count: 3,
        not_started_count: 2,
        completion_rate: 37.5,
      },
      last_updated: new Date().toISOString(),
    };
  }, [careerGoal]);
  
  // ローディング表示
  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="bg-gray-200 rounded-lg h-64"></div>
        </div>
      </div>
    );
  }

  // データが存在しない場合
  if (!progressData) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-400 mb-4">
          <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          進捗データがありません
        </h3>
        <p className="text-sm text-gray-500">
          キャリア目標を設定すると、進捗が表示されます。
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* 全体進捗 */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">全体進捗</h3>
        <div className="flex items-center justify-center">
          <div className="relative w-32 h-32">
            {/* 円形進捗バー */}
            <svg className="w-32 h-32 transform -rotate-90" viewBox="0 0 120 120">
              <circle
                cx="60"
                cy="60"
                r="50"
                stroke="currentColor"
                strokeWidth="8"
                fill="transparent"
                className="text-gray-200"
              />
              <circle
                cx="60"
                cy="60"
                r="50"
                stroke="currentColor"
                strokeWidth="8"
                fill="transparent"
                strokeDasharray={`${2 * Math.PI * 50}`}
                strokeDashoffset={`${2 * Math.PI * 50 * (1 - progressData.overall_progress / 100)}`}
                className="text-blue-500 transition-all duration-300"
                strokeLinecap="round"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-2xl font-bold text-gray-900">
                {progressData.overall_progress}%
              </span>
            </div>
          </div>
        </div>
        <p className="text-center text-sm text-gray-600 mt-4">
          最終更新: {new Date(progressData.last_updated).toLocaleDateString('ja-JP')}
        </p>
      </div>

      {/* スキル別進捗 */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">スキル別進捗</h3>
        <div className="space-y-4">
          {progressData.skill_progress.map((skill, index) => (
            <div key={index} className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="font-medium text-gray-900">{skill.skill_name}</span>
                <span className="text-gray-600">
                  {skill.current_level} → {skill.target_level} ({skill.progress_percentage}%)
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${skill.progress_percentage}%` }}
                ></div>
              </div>
              <div className="text-xs text-gray-500">
                カテゴリ: {skill.category}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* アクションプラン進捗 */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">アクションプラン進捗</h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-900">
              {progressData.action_plan_progress.total_count}
            </div>
            <div className="text-sm text-gray-600">総数</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {progressData.action_plan_progress.completed_count}
            </div>
            <div className="text-sm text-gray-600">完了</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">
              {progressData.action_plan_progress.in_progress_count}
            </div>
            <div className="text-sm text-gray-600">進行中</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-600">
              {progressData.action_plan_progress.not_started_count}
            </div>
            <div className="text-sm text-gray-600">未着手</div>
          </div>
        </div>
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="font-medium text-gray-900">完了率</span>
            <span className="text-gray-600">
              {progressData.action_plan_progress.completion_rate}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className="bg-green-500 h-3 rounded-full transition-all duration-300"
              style={{ width: `${progressData.action_plan_progress.completion_rate}%` }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
}
