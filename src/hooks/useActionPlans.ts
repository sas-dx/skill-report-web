/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: アクションプラン管理用カスタムフック
 */

import { useState, useEffect, useCallback } from 'react';
import {
  ActionPlan,
  ActionPlanGetResponse,
  ActionPlanCreateRequest,
  ActionPlanCreateResponse,
  ActionPlanUpdateRequest,
  ActionPlanUpdateResponse,
  ActionPlanDeleteResponse,
  LoadingState,
  OperationState
} from '@/types/career';

// ============================================================================
// カスタムフック: useActionPlans
// ============================================================================

interface UseActionPlansOptions {
  autoFetch?: boolean;
  page?: number;
  limit?: number;
  status?: string;
  priority?: string;
  category?: string;
}

interface UseActionPlansReturn {
  // データ
  actionPlans: ActionPlan[];
  totalCount: number;
  pagination: {
    page: number;
    limit: number;
    total_pages: number;
  } | null;
  
  // 状態
  loading: LoadingState;
  creating: OperationState;
  updating: OperationState;
  deleting: OperationState;
  
  // 操作関数
  fetchActionPlans: (options?: {
    page?: number;
    limit?: number;
    status?: string;
    priority?: string;
    category?: string;
  }) => Promise<void>;
  createActionPlan: (data: ActionPlanCreateRequest) => Promise<ActionPlan | null>;
  updateActionPlan: (id: string, data: ActionPlanUpdateRequest) => Promise<ActionPlan | null>;
  deleteActionPlan: (id: string) => Promise<boolean>;
  refreshActionPlans: () => Promise<void>;
}

export function useActionPlans(options: UseActionPlansOptions = {}): UseActionPlansReturn {
  const {
    autoFetch = true,
    page = 1,
    limit = 20,
    status,
    priority,
    category
  } = options;

  // ============================================================================
  // State管理
  // ============================================================================
  
  const [actionPlans, setActionPlans] = useState<ActionPlan[]>([]);
  const [totalCount, setTotalCount] = useState<number>(0);
  const [pagination, setPagination] = useState<{
    page: number;
    limit: number;
    total_pages: number;
  } | null>(null);

  const [loading, setLoading] = useState<LoadingState>({
    isLoading: false,
    error: null
  });

  const [creating, setCreating] = useState<OperationState>({
    isLoading: false,
    error: null,
    isSuccess: false
  });

  const [updating, setUpdating] = useState<OperationState>({
    isLoading: false,
    error: null,
    isSuccess: false
  });

  const [deleting, setDeleting] = useState<OperationState>({
    isLoading: false,
    error: null,
    isSuccess: false
  });

  // ============================================================================
  // API呼び出し関数
  // ============================================================================

  /**
   * アクションプラン一覧取得 (API-703)
   */
  const fetchActionPlans = useCallback(async (fetchOptions?: {
    page?: number;
    limit?: number;
    status?: string;
    priority?: string;
    category?: string;
  }) => {
    setLoading({ isLoading: true, error: null });

    try {
      const params = new URLSearchParams();
      params.append('page', String(fetchOptions?.page || page));
      params.append('limit', String(fetchOptions?.limit || limit));
      
      if (fetchOptions?.status || status) {
        params.append('status', fetchOptions?.status || status!);
      }
      if (fetchOptions?.priority || priority) {
        params.append('priority', fetchOptions?.priority || priority!);
      }
      if (fetchOptions?.category || category) {
        params.append('category', fetchOptions?.category || category!);
      }

      const response = await fetch(`/api/career/action-plan?${params.toString()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': 'emp_001' // 実際の実装では認証から取得
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result: ActionPlanGetResponse = await response.json();

      if (result.success && result.data) {
        setActionPlans(result.data.action_plans);
        setTotalCount(result.data.total_count);
        setPagination(result.data.pagination || null);
        setLoading({ isLoading: false, error: null });
      } else {
        throw new Error(result.error?.message || 'アクションプランの取得に失敗しました');
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : '不明なエラーが発生しました';
      setLoading({ isLoading: false, error: errorMessage });
      console.error('アクションプラン取得エラー:', error);
    }
  }, [page, limit, status, priority, category]);

  /**
   * アクションプラン作成 (API-706)
   */
  const createActionPlan = useCallback(async (data: ActionPlanCreateRequest): Promise<ActionPlan | null> => {
    setCreating({ isLoading: true, error: null, isSuccess: false });

    try {
      const response = await fetch('/api/career/action-plan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': 'emp_001' // 実際の実装では認証から取得
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result: ActionPlanCreateResponse = await response.json();

      if (result.success && result.data) {
        setCreating({ isLoading: false, error: null, isSuccess: true });
        
        // 作成後にリストを更新
        await fetchActionPlans();
        
        return result.data.action_plan;
      } else {
        throw new Error(result.error?.message || 'アクションプランの作成に失敗しました');
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : '不明なエラーが発生しました';
      setCreating({ isLoading: false, error: errorMessage, isSuccess: false });
      console.error('アクションプラン作成エラー:', error);
      return null;
    }
  }, [fetchActionPlans]);

  /**
   * アクションプラン更新 (API-707)
   */
  const updateActionPlan = useCallback(async (id: string, data: ActionPlanUpdateRequest): Promise<ActionPlan | null> => {
    setUpdating({ isLoading: true, error: null, isSuccess: false });

    try {
      const response = await fetch(`/api/career/action-plan/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': 'emp_001' // 実際の実装では認証から取得
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result: ActionPlanUpdateResponse = await response.json();

      if (result.success && result.data) {
        setUpdating({ isLoading: false, error: null, isSuccess: true });
        
        // 更新後にリストを更新
        await fetchActionPlans();
        
        return result.data.action_plan;
      } else {
        throw new Error(result.error?.message || 'アクションプランの更新に失敗しました');
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : '不明なエラーが発生しました';
      setUpdating({ isLoading: false, error: errorMessage, isSuccess: false });
      console.error('アクションプラン更新エラー:', error);
      return null;
    }
  }, [fetchActionPlans]);

  /**
   * アクションプラン削除 (API-708)
   */
  const deleteActionPlan = useCallback(async (id: string): Promise<boolean> => {
    setDeleting({ isLoading: true, error: null, isSuccess: false });

    try {
      const response = await fetch(`/api/career/action-plan/${id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': 'emp_001' // 実際の実装では認証から取得
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result: ActionPlanDeleteResponse = await response.json();

      if (result.success) {
        setDeleting({ isLoading: false, error: null, isSuccess: true });
        
        // 削除後にリストを更新
        await fetchActionPlans();
        
        return true;
      } else {
        throw new Error(result.error?.message || 'アクションプランの削除に失敗しました');
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : '不明なエラーが発生しました';
      setDeleting({ isLoading: false, error: errorMessage, isSuccess: false });
      console.error('アクションプラン削除エラー:', error);
      return false;
    }
  }, [fetchActionPlans]);

  /**
   * アクションプラン一覧の再取得
   */
  const refreshActionPlans = useCallback(async () => {
    await fetchActionPlans();
  }, [fetchActionPlans]);

  // ============================================================================
  // 初期化処理
  // ============================================================================

  useEffect(() => {
    if (autoFetch) {
      fetchActionPlans();
    }
  }, [autoFetch, fetchActionPlans]);

  // ============================================================================
  // 戻り値
  // ============================================================================

  return {
    // データ
    actionPlans,
    totalCount,
    pagination,
    
    // 状態
    loading,
    creating,
    updating,
    deleting,
    
    // 操作関数
    fetchActionPlans,
    createActionPlan,
    updateActionPlan,
    deleteActionPlan,
    refreshActionPlans
  };
}

// ============================================================================
// 個別アクションプラン管理用フック
// ============================================================================

interface UseActionPlanReturn {
  actionPlan: ActionPlan | null;
  loading: LoadingState;
  updating: OperationState;
  deleting: OperationState;
  
  updateActionPlan: (data: ActionPlanUpdateRequest) => Promise<ActionPlan | null>;
  deleteActionPlan: () => Promise<boolean>;
  refreshActionPlan: () => Promise<void>;
}

export function useActionPlan(actionPlanId: string): UseActionPlanReturn {
  const [actionPlan, setActionPlan] = useState<ActionPlan | null>(null);
  const [loading, setLoading] = useState<LoadingState>({
    isLoading: false,
    error: null
  });
  const [updating, setUpdating] = useState<OperationState>({
    isLoading: false,
    error: null,
    isSuccess: false
  });
  const [deleting, setDeleting] = useState<OperationState>({
    isLoading: false,
    error: null,
    isSuccess: false
  });

  /**
   * 個別アクションプラン取得
   */
  const fetchActionPlan = useCallback(async () => {
    setLoading({ isLoading: true, error: null });

    try {
      // 一覧APIから該当IDのアクションプランを取得
      const response = await fetch('/api/career/action-plan', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': 'emp_001'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result: ActionPlanGetResponse = await response.json();

      if (result.success && result.data) {
        const foundActionPlan = result.data.action_plans.find(ap => ap.action_id === actionPlanId);
        setActionPlan(foundActionPlan || null);
        setLoading({ isLoading: false, error: null });
      } else {
        throw new Error(result.error?.message || 'アクションプランの取得に失敗しました');
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : '不明なエラーが発生しました';
      setLoading({ isLoading: false, error: errorMessage });
      console.error('アクションプラン取得エラー:', error);
    }
  }, [actionPlanId]);

  /**
   * アクションプラン更新
   */
  const updateActionPlan = useCallback(async (data: ActionPlanUpdateRequest): Promise<ActionPlan | null> => {
    setUpdating({ isLoading: true, error: null, isSuccess: false });

    try {
      const response = await fetch(`/api/career/action-plan/${actionPlanId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': 'emp_001'
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result: ActionPlanUpdateResponse = await response.json();

      if (result.success && result.data) {
        setActionPlan(result.data.action_plan);
        setUpdating({ isLoading: false, error: null, isSuccess: true });
        return result.data.action_plan;
      } else {
        throw new Error(result.error?.message || 'アクションプランの更新に失敗しました');
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : '不明なエラーが発生しました';
      setUpdating({ isLoading: false, error: errorMessage, isSuccess: false });
      console.error('アクションプラン更新エラー:', error);
      return null;
    }
  }, [actionPlanId]);

  /**
   * アクションプラン削除
   */
  const deleteActionPlan = useCallback(async (): Promise<boolean> => {
    setDeleting({ isLoading: true, error: null, isSuccess: false });

    try {
      const response = await fetch(`/api/career/action-plan/${actionPlanId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': 'emp_001'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result: ActionPlanDeleteResponse = await response.json();

      if (result.success) {
        setActionPlan(null);
        setDeleting({ isLoading: false, error: null, isSuccess: true });
        return true;
      } else {
        throw new Error(result.error?.message || 'アクションプランの削除に失敗しました');
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : '不明なエラーが発生しました';
      setDeleting({ isLoading: false, error: errorMessage, isSuccess: false });
      console.error('アクションプラン削除エラー:', error);
      return false;
    }
  }, [actionPlanId]);

  /**
   * アクションプランの再取得
   */
  const refreshActionPlan = useCallback(async () => {
    await fetchActionPlan();
  }, [fetchActionPlan]);

  useEffect(() => {
    if (actionPlanId) {
      fetchActionPlan();
    }
  }, [actionPlanId, fetchActionPlan]);

  return {
    actionPlan,
    loading,
    updating,
    deleting,
    updateActionPlan,
    deleteActionPlan,
    refreshActionPlan
  };
}
