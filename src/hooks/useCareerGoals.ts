/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: キャリア目標操作カスタムフック
 */

import { useState, useCallback } from 'react';
import { CareerGoal } from '@/types/career';

/**
 * キャリア目標操作フックの戻り値型
 */
interface UseCareerGoalsReturn {
  addCareerGoal: (goal: CareerGoal, year: number) => Promise<void>;
  updateCareerGoal: (goal: CareerGoal, year: number) => Promise<void>;
  deleteCareerGoal: (goal: CareerGoal, year: number) => Promise<void>;
  isLoading: boolean;
  error: string | null;
  isSuccess: boolean;
}

/**
 * キャリア目標操作カスタムフック
 * 
 * @param userId - ユーザーID（オプション）
 * @returns キャリア目標操作関数とローディング状態
 */
export function useCareerGoals(userId?: string): UseCareerGoalsReturn {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSuccess, setIsSuccess] = useState(false);

  /**
   * キャリア目標追加
   */
  const addCareerGoal = useCallback(async (goal: CareerGoal, year: number) => {
    try {
      setIsLoading(true);
      setError(null);
      setIsSuccess(false);

      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      if (userId) {
        headers['x-user-id'] = userId;
      }

      // バックエンドが期待するCreateCareerGoalData形式に変換
      const createData = {
        title: goal.title,
        description: goal.description,
        goal_type: goal.goal_type, // フォームから送信された値を使用
        target_date: goal.target_date,
        status: goal.status,
        priority: goal.priority,
        progress_percentage: goal.progress_percentage,
      };

      // デバッグ用ログ追加
      console.log('=== useCareerGoals addCareerGoal デバッグ ===');
      console.log('元のgoal:', goal);
      console.log('送信するcreateData:', createData);
      console.log('goal_type:', createData.goal_type, 'typeof:', typeof createData.goal_type);

      const response = await fetch(`/api/career-goals/${userId || 'current'}`, {
        method: 'POST',
        headers,
        body: JSON.stringify(createData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error?.message || 'キャリア目標の追加に失敗しました');
      }

      setIsSuccess(true);
    } catch (err) {
      console.error('キャリア目標追加エラー:', err);
      setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
    } finally {
      setIsLoading(false);
    }
  }, [userId]);

  /**
   * キャリア目標更新
   */
  const updateCareerGoal = useCallback(async (goal: CareerGoal, year: number) => {
    try {
      setIsLoading(true);
      setError(null);
      setIsSuccess(false);

      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      if (userId) {
        headers['x-user-id'] = userId;
      }

      // バックエンドが期待するUpdateCareerGoalData形式に変換
      const updateData = {
        goal_id: goal.id,
        title: goal.title,
        description: goal.description,
        goal_type: goal.goal_type, // フォームから送信された値を使用
        target_date: goal.target_date,
        status: goal.status,
        priority: goal.priority,
        progress_percentage: goal.progress_percentage,
      };

      const response = await fetch(`/api/career-goals/${userId || 'current'}`, {
        method: 'PUT',
        headers,
        body: JSON.stringify(updateData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error?.message || 'キャリア目標の更新に失敗しました');
      }

      setIsSuccess(true);
    } catch (err) {
      console.error('キャリア目標更新エラー:', err);
      setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
    } finally {
      setIsLoading(false);
    }
  }, [userId]);

  /**
   * キャリア目標削除
   */
  const deleteCareerGoal = useCallback(async (goal: CareerGoal, year: number) => {
    try {
      setIsLoading(true);
      setError(null);
      setIsSuccess(false);

      console.log('削除対象の目標:', { goal, year, userId });

      // goal_idを取得（複数のフィールドから適切なIDを特定）
      let goalId = goal.id;
      
      // もしgoal.goal_idが存在する場合はそれを優先
      if ('goal_id' in goal && typeof goal.goal_id === 'string' && goal.goal_id) {
        goalId = goal.goal_id;
      }
      
      console.log('使用するgoal_id:', goalId);

      if (!goalId) {
        throw new Error('削除対象の目標IDが特定できません');
      }

      // クエリパラメータでgoal_idを送信
      const url = new URL(`/api/career-goals/${userId || 'current'}`, window.location.origin);
      url.searchParams.set('goal_id', goalId);

      const headers: HeadersInit = {};

      if (userId) {
        headers['x-user-id'] = userId;
      }

      const response = await fetch(url.toString(), {
        method: 'DELETE',
        headers,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error?.message || 'キャリア目標の削除に失敗しました');
      }

      setIsSuccess(true);
    } catch (err) {
      console.error('キャリア目標削除エラー:', err);
      setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
    } finally {
      setIsLoading(false);
    }
  }, [userId]);

  return {
    addCareerGoal,
    updateCareerGoal,
    deleteCareerGoal,
    isLoading,
    error,
    isSuccess,
  };
}
