/**
 * 要求仕様ID: PRO.1-BASE.1
 * 実装内容: 更新履歴取得フック
 */
'use client';

import { useState, useEffect } from 'react';
import { getUpdateHistory } from '@/lib/api/profile';

export interface UpdateHistoryItem {
  date: string;
  field: string;
  oldValue: string;
  newValue: string;
  updatedBy: string;
}

export interface UseUpdateHistoryReturn {
  history: UpdateHistoryItem[];
  loading: boolean;
  error: string | null;
}

export function useUpdateHistory(userId: string, limit: number = 50): UseUpdateHistoryReturn {
  const [history, setHistory] = useState<UpdateHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUpdateHistory = async () => {
      try {
        setLoading(true);
        setError(null);

        console.log('useUpdateHistory - Fetching update history for userId:', userId, 'limit:', limit);
        const response = await getUpdateHistory(userId, limit);
        console.log('useUpdateHistory - API response:', response);

        if (response.success && response.data?.history) {
          console.log('useUpdateHistory - History found:', response.data.history);
          setHistory(response.data.history.map(item => ({
            date: item.updated_at,
            field: item.field_name,
            oldValue: item.old_value || '',
            newValue: item.new_value || '',
            updatedBy: item.updated_by_name
          })));
        } else if (response.success && !response.data?.history) {
          // 履歴がない場合
          console.log('useUpdateHistory - No history found for user');
          setHistory([]);
          setError(null);
        } else {
          console.log('useUpdateHistory - Error response:', response);
          setError(response.error?.message || '更新履歴の取得に失敗しました');
        }
      } catch (error) {
        console.error('Update history fetch error:', error);
        setError('更新履歴の取得中にエラーが発生しました');
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      fetchUpdateHistory();
    }
  }, [userId, limit]);

  return { history, loading, error };
}
