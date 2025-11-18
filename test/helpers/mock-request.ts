/**
 * 統合テスト用モックリクエストユーティリティ
 * 要求仕様ID: TEST-INT.1
 * 実装ガイド: docs/testing/04_統合テスト実装ガイド.md
 */

import { NextRequest } from 'next/server'
import { generateToken } from '@/lib/auth'

/**
 * NextRequestのモックを作成する
 * @param url - リクエストURL（デフォルト: http://localhost:3000/api/test）
 * @param options - リクエストオプション
 * @returns モックNextRequestオブジェクト
 */
export function createMockRequest(
  url: string = 'http://localhost:3000/api/test',
  options: {
    method?: string
    headers?: Record<string, string>
    body?: any
  } = {}
): NextRequest {
  const { method = 'GET', headers = {}, body } = options

  const requestInit: RequestInit = {
    method,
    headers: {
      'content-type': 'application/json',
      ...headers
    }
  }

  // POST/PUT/PATCHリクエストの場合、bodyを追加
  if (body && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
    requestInit.body = JSON.stringify(body)
  }

  return new NextRequest(url, requestInit)
}

/**
 * 認証付きNextRequestのモックを作成する
 * @param url - リクエストURL
 * @param userId - ユーザーID
 * @param options - リクエストオプション
 * @returns 認証トークン付きモックNextRequestオブジェクト
 */
export function createAuthenticatedMockRequest(
  url: string,
  userId: string,
  options: {
    method?: string
    headers?: Record<string, string>
    body?: any
    loginId?: string
    employeeId?: string
  } = {}
): NextRequest {
  const { loginId = 'test_user', employeeId = 'EMP001', ...requestOptions } = options

  // JWTトークンを生成
  const token = generateToken({
    userId,
    loginId,
    employeeId
  })

  // Authorizationヘッダーを追加
  const headers = {
    ...(requestOptions.headers || {}),
    authorization: `Bearer ${token}`
  }

  return createMockRequest(url, {
    ...requestOptions,
    headers
  })
}

/**
 * GETリクエストのモックを作成する
 * @param url - リクエストURL
 * @param headers - リクエストヘッダー
 * @returns モックNextRequestオブジェクト
 */
export function createMockGETRequest(
  url: string,
  headers?: Record<string, string>
): NextRequest {
  return createMockRequest(url, { method: 'GET', headers })
}

/**
 * POSTリクエストのモックを作成する
 * @param url - リクエストURL
 * @param body - リクエストボディ
 * @param headers - リクエストヘッダー
 * @returns モックNextRequestオブジェクト
 */
export function createMockPOSTRequest(
  url: string,
  body: any,
  headers?: Record<string, string>
): NextRequest {
  return createMockRequest(url, { method: 'POST', body, headers })
}

/**
 * PUTリクエストのモックを作成する
 * @param url - リクエストURL
 * @param body - リクエストボディ
 * @param headers - リクエストヘッダー
 * @returns モックNextRequestオブジェクト
 */
export function createMockPUTRequest(
  url: string,
  body: any,
  headers?: Record<string, string>
): NextRequest {
  return createMockRequest(url, { method: 'PUT', body, headers })
}

/**
 * DELETEリクエストのモックを作成する
 * @param url - リクエストURL
 * @param headers - リクエストヘッダー
 * @returns モックNextRequestオブジェクト
 */
export function createMockDELETERequest(
  url: string,
  headers?: Record<string, string>
): NextRequest {
  return createMockRequest(url, { method: 'DELETE', headers })
}
