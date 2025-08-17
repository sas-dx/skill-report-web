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

  // API呼び出しによるデータ取得
  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        
        // 作業実績データをAPIから取得
        const token = localStorage.getItem('token');
        const response = await fetch('/api/work/me', {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': token ? `Bearer ${token}` : '',
          }
        });

        if (!response.ok) {
          throw new Error(`HTTPエラー: ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
          setWorkRecords(data.data.records || []);
          setSummary(data.data.summary || null);
        } else {
          console.error('APIエラー:', data.error);
          // エラー時はモックデータを使用（フォールバック）
          const mockRecords: WorkRecord[] = [];
          const mockSummary: ProjectSummary = {
            total_projects: 0,
            active_projects: 0,
            completed_projects: 0,
            total_technologies: 0
          };
          setWorkRecords(mockRecords);
          setSummary(mockSummary);
        }
      } catch (error) {
        console.error('データ読み込みエラー:', error);
        // エラー時は空データを設定
        setWorkRecords([]);
        setSummary({
          total_projects: 0,
          active_projects: 0,
          completed_projects: 0,
          total_technologies: 0
        });
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

  const handleAddRecord = async () => {
    if (!newRecord.project_name || !newRecord.project_code || !newRecord.role || !newRecord.start_date) {
      alert('必須項目を入力してください');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/work', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : '',
        },
        body: JSON.stringify(newRecord)
      });

      const data = await response.json();

      if (data.success) {
        alert('作業実績を登録しました');
        // データを再読み込み
        window.location.reload();
      } else {
        alert(`登録エラー: ${data.error?.message || '不明なエラー'}`);
      }
    } catch (error) {
      console.error('登録エラー:', error);
      alert('作業実績の登録に失敗しました');
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

  const handleEditRecord = (record: WorkRecord) => {
    // 編集対象のレコードをフォームに設定
    setNewRecord({
      ...record,
      id: record.id  // IDを保持して更新時に使用
    });
    setActiveTab('add');  // 追加タブに切り替え
  };

  const handleDeleteRecord = async (recordId: string) => {
    if (!confirm('この作業実績を削除してもよろしいですか？')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/work?id=${recordId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : '',
        }
      });

      const data = await response.json();

      if (data.success) {
        alert('作業実績を削除しました');
        // データを再読み込み
        window.location.reload();
      } else {
        alert(`削除エラー: ${data.error?.message || '不明なエラー'}`);
      }
    } catch (error) {
      console.error('削除エラー:', error);
      alert('作業実績の削除に失敗しました');
    }
  };

  const handleUpdateRecord = async () => {
    if (!newRecord.id) {
      // 新規追加の場合は既存の処理を実行
      await handleAddRecord();
      return;
    }

    // 更新処理
    if (!newRecord.project_name || !newRecord.project_code || !newRecord.role || !newRecord.start_date) {
      alert('必須項目を入力してください');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/work', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : '',
        },
        body: JSON.stringify(newRecord)
      });

      const data = await response.json();

      if (data.success) {
        alert('作業実績を更新しました');
        // データを再読み込み
        window.location.reload();
      } else {
        alert(`更新エラー: ${data.error?.message || '不明なエラー'}`);
      }
    } catch (error) {
      console.error('更新エラー:', error);
      alert('作業実績の更新に失敗しました');
    }
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
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">作業実績管理</h1>
                  <p className="text-gray-600 mt-1">プロジェクトの作業実績・成果を管理します</p>
                </div>
                <div className="flex space-x-3">
                  <Button
                    onClick={() => window.location.href = '/work/bulk'}
                    variant="secondary"
                    className="flex items-center space-x-2"
                  >
                    <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
                    </svg>
                    <span>一括登録</span>
                  </Button>
                </div>
              </div>
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
                          <Button 
                            variant="secondary" 
                            size="sm"
                            onClick={() => handleEditRecord(record)}
                          >
                            編集
                          </Button>
                          <Button 
                            variant="secondary" 
                            size="sm"
                            onClick={() => handleDeleteRecord(record.id)}
                          >
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
                <h2 className="text-lg font-medium text-gray-900 mb-6">
                  {newRecord.id ? '作業実績を編集' : '新しい作業実績を追加'}
                </h2>
                
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

                    {/* 使用技術 */}
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        使用技術（カンマ区切りで入力）
                      </label>
                      <Input
                        value={newRecord.technologies?.join(', ') || ''}
                        onChange={(e) => setNewRecord({
                          ...newRecord, 
                          technologies: e.target.value.split(',').map(tech => tech.trim()).filter(tech => tech)
                        })}
                        placeholder="例: React, TypeScript, Node.js"
                      />
                    </div>

                    {/* 成果・実績 */}
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        成果・実績（改行区切りで入力）
                      </label>
                      <textarea
                        value={newRecord.achievements?.join('\n') || ''}
                        onChange={(e) => setNewRecord({
                          ...newRecord,
                          achievements: e.target.value.split('\n').filter(item => item.trim())
                        })}
                        rows={3}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        placeholder="達成した成果や実績を入力してください"
                      />
                    </div>

                    {/* 担当業務 */}
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        担当業務（改行区切りで入力）
                      </label>
                      <textarea
                        value={newRecord.responsibilities?.join('\n') || ''}
                        onChange={(e) => setNewRecord({
                          ...newRecord,
                          responsibilities: e.target.value.split('\n').filter(item => item.trim())
                        })}
                        rows={3}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        placeholder="担当した業務内容を入力してください"
                      />
                    </div>
                  </div>

                  <div className="flex justify-end space-x-3">
                    <Button
                      onClick={() => {
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
                      }}
                      variant="secondary"
                    >
                      キャンセル
                    </Button>
                    <Button
                      onClick={newRecord.id ? handleUpdateRecord : handleAddRecord}
                      variant="primary"
                    >
                      {newRecord.id ? '実績を更新' : '実績を追加'}
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
