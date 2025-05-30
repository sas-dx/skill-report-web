# API定義書: API-025 テナント管理API

## 基本情報

| 項目 | 内容 |
|------|------|
| API ID | API-025 |
| API名称 | テナント管理API |
| エンドポイント | /api/tenants |
| 概要 | テナント作成・編集・削除・一覧取得 |
| 利用画面 | SCR-TENANT-ADMIN |
| 優先度 | 最高 |
| 実装予定 | Week 1-2 |

---

## エンドポイント詳細

### 1. テナント一覧取得

#### リクエスト
```http
GET /api/tenants
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### クエリパラメータ
| パラメータ名 | 型 | 必須 | 説明 | 例 |
|-------------|---|------|------|---|
| page | number | × | ページ番号（デフォルト: 1） | 1 |
| limit | number | × | 取得件数（デフォルト: 20） | 20 |
| status | string | × | ステータスフィルタ | active, inactive |
| search | string | × | 検索キーワード | company |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "tenants": [
      {
        "id": "tenant_001",
        "code": "company-a",
        "name": "株式会社A",
        "status": "active",
        "plan": "standard",
        "maxUsers": 100,
        "currentUsers": 45,
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": "2025-01-15T10:30:00Z",
        "settings": {
          "theme": {
            "primaryColor": "#0066cc",
            "secondaryColor": "#f0f0f0",
            "logo": "https://storage.example.com/logos/company-a.png"
          },
          "features": {
            "ssoEnabled": true,
            "notificationEnabled": true,
            "reportingEnabled": true
          }
        }
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 5,
      "totalPages": 1
    }
  }
}
```

#### レスポンス（エラー時）
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "認証が必要です",
    "details": "有効なJWTトークンが必要です"
  }
}
```

### 2. テナント作成

#### リクエスト
```http
POST /api/tenants
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "code": "company-b",
  "name": "株式会社B",
  "plan": "standard",
  "maxUsers": 50,
  "adminUser": {
    "email": "admin@company-b.com",
    "name": "管理者",
    "password": "SecurePassword123!"
  },
  "settings": {
    "theme": {
      "primaryColor": "#ff6600",
      "secondaryColor": "#f5f5f5"
    },
    "features": {
      "ssoEnabled": false,
      "notificationEnabled": true,
      "reportingEnabled": true
    }
  }
}
```

#### バリデーションルール
| フィールド | ルール |
|-----------|--------|
| code | 必須、3-20文字、英数字とハイフンのみ、ユニーク |
| name | 必須、1-100文字 |
| plan | 必須、enum: standard, premium, enterprise |
| maxUsers | 必須、1-10000の整数 |
| adminUser.email | 必須、有効なメールアドレス形式 |
| adminUser.name | 必須、1-50文字 |
| adminUser.password | 必須、8文字以上、英数字記号含む |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "tenant": {
      "id": "tenant_002",
      "code": "company-b",
      "name": "株式会社B",
      "status": "active",
      "plan": "standard",
      "maxUsers": 50,
      "currentUsers": 1,
      "createdAt": "2025-05-30T20:53:00Z",
      "updatedAt": "2025-05-30T20:53:00Z"
    },
    "adminUser": {
      "id": "user_001",
      "email": "admin@company-b.com",
      "name": "管理者",
      "role": "tenant_admin",
      "tenantId": "tenant_002"
    }
  }
}
```

### 3. テナント更新

#### リクエスト
```http
PUT /api/tenants/{tenant_id}
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### パスパラメータ
| パラメータ名 | 型 | 必須 | 説明 |
|-------------|---|------|------|
| tenant_id | string | ○ | テナントID |

#### リクエストボディ
```json
{
  "name": "株式会社B（更新）",
  "plan": "premium",
  "maxUsers": 100,
  "status": "active",
  "settings": {
    "theme": {
      "primaryColor": "#ff6600",
      "secondaryColor": "#f5f5f5",
      "logo": "https://storage.example.com/logos/company-b-new.png"
    },
    "features": {
      "ssoEnabled": true,
      "notificationEnabled": true,
      "reportingEnabled": true
    }
  }
}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "tenant": {
      "id": "tenant_002",
      "code": "company-b",
      "name": "株式会社B（更新）",
      "status": "active",
      "plan": "premium",
      "maxUsers": 100,
      "currentUsers": 1,
      "updatedAt": "2025-05-30T21:00:00Z"
    }
  }
}
```

### 4. テナント削除

#### リクエスト
```http
DELETE /api/tenants/{tenant_id}
Authorization: Bearer {jwt_token}
```

#### パスパラメータ
| パラメータ名 | 型 | 必須 | 説明 |
|-------------|---|------|------|
| tenant_id | string | ○ | テナントID |

#### クエリパラメータ
| パラメータ名 | 型 | 必須 | 説明 |
|-------------|---|------|------|
| force | boolean | × | 強制削除フラグ（デフォルト: false） |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "message": "テナントが正常に削除されました",
    "deletedTenantId": "tenant_002",
    "deletedAt": "2025-05-30T21:05:00Z"
  }
}
```

---

## エラーコード一覧

| エラーコード | HTTPステータス | 説明 | 対処法 |
|-------------|---------------|------|--------|
| UNAUTHORIZED | 401 | 認証エラー | 有効なJWTトークンを設定 |
| FORBIDDEN | 403 | 権限不足 | システム管理者権限が必要 |
| TENANT_NOT_FOUND | 404 | テナントが見つからない | 正しいテナントIDを指定 |
| TENANT_CODE_DUPLICATE | 409 | テナントコードが重複 | 別のテナントコードを指定 |
| VALIDATION_ERROR | 400 | バリデーションエラー | リクエストデータを確認 |
| TENANT_HAS_USERS | 409 | ユーザーが存在するため削除不可 | forceフラグを使用するか、ユーザーを先に削除 |
| INTERNAL_SERVER_ERROR | 500 | サーバー内部エラー | システム管理者に連絡 |

---

## セキュリティ要件

### 認証・認可
- **認証**: JWT Bearer Token必須
- **権限**: システム管理者（system_admin）権限必須
- **テナント分離**: 各テナントのデータは完全分離

### データ保護
- **暗号化**: 機密データはAES-256で暗号化
- **監査ログ**: 全操作を監査ログに記録
- **入力検証**: SQLインジェクション、XSS対策

---

## パフォーマンス要件

| 項目 | 要件 |
|------|------|
| レスポンス時間 | 95%のリクエストが1秒以内 |
| スループット | 100 req/sec |
| 同時接続数 | 50接続 |
| データベース接続 | コネクションプール使用 |

---

## テスト仕様

### 単体テスト
```typescript
describe('Tenant Management API', () => {
  test('GET /api/tenants - 正常系', async () => {
    const response = await request(app)
      .get('/api/tenants')
      .set('Authorization', `Bearer ${adminToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.tenants).toBeInstanceOf(Array);
  });
  
  test('POST /api/tenants - テナント作成', async () => {
    const newTenant = {
      code: 'test-tenant',
      name: 'テストテナント',
      plan: 'standard',
      maxUsers: 10,
      adminUser: {
        email: 'admin@test-tenant.com',
        name: 'テスト管理者',
        password: 'TestPassword123!'
      }
    };
    
    const response = await request(app)
      .post('/api/tenants')
      .set('Authorization', `Bearer ${adminToken}`)
      .send(newTenant)
      .expect(201);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.tenant.code).toBe('test-tenant');
  });
});
```

### 統合テスト
```typescript
describe('Tenant Management Integration', () => {
  test('テナント作成からユーザー登録まで', async () => {
    // 1. テナント作成
    const tenant = await createTenant();
    
    // 2. テナント管理者でログイン
    const adminToken = await loginAsTenantAdmin(tenant.id);
    
    // 3. 一般ユーザー作成
    const user = await createUser(tenant.id, adminToken);
    
    // 4. データ分離確認
    const otherTenantData = await getUsersFromOtherTenant(user.id);
    expect(otherTenantData).toHaveLength(0);
  });
});
```

---

## 実装メモ

### データベーススキーマ
```sql
CREATE TABLE tenants (
  id VARCHAR(50) PRIMARY KEY,
  code VARCHAR(20) UNIQUE NOT NULL,
  name VARCHAR(100) NOT NULL,
  status VARCHAR(20) DEFAULT 'active',
  plan VARCHAR(20) NOT NULL,
  max_users INTEGER NOT NULL,
  current_users INTEGER DEFAULT 0,
  settings JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tenants_code ON tenants(code);
CREATE INDEX idx_tenants_status ON tenants(status);
```

### Next.js実装例
```typescript
// pages/api/tenants/index.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { authenticateToken, requireSystemAdmin } from '@/lib/auth';
import { TenantService } from '@/services/TenantService';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    // 認証・認可チェック
    const user = await authenticateToken(req);
    requireSystemAdmin(user);
    
    const tenantService = new TenantService();
    
    switch (req.method) {
      case 'GET':
        const tenants = await tenantService.getTenants(req.query);
        return res.status(200).json({ success: true, data: tenants });
        
      case 'POST':
        const newTenant = await tenantService.createTenant(req.body);
        return res.status(201).json({ success: true, data: newTenant });
        
      default:
        return res.status(405).json({ success: false, error: 'Method not allowed' });
    }
  } catch (error) {
    return res.status(error.statusCode || 500).json({
      success: false,
      error: {
        code: error.code || 'INTERNAL_SERVER_ERROR',
        message: error.message
      }
    });
  }
}
```

---

## 変更履歴

| 日付 | バージョン | 変更内容 | 変更者 |
|------|-----------|----------|--------|
| 2025-05-30 | 1.0.0 | 初版作成 | システムアーキテクト |
