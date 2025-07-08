// 要求仕様ID: ACC.1-AUTH.1 - ユーザーログアウトAPI
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    // レスポンスを作成
    const response = NextResponse.json(
      {
        success: true,
        message: 'ログアウトしました',
        timestamp: new Date().toISOString(),
      },
      { status: 200 }
    );

    // 認証トークンのCookieを削除
    response.cookies.set('auth-token', '', {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 0, // 即座に削除
      path: '/'
    });

    return response;
  } catch (error) {
    console.error('Logout API Error:', error);
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'INTERNAL_SERVER_ERROR',
          message: 'システムエラーが発生しました',
        },
      },
      { status: 500 }
    );
  }
}
