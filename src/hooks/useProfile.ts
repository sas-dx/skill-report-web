/**
 * 要求仕様ID: PRO.1-BASE.1
 * 対応設計書: docs/design/api/specs/API定義書_API-011_プロフィール取得API.md
 * プロフィール情報取得カスタムフック
 */
'use client';

import { useState, useEffect } from 'react';

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
}

interface UseProfileReturn {
  profile: ProfileData | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export const useProfile = (): UseProfileReturn => {
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('認証トークンが見つかりません');
      }

      const response = await fetch('/api/profiles/me?includeSkillSummary=true', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('認証が必要です');
        }
        if (response.status === 404) {
          throw new Error('プロフィール情報が見つかりません');
        }
        throw new Error(`プロフィール取得に失敗しました: ${response.status}`);
      }

      const data = await response.json();
      
      if (!data.success) {
        throw new Error(data.error?.message || 'プロフィール取得に失敗しました');
      }

      // APIレスポンス構造に合わせて修正: data.data.profile
      setProfile(data.data.profile);
    } catch (err) {
      console.error('プロフィール取得エラー:', err);
      setError(err instanceof Error ? err.message : 'プロフィール取得に失敗しました');
      setProfile(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  return {
    profile,
    loading,
    error,
    refetch: fetchProfile,
  };
};
