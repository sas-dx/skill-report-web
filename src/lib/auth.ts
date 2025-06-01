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
export function generateToken(payload: { userId: string; email: string; role: string }): string {
  return jwt.sign(payload, JWT_SECRET, { expiresIn: JWT_EXPIRES_IN });
}

/**
 * JWTトークンを検証する
 * @param token - 検証するトークン
 * @returns デコードされたペイロード
 */
export function verifyToken(token: string): { userId: string; email: string; role: string } | null {
  try {
    const decoded = jwt.verify(token, JWT_SECRET) as { userId: string; email: string; role: string };
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
