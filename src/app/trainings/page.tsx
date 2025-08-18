/**
 * 研修記録管理画面
 * 要求仕様ID: TRN.1-ATT.1, SCR-TRAINING
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import TrainingForm from '@/components/trainings/TrainingForm';
import { 
  Plus, 
  Search, 
  Filter, 
  Calendar,
  Clock,
  Award,
  BookOpen,
  Users,
  MapPin,
  DollarSign,
  RefreshCw,
  Download,
  Edit,
  Trash2,
  ArrowLeft
} from 'lucide-react';
import { useRouter } from 'next/navigation';

interface TrainingRecord {
  id?: string;
  trainingName: string;
  trainingType: string;
  trainingCategory: string;
  providerName: string;
  instructorName?: string;
  startDate: string;
  endDate: string;
  durationHours: number;
  location?: string;
  cost?: number;
  attendanceStatus: string;
  completionRate: number;
  testScore?: number;
  certificateObtained: boolean;
  satisfactionScore?: number;
}

export default function TrainingsPage() {
  const router = useRouter();
  const [records, setRecords] = useState<TrainingRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedYear, setSelectedYear] = useState<string>(new Date().getFullYear().toString());
  const [searchTerm, setSearchTerm] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [editingRecord, setEditingRecord] = useState<TrainingRecord | null>(null);

  // 研修記録を取得
  const fetchTrainingRecords = async () => {
    try {
      setIsLoading(true);
      
      const params = new URLSearchParams();
      if (selectedYear !== 'all') params.append('year', selectedYear);
      if (selectedCategory !== 'all') params.append('category', selectedCategory);
      
      const tenant = localStorage.getItem('tenant');
      const tenantData = tenant ? JSON.parse(tenant) : null;
      
      const response = await fetch(`/api/trainings/records?${params}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'x-tenant-id': tenantData?.id || ''
        }
      });

      if (response.ok) {
        const data = await response.json();
        setRecords(data.data?.records || []);
      }
    } catch (error) {
      console.error('研修記録取得エラー:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // 研修記録を保存
  const saveTrainingRecord = async (record: TrainingRecord) => {
    const tenant = localStorage.getItem('tenant');
    const tenantData = tenant ? JSON.parse(tenant) : null;
    
    // 更新の場合は個別のエンドポイントを使用
    const url = record.id 
      ? `/api/trainings/records/${record.id}`
      : '/api/trainings/records';
    
    const method = record.id ? 'PUT' : 'POST';
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'x-tenant-id': tenantData?.id || ''
      },
      body: JSON.stringify(record)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error?.message || '保存に失敗しました');
    }

    await fetchTrainingRecords();
  };

  // 研修記録を削除
  const deleteTrainingRecord = async (recordId: string) => {
    if (!confirm('この研修記録を削除しますか？')) return;

    const tenant = localStorage.getItem('tenant');
    const tenantData = tenant ? JSON.parse(tenant) : null;
    
    const response = await fetch(`/api/trainings/records/${recordId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'x-tenant-id': tenantData?.id || ''
      }
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error?.message || '削除に失敗しました');
    }

    await fetchTrainingRecords();
  };

  useEffect(() => {
    fetchTrainingRecords();
  }, [selectedCategory, selectedYear]);

  // フィルタリングされた記録
  const filteredRecords = records.filter(record => 
    searchTerm === '' || 
    record.trainingName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    record.providerName.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // ステータスバッジの取得
  const getStatusBadge = (status: string, completionRate: number) => {
    if (status === 'COMPLETED') {
      return <Badge className="bg-green-100 text-green-800">完了</Badge>;
    } else if (status === 'IN_PROGRESS') {
      return <Badge className="bg-blue-100 text-blue-800">受講中 {completionRate}%</Badge>;
    } else if (status === 'REGISTERED') {
      return <Badge className="bg-yellow-100 text-yellow-800">申込済</Badge>;
    } else {
      return <Badge className="bg-gray-100 text-gray-800">未受講</Badge>;
    }
  };

  // カテゴリバッジの色
  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      '技術研修': 'bg-purple-100 text-purple-800',
      'ビジネススキル': 'bg-blue-100 text-blue-800',
      'マネジメント': 'bg-green-100 text-green-800',
      'コンプライアンス': 'bg-red-100 text-red-800',
      '資格取得': 'bg-yellow-100 text-yellow-800',
      'その他': 'bg-gray-100 text-gray-800'
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="container mx-auto py-8">
      {/* ヘッダー */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-3xl font-bold mb-2">研修記録管理</h1>
            <p className="text-gray-600">研修参加履歴と学習成果を管理</p>
          </div>
          <Button
            onClick={() => router.push('/dashboard')}
            variant="outline"
            className="flex items-center gap-2"
          >
            <ArrowLeft className="h-4 w-4" />
            ダッシュボードに戻る
          </Button>
        </div>
      </div>

      {/* 統計カード */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">総研修時間</p>
                <p className="text-2xl font-bold">
                  {records.reduce((sum, r) => sum + r.durationHours, 0)}時間
                </p>
              </div>
              <Clock className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">完了コース</p>
                <p className="text-2xl font-bold">
                  {records.filter(r => r.attendanceStatus === 'COMPLETED').length}件
                </p>
              </div>
              <Award className="h-8 w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">取得資格</p>
                <p className="text-2xl font-bold">
                  {records.filter(r => r.certificateObtained).length}件
                </p>
              </div>
              <Award className="h-8 w-8 text-yellow-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">平均スコア</p>
                <p className="text-2xl font-bold">
                  {records.filter(r => r.testScore).length > 0
                    ? Math.round(
                        records.filter(r => r.testScore)
                          .reduce((sum, r) => sum + (r.testScore || 0), 0) /
                        records.filter(r => r.testScore).length
                      )
                    : 0}点
                </p>
              </div>
              <BookOpen className="h-8 w-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* フィルター・検索バー */}
      <Card className="mb-6">
        <CardContent className="p-4">
          <div className="flex flex-wrap gap-4 items-center">
            <div className="flex-1 min-w-[200px]">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <input
                  type="text"
                  placeholder="研修名・提供元で検索..."
                  className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
            </div>

            <select
              className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={selectedYear}
              onChange={(e) => setSelectedYear(e.target.value)}
            >
              <option value="all">全期間</option>
              <option value="2024">2024年</option>
              <option value="2023">2023年</option>
              <option value="2022">2022年</option>
            </select>

            <select
              className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
            >
              <option value="all">全カテゴリ</option>
              <option value="技術研修">技術研修</option>
              <option value="ビジネススキル">ビジネススキル</option>
              <option value="マネジメント">マネジメント</option>
              <option value="コンプライアンス">コンプライアンス</option>
              <option value="資格取得">資格取得</option>
            </select>

            <Button onClick={() => setShowAddModal(true)}>
              <Plus className="h-4 w-4 mr-2" />
              研修記録を追加
            </Button>

            <Button variant="outline" onClick={fetchTrainingRecords}>
              <RefreshCw className="h-4 w-4" />
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* 研修記録リスト */}
      <div className="space-y-4">
        {isLoading ? (
          <Card>
            <CardContent className="p-8 text-center">
              <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-4 text-gray-400" />
              <p className="text-gray-500">読み込み中...</p>
            </CardContent>
          </Card>
        ) : filteredRecords.length === 0 ? (
          <Card>
            <CardContent className="p-8 text-center">
              <BookOpen className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p className="text-gray-500">研修記録がありません</p>
              <Button 
                className="mt-4"
                onClick={() => setShowAddModal(true)}
              >
                <Plus className="h-4 w-4 mr-2" />
                最初の研修記録を追加
              </Button>
            </CardContent>
          </Card>
        ) : (
          filteredRecords.map((record) => (
            <Card key={record.id} className="hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-semibold">{record.trainingName}</h3>
                      {getStatusBadge(record.attendanceStatus, record.completionRate)}
                      <Badge className={getCategoryColor(record.trainingCategory)}>
                        {record.trainingCategory}
                      </Badge>
                      {record.certificateObtained && (
                        <Badge className="bg-yellow-100 text-yellow-800">
                          <Award className="h-3 w-3 mr-1" />
                          資格取得
                        </Badge>
                      )}
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4 text-sm">
                      <div className="flex items-center gap-2 text-gray-600">
                        <Calendar className="h-4 w-4" />
                        <span>
                          {new Date(record.startDate).toLocaleDateString('ja-JP')} - 
                          {new Date(record.endDate).toLocaleDateString('ja-JP')}
                        </span>
                      </div>
                      <div className="flex items-center gap-2 text-gray-600">
                        <Clock className="h-4 w-4" />
                        <span>{record.durationHours}時間</span>
                      </div>
                      <div className="flex items-center gap-2 text-gray-600">
                        <Users className="h-4 w-4" />
                        <span>{record.providerName}</span>
                      </div>
                      {record.location && (
                        <div className="flex items-center gap-2 text-gray-600">
                          <MapPin className="h-4 w-4" />
                          <span>{record.location}</span>
                        </div>
                      )}
                    </div>

                    {(record.testScore !== undefined || record.satisfactionScore !== undefined) && (
                      <div className="flex gap-6 mt-4">
                        {record.testScore !== undefined && (
                          <div className="flex items-center gap-2">
                            <span className="text-sm text-gray-600">テストスコア:</span>
                            <span className="font-semibold">{record.testScore}点</span>
                          </div>
                        )}
                        {record.satisfactionScore !== undefined && (
                          <div className="flex items-center gap-2">
                            <span className="text-sm text-gray-600">満足度:</span>
                            <div className="flex">
                              {[...Array(5)].map((_, i) => (
                                <span 
                                  key={i}
                                  className={i < record.satisfactionScore! ? 'text-yellow-400' : 'text-gray-300'}
                                >
                                  ★
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>

                  <div className="flex gap-2 ml-4">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setEditingRecord(record)}
                    >
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      className="text-red-600 hover:bg-red-50"
                      onClick={() => deleteTrainingRecord(record.id!)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>

      {/* 研修記録フォーム */}
      <TrainingForm
        isOpen={showAddModal || !!editingRecord}
        onClose={() => {
          setShowAddModal(false);
          setEditingRecord(null);
        }}
        onSave={saveTrainingRecord}
        editingRecord={editingRecord}
      />
    </div>
  );
}