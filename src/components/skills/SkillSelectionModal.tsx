/**
 * 要求仕様ID: SKL.1-HIER.1, SKL.1-MAINT.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_SKL_Skill_スキル管理画面.md
 * 実装内容: スキル選択モーダル（新規スキル追加時）
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { SkillHierarchy, SkillMaster } from '@/types/skills';
import { X, Search, Plus } from 'lucide-react';

interface SkillSelectionModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectSkill: (skill: SkillHierarchy) => void;
  onCreateCustomSkill: (skillName: string, category: string) => void;
  skillHierarchy: SkillHierarchy[];
  skills: SkillMaster[];
}

export const SkillSelectionModal: React.FC<SkillSelectionModalProps> = ({
  isOpen,
  onClose,
  onSelectSkill,
  onCreateCustomSkill,
  skillHierarchy,
  skills
}) => {
  const [searchKeyword, setSearchKeyword] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [customSkillName, setCustomSkillName] = useState('');
  const [customSkillCategory, setCustomSkillCategory] = useState('technical');
  const [activeTab, setActiveTab] = useState<'existing' | 'custom'>('existing');

  // フィルタリングされたスキル
  const filteredSkills = skills.filter(skill => {
    const matchesKeyword = !searchKeyword || 
      skill.name.toLowerCase().includes(searchKeyword.toLowerCase()) ||
      skill.description?.toLowerCase().includes(searchKeyword.toLowerCase());
    
    const matchesCategory = !selectedCategory || skill.category === selectedCategory;
    
    return matchesKeyword && matchesCategory;
  });

  // カテゴリ一覧
  const categories = Array.from(new Set(skillHierarchy.map(h => h.id)));

  // モーダルを閉じる
  const handleClose = () => {
    setSearchKeyword('');
    setSelectedCategory('');
    setCustomSkillName('');
    setCustomSkillCategory('technical');
    setActiveTab('existing');
    onClose();
  };

  // 既存スキル選択
  const handleSelectExistingSkill = (skill: SkillMaster) => {
    // SkillMasterからSkillHierarchyに変換
    const hierarchySkill: SkillHierarchy = {
      id: skill.id,
      name: skill.name,
      category: skill.category,
      subcategory: skill.subcategory,
      level: 3, // スキル項目レベル
      children: [],
      ...(skill.description && { description: skill.description })
    };
    onSelectSkill(hierarchySkill);
    handleClose();
  };

  // カスタムスキル作成
  const handleCreateCustomSkill = () => {
    if (!customSkillName.trim()) {
      return;
    }
    onCreateCustomSkill(customSkillName.trim(), customSkillCategory);
    handleClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[80vh] overflow-hidden">
        {/* ヘッダー */}
        <div className="flex items-center justify-between p-6 border-b">
          <h2 className="text-xl font-semibold text-gray-900">スキル選択</h2>
          <button
            onClick={handleClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X size={24} />
          </button>
        </div>

        {/* タブ */}
        <div className="flex border-b">
          <button
            onClick={() => setActiveTab('existing')}
            className={`px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'existing'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            既存スキルから選択
          </button>
          <button
            onClick={() => setActiveTab('custom')}
            className={`px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'custom'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            カスタムスキル作成
          </button>
        </div>

        <div className="p-6 overflow-y-auto max-h-[60vh]">
          {activeTab === 'existing' ? (
            <div className="space-y-4">
              {/* 検索・フィルタ */}
              <div className="flex space-x-4">
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                    <Input
                      type="text"
                      placeholder="スキル名で検索..."
                      value={searchKeyword}
                      onChange={(e) => setSearchKeyword(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>
                <div className="w-48">
                  <select
                    value={selectedCategory}
                    onChange={(e) => setSelectedCategory(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">全カテゴリ</option>
                    {categories.map(category => (
                      <option key={category} value={category}>
                        {skillHierarchy.find(h => h.id === category)?.name || category}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* スキル一覧 */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-96 overflow-y-auto">
                {filteredSkills.map(skill => (
                  <div
                    key={skill.id}
                    onClick={() => handleSelectExistingSkill(skill)}
                    className="p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 cursor-pointer transition-colors"
                  >
                    <h4 className="font-medium text-gray-900">{skill.name}</h4>
                    <p className="text-sm text-gray-600 mt-1">
                      {skill.category}
                      {skill.subcategory && ` > ${skill.subcategory}`}
                    </p>
                    {skill.description && (
                      <p className="text-xs text-gray-500 mt-2 line-clamp-2">
                        {skill.description}
                      </p>
                    )}
                  </div>
                ))}
              </div>

              {filteredSkills.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  <p>該当するスキルが見つかりません</p>
                  <p className="text-sm mt-1">検索条件を変更するか、カスタムスキルを作成してください</p>
                </div>
              )}
            </div>
          ) : (
            <div className="space-y-6">
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-start">
                  <Plus className="text-blue-600 mt-0.5 mr-2" size={20} />
                  <div>
                    <h3 className="text-sm font-medium text-blue-900">カスタムスキル作成</h3>
                    <p className="text-sm text-blue-700 mt-1">
                      既存のスキルマスタにないスキルを新規作成できます
                    </p>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <label htmlFor="customSkillName" className="block text-sm font-medium text-gray-700 mb-2">
                    スキル名 <span className="text-red-500">*</span>
                  </label>
                  <Input
                    id="customSkillName"
                    type="text"
                    value={customSkillName}
                    onChange={(e) => setCustomSkillName(e.target.value)}
                    placeholder="例: 新しいプログラミング言語、特殊なツールなど"
                    className="w-full"
                  />
                </div>

                <div>
                  <label htmlFor="customSkillCategory" className="block text-sm font-medium text-gray-700 mb-2">
                    カテゴリ <span className="text-red-500">*</span>
                  </label>
                  <select
                    id="customSkillCategory"
                    value={customSkillCategory}
                    onChange={(e) => setCustomSkillCategory(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="technical">技術スキル</option>
                    <option value="business">ビジネススキル</option>
                    <option value="management">マネジメントスキル</option>
                    <option value="communication">コミュニケーションスキル</option>
                    <option value="other">その他</option>
                  </select>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* フッター */}
        <div className="flex justify-end space-x-3 p-6 border-t bg-gray-50">
          <Button
            variant="secondary"
            onClick={handleClose}
          >
            キャンセル
          </Button>
          {activeTab === 'custom' && (
            <Button
              onClick={handleCreateCustomSkill}
              disabled={!customSkillName.trim()}
            >
              カスタムスキル作成
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};
