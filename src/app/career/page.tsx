// CAR.1-PLAN.1: キャリアプラン管理画面
'use client';

import React, { useState } from 'react';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { Sidebar } from '@/components/dashboard/Sidebar';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { RadarChart } from '@/components/ui/RadarChart';

interface ActionPlan {
  id: string;
  item: string;
  skill: string;
  deadline: string;
  status: '未着手' | '進行中' | '完了';
}

export default function CareerPage() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [careerGoal, setCareerGoal] = useState({
    position: '',
    targetYear: '2027年',
    description: ''
  });
  const [actionPlans, setActionPlans] = useState<ActionPlan[]>([
    {
      id: '1',
      item: 'Java研修',
      skill: 'Java基礎',
      deadline: '6月末',
      status: '未着手'
    },
    {
      id: '2',
      item: '資格取得',
      skill: 'AWS認定',
      deadline: '9月末',
      status: '進行中'
    }
  ]);
  const [supervisorComment, setSupervisorComment] = useState('');

  const handleMenuClick = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleSidebarClose = () => {
    setIsSidebarOpen(false);
  };

  const handleSaveGoal = () => {
    console.log('キャリア目標を保存:', careerGoal);
    alert('キャリア目標を保存しました');
  };

  const handleAddActionPlan = () => {
    const newPlan: ActionPlan = {
      id: Date.now().toString(),
      item: '新規項目',
      skill: '新規スキル',
      deadline: '未設定',
      status: '未着手'
    };
    setActionPlans([...actionPlans, newPlan]);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case '未着手':
        return 'text-gray-500 bg-gray-100';
      case '進行中':
        return 'text-blue-500 bg-blue-100';
      case '完了':
        return 'text-green-500 bg-green-100';
      default:
        return 'text-gray-500 bg-gray-100';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ヘッダー */}
      <DashboardHeader 
        onMenuClick={handleMenuClick}
        title="年間スキル報告書システム"
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
            
            {/* ① キャリア目標セクション */}
            <div className="bg-white shadow rounded-lg p-6 mb-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">キャリア目標</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    目標ポジション
                  </label>
                  <Input
                    value={careerGoal.position}
                    onChange={(e) => setCareerGoal({...careerGoal, position: e.target.value})}
                    placeholder="例: シニアエンジニア"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    達成目標時期
                  </label>
                  <select
                    value={careerGoal.targetYear}
                    onChange={(e) => setCareerGoal({...careerGoal, targetYear: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="2025年">2025年</option>
                    <option value="2026年">2026年</option>
                    <option value="2027年">2027年</option>
                    <option value="2028年">2028年</option>
                    <option value="2029年">2029年</option>
                    <option value="2030年">2030年</option>
                  </select>
                </div>
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  目標概要
                </label>
                <textarea
                  value={careerGoal.description}
                  onChange={(e) => setCareerGoal({...careerGoal, description: e.target.value})}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  placeholder="キャリア目標の詳細を入力してください"
                />
              </div>
              <Button onClick={handleSaveGoal} variant="primary">
                保存
              </Button>
            </div>

            {/* ② スキルギャップ分析セクション */}
            <div className="bg-white shadow rounded-lg p-6 mb-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">スキルギャップ分析</h2>
              <div className="bg-gray-50 rounded-lg p-6 mb-4">
                <RadarChart 
                  data={[
                    { label: 'JavaScript', current: 3, target: 4 },
                    { label: 'React', current: 2, target: 4 },
                    { label: 'Node.js', current: 2, target: 3 },
                    { label: 'TypeScript', current: 1, target: 3 },
                    { label: 'AWS', current: 1, target: 4 },
                    { label: 'Docker', current: 2, target: 3 }
                  ]}
                  size={280}
                />
              </div>
              <Button variant="secondary" className="w-full">
                スキル目標設定
              </Button>
            </div>

            {/* ③ アクションプランセクション */}
            <div className="bg-white shadow rounded-lg p-6 mb-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-medium text-gray-900">アクションプラン</h2>
                <Button onClick={handleAddActionPlan} variant="primary" size="sm">
                  + 新規追加
                </Button>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        項目
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        習得スキル
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        期限
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        状態
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        操作
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {actionPlans.map((plan) => (
                      <tr key={plan.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {plan.item}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {plan.skill}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {plan.deadline}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(plan.status)}`}>
                            {plan.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <button className="text-blue-600 hover:text-blue-900">
                            編集
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* ④ 上司コメントセクション */}
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">上司コメント</h2>
              <textarea
                value={supervisorComment}
                onChange={(e) => setSupervisorComment(e.target.value)}
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="上司からのコメントを入力してください"
              />
              <div className="mt-3 text-sm text-gray-500">
                最終更新: 2025/05/15 山田部長
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}
