// CAR.1-PLAN.1: キャリア目標管理画面
'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { 
  mockCareerPlan, 
  mockCareerGoals, 
  goalTypeLabels, 
  goalStatusLabels,
  type CareerGoal 
} from '@/lib/mockData';

export default function CareerPage() {
  const [careerPlan] = useState(mockCareerPlan);
  const [goals] = useState(mockCareerGoals);
  const [selectedGoalType, setSelectedGoalType] = useState<'all' | 'short' | 'medium' | 'long'>('all');

  const filteredGoals = selectedGoalType === 'all' 
    ? goals 
    : goals.filter(goal => goal.goal_type === selectedGoalType);

  const getStatusColor = (status: CareerGoal['status']) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'in_progress': return 'bg-blue-100 text-blue-800';
      case 'planning': return 'bg-yellow-100 text-yellow-800';
      case 'postponed': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getProgressColor = (progress: number) => {
    if (progress >= 80) return 'bg-green-500';
    if (progress >= 50) return 'bg-blue-500';
    if (progress >= 20) return 'bg-yellow-500';
    return 'bg-gray-300';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* ヘッダー */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">キャリア目標</h1>
          <p className="mt-2 text-gray-600">
            キャリアビジョンと目標の設定・管理を行います
          </p>
        </div>

        {/* キャリアビジョン */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-8">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">キャリアビジョン</h2>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">現在の状況</h3>
                <div className="space-y-3">
                  <div>
                    <span className="text-sm font-medium text-gray-500">現在の役職</span>
                    <p className="text-gray-900">{careerPlan.current_position}</p>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-gray-500">目標役職</span>
                    <p className="text-gray-900">{careerPlan.target_position}</p>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-gray-500">目標年</span>
                    <p className="text-gray-900">{careerPlan.target_year}年</p>
                  </div>
                </div>
              </div>
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">キャリアビジョン</h3>
                <p className="text-gray-700 leading-relaxed">
                  {careerPlan.vision}
                </p>
              </div>
            </div>
            <div className="mt-6 flex justify-end">
              <Button variant="outline">
                ビジョンを編集
              </Button>
            </div>
          </div>
        </div>

        {/* 目標一覧 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
              <h2 className="text-xl font-semibold text-gray-900">目標一覧</h2>
              <div className="mt-4 sm:mt-0 flex space-x-3">
                <select
                  value={selectedGoalType}
                  onChange={(e) => setSelectedGoalType(e.target.value as any)}
                  className="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-blue-500"
                >
                  <option value="all">すべて</option>
                  <option value="short">短期目標</option>
                  <option value="medium">中期目標</option>
                  <option value="long">長期目標</option>
                </select>
                <Button>
                  新しい目標を追加
                </Button>
              </div>
            </div>
          </div>

          <div className="p-6">
            {filteredGoals.length === 0 ? (
              <div className="text-center py-12">
                <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900">目標がありません</h3>
                <p className="mt-1 text-sm text-gray-500">
                  新しい目標を追加して、キャリア計画を始めましょう。
                </p>
                <div className="mt-6">
                  <Button>
                    最初の目標を追加
                  </Button>
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                {filteredGoals.map((goal) => (
                  <div key={goal.id} className="border border-gray-200 rounded-lg p-6">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-3">
                          <h3 className="text-lg font-medium text-gray-900">
                            {goal.title}
                          </h3>
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(goal.status)}`}>
                            {goalStatusLabels[goal.status]}
                          </span>
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                            {goalTypeLabels[goal.goal_type]}
                          </span>
                        </div>
                        <p className="text-gray-700 mb-4">
                          {goal.description}
                        </p>
                        
                        {/* 進捗バー */}
                        <div className="mb-4">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-gray-700">進捗</span>
                            <span className="text-sm text-gray-500">{goal.progress}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(goal.progress)}`}
                              style={{ width: `${goal.progress}%` }}
                            />
                          </div>
                        </div>

                        {/* 必要スキル */}
                        <div className="mb-4">
                          <span className="text-sm font-medium text-gray-700 block mb-2">必要スキル</span>
                          <div className="flex flex-wrap gap-2">
                            {goal.skills_required.map((skill, index) => (
                              <span 
                                key={index}
                                className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                              >
                                {skill}
                              </span>
                            ))}
                          </div>
                        </div>

                        {/* 期限 */}
                        <div className="text-sm text-gray-500">
                          目標期限: {new Date(goal.target_date).toLocaleDateString('ja-JP')}
                        </div>
                      </div>
                      
                      <div className="ml-6 flex flex-col space-y-2">
                        <Button variant="outline" size="sm">
                          編集
                        </Button>
                        <Button variant="outline" size="sm">
                          進捗更新
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
