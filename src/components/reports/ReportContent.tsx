// RPT.1-EXCEL.1: レポートコンテンツコンポーネント
'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { Spinner } from '@/components/ui/Spinner';

interface ReportTemplate {
  id: string;
  name: string;
  description: string;
  category: string;
  format: 'excel' | 'pdf' | 'csv';
  icon: string;
}

interface GeneratedReport {
  id: string;
  name: string;
  generatedAt: string;
  format: string;
  size: string;
  status: 'completed' | 'generating' | 'failed';
  downloadUrl?: string;
}

export function ReportContent() {
  const [isLoading, setIsLoading] = useState(false);
  const [reportTemplates, setReportTemplates] = useState<ReportTemplate[]>([]);
  const [generatedReports, setGeneratedReports] = useState<GeneratedReport[]>([]);
  const [activeTab, setActiveTab] = useState<'templates' | 'history'>('templates');

  // モックデータの初期化
  useEffect(() => {
    const mockTemplates: ReportTemplate[] = [
      {
        id: '1',
        name: 'スキル一覧レポート',
        description: '全社員のスキル情報を一覧で出力',
        category: 'スキル管理',
        format: 'excel',
        icon: '📊'
      },
      {
        id: '2',
        name: '個人スキル報告書',
        description: '個人のスキル詳細情報をPDF形式で出力',
        category: 'スキル管理',
        format: 'pdf',
        icon: '📄'
      },
      {
        id: '3',
        name: '研修実績レポート',
        description: '研修参加実績と効果測定結果',
        category: '研修管理',
        format: 'excel',
        icon: '🎓'
      },
      {
        id: '4',
        name: 'キャリア目標進捗レポート',
        description: '部門別キャリア目標の進捗状況',
        category: 'キャリア管理',
        format: 'excel',
        icon: '🎯'
      },
      {
        id: '5',
        name: '作業実績サマリー',
        description: 'プロジェクト別作業実績の集計',
        category: '作業管理',
        format: 'csv',
        icon: '📈'
      },
      {
        id: '6',
        name: '組織スキルマップ',
        description: '組織全体のスキル分布状況',
        category: '分析',
        format: 'pdf',
        icon: '🗺️'
      }
    ];

    const mockGeneratedReports: GeneratedReport[] = [
      {
        id: '1',
        name: 'スキル一覧レポート_2025年5月',
        generatedAt: '2025-05-30 14:30',
        format: 'Excel',
        size: '2.3MB',
        status: 'completed',
        downloadUrl: '/downloads/skill-report-202505.xlsx'
      },
      {
        id: '2',
        name: '研修実績レポート_Q1',
        generatedAt: '2025-05-28 09:15',
        format: 'Excel',
        size: '1.8MB',
        status: 'completed',
        downloadUrl: '/downloads/training-report-q1.xlsx'
      },
      {
        id: '3',
        name: '組織スキルマップ_2025年度',
        generatedAt: '2025-05-25 16:45',
        format: 'PDF',
        size: '5.2MB',
        status: 'completed',
        downloadUrl: '/downloads/skill-map-2025.pdf'
      }
    ];

    setReportTemplates(mockTemplates);
    setGeneratedReports(mockGeneratedReports);
  }, []);

  const handleGenerateReport = async (templateId: string) => {
    setIsLoading(true);
    try {
      // TODO: 実際のレポート生成処理を実装
      await new Promise(resolve => setTimeout(resolve, 2000)); // 模擬的な処理時間
      
      // 生成完了後の処理
      const template = reportTemplates.find(t => t.id === templateId);
      if (template) {
        const newReport: GeneratedReport = {
          id: Date.now().toString(),
          name: `${template.name}_${new Date().toLocaleDateString('ja-JP')}`,
          generatedAt: new Date().toLocaleString('ja-JP'),
          format: template.format.toUpperCase(),
          size: '1.5MB',
          status: 'completed',
          downloadUrl: `/downloads/report-${Date.now()}.${template.format}`
        };
        setGeneratedReports(prev => [newReport, ...prev]);
      }
    } catch (error) {
      console.error('レポート生成エラー:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = (report: GeneratedReport) => {
    if (report.downloadUrl) {
      // TODO: 実際のダウンロード処理を実装
      console.log('ダウンロード:', report.downloadUrl);
    }
  };

  const getFormatBadge = (format: string) => {
    const formatConfig = {
      excel: { label: 'Excel', className: 'bg-green-100 text-green-800' },
      pdf: { label: 'PDF', className: 'bg-red-100 text-red-800' },
      csv: { label: 'CSV', className: 'bg-blue-100 text-blue-800' }
    };

    const config = formatConfig[format.toLowerCase() as keyof typeof formatConfig] || 
                   { label: format, className: 'bg-gray-100 text-gray-800' };
    
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.className}`}>
        {config.label}
      </span>
    );
  };

  const getStatusBadge = (status: string) => {
    const statusConfig = {
      completed: { label: '完了', className: 'bg-green-100 text-green-800' },
      generating: { label: '生成中', className: 'bg-blue-100 text-blue-800' },
      failed: { label: '失敗', className: 'bg-red-100 text-red-800' }
    };

    const config = statusConfig[status as keyof typeof statusConfig];
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.className}`}>
        {config.label}
      </span>
    );
  };

  return (
    <div className="p-6">
      {/* ページタイトル */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">レポート管理</h1>
        <p className="text-gray-600 mt-1">各種レポートの生成とダウンロードを行います</p>
      </div>

      {/* タブナビゲーション */}
      <div className="mb-6">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('templates')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'templates'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              レポートテンプレート
            </button>
            <button
              onClick={() => setActiveTab('history')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'history'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              生成履歴
            </button>
          </nav>
        </div>
      </div>

      {/* レポートテンプレートタブ */}
      {activeTab === 'templates' && (
        <div>
          {/* カテゴリ別グリッド表示 */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {reportTemplates.map((template) => (
              <div key={template.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center">
                    <span className="text-2xl mr-3">{template.icon}</span>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">{template.name}</h3>
                      <p className="text-sm text-gray-500">{template.category}</p>
                    </div>
                  </div>
                  {getFormatBadge(template.format)}
                </div>
                
                <p className="text-gray-600 text-sm mb-4">{template.description}</p>
                
                <Button
                  onClick={() => handleGenerateReport(template.id)}
                  variant="primary"
                  disabled={isLoading}
                  className="w-full"
                >
                  {isLoading ? '生成中...' : 'レポート生成'}
                </Button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 生成履歴タブ */}
      {activeTab === 'history' && (
        <div>
          <div className="bg-white rounded-lg shadow">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      レポート名
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      生成日時
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      形式
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      サイズ
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
                  {generatedReports.map((report) => (
                    <tr key={report.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">{report.name}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {report.generatedAt}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {getFormatBadge(report.format)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {report.size}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {getStatusBadge(report.status)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        {report.status === 'completed' && (
                          <button
                            onClick={() => handleDownload(report)}
                            className="text-blue-600 hover:text-blue-900 mr-3"
                          >
                            ダウンロード
                          </button>
                        )}
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
      {isLoading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-white rounded-lg p-6 flex items-center space-x-3">
            <Spinner size="md" />
            <span className="text-gray-700">レポートを生成しています...</span>
          </div>
        </div>
      )}
    </div>
  );
}
