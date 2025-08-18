// ダッシュボードデータ取得用カスタムフック
import { useState, useEffect } from 'react';
import type { DashboardData, DashboardSettings } from '@/types/dashboard';

export const useDashboard = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [settings, setSettings] = useState<DashboardSettings | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // ダッシュボードデータ取得
  const fetchDashboardData = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('認証トークンが見つかりません');
      }

      const response = await fetch('/api/dashboard', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('データの取得に失敗しました');
      }

      const result = await response.json();
      if (result.success && result.data) {
        setData(result.data);
      } else {
        throw new Error(result.error || 'データの取得に失敗しました');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'エラーが発生しました');
      console.error('Dashboard data fetch error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // ダッシュボード設定取得
  const fetchDashboardSettings = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch('/api/dashboard/settings', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const result = await response.json();
        if (result.success && result.data) {
          setSettings(result.data);
        }
      }
    } catch (err) {
      console.error('Dashboard settings fetch error:', err);
    }
  };

  // ダッシュボード設定更新
  const updateSettings = async (newSettings: Partial<DashboardSettings>) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('認証トークンが見つかりません');
      }

      const response = await fetch('/api/dashboard/settings', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newSettings)
      });

      if (!response.ok) {
        throw new Error('設定の更新に失敗しました');
      }

      const result = await response.json();
      if (result.success && result.data) {
        setSettings(result.data);
        return true;
      }
      return false;
    } catch (err) {
      console.error('Dashboard settings update error:', err);
      return false;
    }
  };

  // 設定リセット
  const resetSettings = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('認証トークンが見つかりません');
      }

      const response = await fetch('/api/dashboard/settings', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('設定のリセットに失敗しました');
      }

      // デフォルト設定を再取得
      await fetchDashboardSettings();
      return true;
    } catch (err) {
      console.error('Dashboard settings reset error:', err);
      return false;
    }
  };

  // データリフレッシュ
  const refresh = async () => {
    await fetchDashboardData();
  };

  // 初回データ取得
  useEffect(() => {
    fetchDashboardData();
    fetchDashboardSettings();
  }, []);

  // 自動リフレッシュ設定
  useEffect(() => {
    if (settings?.refresh_interval && settings.refresh_interval > 0) {
      const interval = setInterval(() => {
        fetchDashboardData();
      }, settings.refresh_interval * 1000);

      return () => clearInterval(interval);
    }
    return undefined;
  }, [settings?.refresh_interval]);

  return {
    data,
    settings,
    isLoading,
    error,
    refresh,
    updateSettings,
    resetSettings
  };
};

// ユーザーサマリー取得用フック
export const useUserSummary = () => {
  const [summary, setSummary] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchUserSummary = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('認証トークンが見つかりません');
      }

      const response = await fetch('/api/dashboard/user-summary', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('データの取得に失敗しました');
      }

      const result = await response.json();
      if (result.success && result.data) {
        setSummary(result.data);
      } else {
        throw new Error(result.error || 'データの取得に失敗しました');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'エラーが発生しました');
      console.error('User summary fetch error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchUserSummary();
  }, []);

  return {
    summary,
    isLoading,
    error,
    refresh: fetchUserSummary
  };
};