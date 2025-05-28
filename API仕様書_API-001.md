# API仕様書：API-001 ユーザー認証API

## 1. 基本情報

- **API ID**: API-001
- **API名称**: ユーザー認証API
- **概要**: ユーザーID・パスワードによる認証を行い、認証成功時にはアクセストークンを発行する
- **エンドポイント**: `/api/auth/login`
- **HTTPメソッド**: POST
- **リクエスト形式**: JSON
- **レスポンス形式**: JSON
- **認証要件**: 不要（認証前API）
- **利用画面**: [SCR-LOGIN](画面設計書_SCR-LOGIN.md)
- **作成日**: 2025/05/28
- **作成者**: API設計担当
- **改訂履歴**: 2025/05/28 初版作成

---

## 2. リクエスト仕様

### 2.1 リクエストパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| user_id | string | ○ | ユーザーID | 社員番号またはメールアドレス<br>最大長：100文字 |
| password | string | ○ | パスワード | 8文字以上<br>最大長：100文字 |
| remember_me | boolean | - | ログイン状態維持 | デフォルト：false |

### 2.2 リクエスト例

```json
{
  "user_id": "tanaka.taro@example.com",
  "password": "P@ssw0rd",
  "remember_me": true
}
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| token | string | アクセストークン | JWT形式 |
| refresh_token | string | リフレッシュトークン | JWT形式 |
| expires_in | number | トークン有効期限（秒） | デフォルト：3600（1時間） |
| user_info | object | ユーザー基本情報 | 詳細は以下 |

#### user_info オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | ユーザーID | |
| employee_id | string | 社員番号 | |
| name | string | 氏名 | |
| email | string | メールアドレス | |
| department | string | 所属部署 | |
| position | string | 役職 | |
| role | string | システムロール | "admin", "manager", "user"のいずれか |
| last_login | string | 最終ログイン日時 | ISO 8601形式 |

### 3.2 正常時レスポンス例

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600,
  "user_info": {
    "user_id": "tanaka.taro@example.com",
    "employee_id": "E001",
    "name": "田中 太郎",
    "email": "tanaka.taro@example.com",
    "department": "開発部",
    "position": "主任",
    "role": "user",
    "last_login": "2025-05-27T10:30:00+09:00"
  }
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | リクエストパラメータの形式不正 |
| 401 Unauthorized | AUTHENTICATION_FAILED | ユーザーIDまたはパスワードが違います | 認証失敗 |
| 403 Forbidden | ACCOUNT_LOCKED | アカウントがロックされています | アカウントロック状態 |
| 429 Too Many Requests | TOO_MANY_ATTEMPTS | ログイン試行回数が上限を超えました | 短時間での複数回ログイン失敗 |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "AUTHENTICATION_FAILED",
    "message": "ユーザーIDまたはパスワードが違います",
    "details": "認証に失敗しました。ユーザーIDとパスワードを確認してください。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストパラメータのバリデーション
   - user_id、passwordの必須チェック
   - 形式チェック（文字数制限等）
2. ユーザー認証処理
   - ユーザーIDの存在確認
   - パスワードの照合（ハッシュ値比較）
   - アカウント状態確認（有効/無効/ロック）
3. 認証成功時の処理
   - アクセストークン生成（JWT）
   - リフレッシュトークン生成（JWT）
   - ユーザー情報取得
   - ログイン履歴更新
4. レスポンス返却

### 4.2 セキュリティ要件

- パスワードはハッシュ化して保存（bcrypt等）
- トークンはJWT形式で、署名検証あり
- ログイン失敗回数の制限（5回連続失敗でアカウントロック）
- アカウントロック解除は管理者操作または30分経過後
- 全通信はHTTPS（TLS 1.2以上）で暗号化
- CSRFトークン対策実施

### 4.3 パフォーマンス要件

- レスポンスタイム：平均500ms以内
- 同時接続：最大500ユーザー
- スロットリング：同一IPアドレスからの連続リクエスト制限（10回/分）

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-002](API仕様書_API-002.md) | SSO認証API | 代替認証手段 |
| [API-003](API仕様書_API-003.md) | 権限情報取得API | 認証後の権限取得 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| user_auth | 認証情報 | 参照（R） |
| login_history | ログイン履歴 | 作成（C） |
| account_lock | アカウントロック情報 | 参照/作成/更新（R/C/U） |

### 5.3 注意事項・補足

- パスワードポリシー：8文字以上、英大文字・小文字・数字・記号を含む
- アカウントロックは管理者画面から解除可能
- ログイン履歴は監査目的で90日間保持
- 初回ログイン時はパスワード変更を強制
- remember_me=trueの場合、リフレッシュトークンの有効期間は30日
- 本番環境ではレート制限を実装（DoS対策）

---

## 6. サンプルコード

### 6.1 リクエスト例（curl）

```bash
curl -X POST https://api.example.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "tanaka.taro@example.com",
    "password": "P@ssw0rd",
    "remember_me": true
  }'
```

### 6.2 リクエスト例（JavaScript/Fetch API）

```javascript
const response = await fetch('https://api.example.com/api/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    user_id: 'tanaka.taro@example.com',
    password: 'P@ssw0rd',
    remember_me: true
  })
});

const data = await response.json();
if (response.ok) {
  // 認証成功時の処理
  localStorage.setItem('token', data.token);
  localStorage.setItem('refresh_token', data.refresh_token);
} else {
  // エラー処理
  console.error(data.error.message);
}
```

### 6.3 レスポンス処理例（TypeScript）

```typescript
interface AuthResponse {
  token: string;
  refresh_token: string;
  expires_in: number;
  user_info: {
    user_id: string;
    employee_id: string;
    name: string;
    email: string;
    department: string;
    position: string;
    role: 'admin' | 'manager' | 'user';
    last_login: string;
  };
}

interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: string;
  };
}

// レスポンス処理
function handleAuthResponse(response: AuthResponse | ErrorResponse): void {
  if ('token' in response) {
    // 認証成功
    const auth = response as AuthResponse;
    setAuthToken(auth.token);
    setUserInfo(auth.user_info);
    redirectToDashboard();
  } else {
    // エラー処理
    const error = response as ErrorResponse;
    showErrorMessage(error.error.message);
  }
}
