/**
 * 要求仕様ID: SKL.1-HIER.1, SKL.1-EVAL.1, SKL.1-MAINT.1, SKL.1-SRCH.1
 * 対応設計書: docs/design/api/specs/API定義書_API-021_スキル情報取得API.md
 * 実装内容: スキル管理API連携サービス
 */

import {
  SkillHierarchy,
  UserSkill,
  SkillMaster,
  Certification,
  CertificationMaster,
  SkillSearchResult,
  SkillFormData,
  CertificationFormData,
  SkillSearchParams,
  SkillApiResponse,
  SkillApiError,
  SkillLevel
} from '@/types/skills';
import { getAuthHeaders } from '@/lib/authClient';

const API_BASE_URL = '/api';

// 共通のfetch関数
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  // 認証ヘッダーを自動的に追加
  const authHeaders = getAuthHeaders();
  
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...authHeaders,
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, defaultOptions);
    
    if (!response.ok) {
      // APIが存在しない場合（404）やその他のエラーの場合は例外を投げる
      console.warn(`API Error [${endpoint}]: ${response.status} ${response.statusText}`);
      throw new Error(`API_ERROR: ${response.status}`);
    }

    // レスポンスのContent-Typeをチェック
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      console.warn(`API Error [${endpoint}]: Invalid content type: ${contentType}`);
      throw new Error('API_ERROR: Invalid response format');
    }

    const data: SkillApiResponse<T> = await response.json();
    
    if (!data.success) {
      throw new Error(data.message || 'API request failed');
    }

    return data.data;
  } catch (error) {
    // ネットワークエラーやその他のエラーをキャッチ
    if (error instanceof TypeError && error.message.includes('fetch')) {
      console.warn(`Network error [${endpoint}]:`, error);
      throw new Error('API_ERROR: Network error');
    }
    
    // JSONパースエラーの場合
    if (error instanceof SyntaxError) {
      console.warn(`JSON parse error [${endpoint}]:`, error);
      throw new Error('API_ERROR: Invalid JSON response');
    }
    
    // APIエラーの場合は例外を再投げして、呼び出し元でモックデータを返すようにする
    console.warn(`API request failed [${endpoint}]:`, error);
    throw error;
  }
}

// APIレスポンス変換関数
function convertSkillResponseToUserSkill(skillResponse: any): UserSkill {
  return {
    id: skillResponse.skill_id || '',
    skillId: skillResponse.skill_id || '',
    userId: 'current-user', // 現在のユーザーID
    skillName: skillResponse.name || '',
    category: skillResponse.category || 'technical',
    subcategory: skillResponse.subcategory || undefined,
    level: (skillResponse.level as SkillLevel) || 1,
    acquiredDate: skillResponse.acquired_date || undefined,
    experienceYears: skillResponse.experience_years || undefined,
    lastUsed: skillResponse.last_used_date || undefined,
    remarks: skillResponse.description || undefined,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };
}

// スキルマスタAPI (API-023)
export const skillMasterApi = {
  // スキル階層取得
  async getHierarchy(category?: string): Promise<SkillHierarchy[]> {
    try {
      const params = new URLSearchParams();
      if (category) {
        params.append('category', category);
        console.log('API request with category:', category);
      }
      
      const apiResponse = await apiRequest<any[]>(
        `/skills/master${params.toString() ? `?${params.toString()}` : ''}`
      );
      
      console.log('API response:', apiResponse);
      
      // APIレスポンスの構造を確認して適切に変換
      if (Array.isArray(apiResponse) && apiResponse.length > 0) {
        // APIが3階層構造のデータを返している場合
        const hierarchyData: SkillHierarchy[] = apiResponse.map(categoryData => ({
          id: categoryData.id || categoryData.category_id || categoryData.category_code,
          name: categoryData.name || categoryData.category_name,
          category: categoryData.name || categoryData.category_name,
          level: categoryData.level || 1,
          description: categoryData.description || '',
          children: (categoryData.children || []).map((subcategory: any) => ({
            id: subcategory.id,
            name: subcategory.name,
            category: categoryData.name || categoryData.category_name,
            subcategory: subcategory.name,
            parentId: categoryData.id || categoryData.category_id,
            level: subcategory.level || 2,
            description: subcategory.description || '',
            children: (subcategory.children || []).map((skill: any) => ({
              id: skill.id,
              name: skill.name,
              category: categoryData.name || categoryData.category_name,
              subcategory: subcategory.name,
              parentId: subcategory.id,
              level: skill.level || 3,
              description: skill.description || '',
              difficulty_level: skill.difficulty_level,
              importance_level: skill.importance_level
            }))
          }))
        }));
        
        console.log('Converted hierarchy data:', hierarchyData);
        return hierarchyData;
      }
      
      // フォールバック処理
      throw new Error('Invalid API response structure');
    } catch (error) {
      console.warn('スキル階層API呼び出しに失敗しました。モックデータを返します:', error);
      
      // 完全なモックデータを定義
      const allMockData = [
        {
          id: 'TECH',
          name: '技術スキル',
          category: '技術スキル',
          level: 1,
          description: 'プログラミング言語・フレームワーク・技術基盤',
          children: [
            {
              id: 'TECH_programming',
              name: 'プログラミング',
              category: '技術スキル',
              subcategory: 'プログラミング',
              parentId: 'TECH',
              level: 2,
              description: 'プログラミング言語',
              children: [
                {
                  id: 'javascript',
                  name: 'JavaScript',
                  category: '技術スキル',
                  subcategory: 'プログラミング',
                  parentId: 'TECH_programming',
                  level: 3,
                  description: 'JavaScript プログラミング言語'
                },
                {
                  id: 'typescript',
                  name: 'TypeScript',
                  category: '技術スキル',
                  subcategory: 'プログラミング',
                  parentId: 'TECH_programming',
                  level: 3,
                  description: 'TypeScript プログラミング言語'
                },
                {
                  id: 'python',
                  name: 'Python',
                  category: '技術スキル',
                  subcategory: 'プログラミング',
                  parentId: 'TECH_programming',
                  level: 3,
                  description: 'Python プログラミング言語'
                }
              ]
            },
            {
              id: 'TECH_framework',
              name: 'フレームワーク',
              category: '技術スキル',
              subcategory: 'フレームワーク',
              parentId: 'TECH',
              level: 2,
              description: 'フレームワーク・ライブラリ',
              children: [
                {
                  id: 'react',
                  name: 'React',
                  category: '技術スキル',
                  subcategory: 'フレームワーク',
                  parentId: 'TECH_framework',
                  level: 3,
                  description: 'React フレームワーク'
                },
                {
                  id: 'nextjs',
                  name: 'Next.js',
                  category: '技術スキル',
                  subcategory: 'フレームワーク',
                  parentId: 'TECH_framework',
                  level: 3,
                  description: 'Next.js フレームワーク'
                }
              ]
            },
            {
              id: 'TECH_database',
              name: 'データベース',
              category: '技術スキル',
              subcategory: 'データベース',
              parentId: 'TECH',
              level: 2,
              description: 'データベース技術',
              children: [
                {
                  id: 'postgresql',
                  name: 'PostgreSQL',
                  category: '技術スキル',
                  subcategory: 'データベース',
                  parentId: 'TECH_database',
                  level: 3,
                  description: 'PostgreSQL データベース'
                },
                {
                  id: 'mysql',
                  name: 'MySQL',
                  category: '技術スキル',
                  subcategory: 'データベース',
                  parentId: 'TECH_database',
                  level: 3,
                  description: 'MySQL データベース'
                }
              ]
            }
          ]
        },
        {
          id: 'DEV',
          name: '開発スキル',
          category: '開発スキル',
          level: 1,
          description: '開発手法・ツール・プロセス',
          children: [
            {
              id: 'DEV_version_control',
              name: 'バージョン管理',
              category: '開発スキル',
              subcategory: 'バージョン管理',
              parentId: 'DEV',
              level: 2,
              description: 'ソースコード管理',
              children: [
                {
                  id: 'git',
                  name: 'Git',
                  category: '開発スキル',
                  subcategory: 'バージョン管理',
                  parentId: 'DEV_version_control',
                  level: 3,
                  description: 'Git バージョン管理システム'
                },
                {
                  id: 'github',
                  name: 'GitHub',
                  category: '開発スキル',
                  subcategory: 'バージョン管理',
                  parentId: 'DEV_version_control',
                  level: 3,
                  description: 'GitHub プラットフォーム'
                }
              ]
            },
            {
              id: 'DEV_container',
              name: 'コンテナ技術',
              category: '開発スキル',
              subcategory: 'コンテナ技術',
              parentId: 'DEV',
              level: 2,
              description: 'コンテナ化技術',
              children: [
                {
                  id: 'docker',
                  name: 'Docker',
                  category: '開発スキル',
                  subcategory: 'コンテナ技術',
                  parentId: 'DEV_container',
                  level: 3,
                  description: 'Docker コンテナ技術'
                },
                {
                  id: 'kubernetes',
                  name: 'Kubernetes',
                  category: '開発スキル',
                  subcategory: 'コンテナ技術',
                  parentId: 'DEV_container',
                  level: 3,
                  description: 'Kubernetes オーケストレーション'
                }
              ]
            },
            {
              id: 'DEV_automation',
              name: '自動化',
              category: '開発スキル',
              subcategory: '自動化',
              parentId: 'DEV',
              level: 2,
              description: '開発プロセス自動化',
              children: [
                {
                  id: 'ci-cd',
                  name: 'CI/CD',
                  category: '開発スキル',
                  subcategory: '自動化',
                  parentId: 'DEV_automation',
                  level: 3,
                  description: '継続的インテグレーション・デプロイメント'
                },
                {
                  id: 'testing',
                  name: 'テスト技法',
                  category: '開発スキル',
                  subcategory: '自動化',
                  parentId: 'DEV_automation',
                  level: 3,
                  description: 'ユニットテスト・統合テスト・E2Eテスト'
                }
              ]
            }
          ]
        },
        {
          id: 'BIZ',
          name: '業務スキル',
          category: '業務スキル',
          level: 1,
          description: '業務知識・ドメイン知識',
          children: [
            {
              id: 'BIZ_analysis',
              name: '分析',
              category: '業務スキル',
              subcategory: '分析',
              parentId: 'BIZ',
              level: 2,
              description: '業務分析・要件分析',
              children: [
                {
                  id: 'requirements-analysis',
                  name: '要件分析',
                  category: '業務スキル',
                  subcategory: '分析',
                  parentId: 'BIZ_analysis',
                  level: 3,
                  description: '業務要件の分析・整理'
                },
                {
                  id: 'business-analysis',
                  name: '業務分析',
                  category: '業務スキル',
                  subcategory: '分析',
                  parentId: 'BIZ_analysis',
                  level: 3,
                  description: '業務プロセスの分析・改善'
                }
              ]
            },
            {
              id: 'BIZ_design',
              name: '設計',
              category: '業務スキル',
              subcategory: '設計',
              parentId: 'BIZ',
              level: 2,
              description: 'システム設計・業務設計',
              children: [
                {
                  id: 'system-design',
                  name: 'システム設計',
                  category: '業務スキル',
                  subcategory: '設計',
                  parentId: 'BIZ_design',
                  level: 3,
                  description: 'システム全体の設計・アーキテクチャ'
                },
                {
                  id: 'ui-ux-design',
                  name: 'UI/UX設計',
                  category: '業務スキル',
                  subcategory: '設計',
                  parentId: 'BIZ_design',
                  level: 3,
                  description: 'ユーザーインターフェース・体験設計'
                }
              ]
            },
            {
              id: 'BIZ_communication',
              name: 'コミュニケーション',
              category: '業務スキル',
              subcategory: 'コミュニケーション',
              parentId: 'BIZ',
              level: 2,
              description: 'コミュニケーション・ドキュメント作成',
              children: [
                {
                  id: 'documentation',
                  name: 'ドキュメント作成',
                  category: '業務スキル',
                  subcategory: 'コミュニケーション',
                  parentId: 'BIZ_communication',
                  level: 3,
                  description: '技術文書・仕様書の作成'
                },
                {
                  id: 'presentation',
                  name: 'プレゼンテーション',
                  category: '業務スキル',
                  subcategory: 'コミュニケーション',
                  parentId: 'BIZ_communication',
                  level: 3,
                  description: '効果的なプレゼンテーション技法'
                }
              ]
            }
          ]
        },
        {
          id: 'MGT',
          name: '管理スキル',
          category: '管理スキル',
          level: 1,
          description: 'プロジェクト管理・チーム管理',
          children: [
            {
              id: 'MGT_project',
              name: 'プロジェクト',
              category: '管理スキル',
              subcategory: 'プロジェクト',
              parentId: 'MGT',
              level: 2,
              description: 'プロジェクト管理・計画',
              children: [
                {
                  id: 'project-management',
                  name: 'プロジェクト管理',
                  category: '管理スキル',
                  subcategory: 'プロジェクト',
                  parentId: 'MGT_project',
                  level: 3,
                  description: 'プロジェクトの計画・実行・管理'
                },
                {
                  id: 'schedule-management',
                  name: 'スケジュール管理',
                  category: '管理スキル',
                  subcategory: 'プロジェクト',
                  parentId: 'MGT_project',
                  level: 3,
                  description: 'プロジェクトスケジュールの管理'
                }
              ]
            },
            {
              id: 'MGT_leadership',
              name: 'リーダーシップ',
              category: '管理スキル',
              subcategory: 'リーダーシップ',
              parentId: 'MGT',
              level: 2,
              description: 'チーム指導・人材育成',
              children: [
                {
                  id: 'team-leadership',
                  name: 'チームリーダーシップ',
                  category: '管理スキル',
                  subcategory: 'リーダーシップ',
                  parentId: 'MGT_leadership',
                  level: 3,
                  description: 'チームの指導・育成・マネジメント'
                },
                {
                  id: 'mentoring',
                  name: 'メンタリング',
                  category: '管理スキル',
                  subcategory: 'リーダーシップ',
                  parentId: 'MGT_leadership',
                  level: 3,
                  description: '後輩・部下の指導・育成'
                }
              ]
            },
            {
              id: 'MGT_risk',
              name: 'リスク',
              category: '管理スキル',
              subcategory: 'リスク',
              parentId: 'MGT',
              level: 2,
              description: 'リスク管理・品質管理',
              children: [
                {
                  id: 'risk-management',
                  name: 'リスク管理',
                  category: '管理スキル',
                  subcategory: 'リスク',
                  parentId: 'MGT_risk',
                  level: 3,
                  description: 'プロジェクトリスクの識別・対策'
                },
                {
                  id: 'quality-management',
                  name: '品質管理',
                  category: '管理スキル',
                  subcategory: 'リスク',
                  parentId: 'MGT_risk',
                  level: 3,
                  description: '品質保証・品質改善'
                }
              ]
            }
          ]
        },
        {
          id: 'PROD',
          name: '生産スキル',
          category: '生産スキル',
          level: 1,
          description: '生産性向上・効率化',
          children: [
            {
              id: 'PROD_efficiency',
              name: '効率化',
              category: '生産スキル',
              subcategory: '効率化',
              parentId: 'PROD',
              level: 2,
              description: '業務効率化・自動化',
              children: [
                {
                  id: 'automation',
                  name: '自動化',
                  category: '生産スキル',
                  subcategory: '効率化',
                  parentId: 'PROD_efficiency',
                  level: 3,
                  description: '業務プロセスの自動化'
                },
                {
                  id: 'process-improvement',
                  name: 'プロセス改善',
                  category: '生産スキル',
                  subcategory: '効率化',
                  parentId: 'PROD_efficiency',
                  level: 3,
                  description: '業務プロセスの改善・最適化'
                }
              ]
            },
            {
              id: 'PROD_performance',
              name: 'パフォーマンス',
              category: '生産スキル',
              subcategory: 'パフォーマンス',
              parentId: 'PROD',
              level: 2,
              description: 'システム・業務パフォーマンス向上',
              children: [
                {
                  id: 'optimization',
                  name: '最適化',
                  category: '生産スキル',
                  subcategory: 'パフォーマンス',
                  parentId: 'PROD_performance',
                  level: 3,
                  description: 'システム・プロセスの最適化'
                },
                {
                  id: 'monitoring',
                  name: '監視・運用',
                  category: '生産スキル',
                  subcategory: 'パフォーマンス',
                  parentId: 'PROD_performance',
                  level: 3,
                  description: 'システム監視・運用保守'
                }
              ]
            }
          ]
        }
      ];

      // カテゴリが指定されている場合は、そのカテゴリのみを返す
      if (category) {
        const filteredData = allMockData.filter(item => item.id === category);
        console.log('Filtering mock data for category:', category, 'Result:', filteredData);
        return filteredData;
      }

      console.log('Returning all mock data:', allMockData);
      return allMockData;
    }
  },

  // スキルマスタ一覧取得
  async getSkills(params?: { category?: string; subcategory?: string }): Promise<SkillMaster[]> {
    try {
      const searchParams = new URLSearchParams();
      if (params?.category) searchParams.append('category', params.category);
      if (params?.subcategory) searchParams.append('subcategory', params.subcategory);
      
      return await apiRequest<SkillMaster[]>(
        `/skills/master${searchParams.toString() ? `?${searchParams.toString()}` : ''}`
      );
    } catch (error) {
      console.warn('スキルマスタAPI呼び出しに失敗しました。モックデータを返します:', error);
      
      // モックデータを返す
      return [
        {
          id: 'javascript',
          name: 'JavaScript',
          category: '技術スキル',
          subcategory: 'プログラミング言語',
          description: 'Webフロントエンド開発言語',
          isActive: true,
          sortOrder: 1
        },
        {
          id: 'typescript',
          name: 'TypeScript',
          category: '技術スキル',
          subcategory: 'プログラミング言語',
          description: 'JavaScript拡張言語',
          isActive: true,
          sortOrder: 2
        },
        {
          id: 'react',
          name: 'React',
          category: '技術スキル',
          subcategory: 'フレームワーク',
          description: 'Webフロントエンドライブラリ',
          isActive: true,
          sortOrder: 3
        }
      ];
    }
  }
};

// ユーザースキルAPI (API-021, API-022)
export const userSkillApi = {
  // ユーザースキル取得
  async getUserSkills(userId?: string): Promise<UserSkill[]> {
    try {
      const endpoint = userId ? `/skills/${userId}` : '/skills';
      const skillResponses = await apiRequest<any[]>(endpoint);
      return skillResponses.map(convertSkillResponseToUserSkill);
    } catch (error) {
      console.warn('ユーザースキルAPI呼び出しに失敗しました。モックデータを返します:', error);
      
      // モックデータを返す
      return [
        {
          id: '1',
          skillId: 'javascript',
          userId: 'current-user',
          skillName: 'JavaScript',
          category: '技術スキル',
          subcategory: 'プログラミング言語',
          level: 3,
          acquiredDate: '2023-01-01',
          experienceYears: 2,
          lastUsed: '2024-12-01',
          remarks: 'React、Vue.jsでの開発経験あり',
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString()
        },
        {
          id: '2',
          skillId: 'typescript',
          userId: 'current-user',
          skillName: 'TypeScript',
          category: '技術スキル',
          subcategory: 'プログラミング言語',
          level: 2,
          acquiredDate: '2023-06-01',
          experienceYears: 1,
          lastUsed: '2024-11-01',
          remarks: 'Next.jsプロジェクトで使用',
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString()
        },
        {
          id: '3',
          skillId: 'react',
          userId: 'current-user',
          skillName: 'React',
          category: '技術スキル',
          subcategory: 'フレームワーク',
          level: 3,
          acquiredDate: '2022-08-01',
          experienceYears: 2,
          lastUsed: '2024-12-01',
          remarks: 'Hooks、Context APIを活用',
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString()
        }
      ];
    }
  },

  // 特定スキル取得
  async getSkill(skillId: string, userId?: string): Promise<UserSkill> {
    try {
      const endpoint = userId ? `/skills/${userId}` : '/skills';
      const params = new URLSearchParams({ skillId });
      const skillResponse = await apiRequest<any>(`${endpoint}?${params.toString()}`);
      return convertSkillResponseToUserSkill(skillResponse);
    } catch (error) {
      console.warn('スキル取得API呼び出しに失敗しました。モックデータを返します:', error);
      
      // モックデータを返す
      return {
        id: skillId,
        skillId: skillId,
        userId: 'current-user',
        skillName: skillId,
        category: '技術スキル',
        subcategory: 'プログラミング言語',
        level: 1,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };
    }
  },

  // スキル情報更新
  async updateSkill(skillData: SkillFormData, userId?: string): Promise<UserSkill> {
    try {
      const endpoint = userId ? `/skills/${userId}` : '/skills';
      
      // APIが期待する形式に変換
      const requestData = {
        year: new Date().getFullYear(),
        skills: [{
          skill_id: skillData.skillId,
          name: skillData.skillId, // スキル名（実際にはマスタから取得すべき）
          category: 'technical', // デフォルトカテゴリ
          level: skillData.level,
          experience_years: skillData.experienceYears || 0,
          description: skillData.remarks || '',
          last_used_date: skillData.lastUsed || '',
          projects: [],
          certifications: [],
          self_assessment: {
            strengths: '',
            weaknesses: '',
            improvement_plan: ''
          }
        }]
      };
      
      const response = await apiRequest<any>(endpoint, {
        method: 'PUT',
        body: JSON.stringify(requestData),
      });
      
      // レスポンスから最初のスキルを取得して変換
      const skillResponse = response.skills[0];
      return convertSkillResponseToUserSkill(skillResponse);
    } catch (error) {
      console.warn('スキル更新API呼び出しに失敗しました。モックデータを返します:', error);
      
      // モックデータを返す
      return {
        id: skillData.skillId,
        skillId: skillData.skillId,
        userId: 'current-user',
        skillName: skillData.skillId,
        category: '技術スキル',
        level: skillData.level,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };
    }
  },

  // スキル作成
  async createSkill(skillData: SkillFormData, userId?: string): Promise<UserSkill> {
    try {
      const endpoint = userId ? `/skills/${userId}` : '/skills';
      
      // APIが期待する形式に変換
      const requestData = {
        year: new Date().getFullYear(),
        skills: [{
          skill_id: skillData.skillId,
          name: skillData.skillId,
          category: 'technical',
          level: skillData.level,
          experience_years: skillData.experienceYears || 0,
          description: skillData.remarks || '',
          last_used_date: skillData.lastUsed || '',
          projects: [],
          certifications: [],
          self_assessment: {
            strengths: '',
            weaknesses: '',
            improvement_plan: ''
          }
        }]
      };
      
      const response = await apiRequest<any>(endpoint, {
        method: 'POST',
        body: JSON.stringify(requestData),
      });
      
      const skillResponse = response.skills[0];
      return convertSkillResponseToUserSkill(skillResponse);
    } catch (error) {
      console.warn('スキル作成API呼び出しに失敗しました。モックデータを返します:', error);
      
      return {
        id: skillData.skillId,
        skillId: skillData.skillId,
        userId: 'current-user',
        skillName: skillData.skillId,
        category: '技術スキル',
        level: skillData.level,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };
    }
  },

  // スキル削除
  async deleteSkill(skillId: string, userId?: string): Promise<void> {
    try {
      const endpoint = userId ? `/skills/${userId}` : '/skills';
      const params = new URLSearchParams({ skillId });
      
      await apiRequest<void>(`${endpoint}?${params.toString()}`, {
        method: 'DELETE',
      });
    } catch (error) {
      console.warn('スキル削除API呼び出しに失敗しました:', error);
      // モックでは何もしない
    }
  }
};

// スキル検索API
export const skillSearchApi = {
  // スキル検索
  async searchSkills(params: SkillSearchParams): Promise<SkillSearchResult[]> {
    try {
      const searchParams = new URLSearchParams();
      if (params.keyword) searchParams.append('keyword', params.keyword);
      if (params.category) searchParams.append('category', params.category);
      if (params.subcategory) searchParams.append('subcategory', params.subcategory);
      if (params.level) searchParams.append('level', params.level.toString());
      
      return await apiRequest<SkillSearchResult[]>(
        `/skills/search?${searchParams.toString()}`
      );
    } catch (error) {
      console.warn('スキル検索API呼び出しに失敗しました。モックデータを返します:', error);
      
      // モックデータを返す
      return [
        {
          skillId: 'javascript',
          skillName: 'JavaScript',
          category: '技術スキル',
          subcategory: 'プログラミング言語',
          description: 'Webフロントエンド開発言語',
          userCount: 150,
          averageLevel: 2.8
        },
        {
          skillId: 'typescript',
          skillName: 'TypeScript',
          category: '技術スキル',
          subcategory: 'プログラミング言語',
          description: 'JavaScript拡張言語',
          userCount: 120,
          averageLevel: 2.5
        }
      ];
    }
  }
};

// 資格情報API
export const certificationApi = {
  // 資格一覧取得
  async getCertifications(userId?: string): Promise<Certification[]> {
    try {
      const endpoint = userId ? `/certifications?userId=${userId}` : '/certifications';
      return await apiRequest<Certification[]>(endpoint);
    } catch (error) {
      console.warn('資格情報API呼び出しに失敗しました。モックデータを返します:', error);
      
      // モックデータを返す
      return [
        {
          id: '1',
          userId: 'current-user',
          certificationName: 'AWS Solutions Architect Associate',
          acquiredDate: '2023-06-15',
          expiryDate: '2026-06-15',
          score: '850',
          remarks: 'クラウドアーキテクチャ設計の基礎知識',
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString()
        }
      ];
    }
  },

  // 資格作成
  async createCertification(certificationData: CertificationFormData, userId?: string): Promise<Certification> {
    try {
      const endpoint = '/certifications';
      
      const requestData = {
        ...certificationData,
        userId: userId || 'current-user'
      };
      
      return await apiRequest<Certification>(endpoint, {
        method: 'POST',
        body: JSON.stringify(requestData),
      });
    } catch (error) {
      console.warn('資格作成API呼び出しに失敗しました。モックデータを返します:', error);
      
      return {
        id: Date.now().toString(),
        userId: 'current-user',
        certificationName: certificationData.certificationName,
        acquiredDate: certificationData.acquiredDate,
        expiryDate: certificationData.expiryDate || '',
        score: certificationData.score || '',
        remarks: certificationData.remarks || '',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };
    }
  },

  // 資格更新
  async updateCertification(id: string, certificationData: CertificationFormData): Promise<Certification> {
    try {
      return await apiRequest<Certification>(`/certifications/${id}`, {
        method: 'PUT',
        body: JSON.stringify(certificationData),
      });
    } catch (error) {
      console.warn('資格更新API呼び出しに失敗しました。モックデータを返します:', error);
      
      return {
        id,
        userId: 'current-user',
        certificationName: certificationData.certificationName,
        acquiredDate: certificationData.acquiredDate,
        expiryDate: certificationData.expiryDate || '',
        score: certificationData.score || '',
        remarks: certificationData.remarks || '',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };
    }
  },

  // 資格削除
  async deleteCertification(id: string): Promise<void> {
    try {
      await apiRequest<void>(`/certifications/${id}`, {
        method: 'DELETE',
      });
    } catch (error) {
      console.warn('資格削除API呼び出しに失敗しました:', error);
      // モックでは何もしない
    }
  },

  // 資格マスタ取得
  async getCertificationMasters(): Promise<CertificationMaster[]> {
    try {
      return await apiRequest<CertificationMaster[]>('/certifications/master');
    } catch (error) {
      console.warn('資格マスタAPI呼び出しに失敗しました。モックデータを返します:', error);
      
      return [
        {
          id: 'aws-saa',
          name: 'AWS Solutions Architect Associate',
          organizationName: 'Amazon Web Services',
          category: 'クラウド',
          description: 'AWSクラウドアーキテクチャ設計の基礎資格',
          isActive: true
        },
        {
          id: 'aws-sap',
          name: 'AWS Solutions Architect Professional',
          organizationName: 'Amazon Web Services',
          category: 'クラウド',
          description: 'AWSクラウドアーキテクチャ設計の上級資格',
          isActive: true
        }
      ];
    }
  }
};

// 統合API（useSkillsフックで使用）
export const skillsApi = {
  ...userSkillApi,
  ...skillMasterApi,
  ...skillSearchApi,
  ...certificationApi
};

// エラーハンドリング関数
export function handleApiError(error: unknown): string {
  if (error instanceof Error) {
    if (error.message.includes('API_ERROR')) {
      return 'APIエラーが発生しました。しばらく時間をおいて再度お試しください。';
    }
    return error.message;
  }
  return '予期しないエラーが発生しました。';
}

// デフォルトエクスポート
export default skillsApi;
