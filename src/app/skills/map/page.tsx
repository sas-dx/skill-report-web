/**
 * 要求仕様ID: SKL.1-HIER.1
 * 対応設計書: docs/design/screens/specs/画面設計書_SCR-SKILLMAP_スキルマップ画面.md
 * 実装内容: スキルマップ表示・検索・エクスポート機能
 */
'use client';

import React, { useState, useEffect } from 'react';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { Sidebar } from '@/components/dashboard/Sidebar';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Spinner } from '@/components/ui/Spinner';
import { SkillMapChart } from '@/components/skills/SkillMapChart';
import { SkillMapFilters } from '@/components/skills/SkillMapFilters';
import { SkillMapTable } from '@/components/skills/SkillMapTable';
import { SkillMapExport } from '@/components/skills/SkillMapExport';

interface Employee {
  id: string;
  empNo: string;
  name: string;
  department: string;
  position: string;
  skills: EmployeeSkill[];
}

interface EmployeeSkill {
  id: string;
  skillName: string;
  category: string;
  subcategory: string;
  level: number;
  experienceYears: number;
  lastUsed: string;
  certification?: string;
}

interface SkillMapFilters {
  department: string;
  position: string;
  skillCategory: string;
  skillLevel: number;
  searchTerm: string;
}

interface SkillMapData {
  employees: Employee[];
  skillCategories: string[];
  departments: string[];
  positions: string[];
}

export default function SkillMapPage() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [skillMapData, setSkillMapData] = useState<SkillMapData>({
    employees: [],
    skillCategories: [],
    departments: [],
    positions: []
  });
  const [filters, setFilters] = useState<SkillMapFilters>({
    department: '',
    position: '',
    skillCategory: '',
    skillLevel: 0,
    searchTerm: ''
  });
  const [activeView, setActiveView] = useState<'chart' | 'table'>('chart');
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);

  const handleMenuClick = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleSidebarClose = () => {
    setIsSidebarOpen(false);
  };

  // データ読み込み
  useEffect(() => {
    const loadSkillMapData = async () => {
      try {
        setIsLoading(true);
        
        // モックデータ（実際のAPIに置き換え予定）
        await new Promise(resolve => setTimeout(resolve, 1000));

        const mockData: SkillMapData = {
          employees: [
            {
              id: '1',
              empNo: 'EMP001',
              name: '山田太郎',
              department: '開発部',
              position: 'シニアエンジニア',
              skills: [
                {
                  id: '1',
                  skillName: 'JavaScript',
                  category: 'プログラミング言語',
                  subcategory: 'フロントエンド',
                  level: 4,
                  experienceYears: 5,
                  lastUsed: '2025-06-20',
                  certification: ''
                },
                {
                  id: '2',
                  skillName: 'React',
                  category: 'プログラミング言語',
                  subcategory: 'フロントエンド',
                  level: 4,
                  experienceYears: 3,
                  lastUsed: '2025-06-20',
                  certification: ''
                },
                {
                  id: '3',
                  skillName: 'AWS',
                  category: 'インフラ・クラウド',
                  subcategory: 'クラウドサービス',
                  level: 3,
                  experienceYears: 2,
                  lastUsed: '2025-06-15',
                  certification: 'AWS Solutions Architect Associate'
                }
              ]
            },
            {
              id: '2',
              empNo: 'EMP002',
              name: '佐藤花子',
              department: '開発部',
              position: 'エンジニア',
              skills: [
                {
                  id: '4',
                  skillName: 'Python',
                  category: 'プログラミング言語',
                  subcategory: 'バックエンド',
                  level: 3,
                  experienceYears: 2,
                  lastUsed: '2025-06-18',
                  certification: ''
                },
                {
                  id: '5',
                  skillName: 'PostgreSQL',
                  category: 'データベース',
                  subcategory: 'リレーショナル',
                  level: 3,
                  experienceYears: 2,
                  lastUsed: '2025-06-19',
                  certification: ''
                }
              ]
            },
            {
              id: '3',
              empNo: 'EMP003',
              name: '田中一郎',
              department: 'インフラ部',
              position: 'インフラエンジニア',
              skills: [
                {
                  id: '6',
                  skillName: 'Docker',
                  category: 'インフラ・クラウド',
                  subcategory: 'コンテナ',
                  level: 4,
                  experienceYears: 3,
                  lastUsed: '2025-06-20',
                  certification: ''
                },
                {
                  id: '7',
                  skillName: 'Kubernetes',
                  category: 'インフラ・クラウド',
                  subcategory: 'コンテナ',
                  level: 3,
                  experienceYears: 1,
                  lastUsed: '2025-06-10',
                  certification: 'CKA'
                }
              ]
            }
          ],
          skillCategories: ['プログラミング言語', 'インフラ・クラウド', 'データベース'],
          departments: ['開発部', 'インフラ部', '営業部'],
          positions: ['シニアエンジニア', 'エンジニア', 'インフラエンジニア', 'マネージャー']
        };

        setSkillMapData(mockData);
      } catch (error) {
        console.error('スキルマップデータの読み込みエラー:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadSkillMapData();
  }, []);

  // フィルター適用
  const filteredEmployees = skillMapData.employees.filter(employee => {
    // 部署フィルター
    if (filters.department && employee.department !== filters.department) {
      return false;
    }

    // 役職フィルター
    if (filters.position && employee.position !== filters.position) {
      return false;
    }

    // 検索キーワード
    if (filters.searchTerm) {
      const searchLower = filters.searchTerm.toLowerCase();
      const matchesName = employee.name.toLowerCase().includes(searchLower);
      const matchesSkill = employee.skills.some(skill => 
        skill.skillName.toLowerCase().includes(searchLower)
      );
      if (!matchesName && !matchesSkill) {
        return false;
      }
    }

    // スキルカテゴリフィルター
    if (filters.skillCategory) {
      const hasSkillInCategory = employee.skills.some(skill => 
        skill.category === filters.skillCategory
      );
      if (!hasSkillInCategory) {
        return false;
      }
    }

    // スキルレベルフィルター
    if (filters.skillLevel > 0) {
      const hasSkillAtLevel = employee.skills.some(skill => 
        skill.level >= filters.skillLevel
      );
      if (!hasSkillAtLevel) {
        return false;
      }
    }

    return true;
  });

  const handleFilterChange = (newFilters: Partial<SkillMapFilters>) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  const handleExport = async (format: 'excel' | 'csv' | 'pdf') => {
    try {
      const response = await fetch('/api/skills/map/export', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          format,
          filters,
          employees: filteredEmployees
        }),
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `skillmap_${new Date().toISOString().split('T')[0]}.${format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        throw new Error('エクスポートに失敗しました');
      }
    } catch (error) {
      console.error('エクスポートエラー:', error);
      alert('エクスポートに失敗しました');
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <DashboardHeader 
          onMenuClick={handleMenuClick}
          title="スキルマップ"
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
        title="スキルマップ"
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
          <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
            {/* ページヘッダー */}
            <div className="mb-8">
              <h1 className="text-2xl font-bold text-gray-900">スキルマップ</h1>
              <p className="text-gray-600 mt-1">組織全体のスキル分布を可視化・分析します</p>
            </div>

            {/* フィルター */}
            <SkillMapFilters
              filters={filters}
              skillCategories={skillMapData.skillCategories}
              departments={skillMapData.departments}
              positions={skillMapData.positions}
              onFilterChange={handleFilterChange}
            />

            {/* ビュー切り替えとエクスポート */}
            <div className="mb-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div className="flex space-x-2">
                <Button
                  onClick={() => setActiveView('chart')}
                  variant={activeView === 'chart' ? 'primary' : 'secondary'}
                  size="sm"
                >
                  チャート表示
                </Button>
                <Button
                  onClick={() => setActiveView('table')}
                  variant={activeView === 'table' ? 'primary' : 'secondary'}
                  size="sm"
                >
                  テーブル表示
                </Button>
              </div>

              <SkillMapExport onExport={handleExport} />
            </div>

            {/* 結果表示 */}
            <div className="mb-4">
              <p className="text-sm text-gray-600">
                {filteredEmployees.length}名の従業員が表示されています
              </p>
            </div>

            {/* メインコンテンツ */}
            {activeView === 'chart' ? (
              <SkillMapChart 
                employees={filteredEmployees}
                selectedSkills={selectedSkills}
                onSkillSelect={setSelectedSkills}
              />
            ) : (
              <SkillMapTable 
                employees={filteredEmployees}
                onEmployeeSelect={(employeeId) => {
                  console.log('Selected employee:', employeeId);
                }}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
