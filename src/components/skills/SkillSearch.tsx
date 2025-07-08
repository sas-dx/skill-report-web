/**
 * 要求仕様ID: SKL.1-SEARCH.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_SKL_Skill_スキル管理画面.md
 * 実装内容: スキル検索・フィルタリング機能
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { SkillSearchFilters, SkillCategoryWithId } from '@/types/skills';

interface SkillSearchProps {
  categories: SkillCategoryWithId[];
  onSearch: (filters: SkillSearchFilters) => void;
  onReset: () => void;
  isLoading?: boolean;
}

export const SkillSearch: React.FC<SkillSearchProps> = ({
  categories,
  onSearch,
  onReset,
  isLoading = false
}) => {
  const [filters, setFilters] = useState<SkillSearchFilters>({
    keyword: '',
    categoryId: '',
    subcategoryId: ''
  });

  const [subcategories, setSubcategories] = useState<SkillCategoryWithId[]>([]);

  // カテゴリ変更時にサブカテゴリを更新
  useEffect(() => {
    if (filters.categoryId) {
      const selectedCategory = categories.find(cat => cat.id === filters.categoryId);
      setSubcategories(selectedCategory?.subcategories || []);
      
      // サブカテゴリをリセット
      setFilters(prev => ({
        ...prev,
        subcategoryId: ''
      }));
    } else {
      setSubcategories([]);
    }
  }, [filters.categoryId, categories]);

  // フィルタ更新
  const updateFilter = (key: keyof SkillSearchFilters, value: any) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  // 検索実行
  const handleSearch = () => {
    onSearch(filters);
  };

  // リセット
  const handleReset = () => {
    const resetFilters: SkillSearchFilters = {
      keyword: '',
      categoryId: '',
      subcategoryId: ''
    };
    setFilters(resetFilters);
    setSubcategories([]);
    onReset();
  };

  // Enterキーでの検索
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-medium text-gray-900">スキル検索</h3>
        <Button
          variant="secondary"
          size="sm"
          onClick={handleReset}
          disabled={isLoading}
        >
          リセット
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {/* キーワード検索 */}
        <div className="lg:col-span-3">
          <label htmlFor="keyword" className="block text-xs font-medium text-gray-700 mb-1">
            キーワード
          </label>
          <Input
            id="keyword"
            type="text"
            placeholder="スキル名、説明で検索..."
            value={filters.keyword}
            onChange={(e) => updateFilter('keyword', e.target.value)}
            onKeyPress={handleKeyPress}
            className="w-full"
          />
        </div>

        {/* カテゴリ */}
        <div>
          <label htmlFor="category" className="block text-xs font-medium text-gray-700 mb-1">
            カテゴリ
          </label>
          <select
            id="category"
            value={filters.categoryId}
            onChange={(e) => updateFilter('categoryId', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
          >
            <option value="">すべて</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
        </div>

        {/* サブカテゴリ */}
        <div>
          <label htmlFor="subcategory" className="block text-xs font-medium text-gray-700 mb-1">
            サブカテゴリ
          </label>
          <select
            id="subcategory"
            value={filters.subcategoryId}
            onChange={(e) => updateFilter('subcategoryId', e.target.value)}
            disabled={!filters.categoryId || subcategories.length === 0}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm disabled:bg-gray-100"
          >
            <option value="">すべて</option>
            {subcategories.map((subcategory) => (
              <option key={subcategory.id} value={subcategory.id}>
                {subcategory.name}
              </option>
            ))}
          </select>
        </div>

        {/* スキルレベル範囲 */}
        <div>
          <label className="block text-xs font-medium text-gray-700 mb-1">
            スキルレベル
          </label>
          <div className="flex items-center space-x-2">
            <select
              value={filters.minLevel || ''}
              onChange={(e) => updateFilter('minLevel', e.target.value ? parseInt(e.target.value) : undefined)}
              className="flex-1 px-2 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
            >
              <option value="">最小</option>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
            </select>
            <span className="text-gray-500 text-sm">〜</span>
            <select
              value={filters.maxLevel || ''}
              onChange={(e) => updateFilter('maxLevel', e.target.value ? parseInt(e.target.value) : undefined)}
              className="flex-1 px-2 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
            >
              <option value="">最大</option>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
            </select>
          </div>
        </div>

        {/* 経験有無 */}
        <div>
          <label htmlFor="hasExperience" className="block text-xs font-medium text-gray-700 mb-1">
            経験有無
          </label>
          <select
            id="hasExperience"
            value={filters.hasExperience === undefined ? '' : filters.hasExperience.toString()}
            onChange={(e) => updateFilter('hasExperience', e.target.value === '' ? undefined : e.target.value === 'true')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
          >
            <option value="">すべて</option>
            <option value="true">経験あり</option>
            <option value="false">経験なし</option>
          </select>
        </div>

        {/* アクティブ状態 */}
        <div>
          <label htmlFor="isActive" className="block text-xs font-medium text-gray-700 mb-1">
            使用状況
          </label>
          <select
            id="isActive"
            value={filters.isActive === undefined ? '' : filters.isActive.toString()}
            onChange={(e) => updateFilter('isActive', e.target.value === '' ? undefined : e.target.value === 'true')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
          >
            <option value="">すべて</option>
            <option value="true">現在使用中</option>
            <option value="false">使用していない</option>
          </select>
        </div>
      </div>

      {/* 検索ボタン */}
      <div className="flex justify-end mt-4">
        <Button
          onClick={handleSearch}
          disabled={isLoading}
          className="px-6"
        >
          {isLoading ? '検索中...' : '検索'}
        </Button>
      </div>

      {/* 検索条件の表示 */}
      {(filters.keyword || filters.categoryId || filters.subcategoryId || 
        filters.minLevel !== undefined || filters.maxLevel !== undefined ||
        filters.hasExperience !== undefined || filters.isActive !== undefined) && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <p className="text-xs text-gray-600 mb-2">現在の検索条件:</p>
          <div className="flex flex-wrap gap-2">
            {filters.keyword && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-blue-100 text-blue-800">
                キーワード: {filters.keyword}
              </span>
            )}
            {filters.categoryId && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800">
                カテゴリ: {categories.find(c => c.id === filters.categoryId)?.name}
              </span>
            )}
            {filters.subcategoryId && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800">
                サブカテゴリ: {subcategories.find(c => c.id === filters.subcategoryId)?.name}
              </span>
            )}
            {(filters.minLevel !== undefined || filters.maxLevel !== undefined) && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-purple-100 text-purple-800">
                レベル: {filters.minLevel || '1'}〜{filters.maxLevel || '4'}
              </span>
            )}
            {filters.hasExperience !== undefined && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-orange-100 text-orange-800">
                {filters.hasExperience ? '経験あり' : '経験なし'}
              </span>
            )}
            {filters.isActive !== undefined && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-gray-100 text-gray-800">
                {filters.isActive ? '使用中' : '未使用'}
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
