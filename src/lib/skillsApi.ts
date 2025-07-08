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
  SkillApiError
} from '@/types/skills';

const API_BASE_URL = '/api';

// 共通のfetch関数
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, defaultOptions);
    
    if (!response.ok) {
      const errorData: SkillApiError = await response.json();
      throw new Error(errorData.error?.message || `HTTP ${response.status}`);
    }

    const data: SkillApiResponse<T> = await response.json();
    
    if (!data.success) {
      throw new Error(data.message || 'API request failed');
    }

    return data.data;
  } catch (error) {
    console.error(`API Error [${endpoint}]:`, error);
    throw error;
  }
}

// スキルマスタAPI (API-023)
export const skillMasterApi = {
  // スキル階層取得
  async getHierarchy(category?: string): Promise<SkillHierarchy[]> {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    
    return apiRequest<SkillHierarchy[]>(
      `/skills/master${params.toString() ? `?${params.toString()}` : ''}`
    );
  },

  // スキルマスタ一覧取得
  async getSkills(params?: { category?: string; subcategory?: string }): Promise<SkillMaster[]> {
    const searchParams = new URLSearchParams();
    if (params?.category) searchParams.append('category', params.category);
    if (params?.subcategory) searchParams.append('subcategory', params.subcategory);
    
    return apiRequest<SkillMaster[]>(
      `/skills/master${searchParams.toString() ? `?${searchParams.toString()}` : ''}`
    );
  }
};

// ユーザースキルAPI (API-021, API-022)
export const userSkillApi = {
  // ユーザースキル取得
  async getUserSkills(userId?: string): Promise<UserSkill[]> {
    const endpoint = userId ? `/skills/${userId}` : '/skills';
    return apiRequest<UserSkill[]>(endpoint);
  },

  // 特定スキル取得
  async getSkill(skillId: string, userId?: string): Promise<UserSkill> {
    const endpoint = userId ? `/skills/${userId}` : '/skills';
    const params = new URLSearchParams({ skillId });
    return apiRequest<UserSkill>(`${endpoint}?${params.toString()}`);
  },

  // スキル情報更新
  async updateSkill(skillData: SkillFormData, userId?: string): Promise<UserSkill> {
    const endpoint = userId ? `/skills/${userId}` : '/skills';
    return apiRequest<UserSkill>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(skillData),
    });
  },

  // スキル情報作成
  async createSkill(skillData: SkillFormData, userId?: string): Promise<UserSkill> {
    const endpoint = userId ? `/skills/${userId}` : '/skills';
    return apiRequest<UserSkill>(endpoint, {
      method: 'POST',
      body: JSON.stringify(skillData),
    });
  },

  // スキル削除
  async deleteSkill(skillId: string, userId?: string): Promise<void> {
    const endpoint = userId ? `/skills/${userId}` : '/skills';
    return apiRequest<void>(endpoint, {
      method: 'DELETE',
      body: JSON.stringify({ skillId }),
    });
  }
};

// スキル検索API (API-030)
export const skillSearchApi = {
  // スキル検索
  async searchSkills(params: SkillSearchParams): Promise<SkillSearchResult> {
    const searchParams = new URLSearchParams();
    
    if (params.keyword) searchParams.append('keyword', params.keyword);
    if (params.category) searchParams.append('category', params.category);
    if (params.subcategory) searchParams.append('subcategory', params.subcategory);
    if (params.level) searchParams.append('level', params.level.toString());
    if (params.hasExperience !== undefined) searchParams.append('hasExperience', params.hasExperience.toString());
    if (params.page) searchParams.append('page', params.page.toString());
    if (params.limit) searchParams.append('limit', params.limit.toString());

    return apiRequest<SkillSearchResult>(`/skills/search?${searchParams.toString()}`);
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
    const searchParams = new URLSearchParams();
    if (params?.department) searchParams.append('department', params.department);
    if (params?.position) searchParams.append('position', params.position);
    if (params?.skills) {
      params.skills.forEach(skill => searchParams.append('skills', skill));
    }
    
    return apiRequest<any>(`/skills/map?${searchParams.toString()}`);
  },

  // スキルマップ条件取得
  async getMapConditions(): Promise<any> {
    return apiRequest<any>('/skills/map/conditions');
  },

  // スキルマップエクスポート
  async exportSkillMap(params: any): Promise<Blob> {
    const response = await fetch(`${API_BASE_URL}/skills/map/export`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
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
