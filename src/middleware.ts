/**
 * Next.js Middleware for Authentication
 * 要求仕様ID: ACC.1-AUTH.1, SEC.1-ACS.1
 */

import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth } from '@/lib/auth';

// 認証が不要なパス
const publicPaths = [
  '/',
  '/api/auth/login',
  '/api/auth/refresh',
  '/api/test',
  '/_next',
  '/favicon.ico'
];

// 認証が必要なAPIパス
const protectedApiPaths = [
  '/api/career',
  '/api/work',
  '/api/skills',
  '/api/trainings',
  '/api/notifications',
  '/api/reports',
  '/api/skill-categories'
];

// 認証が必要なページパス
const protectedPagePaths = [
  '/dashboard',
  '/work',
  '/skills',
  '/career',
  '/trainings',
  '/reports'
];

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // 静的ファイルやpublicパスは認証をスキップ
  if (publicPaths.some(path => pathname.startsWith(path))) {
    return NextResponse.next();
  }

  // APIパスの認証チェック
  if (protectedApiPaths.some(path => pathname.startsWith(path))) {
    const authResult = await verifyAuth(request);
    
    if (!authResult.success) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'AUTHENTICATION_REQUIRED',
            message: '認証が必要です'
          },
          timestamp: new Date().toISOString()
        },
        { status: 401 }
      );
    }

    // 認証情報をヘッダーに追加（後続の処理で利用可能）
    const response = NextResponse.next();
    response.headers.set('x-user-id', authResult.userId || '');
    response.headers.set('x-employee-id', authResult.employeeId || '');
    response.headers.set('x-tenant-id', authResult.tenantId || '');
    response.headers.set('x-user-role', authResult.role || '');

    return response;
  }

  // ページパスの認証チェック
  if (protectedPagePaths.some(path => pathname.startsWith(path))) {
    // クライアントサイドでの認証チェックのため、ここではそのまま通す
    // 実際の認証はページコンポーネント内で行う
    return NextResponse.next();
  }

  return NextResponse.next();
}

// ミドルウェアを適用するパスの設定
export const config = {
  matcher: [
    /*
     * 以下を除くすべてのパスにマッチ:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
};