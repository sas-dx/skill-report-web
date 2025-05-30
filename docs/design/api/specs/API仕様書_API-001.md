# API仕様書: API-001 ユーザー認証API

## 基本情報

| 項目 | 内容 |
|------|------|
| API ID | API-001 |
| API名称 | ユーザー認証API |
| エンドポイント | /api/auth/login |
| 概要 | ユーザーID・パスワードによる認証、JWTトークン発行 |
| 利用画面 | SCR-LOGIN |
| 優先度 | 最高 |
| 実装予定 | Week 1 |

---

## エンドポイント詳細

### 1. ユーザーログイン

#### リクエスト
```http
POST /api/auth/login
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "email": "user@company-a.com",
  "password": "SecurePassword123!",
  "tenantCode": "company-a",
  "rememberMe": false
}
```

#### バリデーションルール
| フィールド | ルール |
|-----------|--------|
| email | 必須、有効なメールアドレス形式 |
| password | 必須、1文字以上 |
| tenantCode | 必須、3-20文字、英数字とハイフンのみ |
| rememberMe | オプション、boolean |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_001",
      "email": "user@company-a.com",
      "name": "田中太郎",
      "role": "user",
      "tenantId": "tenant_001",
      "tenantCode": "company-a",
      "tenantName": "株式会社A",
      "permissions": [
        "profile:read",
        "profile:write",
        "skills:read",
        "skills:write"
      ],
      "lastLoginAt": "2025-05-30T20:54:00Z"
    },
    "tokens": {
      "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "expiresIn": 3600,
      "tokenType": "Bearer"
    },
    "tenant": {
      "id": "tenant_001",
      "code": "company-a",
      "name": "株式会社A",
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
  }
}
```

#### レスポンス（エラー時）
```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "メールアドレスまたはパスワードが正しくありません",
    "details": "認証に失敗しました",
    "remainingAttempts": 2
  }
}
```

### 2. トークンリフレッシュ

#### リクエスト
```http
POST /api/auth/refresh
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "tokens": {
      "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "expiresIn": 3600,
      "tokenType": "Bearer"
    }
  }
}
```

### 3. ログアウト

#### リクエスト
```http
POST /api/auth/logout
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "message": "正常にログアウトしました",
    "loggedOutAt": "2025-05-30T21:00:00Z"
  }
}
```

### 4. パスワードリセット要求

#### リクエスト
```http
POST /api/auth/password-reset-request
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "email": "user@company-a.com",
  "tenantCode": "company-a"
}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "message": "パスワードリセット用のメールを送信しました",
    "email": "user@company-a.com",
    "expiresIn": 1800
  }
}
```

### 5. パスワードリセット実行

#### リクエスト
```http
POST /api/auth/password-reset
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "token": "reset_token_here",
  "newPassword": "NewSecurePassword123!",
  "confirmPassword": "NewSecurePassword123!"
}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "message": "パスワードが正常に変更されました",
    "changedAt": "2025-05-30T21:05:00Z"
  }
}
```

---

## エラーコード一覧

| エラーコード | HTTPステータス | 説明 | 対処法 |
|-------------|---------------|------|--------|
| INVALID_CREDENTIALS | 401 | 認証情報が無効 | 正しいメールアドレス・パスワードを入力 |
| ACCOUNT_LOCKED | 423 | アカウントがロック中 | 管理者に連絡するか、時間をおいて再試行 |
| TENANT_NOT_FOUND | 404 | テナントが見つからない | 正しいテナントコードを入力 |
| TENANT_INACTIVE | 403 | テナントが無効 | テナント管理者に連絡 |
| USER_INACTIVE | 403 | ユーザーが無効 | 管理者に連絡 |
| TOKEN_EXPIRED | 401 | トークンが期限切れ | リフレッシュトークンで更新 |
| TOKEN_INVALID | 401 | トークンが無効 | 再ログインが必要 |
| PASSWORD_RESET_TOKEN_EXPIRED | 400 | リセットトークンが期限切れ | 新しいリセット要求を送信 |
| PASSWORD_VALIDATION_ERROR | 400 | パスワード形式エラー | パスワード要件を確認 |
| TOO_MANY_ATTEMPTS | 429 | ログイン試行回数超過 | 時間をおいて再試行 |
| VALIDATION_ERROR | 400 | バリデーションエラー | リクエストデータを確認 |
| INTERNAL_SERVER_ERROR | 500 | サーバー内部エラー | システム管理者に連絡 |

---

## セキュリティ要件

### 認証セキュリティ
- **パスワードハッシュ化**: bcrypt（ソルト付き）
- **ログイン試行制限**: 5回失敗で30分ロック
- **JWT署名**: RS256アルゴリズム使用
- **トークン有効期限**: アクセストークン1時間、リフレッシュトークン30日

### テナント分離
- **テナント識別**: JWTペイロードにテナントID含有
- **データアクセス制御**: テナントIDによる完全分離
- **権限チェック**: リクエスト毎にテナント・権限検証

### セッション管理
- **セッション固定攻撃対策**: ログイン時にセッションID再生成
- **CSRF対策**: SameSite Cookieとトークン検証
- **XSS対策**: HTTPOnly Cookie使用

---

## パフォーマンス要件

| 項目 | 要件 |
|------|------|
| レスポンス時間 | 95%のリクエストが500ms以内 |
| スループット | 500 req/sec |
| 同時ログイン数 | 1000セッション |
| トークン検証 | 100ms以内 |

---

## JWT仕様

### アクセストークンペイロード
```json
{
  "sub": "user_001",
  "email": "user@company-a.com",
  "name": "田中太郎",
  "role": "user",
  "tenantId": "tenant_001",
  "tenantCode": "company-a",
  "permissions": [
    "profile:read",
    "profile:write",
    "skills:read",
    "skills:write"
  ],
  "iat": 1717104840,
  "exp": 1717108440,
  "iss": "skill-report-system",
  "aud": "skill-report-client"
}
```

### リフレッシュトークンペイロード
```json
{
  "sub": "user_001",
  "tenantId": "tenant_001",
  "tokenType": "refresh",
  "iat": 1717104840,
  "exp": 1719696840,
  "iss": "skill-report-system"
}
```

---

## テスト仕様

### 単体テスト
```typescript
describe('User Authentication API', () => {
  test('POST /api/auth/login - 正常ログイン', async () => {
    const loginData = {
      email: 'test@company-a.com',
      password: 'TestPassword123!',
      tenantCode: 'company-a'
    };
    
    const response = await request(app)
      .post('/api/auth/login')
      .send(loginData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.tokens.accessToken).toBeDefined();
    expect(response.body.data.user.tenantCode).toBe('company-a');
  });
  
  test('POST /api/auth/login - 無効な認証情報', async () => {
    const loginData = {
      email: 'test@company-a.com',
      password: 'WrongPassword',
      tenantCode: 'company-a'
    };
    
    const response = await request(app)
      .post('/api/auth/login')
      .send(loginData)
      .expect(401);
    
    expect(response.body.success).toBe(false);
    expect(response.body.error.code).toBe('INVALID_CREDENTIALS');
  });
  
  test('POST /api/auth/refresh - トークンリフレッシュ', async () => {
    const refreshData = {
      refreshToken: validRefreshToken
    };
    
    const response = await request(app)
      .post('/api/auth/refresh')
      .send(refreshData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.tokens.accessToken).toBeDefined();
  });
});
```

### セキュリティテスト
```typescript
describe('Authentication Security', () => {
  test('ログイン試行回数制限', async () => {
    const loginData = {
      email: 'test@company-a.com',
      password: 'WrongPassword',
      tenantCode: 'company-a'
    };
    
    // 5回失敗させる
    for (let i = 0; i < 5; i++) {
      await request(app).post('/api/auth/login').send(loginData).expect(401);
    }
    
    // 6回目はアカウントロック
    const response = await request(app)
      .post('/api/auth/login')
      .send(loginData)
      .expect(423);
    
    expect(response.body.error.code).toBe('ACCOUNT_LOCKED');
  });
  
  test('テナント間データ分離', async () => {
    const tenantAToken = await loginAsUser('company-a');
    const tenantBToken = await loginAsUser('company-b');
    
    // テナントAのトークンでテナントBのデータにアクセス
    const response = await request(app)
      .get('/api/profiles/tenant-b-user')
      .set('Authorization', `Bearer ${tenantAToken}`)
      .expect(403);
    
    expect(response.body.error.code).toBe('FORBIDDEN');
  });
});
```

---

## 実装メモ

### データベーススキーマ
```sql
CREATE TABLE users (
  id VARCHAR(50) PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(100) NOT NULL,
  role VARCHAR(50) NOT NULL,
  tenant_id VARCHAR(50) NOT NULL,
  status VARCHAR(20) DEFAULT 'active',
  failed_login_attempts INTEGER DEFAULT 0,
  locked_until TIMESTAMP NULL,
  last_login_at TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

CREATE TABLE refresh_tokens (
  id VARCHAR(50) PRIMARY KEY,
  user_id VARCHAR(50) NOT NULL,
  token_hash VARCHAR(255) NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_tenant_id ON users(tenant_id);
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
```

### Next.js実装例
```typescript
// pages/api/auth/login.ts
import { NextApiRequest, NextApiResponse } from 'next';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { AuthService } from '@/services/AuthService';
import { UserService } from '@/services/UserService';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, error: 'Method not allowed' });
  }
  
  try {
    const { email, password, tenantCode, rememberMe } = req.body;
    
    // バリデーション
    if (!email || !password || !tenantCode) {
      return res.status(400).json({
        success: false,
        error: { code: 'VALIDATION_ERROR', message: '必須項目が不足しています' }
      });
    }
    
    const authService = new AuthService();
    const userService = new UserService();
    
    // ユーザー認証
    const user = await userService.findByEmailAndTenant(email, tenantCode);
    if (!user || !await bcrypt.compare(password, user.passwordHash)) {
      await authService.recordFailedLogin(email, tenantCode);
      return res.status(401).json({
        success: false,
        error: { code: 'INVALID_CREDENTIALS', message: '認証に失敗しました' }
      });
    }
    
    // アカウントロックチェック
    if (await authService.isAccountLocked(user.id)) {
      return res.status(423).json({
        success: false,
        error: { code: 'ACCOUNT_LOCKED', message: 'アカウントがロックされています' }
      });
    }
    
    // JWTトークン生成
    const tokens = await authService.generateTokens(user, rememberMe);
    
    // ログイン成功処理
    await authService.recordSuccessfulLogin(user.id);
    
    return res.status(200).json({
      success: true,
      data: {
        user: await userService.getUserProfile(user.id),
        tokens,
        tenant: await userService.getTenantInfo(user.tenantId)
      }
    });
    
  } catch (error) {
    console.error('Login error:', error);
    return res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_SERVER_ERROR', message: 'サーバーエラーが発生しました' }
    });
  }
}
```

---

## 変更履歴

| 日付 | バージョン | 変更内容 | 変更者 |
|------|-----------|----------|--------|
| 2025-05-30 | 1.0.0 | 初版作成 | システムアーキテクト |
