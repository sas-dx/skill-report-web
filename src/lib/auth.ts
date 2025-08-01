// PLT.1-WEB.1: 認証・セキュリティ機能
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

// Node.js環境変数の型定義
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      JWT_SECRET?: string;
      JWT_EXPIRES_IN?: string;
    }
  }
}

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '24h';

/**
 * パスワードをハッシュ化する
 * @param password - 平文パスワード
 * @returns ハッシュ化されたパスワード
 */
export async function hashPassword(password: string): Promise<string> {
  const saltRounds = 12;
  return await bcrypt.hash(password, saltRounds);
}

/**
 * パスワードを検証する
 * @param password - 平文パスワード
 * @param hashedPassword - ハッシュ化されたパスワード
 * @returns 検証結果
 */
export async function verifyPassword(password: string, hashedPassword: string): Promise<boolean> {
  return await bcrypt.compare(password, hashedPassword);
}

/**
 * JWTトークンを生成する
 * @param payload - トークンに含めるデータ
 * @returns JWTトークン
 */
export function generateToken(payload: { userId: string; loginId: string; employeeId: string }): string {
  return jwt.sign(payload, JWT_SECRET as jwt.Secret, { expiresIn: JWT_EXPIRES_IN } as jwt.SignOptions);
}

/**
 * JWTトークンを検証する
 * @param token - 検証するトークン
 * @returns デコードされたペイロード
 */
export function verifyToken(token: string): { userId: string; loginId: string; employeeId: string } | null {
  try {
    const decoded = jwt.verify(token, JWT_SECRET) as { userId: string; loginId: string; employeeId: string };
    return decoded;
  } catch (error) {
    return null;
  }
}

/**
 * リクエストからトークンを取得する
 * @param request - HTTPリクエスト
 * @returns トークン文字列またはnull
 */
export function getTokenFromRequest(request: Request): string | null {
  const authHeader = request.headers.get('authorization');
  if (authHeader && authHeader.startsWith('Bearer ')) {
    return authHeader.substring(7);
  }
  return null;
}

/**
 * リクエストの認証を検証する
 * @param request - HTTPリクエスト
 * @returns 認証結果
 */
export async function verifyAuth(request: Request): Promise<{ success: boolean; userId?: string; loginId?: string; employeeId?: string }> {
  const token = getTokenFromRequest(request);
  
  if (!token) {
    return { success: false };
  }

  const decoded = verifyToken(token);
  
  if (!decoded) {
    return { success: false };
  }

  return {
    success: true,
    userId: decoded.userId,
    loginId: decoded.loginId,
    employeeId: decoded.employeeId
  };
}
