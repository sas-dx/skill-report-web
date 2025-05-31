# 技術コンテキスト

## 技術スタック概要

### フロントエンド技術
- **Next.js 14**: App Router、Server Components、Server Actions
- **React 18**: Concurrent Features、Suspense、Error Boundaries
- **TypeScript 5.x**: 厳密な型チェック、最新言語機能
- **Tailwind CSS 3.x**: ユーティリティファースト、レスポンシブ対応
- **Zustand**: 軽量状態管理、TypeScript完全対応

### バックエンド技術
- **Next.js API Routes**: サーバーサイド処理、ミドルウェア
- **Prisma ORM**: タイプセーフなデータベースアクセス
- **NextAuth.js**: 認証・セッション管理、マルチテナント対応
- **Zod**: スキーマバリデーション、型安全性

### データベース・インフラ
- **PostgreSQL 15**: Row Level Security、JSON型、パフォーマンス最適化
- **Vercel Platform**: サーバーレス、エッジ配信、自動スケーリング
- **Docker**: 開発環境統一、コンテナ化

## 開発環境構成

### Docker開発環境
```yaml
# docker-compose.yml 構成
services:
  app:                    # Next.js アプリケーション
    - ポート: 3000
    - ホットリロード対応
    - 環境変数設定
  
  postgres:               # PostgreSQL データベース
    - ポート: 5433
    - データ永続化
    - 初期化スクリプト
  
  pgadmin:               # データベース管理ツール
    - ポート: 8080
    - GUI管理インターフェース
```

### 開発ツール設定
```json
// package.json 主要依存関係
{
  "dependencies": {
    "next": "14.x",
    "react": "18.x",
    "typescript": "5.x",
    "prisma": "latest",
    "next-auth": "latest",
    "zustand": "latest",
    "tailwindcss": "3.x",
    "zod": "latest"
  },
  "devDependencies": {
    "eslint": "latest",
    "prettier": "latest",
    "@types/node": "latest",
    "@types/react": "latest"
  }
}
```

## マルチテナント技術実装

### Row Level Security (RLS)
```sql
-- PostgreSQL RLS 設定パターン
ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON table_name
    FOR ALL TO authenticated
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);

-- セッション設定
SET app.current_tenant_id = 'tenant-uuid-here';
```

### テナント認証フロー
```typescript
// NextAuth.js マルチテナント設定
export const authOptions: NextAuthOptions = {
  providers: [
    // 認証プロバイダー設定
  ],
  callbacks: {
    async session({ session, token }) {
      // テナント情報をセッションに追加
      session.tenantId = token.tenantId;
      return session;
    },
    async jwt({ token, user, account }) {
      // JWTにテナント情報を含める
      if (user) {
        token.tenantId = user.tenantId;
      }
      return token;
    }
  }
};
```

### データアクセス層
```typescript
// Prisma マルチテナント対応
class TenantAwarePrismaClient {
  private prisma: PrismaClient;
  
  constructor(private tenantId: string) {
    this.prisma = new PrismaClient();
  }
  
  async executeQuery<T>(query: () => Promise<T>): Promise<T> {
    // RLS設定
    await this.prisma.$executeRaw`
      SET app.current_tenant_id = ${this.tenantId}
    `;
    
    // クエリ実行
    return await query();
  }
}
```

## API設計・実装パターン

### API Route構造
```typescript
// /app/api/v1/[resource]/route.ts
export async function GET(request: NextRequest) {
  try {
    // 1. 認証チェック
    const session = await getServerSession(authOptions);
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }
    
    // 2. テナント情報取得
    const tenantId = session.tenantId;
    
    // 3. ビジネスロジック実行
    const result = await service.getData(tenantId);
    
    // 4. レスポンス返却
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

### バリデーション・型安全性
```typescript
// Zod スキーマ定義
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

// API での使用
export async function POST(request: NextRequest) {
  const body = await request.json();
  const validatedData = CreateUserSchema.parse(body);
  // 型安全な処理続行
}
```

## フロントエンド技術実装

### App Router活用
```typescript
// app/layout.tsx - ルートレイアウト
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body>
        <SessionProvider>
          <TenantProvider>
            <ThemeProvider>
              {children}
            </ThemeProvider>
          </TenantProvider>
        </SessionProvider>
      </body>
    </html>
  );
}

// app/(dashboard)/page.tsx - ダッシュボード
export default async function DashboardPage() {
  const session = await getServerSession(authOptions);
  const data = await fetchDashboardData(session.tenantId);
  
  return <DashboardComponent data={data} />;
}
```

### 状態管理（Zustand）
```typescript
// stores/appStore.ts
interface AppState {
  // 認証状態
  auth: {
    user: User | null;
    isAuthenticated: boolean;
  };
  
  // テナント状態
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
    // テナント切り替えロジック
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

### コンポーネント設計
```typescript
// components/ui/Button.tsx - 共通UIコンポーネント
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

### Prisma スキーマ設計
```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

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

model TRN_UserProfile {
  user_id       String   @id @default(uuid()) @db.Uuid
  tenant_id     String   @db.Uuid
  emp_no        String   @db.VarChar(20)
  name          String   @db.VarChar(100)
  email         String   @db.VarChar(255)
  created_at    DateTime @default(now())
  updated_at    DateTime @updatedAt
  
  // リレーション
  tenant        MST_Tenant @relation(fields: [tenant_id], references: [tenant_id])
  skills        TRN_SkillAssessment[]
  
  @@unique([tenant_id, emp_no])
  @@map("TRN_UserProfile")
}
```

### マイグレーション管理
```sql
-- migrations/001_enable_rls.sql
-- Row Level Security 有効化
ALTER TABLE "TRN_UserProfile" ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_users ON "TRN_UserProfile"
    FOR ALL TO authenticated
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);

-- インデックス作成
CREATE INDEX idx_user_profile_tenant_id ON "TRN_UserProfile"(tenant_id);
CREATE INDEX idx_user_profile_emp_no ON "TRN_UserProfile"(tenant_id, emp_no);
```

## バッチ処理技術実装

### バッチ基盤アーキテクチャ
```typescript
// lib/batch/BaseBatch.ts
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

### 具体的バッチ実装例
```typescript
// batches/SystemHealthCheckBatch.ts
export class SystemHealthCheckBatch extends BaseBatch {
  constructor() {
    super('BATCH-001');
  }
  
  async execute(): Promise<void> {
    // データベース接続チェック
    await this.checkDatabase();
    
    // API エンドポイントチェック
    await this.checkApiEndpoints();
    
    // リソース使用量チェック
    await this.checkResourceUsage();
    
    // 外部サービス接続チェック
    await this.checkExternalServices();
  }
  
  private async checkDatabase(): Promise<void> {
    // PostgreSQL 接続・性能チェック
  }
  
  private async checkApiEndpoints(): Promise<void> {
    // 主要API エンドポイントの応答チェック
  }
  
  private async checkResourceUsage(): Promise<void> {
    // CPU、メモリ、ディスク使用量チェック
  }
  
  private async checkExternalServices(): Promise<void> {
    // 外部API、メール送信等のチェック
  }
}
```

## セキュリティ技術実装

### 認証・認可
```typescript
// middleware.ts - Next.js ミドルウェア
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

export const config = {
  matcher: [
    '/((?!api/auth|_next/static|_next/image|favicon.ico|login|tenant-select).*)',
  ],
};
```

### データ暗号化
```typescript
// lib/encryption.ts
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

export function decrypt(encryptedText: string): string {
  const [ivHex, authTagHex, encrypted] = encryptedText.split(':');
  
  const iv = Buffer.from(ivHex, 'hex');
  const authTag = Buffer.from(authTagHex, 'hex');
  
  const decipher = crypto.createDecipher(ALGORITHM, ENCRYPTION_KEY);
  decipher.setAAD(Buffer.from('additional-data'));
  decipher.setAuthTag(authTag);
  
  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  
  return decrypted;
}
```

## 監視・ログ技術実装

### 構造化ログ
```typescript
// lib/logger.ts
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
  
  error(message: string, error: Error, context: LogContext) {
    this.winston.error(message, {
      ...context,
      error: {
        message: error.message,
        stack: error.stack
      },
      timestamp: new Date().toISOString()
    });
  }
  
  warn(message: string, context: LogContext) {
    this.winston.warn(message, {
      ...context,
      timestamp: new Date().toISOString()
    });
  }
}

export const logger = new Logger();
```

## パフォーマンス最適化

### キャッシュ戦略
```typescript
// lib/cache.ts
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
  
  async invalidate(pattern: string): Promise<void> {
    const keys = await this.redis.keys(pattern);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }
  
  // テナント別キャッシュキー生成
  tenantKey(tenantId: string, resource: string, id?: string): string {
    return `tenant:${tenantId}:${resource}${id ? `:${id}` : ''}`;
  }
}

export const cache = new CacheManager();
```

この技術コンテキストにより、マルチテナント対応の高性能・高セキュリティなシステムを実現します。
