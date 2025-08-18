/**
 * 要求仕様ID: ACC.1-AUTH.1
 * 認証ユーティリティ関数
 */

export interface User {
  id: string;
  empNo: string;
  email: string;
  name: string;
  nameKana: string;
  department: string | null;
  position: string | null;
}

/**
 * ローカルストレージから認証トークンを取得
 */
export function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('token');
}

/**
 * ローカルストレージからユーザー情報を取得
 */
export function getUser(): User | null {
  if (typeof window === 'undefined') return null;
  const userStr = localStorage.getItem('user');
  if (!userStr) return null;
  
  try {
    return JSON.parse(userStr);
  } catch (error) {
    console.error('Failed to parse user data:', error);
    return null;
  }
}

/**
 * 認証状態をチェック
 */
export function isAuthenticated(): boolean {
  const token = getAuthToken();
  const user = getUser();
  return !!(token && user);
}

/**
 * ログアウト処理
 */
export function logout(): void {
  if (typeof window === 'undefined') return;
  
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  
  // ログイン画面にリダイレクト
  window.location.href = '/';
}

/**
 * APIリクエスト用の認証ヘッダーを取得
 */
export function getAuthHeaders(): Record<string, string> {
  const token = getAuthToken();
  if (!token) return {};
  
  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };
}

/**
 * 認証が必要なAPIリクエストを実行
 */
export async function authenticatedFetch(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  const headers = {
    ...getAuthHeaders(),
    ...options.headers,
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  // 401エラーの場合は自動的にログアウト
  if (response.status === 401) {
    logout();
    throw new Error('認証が無効です。再度ログインしてください。');
  }

  return response;
}
