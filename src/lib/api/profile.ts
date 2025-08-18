/**
 * 要求仕様ID: PRO.1-BASE.1
 * 対応設計書: docs/design/api/specs/API定義書_API-011_プロフィール取得API.md
 * 実装内容: プロフィールAPI クライアント関数
 */

// プロフィール情報の型定義
export interface ProfileData {
  id: string;
  email: string;
  employeeId: string;
  personalInfo: {
    lastName: string;
    firstName: string;
    lastNameKana: string;
    firstNameKana: string;
    displayName: string;
    phoneNumber: string;
    emergencyContact: {
      name: string;
      relationship: string;
      phoneNumber: string;
    };
  };
  organizationInfo: {
    tenantId: string;
    tenantName: string;
    departmentId: string;
    departmentName: string;
    divisionId: string;
    divisionName: string;
    positionId: string;
    positionName: string;
    employmentType: string;
    hireDate: string;
    managerUserId: string;
    managerName: string;
  };
  workInfo: {
    workLocation: string;
    workStyle: string;
    contractHours: number;
    overtimeAllowed: boolean;
    remoteWorkAllowed: boolean;
    flexTimeAllowed: boolean;
  };
  systemInfo: {
    status: string;
    role: string;
    permissions: string[];
    lastLoginAt: string;
    createdAt: string;
    updatedAt: string;
  };
  preferences: {
    language: string;
    timezone: string;
    dateFormat: string;
    notifications: {
      email: boolean;
      inApp: boolean;
      skillExpiry: boolean;
      goalReminder: boolean;
    };
    privacy: {
      profileVisibility: string;
      skillVisibility: string;
      goalVisibility: string;
    };
  };
}

export interface SkillSummary {
  totalSkills: number;
  skillsByCategory: {
    technical: number;
    business: number;
    management: number;
  };
  skillsByLevel: {
    '×': number;
    '△': number;
    '○': number;
    '◎': number;
  };
  topSkills: Array<{
    skillId: string;
    skillName: string;
    level: string;
    categoryName: string;
  }>;
  certifications: {
    total: number;
    active: number;
    expiringSoon: number;
  };
  lastUpdated: string;
}

export interface GoalSummary {
  currentGoals: number;
  completedGoals: number;
  overallProgress: number;
  goalsByStatus: {
    not_started: number;
    in_progress: number;
    completed: number;
    on_hold: number;
  };
  upcomingDeadlines: Array<{
    goalId: string;
    goalTitle: string;
    deadline: string;
    progress: number;
    daysRemaining: number;
  }>;
  lastUpdated: string;
}

export interface ProfileResponse {
  success: boolean;
  data?: {
    profile: ProfileData;
    skillSummary?: SkillSummary;
    goalSummary?: GoalSummary;
    updateHistory?: Array<{
      id: string;
      fieldName: string;
      previousValue: string;
      newValue: string;
      changeReason: string;
      updatedBy: string;
      updatedByName: string;
      updatedAt: string;
      approvedBy: string;
      approvedByName: string;
      approvedAt: string;
    }>;
  };
  error?: {
    code: string;
    message: string;
    details?: string;
  };
}

export interface ProfileUpdateRequest {
  first_name?: string;
  last_name?: string;
  first_name_kana?: string;
  last_name_kana?: string;
  display_name?: string;
  email?: string;
  contact_info?: {
    phone?: string;
    emergency_contact?: {
      name?: string;
      phone?: string;
    };
  };
  organization_info?: {
    department_id?: string;
    position_id?: string;
  };
}

export interface ProfileUpdateResponse {
  success: boolean;
  data?: {
    user_id: string;
    username: string;
    email: string;
    display_name: string;
    first_name: string;
    last_name: string;
    first_name_kana: string;
    last_name_kana: string;
    employee_id: string;
    department: {
      department_id: string;
      name: string;
      code: string;
      parent_id: string;
    };
    position: {
      position_id: string;
      name: string;
      level: number;
      is_manager: boolean;
    };
    join_date: string;
    profile_image: string;
    contact_info: {
      phone: string;
      extension: string;
      mobile: string;
      emergency_contact: string;
      address: {
        postal_code: string;
        prefecture: string;
        city: string;
        street_address: string;
      };
    };
    updated_by: string;
    updated_at: string;
    change_summary: {
      updated_fields: string[];
      profile_image_changed: boolean;
      skills_changed: boolean;
    };
  };
  error?: {
    code: string;
    message: string;
    details?: string;
    invalid_fields?: Array<{
      field: string;
      reason: string;
    }>;
  };
}

// 共通のAPIレスポンス型
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: string;
  };
}

/**
 * プロフィール情報を取得する
 * @param userId ユーザーID（"me"で現在のユーザー）
 * @param options オプション
 * @returns プロフィール情報
 */
export async function getProfile(
  userId: string = 'me',
  options: {
    includeHistory?: boolean;
    includeSkillSummary?: boolean;
    includeGoalSummary?: boolean;
  } = {}
): Promise<ProfileResponse> {
  try {
    const params = new URLSearchParams();
    if (options.includeHistory) params.append('includeHistory', 'true');
    if (options.includeSkillSummary) params.append('includeSkillSummary', 'true');
    if (options.includeGoalSummary) params.append('includeGoalSummary', 'true');

    const queryString = params.toString();
    const url = `/api/profiles/${userId}${queryString ? `?${queryString}` : ''}`;

    // 認証トークンを取得
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
      },
      credentials: 'include',
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error?.message || 'プロフィール取得に失敗しました');
    }

    return data;
  } catch (error) {
    console.error('Profile fetch error:', error);
    return {
      success: false,
      error: {
        code: 'FETCH_ERROR',
        message: error instanceof Error ? error.message : 'プロフィール取得に失敗しました'
      }
    };
  }
}

/**
 * プロフィール情報を更新する
 * @param userId ユーザーID（"me"で現在のユーザー）
 * @param updateData 更新データ
 * @returns 更新結果
 */
export async function updateProfile(
  userId: string = 'me',
  updateData: ProfileUpdateRequest
): Promise<ProfileUpdateResponse> {
  try {
    // 認証トークンを取得
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    
    const url = userId === 'me' ? '/api/profiles/me' : `/api/profiles/${userId}`;
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
      },
      credentials: 'include',
      body: JSON.stringify(updateData),
    });

    const data = await response.json();

    if (!response.ok) {
      console.error('Profile update API error:', {
        status: response.status,
        statusText: response.statusText,
        errorData: data
      });
      throw new Error(data.error?.message || 'プロフィール更新に失敗しました');
    }

    return data;
  } catch (error) {
    console.error('Profile update error:', error);
    return {
      success: false,
      error: {
        code: 'UPDATE_ERROR',
        message: error instanceof Error ? error.message : 'プロフィール更新に失敗しました'
      }
    };
  }
}

/**
 * プロフィール更新履歴を取得する
 * @param userId ユーザーID（"me"で現在のユーザー）
 * @param options オプション
 * @returns 更新履歴
 */
export async function getProfileHistory(
  userId: string = 'me',
  options: {
    limit?: number;
    offset?: number;
  } = {}
): Promise<{
  success: boolean;
  data?: {
    history: Array<{
      id: string;
      date: string;
      field: string;
      oldValue: string;
      newValue: string;
      updatedBy: string;
      reason: string;
    }>;
    pagination: {
      total: number;
      limit: number;
      offset: number;
      hasMore: boolean;
    };
  };
  error?: {
    code: string;
    message: string;
  };
}> {
  try {
    const params = new URLSearchParams();
    if (options.limit) params.append('limit', options.limit.toString());
    if (options.offset) params.append('offset', options.offset.toString());

    const queryString = params.toString();
    const url = `/api/profiles/${userId}/history${queryString ? `?${queryString}` : ''}`;

    // 認証トークンを取得
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
      },
      credentials: 'include',
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error?.message || 'プロフィール履歴取得に失敗しました');
    }

    return data;
  } catch (error) {
    console.error('Profile history fetch error:', error);
    return {
      success: false,
      error: {
        code: 'FETCH_ERROR',
        message: error instanceof Error ? error.message : 'プロフィール履歴取得に失敗しました'
      }
    };
  }
}

/**
 * ユーザーの上長情報を取得する
 * @param userId ユーザーID（"me"で現在のユーザー）
 * @returns 上長情報
 */
export async function getManagerInfo(
  userId: string = 'me'
): Promise<ApiResponse<{
  employee: {
    id: number;
    employee_code: string;
    full_name: string;
  };
  manager: {
    id: number;
    employee_code: string;
    full_name: string;
    email: string;
    phone: string;
    department_name: string;
    position_name: string;
  } | null;
}>> {
  try {
    const url = `/api/profiles/${userId}/manager`;

    // 認証トークンを取得
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
      },
      credentials: 'include',
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error?.message || '上長情報取得に失敗しました');
    }

    return data;
  } catch (error) {
    console.error('Manager info fetch error:', error);
    return {
      success: false,
      error: {
        code: 'FETCH_ERROR',
        message: error instanceof Error ? error.message : '上長情報取得に失敗しました'
      }
    };
  }
}

/**
 * プロフィール更新履歴を取得する
 * @param userId ユーザーID
 * @param limit 取得件数
 * @returns 更新履歴
 */
export async function getUpdateHistory(
  userId: string,
  limit: number = 50
): Promise<ApiResponse<{
  history: Array<{
    id: string;
    field_name: string;
    old_value: string | null;
    new_value: string | null;
    updated_at: string;
    updated_by_name: string;
  }>;
}>> {
  try {
    const params = new URLSearchParams();
    params.append('limit', limit.toString());

    const url = `/api/profiles/${userId}/history?${params.toString()}`;

    // 認証トークンを取得
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
      },
      credentials: 'include',
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error?.message || '更新履歴取得に失敗しました');
    }

    return data;
  } catch (error) {
    console.error('Update history fetch error:', error);
    return {
      success: false,
      error: {
        code: 'FETCH_ERROR',
        message: error instanceof Error ? error.message : '更新履歴取得に失敗しました'
      }
    };
  }
}
