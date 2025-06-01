// WPM.1-DET.1: 作業実績管理画面
'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { 
  mockWorkRecords, 
  projectStatusLabels,
  type WorkRecord 
} from '@/lib/mockData';

export default function WorkPage() {
  const [workRecords] = useState(mockWorkRecords);
  const [selectedStatus, setSelectedStatus] = useState<'all' | 'planning' | 'active' | 'completed' | 'suspended'>('all');
  const [expandedRecord, setExpandedRecord] = useState<string | null>(null);

  const filteredRecords = selectedStatus === 'all' 
    ? workRecords 
    : workRecords.filter(record => record.project.status === selectedStatus);

  const getStatusColor = (status: WorkRecord['project']['status']) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'active': return 'bg-blue-100 text-blue-800';
      case 'planning': return 'bg-yellow-100 text-yellow-800';
      case 'suspended': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const toggleExpanded = (recordId: string) => {
    setExpandedRecord(expandedRecord === recordId ? null : recordId);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ja-JP');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* ヘッダー */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">作業実績</h1>
          <p className="mt-2 text-gray-600">
            プロジェクトでの作業実績と成果を管理します
          </p>
        </div>

        {/* フィルター・アクション */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-8">
          <div className="px-6 py-4">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
              <div className="flex items-center space-x-4">
                <label className="text-sm font-medium text-gray-700">
                  ステータス:
                </label>
                <select
                  value={selectedStatus}
                  onChange={(e) => setSelectedStatus(e.target.value as any)}
                  className="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-blue-500"
                >
                  <option value="all">すべて</option>
                  <option value="planning">計画中</option>
                  <option value="active">進行中</option>
                  <option value="completed">完了</option>
                  <option value="suspended">中断</option>
                </select>
              </div>
              <div className="mt-4 sm:mt-0">
                <Button>
                  新しい実績を追加
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* 実績一覧 */}
        <div className="space-y-6">
          {filteredRecords.length === 0 ? (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200">
              <div className="text-center py-12">
                <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900">作業実績がありません</h3>
                <p className="mt-1 text-sm text-gray-500">
                  新しい作業実績を追加して、プロジェクトの成果を記録しましょう。
                </p>
                <div className="mt-6">
                  <Button>
                    最初の実績を追加
                  </Button>
                </div>
              </div>
            </div>
          ) : (
            filteredRecords.map((record) => (
              <div key={record.id} className="bg-white rounded-lg shadow-sm border border-gray-200">
                {/* プロジェクト概要 */}
                <div className="px-6 py-4 border-b border-gray-200">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="text-xl font-semibold text-gray-900">
                          {record.project.project_name}
                        </h3>
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(record.project.status)}`}>
                          {projectStatusLabels[record.project.status]}
                        </span>
                      </div>
                      {record.project.client_name && (
                        <p className="text-sm text-gray-600 mb-2">
                          クライアント: {record.project.client_name}
                        </p>
                      )}
                      <p className="text-gray-700 mb-3">
                        {record.project.description}
                      </p>
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm">
                        <div>
                          <span className="font-medium text-gray-500">期間:</span>
                          <p className="text-gray-900">
                            {formatDate(record.project.start_date)} - {record.project.end_date ? formatDate(record.project.end_date) : '進行中'}
                          </p>
                        </div>
                        <div>
                          <span className="font-medium text-gray-500">役割:</span>
                          <p className="text-gray-900">{record.project.role}</p>
                        </div>
                        <div>
                          <span className="font-medium text-gray-500">チーム規模:</span>
                          <p className="text-gray-900">{record.project.team_size}名</p>
                        </div>
                      </div>
                    </div>
                    <div className="ml-6 flex flex-col space-y-2">
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => toggleExpanded(record.id)}
                      >
                        {expandedRecord === record.id ? '詳細を閉じる' : '詳細を見る'}
                      </Button>
                      <Button variant="outline" size="sm">
                        編集
                      </Button>
                    </div>
                  </div>
                </div>

                {/* 技術スタック */}
                <div className="px-6 py-4 border-b border-gray-200">
                  <h4 className="text-sm font-medium text-gray-700 mb-2">使用技術</h4>
                  <div className="flex flex-wrap gap-2">
                    {record.project.technologies.map((tech, index) => (
                      <span 
                        key={index}
                        className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>

                {/* 詳細情報（展開時） */}
                {expandedRecord === record.id && (
                  <div className="px-6 py-6 space-y-6">
                    {/* 担当業務 */}
                    <div>
                      <h4 className="text-lg font-medium text-gray-900 mb-3">担当業務</h4>
                      <ul className="space-y-2">
                        {record.responsibilities.map((responsibility, index) => (
                          <li key={index} className="flex items-start">
                            <span className="flex-shrink-0 w-1.5 h-1.5 bg-blue-500 rounded-full mt-2 mr-3"></span>
                            <span className="text-gray-700">{responsibility}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* 成果・実績 */}
                    <div>
                      <h4 className="text-lg font-medium text-gray-900 mb-3">成果・実績</h4>
                      <ul className="space-y-2">
                        {record.achievements.map((achievement, index) => (
                          <li key={index} className="flex items-start">
                            <span className="flex-shrink-0 w-1.5 h-1.5 bg-green-500 rounded-full mt-2 mr-3"></span>
                            <span className="text-gray-700">{achievement}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* スキル情報 */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                      <div>
                        <h4 className="text-lg font-medium text-gray-900 mb-3">使用したスキル</h4>
                        <div className="flex flex-wrap gap-2">
                          {record.skills_used.map((skill, index) => (
                            <span 
                              key={index}
                              className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
                            >
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                      <div>
                        <h4 className="text-lg font-medium text-gray-900 mb-3">習得したスキル</h4>
                        <div className="flex flex-wrap gap-2">
                          {record.skills_acquired.map((skill, index) => (
                            <span 
                              key={index}
                              className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
                            >
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>

                    {/* 課題・学び */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                      <div>
                        <h4 className="text-lg font-medium text-gray-900 mb-3">課題・困難</h4>
                        <p className="text-gray-700 leading-relaxed">
                          {record.challenges}
                        </p>
                      </div>
                      <div>
                        <h4 className="text-lg font-medium text-gray-900 mb-3">学んだこと</h4>
                        <p className="text-gray-700 leading-relaxed">
                          {record.lessons_learned}
                        </p>
                      </div>
                    </div>

                    {/* 更新情報 */}
                    <div className="pt-4 border-t border-gray-200">
                      <div className="flex justify-between text-sm text-gray-500">
                        <span>作成日: {formatDate(record.created_at)}</span>
                        <span>最終更新: {formatDate(record.updated_at)}</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
