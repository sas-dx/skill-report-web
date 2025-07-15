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

// スキルマスタAPI (API-023)
export const skillMasterApi = {
  // スキル階層取得
  async getHierarchy(category?: string): Promise<SkillHierarchy[]> {
    try {
      const params = new URLSearchParams();
      if (category) params.append('category', category);
      
      const apiResponse = await apiRequest<any[]>(
        `/skills/master${params.toString() ? `?${params.toString()}` : ''}`
      );
      
      // APIレスポンスをSkillHierarchy形式に変換
      const hierarchyData: SkillHierarchy[] = apiResponse.map(categoryData => ({
        id: categoryData.category_id || categoryData.category_code,
        name: categoryData.category_name,
        category: categoryData.category_name,
        level: 1,
        description: categoryData.description || '',
        children: categoryData.skills?.map((skill: any) => ({
          id: skill.skill_id || skill.skill_code,
          name: skill.skill_name,
          category: categoryData.category_name,
          subcategory: categoryData.category_name,
          parentId: categoryData.category_id || categoryData.category_code,
          level: 2,
          description: skill.description || ''
        })) || []
      }));
      
      return hierarchyData;
    } catch (error) {
      console.warn('スキル階層API呼び出しに失敗しました。モックデータを返します:', error);
      
      // モックデータを返す
      return [
        {
          id: 'frontend',
          name: 'フロントエンド',
          category: 'フロントエンド',
          level: 1,
          description: 'フロントエンド開発技術',
          children: [
            {
              id: 'javascript',
              name: 'JavaScript',
              category: 'フロントエンド',
              subcategory: 'フロントエンド',
              parentId: 'frontend',
              level: 2,
              description: 'JavaScript プログラミング言語'
            },
            {
              id: 'typescript',
              name: 'TypeScript',
              category: 'フロントエンド',
              subcategory: 'フロントエンド',
              parentId: 'frontend',
              level: 2,
              description: 'TypeScript プログラミング言語'
            },
            {
              id: 'react',
              name: 'React',
              category: 'フロントエンド',
              subcategory: 'フロントエンド',
              parentId: 'frontend',
              level: 2,
              description: 'React フレームワーク'
            }
          ]
        },
        {
          id: 'backend',
          name: 'バックエンド',
          category: 'バックエンド',
          level: 1,
          description: 'バックエンド開発技術',
          children: [
            {
              id: 'nodejs',
              name: 'Node.js',
              category: 'バックエンド',
              subcategory: 'バックエンド',
              parentId: 'backend',
              level: 2,
              description: 'Node.js ランタイム環境'
            },
            {
              id: 'python',
              name: 'Python',
              category: 'バックエンド',
              subcategory: 'バックエンド',
              parentId: 'backend',
              level: 2,
              description: 'Python プログラミング言語'
            }
          ]
        },
        {
          id: 'database',
          name: 'データベース',
          category: 'データベース',
          level: 1,
          description: 'データベース技術',
          children: [
            {
              id: 'postgresql',
              name: 'PostgreSQL',
              category: 'データベース',
              subcategory: 'データベース',
              parentId: 'database',
              level: 2,
              description: 'PostgreSQL データベース'
            },
            {
              id: 'mysql',
              name: 'MySQL',
              category: 'データベース',
              subcategory: 'データベース',
              parentId: 'database',
              level: 2,
              description: 'MySQL データベース'
            }
          ]
        }
      ];
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
    const endpoint = userId ? `/skills/${userId}` : '/skills';
    const params = new URLSearchParams({ skillId });
    const skillResponse = await apiRequest<any>(`${endpoint}?${params.toString()}`);
    return convertSkillResponseToUserSkill(skillResponse);
  },

  // スキル情報更新
  async updateSkill(skillData: SkillFormData, userId?: string): Promise<UserSkill> {
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
  },

  // スキル情報作成
  async createSkill(skillData: SkillFormData, userId?: string): Promise<UserSkill> {
    const endpoint = userId ? `/skills/${userId}` : '/skills';
    
    // APIが期待する形式に変換
    const requestData = {
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
    };
    
    const skillResponse = await apiRequest<any>(endpoint, {
      method: 'POST',
      body: JSON.stringify(requestData),
    });
    
    return convertSkillResponseToUserSkill(skillResponse);
  },

  // スキル削除
  async deleteSkill(skillId: string, userId?: string): Promise<void> {
    const endpoint = userId ? `/skills/${userId}` : '/skills';
    await apiRequest<void>(endpoint, {
      method: 'DELETE',
      body: JSON.stringify({ skillId }),
    });
  }
};

// スキル検索API (API-030)
export const skillSearchApi = {
  // スキル検索
  async searchSkills(params: SkillSearchParams): Promise<SkillSearchResult> {
    try {
      const searchParams = new URLSearchParams();
      
      if (params.keyword) searchParams.append('keyword', params.keyword);
      if (params.category) searchParams.append('category', params.category);
      if (params.subcategory) searchParams.append('subcategory', params.subcategory);
      if (params.level) searchParams.append('level', params.level.toString());
      if (params.hasExperience !== undefined) searchParams.append('hasExperience', params.hasExperience.toString());
      if (params.page) searchParams.append('page', params.page.toString());
      if (params.limit) searchParams.append('limit', params.limit.toString());

      // APIレスポンスを直接取得（SkillApiResponse形式ではない）
      const url = `/api/skills/search?${searchParams.toString()}`;
      const authHeaders = getAuthHeaders();
      
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...authHeaders,
        },
      });

      if (!response.ok) {
        throw new Error(`API_ERROR: ${response.status}`);
      }

      const apiResponse = await response.json();
      
      if (!apiResponse.success) {
        throw new Error(apiResponse.error?.message || 'API request failed');
      }

      // APIレスポンスの data.results を SkillMaster[] に変換
      const searchResults = apiResponse.data.results.map((result: any) => ({
        id: result.skill_id || result.skill_code,
        name: result.skill_name,
        category: result.category?.category_name || '技術スキル',
        subcategory: result.category?.category_code || undefined,
        description: result.description || '',
        isActive: result.is_active || true,
        sortOrder: 1
      }));

      return {
        skills: searchResults,
        total: apiResponse.data.pagination?.total_count || searchResults.length,
        page: apiResponse.data.pagination?.current_page || 1,
        limit: apiResponse.data.pagination?.limit || 20
      };
    } catch (error) {
      console.warn('スキル検索API呼び出しに失敗しました。モックデータを返します:', error);
      
      // モックデータを返す
      const mockSkills: SkillMaster[] = [
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
        },
        {
          id: 'nodejs',
          name: 'Node.js',
          category: '技術スキル',
          subcategory: 'ランタイム',
          description: 'サーバーサイドJavaScript',
          isActive: true,
          sortOrder: 4
        }
      ];

      // フィルタリング処理
      let filteredSkills = mockSkills;
      
      if (params.keyword) {
        const keyword = params.keyword.toLowerCase();
        filteredSkills = filteredSkills.filter(skill => 
          skill.name.toLowerCase().includes(keyword) ||
          skill.description?.toLowerCase().includes(keyword)
        );
      }
      
      if (params.category) {
        filteredSkills = filteredSkills.filter(skill => skill.category === params.category);
      }
      
      if (params.subcategory) {
        filteredSkills = filteredSkills.filter(skill => skill.subcategory === params.subcategory);
      }

      // ページネーション
      const page = params.page || 1;
      const limit = params.limit || 10;
      const startIndex = (page - 1) * limit;
      const endIndex = startIndex + limit;
      const paginatedSkills = filteredSkills.slice(startIndex, endIndex);

      return {
        skills: paginatedSkills,
        total: filteredSkills.length,
        page,
        limit
      };
    }
  }
};

// 資格マスタAPI (API-009)
export const certificationMasterApi = {
  // 資格マスタ取得
  async getCertifications(params?: { keyword?: string; category?: string }): Promise<CertificationMaster[]> {
    const searchParams = new URLSearchParams();
    if (params?.keyword) searchParams.append('keyword', params.keyword);
    if (params?.category) searchParams.append('category', params.category);
    
    return apiRequest<CertificationMaster[]>(
      `/certifications/master${searchParams.toString() ? `?${searchParams.toString()}` : ''}`
    );
  }
};

// ユーザー資格API (API-010)
export const userCertificationApi = {
  // ユーザー資格取得
  async getUserCertifications(userId?: string): Promise<Certification[]> {
    const endpoint = userId ? `/certifications/${userId}` : '/certifications';
    return apiRequest<Certification[]>(endpoint);
  },

  // 資格情報作成
  async createCertification(certData: CertificationFormData, userId?: string): Promise<Certification> {
    const endpoint = userId ? `/certifications/${userId}` : '/certifications';
    return apiRequest<Certification>(endpoint, {
      method: 'POST',
      body: JSON.stringify(certData),
    });
  },

  // 資格情報更新
  async updateCertification(certId: string, certData: CertificationFormData, userId?: string): Promise<Certification> {
    const endpoint = userId ? `/certifications/${userId}` : '/certifications';
    return apiRequest<Certification>(endpoint, {
      method: 'PUT',
      body: JSON.stringify({ id: certId, ...certData }),
    });
  },

  // 資格削除
  async deleteCertification(certId: string, userId?: string): Promise<void> {
    const endpoint = userId ? `/certifications/${userId}` : '/certifications';
    return apiRequest<void>(endpoint, {
      method: 'DELETE',
      body: JSON.stringify({ id: certId }),
    });
  }
};

// スキルマップAPI (API-026)
export const skillMapApi = {
  // スキルマップデータ取得
  async getSkillMapData(params?: {
    department?: string;
    position?: string;
    skills?: string[];
  }): Promise<any> {
    try {
      const searchParams = new URLSearchParams();
      if (params?.department) searchParams.append('department', params.department);
      if (params?.position) searchParams.append('position', params.position);
      if (params?.skills) {
        params.skills.forEach(skill => searchParams.append('skills', skill));
      }
      
      return await apiRequest<any>(`/skills/map?${searchParams.toString()}`);
    } catch (error) {
      console.warn('スキルマップAPI呼び出しに失敗しました。モックデータを返します:', error);
      
      // モックデータを返す
      return {
        users: [
          {
            id: 'user1',
            name: '山田太郎',
            department: '開発部',
            position: 'シニアエンジニア',
            skills: [
              { skillId: 'javascript', skillName: 'JavaScript', level: 4 },
              { skillId: 'typescript', skillName: 'TypeScript', level: 3 },
              { skillId: 'react', skillName: 'React', level: 4 }
            ]
          },
          {
            id: 'user2',
            name: '佐藤花子',
            department: '開発部',
            position: 'エンジニア',
            skills: [
              { skillId: 'javascript', skillName: 'JavaScript', level: 3 },
              { skillId: 'typescript', skillName: 'TypeScript', level: 2 },
              { skillId: 'react', skillName: 'React', level: 3 }
            ]
          }
        ],
        skillSummary: {
          javascript: { total: 2, levels: { 1: 0, 2: 0, 3: 1, 4: 1 } },
          typescript: { total: 2, levels: { 1: 0, 2: 1, 3: 1, 4: 0 } },
          react: { total: 2, levels: { 1: 0, 2: 0, 3: 1, 4: 1 } }
        }
      };
    }
  },

  // スキルマップ条件取得
  async getMapConditions(): Promise<any> {
    try {
      return await apiRequest<any>('/skills/map/conditions');
    } catch (error) {
      console.warn('スキルマップ条件API呼び出しに失敗しました。モックデータを返します:', error);
      
      // モックデータを返す
      return {
        departments: [
          { id: 'dev', name: '開発部' },
          { id: 'sales', name: '営業部' },
          { id: 'hr', name: '人事部' }
        ],
        positions: [
          { id: 'senior', name: 'シニアエンジニア' },
          { id: 'engineer', name: 'エンジニア' },
          { id: 'junior', name: 'ジュニアエンジニア' }
        ],
        skills: [
          { id: 'javascript', name: 'JavaScript', category: '技術スキル' },
          { id: 'typescript', name: 'TypeScript', category: '技術スキル' },
          { id: 'react', name: 'React', category: '技術スキル' },
          { id: 'nodejs', name: 'Node.js', category: '技術スキル' }
        ]
      };
    }
  },

  // スキルマップエクスポート
  async exportSkillMap(params: any): Promise<Blob> {
    const authHeaders = getAuthHeaders();
    
    const response = await fetch(`${API_BASE_URL}/skills/map/export`, {
      method: 'POST',
      headers: {
        ...authHeaders,
      },
      body: JSON.stringify(params),
    });

    if (!response.ok) {
      throw new Error(`Export failed: ${response.status}`);
    }

    return response.blob();
  }
};

// エラーハンドリング用ユーティリティ
export const handleApiError = (error: unknown): string => {
  if (error instanceof Error) {
    return error.message;
  }
  return 'An unexpected error occurred';
};

// ローディング状態管理用ユーティリティ
export const createLoadingState = () => {
  let loadingCount = 0;
  
  return {
    start: () => ++loadingCount > 0,
    end: () => --loadingCount > 0,
    isLoading: () => loadingCount > 0
  };
};
