// WPM.1-DET.1: 作業実績管理画面
'use client';

import React, { useState, useEffect } from 'react';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { Sidebar } from '@/components/dashboard/Sidebar';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Spinner } from '@/components/ui/Spinner';

interface WorkRecord {
  id: string;
  project_name: string;
  project_code: string;
  role: string;
  start_date: string;
  end_date?: string;
  status: 'active' | 'completed' | 'on_hold';
  description: string;
  technologies: string[];
  achievements: string[];
  team_size: number;
  responsibilities: string[];
  created_at: string;
  updated_at: string;
}

interface ProjectSummary {
  total_projects: number;
  active_projects: number;
  completed_projects: number;
  total_technologies: number;
}

export default function WorkPage() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [workRecords, setWorkRecords] = useState<WorkRecord[]>([]);
  const [summary, setSummary] = useState<ProjectSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'records' | 'add'>('overview');
  const [selectedStatus, setSelectedStatus] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [newRecord, setNewRecord] = useState<Partial<WorkRecord>>({
    project_name: '',
    project_code: '',
    role: '',
    start_date: '',
    end_date: '',
    status: 'active',
    description: '',
    technologies: [],
    achievements: [],
    team_size: 1,
    responsibilities: []
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

        const mockRecords: WorkRecord[] = [
          {
            id: '1',
            project_name: '年間スキル報告書WEB化プロジェクト',
            project_code: 'SKILL-WEB-2025',
            role: 'プロジェクトリーダー',
            start_date: '2025-05-01',
            end_date: '',
            status: 'active',
            description: '既存のExcelベースのスキル報告書をWebアプリケーション化するプロジェクト',
            technologies: ['Next.js', 'TypeScript', 'React', 'Tailwind CSS', 'PostgreSQL'],
            achievements: [
              'プロジェクト計画の策定と承認取得',
              '技術スタックの選定と環境構築',
              'UI/UXデザインの設計と実装'
            ],
            team_size: 6,
            responsibilities: [
              'プロジェクト全体の進行管理',
              '技術的な意思決定',
              'チームメンバーのタスク管理',
              'ステークホルダーとの調整'
            ],
            created_at: '2025-05-01',
            updated_at: '2025-05-30'
          },
          {
            id: '2',
            project_name: '顧客管理システム改修',
            project_code: 'CRM-UPG-2024',
            role: 'フロントエンドエンジニア',
            start_date: '2024-10-01',
            end_date: '2025-03-31',
            status: 'completed',
            description: '既存の顧客管理システムのUI/UX改善とパフォーマンス最適化',
            technologies: ['React', 'Redux', 'Material-UI', 'Node.js', 'MySQL'],
            achievements: [
              'ページ読み込み速度を50%改善',
              'ユーザビリティテストで満足度90%達成',
              'レスポンシブデザインの実装完了'
            ],
            team_size: 4,
            responsibilities: [
              'フロントエンド開発',
              'UI/UXデザインの実装',
              'パフォーマンス最適化',
              'テストケース作成・実行'
            ],
            created_at: '2024-10-01',
            updated_at: '2025-03-31'
          },
          {
            id: '3',
            project_name: 'ECサイト新規構築',
            project_code: 'EC-NEW-2024',
            role: 'フルスタックエンジニア',
            start_date: '2024-06-01',
            end_date: '2024-09-30',
            status: 'completed',
            description: '中小企業向けECサイトの新規構築プロジェクト',
            technologies: ['Vue.js', 'Nuxt.js', 'Express.js', 'MongoDB', 'AWS'],
            achievements: [
              '決済システムの安全な実装',
              '在庫管理機能の自動化',
              'SEO最適化による検索順位向上'
            ],
            team_size: 3,
            responsibilities: [
              'フロントエンド・バックエンド開発',
              'データベース設計',
              'AWS環境構築・運用',
              '決済システム連携'
            ],
            created_at: '2024-06-01',
            updated_at: '2024-09-30'
          }
        ];

        const mockSummary: ProjectSummary = {
          total_projects: mockRecords.length,
          active_projects: mockRecords.filter(r => r.status === 'active').length,
          completed_projects: mockRecords.filter(r => r.status === 'completed').length,
          total_technologies: [...new Set(mockRecords.flatMap(r => r.technologies))].length
        };

        setWorkRecords(mockRecords);
        setSummary(mockSummary);
      } catch (error) {
        console.error('データ読み込みエラー:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, []);

  const getStatusText = (status: string) => {
    const statuses = {
      active: '進行中',
      completed: '完了',
      on_hold: '保留中'
    };
    return statuses[status as keyof typeof statuses] || status;
  };

  const getStatusColor = (status: string) => {
    const colors = {
      active: 'bg-blue-100 text-blue-800',
      completed: 'bg-green-100 text-green-800',
      on_hold: 'bg-yellow-100 text-yellow-800'
    };
    return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  const filteredRecords = workRecords.filter(record => {
    const matchesStatus = selectedStatus === 'all' || record.status === selectedStatus;
    const matchesSearch = record.project_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         record.project_code.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         record.role.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesStatus && matchesSearch;
  });

  const handleAddRecord = () => {
    if (!newRecord.project_name || !newRecord.project_code || !newRecord.role || !newRecord.start_date) {
      alert('必須項目を入力してください');
      return;
    }

    const record: WorkRecord = {
      id: Date.now().toString(),
      project_name: newRecord.project_name!,
      project_code: newRecord.project_code!,
      role: newRecord.role!,
      start_date: newRecord.start_date!,
      end_date: newRecord.end_date || '',
      status: newRecord.status || 'active',
      description: newRecord.description || '',
      technologies: newRecord.technologies || [],
      achievements: newRecord.achievements || [],
      team_size: newRecord.team_size || 1,
      responsibilities: newRecord.responsibilities || [],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };

    setWorkRecords([...workRecords, record]);
    setNewRecord({
      project_name: '',
      project_code: '',
      role: '',
      start_date: '',
      end_date: '',
      status: 'active',
      description: '',
      technologies: [],
      achievements: [],
      team_size: 1,
      responsibilities: []
    });
    setActiveTab('records');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <DashboardHeader 
          onMenuClick={handleMenuClick}
          title="作業実績"
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
        title="作業実績"
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
              <h1 className="text-2xl font-bold text-gray-900">作業実績管理</h1>
              <p className="text-gray-600 mt-1">プロジェクトの作業実績・成果を管理します</p>
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
                    onClick={() => setActiveTab('records')}
                    className={`py-2 px-1 border-b-2 font-medium text-sm ${
                      activeTab === 'records'
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    実績一覧
                  </button>
                  <button
                    onClick={() => setActiveTab('add')}
                    className={`py-2 px-1 border-b-2 font-medium text-sm ${
                      activeTab === 'add'
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    実績追加
                  </button>
                </nav>
              </div>
            </div>

            {/* 概要タブ */}
            {activeTab === 'overview' && summary && (
              <div className="space-y-6">
                {/* サマリーカード */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                  <div className="bg-white p-6 rounded-lg shadow">
                    <h3 className="text-lg font-medium text-gray-900 mb-2">総プロジェクト数</h3>
                    <p className="text-3xl font-bold text-blue-600">{summary.total_projects}</p>
                  </div>
                  <div className="bg-white p-6 rounded-lg shadow">
                    <h3 className="text-lg font-medium text-gray-900 mb-2">進行中</h3>
                    <p className="text-3xl font-bold text-yellow-600">{summary.active_projects}</p>
                  </div>
                  <div className="bg-white p-6 rounded-lg shadow">
                    <h3 className="text-lg font-medium text-gray-900 mb-2">完了</h3>
                    <p className="text-3xl font-bold text-green-600">{summary.completed_projects}</p>
                  </div>
                  <div className="bg-white p-6 rounded-lg shadow">
                    <h3 className="text-lg font-medium text-gray-900 mb-2">使用技術数</h3>
                    <p className="text-3xl font-bold text-purple-600">{summary.total_technologies}</p>
                  </div>
                </div>

                {/* 最近のプロジェクト */}
                <div className="bg-white shadow rounded-lg">
                  <div className="px-6 py-4 border-b border-gray-200">
                    <h2 className="text-lg font-medium text-gray-900">最近のプロジェクト</h2>
                  </div>
                  <div className="p-6">
                    <div className="space-y-4">
                      {workRecords.slice(0, 3).map((record) => (
                        <div key={record.id} className="border-l-4 border-blue-500 pl-4">
                          <div className="flex items-start justify-between">
                            <div>
                              <h3 className="font-medium text-gray-900">{record.project_name}</h3>
                              <p className="text-sm text-gray-600 mt-1">{record.project_code} - {record.role}</p>
                              <div className="flex items-center mt-2 space-x-4">
                                <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(record.status)}`}>
                                  {getStatusText(record.status)}
                                </span>
                                <span className="text-sm text-gray-500">
                                  {record.start_date} 〜 {record.end_date || '進行中'}
                                </span>
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* 実績一覧タブ */}
            {activeTab === 'records' && (
              <div>
                {/* 検索・フィルター */}
                <div className="mb-6 bg-white p-4 rounded-lg shadow">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        キーワード検索
                      </label>
                      <Input
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        placeholder="プロジェクト名、コード、役割で検索"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        ステータスフィルター
                      </label>
                      <select
                        value={selectedStatus}
                        onChange={(e) => setSelectedStatus(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="all">すべて</option>
                        <option value="active">進行中</option>
                        <option value="completed">完了</option>
                        <option value="on_hold">保留中</option>
                      </select>
                    </div>
                  </div>
                </div>

                {/* 実績一覧 */}
                <div className="space-y-6">
                  {filteredRecords.map((record) => (
                    <div key={record.id} className="bg-white shadow rounded-lg p-6">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="text-lg font-medium text-gray-900">{record.project_name}</h3>
                          <p className="text-gray-600 mt-1">{record.project_code}</p>
                          
                          <div className="flex items-center mt-4 space-x-4">
                            <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(record.status)}`}>
                              {getStatusText(record.status)}
                            </span>
                            <span className="text-sm text-gray-500">
                              役割: {record.role}
                            </span>
                            <span className="text-sm text-gray-500">
                              期間: {record.start_date} 〜 {record.end_date || '進行中'}
                            </span>
                            <span className="text-sm text-gray-500">
                              チーム規模: {record.team_size}名
                            </span>
                          </div>

                          <p className="text-gray-700 mt-4">{record.description}</p>

                          {/* 使用技術 */}
                          {record.technologies.length > 0 && (
                            <div className="mt-4">
                              <span className="text-sm font-medium text-gray-700">使用技術:</span>
                              <div className="flex flex-wrap gap-2 mt-1">
                                {record.technologies.map((tech, index) => (
                                  <span
                                    key={index}
                                    className="px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded"
                                  >
                                    {tech}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}

                          {/* 担当業務 */}
                          {record.responsibilities.length > 0 && (
                            <div className="mt-4">
                              <span className="text-sm font-medium text-gray-700">担当業務:</span>
                              <ul className="mt-1 text-sm text-gray-600 list-disc list-inside">
                                {record.responsibilities.map((resp, index) => (
                                  <li key={index}>{resp}</li>
                                ))}
                              </ul>
                            </div>
                          )}

                          {/* 成果・実績 */}
                          {record.achievements.length > 0 && (
                            <div className="mt-4">
                              <span className="text-sm font-medium text-gray-700">成果・実績:</span>
                              <ul className="mt-1 text-sm text-gray-600 list-disc list-inside">
                                {record.achievements.map((achievement, index) => (
                                  <li key={index}>{achievement}</li>
                                ))}
                              </ul>
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

            {/* 実績追加タブ */}
            {activeTab === 'add' && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-6">新しい作業実績を追加</h2>
                
                <div className="space-y-6">
                  {/* 基本情報 */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        プロジェクト名 <span className="text-red-500">*</span>
                      </label>
                      <Input
                        value={newRecord.project_name}
                        onChange={(e) => setNewRecord({...newRecord, project_name: e.target.value})}
                        placeholder="例: 年間スキル報告書WEB化プロジェクト"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        プロジェクトコード <span className="text-red-500">*</span>
                      </label>
                      <Input
                        value={newRecord.project_code}
                        onChange={(e) => setNewRecord({...newRecord, project_code: e.target.value})}
                        placeholder="例: SKILL-WEB-2025"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        役割 <span className="text-red-500">*</span>
                      </label>
                      <Input
                        value={newRecord.role}
                        onChange={(e) => setNewRecord({...newRecord, role: e.target.value})}
                        placeholder="例: プロジェクトリーダー"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        ステータス
                      </label>
                      <select
                        value={newRecord.status}
                        onChange={(e) => setNewRecord({...newRecord, status: e.target.value as any})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="active">進行中</option>
                        <option value="completed">完了</option>
                        <option value="on_hold">保留中</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        開始日 <span className="text-red-500">*</span>
                      </label>
                      <Input
                        type="date"
                        value={newRecord.start_date}
                        onChange={(e) => setNewRecord({...newRecord, start_date: e.target.value})}
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        終了日
                      </label>
                      <Input
                        type="date"
                        value={newRecord.end_date}
                        onChange={(e) => setNewRecord({...newRecord, end_date: e.target.value})}
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        チーム規模
                      </label>
                      <Input
                        type="number"
                        value={newRecord.team_size}
                        onChange={(e) => setNewRecord({...newRecord, team_size: parseInt(e.target.value) || 1})}
                        min="1"
                        placeholder="1"
                      />
                    </div>

                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        プロジェクト概要
                      </label>
                      <textarea
                        value={newRecord.description}
                        onChange={(e) => setNewRecord({...newRecord, description: e.target.value})}
                        rows={3}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        placeholder="プロジェクトの概要や目的を入力してください"
                      />
                    </div>
                  </div>

                  <div className="flex justify-end space-x-3">
                    <Button
                      onClick={() => setActiveTab('records')}
                      variant="secondary"
                    >
                      キャンセル
                    </Button>
                    <Button
                      onClick={handleAddRecord}
                      variant="primary"
                    >
                      実績を追加
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
