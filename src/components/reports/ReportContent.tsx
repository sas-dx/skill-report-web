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
  const [isLoading, setIsLoading] = useState(true);
  const [reportTemplates, setReportTemplates] = useState<ReportTemplate[]>([]);
  const [generatedReports, setGeneratedReports] = useState<GeneratedReport[]>([]);
  const [activeTab, setActiveTab] = useState<'templates' | 'history'>('templates');
  const [error, setError] = useState<string | null>(null);
  const [notification, setNotification] = useState<{message: string, type: 'success' | 'error'} | null>(null);

  // データの初期化
  useEffect(() => {
    loadData();
  }, []);

  // 通知の自動非表示
  useEffect(() => {
    if (notification) {
      const timer = setTimeout(() => {
        setNotification(null);
      }, 5000); // 5秒後に自動で非表示
      return () => clearTimeout(timer);
    }
    return undefined;
  }, [notification]);

  const loadData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      await Promise.all([
        loadReportTemplates(),
        loadGeneratedReports()
      ]);
    } catch (error) {
      console.error('データ読み込みエラー:', error);
      setError('データの読み込みに失敗しました。ページを再読み込みしてください。');
    } finally {
      setIsLoading(false);
    }
  };

  const loadReportTemplates = async () => {
    try {
      const tenant = localStorage.getItem('tenant');
      const tenantData = tenant ? JSON.parse(tenant) : null;
      
      const response = await fetch('/api/reports/templates', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'x-tenant-id': tenantData?.id || ''
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      if (result.success && result.data?.templates) {
        const formattedTemplates = result.data.templates.map((template: any) => ({
          id: template.id,
          name: template.templateName,
          description: template.description,
          category: template.category,
          format: template.format,
          icon: getCategoryIcon(template.category)
        }));
        setReportTemplates(formattedTemplates);
      }
    } catch (error) {
      console.error('レポートテンプレート読み込みエラー:', error);
    }
  };

  const loadGeneratedReports = async () => {
    try {
      const tenant = localStorage.getItem('tenant');
      const tenantData = tenant ? JSON.parse(tenant) : null;
      
      const response = await fetch('/api/reports/history', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'x-tenant-id': tenantData?.id || ''
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      if (result.success && result.data?.reports) {
        const formattedReports = result.data.reports.map((report: any) => ({
          id: report.id,
          name: report.title,
          generatedAt: report.completedAt ? new Date(report.completedAt).toLocaleString('ja-JP') : '処理中',
          format: report.format.toUpperCase(),
          size: formatFileSize(report.fileSize),
          status: mapStatus(report.status),
          downloadUrl: report.status === 'COMPLETED' ? `/api/reports/${report.id}/download` : undefined
        }));
        setGeneratedReports(formattedReports);
      }
    } catch (error) {
      console.error('生成レポート履歴読み込みエラー:', error);
    }
  };

  const getCategoryIcon = (category: string): string => {
    const iconMap: { [key: string]: string } = {
      'スキル管理': '📊',
      '研修管理': '🎓',
      'キャリア管理': '🎯',
      '作業管理': '📈',
      '分析': '🗺️'
    };
    return iconMap[category] || '📄';
  };

  const formatFileSize = (bytes: number | null): string => {
    if (!bytes) return '';
    const sizes = ['B', 'KB', 'MB', 'GB'];
    if (bytes === 0) return '0 B';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
  };

  const mapStatus = (status: string): 'completed' | 'generating' | 'failed' => {
    switch (status) {
      case 'COMPLETED': return 'completed';
      case 'PENDING':
      case 'PROCESSING': return 'generating';
      case 'FAILED':
      case 'ERROR': return 'failed';
      default: return 'generating';
    }
  };

  const handleGenerateReport = async (templateId: string) => {
    try {
      const template = reportTemplates.find(t => t.id === templateId);
      if (!template) {
        throw new Error('テンプレートが見つかりません');
      }

      const tenant = localStorage.getItem('tenant');
      const tenantData = tenant ? JSON.parse(tenant) : null;
      
      const response = await fetch('/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'x-tenant-id': tenantData?.id || ''
        },
        body: JSON.stringify({
          templateId,
          reportTitle: `${template.name}_${new Date().toLocaleDateString('ja-JP')}`,
          parameters: {
            // デフォルトパラメータ（必要に応じて調整）
            startDate: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            endDate: new Date().toISOString().split('T')[0]
          }
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      if (result.success) {
        // 生成リクエスト成功の通知
        setNotification({
          message: 'レポート生成リクエストを受け付けました。生成が完了次第、履歴に表示されます。',
          type: 'success'
        });
        
        // 履歴を再読み込み
        await loadGeneratedReports();
      } else {
        throw new Error(result.error?.message || 'レポート生成に失敗しました');
      }
    } catch (error) {
      console.error('レポート生成エラー:', error);
      setNotification({
        message: 'レポート生成に失敗しました。しばらく時間をおいて再度お試しください。',
        type: 'error'
      });
    }
  };

  const handleDownload = (report: GeneratedReport) => {
    if (report.downloadUrl && report.status === 'completed') {
      // ダウンロードリンクを開く
      const link = document.createElement('a');
      link.href = report.downloadUrl;
      link.download = report.name;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  const handleDeleteReport = async (reportId: string) => {
    if (!confirm('このレポートを削除しますか？この操作は取り消せません。')) {
      return;
    }

    try {
      const tenant = localStorage.getItem('tenant');
      const tenantData = tenant ? JSON.parse(tenant) : null;
      
      const response = await fetch(`/api/reports/${reportId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'x-tenant-id': tenantData?.id || ''
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      if (result.success) {
        setNotification({
          message: 'レポートを削除しました。',
          type: 'success'
        });
        // 履歴を再読み込み
        await loadGeneratedReports();
      } else {
        throw new Error(result.error?.message || 'レポート削除に失敗しました');
      }
    } catch (error) {
      console.error('レポート削除エラー:', error);
      setNotification({
        message: 'レポート削除に失敗しました。',
        type: 'error'
      });
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

      {/* 通知表示 */}
      {notification && (
        <div className={`mb-6 p-4 rounded-md ${
          notification.type === 'success' 
            ? 'bg-green-100 border border-green-400 text-green-700' 
            : 'bg-red-100 border border-red-400 text-red-700'
        }`}>
          <div className="flex justify-between items-center">
            <span>{notification.message}</span>
            <button
              onClick={() => setNotification(null)}
              className="ml-3 text-lg font-semibold leading-none"
            >
              ×
            </button>
          </div>
        </div>
      )}

      {/* エラー表示 */}
      {error && (
        <div className="mb-6 p-4 rounded-md bg-red-100 border border-red-400 text-red-700">
          <div className="flex justify-between items-center">
            <span>{error}</span>
            <button
              onClick={() => setError(null)}
              className="ml-3 text-lg font-semibold leading-none"
            >
              ×
            </button>
          </div>
        </div>
      )}

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
          {isLoading ? (
            <div className="text-center py-12">
              <Spinner size="lg" />
              <p className="text-gray-600 mt-4">テンプレートを読み込み中...</p>
            </div>
          ) : reportTemplates.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">📊</div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">レポートテンプレートがありません</h3>
              <p className="text-gray-500">利用可能なレポートテンプレートがありません。</p>
            </div>
          ) : (
            /* カテゴリ別グリッド表示 */
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
                    レポート生成
                  </Button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* 生成履歴タブ */}
      {activeTab === 'history' && (
        <div>
          {isLoading ? (
            <div className="text-center py-12">
              <Spinner size="lg" />
              <p className="text-gray-600 mt-4">履歴を読み込み中...</p>
            </div>
          ) : generatedReports.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">📂</div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">生成履歴がありません</h3>
              <p className="text-gray-500">まだレポートが生成されていません。テンプレートからレポートを生成してください。</p>
            </div>
          ) : (
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
                          <button 
                            onClick={() => handleDeleteReport(report.id)}
                            className="text-red-600 hover:text-red-900"
                          >
                            削除
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

    </div>
  );
}
