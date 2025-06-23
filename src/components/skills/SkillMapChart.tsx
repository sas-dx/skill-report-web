/**
 * 要求仕様ID: SKL.1-HIER.1
 * 対応設計書: docs/design/screens/specs/画面設計書_SCR-SKILLMAP_スキルマップ画面.md
 * 実装内容: スキルマップチャート表示機能
 */
'use client';

import React, { useState, useMemo } from 'react';

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

interface SkillMapChartProps {
  employees: Employee[];
  selectedSkills: string[];
  onSkillSelect: (skills: string[]) => void;
}

interface SkillSummary {
  skillName: string;
  category: string;
  totalEmployees: number;
  levelDistribution: { [level: number]: number };
  averageLevel: number;
  averageExperience: number;
}

export function SkillMapChart({ employees, selectedSkills, onSkillSelect }: SkillMapChartProps) {
  const [viewMode, setViewMode] = useState<'skills' | 'departments' | 'levels'>('skills');
  const [selectedCategory, setSelectedCategory] = useState<string>('');

  // スキル集計データの生成
  const skillSummaries = useMemo(() => {
    const skillMap = new Map<string, SkillSummary>();

    employees.forEach(employee => {
      employee.skills.forEach(skill => {
        if (!skillMap.has(skill.skillName)) {
          skillMap.set(skill.skillName, {
            skillName: skill.skillName,
            category: skill.category,
            totalEmployees: 0,
            levelDistribution: { 1: 0, 2: 0, 3: 0, 4: 0 },
            averageLevel: 0,
            averageExperience: 0
          });
        }

        const summary = skillMap.get(skill.skillName);
        if (summary) {
          summary.totalEmployees++;
          if (skill.level >= 1 && skill.level <= 4) {
            summary.levelDistribution[skill.level] = (summary.levelDistribution[skill.level] || 0) + 1;
          }
        }
      });
    });

    // 平均値の計算
    skillMap.forEach((summary, skillName) => {
      let totalLevel = 0;
      let totalExperience = 0;
      let count = 0;

      employees.forEach(employee => {
        employee.skills.forEach(skill => {
          if (skill.skillName === skillName) {
            totalLevel += skill.level;
            totalExperience += skill.experienceYears;
            count++;
          }
        });
      });

      summary.averageLevel = count > 0 ? totalLevel / count : 0;
      summary.averageExperience = count > 0 ? totalExperience / count : 0;
    });

    return Array.from(skillMap.values()).sort((a, b) => b.totalEmployees - a.totalEmployees);
  }, [employees]);

  // カテゴリ別集計
  const categoryData = useMemo(() => {
    const categoryMap = new Map<string, { count: number; employees: Set<string> }>();

    employees.forEach(employee => {
      employee.skills.forEach(skill => {
        if (!categoryMap.has(skill.category)) {
          categoryMap.set(skill.category, { count: 0, employees: new Set() });
        }
        const data = categoryMap.get(skill.category);
        if (data) {
          data.count++;
          data.employees.add(employee.id);
        }
      });
    });

    return Array.from(categoryMap.entries()).map(([category, data]) => ({
      category,
      skillCount: data.count,
      employeeCount: data.employees.size
    })).sort((a, b) => b.employeeCount - a.employeeCount);
  }, [employees]);

  // 部署別集計
  const departmentData = useMemo(() => {
    const deptMap = new Map<string, { employees: number; skills: Set<string> }>();

    employees.forEach(employee => {
      if (!deptMap.has(employee.department)) {
        deptMap.set(employee.department, { employees: 0, skills: new Set() });
      }
      const data = deptMap.get(employee.department);
      if (data) {
        data.employees++;
        employee.skills.forEach(skill => data.skills.add(skill.skillName));
      }
    });

    return Array.from(deptMap.entries()).map(([department, data]) => ({
      department,
      employeeCount: data.employees,
      uniqueSkillCount: data.skills.size
    })).sort((a, b) => b.employeeCount - a.employeeCount);
  }, [employees]);

  const getLevelText = (level: number) => {
    const levels = ['', '×', '△', '○', '◎'];
    return levels[level] || '';
  };

  const getLevelColor = (level: number) => {
    const colors = ['', 'bg-red-100 text-red-800', 'bg-yellow-100 text-yellow-800', 'bg-blue-100 text-blue-800', 'bg-green-100 text-green-800'];
    return colors[level] || '';
  };

  const filteredSkills = selectedCategory 
    ? skillSummaries.filter(skill => skill.category === selectedCategory)
    : skillSummaries;

  const categories = [...new Set(skillSummaries.map(skill => skill.category))];

  return (
    <div className="space-y-6">
      {/* ビューモード切り替え */}
      <div className="flex flex-wrap gap-2">
        <button
          onClick={() => setViewMode('skills')}
          className={`px-4 py-2 rounded-md text-sm font-medium ${
            viewMode === 'skills'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          スキル別表示
        </button>
        <button
          onClick={() => setViewMode('departments')}
          className={`px-4 py-2 rounded-md text-sm font-medium ${
            viewMode === 'departments'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          部署別表示
        </button>
        <button
          onClick={() => setViewMode('levels')}
          className={`px-4 py-2 rounded-md text-sm font-medium ${
            viewMode === 'levels'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          レベル分布
        </button>
      </div>

      {/* スキル別表示 */}
      {viewMode === 'skills' && (
        <div className="space-y-4">
          {/* カテゴリフィルター */}
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setSelectedCategory('')}
              className={`px-3 py-1 rounded-full text-sm ${
                selectedCategory === ''
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              すべて
            </button>
            {categories.map(category => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-3 py-1 rounded-full text-sm ${
                  selectedCategory === category
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {category}
              </button>
            ))}
          </div>

          {/* スキル一覧 */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredSkills.slice(0, 12).map(skill => (
              <div key={skill.skillName} className="bg-white p-4 rounded-lg shadow border">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h3 className="font-medium text-gray-900">{skill.skillName}</h3>
                    <p className="text-sm text-gray-500">{skill.category}</p>
                  </div>
                  <span className="text-lg font-bold text-blue-600">
                    {skill.totalEmployees}人
                  </span>
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>平均レベル:</span>
                    <span className="font-medium">{skill.averageLevel.toFixed(1)}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>平均経験年数:</span>
                    <span className="font-medium">{skill.averageExperience.toFixed(1)}年</span>
                  </div>

                  {/* レベル分布 */}
                  <div className="mt-3">
                    <p className="text-xs text-gray-500 mb-2">レベル分布</p>
                    <div className="flex space-x-1">
                      {[1, 2, 3, 4].map(level => (
                        <div key={level} className="flex-1">
                          <div className={`text-center py-1 rounded text-xs ${getLevelColor(level)}`}>
                            <div className="font-bold">{getLevelText(level)}</div>
                            <div>{skill.levelDistribution[level] || 0}人</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {filteredSkills.length > 12 && (
            <div className="text-center">
              <p className="text-sm text-gray-500">
                他 {filteredSkills.length - 12} 件のスキルがあります
              </p>
            </div>
          )}
        </div>
      )}

      {/* 部署別表示 */}
      {viewMode === 'departments' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {departmentData.map(dept => (
            <div key={dept.department} className="bg-white p-6 rounded-lg shadow border">
              <h3 className="text-lg font-medium text-gray-900 mb-4">{dept.department}</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">従業員数:</span>
                  <span className="font-bold text-blue-600">{dept.employeeCount}人</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">保有スキル数:</span>
                  <span className="font-bold text-green-600">{dept.uniqueSkillCount}種類</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">1人あたり平均:</span>
                  <span className="font-medium">{(dept.uniqueSkillCount / dept.employeeCount).toFixed(1)}種類</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* レベル分布表示 */}
      {viewMode === 'levels' && (
        <div className="space-y-6">
          {/* カテゴリ別レベル分布 */}
          {categoryData.map(category => (
            <div key={category.category} className="bg-white p-6 rounded-lg shadow border">
              <h3 className="text-lg font-medium text-gray-900 mb-4">{category.category}</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[1, 2, 3, 4].map(level => {
                  const levelCount = skillSummaries
                    .filter(skill => skill.category === category.category)
                    .reduce((sum, skill) => sum + (skill.levelDistribution[level] || 0), 0);
                  
                  return (
                    <div key={level} className={`text-center p-4 rounded-lg ${getLevelColor(level)}`}>
                      <div className="text-2xl font-bold mb-1">{getLevelText(level)}</div>
                      <div className="text-sm">レベル {level}</div>
                      <div className="text-lg font-bold mt-2">{levelCount}人</div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* データが空の場合 */}
      {employees.length === 0 && (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
            />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">データがありません</h3>
          <p className="mt-1 text-sm text-gray-500">
            検索条件を変更してください
          </p>
        </div>
      )}
    </div>
  );
}
