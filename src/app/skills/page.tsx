// SKL.1-HIER.1: スキル管理画面
'use client';

import React, { useState, useEffect } from 'react';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { Sidebar } from '@/components/dashboard/Sidebar';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Spinner } from '@/components/ui/Spinner';

interface Skill {
  id: string;
  category: string;
  subcategory: string;
  name: string;
  level: number;
  experience_years?: number;
  last_used?: string;
  certification?: string;
  notes?: string;
  skillRecordId?: string;
  skillItemId?: string;
}

interface SkillCategory {
  id: string;
  name: string;
  subcategories: SkillSubcategory[];
}

interface SkillSubcategory {
  id: string;
  name: string;
  skills: string[];
}

export default function SkillsPage() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [skillCategories, setSkillCategories] = useState<SkillCategory[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'list' | 'add' | 'edit'>('list');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [editingSkill, setEditingSkill] = useState<Skill | null>(null);
  const [newSkill, setNewSkill] = useState<Partial<Skill>>({
    category: '',
    subcategory: '',
    name: '',
    level: 1,
    experience_years: 0,
    last_used: '',
    certification: '',
    notes: ''
  });

  const handleMenuClick = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleSidebarClose = () => {
    setIsSidebarOpen(false);
  };

  // API呼び出しによるデータ取得
  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        
        // 認証トークンを取得
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('認証トークンが見つかりません');
        }
        
        // スキルカテゴリマスタをAPIから取得
        const [categoriesResponse, skillsResponse] = await Promise.all([
          fetch('/api/skill-categories', {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            }
          }),
          fetch('/api/skills/me', {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            }
          })
        ]);

        if (!categoriesResponse.ok || !skillsResponse.ok) {
          throw new Error('APIエラー');
        }

        const categoriesData = await categoriesResponse.json();
        const skillsData = await skillsResponse.json();

        if (categoriesData.success) {
          console.log('Categories API response:', categoriesData.data);
          
          // APIレスポンスをフロントエンドの形式に変換
          // flatCategoriesを使用（階層構造は含まれているため）
          const categoriesSource = categoriesData.data.flatCategories || [];
          
          // flatCategoriesの場合、categoryIdとcategoryNameをid/nameにマッピング
          const transformedCategories = categoriesSource.map((cat: any) => ({
            id: cat.categoryId,  // APIからのcategoryIdをそのまま使用
            name: cat.categoryName,  // APIからのcategoryNameをそのまま使用
            subcategories: cat.children?.map((sub: any) => ({
              id: sub.categoryId,
              name: sub.categoryName,
              skills: sub.skills || []
            })) || []
          }));
          
          console.log('Transformed categories:', transformedCategories);
          setSkillCategories(transformedCategories);
        }

        if (skillsData.success) {
          // APIレスポンスをフロントエンドの形式に変換
          const transformedSkills: Skill[] = [];
          skillsData.data.skills?.forEach((category: any) => {
            category.skills?.forEach((skill: any) => {
              transformedSkills.push({
                id: skill.skillRecordId,
                skillRecordId: skill.skillRecordId,
                skillItemId: skill.skillItemId,
                category: category.categoryName,
                subcategory: skill.subcategory || '',
                name: skill.skillName,
                level: skill.skillLevel,
                experience_years: skill.projectExperienceCount || 0,
                last_used: skill.lastUsedDate || '',
                certification: skill.certification || '',
                notes: skill.evidenceDescription || ''
              });
            });
          });
          setSkills(transformedSkills);
        } else {
          // エラー時は空データを設定
          setSkills([]);
        }
      } catch (error) {
        console.error('データ読み込みエラー:', error);
        // エラー時は空データを設定
        setSkillCategories([]);
        setSkills([]);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, []);

  const getLevelText = (level: number) => {
    const levels = ['', '×', '△', '○', '◎'];
    return levels[level] || '';
  };

  const getLevelColor = (level: number) => {
    const colors = ['', 'text-red-500', 'text-yellow-500', 'text-blue-500', 'text-green-500'];
    return colors[level] || '';
  };

  const filteredSkills = skills.filter(skill => {
    const matchesSearch = skill.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         skill.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         skill.subcategory.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === '' || skill.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const handleAddSkill = async () => {
    if (!newSkill.name || !newSkill.category) {
      alert('必須項目を入力してください');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('認証トークンが見つかりません');
        return;
      }

      // カテゴリ名からカテゴリIDを取得
      const selectedCategoryObj = skillCategories.find(cat => cat.name === newSkill.category);
      const categoryId = selectedCategoryObj?.id || newSkill.category;
      
      // スキルアイテムIDを生成（スキル名から）
      const skillItemId = `SKILL_${newSkill.name.toUpperCase().replace(/[^A-Z0-9]/g, '_')}_${Date.now()}`;
      
      const response = await fetch('/api/skills', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          skillItemId: skillItemId,  // 生成したスキルアイテムID
          skillName: newSkill.name,  // スキル名も送信
          skillCategoryId: categoryId,  // カテゴリIDを使用
          skillLevel: newSkill.level || 1,
          selfAssessment: newSkill.level || 1,
          projectExperienceCount: newSkill.experience_years,
          lastUsedDate: newSkill.last_used,
          evidenceDescription: newSkill.notes,
        }),
      });

      if (!response.ok) {
        throw new Error('スキルの追加に失敗しました');
      }

      // データを再取得
      window.location.reload();
    } catch (error) {
      console.error('スキル追加エラー:', error);
      alert('スキルの追加に失敗しました');
    }
  };

  const handleEditSkill = (skill: Skill) => {
    setEditingSkill(skill);
    setActiveTab('edit');
  };

  const handleUpdateSkill = async () => {
    if (!editingSkill) return;

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('認証トークンが見つかりません');
        return;
      }

      // デバッグ: editingSkillの内容を確認
      console.log('Editing skill:', editingSkill);
      console.log('skillRecordId:', editingSkill.skillRecordId);
      console.log('experience_years:', editingSkill.experience_years);
      console.log('last_used:', editingSkill.last_used);

      if (!editingSkill.skillRecordId) {
        alert('スキルIDが見つかりません。一覧を再読み込みしてください。');
        window.location.reload();
        return;
      }

      const requestBody = {
        skillRecordId: editingSkill.skillRecordId || editingSkill.id,
        skillLevel: editingSkill.level,
        selfAssessment: editingSkill.level,
        learningHours: editingSkill.experience_years ? editingSkill.experience_years * 200 : 0,
        projectExperienceCount: editingSkill.experience_years || 0,
        lastUsedDate: editingSkill.last_used || '',
        evidenceDescription: editingSkill.notes || '',
      };

      console.log('Request body:', requestBody);

      const response = await fetch('/api/skills', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error('スキルの更新に失敗しました');
      }

      window.location.reload();
    } catch (error) {
      console.error('スキル更新エラー:', error);
      alert('スキルの更新に失敗しました');
    }
  };

  const handleDeleteSkill = async (skillId: string) => {
    if (!confirm('このスキルを削除してもよろしいですか？')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('認証トークンが見つかりません');
        return;
      }

      const response = await fetch(`/api/skills?skillRecordId=${skillId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('スキルの削除に失敗しました');
      }

      window.location.reload();
    } catch (error) {
      console.error('スキル削除エラー:', error);
      alert('スキルの削除に失敗しました');
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <DashboardHeader 
          onMenuClick={handleMenuClick}
          title="スキル管理"
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
        title="スキル管理"
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
          <div className="max-w-6xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
            {/* ページヘッダー */}
            <div className="mb-8">
              <h1 className="text-2xl font-bold text-gray-900">スキル管理</h1>
              <p className="text-gray-600 mt-1">保有スキルの登録・管理を行います</p>
            </div>

            {/* タブナビゲーション */}
            <div className="mb-6">
              <div className="border-b border-gray-200">
                <nav className="-mb-px flex space-x-8">
                  <button
                    onClick={() => setActiveTab('list')}
                    className={`py-2 px-1 border-b-2 font-medium text-sm ${
                      activeTab === 'list'
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    スキル一覧
                  </button>
                  <button
                    onClick={() => setActiveTab('add')}
                    className={`py-2 px-1 border-b-2 font-medium text-sm ${
                      activeTab === 'add'
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    スキル追加
                  </button>
                </nav>
              </div>
            </div>

            {/* スキル一覧タブ */}
            {activeTab === 'list' && (
              <div>
                {/* 検索・フィルター */}
                <div className="mb-6 bg-white p-4 rounded-lg shadow">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        キーワード検索
                      </label>
                      <Input
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        placeholder="スキル名、カテゴリで検索"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        カテゴリフィルター
                      </label>
                      <select
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="">すべてのカテゴリ</option>
                        {skillCategories.length > 0 ? (
                          skillCategories.map(category => (
                            <option key={category.id} value={category.name}>
                              {category.name}
                            </option>
                          ))
                        ) : (
                          <option value="" disabled>カテゴリを読み込み中...</option>
                        )}
                      </select>
                    </div>
                  </div>
                </div>

                {/* スキル一覧 */}
                <div className="bg-white shadow rounded-lg overflow-hidden">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          スキル名
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          カテゴリ
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          レベル
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          経験年数
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          最終使用
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          操作
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {filteredSkills.map((skill) => (
                        <tr key={skill.id} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm font-medium text-gray-900">{skill.name}</div>
                            <div className="text-sm text-gray-500">{skill.subcategory}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {skill.category}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`text-lg font-bold ${getLevelColor(skill.level)}`}>
                              {getLevelText(skill.level)}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {skill.experience_years}年
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {skill.last_used}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                            <button 
                              onClick={() => handleEditSkill(skill)}
                              className="text-blue-600 hover:text-blue-900 mr-3"
                            >
                              編集
                            </button>
                            <button 
                              onClick={() => handleDeleteSkill(skill.skillRecordId || skill.id)}
                              className="text-red-600 hover:text-red-900"
                            >
                              削除
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* スキル追加タブ */}
            {activeTab === 'add' && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-6">新しいスキルを追加</h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* カテゴリ */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      カテゴリ <span className="text-red-500">*</span>
                    </label>
                    <select
                      value={newSkill.category}
                      onChange={(e) => setNewSkill({...newSkill, category: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="">カテゴリを選択</option>
                      {skillCategories.length > 0 ? (
                        skillCategories.map(category => (
                          <option key={category.id} value={category.name}>
                            {category.name}
                          </option>
                        ))
                      ) : (
                        <option value="" disabled>カテゴリを読み込み中...</option>
                      )}
                    </select>
                  </div>

                  {/* サブカテゴリ（オプション） */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      サブカテゴリ（任意）
                    </label>
                    <Input
                      value={newSkill.subcategory}
                      onChange={(e) => setNewSkill({...newSkill, subcategory: e.target.value})}
                      placeholder="例: Frontend, Backend など（任意）"
                      disabled={!newSkill.category}
                    />
                  </div>

                  {/* スキル名 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      スキル名 <span className="text-red-500">*</span>
                    </label>
                    <Input
                      value={newSkill.name}
                      onChange={(e) => setNewSkill({...newSkill, name: e.target.value})}
                      placeholder="例: JavaScript"
                    />
                  </div>

                  {/* レベル */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      レベル <span className="text-red-500">*</span>
                    </label>
                    <select
                      value={newSkill.level}
                      onChange={(e) => setNewSkill({...newSkill, level: parseInt(e.target.value)})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value={1}>× - 未経験</option>
                      <option value={2}>△ - 基礎レベル</option>
                      <option value={3}>○ - 実務レベル</option>
                      <option value={4}>◎ - エキスパート</option>
                    </select>
                  </div>

                  {/* 経験年数 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      経験年数
                    </label>
                    <Input
                      type="number"
                      value={newSkill.experience_years}
                      onChange={(e) => setNewSkill({...newSkill, experience_years: parseInt(e.target.value) || 0})}
                      min="0"
                      placeholder="0"
                    />
                  </div>

                  {/* 最終使用日 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      最終使用日
                    </label>
                    <Input
                      type="date"
                      value={newSkill.last_used}
                      onChange={(e) => setNewSkill({...newSkill, last_used: e.target.value})}
                    />
                  </div>

                  {/* 資格・認定 */}
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      関連資格・認定
                    </label>
                    <Input
                      value={newSkill.certification}
                      onChange={(e) => setNewSkill({...newSkill, certification: e.target.value})}
                      placeholder="例: AWS Solutions Architect Associate"
                    />
                  </div>

                  {/* 備考 */}
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      備考・詳細
                    </label>
                    <textarea
                      value={newSkill.notes}
                      onChange={(e) => setNewSkill({...newSkill, notes: e.target.value})}
                      rows={3}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      placeholder="スキルの詳細や特記事項を入力"
                    />
                  </div>
                </div>

                <div className="mt-6 flex justify-end space-x-3">
                  <Button
                    onClick={() => setActiveTab('list')}
                    variant="secondary"
                  >
                    キャンセル
                  </Button>
                  <Button
                    onClick={handleAddSkill}
                    variant="primary"
                  >
                    スキルを追加
                  </Button>
                </div>
              </div>
            )}

            {/* スキル編集タブ */}
            {activeTab === 'edit' && editingSkill && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-6">スキルを編集</h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* スキル名（読み取り専用） */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      スキル名
                    </label>
                    <Input
                      value={editingSkill.name}
                      disabled
                      className="bg-gray-50"
                    />
                  </div>

                  {/* カテゴリ（読み取り専用） */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      カテゴリ
                    </label>
                    <Input
                      value={editingSkill.category}
                      disabled
                      className="bg-gray-50"
                    />
                  </div>

                  {/* レベル */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      レベル <span className="text-red-500">*</span>
                    </label>
                    <select
                      value={editingSkill.level}
                      onChange={(e) => setEditingSkill({...editingSkill, level: parseInt(e.target.value)})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value={1}>× - 未経験</option>
                      <option value={2}>△ - 基礎レベル</option>
                      <option value={3}>○ - 実務レベル</option>
                      <option value={4}>◎ - エキスパート</option>
                    </select>
                  </div>

                  {/* 経験年数 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      経験年数
                    </label>
                    <Input
                      type="number"
                      value={editingSkill.experience_years}
                      onChange={(e) => setEditingSkill({...editingSkill, experience_years: parseInt(e.target.value)})}
                      min={0}
                    />
                  </div>

                  {/* 最終使用 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      最終使用
                    </label>
                    <Input
                      type="date"
                      value={editingSkill.last_used}
                      onChange={(e) => setEditingSkill({...editingSkill, last_used: e.target.value})}
                    />
                  </div>

                  {/* 資格・認定 */}
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      関連資格・認定
                    </label>
                    <Input
                      value={editingSkill.certification}
                      onChange={(e) => setEditingSkill({...editingSkill, certification: e.target.value})}
                      placeholder="例: AWS Solutions Architect Associate"
                    />
                  </div>

                  {/* 備考 */}
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      備考・詳細
                    </label>
                    <textarea
                      value={editingSkill.notes}
                      onChange={(e) => setEditingSkill({...editingSkill, notes: e.target.value})}
                      rows={3}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      placeholder="スキルの詳細や特記事項を入力"
                    />
                  </div>
                </div>

                <div className="mt-6 flex justify-end space-x-3">
                  <Button
                    onClick={() => {
                      setEditingSkill(null);
                      setActiveTab('list');
                    }}
                    variant="secondary"
                  >
                    キャンセル
                  </Button>
                  <Button
                    onClick={handleUpdateSkill}
                    variant="primary"
                  >
                    更新する
                  </Button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
