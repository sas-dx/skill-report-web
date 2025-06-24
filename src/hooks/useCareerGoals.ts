/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: キャリア目標管理カスタムフック
 */

import { useState, useCallback } from 'react';
import { 
  CareerGoalUpdateRequest,
  CareerGoalUpdateResponse,
  CareerGoal,
  OperationState 
} from '@/types/career';

/**
 * キャリア目標管理フックの戻り値型
 */
interface UseCareerGoalsReturn extends OperationState {
  updateCareerGoals: (request: CareerGoalUpdateRequest) => Promise<CareerGoalUpdateResponse | null>;
  addCareerGoal: (goal: CareerGoal, year: number) => Promise<CareerGoalUpdateResponse | null>;
  updateCareerGoal: (goal: CareerGoal, year: number) => Promise<CareerGoalUpdateResponse | null>;
  deleteCareerGoal: (goal: CareerGoal, year: number) => Promise<CareerGoalUpdateResponse | null>;
}

/**
 * キャリア目標管理カスタムフック
 * API-701: キャリア目標更新APIを呼び出し、目標の追加・更新・削除を行う
 * 
 * @param userId - ユーザーID（オプション、未指定時はヘッダーから取得）
 * @returns キャリア目標操作関数とローディング状態
 */
export function useCareerGoals(userId?: string): UseCareerGoalsReturn {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSuccess, setIsSuccess] = useState(false);

  /**
   * キャリア目標を更新する共通関数
   */
  const updateCareerGoals = useCallback(async (
    request: CareerGoalUpdateRequest
  ): Promise<CareerGoalUpdateResponse | null> => {
    try {
      setIsLoading(true);
      setError(null);
      setIsSuccess(false);

      // API-701: キャリア目標更新API呼び出し
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      // ユーザーIDが指定されている場合はヘッダーに追加
      if (userId) {
        headers['x-user-id'] = userId;
      }

      const response = await fetch(`/api/career-goals/${userId || 'current'}`, {
        method: 'POST',
        headers,
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: CareerGoalUpdateResponse = await response.json();

      setIsSuccess(true);
      return data;

    } catch (err) {
      console.error('キャリア目標更新エラー:', err);
      setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [userId]);

  /**
   * キャリア目標を追加する
   */
  const addCareerGoal = useCallback(async (
    goal: CareerGoal,
    year: number
  ): Promise<CareerGoalUpdateResponse | null> => {
    const request: CareerGoalUpdateRequest = {
      year,
      operation_type: 'add',
      career_goals: [goal],
    };

    return updateCareerGoals(request);
  }, [updateCareerGoals]);

  /**
   * キャリア目標を更新する
   */
  const updateCareerGoal = useCallback(async (
    goal: CareerGoal,
    year: number
  ): Promise<CareerGoalUpdateResponse | null> => {
    const request: CareerGoalUpdateRequest = {
      year,
      operation_type: 'update',
      career_goals: [goal],
    };

    return updateCareerGoals(request);
  }, [updateCareerGoals]);

  /**
   * キャリア目標を削除する
   */
  const deleteCareerGoal = useCallback(async (
    goal: CareerGoal,
    year: number
  ): Promise<CareerGoalUpdateResponse | null> => {
    const request: CareerGoalUpdateRequest = {
      year,
      operation_type: 'delete',
      career_goals: [goal],
    };

    return updateCareerGoals(request);
  }, [updateCareerGoals]);

  return {
    isLoading,
    error,
    isSuccess,
    updateCareerGoals,
    addCareerGoal,
    updateCareerGoal,
    deleteCareerGoal,
  };
}

/**
 * キャリア目標フォーム用のバリデーションフック
 */
export function useCareerGoalValidation() {
  const [errors, setErrors] = useState<Record<string, string>>({});

  /**
   * キャリア目標をバリデーションする
   */
  const validateCareerGoal = useCallback((goal: Partial<CareerGoal>): boolean => {
    const newErrors: Record<string, string> = {};

    // タイトルの検証
    if (!goal.title?.trim()) {
      newErrors.title = 'タイトルは必須です';
    } else if (goal.title.length > 100) {
      newErrors.title = 'タイトルは100文字以内で入力してください';
    }

    // 説明の検証
    if (goal.description && goal.description.length > 500) {
      newErrors.description = '説明は500文字以内で入力してください';
    }

    // 目標日の検証
    if (!goal.target_date) {
      newErrors.target_date = '目標日は必須です';
    } else {
      const targetDate = new Date(goal.target_date);
      const today = new Date();
      if (targetDate <= today) {
        newErrors.target_date = '目標日は今日より後の日付を設定してください';
      }
    }

    // ステータスの検証
    if (!goal.status) {
      newErrors.status = 'ステータスは必須です';
    }

    // 優先度の検証
    if (goal.priority !== undefined && (goal.priority < 1 || goal.priority > 5)) {
      newErrors.priority = '優先度は1から5の範囲で設定してください';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }, []);

  /**
   * エラーをクリアする
   */
  const clearErrors = useCallback(() => {
    setErrors({});
  }, []);

  /**
   * 特定のフィールドのエラーをクリアする
   */
  const clearFieldError = useCallback((field: string) => {
    setErrors(prev => {
      const newErrors = { ...prev };
      delete newErrors[field];
      return newErrors;
    });
  }, []);

  return {
    errors,
    validateCareerGoal,
    clearErrors,
    clearFieldError,
  };
}

/**
 * アクションプラン管理用のフック
 */
export function useActionPlans() {
  const [actionPlans, setActionPlans] = useState<any[]>([]);

  /**
   * アクションプランを追加する
   */
  const addActionPlan = useCallback((plan: any) => {
    setActionPlans(prev => [...prev, { ...plan, id: Date.now().toString() }]);
  }, []);

  /**
   * アクションプランを更新する
   */
  const updateActionPlan = useCallback((id: string, updates: Partial<any>) => {
    setActionPlans(prev => 
      prev.map(plan => plan.id === id ? { ...plan, ...updates } : plan)
    );
  }, []);

  /**
   * アクションプランを削除する
   */
  const removeActionPlan = useCallback((id: string) => {
    setActionPlans(prev => prev.filter(plan => plan.id !== id));
  }, []);

  /**
   * アクションプランをクリアする
   */
  const clearActionPlans = useCallback(() => {
    setActionPlans([]);
  }, []);

  return {
    actionPlans,
    addActionPlan,
    updateActionPlan,
    removeActionPlan,
    clearActionPlans,
    setActionPlans,
  };
}
