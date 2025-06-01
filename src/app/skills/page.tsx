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
  const [activeTab, setActiveTab] = useState<'list' | 'add'>('list');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
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

  // モックデータの初期化
  useEffect(() => {
    const loadData = async () => {
      try {
        await new Promise(resolve => setTimeout(resolve, 1000));

        const mockCategories: SkillCategory[] = [
          {
            id: '1',
            name: 'プログラミング言語',
            subcategories: [
              { id: '1-1', name: 'フロントエンド', skills: ['JavaScript', 'TypeScript', 'React', 'Vue.js', 'Angular'] },
              { id: '1-2', name: 'バックエンド', skills: ['Node.js', 'Python', 'Java', 'C#', 'Go'] },
              { id: '1-3', name: 'モバイル', skills: ['React Native', 'Flutter', 'Swift', 'Kotlin'] }
            ]
          },
          {
            id: '2',
            name: 'インフラ・クラウド',
            subcategories: [
              { id: '2-1', name: 'クラウドサービス', skills: ['AWS', 'Azure', 'GCP', 'Vercel', 'Netlify'] },
              { id: '2-2', name: 'コンテナ', skills: ['Docker', 'Kubernetes', 'Docker Compose'] },
              { id: '2-3', name: 'CI/CD', skills: ['GitHub Actions', 'Jenkins', 'GitLab CI'] }
            ]
          },
          {
            id: '3',
            name: 'データベース',
            subcategories: [
              { id: '3-1', name: 'リレーショナル', skills: ['PostgreSQL', 'MySQL', 'SQL Server'] },
              { id: '3-2', name: 'NoSQL', skills: ['MongoDB', 'Redis', 'DynamoDB'] }
            ]
          }
        ];

        const mockSkills: Skill[] = [
          {
            id: '1',
            category: 'プログラミング言語',
            subcategory: 'フロントエンド',
            name: 'JavaScript',
            level: 4,
            experience_years: 5,
            last_used: '2025-05-30',
            certification: '',
            notes: 'ES6+の機能を活用した開発経験豊富'
          },
          {
            id: '2',
            category: 'プログラミング言語',
            subcategory: 'フロントエンド',
            name: 'React',
            level: 4,
            experience_years: 3,
            last_used: '2025-05-30',
            certification: '',
            notes: 'Hooks、Context API、Next.jsでの開発経験あり'
          },
          {
            id: '3',
            category: 'インフラ・クラウド',
            subcategory: 'クラウドサービス',
            name: 'AWS',
            level: 3,
            experience_years: 2,
            last_used: '2025-05-15',
            certification: 'AWS Solutions Architect Associate',
            notes: 'EC2、S3、RDS、Lambda等の基本サービス利用経験'
          }
        ];

        setSkillCategories(mockCategories);
        setSkills(mockSkills);
      } catch (error) {
        console.error('データ読み込みエラー:', error);
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

  const handleAddSkill = () => {
    if (!newSkill.name || !newSkill.category || !newSkill.subcategory) {
      alert('必須項目を入力してください');
      return;
    }

    const skill: Skill = {
      id: Date.now().toString(),
      category: newSkill.category!,
      subcategory: newSkill.subcategory!,
      name: newSkill.name!,
      level: newSkill.level || 1,
      experience_years: newSkill.experience_years || 0,
      last_used: newSkill.last_used || '',
      certification: newSkill.certification || '',
      notes: newSkill.notes || ''
    };

    setSkills([...skills, skill]);
    setNewSkill({
      category: '',
      subcategory: '',
      name: '',
      level: 1,
      experience_years: 0,
      last_used: '',
      certification: '',
      notes: ''
    });
    setActiveTab('list');
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
                        {skillCategories.map(category => (
                          <option key={category.id} value={category.name}>
                            {category.name}
                          </option>
                        ))}
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
                            <button className="text-blue-600 hover:text-blue-900 mr-3">
                              編集
                            </button>
                            <button className="text-red-600 hover:text-red-900">
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
                      onChange={(e) => setNewSkill({...newSkill, category: e.target.value, subcategory: ''})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="">カテゴリを選択</option>
                      {skillCategories.map(category => (
                        <option key={category.id} value={category.name}>
                          {category.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* サブカテゴリ */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      サブカテゴリ <span className="text-red-500">*</span>
                    </label>
                    <select
                      value={newSkill.subcategory}
                      onChange={(e) => setNewSkill({...newSkill, subcategory: e.target.value})}
                      disabled={!newSkill.category}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-50"
                    >
                      <option value="">サブカテゴリを選択</option>
                      {skillCategories
                        .find(cat => cat.name === newSkill.category)
                        ?.subcategories.map(sub => (
                          <option key={sub.id} value={sub.name}>
                            {sub.name}
                          </option>
                        ))}
                    </select>
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
          </div>
        </div>
      </div>
    </div>
  );
}
