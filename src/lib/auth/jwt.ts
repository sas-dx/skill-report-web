/**
 * JWT認証システム
 * 要求仕様ID: TNT.3-AUTH.1, PLT.1-WEB.1
 */

import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import { prisma } from '@/lib/prisma';

// JWT設定
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '24h';
const REFRESH_TOKEN_EXPIRES_IN = process.env.REFRESH_TOKEN_EXPIRES_IN || '7d';

export interface JWTPayload {
  userId: string;
  employeeCode: string;
  email: string;
  tenantId: string;
  tenantCode: string;
  role: string;
  permissions: string[];
  sessionId: string;
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

/**
 * パスワードのハッシュ化
 */
export async function hashPassword(password: string): Promise<string> {
  const salt = await bcrypt.genSalt(10);
  return bcrypt.hash(password, salt);
}

/**
 * パスワードの検証
 */
export async function verifyPassword(password: string, hashedPassword: string): Promise<boolean> {
  return bcrypt.compare(password, hashedPassword);
}

/**
 * JWTトークンの生成
 */
export function generateToken(payload: JWTPayload): string {
  return jwt.sign(payload as any, JWT_SECRET, {
    expiresIn: JWT_EXPIRES_IN,
    issuer: 'skill-report-system',
    audience: payload.tenantCode,
  } as any);
}

/**
 * リフレッシュトークンの生成
 */
export function generateRefreshToken(payload: JWTPayload): string {
  return jwt.sign(
    { 
      userId: payload.userId,
      tenantId: payload.tenantId,
      sessionId: payload.sessionId,
      type: 'refresh'
    } as any,
    JWT_SECRET,
    {
      expiresIn: REFRESH_TOKEN_EXPIRES_IN,
      issuer: 'skill-report-system',
    } as any
  );
}

/**
 * アクセストークンとリフレッシュトークンの生成
 */
export function generateAuthTokens(payload: JWTPayload): AuthTokens {
  const accessToken = generateToken(payload);
  const refreshToken = generateRefreshToken(payload);
  
  return {
    accessToken,
    refreshToken,
    expiresIn: 24 * 60 * 60 * 1000, // 24時間（ミリ秒）
  };
}

/**
 * JWTトークンの検証
 */
export async function verifyToken(token: string): Promise<JWTPayload | null> {
  try {
    const decoded = jwt.verify(token, JWT_SECRET) as JWTPayload;
    
    // セッションの有効性を確認
    const session = await prisma.tokenStore.findFirst({
      where: {
        token_value: token,
        token_type: 'ACCESS',
        is_revoked: false,
        is_deleted: false,
        expires_at: {
          gt: new Date()
        }
      }
    });
    
    if (!session) {
      return null;
    }
    
    return decoded;
  } catch (error) {
    console.error('JWT検証エラー:', error);
    return null;
  }
}

/**
 * リフレッシュトークンの検証とアクセストークンの再発行
 */
export async function refreshAccessToken(refreshToken: string): Promise<AuthTokens | null> {
  try {
    const decoded = jwt.verify(refreshToken, JWT_SECRET) as any;
    
    if (decoded.type !== 'refresh') {
      return null;
    }
    
    // リフレッシュトークンの有効性を確認
    const storedToken = await prisma.tokenStore.findFirst({
      where: {
        token_value: refreshToken,
        token_type: 'REFRESH',
        is_revoked: false,
        is_deleted: false,
        expires_at: {
          gt: new Date()
        }
      }
    });
    
    if (!storedToken) {
      return null;
    }
    
    // ユーザー情報を取得
    const user = await prisma.employee.findFirst({
      where: {
        id: decoded.userId,
        is_deleted: false
      }
    });
    
    if (!user) {
      return null;
    }
    
    // テナント情報を取得
    const tenant = await prisma.tenant.findUnique({
      where: { tenant_id: decoded.tenantId }
    });
    
    if (!tenant) {
      return null;
    }
    
    // ユーザーのロールと権限を取得
    const userRole = await prisma.userRole.findFirst({
      where: {
        user_id: user.id,
        is_deleted: false
      }
    });
    
    let permissions: string[] = [];
    if (userRole) {
      const rolePermissions = await prisma.rolePermission.findMany({
        where: {
          role_id: userRole.role_id,
          is_deleted: false
        }
      } as any);
      
      permissions = rolePermissions
        .filter((rp: any) => rp.permission)
        .map((rp: any) => rp.permission!.permission_key || '');
    }
    
    // 新しいトークンを生成
    const newPayload: JWTPayload = {
      userId: user.id,
      employeeCode: user.employee_code,
      email: user.email || '',
      tenantId: tenant.tenant_id,
      tenantCode: tenant.tenant_code || '',
      role: userRole?.role_id || 'user',
      permissions,
      sessionId: decoded.sessionId
    };
    
    return generateAuthTokens(newPayload);
  } catch (error) {
    console.error('リフレッシュトークン検証エラー:', error);
    return null;
  }
}

/**
 * トークンの無効化（ログアウト時）
 */
export async function revokeToken(token: string): Promise<boolean> {
  try {
    await prisma.tokenStore.updateMany({
      where: {
        token_value: token
      },
      data: {
        is_revoked: true,
        revoked_at: new Date()
      }
    });
    
    return true;
  } catch (error) {
    console.error('トークン無効化エラー:', error);
    return false;
  }
}

/**
 * セッションIDの生成
 */
export function generateSessionId(): string {
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * トークンの保存
 */
export async function saveToken(
  token: string,
  type: 'ACCESS' | 'REFRESH',
  userId: string,
  tenantId: string,
  expiresAt: Date
): Promise<void> {
  try {
    await prisma.tokenStore.create({
      data: {
        id: `token_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        token_type: type,
        token_value: token,
        user_id: userId,
        tenant_id: tenantId,
        expires_at: expiresAt,
        is_revoked: false,
        is_deleted: false
      }
    });
  } catch (error) {
    console.error('トークン保存エラー:', error);
    throw error;
  }
}