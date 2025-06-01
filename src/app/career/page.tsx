// CAR.1-PLAN.1: キャリア目標管理画面
'use client';

import React, { useState, useEffect } from 'react';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { Sidebar } from '@/components/dashboard/Sidebar';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Spinner } from '@/components/ui/Spinner';

interface CareerGoal {
  id: string;
  title: string;
  description: string;
  category: 'short' | 'medium' | 'long';
  target_date: string;
  status: 'not_started' | 'in_progress' | 'completed' | 'on_hold';
  progress: number;
  skills_required: string[];
  milestones: Milestone[];
  created_at: string;
  updated_at: string;
}

interface Milestone {
  id: string;
  title: string;
  description: string;
  target_date: string;
  status: 'not_started' | 'in_progress' | 'completed';
  completed_at?: string;
}

export default function CareerPage() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [goals, setGoals] = useState<CareerGoal[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'goals' | 'add'>('overview');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [newGoal, setNewGoal] = useState<Partial<CareerGoal>>({
    title: '',
    description: '',
    category: 'short',
    target_date: '',
    skills_required: [],
    milestones: []
  });

  const handleMenuClick = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleSidebarClose = () => {
    setIsSidebarOpen(false);
  };

  // モックデータの初期化
  useEffect(() => {
    const loadData = async () => {
      try {
        await new Promise(resolve => setTimeout(resolve, 1000));

        const mockGoals: CareerGoal[] = [
          {
            id: '1',
            title: 'フルスタックエンジニアとしてのスキル向上',
            description: 'フロントエンドとバックエンドの両方で高いレベルの開発スキルを身につける',
            category: 'short',
            target_date: '2025-12-31',
            status: 'in_progress',
            progress: 65,
            skills_required: ['React', 'Node.js', 'TypeScript', 'AWS'],
            milestones: [
              {
                id: '1-1',
                title: 'React上級レベル習得',
                description: 'React Hooks、Context API、パフォーマンス最適化を習得',
                target_date: '2025-08-31',
                status: 'completed',
                completed_at: '2025-07-15'
              },
              {
                id: '1-2',
                title: 'Node.js API開発スキル習得',
                description: 'Express.js、データベース連携、認証機能の実装',
                target_date: '2025-10-31',
                status: 'in_progress'
              }
            ],
            created_at: '2025-01-01',
            updated_at: '2025-05-30'
          },
          {
            id: '2',
            title: 'チームリーダーとしての経験積み',
            description: '3-5名のチームをリードし、プロジェクト管理スキルを向上させる',
            category: 'medium',
            target_date: '2026-06-30',
            status: 'not_started',
            progress: 0,
            skills_required: ['プロジェクト管理', 'コミュニケーション', 'メンタリング'],
            milestones: [
              {
                id: '2-1',
                title: 'プロジェクト管理研修受講',
                description: 'PMP資格取得に向けた研修を受講',
                target_date: '2025-09-30',
                status: 'not_started'
              }
            ],
            created_at: '2025-01-15',
            updated_at: '2025-01-15'
          },
          {
            id: '3',
            title: 'アーキテクト職への昇進',
            description: 'システム全体の設計・アーキテクチャを担当できるレベルに到達',
            category: 'long',
            target_date: '2028-03-31',
            status: 'not_started',
            progress: 10,
            skills_required: ['システム設計', 'アーキテクチャ', '技術選定', 'ドキュメンテーション'],
            milestones: [],
            created_at: '2025-02-01',
            updated_at: '2025-02-01'
          }
        ];

        setGoals(mockGoals);
      } catch (error) {
        console.error('データ読み込みエラー:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, []);

  const getCategoryText = (category: string) => {
    const categories = {
      short: '短期目標（1年以内）',
      medium: '中期目標（1-3年）',
      long: '長期目標（3年以上）'
    };
    return categories[category as keyof typeof categories] || category;
  };

  const getStatusText = (status: string) => {
    const statuses = {
      not_started: '未開始',
      in_progress: '進行中',
      completed: '完了',
      on_hold: '保留中'
    };
    return statuses[status as keyof typeof statuses] || status;
  };

  const getStatusColor = (status: string) => {
    const colors = {
      not_started: 'bg-gray-100 text-gray-800',
      in_progress: 'bg-blue-100 text-blue-800',
      completed: 'bg-green-100 text-green-800',
      on_hold: 'bg-yellow-100 text-yellow-800'
    };
    return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  const filteredGoals = goals.filter(goal => {
    if (selectedCategory === 'all') return true;
    return goal.category === selectedCategory;
  });

  const handleAddGoal = () => {
    if (!newGoal.title || !newGoal.target_date) {
      alert('必須項目を入力してください');
      return;
    }

    const goal: CareerGoal = {
      id: Date.now().toString(),
      title: newGoal.title!,
      description: newGoal.description || '',
      category: newGoal.category || 'short',
      target_date: newGoal.target_date!,
      status: 'not_started',
      progress: 0,
      skills_required: newGoal.skills_required || [],
      milestones: [],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };

    setGoals([...goals, goal]);
    setNewGoal({
      title: '',
      description: '',
      category: 'short',
      target_date: '',
      skills_required: [],
      milestones: []
    });
    setActiveTab('goals');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <DashboardHeader 
          onMenuClick={handleMenuClick}
          title="キャリア目標"
        />
        <div className="flex pt-16">
          <Sidebar 
            isOpen={isSidebarOpen}
            onClose={handleSidebarClose}
          />
          <div className="flex-1 lg:ml-64 flex items-center justify-center">
            <Spinner size="lg" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ヘッダー */}
      <DashboardHeader 
        onMenuClick={handleMenuClick}
        title="キャリア目標"
      />

      {/* メインレイアウト */}
      <div className="flex pt-16">
        {/* サイドバー */}
        <Sidebar 
          isOpen={isSidebarOpen}
          onClose={handleSidebarClose}
        />

        {/* メインコンテンツエリア */}
        <div className="flex-1 lg:ml-64">
          <div className="max-w-6xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
            {/* ページヘッダー */}
            <div className="mb-8">
              <h1 className="text-2xl font-bold text-gray-900">キャリア目標管理</h1>
              <p className="text-gray-600 mt-1">キャリア目標の設定・進捗管理を行います</p>
            </div>

            {/* タブナビゲーション */}
            <div className="mb-6">
              <div className="border-b border-gray-200">
                <nav className="-mb-px flex space-x-8">
                  <button
                    onClick={() => setActiveTab('overview')}
                    className={`py-2 px-1 border-b-2 font-medium text-sm ${
                      activeTab === 'overview'
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    概要
                  </button>
                  <button
                    onClick={() => setActiveTab('goals')}
                    className={`py-2 px-1 border-b-2 font-medium text-sm ${
                      activeTab === 'goals'
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    目標一覧
                  </button>
                  <button
                    onClick={() => setActiveTab('add')}
                    className={`py-2 px-1 border-b-2 font-medium text-sm ${
                      activeTab === 'add'
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    目標追加
                  </button>
                </nav>
              </div>
            </div>

            {/* 概要タブ */}
            {activeTab === 'overview' && (
              <div className="space-y-6">
                {/* 進捗サマリー */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="bg-white p-6 rounded-lg shadow">
                    <h3 className="text-lg font-medium text-gray-900 mb-2">総目標数</h3>
                    <p className="text-3xl font-bold text-blue-600">{goals.length}</p>
                  </div>
                  <div className="bg-white p-6 rounded-lg shadow">
                    <h3 className="text-lg font-medium text-gray-900 mb-2">進行中</h3>
                    <p className="text-3xl font-bold text-yellow-600">
                      {goals.filter(g => g.status === 'in_progress').length}
                    </p>
                  </div>
                  <div className="bg-white p-6 rounded-lg shadow">
                    <h3 className="text-lg font-medium text-gray-900 mb-2">完了</h3>
                    <p className="text-3xl font-bold text-green-600">
                      {goals.filter(g => g.status === 'completed').length}
                    </p>
                  </div>
                </div>

                {/* 最近の目標 */}
                <div className="bg-white shadow rounded-lg">
                  <div className="px-6 py-4 border-b border-gray-200">
                    <h2 className="text-lg font-medium text-gray-900">最近の目標</h2>
                  </div>
                  <div className="p-6">
                    <div className="space-y-4">
                      {goals.slice(0, 3).map((goal) => (
                        <div key={goal.id} className="border-l-4 border-blue-500 pl-4">
                          <h3 className="font-medium text-gray-900">{goal.title}</h3>
                          <p className="text-sm text-gray-600 mt-1">{goal.description}</p>
                          <div className="flex items-center mt-2 space-x-4">
                            <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(goal.status)}`}>
                              {getStatusText(goal.status)}
                            </span>
                            <span className="text-sm text-gray-500">
                              進捗: {goal.progress}%
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* 目標一覧タブ */}
            {activeTab === 'goals' && (
              <div>
                {/* フィルター */}
                <div className="mb-6 bg-white p-4 rounded-lg shadow">
                  <div className="flex items-center space-x-4">
                    <label className="text-sm font-medium text-gray-700">
                      カテゴリフィルター:
                    </label>
                    <select
                      value={selectedCategory}
                      onChange={(e) => setSelectedCategory(e.target.value)}
                      className="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="all">すべて</option>
                      <option value="short">短期目標</option>
                      <option value="medium">中期目標</option>
                      <option value="long">長期目標</option>
                    </select>
                  </div>
                </div>

                {/* 目標一覧 */}
                <div className="space-y-6">
                  {filteredGoals.map((goal) => (
                    <div key={goal.id} className="bg-white shadow rounded-lg p-6">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="text-lg font-medium text-gray-900">{goal.title}</h3>
                          <p className="text-gray-600 mt-1">{goal.description}</p>
                          
                          <div className="flex items-center mt-4 space-x-4">
                            <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(goal.status)}`}>
                              {getStatusText(goal.status)}
                            </span>
                            <span className="text-sm text-gray-500">
                              {getCategoryText(goal.category)}
                            </span>
                            <span className="text-sm text-gray-500">
                              期限: {goal.target_date}
                            </span>
                          </div>

                          {/* 進捗バー */}
                          <div className="mt-4">
                            <div className="flex items-center justify-between text-sm text-gray-600 mb-1">
                              <span>進捗</span>
                              <span>{goal.progress}%</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div
                                className="bg-blue-600 h-2 rounded-full"
                                style={{ width: `${goal.progress}%` }}
                              ></div>
                            </div>
                          </div>

                          {/* 必要スキル */}
                          {goal.skills_required.length > 0 && (
                            <div className="mt-4">
                              <span className="text-sm font-medium text-gray-700">必要スキル:</span>
                              <div className="flex flex-wrap gap-2 mt-1">
                                {goal.skills_required.map((skill, index) => (
                                  <span
                                    key={index}
                                    className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded"
                                  >
                                    {skill}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}

                          {/* マイルストーン */}
                          {goal.milestones.length > 0 && (
                            <div className="mt-4">
                              <span className="text-sm font-medium text-gray-700">マイルストーン:</span>
                              <div className="mt-2 space-y-2">
                                {goal.milestones.map((milestone) => (
                                  <div key={milestone.id} className="flex items-center space-x-2">
                                    <div className={`w-3 h-3 rounded-full ${
                                      milestone.status === 'completed' ? 'bg-green-500' :
                                      milestone.status === 'in_progress' ? 'bg-blue-500' : 'bg-gray-300'
                                    }`}></div>
                                    <span className="text-sm text-gray-600">{milestone.title}</span>
                                    <span className="text-xs text-gray-500">({milestone.target_date})</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>

                        <div className="ml-4 flex space-x-2">
                          <Button variant="secondary" size="sm">
                            編集
                          </Button>
                          <Button variant="secondary" size="sm">
                            削除
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 目標追加タブ */}
            {activeTab === 'add' && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-6">新しい目標を追加</h2>
                
                <div className="space-y-6">
                  {/* 基本情報 */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        目標タイトル <span className="text-red-500">*</span>
                      </label>
                      <Input
                        value={newGoal.title}
                        onChange={(e) => setNewGoal({...newGoal, title: e.target.value})}
                        placeholder="例: フルスタックエンジニアとしてのスキル向上"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        カテゴリ <span className="text-red-500">*</span>
                      </label>
                      <select
                        value={newGoal.category}
                        onChange={(e) => setNewGoal({...newGoal, category: e.target.value as any})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="short">短期目標（1年以内）</option>
                        <option value="medium">中期目標（1-3年）</option>
                        <option value="long">長期目標（3年以上）</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        目標期限 <span className="text-red-500">*</span>
                      </label>
                      <Input
                        type="date"
                        value={newGoal.target_date}
                        onChange={(e) => setNewGoal({...newGoal, target_date: e.target.value})}
                      />
                    </div>

                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        目標の詳細説明
                      </label>
                      <textarea
                        value={newGoal.description}
                        onChange={(e) => setNewGoal({...newGoal, description: e.target.value})}
                        rows={4}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        placeholder="目標の詳細や達成したい内容を入力してください"
                      />
                    </div>
                  </div>

                  <div className="flex justify-end space-x-3">
                    <Button
                      onClick={() => setActiveTab('goals')}
                      variant="secondary"
                    >
                      キャンセル
                    </Button>
                    <Button
                      onClick={handleAddGoal}
                      variant="primary"
                    >
                      目標を追加
                    </Button>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
