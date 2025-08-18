/**
 * 要求仕様ID: PRO.1-BASE.1
 * 対応設計書: docs/design/api/specs/API定義書_API-013_組織情報取得API.md
 * 実装内容: 組織情報API クライアント関数
 */

// 部署情報の型定義
export interface Department {
  department_id: string;
  name: string;
  code: string;
  parent_id: string | null;
  level: number;
  is_active: boolean;
  display_order: number;
}

// 役職情報の型定義
export interface Position {
  position_id: string;
  name: string;
  level: number;
  is_manager: boolean;
  is_active: boolean;
  display_order: number;
}

// 組織情報レスポンスの型定義
export interface OrganizationResponse {
  success: boolean;
  data?: {
    departments: Department[];
    positions: Position[];
  };
  error?: {
    code: string;
    message: string;
    details?: string;
  };
}

/**
 * 組織情報（部署・役職）を取得する
 * @returns 組織情報
 */
export async function getOrganizationInfo(): Promise<OrganizationResponse> {
  try {
    // 認証トークンを取得
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    
    const response = await fetch('/api/organization', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
      },
      credentials: 'include',
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error?.message || '組織情報取得に失敗しました');
    }

    return data;
  } catch (error) {
    console.error('Organization fetch error:', error);
    return {
      success: false,
      error: {
        code: 'FETCH_ERROR',
        message: error instanceof Error ? error.message : '組織情報取得に失敗しました'
      }
    };
  }
}

/**
 * 部署情報をセレクトボックス用のオプションに変換する
 * @param departments 部署情報配列
 * @returns セレクトボックス用オプション
 */
export function departmentsToSelectOptions(departments: Department[]) {
  return departments
    .filter(dept => dept.is_active)
    .sort((a, b) => a.display_order - b.display_order)
    .map(dept => ({
      value: dept.department_id,
      label: dept.name,
      disabled: false
    }));
}

/**
 * 役職情報をセレクトボックス用のオプションに変換する
 * @param positions 役職情報配列
 * @returns セレクトボックス用オプション
 */
export function positionsToSelectOptions(positions: Position[]) {
  return positions
    .filter(pos => pos.is_active)
    .sort((a, b) => a.display_order - b.display_order)
    .map(pos => ({
      value: pos.position_id,
      label: pos.name,
      disabled: false
    }));
}
