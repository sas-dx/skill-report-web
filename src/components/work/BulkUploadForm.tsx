'use client';

// WRK.2-BULK.1: 作業実績一括登録フォーム（設計書準拠）
import React, { useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { Spinner } from '@/components/ui/Spinner';

interface BulkWorkRecord {
  project_name: string;
  project_code: string;
  client_name?: string;
  project_type?: string;
  project_scale?: string;
  start_date: string;
  end_date?: string;
  participation_rate?: number;
  role_title: string;
  responsibilities?: string;
  technologies_used?: string;
  skills_applied?: string;
  achievements?: string;
  challenges_faced?: string;
  lessons_learned?: string;
  team_size?: number;
  budget_range?: string;
  project_status: string;
  evaluation_score?: number;
  evaluation_comment?: string;
  is_confidential?: boolean;
  is_public_reference?: boolean;
  validation_status?: 'OK' | 'エラー';
  validation_errors?: string[];
}

interface ValidationError {
  row: number;
  field: string;
  message: string;
}

interface ValidationResultItem {
  row: number;
  status: 'OK' | 'ERROR' | 'WARNING';
  errors: Array<{ field: string; message: string }>;
  data: BulkWorkRecord;
}

interface ValidationResult {
  success: boolean;
  message: string;
  validation_id?: string;
  summary: {
    total_count: number;
    success_count: number;
    error_count: number;
    success_rate: number;
  };
  validation_result: ValidationResultItem[];
}

interface ExecutionResult {
  success: boolean;
  message: string;
  success_count: number;
  error_count: number;
  result_details?: Array<{
    row: number;
    status: 'success' | 'error';
    message: string;
  }>;
}

// 処理ステップの定義
type ProcessStep = 'upload' | 'validation' | 'execution';

export function BulkUploadForm() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState<ProcessStep>('upload');
  const [isProcessing, setIsProcessing] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [validationResult, setValidationResult] = useState<ValidationResult | null>(null);
  const [executionResult, setExecutionResult] = useState<ExecutionResult | null>(null);
  const [showErrorsOnly, setShowErrorsOnly] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // API-103: テンプレートダウンロード
  const handleDownloadTemplate = async (format: 'csv' | 'xlsx' = 'xlsx') => {
    try {
      const response = await fetch(`/api/work/bulk/template?format=${format}`);

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `work_records_template.${format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        alert('テンプレートファイルのダウンロードに失敗しました');
      }
    } catch (error) {
      console.error('Template download error:', error);
      alert('テンプレートファイルのダウンロードに失敗しました');
    }
  };

  // 戻るボタン処理
  const handleBack = () => {
    router.push('/work');
  };

  // ファイル選択処理
  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // ファイル形式チェック
      const allowedTypes = ['text/csv', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
      if (!allowedTypes.includes(file.type) && !file.name.match(/\.(csv|xlsx?)$/i)) {
        alert('対応していないファイル形式です');
        return;
      }

      setSelectedFile(file);
      setValidationResult(null);
      setExecutionResult(null);
      setCurrentStep('upload');
    }
  };

  // API-101: ファイルアップロード・バリデーション
  const handleUpload = async () => {
    if (!selectedFile) {
      alert('ファイルを選択してください');
      return;
    }

    setIsProcessing(true);
    setValidationResult(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('/api/work/bulk/validate', {
        method: 'POST',
        body: formData
      });

      const result: ValidationResult = await response.json();
      setValidationResult(result);

      if (result.success) {
        setCurrentStep('validation');
      }

    } catch (error) {
      console.error('Upload error:', error);
      setValidationResult({
        success: false,
        message: 'アップロードに失敗しました',
        summary: {
          total_count: 0,
          success_count: 0,
          error_count: 0,
          success_rate: 0
        },
        validation_result: []
      });
    } finally {
      setIsProcessing(false);
    }
  };

  // API-102: 一括登録実行
  const handleExecute = async () => {
    if (!validationResult?.validation_id) {
      alert('バリデーション結果が見つかりません');
      return;
    }

    setIsProcessing(true);
    setExecutionResult(null);

    try {
      const response = await fetch('/api/work/bulk/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          validation_id: validationResult.validation_id
        })
      });

      const result: ExecutionResult = await response.json();
      setExecutionResult(result);

      if (result.success) {
        setCurrentStep('execution');
      }

    } catch (error) {
      console.error('Execution error:', error);
      setExecutionResult({
        success: false,
        message: '登録処理に失敗しました',
        success_count: 0,
        error_count: 0
      });
    } finally {
      setIsProcessing(false);
    }
  };

  // エラー行のみ表示切り替え
  const toggleErrorsOnly = () => {
    setShowErrorsOnly(!showErrorsOnly);
  };

  // アップロードステップに戻る
  const handleBackToUpload = () => {
    setCurrentStep('upload');
    setValidationResult(null);
    setExecutionResult(null);
    setShowErrorsOnly(false);
  };

  // 表示用レコードのフィルタリング
  const getDisplayRecords = () => {
    if (!validationResult?.validation_result) return [];
    
    if (showErrorsOnly) {
      return validationResult.validation_result.filter(item => item.status === 'ERROR');
    }
    
    return validationResult.validation_result;
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      {/* ヘッダー */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              作業実績一括登録
            </h1>
            <p className="text-gray-600">
              CSV/Excelファイルを使用して複数の作業実績を一度に登録できます
            </p>
          </div>
          <Button
            onClick={handleBack}
            variant="secondary"
            className="flex items-center space-x-2"
          >
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            <span>戻る</span>
          </Button>
        </div>
      </div>

      {/* ステップ表示 */}
      <div className="bg-white rounded-lg shadow-sm border p-4">
        <div className="flex items-center justify-between">
          <div className={`flex items-center space-x-2 ${currentStep === 'upload' ? 'text-blue-600' : 'text-gray-400'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep === 'upload' ? 'bg-blue-100' : 'bg-gray-100'}`}>
              1
            </div>
            <span className="font-medium">ファイルアップロード</span>
          </div>
          <div className={`flex items-center space-x-2 ${currentStep === 'validation' ? 'text-blue-600' : 'text-gray-400'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep === 'validation' ? 'bg-blue-100' : 'bg-gray-100'}`}>
              2
            </div>
            <span className="font-medium">登録前確認</span>
          </div>
          <div className={`flex items-center space-x-2 ${currentStep === 'execution' ? 'text-blue-600' : 'text-gray-400'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep === 'execution' ? 'bg-blue-100' : 'bg-gray-100'}`}>
              3
            </div>
            <span className="font-medium">登録完了</span>
          </div>
        </div>
      </div>

      {/* テンプレートダウンロード */}
      <div className="bg-blue-50 rounded-lg border border-blue-200 p-4">
        <div className="flex items-start space-x-3">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="flex-1">
            <h3 className="text-sm font-medium text-blue-800">
              テンプレートダウンロード
            </h3>
            <p className="text-sm text-blue-700 mt-1">
              正しい形式でデータを入力するために、まずテンプレートファイルをダウンロードしてください
            </p>
            <div className="flex space-x-2 mt-3">
              <Button
                onClick={() => handleDownloadTemplate('xlsx')}
                variant="secondary"
                size="sm"
              >
                Excelテンプレート
              </Button>
              <Button
                onClick={() => handleDownloadTemplate('csv')}
                variant="secondary"
                size="sm"
              >
                CSVテンプレート
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* ファイルアップロード */}
      {currentStep === 'upload' && (
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            ファイルアップロード
          </h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                ファイルを選択
              </label>
              <input
                ref={fileInputRef}
                type="file"
                accept=".csv,.xlsx,.xls"
                onChange={handleFileSelect}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              />
              <p className="text-sm text-gray-500 mt-1">
                対応形式: CSV, Excel(xlsx)
              </p>
            </div>

            {selectedFile && (
              <div className="bg-gray-50 rounded-md p-3">
                <p className="text-sm text-gray-600">
                  選択されたファイル: <span className="font-medium">{selectedFile.name}</span>
                </p>
                <p className="text-sm text-gray-500">
                  サイズ: {Math.round(selectedFile.size / 1024)}KB
                </p>
              </div>
            )}

            <div className="flex space-x-3">
              <Button
                onClick={handleUpload}
                disabled={!selectedFile || isProcessing}
                className="flex items-center space-x-2"
              >
                {isProcessing && <Spinner size="sm" />}
                <span>{isProcessing ? 'アップロード中...' : 'アップロード'}</span>
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* 登録前確認 */}
      {currentStep === 'validation' && validationResult && (
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">
              登録前確認
            </h2>
            <div className="flex space-x-2">
              {validationResult.success && (
                <Button
                  onClick={handleBackToUpload}
                  variant="secondary"
                  size="sm"
                  className="flex items-center space-x-2"
                >
                  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                  <span>戻る</span>
                </Button>
              )}
              <Button
                onClick={toggleErrorsOnly}
                variant="secondary"
                size="sm"
                className={showErrorsOnly ? 'bg-red-100 text-red-700' : ''}
              >
                エラー行のみ表示
              </Button>
              <Button
                onClick={handleExecute}
                disabled={isProcessing || validationResult.summary.error_count > 0}
                className="flex items-center space-x-2"
              >
                {isProcessing && <Spinner size="sm" />}
                <span>{isProcessing ? '登録中...' : '一括登録実行'}</span>
              </Button>
            </div>
          </div>

          {/* サマリー */}
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div className="text-center p-3 bg-gray-50 rounded">
              <div className="text-lg font-semibold text-gray-900">
                {validationResult.summary.total_count}
              </div>
              <div className="text-sm text-gray-600">総件数</div>
            </div>
            <div className="text-center p-3 bg-green-50 rounded">
              <div className="text-lg font-semibold text-green-600">
                {validationResult.summary.success_count}
              </div>
              <div className="text-sm text-gray-600">正常</div>
            </div>
            <div className="text-center p-3 bg-red-50 rounded">
              <div className="text-lg font-semibold text-red-600">
                {validationResult.summary.error_count}
              </div>
              <div className="text-sm text-gray-600">エラー</div>
            </div>
          </div>

          {/* データテーブル */}
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">行</th>
                  <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">プロジェクト名</th>
                  <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">作業日</th>
                  <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">作業内容</th>
                  <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">工数</th>
                  <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">状態</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {getDisplayRecords()?.slice(0, 20)?.map((item, index) => (
                  <tr key={index} className={`hover:bg-gray-50 ${item.status === 'ERROR' ? 'bg-red-50' : ''}`}>
                    <td className="px-3 py-2 text-sm text-gray-900">{item.row}</td>
                    <td className="px-3 py-2 text-sm text-gray-900">{item.data.project_name}</td>
                    <td className="px-3 py-2 text-sm text-gray-900">{item.data.start_date}</td>
                    <td className="px-3 py-2 text-sm text-gray-900">{item.data.role_title}</td>
                    <td className="px-3 py-2 text-sm text-gray-900">{item.data.participation_rate || '-'}</td>
                    <td className="px-3 py-2 text-sm">
                      {item.status === 'ERROR' ? (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                          エラー
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          OK
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {getDisplayRecords()?.length > 20 && (
              <p className="text-sm text-gray-500 mt-2">
                ...他 {getDisplayRecords()?.length - 20} 件
              </p>
            )}
          </div>

          {/* エラー詳細 */}
          {validationResult.validation_result.some(item => item.errors.length > 0) && (
            <div className="mt-4 p-4 bg-red-50 rounded-lg">
              <h4 className="text-sm font-medium text-red-800 mb-2">エラー詳細:</h4>
              <div className="max-h-40 overflow-y-auto space-y-1">
                {validationResult.validation_result
                  .filter(item => item.errors.length > 0)
                  .map((item, itemIndex) => 
                    item.errors.map((error, errorIndex) => (
                      <div key={`${itemIndex}-${errorIndex}`} className="text-sm text-red-700">
                        行{item.row}: {error.field} - {error.message}
                      </div>
                    ))
                  )
                  .flat()}
              </div>
            </div>
          )}
        </div>
      )}

      {/* 実行結果 */}
      {currentStep === 'execution' && executionResult && (
        <div className={`rounded-lg border p-6 ${
          executionResult.success 
            ? 'bg-green-50 border-green-200' 
            : 'bg-red-50 border-red-200'
        }`}>
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0">
              {executionResult.success ? (
                <svg className="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              ) : (
                <svg className="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              )}
            </div>
            <div className="flex-1">
              <h3 className={`text-sm font-medium ${
                executionResult.success ? 'text-green-800' : 'text-red-800'
              }`}>
                {executionResult.message}
              </h3>

              {/* 実行結果サマリー */}
              <div className="mt-3 grid grid-cols-2 gap-4">
                <div className="text-center">
                  <div className="text-lg font-semibold text-green-600">
                    {executionResult.success_count}
                  </div>
                  <div className="text-sm text-gray-600">成功件数</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-semibold text-red-600">
                    {executionResult.error_count}
                  </div>
                  <div className="text-sm text-gray-600">エラー件数</div>
                </div>
              </div>

              {/* 詳細結果 */}
              {executionResult.result_details && executionResult.result_details.length > 0 && (
                <div className="mt-4">
                  <h4 className="text-sm font-medium text-gray-800 mb-2">詳細結果:</h4>
                  <div className="max-h-40 overflow-y-auto space-y-1">
                    {executionResult.result_details.map((detail, index) => (
                      <div key={index} className={`text-sm ${detail.status === 'success' ? 'text-green-700' : 'text-red-700'}`}>
                        行{detail.row}: {detail.message}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 完了後のアクション */}
              {executionResult.success && (
                <div className="mt-4 flex space-x-2">
                  <Button
                    onClick={handleBack}
                    variant="primary"
                  >
                    作業実績画面に戻る
                  </Button>
                  <Button
                    onClick={() => {
                      setCurrentStep('upload');
                      setSelectedFile(null);
                      setValidationResult(null);
                      setExecutionResult(null);
                      if (fileInputRef.current) {
                        fileInputRef.current.value = '';
                      }
                    }}
                    variant="secondary"
                  >
                    続けて登録
                  </Button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* バリデーション結果（アップロード直後） */}
      {validationResult && !validationResult.success && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="flex-1">
              <h3 className="text-sm font-medium text-red-800">
                {validationResult.message}
              </h3>
              <p className="text-sm text-red-700 mt-1">
                ファイルを修正してから再度アップロードしてください。
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
