/**
 * 要求仕様ID: PRO.1-BASE.1
 * 実装内容: 上長情報取得フック
 */

import { useState, useEffect } from 'react';
import { getManagerInfo } from '@/lib/api/profile';

export interface ManagerInfo {
  id: string;
  employeeCode: string;
  name: string;
  email: string;
  phone: string;
  departmentName: string;
  positionName: string;
}

interface UseManagerInfoReturn {
  manager: ManagerInfo | null;
  loading: boolean;
  error: string | null;
}

export function useManagerInfo(userId: string): UseManagerInfoReturn {
  const [manager, setManager] = useState<ManagerInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchManagerInfo = async () => {
      try {
        setLoading(true);
        setError(null);

        console.log('useManagerInfo - Fetching manager info for userId:', userId);
        const response = await getManagerInfo(userId);
        console.log('useManagerInfo - API response:', response);

        if (response.success && response.data?.manager) {
          console.log('useManagerInfo - Manager found:', response.data.manager);
          setManager({
            id: response.data.manager.id.toString(),
            employeeCode: response.data.manager.employee_code,
            name: response.data.manager.full_name,
            email: response.data.manager.email,
            phone: response.data.manager.phone,
            departmentName: response.data.manager.department_name,
            positionName: response.data.manager.position_name,
          });
        } else if (response.success && !response.data?.manager) {
          // 上長が設定されていない場合
          console.log('useManagerInfo - No manager set for user');
          setManager(null);
          setError(null);
        } else {
          console.log('useManagerInfo - Error response:', response);
          setError(response.error?.message || '上長情報の取得に失敗しました');
        }
      } catch (error) {
        console.error('Manager info fetch error:', error);
        setError('上長情報の取得中にエラーが発生しました');
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      fetchManagerInfo();
    }
  }, [userId]);

  return { manager, loading, error };
}
