/**
 * 要求仕様ID: SKL.1-HIER.1
 * 対応設計書: docs/design/screens/specs/画面設計書_SCR-SKILLMAP_スキルマップ画面.md
 * 実装内容: スキルマップテーブル表示機能
 */
'use client';

import React, { useState } from 'react';

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

interface SkillMapTableProps {
  employees: Employee[];
  onEmployeeSelect: (employeeId: string) => void;
}

export function SkillMapTable({ employees, onEmployeeSelect }: SkillMapTableProps) {
  const [sortField, setSortField] = useState<'name' | 'department' | 'position'>('name');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc');
  const [expandedRows, setExpandedRows] = useState<Set<string>>(new Set());

  const getLevelText = (level: number) => {
    const levels = ['', '×', '△', '○', '◎'];
    return levels[level] || '';
  };

  const getLevelColor = (level: number) => {
    const colors = ['', 'text-red-500', 'text-yellow-500', 'text-blue-500', 'text-green-500'];
    return colors[level] || '';
  };

  const handleSort = (field: 'name' | 'department' | 'position') => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  const toggleRowExpansion = (employeeId: string) => {
    const newExpanded = new Set(expandedRows);
    if (newExpanded.has(employeeId)) {
      newExpanded.delete(employeeId);
    } else {
      newExpanded.add(employeeId);
    }
    setExpandedRows(newExpanded);
  };

  const sortedEmployees = [...employees].sort((a, b) => {
    let aValue = '';
    let bValue = '';

    switch (sortField) {
      case 'name':
        aValue = a.name;
        bValue = b.name;
        break;
      case 'department':
        aValue = a.department;
        bValue = b.department;
        break;
      case 'position':
        aValue = a.position;
        bValue = b.position;
        break;
    }

    if (sortDirection === 'asc') {
      return aValue.localeCompare(bValue);
    } else {
      return bValue.localeCompare(aValue);
    }
  });

  const SortIcon = ({ field }: { field: 'name' | 'department' | 'position' }) => {
    if (sortField !== field) {
      return (
        <svg className="ml-1 h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
        </svg>
      );
    }

    return sortDirection === 'asc' ? (
      <svg className="ml-1 h-4 w-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
      </svg>
    ) : (
      <svg className="ml-1 h-4 w-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
      </svg>
    );
  };

  return (
    <div className="bg-white shadow rounded-lg overflow-hidden">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                <button
                  onClick={() => handleSort('name')}
                  className="flex items-center hover:text-gray-700"
                >
                  従業員名
                  <SortIcon field="name" />
                </button>
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                <button
                  onClick={() => handleSort('department')}
                  className="flex items-center hover:text-gray-700"
                >
                  部署
                  <SortIcon field="department" />
                </button>
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                <button
                  onClick={() => handleSort('position')}
                  className="flex items-center hover:text-gray-700"
                >
                  役職
                  <SortIcon field="position" />
                </button>
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                スキル数
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                主要スキル
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                操作
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {sortedEmployees.map((employee) => (
              <React.Fragment key={employee.id}>
                {/* メイン行 */}
                <tr className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div>
                        <div className="text-sm font-medium text-gray-900">{employee.name}</div>
                        <div className="text-sm text-gray-500">{employee.empNo}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {employee.department}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {employee.position}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {employee.skills.length}件
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex flex-wrap gap-1">
                      {employee.skills.slice(0, 3).map((skill) => (
                        <span
                          key={skill.id}
                          className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                        >
                          {skill.skillName}
                          <span className={`ml-1 font-bold ${getLevelColor(skill.level)}`}>
                            {getLevelText(skill.level)}
                          </span>
                        </span>
                      ))}
                      {employee.skills.length > 3 && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                          +{employee.skills.length - 3}
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button
                      onClick={() => toggleRowExpansion(employee.id)}
                      className="text-blue-600 hover:text-blue-900 mr-3"
                    >
                      {expandedRows.has(employee.id) ? '詳細を閉じる' : '詳細を表示'}
                    </button>
                    <button
                      onClick={() => onEmployeeSelect(employee.id)}
                      className="text-green-600 hover:text-green-900"
                    >
                      選択
                    </button>
                  </td>
                </tr>

                {/* 展開行（スキル詳細） */}
                {expandedRows.has(employee.id) && (
                  <tr>
                    <td colSpan={6} className="px-6 py-4 bg-gray-50">
                      <div className="space-y-3">
                        <h4 className="text-sm font-medium text-gray-900">保有スキル詳細</h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                          {employee.skills.map((skill) => (
                            <div
                              key={skill.id}
                              className="bg-white p-3 rounded-lg border border-gray-200"
                            >
                              <div className="flex items-center justify-between mb-2">
                                <h5 className="text-sm font-medium text-gray-900">
                                  {skill.skillName}
                                </h5>
                                <span className={`text-lg font-bold ${getLevelColor(skill.level)}`}>
                                  {getLevelText(skill.level)}
                                </span>
                              </div>
                              <div className="text-xs text-gray-500 space-y-1">
                                <div>カテゴリ: {skill.category}</div>
                                <div>サブカテゴリ: {skill.subcategory}</div>
                                <div>経験年数: {skill.experienceYears}年</div>
                                <div>最終使用: {skill.lastUsed}</div>
                                {skill.certification && (
                                  <div>資格: {skill.certification}</div>
                                )}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>

      {employees.length === 0 && (
        <div className="text-center py-12">
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
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
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
