/**
 * NextRequest モックヘルパー
 *
 * Next.js App RouterのNextRequestオブジェクトをモックするためのヘルパー関数
 */

import { NextRequest } from 'next/server'

/**
 * NextRequestのモックを作成
 *
 * @param options - オプション設定
 * @param options.headers - リクエストヘッダー
 * @param options.url - リクエストURL
 * @param options.method - HTTPメソッド
 * @param options.body - リクエストボディ
 * @returns モックされたNextRequestオブジェクト
 *
 * @example
 * ```typescript
 * const request = createMockNextRequest({
 *   headers: { 'x-user-id': 'user_001' },
 *   url: 'http://localhost:3000/api/users'
 * })
 * ```
 */
export function createMockNextRequest(options: {
  headers?: Record<string, string>
  url?: string
  method?: string
  body?: any
} = {}): NextRequest {
  const {
    headers = {},
    url = 'http://localhost:3000',
    method = 'GET',
    body = null,
  } = options

  return {
    url,
    method,
    headers: {
      get: (name: string) => headers[name.toLowerCase()] || null,
      has: (name: string) => name.toLowerCase() in headers,
      forEach: (callback: (value: string, key: string) => void) => {
        Object.entries(headers).forEach(([key, value]) => callback(value, key))
      },
    },
    body,
    json: async () => (body ? JSON.parse(body) : {}),
    text: async () => (body ? body : ''),
  } as unknown as NextRequest
}

/**
 * 認証ヘッダー付きNextRequestのモックを作成
 *
 * @param userId - ユーザーID
 * @param additionalHeaders - 追加ヘッダー
 * @param url - リクエストURL
 * @returns モックされたNextRequestオブジェクト
 *
 * @example
 * ```typescript
 * const request = createAuthenticatedRequest('emp_001')
 * ```
 */
export function createAuthenticatedRequest(
  userId: string,
  additionalHeaders: Record<string, string> = {},
  url?: string
): NextRequest {
  return createMockNextRequest({
    headers: {
      'x-user-id': userId,
      ...additionalHeaders,
    },
    url,
  })
}
