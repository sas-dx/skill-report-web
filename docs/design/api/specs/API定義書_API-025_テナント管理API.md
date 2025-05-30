# API仕様書：テナント管理API

| 項目                | 内容                                                                                |
|---------------------|------------------------------------------------------------------------------------|
| **API ID**          | API-025                                                                            |
| **API名称**         | テナント管理API                                                                    |
| **エンドポイント**  | /api/tenants                                                                       |
| **HTTPメソッド**    | GET/POST/PUT/DELETE                                                                |
| **概要・目的**      | マルチテナント環境でのテナント作成・編集・削除・一覧取得を行う                      |
| **利用画面**        | SCR-TENANT-ADMIN                                                                   |
| **優先度**          | 高                                                                                  |
| **認証要件**        | 必須（システム管理者権限）                                                          |
| **レート制限**      | 100 req/min                                                                        |

## 1. エンドポイント詳細

### 1.1 テナント一覧取得

#### リクエスト
```http
GET /api/tenants?page=1&limit=20&status=active&search=company
Authorization: Bearer {jwt_token}
```

#### クエリパラメータ
| パラメータ名 | 型      | 必須 | 説明                                           |
|--------------|---------|------|------------------------------------------------|
| page         | Integer | No   | ページ番号（デフォルト: 1）                    |
| limit        | Integer | No   | 1ページあたりの件数（デフォルト: 20、最大: 100）|
| status       | String  | No   | ステータスフィルタ（active/inactive/all）      |
| search       | String  | No   | 検索キーワード（名前・コードで部分一致）       |
| sortBy       | String  | No   | ソート項目（name/code/createdAt）              |
| sortOrder    | String  | No   | ソート順（asc/desc、デフォルト: asc）          |

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
        "domain": "company-a.com",
        "status": "active",
        "plan": "enterprise",
        "userCount": 150,
        "maxUsers": 200,
        "storageUsed": 2048,
        "storageLimit": 10240,
        "features": {
          "ssoEnabled": true,
          "apiAccess": true,
          "customBranding": true,
          "advancedReporting": true
        },
        "billing": {
          "monthlyFee": 50000,
          "currency": "JPY",
          "billingCycle": "monthly",
          "nextBillingDate": "2025-06-30"
        },
        "createdAt": "2025-01-15T09:00:00Z",
        "updatedAt": "2025-05-30T10:30:00Z"
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 5,
      "totalItems": 95,
      "itemsPerPage": 20,
      "hasNext": true,
      "hasPrev": false
    }
  }
}
```

### 1.2 テナント詳細取得

#### リクエスト
```http
GET /api/tenants/{tenant_id}
Authorization: Bearer {jwt_token}
```

#### パスパラメータ
| パラメータ名 | 型     | 必須 | 説明       |
|--------------|--------|------|------------|
| tenant_id    | String | Yes  | テナントID |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "tenant": {
      "id": "tenant_001",
      "code": "company-a",
      "name": "株式会社A",
      "domain": "company-a.com",
      "description": "大手製造業企業",
      "status": "active",
      "plan": "enterprise",
      "settings": {
        "theme": {
          "primaryColor": "#0066cc",
          "secondaryColor": "#f0f0f0",
          "logo": "https://storage.example.com/logos/company-a.png",
          "favicon": "https://storage.example.com/favicons/company-a.ico"
        },
        "features": {
          "ssoEnabled": true,
          "apiAccess": true,
          "customBranding": true,
          "advancedReporting": true,
          "dataExport": true,
          "auditLog": true
        },
        "security": {
          "passwordPolicy": {
            "minLength": 8,
            "requireUppercase": true,
            "requireLowercase": true,
            "requireNumbers": true,
            "requireSymbols": true,
            "maxAge": 90
          },
          "sessionTimeout": 3600,
          "ipWhitelist": ["192.168.1.0/24", "10.0.0.0/8"],
          "mfaRequired": false
        },
        "notifications": {
          "emailEnabled": true,
          "slackEnabled": true,
          "teamsEnabled": false,
          "lineWorksEnabled": false
        }
      },
      "usage": {
        "userCount": 150,
        "maxUsers": 200,
        "storageUsed": 2048,
        "storageLimit": 10240,
        "apiCallsThisMonth": 45000,
        "apiCallsLimit": 100000
      },
      "billing": {
        "plan": "enterprise",
        "monthlyFee": 50000,
        "currency": "JPY",
        "billingCycle": "monthly",
        "nextBillingDate": "2025-06-30",
        "paymentMethod": "bank_transfer",
        "billingContact": {
          "name": "経理部",
          "email": "billing@company-a.com",
          "phone": "03-1234-5678"
        }
      },
      "contacts": {
        "primary": {
          "name": "田中太郎",
          "email": "tanaka@company-a.com",
          "phone": "03-1234-5678",
          "role": "システム管理者"
        },
        "billing": {
          "name": "経理部",
          "email": "billing@company-a.com",
          "phone": "03-1234-5679"
        }
      },
      "createdAt": "2025-01-15T09:00:00Z",
      "updatedAt": "2025-05-30T10:30:00Z"
    }
  }
}
```

### 1.3 テナント作成

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
  "domain": "company-b.com",
  "description": "IT企業",
  "plan": "standard",
  "maxUsers": 100,
  "storageLimit": 5120,
  "settings": {
    "theme": {
      "primaryColor": "#ff6600",
      "secondaryColor": "#f5f5f5"
    },
    "features": {
      "ssoEnabled": false,
      "apiAccess": true,
      "customBranding": false,
      "advancedReporting": false
    },
    "security": {
      "passwordPolicy": {
        "minLength": 8,
        "requireUppercase": true,
        "requireLowercase": true,
        "requireNumbers": true,
        "requireSymbols": false
      },
      "sessionTimeout": 3600,
      "mfaRequired": false
    }
  },
  "contacts": {
    "primary": {
      "name": "佐藤花子",
      "email": "sato@company-b.com",
      "phone": "03-9876-5432",
      "role": "システム管理者"
    },
    "billing": {
      "name": "経理部",
      "email": "billing@company-b.com",
      "phone": "03-9876-5433"
    }
  }
}
```

#### バリデーションルール
| フィールド | ルール |
|-----------|--------|
| code | 必須、3-20文字、英数字とハイフンのみ、一意 |
| name | 必須、1-100文字 |
| domain | 必須、有効なドメイン形式、一意 |
| plan | 必須、有効なプラン（trial/standard/enterprise） |
| maxUsers | 必須、1以上の整数 |
| storageLimit | 必須、1以上の整数（MB単位） |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "tenant": {
      "id": "tenant_002",
      "code": "company-b",
      "name": "株式会社B",
      "domain": "company-b.com",
      "status": "active",
      "plan": "standard",
      "createdAt": "2025-05-30T11:00:00Z"
    },
    "adminUser": {
      "id": "user_admin_002",
      "email": "sato@company-b.com",
      "temporaryPassword": "TempPass123!",
      "passwordResetRequired": true
    }
  }
}
```

### 1.4 テナント更新

#### リクエスト
```http
PUT /api/tenants/{tenant_id}
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "name": "株式会社B（更新後）",
  "description": "IT企業（更新）",
  "plan": "enterprise",
  "maxUsers": 200,
  "storageLimit": 10240,
  "settings": {
    "theme": {
      "primaryColor": "#0066cc",
      "secondaryColor": "#f0f0f0"
    },
    "features": {
      "ssoEnabled": true,
      "apiAccess": true,
      "customBranding": true,
      "advancedReporting": true
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
      "name": "株式会社B（更新後）",
      "plan": "enterprise",
      "updatedAt": "2025-05-30T11:30:00Z"
    }
  }
}
```

### 1.5 テナント削除

#### リクエスト
```http
DELETE /api/tenants/{tenant_id}
Authorization: Bearer {jwt_token}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "message": "テナントが正常に削除されました",
    "deletedTenantId": "tenant_002",
    "deletedAt": "2025-05-30T12:00:00Z"
  }
}
```

## 2. エラーレスポンス

### 2.1 共通エラーフォーマット
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "エラーメッセージ",
    "details": "詳細情報",
    "field": "エラーフィールド（バリデーションエラーの場合）"
  }
}
```

### 2.2 エラーコード一覧
| エラーコード | HTTPステータス | 説明 |
|-------------|---------------|------|
| TENANT_NOT_FOUND | 404 | テナントが見つからない |
| TENANT_CODE_DUPLICATE | 409 | テナントコードが重複 |
| TENANT_DOMAIN_DUPLICATE | 409 | ドメインが重複 |
| INVALID_PLAN | 400 | 無効なプラン |
| INSUFFICIENT_PERMISSIONS | 403 | 権限不足 |
| TENANT_HAS_USERS | 409 | ユーザーが存在するため削除不可 |
| VALIDATION_ERROR | 400 | バリデーションエラー |

## 3. 実装仕様

### 3.1 データベーススキーマ
```sql
CREATE TABLE tenants (
  id VARCHAR(50) PRIMARY KEY,
  code VARCHAR(20) UNIQUE NOT NULL,
  name VARCHAR(100) NOT NULL,
  domain VARCHAR(255) UNIQUE NOT NULL,
  description TEXT,
  status VARCHAR(20) DEFAULT 'active',
  plan VARCHAR(20) NOT NULL,
  max_users INTEGER NOT NULL,
  storage_limit INTEGER NOT NULL,
  settings JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tenant_contacts (
  id VARCHAR(50) PRIMARY KEY,
  tenant_id VARCHAR(50) NOT NULL,
  contact_type VARCHAR(20) NOT NULL,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(20),
  role VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);
```

### 3.2 セキュリティ要件
- システム管理者権限必須
- テナント間データ完全分離
- 監査ログ記録
- レート制限適用

## 4. 改訂履歴

| 改訂日     | 改訂者 | 改訂内容                                         |
|------------|--------|--------------------------------------------------|
| 2025/05/30 | 初版   | 初版作成                                         |
