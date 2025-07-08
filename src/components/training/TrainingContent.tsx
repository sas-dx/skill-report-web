// TRN.1-HIST.1: 研修記録コンテンツコンポーネント
'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Spinner } from '@/components/ui/Spinner';

interface TrainingRecord {
  id: string;
  trainingName: string;
  category: string;
  startDate: string;
  endDate: string;
  hours: number;
  status: 'completed' | 'in_progress' | 'planned';
  pduPoints: number;
  description: string;
  skills?: string[]; // 習得したスキル情報
}

interface CertificationRecord {
  id: string;
  certificationName: string;
  organization: string;
  acquiredDate: string;
  expiryDate: string;
  status: 'active' | 'expired' | 'pending';
  score?: string;
  description: string;
}

export function TrainingContent() {
  const [activeTab, setActiveTab] = useState<'training' | 'certification'>('training');
  const [isLoading, setIsLoading] = useState(false);
  const [trainingRecords, setTrainingRecords] = useState<TrainingRecord[]>([]);
  const [certificationRecords, setCertificationRecords] = useState<CertificationRecord[]>([]);
  const [showAddForm, setShowAddForm] = useState(false);

  // APIからデータを取得
  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        // 仮のユーザーID（実際の環境では認証情報から取得）
        //const userId = 'emp-001'; // シードデータに合わせたID
        const userId = 'emp_001'; // シードデータに合わせたID
        
        // 研修情報APIの呼び出し
        const trainingResponse = await fetch(`/api/trainings/${userId}`);
        const trainingData = await trainingResponse.json();
        
        console.log('研修API応答:', trainingData);
        
        if (trainingData.success) {
          // APIレスポンスの形式に合わせてデータを変換
          if (Array.isArray(trainingData.data.trainings)) {
            const formattedTrainings = trainingData.data.trainings.map((item: any) => ({
              id: item.id || item.training_history_id || `training-${Math.random()}`,
              trainingName: item.training_name || '不明な研修',
              category: item.training_category || item.training_type || '未分類',
              startDate: item.start_date ? new Date(item.start_date).toISOString().split('T')[0] : '-',
              endDate: item.end_date ? new Date(item.end_date).toISOString().split('T')[0] : '-',
              hours: item.duration_hours || 0,
              status: (item.attendance_status || 'completed').toLowerCase(),
              pduPoints: item.pdu_points || 0,
              description: item.learning_objectives || '',
              // スキル情報の処理
              skills: item.skills_acquired ? 
                (typeof item.skills_acquired === 'string' ? 
                  JSON.parse(item.skills_acquired) : 
                  item.skills_acquired) : 
                []
            }));
            setTrainingRecords(formattedTrainings);
            console.log('研修データ取得成功:', formattedTrainings);
          } else {
            console.warn('研修データの形式が予期しないものです:', trainingData.data);
            // フォールバックとしてモックデータを使用
            useTrainingMockData();
          }
        } else {
          console.error('研修データ取得エラー:', trainingData.error);
          // エラー時はモックデータを使用
          useTrainingMockData();
        }
        
        // 資格情報APIの呼び出し
        const certResponse = await fetch(`/api/certifications/${userId}`);
        const certData = await certResponse.json();
        
        console.log('資格API応答:', certData);
        
        if (certData.success) {
          // APIレスポンスの形式に合わせてデータを変換
          if (Array.isArray(certData.data.certifications)) {
            const formattedCerts = certData.data.certifications.map((item: any) => ({
              id: item.id || item.pdu_id || `cert-${Math.random()}`,
              certificationName: item.certification_name || item.activity_name || '不明な資格',
              organization: item.issuer || item.certification_provider || '不明',
              acquiredDate: item.activity_date ? new Date(item.activity_date).toISOString().split('T')[0] : '-',
              expiryDate: item.expiry_date ? new Date(item.expiry_date).toISOString().split('T')[0] : '無期限',
              status: (item.approval_status || 'active').toLowerCase(),
              score: item.certificate_number || item.pdu_points?.toString() || '-',
              description: item.pdu_category || item.certification_level || ''
            }));
            setCertificationRecords(formattedCerts);
            console.log('資格データ取得成功:', formattedCerts);
          } else {
            console.warn('資格データの形式が予期しないものです:', certData.data);
            // フォールバックとしてモックデータを使用
            useCertificationMockData();
          }
        } else {
          console.error('資格データ取得エラー:', certData.error);
          // エラー時はモックデータを使用
          useCertificationMockData();
        }
      } catch (error) {
        console.error('データ取得エラー:', error);
        // エラー時はモックデータを使用
        useTrainingMockData();
        useCertificationMockData();
      } finally {
        // 少し遅延させてローディング状態を解除（UIの表示を確認するため）
        setTimeout(() => {
          setIsLoading(false);
        }, 500);
      }
    };

    // モックデータを設定する関数
    const useTrainingMockData = () => {
      setTrainingRecords([
        {
          id: '1',
          trainingName: 'React.js基礎研修_mock',
          category: 'フロントエンド',
          startDate: '2025-04-01',
          endDate: '2025-04-05',
          hours: 40,
          status: 'completed',
          pduPoints: 40,
          description: 'React.jsの基礎から応用まで学習_mock',
          skills: ['React', 'JavaScript', 'フロントエンド開発']
        },
        {
          id: '2',
          trainingName: 'AWS認定ソリューションアーキテクト研修_mock',
          category: 'クラウド',
          startDate: '2025-05-01',
          endDate: '2025-05-31',
          hours: 80,
          status: 'in_progress',
          pduPoints: 80,
          description: 'AWS認定資格取得のための研修_mock',
          skills: ['AWS', 'クラウドアーキテクチャ', 'インフラ設計']
        }
      ]);
    };

    const useCertificationMockData = () => {
      setCertificationRecords([
        {
          id: '1',
          certificationName: '基本情報技術者試験_mock',
          organization: 'IPA',
          acquiredDate: '2024-10-15',
          expiryDate: '無期限',
          status: 'active',
          score: '合格',
          description: 'IT基礎知識の国家資格'
        },
        {
          id: '2',
          certificationName: 'AWS認定ソリューションアーキテクト_mock',
          organization: 'Amazon Web Services',
          acquiredDate: '2025-03-20',
          expiryDate: '2028-03-20',
          status: 'active',
          score: '850/1000',
          description: 'AWSクラウドアーキテクチャ設計の認定資格'
        }
      ]);
    };

    fetchData();
  }, []);

  const getStatusBadge = (status: string) => {
    const statusConfig = {
      completed: { label: '完了', className: 'bg-green-100 text-green-800' },
      in_progress: { label: '受講中', className: 'bg-blue-100 text-blue-800' },
      planned: { label: '予定', className: 'bg-gray-100 text-gray-800' },
      active: { label: '有効', className: 'bg-green-100 text-green-800' },
      expired: { label: '期限切れ', className: 'bg-red-100 text-red-800' },
      pending: { label: '申請中', className: 'bg-yellow-100 text-yellow-800' }
    };

    const config = statusConfig[status as keyof typeof statusConfig];
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.className}`}>
        {config.label}
      </span>
    );
  };

  const handleAddRecord = () => {
    setShowAddForm(true);
  };

  const handleCancelAdd = () => {
    setShowAddForm(false);
  };

  const handleSaveRecord = () => {
    // TODO: 実際の保存処理を実装
    setShowAddForm(false);
  };

  return (
    <div className="p-6">
      {/* ページタイトル */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">研修・資格管理</h1>
        <p className="text-gray-600 mt-1">研修記録と資格情報を管理します</p>
      </div>

      {/* タブナビゲーション */}
      <div className="mb-6">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('training')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'training'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              研修記録
            </button>
            <button
              onClick={() => setActiveTab('certification')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'certification'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              資格情報
            </button>
          </nav>
        </div>
      </div>

      {/* 研修記録タブ */}
      {activeTab === 'training' && (
        <div>
          {/* アクションボタン */}
          <div className="mb-4 flex justify-between items-center">
            <div className="flex space-x-2">
              <Button onClick={handleAddRecord} variant="primary">
                新規研修記録
              </Button>
              <Button variant="secondary">
                CSVインポート
              </Button>
            </div>
            <div className="text-sm text-gray-600">
              総PDU: {trainingRecords.reduce((sum, record) => sum + record.pduPoints, 0)} ポイント
            </div>
          </div>

          {/* 研修記録一覧 */}
          <div className="bg-white rounded-lg shadow">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      研修名
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      カテゴリ
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      期間
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      時間
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      PDU
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      ステータス
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      操作
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {trainingRecords.map((record) => (
                    <tr key={record.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">{record.trainingName}</div>
                      <div className="text-sm text-gray-500">{record.description}</div>
                      {record.skills && record.skills.length > 0 && (
                        <div className="mt-1 flex flex-wrap gap-1">
                          {record.skills.map((skill: string, index: number) => (
                            <span key={index} className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                              {skill}
                            </span>
                          ))}
                        </div>
                      )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {record.category}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {record.startDate} ～ {record.endDate}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {record.hours}時間
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {record.pduPoints}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {getStatusBadge(record.status)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <button className="text-blue-600 hover:text-blue-900 mr-3">編集</button>
                        <button className="text-red-600 hover:text-red-900">削除</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* 資格情報タブ */}
      {activeTab === 'certification' && (
        <div>
          {/* アクションボタン */}
          <div className="mb-4">
            <Button onClick={handleAddRecord} variant="primary">
              新規資格登録
            </Button>
          </div>

          {/* 資格情報一覧 */}
          <div className="bg-white rounded-lg shadow">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      資格名
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      発行機関
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      取得日
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      有効期限
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      スコア
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      ステータス
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      操作
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {certificationRecords.map((record) => (
                    <tr key={record.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">{record.certificationName}</div>
                        <div className="text-sm text-gray-500">{record.description}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {record.organization}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {record.acquiredDate}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {record.expiryDate}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {record.score || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {getStatusBadge(record.status)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <button className="text-blue-600 hover:text-blue-900 mr-3">編集</button>
                        <button className="text-red-600 hover:text-red-900">削除</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ローディング表示 */}
      {isLoading ? (
        <div className="flex justify-center items-center py-8">
          <Spinner size="lg" />
        </div>
      ) : (
        <>
          {/* データが空の場合のメッセージ */}
          {activeTab === 'training' && trainingRecords.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              研修記録がありません。「新規研修記録」ボタンから登録してください。
            </div>
          )}
          {activeTab === 'certification' && certificationRecords.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              資格情報がありません。「新規資格登録」ボタンから登録してください。
            </div>
          )}
        </>
      )}
    </div>
  );
}
