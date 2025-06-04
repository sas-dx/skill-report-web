# 技術コンテキスト

## 技術スタック概要

### 実装済みフロントエンド技術
- **Next.js 14**: App Router、Server Components ✅
- **React 18**: 基本機能、コンポーネント ✅
- **TypeScript 5.x**: 厳密な型チェック ✅
- **Tailwind CSS 3.x**: ユーティリティファースト、レスポンシブ対応 ✅
- **Radix UI**: UIコンポーネントライブラリ ✅
- **Lucide React**: アイコンライブラリ ✅

### 実装済みバックエンド技術
- **Next.js API Routes**: 基本的なAPI構造 ✅
- **Prisma ORM**: データベースアクセス（シングルテナント版） ✅
- **bcryptjs**: パスワードハッシュ化 ✅
- **jsonwebtoken**: JWT認証（基本実装） ✅
- **Zod**: スキーマバリデーション ✅

### 未実装技術
- **NextAuth.js**: 認証・セッション管理、マルチテナント対応 ❌
- **Zustand**: 軽量状態管理 ❌
- **Row Level Security**: PostgreSQL RLS ❌

### データベース・インフラ
- **PostgreSQL 15**: Docker環境 ✅
- **Docker**: 開発環境統一、コンテナ化 ✅
- **Vercel Platform**: 本番環境（未構築） ❌

## 開発環境構成

### Docker開発環境（実装済み）
```yaml
# docker-compose.yml 構成 ✅
services:
  app:                    # Next.js アプリケーション
    - ポート: 3000 ✅
    - ホットリロード対応 ✅
    - 環境変数設定 ✅
  
  postgres:               # PostgreSQL データベース
    - ポート: 5433 ✅
    - データ永続化 ✅
    - 初期化スクリプト ✅
  
  pgadmin:               # データベース管理ツール
    - ポート: 8080 ✅
    - GUI管理インターフェース ✅
```

### 開発ツール設定（実装済み）
```json
// package.json 主要依存関係 ✅
{
  "dependencies": {
    "next": "^14.2.29",
    "react": "^18.3.1",
    "typescript": "^5.8.3",
    "prisma": "^5.14.0",
    "@prisma/client": "^5.14.0",
    "tailwindcss": "^3.4.3",
    "@radix-ui/react-*": "最新版",
    "zod": "^3.23.8",
    "bcryptjs": "^2.4.3",
    "jsonwebtoken": "^9.0.2",
    "lucide-react": "^0.378.0"
  },
  "devDependencies": {
    "eslint": "^8.57.0",
    "prettier": "^3.2.5",
    "@types/node": "^20.12.12",
    "@types/react": "^18.3.2"
  }
}
```

## 現在の実装状況

### シングルテナント実装（実装済み）
```sql
-- 現在のPrismaスキーマ構造
model User {
  id        String   @id @default(cuid())
  emp_no    String   @unique
  email     String   @unique
  name      String
  // tenant_id なし（シングルテナント）
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

### 設計書のマルチテナント構造（未実装）
```sql
-- 設計書のマルチテナント構造（未実装）
model User {
  id        String   @id @default(cuid())
  tenant_id String   // 未実装
  emp_no    String   
  email     String   
  name      String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  tenant    Tenant   @relation(fields: [tenant_id], references: [id]) // 未実装
  
  @@unique([tenant_id, emp_no]) // 未実装
}
```

### Row Level Security（未実装）
```sql
-- PostgreSQL RLS 設定パターン（未実装）
ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON table_name
    FOR ALL TO authenticated
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);

-- セッション設定（未実装）
SET app.current_tenant_id = 'tenant-uuid-here';
```

### テナント認証フロー（未実装）
```typescript
// 設計書のマルチテナント認証（未実装）
export const authOptions: NextAuthOptions = {
  providers: [
    // 認証プロバイダー設定
  ],
  callbacks: {
    async session({ session, token }) {
      // テナント情報をセッションに追加（未実装）
      session.tenantId = token.tenantId;
      return session;
    },
    async jwt({ token, user, account }) {
      // JWTにテナント情報を含める（未実装）
      if (user) {
        token.tenantId = user.tenantId;
      }
      return token;
    }
  }
};
```

### データアクセス層（部分実装）
```typescript
// 現在の実装（シングルテナント）
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export async function getUsers() {
  return await prisma.user.findMany(); // テナント分離なし
}

// 設計書のマルチテナント対応（未実装）
class TenantAwarePrismaClient {
  private prisma: PrismaClient;
  
  constructor(private tenantId: string) {
    this.prisma = new PrismaClient();
  }
  
  async executeQuery<T>(query: () => Promise<T>): Promise<T> {
    // RLS設定（未実装）
    await this.prisma.$executeRaw`
      SET app.current_tenant_id = ${this.tenantId}
    `;
    
    // クエリ実行
    return await query();
  }
}
```

## API設計・実装パターン

### 現在のAPI Route構造（部分実装）
```typescript
// /app/api/auth/login/route.ts（実装済み）
export async function POST(request: NextRequest) {
  try {
    const { email, password } = await request.json();
    
    // 基本的な認証処理のみ
    const user = await authenticateUser(email, password);
    
    if (user) {
      return NextResponse.json({ success: true, user });
    } else {
      return NextResponse.json({ error: 'Invalid credentials' }, { status: 401 });
    }
  } catch (error) {
    return NextResponse.json({ error: 'Server error' }, { status: 500 });
  }
}

// 設計書の統一API構造（未実装）
export async function GET(request: NextRequest) {
  try {
    // 1. 認証チェック（未実装）
    const session = await getServerSession(authOptions);
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }
    
    // 2. テナント情報取得（未実装）
    const tenantId = session.tenantId;
    
    // 3. ビジネスロジック実行（未実装）
    const result = await service.getData(tenantId);
    
    // 4. レスポンス返却（未実装）
    return NextResponse.json({
      success: true,
      data: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    return handleApiError(error);
  }
}
```

### バリデーション・型安全性（部分実装）
```typescript
// Zod スキーマ定義（基本実装済み）
import { z } from 'zod';

const LoginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(6)
});

// 設計書の詳細スキーマ（未実装）
const CreateUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  department: z.string().optional(),
  skills: z.array(z.object({
    skillId: z.string().uuid(),
    level: z.number().min(1).max(4)
  }))
});

type CreateUserRequest = z.infer<typeof CreateUserSchema>;

// API での使用（未実装）
export async function POST(request: NextRequest) {
  const body = await request.json();
  const validatedData = CreateUserSchema.parse(body);
  // 型安全な処理続行
}
```

## フロントエンド技術実装

### App Router活用（実装済み）
```typescript
// app/layout.tsx - ルートレイアウト ✅
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body>
        {/* 基本レイアウト実装済み */}
        {children}
      </body>
    </html>
  );
}

// app/dashboard/page.tsx - ダッシュボード ✅
export default function DashboardPage() {
  return <DashboardContent />;
}

// 設計書のマルチテナント対応（未実装）
export default async function DashboardPage() {
  const session = await getServerSession(authOptions);
  const data = await fetchDashboardData(session.tenantId);
  
  return <DashboardComponent data={data} />;
}
```

### 状態管理（未実装）
```typescript
// 設計書のZustand状態管理（未実装）
interface AppState {
  // 認証状態
  auth: {
    user: User | null;
    isAuthenticated: boolean;
  };
  
  // テナント状態（未実装）
  tenant: {
    currentTenant: Tenant | null;
    availableTenants: Tenant[];
  };
  
  // アクション
  setUser: (user: User | null) => void;
  setCurrentTenant: (tenant: Tenant) => void;
  switchTenant: (tenantId: string) => Promise<void>;
}

export const useAppStore = create<AppState>((set, get) => ({
  auth: {
    user: null,
    isAuthenticated: false,
  },
  tenant: {
    currentTenant: null,
    availableTenants: [],
  },
  
  setUser: (user) => set((state) => ({
    auth: { ...state.auth, user, isAuthenticated: !!user }
  })),
  
  setCurrentTenant: (tenant) => set((state) => ({
    tenant: { ...state.tenant, currentTenant: tenant }
  })),
  
  switchTenant: async (tenantId) => {
    // テナント切り替えロジック（未実装）
    const response = await fetch(`/api/v1/tenants/${tenantId}/switch`, {
      method: 'POST'
    });
    
    if (response.ok) {
      const tenant = await response.json();
      get().setCurrentTenant(tenant.data);
      window.location.reload(); // データ再取得のため
    }
  }
}));
```

### コンポーネント設計（実装済み）
```typescript
// components/ui/Button.tsx - 共通UIコンポーネント ✅
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  loading = false,
  children,
  onClick
}) => {
  // 実装済み
  const baseClasses = 'font-medium rounded-md transition-colors';
  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
    danger: 'bg-red-600 text-white hover:bg-red-700'
  };
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  };
  
  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`}
      onClick={onClick}
      disabled={loading}
    >
      {loading ? <Spinner /> : children}
    </button>
  );
};
```

## データベース技術実装

### 現在のPrisma スキーマ（シングルテナント版）
```prisma
// prisma/schema.prisma ✅
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// 実装済みモデル（シングルテナント版）
model User {
  id        String   @id @default(cuid())
  emp_no    String   @unique
  email     String   @unique
  name      String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  // リレーション
  userAuth  UserAuth?
  skills    UserSkill[]
  
  @@map("users")
}

model UserAuth {
  id           String @id @default(cuid())
  userId       String @unique
  passwordHash String
  
  user User @relation(fields: [userId], references: [id])
  
  @@map("user_auth")
}

// 設計書のマルチテナント版（未実装）
model MST_Tenant {
  tenant_id     String   @id @default(uuid()) @db.Uuid
  tenant_name   String   @db.VarChar(100)
  tenant_code   String   @unique @db.VarChar(20)
  status        String   @db.VarChar(20)
  created_at    DateTime @default(now())
  updated_at    DateTime @updatedAt
  
  // リレーション
  users         TRN_UserProfile[]
  settings      MST_TenantSettings[]
  
  @@map("MST_Tenant")
}
```

### マイグレーション管理（部分実装）
```sql
-- 基本テーブル作成（実装済み）
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    emp_no TEXT UNIQUE,
    email TEXT UNIQUE,
    name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 設計書のマルチテナント対応（未実装）
-- migrations/001_enable_rls.sql
ALTER TABLE "users" ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_users ON "users"
    FOR ALL TO authenticated
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);

-- インデックス作成（未実装）
CREATE INDEX idx_user_profile_tenant_id ON "users"(tenant_id);
CREATE INDEX idx_user_profile_emp_no ON "users"(tenant_id, emp_no);
```

## バッチ処理技術実装

### 設計書のバッチ基盤アーキテクチャ（未実装）
```typescript
// lib/batch/BaseBatch.ts（未実装）
export abstract class BaseBatch {
  protected batchId: string;
  protected tenantId?: string;
  
  constructor(batchId: string, tenantId?: string) {
    this.batchId = batchId;
    this.tenantId = tenantId;
  }
  
  abstract execute(): Promise<void>;
  
  async run(): Promise<void> {
    const startTime = Date.now();
    
    try {
      await this.beforeExecute();
      await this.execute();
      await this.afterExecute();
      
      await this.logSuccess(Date.now() - startTime);
    } catch (error) {
      await this.logError(error);
      throw error;
    }
  }
  
  protected async beforeExecute(): Promise<void> {
    // 前処理（ログ出力、リソース確保等）
  }
  
  protected async afterExecute(): Promise<void> {
    // 後処理（リソース解放、通知等）
  }
  
  protected async logSuccess(duration: number): Promise<void> {
    // 成功ログ出力
  }
  
  protected async logError(error: any): Promise<void> {
    // エラーログ出力
  }
}
```

## セキュリティ技術実装

### 現在の認証・認可（基本実装）
```typescript
// src/lib/auth.ts（基本実装済み）
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

export async function authenticateUser(email: string, password: string) {
  // 基本的な認証処理のみ実装
  const user = await prisma.user.findUnique({
    where: { email },
    include: { userAuth: true }
  });
  
  if (user && user.userAuth) {
    const isValid = await bcrypt.compare(password, user.userAuth.passwordHash);
    return isValid ? user : null;
  }
  
  return null;
}

// 設計書のミドルウェア（未実装）
export async function middleware(request: NextRequest) {
  // 1. 認証チェック
  const token = await getToken({ req: request });
  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  // 2. テナント情報設定
  const tenantId = token.tenantId as string;
  if (!tenantId) {
    return NextResponse.redirect(new URL('/tenant-select', request.url));
  }
  
  // 3. 権限チェック
  const hasPermission = await checkPermission(token.userId, request.nextUrl.pathname);
  if (!hasPermission) {
    return NextResponse.redirect(new URL('/unauthorized', request.url));
  }
  
  // 4. リクエストヘッダーにテナント情報追加
  const requestHeaders = new Headers(request.headers);
  requestHeaders.set('x-tenant-id', tenantId);
  
  return NextResponse.next({
    request: {
      headers: requestHeaders,
    },
  });
}
```

### データ暗号化（部分実装）
```typescript
// 実装済み: 基本暗号化
import bcrypt from 'bcryptjs';

export async function hashPassword(password: string): Promise<string> {
  return await bcrypt.hash(password, 10);
}

export async function verifyPassword(password: string, hash: string): Promise<boolean> {
  return await bcrypt.compare(password, hash);
}

// 設計書の高度な暗号化（未実装）
import crypto from 'crypto';

const ENCRYPTION_KEY = process.env.ENCRYPTION_KEY!;
const ALGORITHM = 'aes-256-gcm';

export function encrypt(text: string): string {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipher(ALGORITHM, ENCRYPTION_KEY);
  cipher.setAAD(Buffer.from('additional-data'));
  
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  const authTag = cipher.getAuthTag();
  
  return `${iv.toString('hex')}:${authTag.toString('hex')}:${encrypted}`;
}
```

## 監視・ログ技術実装

### 現在の実装（基本のみ）
```typescript
// 基本的なconsole.log使用 ✅
console.log('User logged in:', { userId: user.id });

// 設計書の構造化ログ（未実装）
import winston from 'winston';

interface LogContext {
  tenantId?: string;
  userId?: string;
  action: string;
  resource?: string;
  details?: any;
  traceId?: string;
}

class Logger {
  private winston: winston.Logger;
  
  constructor() {
    this.winston = winston.createLogger({
      level: process.env.LOG_LEVEL || 'info',
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json()
      ),
      transports: [
        new winston.transports.Console(),
        new winston.transports.File({ filename: 'app.log' })
      ]
    });
  }
  
  info(message: string, context: LogContext) {
    this.winston.info(message, {
      ...context,
      timestamp: new Date().toISOString()
    });
  }
}

export const logger = new Logger();
```

## パフォーマンス最適化

### 現在の実装（基本のみ）
```typescript
// 基本的なPrismaクエリ ✅
export async function getUsers() {
  return await prisma.user.findMany({
    include: {
      skills: true
    }
  });
}

// 設計書のキャッシュ戦略（未実装）
import { Redis } from 'ioredis';

class CacheManager {
  private redis: Redis;
  
  constructor() {
    this.redis = new Redis(process.env.REDIS_URL!);
  }
  
  async get<T>(key: string): Promise<T | null> {
    const cached = await this.redis.get(key);
    return cached ? JSON.parse(cached) : null;
  }
  
  async set<T>(key: string, value: T, ttl: number = 3600): Promise<void> {
    await this.redis.setex(key, ttl, JSON.stringify(value));
  }
  
  // テナント別キャッシュキー生成
  tenantKey(tenantId: string, resource: string, id?: string): string {
    return `tenant:${tenantId}:${resource}${id ? `:${id}` : ''}`;
  }
}

export const cache = new CacheManager();
```

## 実装方針の技術的選択肢

### 選択肢1: マルチテナント対応実装
**技術的変更点**:
- Prismaスキーマ全面改修
- PostgreSQL RLS実装
- NextAuth.js導入
- 状態管理（Zustand）導入
- API全面修正

### 選択肢2: シングルテナント継続
**技術的完成項目**:
- 現在のPrismaスキーマ完成
- CRUD API実装
- 認証強化
- テスト実装

### 選択肢3: 段階的移行
**Phase 1**: シングルテナント完成
**Phase 2**: マルチテナント技術導入

## 次回実装時の技術的重点項目

### 共通技術実装
1. **API実装**: CRUD操作の完全実装
2. **認証強化**: JWT・セッション管理
3. **バリデーション**: Zod活用の入力検証
4. **エラーハンドリング**: 統一エラー処理

### 方針別技術実装
- **マルチテナント**: RLS・テナント管理・認証拡張
- **シングルテナント**: 機能完成・テスト・デプロイ
- **段階的移行**: Phase 1完成後にマルチテナント技術導入

この技術コンテキストにより、現実的な実装状況に基づいた技術的意思決定と開発計画策定が可能になります。
