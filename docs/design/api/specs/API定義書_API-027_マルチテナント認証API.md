# API定義書: API-027 マルチテナント認証API

## 基本情報

| 項目 | 内容 |
|------|------|
| API ID | API-027 |
| API名称 | マルチテナント認証API |
| エンドポイント | /api/auth/tenant |
| 概要 | テナント選択・認証 |
| 利用画面 | SCR-TENANT-SELECT, SCR-LOGIN |
| 優先度 | 最高 |
| 実装予定 | Week 1 |

---

## エンドポイント詳細

### 1. テナント一覧取得

#### リクエスト
```http
GET /api/auth/tenant/list
Content-Type: application/json
```

#### クエリパラメータ
| パラメータ名 | 型 | 必須 | 説明 | 例 |
|-------------|---|------|------|---|
| email | string | × | メールアドレス（所属テナント絞り込み） | user@company-a.com |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "tenants": [
      {
        "id": "tenant_001",
        "name": "株式会社A",
        "domain": "company-a.com",
        "subdomain": "company-a",
        "logoUrl": "https://storage.example.com/logos/company-a.png",
        "theme": {
          "primaryColor": "#1976d2",
          "secondaryColor": "#424242"
        },
        "status": "active",
        "plan": "premium",
        "userCount": 150,
        "maxUsers": 200
      },
      {
        "id": "tenant_002",
        "name": "株式会社B",
        "domain": "company-b.com",
        "subdomain": "company-b",
        "logoUrl": "https://storage.example.com/logos/company-b.png",
        "theme": {
          "primaryColor": "#4caf50",
          "secondaryColor": "#757575"
        },
        "status": "active",
        "plan": "standard",
        "userCount": 45,
        "maxUsers": 50
      }
    ],
    "totalCount": 2
  }
}
```

### 2. テナント選択・認証

#### リクエスト
```http
POST /api/auth/tenant
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "tenantId": "tenant_001",
  "email": "tanaka@company-a.com",
  "password": "SecurePassword123!",
  "rememberMe": true
}
```

#### バリデーションルール
| フィールド | ルール |
|-----------|--------|
| tenantId | 必須、有効なテナントID |
| email | 必須、有効なメールアドレス形式 |
| password | 必須、8文字以上、英数字記号含む |
| rememberMe | 任意、boolean |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_001",
      "email": "tanaka@company-a.com",
      "employeeId": "EMP001",
      "displayName": "田中太郎",
      "role": "user",
      "permissions": [
        "profile:read",
        "profile:write",
        "skills:read",
        "skills:write",
        "goals:read",
        "goals:write"
      ],
      "lastLoginAt": "2025-05-30T21:06:00Z"
    },
    "tenant": {
      "id": "tenant_001",
      "name": "株式会社A",
      "domain": "company-a.com",
      "subdomain": "company-a",
      "logoUrl": "https://storage.example.com/logos/company-a.png",
      "theme": {
        "primaryColor": "#1976d2",
        "secondaryColor": "#424242",
        "fontFamily": "Noto Sans JP",
        "borderRadius": "4px"
      },
      "features": {
        "skillMap": true,
        "goalTracking": true,
        "reporting": true,
        "notifications": true,
        "sso": false
      },
      "settings": {
        "language": "ja",
        "timezone": "Asia/Tokyo",
        "dateFormat": "YYYY-MM-DD",
        "skillLevels": ["×", "△", "○", "◎"]
      }
    },
    "tokens": {
      "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refreshToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
      "expiresIn": 3600,
      "tokenType": "Bearer"
    },
    "session": {
      "sessionId": "sess_001",
      "expiresAt": "2025-05-31T21:06:00Z",
      "rememberMe": true
    }
  }
}
```

### 3. テナント切り替え

#### リクエスト
```http
POST /api/auth/tenant/switch
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "tenantId": "tenant_002"
}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "tenant": {
      "id": "tenant_002",
      "name": "株式会社B",
      "domain": "company-b.com",
      "subdomain": "company-b",
      "logoUrl": "https://storage.example.com/logos/company-b.png",
      "theme": {
        "primaryColor": "#4caf50",
        "secondaryColor": "#757575",
        "fontFamily": "Noto Sans JP",
        "borderRadius": "8px"
      },
      "features": {
        "skillMap": true,
        "goalTracking": false,
        "reporting": true,
        "notifications": true,
        "sso": true
      }
    },
    "tokens": {
      "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refreshToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
      "expiresIn": 3600,
      "tokenType": "Bearer"
    },
    "permissions": [
      "profile:read",
      "skills:read",
      "skills:write"
    ]
  }
}
```

### 4. テナント認証状態確認

#### リクエスト
```http
GET /api/auth/tenant/verify
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "valid": true,
    "user": {
      "id": "user_001",
      "email": "tanaka@company-a.com",
      "displayName": "田中太郎",
      "role": "user"
    },
    "tenant": {
      "id": "tenant_001",
      "name": "株式会社A",
      "status": "active"
    },
    "session": {
      "sessionId": "sess_001",
      "expiresAt": "2025-05-31T21:06:00Z",
      "lastActivity": "2025-05-30T21:06:00Z"
    },
    "tokenInfo": {
      "issuedAt": "2025-05-30T21:06:00Z",
      "expiresAt": "2025-05-30T22:06:00Z",
      "remainingTime": 3540
    }
  }
}
```

### 5. テナント認証ログアウト

#### リクエスト
```http
POST /api/auth/tenant/logout
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "logoutAll": false
}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "message": "ログアウトが完了しました",
    "sessionId": "sess_001",
    "loggedOutAt": "2025-05-30T21:10:00Z",
    "allSessions": false
  }
}
```

---

## エラーコード一覧

| エラーコード | HTTPステータス | 説明 | 対処法 |
|-------------|---------------|------|--------|
| INVALID_CREDENTIALS | 401 | 認証情報が無効 | メールアドレス・パスワードを確認 |
| TENANT_NOT_FOUND | 404 | テナントが見つからない | 正しいテナントIDを指定 |
| TENANT_INACTIVE | 403 | テナントが無効 | テナント管理者に連絡 |
| USER_NOT_IN_TENANT | 403 | ユーザーがテナントに所属していない | 正しいテナントを選択 |
| ACCOUNT_LOCKED | 423 | アカウントがロック中 | 時間をおいて再試行 |
| PASSWORD_EXPIRED | 401 | パスワードが期限切れ | パスワードを更新 |
| TENANT_LIMIT_EXCEEDED | 403 | テナントユーザー数上限 | プラン変更またはユーザー削除 |
| SESSION_EXPIRED | 401 | セッション期限切れ | 再ログインが必要 |
| INVALID_TOKEN | 401 | トークンが無効 | 新しいトークンを取得 |
| TENANT_SWITCH_FORBIDDEN | 403 | テナント切り替え権限なし | 管理者に権限付与を依頼 |
| VALIDATION_ERROR | 400 | バリデーションエラー | リクエストデータを確認 |
| INTERNAL_SERVER_ERROR | 500 | サーバー内部エラー | システム管理者に連絡 |

---

## セキュリティ要件

### 認証・認可
- **パスワード**: bcrypt（コスト12）でハッシュ化
- **JWT**: RS256署名、1時間有効期限
- **リフレッシュトークン**: 30日有効期限、ローテーション
- **セッション管理**: Redis使用、自動期限切れ

### セキュリティ対策
- **ログイン試行制限**: 5回失敗で30分ロック
- **ブルートフォース対策**: IP別レート制限
- **CSRF対策**: SameSite Cookie、CSRFトークン
- **XSS対策**: Content Security Policy

### 監査・ログ
- **認証ログ**: 成功・失敗を記録
- **テナント切り替えログ**: 全切り替えを記録
- **セッション管理**: 作成・更新・削除を記録

---

## パフォーマンス要件

| 項目 | 要件 |
|------|------|
| レスポンス時間 | 95%のリクエストが800ms以内 |
| スループット | 200 req/sec |
| 同時セッション | 10,000セッション |
| キャッシュ | Redis使用、TTL 300秒 |

---

## テスト仕様

### 単体テスト
```typescript
describe('Multi-Tenant Auth API', () => {
  test('GET /api/auth/tenant/list - テナント一覧取得', async () => {
    const response = await request(app)
      .get('/api/auth/tenant/list')
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.tenants).toBeInstanceOf(Array);
    expect(response.body.data.tenants[0]).toHaveProperty('id');
    expect(response.body.data.tenants[0]).toHaveProperty('name');
  });
  
  test('POST /api/auth/tenant - 正常認証', async () => {
    const loginData = {
      tenantId: 'tenant_001',
      email: 'tanaka@company-a.com',
      password: 'SecurePassword123!',
      rememberMe: true
    };
    
    const response = await request(app)
      .post('/api/auth/tenant')
      .send(loginData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.user).toBeDefined();
    expect(response.body.data.tenant).toBeDefined();
    expect(response.body.data.tokens.accessToken).toBeDefined();
    expect(response.body.data.tokens.refreshToken).toBeDefined();
  });
  
  test('POST /api/auth/tenant - 無効な認証情報', async () => {
    const loginData = {
      tenantId: 'tenant_001',
      email: 'tanaka@company-a.com',
      password: 'wrongpassword',
      rememberMe: false
    };
    
    const response = await request(app)
      .post('/api/auth/tenant')
      .send(loginData)
      .expect(401);
    
    expect(response.body.success).toBe(false);
    expect(response.body.error.code).toBe('INVALID_CREDENTIALS');
  });
  
  test('POST /api/auth/tenant/switch - テナント切り替え', async () => {
    const switchData = { tenantId: 'tenant_002' };
    
    const response = await request(app)
      .post('/api/auth/tenant/switch')
      .set('Authorization', `Bearer ${validToken}`)
      .send(switchData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.tenant.id).toBe('tenant_002');
    expect(response.body.data.tokens.accessToken).toBeDefined();
  });
  
  test('GET /api/auth/tenant/verify - 認証状態確認', async () => {
    const response = await request(app)
      .get('/api/auth/tenant/verify')
      .set('Authorization', `Bearer ${validToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.valid).toBe(true);
    expect(response.body.data.user).toBeDefined();
    expect(response.body.data.tenant).toBeDefined();
  });
});
```

### 統合テスト
```typescript
describe('Multi-Tenant Auth Integration', () => {
  test('完全な認証フロー', async () => {
    // 1. テナント一覧取得
    const tenantsResponse = await getTenantList();
    expect(tenantsResponse.data.tenants.length).toBeGreaterThan(0);
    
    // 2. テナント認証
    const authResponse = await authenticateWithTenant('tenant_001', 'user@company-a.com', 'password');
    expect(authResponse.data.tokens.accessToken).toBeDefined();
    
    // 3. 認証状態確認
    const verifyResponse = await verifyTenantAuth(authResponse.data.tokens.accessToken);
    expect(verifyResponse.data.valid).toBe(true);
    
    // 4. テナント切り替え
    const switchResponse = await switchTenant('tenant_002', authResponse.data.tokens.accessToken);
    expect(switchResponse.data.tenant.id).toBe('tenant_002');
    
    // 5. ログアウト
    const logoutResponse = await logoutFromTenant(switchResponse.data.tokens.accessToken);
    expect(logoutResponse.data.message).toContain('ログアウト');
  });
  
  test('セキュリティ制約確認', async () => {
    // 1. ログイン試行制限テスト
    for (let i = 0; i < 6; i++) {
      await request(app)
        .post('/api/auth/tenant')
        .send({
          tenantId: 'tenant_001',
          email: 'test@company-a.com',
          password: 'wrongpassword'
        });
    }
    
    // 6回目でアカウントロック
    const response = await request(app)
      .post('/api/auth/tenant')
      .send({
        tenantId: 'tenant_001',
        email: 'test@company-a.com',
        password: 'correctpassword'
      })
      .expect(423);
    
    expect(response.body.error.code).toBe('ACCOUNT_LOCKED');
  });
  
  test('テナント分離確認', async () => {
    // テナントAでログイン
    const authA = await authenticateWithTenant('tenant_a', 'user@company-a.com', 'password');
    
    // テナントBのデータにアクセス試行
    const response = await request(app)
      .get('/api/profiles/tenant-b-user')
      .set('Authorization', `Bearer ${authA.data.tokens.accessToken}`)
      .expect(403);
    
    expect(response.body.error.code).toBe('TENANT_MISMATCH');
  });
});
```

---

## 実装メモ

### データベーススキーマ
```sql
CREATE TABLE tenant_users (
  id VARCHAR(50) PRIMARY KEY,
  tenant_id VARCHAR(50) NOT NULL,
  user_id VARCHAR(50) NOT NULL,
  role VARCHAR(50) NOT NULL DEFAULT 'user',
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_login_at TIMESTAMP,
  login_attempts INTEGER DEFAULT 0,
  locked_until TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (tenant_id) REFERENCES tenants(id),
  FOREIGN KEY (user_id) REFERENCES users(id),
  UNIQUE(tenant_id, user_id)
);

CREATE TABLE user_sessions (
  id VARCHAR(50) PRIMARY KEY,
  user_id VARCHAR(50) NOT NULL,
  tenant_id VARCHAR(50) NOT NULL,
  session_token VARCHAR(255) NOT NULL,
  refresh_token VARCHAR(255) NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ip_address INET,
  user_agent TEXT,
  remember_me BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id),
  UNIQUE(session_token),
  UNIQUE(refresh_token)
);

CREATE TABLE auth_logs (
  id VARCHAR(50) PRIMARY KEY,
  tenant_id VARCHAR(50),
  user_id VARCHAR(50),
  email VARCHAR(255) NOT NULL,
  action VARCHAR(50) NOT NULL,
  status VARCHAR(20) NOT NULL,
  ip_address INET,
  user_agent TEXT,
  error_code VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (tenant_id) REFERENCES tenants(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_tenant_users_tenant_id ON tenant_users(tenant_id);
CREATE INDEX idx_tenant_users_user_id ON tenant_users(user_id);
CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_tenant_id ON user_sessions(tenant_id);
CREATE INDEX idx_user_sessions_expires_at ON user_sessions(expires_at);
CREATE INDEX idx_auth_logs_tenant_id ON auth_logs(tenant_id);
CREATE INDEX idx_auth_logs_created_at ON auth_logs(created_at);
```

### Next.js実装例
```typescript
// pages/api/auth/tenant.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { TenantAuthService } from '@/services/TenantAuthService';
import { validateTenantAuthRequest } from '@/lib/validation';
import { rateLimiter } from '@/lib/rateLimiter';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    // レート制限チェック
    await rateLimiter.check(req.ip, 'tenant_auth', 10, 60); // 1分間に10回まで
    
    const tenantAuthService = new TenantAuthService();
    
    switch (req.method) {
      case 'GET':
        if (req.url?.includes('/list')) {
          const tenants = await tenantAuthService.getTenantList(req.query.email as string);
          return res.status(200).json({ success: true, data: tenants });
        }
        break;
        
      case 'POST':
        if (req.url?.includes('/switch')) {
          const currentUser = await authenticateToken(req);
          const result = await tenantAuthService.switchTenant(
            currentUser.id,
            req.body.tenantId
          );
          return res.status(200).json({ success: true, data: result });
        } else {
          // バリデーション
          const validationResult = validateTenantAuthRequest(req.body);
          if (!validationResult.isValid) {
            return res.status(400).json({
              success: false,
              error: { code: 'VALIDATION_ERROR', message: validationResult.errors }
            });
          }
          
          // 認証実行
          const authResult = await tenantAuthService.authenticate(
            req.body.tenantId,
            req.body.email,
            req.body.password,
            req.body.rememberMe,
            req.ip,
            req.headers['user-agent']
          );
          
          return res.status(200).json({ success: true, data: authResult });
        }
        break;
        
      default:
        return res.status(405).json({ success: false, error: 'Method not allowed' });
    }
  } catch (error) {
    console.error('Tenant auth error:', error);
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

### テナント認証サービス実装例
```typescript
// services/TenantAuthService.ts
export class TenantAuthService {
  async authenticate(tenantId: string, email: string, password: string, rememberMe: boolean, ipAddress: string, userAgent: string) {
    try {
      // 1. テナント存在確認
      const tenant = await this.tenantRepository.findById(tenantId);
      if (!tenant || tenant.status !== 'active') {
        throw new ForbiddenError('TENANT_INACTIVE', 'テナントが無効です');
      }
      
      // 2. ユーザー認証
      const user = await this.userRepository.findByEmail(email);
      if (!user) {
        throw new UnauthorizedError('INVALID_CREDENTIALS', '認証情報が無効です');
      }
      
      // 3. テナント所属確認
      const tenantUser = await this.tenantUserRepository.findByTenantAndUser(tenantId, user.id);
      if (!tenantUser) {
        throw new ForbiddenError('USER_NOT_IN_TENANT', 'ユーザーがテナントに所属していません');
      }
      
      // 4. アカウントロック確認
      if (tenantUser.lockedUntil && tenantUser.lockedUntil > new Date()) {
        throw new LockedError('ACCOUNT_LOCKED', 'アカウントがロックされています');
      }
      
      // 5. パスワード検証
      const isValidPassword = await bcrypt.compare(password, user.passwordHash);
      if (!isValidPassword) {
        await this.handleFailedLogin(tenantUser);
        throw new UnauthorizedError('INVALID_CREDENTIALS', '認証情報が無効です');
      }
      
      // 6. ログイン成功処理
      await this.handleSuccessfulLogin(tenantUser);
      
      // 7. JWT生成
      const tokens = await this.generateTokens(user, tenant);
      
      // 8. セッション作成
      const session = await this.createSession(user.id, tenantId, tokens.refreshToken, rememberMe, ipAddress, userAgent);
      
      // 9. 認証ログ記録
      await this.logAuthEvent(tenantId, user.id, email, 'LOGIN_SUCCESS', ipAddress, userAgent);
      
      return {
        user: this.sanitizeUser(user),
        tenant: this.sanitizeTenant(tenant),
        tokens,
        session: {
          sessionId: session.id,
          expiresAt: session.expiresAt,
          rememberMe
        }
      };
      
    } catch (error) {
      // エラーログ記録
      await this.logAuthEvent(tenantId, null, email, 'LOGIN_FAILED', ipAddress, userAgent, error.code);
      throw error;
    }
  }
  
  private async handleFailedLogin(tenantUser: any) {
    tenantUser.loginAttempts += 1;
    
    if (tenantUser.loginAttempts >= 5) {
      tenantUser.lockedUntil = new Date(Date.now() + 30 * 60 * 1000); // 30分ロック
    }
    
    await this.tenantUserRepository.update(tenantUser);
  }
  
  private async generateTokens(user: any, tenant: any) {
    const payload = {
      userId: user.id,
      tenantId: tenant.id,
      email: user.email,
      role: user.role,
      permissions: user.permissions
    };
    
    const accessToken = jwt.sign(payload, process.env.JWT_PRIVATE_KEY, {
      algorithm: 'RS256',
      expiresIn: '1h',
      issuer: 'skill-report-system',
      audience: tenant.id
    });
    
    const refreshToken = jwt.sign(
      { userId: user.id, tenantId: tenant.id, type: 'refresh' },
      process.env.JWT_PRIVATE_KEY,
      {
        algorithm: 'RS256',
        expiresIn: '30d',
        issuer: 'skill-report-system',
        audience: tenant.id
      }
    );
    
    return {
      accessToken,
      refreshToken,
      expiresIn: 3600,
      tokenType: 'Bearer'
    };
  }
}
```

---

## 変更履歴

| 日付 | バージョン | 変更内容 | 変更者 |
|------|-----------|----------|--------|
| 2025-05-30 | 1.0.0 | 初版作成 | システムアーキテクト |
