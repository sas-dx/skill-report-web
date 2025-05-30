# API定義書：API-002 SSO認証API

## 1. 基本情報

- **API ID**: API-002
- **API名称**: SSO認証API
- **概要**: シングルサインオン（SSO）による認証を行い、アクセストークンを発行する
- **エンドポイント**: `/api/auth/sso`
- **HTTPメソッド**: GET
- **リクエスト形式**: URL パラメータ
- **レスポンス形式**: JSON
- **認証要件**: 不要（認証前の呼び出し）
- **利用画面**: [SCR-LOGIN](画面設計書_SCR-LOGIN.md)
- **作成日**: 2025/05/28
- **作成者**: API設計担当
- **改訂履歴**: 2025/05/28 初版作成

---

## 2. リクエスト仕様

### 2.1 リクエストパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| code | string | ○ | 認証コード | SSOプロバイダから取得した認証コード |
| state | string | ○ | 状態トークン | CSRF対策用のランダムトークン |
| redirect_uri | string | ○ | リダイレクトURI | 認証後のリダイレクト先URI |

### 2.2 リクエスト例

```
GET /api/auth/sso?code=abc123xyz&state=random_state_token&redirect_uri=https://example.com/callback HTTP/1.1
Host: api.example.com
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| access_token | string | アクセストークン | JWT形式 |
| token_type | string | トークンタイプ | 常に "Bearer" |
| expires_in | number | 有効期間 | 秒単位（デフォルト: 3600秒） |
| refresh_token | string | リフレッシュトークン | JWT形式 |
| user_info | object | ユーザー情報 | ユーザー基本情報 |

#### user_info オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | ユーザーID | |
| username | string | ユーザー名 | |
| email | string | メールアドレス | |
| display_name | string | 表示名 | |
| department | string | 部署 | |
| role | string | ロール | "admin", "manager", "user"のいずれか |
| last_login | string | 最終ログイン日時 | ISO 8601形式 |

### 3.2 正常時レスポンス例

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_info": {
    "user_id": "U12345",
    "username": "tanaka.taro",
    "email": "tanaka.taro@example.com",
    "display_name": "田中 太郎",
    "department": "情報システム部",
    "role": "user",
    "last_login": "2025-05-27T15:30:45+09:00"
  }
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_REQUEST | リクエストが不正です | パラメータ不足・形式不正 |
| 400 Bad Request | INVALID_CODE | 認証コードが無効です | 認証コードの有効期限切れ・不正 |
| 400 Bad Request | INVALID_STATE | 状態トークンが無効です | stateトークン不一致 |
| 401 Unauthorized | UNAUTHORIZED | 認証に失敗しました | SSOプロバイダ認証失敗 |
| 403 Forbidden | ACCESS_DENIED | アクセスが拒否されました | アクセス権限なし |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |
| 503 Service Unavailable | SERVICE_UNAVAILABLE | サービスが一時的に利用できません | SSOプロバイダ接続不可 |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_CODE",
    "message": "認証コードが無効です",
    "details": "認証コードの有効期限が切れているか、無効なコードです。再度認証を行ってください。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストパラメータの検証
   - 必須パラメータの存在確認
   - パラメータ形式チェック
   - stateトークンの検証（CSRF対策）
2. SSOプロバイダへの認証コード検証リクエスト
   - 認証コードとリダイレクトURIを送信
   - アクセストークンの取得
3. SSOプロバイダからユーザー情報の取得
   - 取得したアクセストークンを使用
   - ユーザープロファイル情報の取得
4. 内部システムでのユーザー情報検証
   - ユーザーIDの存在確認
   - アクセス権限の確認
5. JWTトークンの生成
   - アクセストークン生成
   - リフレッシュトークン生成
6. ユーザー情報の取得・整形
7. レスポンスの生成・返却

### 4.2 SSOプロバイダ連携仕様

- 対応SSOプロバイダ：Azure AD、Google Workspace
- 認証フロー：Authorization Code Flow
- スコープ：openid profile email
- IDトークン検証：署名検証、発行者検証、有効期限検証
- クレーム検証：aud（対象者）、iss（発行者）

### 4.3 セキュリティ要件

- HTTPS通信必須
- stateパラメータによるCSRF対策
- JWTトークンの署名検証
- アクセストークン有効期限：1時間
- リフレッシュトークン有効期限：14日間
- 認証コード有効期限：10分間

### 4.4 パフォーマンス要件

- レスポンスタイム：平均500ms以内
- タイムアウト：10秒
- 同時接続数：最大100接続

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-001](API仕様書_API-001.md) | ユーザー認証API | ID/パスワードによる認証 |
| [API-003](API仕様書_API-003.md) | 権限情報取得API | ユーザー権限情報取得 |
| [API-004](API仕様書_API-004.md) | 権限設定API | ユーザー権限情報更新 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| user_roles | ユーザーロール | 参照（R） |
| auth_logs | 認証ログ | 作成（C） |
| refresh_tokens | リフレッシュトークン | 作成（C） |

### 5.3 注意事項・補足

- SSOプロバイダの設定はシステム管理者が事前に行う必要がある
- 初回ログイン時は内部システムにユーザー情報が自動登録される
- 複数のSSOプロバイダに対応（Azure AD、Google Workspace）
- SSOプロバイダ側の設定変更時はシステム管理者への通知が必要
- ログイン履歴は監査目的で保存される

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（JavaScript）

```javascript
/**
 * SSO認証を開始する関数
 * @param {string} provider - SSOプロバイダ名（"azure"または"google"）
 */
function startSSOAuthentication(provider) {
  // ランダムなstateトークンを生成（CSRF対策）
  const stateToken = generateRandomToken();
  
  // stateトークンをセッションストレージに保存
  sessionStorage.setItem('sso_state', stateToken);
  
  // リダイレクトURI
  const redirectUri = encodeURIComponent(`${window.location.origin}/auth/callback`);
  
  // SSOプロバイダのURLを構築
  let ssoUrl;
  if (provider === 'azure') {
    ssoUrl = `https://login.microsoftonline.com/${TENANT_ID}/oauth2/v2.0/authorize?`;
    ssoUrl += `client_id=${AZURE_CLIENT_ID}`;
    ssoUrl += `&response_type=code`;
    ssoUrl += `&redirect_uri=${redirectUri}`;
    ssoUrl += `&scope=openid profile email`;
    ssoUrl += `&state=${stateToken}`;
  } else if (provider === 'google') {
    ssoUrl = `https://accounts.google.com/o/oauth2/v2/auth?`;
    ssoUrl += `client_id=${GOOGLE_CLIENT_ID}`;
    ssoUrl += `&response_type=code`;
    ssoUrl += `&redirect_uri=${redirectUri}`;
    ssoUrl += `&scope=openid profile email`;
    ssoUrl += `&state=${stateToken}`;
  } else {
    showError('不明なSSOプロバイダです');
    return;
  }
  
  // SSOプロバイダのログイン画面にリダイレクト
  window.location.href = ssoUrl;
}

/**
 * SSO認証コールバック処理
 */
async function handleSSOCallback() {
  // URLからパラメータを取得
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get('code');
  const state = urlParams.get('state');
  const error = urlParams.get('error');
  
  // エラーチェック
  if (error) {
    showError(`SSOプロバイダからエラーが返されました: ${error}`);
    return;
  }
  
  // 必須パラメータチェック
  if (!code || !state) {
    showError('必要なパラメータが不足しています');
    return;
  }
  
  // stateトークンの検証
  const savedState = sessionStorage.getItem('sso_state');
  if (state !== savedState) {
    showError('セキュリティトークンが一致しません');
    return;
  }
  
  // stateトークンをクリア
  sessionStorage.removeItem('sso_state');
  
  try {
    // リダイレクトURI
    const redirectUri = `${window.location.origin}/auth/callback`;
    
    // APIリクエスト
    const response = await fetch(`/api/auth/sso?code=${code}&state=${state}&redirect_uri=${encodeURIComponent(redirectUri)}`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error.message || 'SSO認証に失敗しました');
    }
    
    // レスポンスの解析
    const authData = await response.json();
    
    // トークンの保存
    localStorage.setItem('access_token', authData.access_token);
    localStorage.setItem('refresh_token', authData.refresh_token);
    localStorage.setItem('token_expiry', Date.now() + (authData.expires_in * 1000));
    localStorage.setItem('user_info', JSON.stringify(authData.user_info));
    
    // ログイン成功後のリダイレクト
    window.location.href = '/dashboard';
    
  } catch (error) {
    showError(`認証エラー: ${error.message}`);
  }
}

/**
 * ランダムなトークンを生成する関数
 * @returns {string} ランダムトークン
 */
function generateRandomToken() {
  const array = new Uint8Array(24);
  window.crypto.getRandomValues(array);
  return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
}
```

### 6.2 バックエンド実装例（Node.js/Express）

```javascript
const express = require('express');
const axios = require('axios');
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');

const router = express.Router();

/**
 * SSO認証API
 */
router.get('/auth/sso', async (req, res) => {
  try {
    // リクエストパラメータの取得
    const { code, state, redirect_uri } = req.query;
    
    // パラメータのバリデーション
    if (!code || !state || !redirect_uri) {
      return res.status(400).json({
        error: {
          code: 'INVALID_REQUEST',
          message: 'リクエストが不正です',
          details: '必須パラメータが不足しています'
        }
      });
    }
    
    // stateトークンの検証（実際の実装ではセッションなどで保存したstateと比較）
    // この例では簡略化のため省略
    
    // SSOプロバイダの判別（実際の実装ではリダイレクトURIなどから判別）
    const provider = detectProvider(redirect_uri);
    
    // SSOプロバイダからトークンを取得
    const tokenResponse = await getTokenFromProvider(provider, code, redirect_uri);
    
    // IDトークンの検証
    const idToken = tokenResponse.id_token;
    const decodedToken = verifyIdToken(idToken, provider);
    
    // ユーザー情報の取得
    const userInfo = await getUserInfo(provider, tokenResponse.access_token);
    
    // 内部システムでのユーザー検証
    const internalUser = await validateAndGetInternalUser(userInfo);
    
    // JWTトークンの生成
    const accessToken = generateAccessToken(internalUser);
    const refreshToken = generateRefreshToken(internalUser);
    
    // リフレッシュトークンの保存
    await saveRefreshToken(refreshToken, internalUser.user_id);
    
    // 認証ログの記録
    await logAuthentication(internalUser.user_id, 'sso', provider);
    
    // レスポンスの返却
    return res.status(200).json({
      access_token: accessToken,
      token_type: 'Bearer',
      expires_in: 3600,
      refresh_token: refreshToken,
      user_info: {
        user_id: internalUser.user_id,
        username: internalUser.username,
        email: internalUser.email,
        display_name: internalUser.display_name,
        department: internalUser.department,
        role: internalUser.role,
        last_login: new Date().toISOString()
      }
    });
    
  } catch (error) {
    console.error('SSO認証エラー:', error);
    
    // エラーレスポンスの生成
    let statusCode = 500;
    let errorResponse = {
      error: {
        code: 'SYSTEM_ERROR',
        message: 'システムエラーが発生しました',
        details: '認証処理中に予期しないエラーが発生しました'
      }
    };
    
    // エラータイプに応じたレスポンス
    if (error.name === 'InvalidCodeError') {
      statusCode = 400;
      errorResponse.error = {
        code: 'INVALID_CODE',
        message: '認証コードが無効です',
        details: error.message
      };
    } else if (error.name === 'UnauthorizedError') {
      statusCode = 401;
      errorResponse.error = {
        code: 'UNAUTHORIZED',
        message: '認証に失敗しました',
        details: error.message
      };
    } else if (error.name === 'AccessDeniedError') {
      statusCode = 403;
      errorResponse.error = {
        code: 'ACCESS_DENIED',
        message: 'アクセスが拒否されました',
        details: error.message
      };
    } else if (error.name === 'ServiceUnavailableError') {
      statusCode = 503;
      errorResponse.error = {
        code: 'SERVICE_UNAVAILABLE',
        message: 'サービスが一時的に利用できません',
        details: error.message
      };
    }
    
    return res.status(statusCode).json(errorResponse);
  }
});

module.exports = router;
```

### 6.3 SSOプロバイダ設定例（Azure AD）

```json
{
  "appRegistration": {
    "name": "スキル報告書管理システム",
    "signInAudience": "AzureADMyOrg",
    "redirectUris": [
      "https://example.com/auth/callback",
      "http://localhost:3000/auth/callback"
    ],
    "logoutUrl": "https://example.com/logout",
    "implicitGrantSettings": {
      "enableAccessTokens": false,
      "enableIdTokens": true
    }
  },
  "apiPermissions": [
    {
      "resourceAppId": "00000003-0000-0000-c000-000000000000",
      "resourceAccess": [
        {
          "id": "e1fe6dd8-ba31-4d61-89e7-88639da4683d",
          "type": "Scope"
        },
        {
          "id": "37f7f235-527c-4136-accd-4a02d197296e",
          "type": "Scope"
        },
        {
          "id": "14dad69e-099b-42c9-810b-d002981feec1",
          "type": "Scope"
        }
      ]
    }
  ],
  "appRoles": [
    {
      "allowedMemberTypes": ["User"],
      "displayName": "管理者",
      "description": "システム管理者権限",
      "value": "admin"
    },
    {
      "allowedMemberTypes": ["User"],
      "displayName": "マネージャー",
      "description": "部門管理者権限",
      "value": "manager"
    },
    {
      "allowedMemberTypes": ["User"],
      "displayName": "一般ユーザー",
      "description": "一般ユーザー権限",
      "value": "user"
    }
  ]
}
