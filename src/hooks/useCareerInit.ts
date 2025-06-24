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
 * キャリア初期データフックの戻り値型
 */
interface UseCareerInitReturn extends LoadingState {
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
 * @param year - 対象年度（オプション、未指定時は現在年度）
 * @returns キャリア初期データとローディング状態
 */
export function useCareerInit(userId?: string, year?: number): UseCareerInitReturn {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [careerGoal, setCareerGoal] = useState<CareerGoalData | null>(null);
  const [skillCategories, setSkillCategories] = useState<SkillCategory[]>([]);
  const [positions, setPositions] = useState<Position[]>([]);

  /**
   * キャリア初期データを取得する
   */
  const fetchCareerInit = useCallback(async () => {
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

      // クエリパラメータの構築
      const params = new URLSearchParams();
      if (year) {
        params.append('year', year.toString());
      }

      const queryString = params.toString();
      const url = `/api/career/init${queryString ? `?${queryString}` : ''}`;

      const response = await fetch(url, {
        method: 'GET',
        headers,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: CareerInitResponse = await response.json();

      if (data.success && data.data) {
        setCareerGoal(data.data.career_goal);
        setSkillCategories(data.data.skill_categories);
        setPositions(data.data.positions);
      } else {
        throw new Error(data.error?.message || 'データの取得に失敗しました');
      }

    } catch (err) {
      console.error('キャリア初期データ取得エラー:', err);
      setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
      
      // エラー時は空のデータを設定
      setCareerGoal(null);
      setSkillCategories([]);
      setPositions([]);
    } finally {
      setIsLoading(false);
    }
  }, [userId, year]);

  /**
   * データを再取得する
   */
  const refetch = useCallback(async () => {
    await fetchCareerInit();
  }, [fetchCareerInit]);

  // 初回マウント時にデータを取得
  useEffect(() => {
    fetchCareerInit();
  }, [fetchCareerInit]);

  return {
    isLoading,
    error,
    careerGoal,
    skillCategories,
    positions,
    refetch,
  };
}

/**
 * キャリア目標フォーム用の初期値生成フック
 */
export function useCareerGoalDefaults() {
  /**
   * 新しいキャリア目標の初期値を生成する
   */
  const createDefaultCareerGoal = useCallback(() => {
    const currentDate = new Date();
    const nextYear = new Date(currentDate.getFullYear() + 1, currentDate.getMonth(), currentDate.getDate());

    return {
      target_position: '',
      target_date: nextYear.toISOString().split('T')[0], // YYYY-MM-DD形式
      target_description: '',
      current_level: '1',
      target_level: '2',
      progress_percentage: 0,
      plan_status: 'not_started',
    } as const;
  }, []);

  /**
   * 既存のキャリア目標から編集用の初期値を生成する
   */
  const createEditCareerGoal = useCallback((goal: CareerGoalData) => {
    return {
      ...goal,
      // 日付フィールドの正規化
      target_date: goal.target_date.split('T')[0],
      last_review_date: goal.last_review_date ? goal.last_review_date.split('T')[0] : null,
      next_review_date: goal.next_review_date ? goal.next_review_date.split('T')[0] : null,
    };
  }, []);

  return {
    createDefaultCareerGoal,
    createEditCareerGoal,
  };
}

/**
 * スキルカテゴリ操作用のフック
 */
export function useSkillCategories(categories: SkillCategory[]) {
  /**
   * 階層構造でスキルカテゴリを取得する
   */
  const getHierarchicalCategories = useCallback(() => {
    const categoryMap = new Map<string, SkillCategory & { children: SkillCategory[] }>();
    
    // 全カテゴリをマップに追加
    categories.forEach(category => {
      categoryMap.set(category.id, { ...category, children: [] });
    });

    // 親子関係を構築
    const rootCategories: (SkillCategory & { children: SkillCategory[] })[] = [];
    
    categories.forEach(category => {
      const categoryWithChildren = categoryMap.get(category.id);
      if (!categoryWithChildren) return;

      if (category.parent_id && categoryMap.has(category.parent_id)) {
        const parent = categoryMap.get(category.parent_id);
        parent?.children.push(categoryWithChildren);
      } else {
        rootCategories.push(categoryWithChildren);
      }
    });

    return rootCategories;
  }, [categories]);

  /**
   * 特定レベルのカテゴリを取得する
   */
  const getCategoriesByLevel = useCallback((level: number) => {
    return categories.filter(category => category.level === level);
  }, [categories]);

  /**
   * 特定タイプのカテゴリを取得する
   */
  const getCategoriesByType = useCallback((type: string) => {
    return categories.filter(category => category.type === type);
  }, [categories]);

  /**
   * カテゴリIDからカテゴリ情報を取得する
   */
  const getCategoryById = useCallback((id: string) => {
    return categories.find(category => category.id === id);
  }, [categories]);

  return {
    getHierarchicalCategories,
    getCategoriesByLevel,
    getCategoriesByType,
    getCategoryById,
  };
}

/**
 * ポジション操作用のフック
 */
export function usePositions(positions: Position[]) {
  /**
   * レベル順でソートされたポジションを取得する
   */
  const getSortedPositions = useCallback(() => {
    return [...positions].sort((a, b) => a.level - b.level);
  }, [positions]);

  /**
   * 管理職ポジションを取得する
   */
  const getManagementPositions = useCallback(() => {
    return positions.filter(position => position.is_management);
  }, [positions]);

  /**
   * 役員ポジションを取得する
   */
  const getExecutivePositions = useCallback(() => {
    return positions.filter(position => position.is_executive);
  }, [positions]);

  /**
   * カテゴリ別ポジションを取得する
   */
  const getPositionsByCategory = useCallback((category: string) => {
    return positions.filter(position => position.category === category);
  }, [positions]);

  /**
   * ポジションIDからポジション情報を取得する
   */
  const getPositionById = useCallback((id: string) => {
    return positions.find(position => position.id === id);
  }, [positions]);

  /**
   * 現在のポジションより上位のポジションを取得する
   */
  const getHigherPositions = useCallback((currentLevel: number) => {
    return positions.filter(position => position.level > currentLevel);
  }, [positions]);

  return {
    getSortedPositions,
    getManagementPositions,
    getExecutivePositions,
    getPositionsByCategory,
    getPositionById,
    getHigherPositions,
  };
}
