# API仕様書：API-001 ユーザー認証API

## 1. 基本情報

- **API ID**: API-001
- **API名称**: ユーザー認証API
- **概要**: ユーザーID・パスワードによる認証を行い、アクセストークンを発行する
- **エンドポイント**: `/api/auth/login`
- **HTTPメソッド**: POST
- **リクエスト形式**: JSON
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
| user_id | string | ○ | ユーザーID | 半角英数字、4〜20文字 |
| password | string | ○ | パスワード | 8文字以上、英大文字・小文字・数字・記号を含む |
| remember_me | boolean | - | ログイン状態を保持するか | デフォルト：false |

### 2.2 リクエスト例

```json
{
  "user_id": "tanaka.taro",
  "password": "P@ssw0rd123",
  "remember_me": true
}
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| access_token | string | アクセストークン | JWT形式 |
| token_type | string | トークンタイプ | 常に "Bearer" |
| expires_in | number | トークン有効期間（秒） | remember_me=falseの場合：3600（1時間）<br>remember_me=trueの場合：2592000（30日） |
| refresh_token | string | リフレッシュトークン | JWT形式 |
| user_info | object | ユーザー基本情報 | 詳細は以下参照 |

#### user_info オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | ユーザーID | |
| user_name | string | ユーザー名 | |
| email | string | メールアドレス | |
| department | string | 所属部署 | |
| role | string | ユーザーロール | "admin", "manager", "user"のいずれか |
| last_login_at | string | 前回ログイン日時 | ISO 8601形式 |

### 3.2 正常時レスポンス例

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 2592000,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_info": {
    "user_id": "tanaka.taro",
    "user_name": "田中 太郎",
    "email": "tanaka.taro@example.com",
    "department": "開発部",
    "role": "user",
    "last_login_at": "2025-05-27T10:15:30+09:00"
  }
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | リクエストパラメータの形式不正 |
| 401 Unauthorized | INVALID_CREDENTIALS | ユーザーIDまたはパスワードが正しくありません | 認証失敗 |
| 401 Unauthorized | ACCOUNT_LOCKED | アカウントがロックされています | ログイン試行回数超過 |
| 403 Forbidden | ACCOUNT_DISABLED | アカウントが無効化されています | 退職者など |
| 429 Too Many Requests | TOO_MANY_REQUESTS | リクエスト回数が制限を超えています | レート制限超過 |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |
| 503 Service Unavailable | SERVICE_UNAVAILABLE | サービスが一時的に利用できません | システム過負荷/メンテナンス中 |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "ユーザーIDまたはパスワードが正しくありません",
    "details": "ログインに5回失敗すると、アカウントが一時的にロックされます。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストパラメータの検証
   - user_idの形式チェック
   - passwordの形式チェック
2. ユーザー認証処理
   - ユーザーIDの存在確認
   - パスワードの照合（ハッシュ比較）
   - アカウント状態の確認（有効/無効/ロック状態）
3. ログイン試行回数の確認
   - 連続失敗回数のチェック
   - 必要に応じてアカウントロック
4. トークン生成
   - アクセストークンの生成（JWT）
   - リフレッシュトークンの生成（JWT）
   - トークン有効期限の設定
5. ログイン履歴の記録
   - ログイン日時、IPアドレス、デバイス情報の記録
6. レスポンスの生成
   - トークン情報の設定
   - ユーザー基本情報の取得・設定
7. レスポンス返却

### 4.2 認証ルール

- パスワード照合は常にハッシュ化して比較（bcryptなど）
- 連続5回のログイン失敗でアカウントを30分間ロック
- パスワードポリシー：8文字以上、英大文字・小文字・数字・記号を含む
- remember_me=trueの場合、長期間有効なトークンを発行（30日）
- remember_me=falseの場合、短期間有効なトークンを発行（1時間）
- 退職者など無効化されたアカウントはログイン不可

### 4.3 セキュリティ要件

- 通信は常にHTTPS（TLS 1.2以上）
- パスワードはbcryptでハッシュ化して保存
- JWTの署名アルゴリズムはHS256またはRS256
- トークンにはユーザーID、ロール、有効期限、発行者情報を含める
- IPアドレスによるレート制限（同一IPから1分間に10回まで）
- ブルートフォース攻撃対策としてログイン試行回数制限を実装
- リクエスト・レスポンスのログにはパスワード情報を含めない

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-002](API仕様書_API-002.md) | SSO認証API | シングルサインオン認証 |
| [API-003](API仕様書_API-003.md) | 権限情報取得API | ユーザー権限情報取得 |
| [API-004](API仕様書_API-004.md) | 権限設定API | ユーザー権限情報更新 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| user_passwords | パスワード情報 | 参照（R） |
| login_histories | ログイン履歴 | 作成（C） |
| login_failures | ログイン失敗履歴 | 参照/作成/更新（R/C/U） |
| access_tokens | トークン情報 | 作成（C） |

### 5.3 注意事項・補足

- 初回ログイン時はパスワード変更を促す
- パスワードは定期的な変更を推奨（90日ごと）
- 過去に使用したパスワードの再利用は制限（過去5回分）
- 多要素認証（MFA）の導入を検討中
- ログイン履歴は監査目的で1年間保持
- 長期間未使用アカウント（180日以上）は自動的に無効化

---

## 6. サンプルコード

### 6.1 ログイン処理例（JavaScript/Fetch API）

```javascript
/**
 * ユーザー認証を行う関数
 * @param {string} userId - ユーザーID
 * @param {string} password - パスワード
 * @param {boolean} rememberMe - ログイン状態を保持するか
 * @returns {Promise<Object>} 認証結果
 */
async function login(userId, password, rememberMe = false) {
  try {
    const response = await fetch('https://api.example.com/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        user_id: userId,
        password: password,
        remember_me: rememberMe
      })
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error.message || 'ログインに失敗しました');
    }
    
    const authData = await response.json();
    
    // トークンをローカルストレージに保存
    localStorage.setItem('access_token', authData.access_token);
    localStorage.setItem('refresh_token', authData.refresh_token);
    localStorage.setItem('token_expires_at', Date.now() + (authData.expires_in * 1000));
    localStorage.setItem('user_info', JSON.stringify(authData.user_info));
    
    return authData;
  } catch (error) {
    console.error('ログインエラー:', error);
    throw error;
  }
}
```

### 6.2 ログインフォーム実装例（React）

```jsx
import React, { useState } from 'react';
import { login } from '../api/authApi';
import { useNavigate } from 'react-router-dom';

const LoginForm = () => {
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const navigate = useNavigate();
  
  // ユーザーID入力ハンドラ
  const handleUserIdChange = (e) => {
    setUserId(e.target.value);
  };
  
  // パスワード入力ハンドラ
  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };
  
  // Remember Me チェックボックスハンドラ
  const handleRememberMeChange = (e) => {
    setRememberMe(e.target.checked);
  };
  
  // ログイン処理ハンドラ
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // 入力検証
    if (!userId.trim()) {
      setError('ユーザーIDを入力してください');
      return;
    }
    
    if (!password) {
      setError('パスワードを入力してください');
      return;
    }
    
    try {
      setIsLoading(true);
      setError(null);
      
      // ログインAPI呼び出し
      const authData = await login(userId, password, rememberMe);
      
      // ログイン成功時の処理
      console.log('ログイン成功:', authData.user_info.user_name);
      
      // ダッシュボードへリダイレクト
      navigate('/dashboard');
      
    } catch (err) {
      setError(err.message || 'ログインに失敗しました。再度お試しください。');
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="login-container">
      <h2>ログイン</h2>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="userId">ユーザーID</label>
          <input
            type="text"
            id="userId"
            value={userId}
            onChange={handleUserIdChange}
            disabled={isLoading}
            autoComplete="username"
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="password">パスワード</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={handlePasswordChange}
            disabled={isLoading}
            autoComplete="current-password"
          />
        </div>
        
        <div className="form-group checkbox">
          <input
            type="checkbox"
            id="rememberMe"
            checked={rememberMe}
            onChange={handleRememberMeChange}
            disabled={isLoading}
          />
          <label htmlFor="rememberMe">ログイン状態を保持する</label>
        </div>
        
        <button 
          type="submit" 
          className="login-button"
          disabled={isLoading}
        >
          {isLoading ? 'ログイン中...' : 'ログイン'}
        </button>
      </form>
      
      <div className="login-links">
        <a href="/forgot-password">パスワードをお忘れですか？</a>
        <a href="/sso-login">シングルサインオンでログイン</a>
      </div>
    </div>
  );
};

export default LoginForm;
```

### 6.3 トークン管理ユーティリティ例（TypeScript）

```typescript
/**
 * 認証トークン管理ユーティリティ
 */
export class TokenManager {
  private static readonly ACCESS_TOKEN_KEY = 'access_token';
  private static readonly REFRESH_TOKEN_KEY = 'refresh_token';
  private static readonly TOKEN_EXPIRES_AT_KEY = 'token_expires_at';
  private static readonly USER_INFO_KEY = 'user_info';
  
  /**
   * アクセストークンを取得
   */
  public static getAccessToken(): string | null {
    return localStorage.getItem(this.ACCESS_TOKEN_KEY);
  }
  
  /**
   * リフレッシュトークンを取得
   */
  public static getRefreshToken(): string | null {
    return localStorage.getItem(this.REFRESH_TOKEN_KEY);
  }
  
  /**
   * ユーザー情報を取得
   */
  public static getUserInfo(): any | null {
    const userInfoStr = localStorage.getItem(this.USER_INFO_KEY);
    if (!userInfoStr) return null;
    
    try {
      return JSON.parse(userInfoStr);
    } catch (e) {
      console.error('ユーザー情報の解析に失敗しました', e);
      return null;
    }
  }
  
  /**
   * トークンが有効かチェック
   */
  public static isTokenValid(): boolean {
    const expiresAtStr = localStorage.getItem(this.TOKEN_EXPIRES_AT_KEY);
    if (!expiresAtStr) return false;
    
    const expiresAt = parseInt(expiresAtStr, 10);
    // 有効期限の5分前に更新が必要と判断
    return Date.now() < expiresAt - (5 * 60 * 1000);
  }
  
  /**
   * 認証情報をクリア（ログアウト時）
   */
  public static clearTokens(): void {
    localStorage.removeItem(this.ACCESS_TOKEN_KEY);
    localStorage.removeItem(this.REFRESH_TOKEN_KEY);
    localStorage.removeItem(this.TOKEN_EXPIRES_AT_KEY);
    localStorage.removeItem(this.USER_INFO_KEY);
  }
  
  /**
   * 認証ヘッダーを生成
   */
  public static getAuthHeader(): { Authorization: string } | {} {
    const token = this.getAccessToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
  }
}
