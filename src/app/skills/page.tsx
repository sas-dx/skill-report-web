/**
 * 要求仕様ID: SKL.1-HIER.1, SKL.1-EVAL.1, SKL.1-SEARCH.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_SKL_Skill_スキル管理画面.md
 * 実装内容: スキル管理メイン画面（設計書準拠）
 */

'use client';

import React, { useState, useEffect } from 'react';
import { SkillHierarchyTree } from '@/components/skills/SkillHierarchyTree';
import { SkillDetailForm } from '@/components/skills/SkillDetailForm';
import { SkillSearch } from '@/components/skills/SkillSearch';
import { Button } from '@/components/ui/Button';
import { Spinner } from '@/components/ui/Spinner';
import { useSkills } from '@/hooks/useSkills';
import { 
  SkillHierarchy, 
  UserSkill, 
  SkillFormData, 
  SkillSearchFilters,
  SkillCategoryWithId,
  SKILL_CATEGORIES,
  Certification,
  CertificationFormData
} from '@/types/skills';

export default function SkillsPage() {
  const {
    skills,
    userSkills,
    skillHierarchy,
    selectedSkill,
    formData,
    isLoading,
    error,
    loadSkills,
    loadUserSkills,
    loadSkillHierarchy,
    selectSkill,
    updateFormData,
    saveSkill,
    deleteSkill,
    searchSkills
  } = useSkills();

  // 設計書準拠：スキルカテゴリタブと資格情報タブ
  const [activeTab, setActiveTab] = useState<'skills' | 'certifications'>('skills');
  const [activeCategory, setActiveCategory] = useState<string>('技術スキル');
  const [viewMode, setViewMode] = useState<'hierarchy' | 'search'>('hierarchy');
  const [showForm, setShowForm] = useState(false);
  const [searchResults, setSearchResults] = useState<UserSkill[]>([]);
  const [certifications, setCertifications] = useState<Certification[]>([]);
  const [showCertForm, setShowCertForm] = useState(false);

  // 初期データ読み込み
  useEffect(() => {
    loadSkills();
    loadUserSkills();
    loadSkillHierarchy();
  }, [loadSkills, loadUserSkills, loadSkillHierarchy]);

  // スキル選択時の処理
  const handleSkillSelect = (skill: SkillHierarchy) => {
    selectSkill(skill);
    setShowForm(true);
  };

  // フォーム保存処理
  const handleFormSave = async (data: SkillFormData) => {
    try {
      await saveSkill(data);
      setShowForm(false);
      // ユーザースキル一覧を再読み込み
      loadUserSkills();
    } catch (error) {
      console.error('スキル保存エラー:', error);
    }
  };

  // フォームキャンセル処理
  const handleFormCancel = () => {
    setShowForm(false);
    selectSkill(null);
  };

  // スキル削除処理
  const handleSkillDelete = async (skillId: string) => {
    if (confirm('このスキル情報を削除しますか？')) {
      try {
        await deleteSkill(skillId);
        setShowForm(false);
        loadUserSkills();
      } catch (error) {
        console.error('スキル削除エラー:', error);
      }
    }
  };

  // 検索処理
  const handleSearch = async (filters: SkillSearchFilters) => {
    try {
      const results = await searchSkills(filters);
      // SkillMasterをUserSkillに変換
      const userSkillResults: UserSkill[] = results.map(skill => ({
        id: skill.id,
        skillId: skill.id,
        userId: 'current-user', // 実際のユーザーIDに置き換え
        skillName: skill.name,
        category: skill.category,
        subcategory: skill.subcategory || undefined,
        level: 1 as const,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      }));
      setSearchResults(userSkillResults);
    } catch (error) {
      console.error('検索エラー:', error);
    }
  };

  // 検索リセット処理
  const handleSearchReset = () => {
    setSearchResults([]);
  };

  // 新規スキル追加
  const handleAddNewSkill = () => {
    selectSkill(null);
    setShowForm(true);
  };

  // カテゴリデータをSkillCategoryWithId形式に変換
  const categories: SkillCategoryWithId[] = [
    { id: 'tech', name: '技術スキル' },
    { id: 'dev', name: '開発スキル' },
    { id: 'business', name: '業務スキル' },
    { id: 'management', name: '管理スキル' },
    { id: 'production', name: '生産スキル' }
  ];

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 text-lg font-medium mb-2">エラーが発生しました</div>
          <div className="text-gray-600 mb-4">{error}</div>
          <Button onClick={() => window.location.reload()}>
            再読み込み
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ヘッダー */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div>
              <h1 className="text-xl font-semibold text-gray-900">スキル管理</h1>
              <p className="text-sm text-gray-600">スキル情報の登録・更新・検索</p>
            </div>
            <div className="flex items-center space-x-4">
              {/* 表示モード切り替え */}
              <div className="flex bg-gray-100 rounded-lg p-1">
                <button
                  onClick={() => setViewMode('hierarchy')}
                  className={`px-3 py-1 text-sm font-medium rounded-md transition-colors ${
                    viewMode === 'hierarchy'
                      ? 'bg-white text-gray-900 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  階層表示
                </button>
                <button
                  onClick={() => setViewMode('search')}
                  className={`px-3 py-1 text-sm font-medium rounded-md transition-colors ${
                    viewMode === 'search'
                      ? 'bg-white text-gray-900 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  検索
                </button>
              </div>
              <Button onClick={handleAddNewSkill}>
                新規スキル追加
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* 設計書準拠：タブナビゲーション */}
        <div className="mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('skills')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'skills'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                スキル管理
              </button>
              <button
                onClick={() => setActiveTab('certifications')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'certifications'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                資格情報
              </button>
            </nav>
          </div>
        </div>

        {activeTab === 'skills' ? (
          <>
            {/* スキルカテゴリタブ */}
            <div className="mb-6">
              <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
                {SKILL_CATEGORIES.map((category) => (
                  <button
                    key={category}
                    onClick={() => setActiveCategory(category)}
                    className={`px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                      activeCategory === category
                        ? 'bg-white text-gray-900 shadow-sm'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    {category}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* 左側: スキル一覧・検索 */}
              <div className="lg:col-span-2">
                {viewMode === 'hierarchy' ? (
                  <div className="bg-white border border-gray-200 rounded-lg">
                    <div className="p-4 border-b border-gray-200">
                      <h2 className="text-lg font-medium text-gray-900">スキル階層</h2>
                      <p className="text-sm text-gray-600">カテゴリ別にスキルを表示</p>
                    </div>
                    <div className="p-4">
                      {isLoading ? (
                        <div className="flex items-center justify-center py-8">
                          <Spinner size="md" />
                          <span className="ml-2 text-gray-600">読み込み中...</span>
                        </div>
                      ) : (
                        <SkillHierarchyTree
                          hierarchy={skillHierarchy}
                          userSkills={userSkills}
                          onSkillSelect={handleSkillSelect}
                          selectedSkillId={selectedSkill?.id || ''}
                        />
                      )}
                    </div>
                  </div>
                ) : (
                  <div>
                    {/* 検索フォーム */}
                    <SkillSearch
                      categories={categories}
                      onSearch={handleSearch}
                      onReset={handleSearchReset}
                      isLoading={isLoading}
                    />

                    {/* 検索結果 */}
                    <div className="bg-white border border-gray-200 rounded-lg">
                      <div className="p-4 border-b border-gray-200">
                        <h2 className="text-lg font-medium text-gray-900">検索結果</h2>
                        <p className="text-sm text-gray-600">
                          {searchResults.length > 0 ? `${searchResults.length}件のスキルが見つかりました` : '検索条件を入力してください'}
                        </p>
                      </div>
                      <div className="p-4">
                        {searchResults.length > 0 ? (
                          <div className="space-y-3">
                            {searchResults.map((skill) => (
                              <div
                                key={skill.id}
                                className="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer"
                                onClick={() => {
                                  // 検索結果からスキル選択時の処理
                                  const hierarchySkill: SkillHierarchy = {
                                    id: skill.skillId,
                                    name: skill.skillName,
                                    category: skill.category,
                                    subcategory: skill.subcategory || undefined,
                                    level: 3,
                                    description: ''
                                  };
                                  handleSkillSelect(hierarchySkill);
                                }}
                              >
                                <div>
                                  <div className="font-medium text-gray-900">{skill.skillName}</div>
                                  <div className="text-sm text-gray-600">
                                    {skill.category} {skill.subcategory && `> ${skill.subcategory}`}
                                  </div>
                                </div>
                                <div className="flex items-center space-x-2">
                                  <span className="text-sm text-gray-600">レベル:</span>
                                  <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                    {skill.level}
                                  </span>
                                </div>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <div className="text-center py-8 text-gray-500">
                            検索結果がありません
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* 右側: スキル詳細フォーム */}
              <div className="lg:col-span-1">
                {showForm ? (
                  <SkillDetailForm
                    selectedSkill={selectedSkill}
                    userSkill={selectedSkill ? userSkills.find(us => us.skillId === selectedSkill.id) || null : null}
                    relatedCertifications={[]}
                    onSave={handleFormSave}
                    onCancel={handleFormCancel}
                    isLoading={isLoading}
                  />
                ) : (
                  <div className="bg-white border border-gray-200 rounded-lg p-6">
                    <div className="text-center text-gray-500">
                      <div className="text-lg font-medium mb-2">スキルを選択してください</div>
                      <p className="text-sm">
                        左側のスキル一覧からスキルを選択するか、<br />
                        「新規スキル追加」ボタンをクリックしてください
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </>
        ) : (
          /* 資格情報タブ */
          <div className="bg-white border border-gray-200 rounded-lg">
            <div className="p-4 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-lg font-medium text-gray-900">資格情報</h2>
                  <p className="text-sm text-gray-600">取得済み資格の管理</p>
                </div>
                <Button onClick={() => setShowCertForm(true)}>
                  新規資格追加
                </Button>
              </div>
            </div>
            <div className="p-4">
              {certifications.length > 0 ? (
                <div className="space-y-4">
                  {certifications.map((cert) => (
                    <div key={cert.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="font-medium text-gray-900">{cert.certificationName}</h3>
                          {cert.organizationName && (
                            <p className="text-sm text-gray-600">{cert.organizationName}</p>
                          )}
                          <div className="mt-2 text-sm text-gray-500">
                            <p>取得日: {cert.acquiredDate}</p>
                            {cert.expiryDate && <p>有効期限: {cert.expiryDate}</p>}
                            {cert.score && <p>スコア: {cert.score}</p>}
                          </div>
                          {cert.remarks && (
                            <p className="mt-2 text-sm text-gray-600">{cert.remarks}</p>
                          )}
                        </div>
                        <div className="flex space-x-2">
                          <Button variant="secondary" size="sm">
                            編集
                          </Button>
                          <Button variant="secondary" size="sm">
                            削除
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <p>登録された資格情報がありません</p>
                  <p className="text-sm mt-1">「新規資格追加」ボタンから資格情報を登録してください</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
