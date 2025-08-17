/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: キャリア目標一覧取得カスタムフック
 */

import { useState, useEffect, useCallback } from 'react';
import { CareerGoal } from '@/types/career';

/**
 * キャリア目標一覧取得フックの戻り値型
 */
interface UseCareerGoalsListReturn {
  goals: CareerGoal[];
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

/**
 * キャリア目標一覧取得カスタムフック
 * 
 * @param userId - ユーザーID
 * @param year - 対象年度
 * @returns キャリア目標一覧とローディング状態
 */
export function useCareerGoalsList(userId?: string, year?: number): UseCareerGoalsListReturn {
  const [goals, setGoals] = useState<CareerGoal[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * キャリア目標一覧を取得
   */
  const fetchGoals = useCallback(async () => {
    if (!userId) return;
    
    try {
      setIsLoading(true);
      setError(null);

      const token = localStorage.getItem('token');
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      // URLパラメータを構築
      const params = new URLSearchParams();
      if (year) {
        params.append('year', year.toString());
      }

      const queryString = params.toString();
      const url = `/api/career-goals/${userId}${queryString ? `?${queryString}` : ''}`;

      console.log('Fetching goals from:', url);

      const response = await fetch(url, {
        method: 'GET',
        headers,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Goals API response:', data);

      if (data.success && data.data?.goals) {
        // APIレスポンスからCareerGoal型に変換
        const convertedGoals: CareerGoal[] = data.data.goals.map((goal: any) => ({
          id: goal.id,
          goal_id: goal.goal_id,
          user_id: userId,
          title: goal.title,
          description: goal.description,
          goal_type: goal.goal_type,
          status: goal.status,
          priority: goal.priority,
          progress_percentage: goal.progress_rate || 0,
          target_date: goal.target_date,
          created_at: goal.created_at,
          updated_at: goal.updated_at,
        }));
        
        setGoals(convertedGoals);
      } else {
        setGoals([]);
      }

    } catch (err) {
      console.error('キャリア目標一覧取得エラー:', err);
      setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
      setGoals([]);
    } finally {
      setIsLoading(false);
    }
  }, [userId, year]);

  // 初回レンダリング時とパラメータ変更時にデータを取得
  useEffect(() => {
    fetchGoals();
  }, [fetchGoals]);

  return {
    goals,
    isLoading,
    error,
    refetch: fetchGoals,
  };
}