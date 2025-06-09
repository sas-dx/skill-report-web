# マルチテナント開発ガイドライン（将来対応）

## 基本方針

### 現在の状況（2025年6月）
- **現在の実装**: シングルテナント設計で開発中
- **設計書**: マルチテナント対応として設計済み
- **将来計画**: Phase 2以降でマルチテナント化を検討
- **段階的移行**: 現在のシングルテナント実装を完成後、マルチテナント化

### 将来のマルチテナント要件
- **データ分離**: テナント間の完全なデータ分離
- **UI分離**: テナント別のカラーテーマ・ロゴ設定
- **権限分離**: テナント別の権限管理・アクセス制御
- **通知分離**: テナント別の通知設定・連携サービス

### 移行時の設計原則
- **後方互換性**: 現在のシングルテナント実装との互換性維持
- **段階的移行**: 機能単位での段階的なマルチテナント化
- **データ移行**: 既存データの安全な移行
- **運用継続**: サービス停止を最小限に抑えた移行

## データ分離実装パターン

### 1. データベース設計

#### テナントID必須化
```sql
-- 全テーブルにtenant_idカラムを必須で追加
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    tenant_id VARCHAR(50) NOT NULL,
    emp_no VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- テナント内での一意制約
    UNIQUE(tenant_id, emp_no),
    UNIQUE(tenant_id, email)
);

-- インデックス設定（パフォーマンス最適化）
CREATE INDEX idx_users_tenant_id ON users(tenant_id);
CREATE INDEX idx_users_tenant_emp_no ON users(tenant_id, emp_no);
```

#### 外部キー制約でのテナント分離
```sql
-- 関連テーブル間でのテナント分離保証
CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    tenant_id VARCHAR(50) NOT NULL,
    user_id INTEGER NOT NULL,
    skill_category VARCHAR(100) NOT NULL,
    skill_level INTEGER CHECK (skill_level >= 1 AND skill_level <= 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 同一テナント内での外部キー制約
    FOREIGN KEY (tenant_id, user_id) 
    REFERENCES users(tenant_id, id) ON DELETE CASCADE
);
```

### 2. Prisma設定

#### スキーマ定義
```prisma
model User {
  id        Int      @id @default(autoincrement())
  tenantId  String   @map("tenant_id")
  empNo     String   @map("emp_no")
  name      String
  email     String
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")
  
  // リレーション（テナント分離考慮）
  skills    Skill[]
  
  // 複合一意制約
  @@unique([tenantId, empNo])
  @@unique([tenantId, email])
  @@index([tenantId])
  @@map("users")
}

model Skill {
  id            Int      @id @default(autoincrement())
  tenantId      String   @map("tenant_id")
  userId        Int      @map("user_id")
  skillCategory String   @map("skill_category")
  skillLevel    Int      @map("skill_level")
  createdAt     DateTime @default(now()) @map("created_at")
  
  // リレーション
  user User @relation(fields: [tenantId, userId], references: [tenantId, id])
  
  @@index([tenantId])
  @@index([tenantId, userId])
  @@map("skills")
}
```

#### データアクセス層
```typescript
// lib/prisma-tenant.ts
import { PrismaClient } from '@prisma/client';

export class TenantPrismaClient {
  private prisma: PrismaClient;
  private tenantId: string;

  constructor(tenantId: string) {
    this.prisma = new PrismaClient();
    this.tenantId = tenantId;
  }

  // テナント分離されたユーザー取得
  async getUsers() {
    return this.prisma.user.findMany({
      where: { tenantId: this.tenantId }
    });
  }

  // テナント分離されたユーザー作成
  async createUser(data: Omit<User, 'id' | 'tenantId' | 'createdAt' | 'updatedAt'>) {
    return this.prisma.user.create({
      data: {
        ...data,
        tenantId: this.tenantId
      }
    });
  }

  // テナント分離されたスキル取得
  async getUserSkills(userId: number) {
    return this.prisma.skill.findMany({
      where: {
        tenantId: this.tenantId,
        userId: userId
      }
    });
  }
}
```

## 認証・認可実装

### 1. JWT + テナント識別

#### JWT ペイロード設計
```typescript
// types/auth.ts
export interface JWTPayload {
  userId: number;
  tenantId: string;
  empNo: string;
  email: string;
  role: string;
  permissions: string[];
  iat: number;
  exp: number;
}
```

#### 認証ミドルウェア
```typescript
// lib/auth-middleware.ts
import jwt from 'jsonwebtoken';
import { NextRequest } from 'next/server';

export async function verifyTenantAuth(request: NextRequest) {
  const token = request.headers.get('authorization')?.replace('Bearer ', '');
  
  if (!token) {
    throw new Error('認証トークンが必要です');
  }

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!) as JWTPayload;
    
    // テナントIDの検証
    const requestTenantId = request.headers.get('x-tenant-id');
    if (payload.tenantId !== requestTenantId) {
      throw new Error('テナントIDが一致しません');
    }

    return payload;
  } catch (error) {
    throw new Error('無効な認証トークンです');
  }
}
```

### 2. API Routes でのテナント分離

#### API Route 実装例
```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { verifyTenantAuth } from '@/lib/auth-middleware';
import { TenantPrismaClient } from '@/lib/prisma-tenant';

export async function GET(request: NextRequest) {
  try {
    // 認証・テナント検証
    const auth = await verifyTenantAuth(request);
    
    // テナント分離されたデータアクセス
    const prisma = new TenantPrismaClient(auth.tenantId);
    const users = await prisma.getUsers();

    return NextResponse.json({
      success: true,
      data: users
    });
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: error.message
    }, { status: 401 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const auth = await verifyTenantAuth(request);
    const userData = await request.json();

    // 入力値検証
    if (!userData.empNo || !userData.name || !userData.email) {
      return NextResponse.json({
        success: false,
        error: '必須項目が不足しています'
      }, { status: 400 });
    }

    const prisma = new TenantPrismaClient(auth.tenantId);
    const user = await prisma.createUser(userData);

    return NextResponse.json({
      success: true,
      data: user
    }, { status: 201 });
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: error.message
    }, { status: 500 });
  }
}
```

## UI分離実装

### 1. テナント別設定管理

#### テナント設定型定義
```typescript
// types/tenant.ts
export interface TenantConfig {
  tenantId: string;
  name: string;
  logo: string;
  primaryColor: string;
  secondaryColor: string;
  accentColor: string;
  fontFamily: string;
  locale: string;
  timezone: string;
  features: {
    skillManagement: boolean;
    careerPlanning: boolean;
    workTracking: boolean;
    training: boolean;
    reporting: boolean;
  };
}
```

#### テナント設定プロバイダー
```typescript
// components/providers/TenantProvider.tsx
'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { TenantConfig } from '@/types/tenant';

const TenantContext = createContext<TenantConfig | null>(null);

export function TenantProvider({ 
  children, 
  tenantId 
}: { 
  children: React.ReactNode;
  tenantId: string;
}) {
  const [config, setConfig] = useState<TenantConfig | null>(null);

  useEffect(() => {
    async function loadTenantConfig() {
      try {
        const response = await fetch(`/api/tenant/${tenantId}/config`);
        const data = await response.json();
        setConfig(data.config);
        
        // CSS変数でテーマ設定
        document.documentElement.style.setProperty('--primary-color', data.config.primaryColor);
        document.documentElement.style.setProperty('--secondary-color', data.config.secondaryColor);
        document.documentElement.style.setProperty('--accent-color', data.config.accentColor);
      } catch (error) {
        console.error('テナント設定の読み込みに失敗しました:', error);
      }
    }

    loadTenantConfig();
  }, [tenantId]);

  return (
    <TenantContext.Provider value={config}>
      {children}
    </TenantContext.Provider>
  );
}

export function useTenant() {
  const context = useContext(TenantContext);
  if (!context) {
    throw new Error('useTenant must be used within a TenantProvider');
  }
  return context;
}
```

### 2. テナント別コンポーネント

#### ヘッダーコンポーネント
```typescript
// components/tenant/TenantHeader.tsx
import { useTenant } from '@/components/providers/TenantProvider';
import Image from 'next/image';

export function TenantHeader() {
  const tenant = useTenant();

  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Image
              src={tenant.logo}
              alt={`${tenant.name} ロゴ`}
              width={120}
              height={40}
              className="h-8 w-auto"
            />
            <h1 className="ml-4 text-xl font-semibold text-gray-900">
              {tenant.name} スキル報告書システム
            </h1>
          </div>
        </div>
      </div>
    </header>
  );
}
```

## 通知分離実装

### 1. テナント別通知設定

#### 通知設定型定義
```typescript
// types/notification.ts
export interface NotificationConfig {
  tenantId: string;
  email: {
    enabled: boolean;
    smtpHost: string;
    smtpPort: number;
    smtpUser: string;
    smtpPassword: string;
    fromAddress: string;
    fromName: string;
  };
  teams: {
    enabled: boolean;
    webhookUrl: string;
  };
  lineWorks: {
    enabled: boolean;
    botToken: string;
    channelId: string;
  };
}
```

#### 通知サービス
```typescript
// lib/notification-service.ts
export class TenantNotificationService {
  private tenantId: string;
  private config: NotificationConfig;

  constructor(tenantId: string, config: NotificationConfig) {
    this.tenantId = tenantId;
    this.config = config;
  }

  async sendSkillUpdateNotification(userId: number, skillData: any) {
    const notifications = [];

    // メール通知
    if (this.config.email.enabled) {
      notifications.push(this.sendEmail({
        to: skillData.userEmail,
        subject: 'スキル情報が更新されました',
        template: 'skill-update',
        data: skillData
      }));
    }

    // Teams通知
    if (this.config.teams.enabled) {
      notifications.push(this.sendTeamsMessage({
        text: `${skillData.userName}さんがスキル情報を更新しました`,
        data: skillData
      }));
    }

    // LINE WORKS通知
    if (this.config.lineWorks.enabled) {
      notifications.push(this.sendLineWorksMessage({
        text: `スキル更新: ${skillData.userName}`,
        data: skillData
      }));
    }

    await Promise.all(notifications);
  }

  private async sendEmail(params: any) {
    // テナント別SMTP設定でメール送信
  }

  private async sendTeamsMessage(params: any) {
    // テナント別Teams Webhook URLで通知送信
  }

  private async sendLineWorksMessage(params: any) {
    // テナント別LINE WORKS設定で通知送信
  }
}
```

## セキュリティ・監査

### 1. テナント分離監査

#### 監査ログ記録
```typescript
// lib/audit-logger.ts
export interface AuditLog {
  tenantId: string;
  userId: number;
  action: string;
  resource: string;
  resourceId: string;
  details: any;
  ipAddress: string;
  userAgent: string;
  timestamp: Date;
}

export class TenantAuditLogger {
  private tenantId: string;

  constructor(tenantId: string) {
    this.tenantId = tenantId;
  }

  async log(params: Omit<AuditLog, 'tenantId' | 'timestamp'>) {
    const auditLog: AuditLog = {
      ...params,
      tenantId: this.tenantId,
      timestamp: new Date()
    };

    // データベースに記録
    await prisma.auditLog.create({
      data: auditLog
    });

    // セキュリティ監視システムに送信
    await this.sendToSecurityMonitoring(auditLog);
  }

  private async sendToSecurityMonitoring(log: AuditLog) {
    // セキュリティ監視システムへの送信
  }
}
```

### 2. テナント間アクセス防止

#### ミドルウェア実装
```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server';
import { verifyTenantAuth } from '@/lib/auth-middleware';

export async function middleware(request: NextRequest) {
  // API ルートのテナント分離チェック
  if (request.nextUrl.pathname.startsWith('/api/')) {
    try {
      const auth = await verifyTenantAuth(request);
      
      // リクエストヘッダーにテナント情報を追加
      const requestHeaders = new Headers(request.headers);
      requestHeaders.set('x-tenant-id', auth.tenantId);
      requestHeaders.set('x-user-id', auth.userId.toString());

      return NextResponse.next({
        request: {
          headers: requestHeaders,
        },
      });
    } catch (error) {
      return NextResponse.json({
        success: false,
        error: 'Unauthorized'
      }, { status: 401 });
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/api/:path*']
};
```

## パフォーマンス最適化

### 1. テナント別キャッシュ戦略

#### Redis キャッシュ実装
```typescript
// lib/tenant-cache.ts
import Redis from 'ioredis';

export class TenantCache {
  private redis: Redis;
  private tenantId: string;

  constructor(tenantId: string) {
    this.redis = new Redis(process.env.REDIS_URL!);
    this.tenantId = tenantId;
  }

  private getKey(key: string): string {
    return `tenant:${this.tenantId}:${key}`;
  }

  async get<T>(key: string): Promise<T | null> {
    const data = await this.redis.get(this.getKey(key));
    return data ? JSON.parse(data) : null;
  }

  async set<T>(key: string, value: T, ttl: number = 3600): Promise<void> {
    await this.redis.setex(
      this.getKey(key),
      ttl,
      JSON.stringify(value)
    );
  }

  async del(key: string): Promise<void> {
    await this.redis.del(this.getKey(key));
  }

  async invalidatePattern(pattern: string): Promise<void> {
    const keys = await this.redis.keys(this.getKey(pattern));
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }
}
```

## 運用・監視

### 1. テナント別メトリクス

#### メトリクス収集
```typescript
// lib/tenant-metrics.ts
export class TenantMetrics {
  private tenantId: string;

  constructor(tenantId: string) {
    this.tenantId = tenantId;
  }

  async recordApiCall(endpoint: string, duration: number, status: number) {
    // メトリクス記録
    await this.sendMetric('api_call', {
      tenant_id: this.tenantId,
      endpoint,
      duration,
      status,
      timestamp: Date.now()
    });
  }

  async recordUserAction(userId: number, action: string) {
    await this.sendMetric('user_action', {
      tenant_id: this.tenantId,
      user_id: userId,
      action,
      timestamp: Date.now()
    });
  }

  private async sendMetric(type: string, data: any) {
    // 監視システムにメトリクス送信
  }
}
```

## 禁止事項・注意事項

### 禁止事項
- テナントIDなしのデータアクセス
- 異なるテナント間でのデータ参照
- テナント情報のハードコーディング
- テナント分離を考慮しないクエリ実行

### 注意事項
- 全データアクセスでテナントID検証を実施
- 外部キー制約でテナント分離を保証
- キャッシュキーにテナントIDを含める
- 監査ログにテナント情報を記録

---

このマルチテナント開発ガイドラインに従って、安全で効率的なマルチテナントシステムを構築してください。
