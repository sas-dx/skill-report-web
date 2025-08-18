/**
 * API共通ユーティリティ関数
 * 要求仕様ID: PLT.1-WEB.1
 * 対応設計書: docs/design/api/共通API仕様.md
 */

import { NextResponse } from 'next/server';

/**
 * 成功レスポンスを作成する
 * @param data レスポンスデータ
 * @param status HTTPステータスコード（デフォルト: 200）
 * @returns NextResponse
 */
export function createSuccessResponse(data: any, status: number = 200): NextResponse {
  return NextResponse.json({
    success: true,
    data,
    timestamp: new Date().toISOString()
  }, { status });
}

/**
 * エラーレスポンスを作成する
 * @param code エラーコード
 * @param message エラーメッセージ
 * @param details エラー詳細（オプション）
 * @param status HTTPステータスコード（デフォルト: 400）
 * @returns NextResponse
 */
export function createErrorResponse(
  code: string,
  message: string,
  details?: string,
  status: number = 400
): NextResponse {
  return NextResponse.json({
    success: false,
    error: {
      code,
      message,
      ...(details && { details })
    },
    timestamp: new Date().toISOString()
  }, { status });
}

/**
 * バリデーションエラーレスポンスを作成する
 * @param errors バリデーションエラーの配列
 * @returns NextResponse
 */
export function createValidationErrorResponse(
  errors: Array<{ field: string; message: string }>
): NextResponse {
  return NextResponse.json({
    success: false,
    error: {
      code: 'VALIDATION_ERROR',
      message: '入力値に誤りがあります',
      details: errors
    },
    timestamp: new Date().toISOString()
  }, { status: 400 });
}

/**
 * 認証エラーレスポンスを作成する
 * @param message エラーメッセージ（オプション）
 * @returns NextResponse
 */
export function createAuthErrorResponse(message?: string): NextResponse {
  return NextResponse.json({
    success: false,
    error: {
      code: 'AUTHENTICATION_ERROR',
      message: message || '認証が必要です'
    },
    timestamp: new Date().toISOString()
  }, { status: 401 });
}

/**
 * 認可エラーレスポンスを作成する
 * @param message エラーメッセージ（オプション）
 * @returns NextResponse
 */
export function createAuthorizationErrorResponse(message?: string): NextResponse {
  return NextResponse.json({
    success: false,
    error: {
      code: 'AUTHORIZATION_ERROR',
      message: message || 'アクセス権限がありません'
    },
    timestamp: new Date().toISOString()
  }, { status: 403 });
}

/**
 * リソースが見つからないエラーレスポンスを作成する
 * @param resource リソース名
 * @param id リソースID（オプション）
 * @returns NextResponse
 */
export function createNotFoundErrorResponse(resource: string, id?: string): NextResponse {
  const message = id 
    ? `${resource}が見つかりません (ID: ${id})`
    : `${resource}が見つかりません`;
    
  return NextResponse.json({
    success: false,
    error: {
      code: 'NOT_FOUND',
      message
    },
    timestamp: new Date().toISOString()
  }, { status: 404 });
}

/**
 * システムエラーレスポンスを作成する
 * @param error エラーオブジェクト
 * @returns NextResponse
 */
export function createSystemErrorResponse(error: Error): NextResponse {
  console.error('System Error:', error);
  
  return NextResponse.json({
    success: false,
    error: {
      code: 'SYSTEM_ERROR',
      message: 'システムエラーが発生しました'
    },
    timestamp: new Date().toISOString()
  }, { status: 500 });
}
