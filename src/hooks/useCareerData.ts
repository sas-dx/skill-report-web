/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: キャリア初期データ取得カスタムフック
 */

import { useState, useEffect, useCallback } from 'react';
import { 
  CareerInitResponse, 
  CareerGoalData, 
  SkillCategory, 
  Position,
  LoadingState 
} from '@/types/career';

/**
 * キャリア初期データ取得フックの戻り値型
 */
interface UseCareerDataReturn extends LoadingState {
  careerGoal: CareerGoalData | null;
  skillCategories: SkillCategory[];
  positions: Position[];
  refetch: () => Promise<void>;
}

/**
 * キャリア初期データ取得カスタムフック
 * API-700: キャリア初期データ取得APIを呼び出し、初期表示に必要なデータを取得する
 * 
 * @param userId - ユーザーID（オプション、未指定時はヘッダーから取得）
 * @returns キャリア初期データとローディング状態
 */
export function useCareerData(userId?: string): UseCareerDataReturn {
  const [careerGoal, setCareerGoal] = useState<CareerGoalData | null>(null);
  const [skillCategories, setSkillCategories] = useState<SkillCategory[]>([]);
  const [positions, setPositions] = useState<Position[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  /**
   * キャリア初期データを取得する関数
   */
  const fetchCareerData = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);

      // API-700: キャリア初期データ取得API呼び出し
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      // ユーザーIDが指定されている場合はヘッダーに追加
      if (userId) {
        headers['x-user-id'] = userId;
      }

      const response = await fetch('/api/career/init', {
        method: 'GET',
        headers,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: CareerInitResponse = await response.json();

      if (!data.success || !data.data) {
        throw new Error(data.error?.message || 'データの取得に失敗しました');
      }

      // 取得したデータを状態に設定
      setCareerGoal(data.data.career_goal);
      setSkillCategories(data.data.skill_categories);
      setPositions(data.data.positions);

    } catch (err) {
      console.error('キャリア初期データ取得エラー:', err);
      setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
    } finally {
      setIsLoading(false);
    }
  }, [userId]);

  /**
   * コンポーネントマウント時にデータを取得
   */
  useEffect(() => {
    fetchCareerData();
  }, [fetchCareerData]);

  return {
    careerGoal,
    skillCategories,
    positions,
    isLoading,
    error,
    refetch: fetchCareerData,
  };
}

/**
 * スキルカテゴリのみを取得するフック
 */
export function useSkillCategories(): {
  skillCategories: SkillCategory[];
  isLoading: boolean;
  error: string | null;
} {
  const { skillCategories, isLoading, error } = useCareerData();
  
  return {
    skillCategories,
    isLoading,
    error,
  };
}

/**
 * ポジションのみを取得するフック
 */
export function usePositions(): {
  positions: Position[];
  isLoading: boolean;
  error: string | null;
} {
  const { positions, isLoading, error } = useCareerData();
  
  return {
    positions,
    isLoading,
    error,
  };
}

/**
 * キャリア目標のみを取得するフック
 */
export function useCareerGoal(userId?: string): {
  careerGoal: CareerGoalData | null;
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
} {
  const { careerGoal, isLoading, error, refetch } = useCareerData(userId);
  
  return {
    careerGoal,
    isLoading,
    error,
    refetch,
  };
}
