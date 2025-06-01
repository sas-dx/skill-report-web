'use client';

import { useState } from 'react';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { Sidebar } from '@/components/dashboard/Sidebar';
import { Button } from '@/components/ui/Button';

export default function CareerPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  
  const [careerGoal, setCareerGoal] = useState({
    position: '',
    targetYear: '2027年',
    description: ''
  });

  const [actionPlans] = useState([
    {
      id: 1,
      item: 'Java研修',
      skill: 'Java基礎',
      deadline: '6月末',
      status: '未着手'
    },
    {
      id: 2,
      item: '資格取得',
      skill: 'AWS認定',
      deadline: '9月末',
      status: '進行中'
    }
  ]);

  const [supervisorComment] = useState({
    comment: '',
    lastUpdated: '2025/05/15',
    updatedBy: '山田部長'
  });

  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardHeader onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
      
      <div className="flex">
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        
        <main className="flex-1 p-6">
          <div className="max-w-6xl mx-auto space-y-6">
            <h1 className="text-2xl font-bold text-gray-900">キャリアプラン管理</h1>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* ① キャリア目標セクション */}
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">キャリア目標</h2>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      目標ポジション:
                    </label>
                    <input
                      type="text"
                      value={careerGoal.position}
                      onChange={(e) => setCareerGoal({...careerGoal, position: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="例: シニアエンジニア"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      達成目標時期:
                    </label>
                    <select
                      value={careerGoal.targetYear}
                      onChange={(e) => setCareerGoal({...careerGoal, targetYear: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="2025年">2025年</option>
                      <option value="2026年">2026年</option>
                      <option value="2027年">2027年</option>
                      <option value="2028年">2028年</option>
                      <option value="2029年">2029年</option>
                      <option value="2030年">2030年</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      目標概要:
                    </label>
                    <textarea
                      value={careerGoal.description}
                      onChange={(e) => setCareerGoal({...careerGoal, description: e.target.value})}
                      rows={4}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="キャリア目標の詳細を入力してください"
                    />
                  </div>
                  
                  <Button variant="primary">
                    保存
                  </Button>
                </div>
              </div>

              {/* ② スキルギャップ分析セクション */}
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">スキルギャップ分析</h2>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                  <div className="w-72 h-72 mx-auto relative mb-4">
                    {/* レーダーチャート（SVG） */}
                    <svg width="288" height="288" viewBox="0 0 288 288" className="mx-auto">
                      {/* 背景グリッド */}
                      <g stroke="#e5e7eb" strokeWidth="1" fill="none">
                        {/* 同心円 */}
                        <circle cx="144" cy="144" r="36" />
                        <circle cx="144" cy="144" r="72" />
                        <circle cx="144" cy="144" r="108" />
                        <circle cx="144" cy="144" r="144" />
                        
                        {/* 軸線 */}
                        <line x1="144" y1="0" x2="144" y2="288" />
                        <line x1="0" y1="144" x2="288" y2="144" />
                        <line x1="41" y1="41" x2="247" y2="247" />
                        <line x1="247" y1="41" x2="41" y2="247" />
                      </g>
                      
                      {/* 軸ラベル */}
                      <g fill="#6b7280" fontSize="11" textAnchor="middle">
                        <text x="144" y="15">フロントエンド</text>
                        <text x="270" y="149">バックエンド</text>
                        <text x="144" y="280">インフラ</text>
                        <text x="22" y="149">マネジメント</text>
                        <text x="225" y="45">AI/ML</text>
                        <text x="63" y="45">セキュリティ</text>
                      </g>
                      
                      {/* 現在スキル（青色） */}
                      <polygon
                        points="144,72 198,126 144,180 108,144 126,90 162,108"
                        fill="rgba(59, 130, 246, 0.3)"
                        stroke="#3b82f6"
                        strokeWidth="2"
                      />
                      
                      {/* 目標スキル（赤色） */}
                      <polygon
                        points="144,36 234,108 144,216 72,144 108,72 180,90"
                        fill="rgba(239, 68, 68, 0.2)"
                        stroke="#ef4444"
                        strokeWidth="2"
                        strokeDasharray="5,5"
                      />
                      
                      {/* データポイント */}
                      <g fill="#3b82f6">
                        <circle cx="144" cy="72" r="3" />
                        <circle cx="198" cy="126" r="3" />
                        <circle cx="144" cy="180" r="3" />
                        <circle cx="108" cy="144" r="3" />
                        <circle cx="126" cy="90" r="3" />
                        <circle cx="162" cy="108" r="3" />
                      </g>
                      
                      <g fill="#ef4444">
                        <circle cx="144" cy="36" r="3" />
                        <circle cx="234" cy="108" r="3" />
                        <circle cx="144" cy="216" r="3" />
                        <circle cx="72" cy="144" r="3" />
                        <circle cx="108" cy="72" r="3" />
                        <circle cx="180" cy="90" r="3" />
                      </g>
                    </svg>
                  </div>
                  
                  {/* 凡例 */}
                  <div className="flex justify-center mb-4 space-x-6">
                    <div className="flex items-center">
                      <div className="w-4 h-4 bg-blue-500 rounded mr-2"></div>
                      <span className="text-sm text-gray-600">現在スキル</span>
                    </div>
                    <div className="flex items-center">
                      <div className="w-4 h-4 border-2 border-red-500 border-dashed rounded mr-2"></div>
                      <span className="text-sm text-gray-600">目標スキル</span>
                    </div>
                  </div>
                  
                  {/* スキル目標設定ボタン */}
                  <div className="mt-4">
                    <Button variant="secondary" size="sm">
                      スキル目標設定
                    </Button>
                  </div>
                </div>
              </div>
            </div>

            {/* ③ アクションプランセクション */}
            <div className="bg-white shadow rounded-lg p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-medium text-gray-900">アクションプラン</h2>
                <Button variant="primary" size="sm">
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
                      <tr key={plan.id}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {plan.item}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {plan.skill}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {plan.deadline}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                            plan.status === '進行中' 
                              ? 'bg-yellow-100 text-yellow-800' 
                              : 'bg-gray-100 text-gray-800'
                          }`}>
                            {plan.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          <Button variant="secondary" size="sm">
                            編集
                          </Button>
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
              <div className="space-y-4">
                <textarea
                  value={supervisorComment.comment}
                  readOnly
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50"
                  placeholder="上司からのコメントが表示されます"
                />
                <div className="text-sm text-gray-500">
                  最終更新: {supervisorComment.lastUpdated} {supervisorComment.updatedBy}
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
