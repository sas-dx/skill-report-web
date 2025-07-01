/**
 * 要求仕様ID: PLT.1-WEB.1, ACC.1-AUTH.1
 * 対応設計書: docs/design/api/specs/API定義書_API-001_ユーザー認証API.md
 * 実装内容: 認証ヘルパー関数
 */

import { NextRequest } from 'next/server';
import jwt from 'jsonwebtoken';
import { prisma } from './prisma';

export interface AuthUser {
  userId: string;
  employeeId: string;
  employeeCode: string;
  fullName: string;
  email: string;
  departmentId: string | null;
  positionId: string | null;
}

export interface JWTPayload {
  userId: string;
  employeeId: string;
  employeeCode: string;
  email: string;
  iat: number;
  exp: number;
}

/**
 * リクエストからJWTトークンを取得・検証し、ユーザー情報を返す
 */
export async function verifyAuth(request: NextRequest): Promise<AuthUser> {
  const token = getTokenFromRequest(request);
  
  if (!token) {
    throw new Error('認証トークンが必要です');
  }

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!) as JWTPayload;
    
    // データベースからユーザー情報を取得
    const employee = await prisma.employee.findUnique({
      where: { 
        employee_code: payload.employeeCode
      },
      select: {
        employee_code: true,
        full_name: true,
        email: true,
        department_id: true,
        position_id: true,
        employee_status: true
      }
    });

    if (!employee || employee.employee_status !== 'ACTIVE') {
      throw new Error('ユーザーが見つからないか、無効な状態です');
    }

    return {
      userId: payload.userId,
      employeeId: payload.employeeId,
      employeeCode: employee.employee_code,
      fullName: employee.full_name || '',
      email: employee.email || '',
      departmentId: employee.department_id || null,
      positionId: employee.position_id || null
    };
  } catch (error) {
    if (error instanceof jwt.JsonWebTokenError) {
      throw new Error('無効な認証トークンです');
    }
    throw error;
  }
}

/**
 * リクエストヘッダーからトークンを取得
 */
function getTokenFromRequest(request: NextRequest): string | null {
  const authHeader = request.headers.get('authorization');
  
  if (authHeader && authHeader.startsWith('Bearer ')) {
    return authHeader.substring(7);
  }
  
  // Cookieからも取得を試行
  const tokenCookie = request.cookies.get('auth-token');
  if (tokenCookie) {
    return tokenCookie.value;
  }
  
  return null;
}

/**
 * JWTトークンを生成
 */
export function generateToken(user: { userId: string; employeeId: string; employeeCode: string; email: string }): string {
  const payload: Omit<JWTPayload, 'iat' | 'exp'> = {
    userId: user.userId,
    employeeId: user.employeeId,
    employeeCode: user.employeeCode,
    email: user.email
  };

  return jwt.sign(payload, process.env.JWT_SECRET!, {
    expiresIn: '24h'
  });
}

/**
 * 認証エラーレスポンス生成
 */
export function createAuthErrorResponse(message: string = '認証が必要です') {
  return Response.json({
    success: false,
    error: {
      code: 'AUTHENTICATION_ERROR',
      message
    }
  }, { status: 401 });
}
