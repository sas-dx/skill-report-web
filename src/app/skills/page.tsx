// SKL.1-HIER.1: スキル管理画面
'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { 
  mockSkillCategories, 
  mockCertifications,
  skillLevelLabels,
  skillLevelDescriptions,
  type SkillCategory, 
  type SkillItem,
  type CertificationData 
} from '@/lib/mockData';

const SkillsPage: React.FC = () => {
  const [skillCategories, setSkillCategories] = useState<SkillCategory[]>(mockSkillCategories);
  const [certifications, setCertifications] = useState<CertificationData[]>(mockCertifications);
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set());
  const [expandedSkills, setExpandedSkills] = useState<Set<string>>(new Set());
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [isEditing, setIsEditing] = useState(false);

  const toggleCategory = (categoryId: string) => {
    const newExpanded = new Set(expandedCategories);
    if (newExpanded.has(categoryId)) {
      newExpanded.delete(categoryId);
    } else {
      newExpanded.add(categoryId);
    }
    setExpandedCategories(newExpanded);
  };

  const toggleSkill = (skillId: string) => {
    const newExpanded = new Set(expandedSkills);
    if (newExpanded.has(skillId)) {
      newExpanded.delete(skillId);
    } else {
      newExpanded.add(skillId);
    }
    setExpandedSkills(newExpanded);
  };

  const updateSkillLevel = (skillId: string, level: number) => {
    const updateSkillInCategory = (skills: SkillItem[]): SkillItem[] => {
      return skills.map(skill => {
        if (skill.id === skillId) {
          return { ...skill, level };
        }
        if (skill.children) {
          return { ...skill, children: updateSkillInCategory(skill.children) };
        }
        return skill;
      });
    };

    setSkillCategories(categories =>
      categories.map(category => ({
        ...category,
        skills: updateSkillInCategory(category.skills)
      }))
    );
  };

  const getSkillLevelColor = (level: number) => {
    switch (level) {
      case 0: return 'bg-gray-100 text-gray-600';
      case 1: return 'bg-red-100 text-red-800';
      case 2: return 'bg-yellow-100 text-yellow-800';
      case 3: return 'bg-blue-100 text-blue-800';
      case 4: return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-600';
    }
  };

  const renderSkillItem = (skill: SkillItem, depth: number = 0) => {
    const hasChildren = skill.children && skill.children.length > 0;
    const isExpanded = expandedSkills.has(skill.id);
    const paddingLeft = `${depth * 1.5 + 1}rem`;

    return (
      <div key={skill.id} className="border-b border-gray-100 last:border-b-0">
        <div 
          className="flex items-center justify-between py-3 hover:bg-gray-50"
          style={{ paddingLeft }}
        >
          <div className="flex items-center flex-1">
            {hasChildren && (
              <button
                onClick={() => toggleSkill(skill.id)}
                className="mr-2 p-1 hover:bg-gray-200 rounded"
              >
                <svg 
                  className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-90' : ''}`}
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            )}
            <div className="flex-1">
              <div className="flex items-center">
                <span className="font-medium text-gray-900">{skill.name}</span>
                {skill.subcategory && (
                  <span className="ml-2 text-xs text-gray-500">
                    ({skill.subcategory})
                  </span>
                )}
              </div>
              {skill.acquired_date && (
                <div className="text-xs text-gray-500 mt-1">
                  習得日: {new Date(skill.acquired_date).toLocaleDateString('ja-JP')}
                </div>
              )}
              {skill.remarks && (
                <div className="text-xs text-gray-600 mt-1">
                  {skill.remarks}
                </div>
              )}
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            {skill.level === 0 ? (
              <span className={`px-3 py-1 text-sm font-medium rounded-full ${getSkillLevelColor(skill.level)}`}>
                未評価
              </span>
            ) : (
              <span className={`px-3 py-2 text-lg font-bold rounded-full ${getSkillLevelColor(skill.level)}`}>
                {skillLevelLabels[skill.level as keyof typeof skillLevelLabels]}
              </span>
            )}
            {isEditing && (
              <select
                value={skill.level}
                onChange={(e) => updateSkillLevel(skill.id, parseInt(e.target.value))}
                className="text-xs border border-gray-300 rounded px-2 py-1"
              >
                {Object.entries(skillLevelLabels).map(([value, label]) => (
                  <option key={value} value={value}>
                    {label} - {skillLevelDescriptions[parseInt(value) as keyof typeof skillLevelDescriptions]}
                  </option>
                ))}
              </select>
            )}
          </div>
        </div>
        
        {hasChildren && isExpanded && (
          <div>
            {skill.children!.map(childSkill => renderSkillItem(childSkill, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  const filteredCategories = skillCategories.filter(category => {
    if (selectedCategory !== 'all' && category.id !== selectedCategory) {
      return false;
    }
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      return category.name.toLowerCase().includes(searchLower) ||
             category.skills.some(skill => 
               skill.name.toLowerCase().includes(searchLower) ||
               (skill.children && skill.children.some(child => 
                 child.name.toLowerCase().includes(searchLower)
               ))
             );
    }
    return true;
  });

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ヘッダー */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">スキル管理</h1>
                <p className="mt-1 text-sm text-gray-600">
                  技術・開発・業務・管理・生産スキルの管理を行います
                </p>
              </div>
              <Button
                onClick={() => setIsEditing(!isEditing)}
                variant={isEditing ? "outline" : "primary"}
              >
                {isEditing ? 'キャンセル' : '編集モード'}
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* メインコンテンツ */}
          <div className="lg:col-span-3 space-y-6">
            {/* 検索・フィルター */}
            <div className="bg-white shadow rounded-lg p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    スキル検索
                  </label>
                  <Input
                    type="text"
                    placeholder="スキル名で検索..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    カテゴリフィルター
                  </label>
                  <select
                    value={selectedCategory}
                    onChange={(e) => setSelectedCategory(e.target.value)}
                    className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                  >
                    <option value="all">すべてのカテゴリ</option>
                    {skillCategories.map(category => (
                      <option key={category.id} value={category.id}>
                        {category.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            {/* スキル一覧 */}
            <div className="space-y-4">
              {filteredCategories.map(category => (
                <div key={category.id} className="bg-white shadow rounded-lg">
                  <div 
                    className="px-6 py-4 border-b border-gray-200 cursor-pointer hover:bg-gray-50"
                    onClick={() => toggleCategory(category.id)}
                  >
                    <div className="flex items-center justify-between">
                      <h2 className="text-lg font-medium text-gray-900 flex items-center">
                        <svg 
                          className={`w-5 h-5 mr-2 transition-transform ${
                            expandedCategories.has(category.id) ? 'rotate-90' : ''
                          }`}
                          fill="none" 
                          stroke="currentColor" 
                          viewBox="0 0 24 24"
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                        {category.name}
                      </h2>
                      <span className="text-sm text-gray-500">
                        {category.skills.length} 項目
                      </span>
                    </div>
                  </div>
                  
                  {expandedCategories.has(category.id) && (
                    <div className="px-6 py-4">
                      {category.skills.map(skill => renderSkillItem(skill))}
                    </div>
                  )}
                </div>
              ))}
            </div>

            {isEditing && (
              <div className="bg-white shadow rounded-lg p-6">
                <div className="flex justify-end space-x-3">
                  <Button
                    variant="outline"
                    onClick={() => setIsEditing(false)}
                  >
                    キャンセル
                  </Button>
                  <Button
                    onClick={() => {
                      setIsEditing(false);
                      alert('スキル情報を保存しました');
                    }}
                  >
                    保存
                  </Button>
                </div>
              </div>
            )}
          </div>

          {/* サイドバー */}
          <div className="space-y-6">
            {/* スキルレベル説明 */}
            <div className="bg-white shadow rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-medium text-gray-900">評価基準</h2>
              </div>
              <div className="px-6 py-4">
                <div className="space-y-3">
                  {Object.entries(skillLevelLabels).map(([level, label]) => (
                    <div key={level} className="flex items-center">
                      {parseInt(level) === 0 ? (
                        <span className={`px-2 py-1 text-xs font-medium rounded mr-3 ${getSkillLevelColor(parseInt(level))}`}>
                          {label}
                        </span>
                      ) : (
                        <span className={`w-5 h-5 text-xs font-medium rounded-full mr-2 flex items-center justify-center ${getSkillLevelColor(parseInt(level))}`}>
                          {label}
                        </span>
                      )}
                      <span className="text-xs text-gray-600">
                        {skillLevelDescriptions[parseInt(level) as keyof typeof skillLevelDescriptions]}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* 資格情報 */}
            <div className="bg-white shadow rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-medium text-gray-900">保有資格</h2>
              </div>
              <div className="px-6 py-4">
                <div className="space-y-4">
                  {certifications.map(cert => (
                    <div key={cert.id} className="border-l-4 border-green-400 pl-4">
                      <h3 className="text-sm font-medium text-gray-900">
                        {cert.cert_name}
                      </h3>
                      <p className="text-xs text-gray-500 mt-1">
                        取得日: {new Date(cert.acquired_date).toLocaleDateString('ja-JP')}
                      </p>
                      {cert.expire_date && (
                        <p className="text-xs text-gray-500">
                          有効期限: {new Date(cert.expire_date).toLocaleDateString('ja-JP')}
                        </p>
                      )}
                      {cert.score && (
                        <p className="text-xs text-gray-600">
                          スコア: {cert.score}
                        </p>
                      )}
                      <p className="text-xs text-gray-500">
                        発行者: {cert.issuer}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* スキル統計 */}
            <div className="bg-white shadow rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-medium text-gray-900">スキル統計</h2>
              </div>
              <div className="px-6 py-4">
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">総スキル数</span>
                    <span className="text-sm font-medium text-gray-900">
                      {skillCategories.reduce((total, category) => 
                        total + category.skills.reduce((catTotal, skill) => 
                          catTotal + 1 + (skill.children?.length || 0), 0
                        ), 0
                      )}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">評価済みスキル</span>
                    <span className="text-sm font-medium text-gray-900">
                      {skillCategories.reduce((total, category) => 
                        total + category.skills.reduce((catTotal, skill) => {
                          let count = skill.level > 0 ? 1 : 0;
                          if (skill.children) {
                            count += skill.children.filter(child => child.level > 0).length;
                          }
                          return catTotal + count;
                        }, 0
                      ), 0
                      )}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">保有資格数</span>
                    <span className="text-sm font-medium text-gray-900">
                      {certifications.length}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SkillsPage;
