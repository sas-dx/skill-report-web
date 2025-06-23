/**
 * 要求仕様ID: SKL.1-HIER.1
 * 対応設計書: docs/design/screens/specs/画面設計書_SCR-SKILLMAP_スキルマップ画面.md
 * 実装内容: スキルマップフィルター機能
 */
'use client';

import React from 'react';
import { Input } from '@/components/ui/Input';

interface SkillMapFiltersProps {
  filters: {
    department: string;
    position: string;
    skillCategory: string;
    skillLevel: number;
    searchTerm: string;
  };
  skillCategories: string[];
  departments: string[];
  positions: string[];
  onFilterChange: (filters: Partial<SkillMapFiltersProps['filters']>) => void;
}

export function SkillMapFilters({
  filters,
  skillCategories,
  departments,
  positions,
  onFilterChange
}: SkillMapFiltersProps) {
  return (
    <div className="mb-6 bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-medium text-gray-900 mb-4">検索・フィルター</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
        {/* キーワード検索 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            キーワード検索
          </label>
          <Input
            value={filters.searchTerm}
            onChange={(e) => onFilterChange({ searchTerm: e.target.value })}
            placeholder="名前、スキル名で検索"
            className="w-full"
          />
        </div>

        {/* 部署フィルター */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            部署
          </label>
          <select
            value={filters.department}
            onChange={(e) => onFilterChange({ department: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">すべての部署</option>
            {departments.map(department => (
              <option key={department} value={department}>
                {department}
              </option>
            ))}
          </select>
        </div>

        {/* 役職フィルター */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            役職
          </label>
          <select
            value={filters.position}
            onChange={(e) => onFilterChange({ position: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">すべての役職</option>
            {positions.map(position => (
              <option key={position} value={position}>
                {position}
              </option>
            ))}
          </select>
        </div>

        {/* スキルカテゴリフィルター */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            スキルカテゴリ
          </label>
          <select
            value={filters.skillCategory}
            onChange={(e) => onFilterChange({ skillCategory: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">すべてのカテゴリ</option>
            {skillCategories.map(category => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>
        </div>

        {/* スキルレベルフィルター */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            最低スキルレベル
          </label>
          <select
            value={filters.skillLevel}
            onChange={(e) => onFilterChange({ skillLevel: parseInt(e.target.value) })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          >
            <option value={0}>すべてのレベル</option>
            <option value={1}>× 未経験以上</option>
            <option value={2}>△ 基礎レベル以上</option>
            <option value={3}>○ 実務レベル以上</option>
            <option value={4}>◎ エキスパート</option>
          </select>
        </div>
      </div>

      {/* フィルタークリア */}
      <div className="mt-4 flex justify-end">
        <button
          onClick={() => onFilterChange({
            department: '',
            position: '',
            skillCategory: '',
            skillLevel: 0,
            searchTerm: ''
          })}
          className="text-sm text-gray-500 hover:text-gray-700"
        >
          フィルターをクリア
        </button>
      </div>
    </div>
  );
}
