# バックエンド設計ガイドライン（Next.js 14 + Prisma特化）

## エグゼクティブサマリー

この文書はNext.js 14 + Prisma ORMを中心としたバックエンド設計ガイドラインを定義します。API Routes設計原則、データベースアクセスパターン、セキュリティ実装、エラーハンドリング、パフォーマンス最適化手法を提供し、スケーラブルで保守性の高いバックエンドシステムの構築を支援します。技術スタック非依存の基本原則は00-core-rules.mdを参照し、このファイルではNext.js 14 + Prisma固有の実装パターンとベストプラクティスに焦点を当てています。

## 基本設計原則

### 1. Next.js 14 API設計原則
- **App Router API Routes**: app/api/ディレクトリ構造でAPI管理
- **Server Actions優先**: フォーム処理・データ更新はServer Actions優先
- **RESTful設計**: REST原則に従ったAPI設計
- **型安全性**: TypeScript + Prismaによる型安全なAPI実装

### 2. Prisma ORM設計原則
- **Prisma Client**: データベースアクセスはPrisma Client経由
- **型安全性**: Prismaが生成する型を活用
- **トランザクション**: 複数操作の整合性保証
- **リレーション**: 適切なリレーション設計

### 3. シングルテナント設計（現実対応）
- **シンプルな設計**: マルチテナント複雑性を排除
- **将来拡張性**: マルチテナント化への移行を考慮
- **データ整合性**: 外部キー制約による整合性保証
- **パフォーマンス**: インデックス最適化

## API設計規約

### 1. RESTful API設計
- **リソース指向**: URLはリソースを表現
- **HTTPメソッドの適切な使用**: GET, POST, PUT, DELETE, PATCH
- **ステータスコードの統一**: 適切なHTTPステータスコードの使用
- **冪等性**: 同じリクエストを複数回実行しても結果が同じ

```javascript
// 良い例（RESTful API）
GET    /api/v1/users          // ユーザー一覧取得
GET    /api/v1/users/123      // 特定ユーザー取得
POST   /api/v1/users          // ユーザー作成
PUT    /api/v1/users/123      // ユーザー更新（全体）
PATCH  /api/v1/users/123      // ユーザー更新（部分）
DELETE /api/v1/users/123      // ユーザー削除

// 悪い例（非RESTful）
GET    /api/getUsers
POST   /api/createUser
POST   /api/updateUser
POST   /api/deleteUser
```

### 2. レスポンス形式の統一
- **成功レスポンス**: 一貫した構造
- **エラーレスポンス**: 標準化されたエラー形式
- **ページネーション**: 大量データの分割取得
- **フィルタリング**: 検索・絞り込み機能

```javascript
// 成功レスポンス例
{
  "success": true,
  "data": {
    "users": [...],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100,
      "totalPages": 5
    }
  },
  "timestamp": "2025-05-26T11:01:00Z"
}

// エラーレスポンス例
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "入力値に誤りがあります",
    "details": [
      {
        "field": "email",
        "message": "有効なメールアドレスを入力してください"
      }
    ]
  },
  "timestamp": "2025-05-26T11:01:00Z"
}
```

### 3. APIバージョニング
- **URLパス**: `/api/v1/`, `/api/v2/`
- **ヘッダー**: `Accept: application/vnd.api+json;version=1`
- **後方互換性**: 既存APIの破壊的変更を避ける
- **廃止予告**: 古いバージョンの段階的廃止

## データベース設計原則

### 1. 正規化とパフォーマンス
- **第3正規形**: データの重複を排除
- **非正規化**: パフォーマンス要件に応じた適切な非正規化
- **インデックス設計**: 検索性能の最適化
- **パーティショニング**: 大量データの分散管理

### 2. トランザクション管理
- **ACID特性**: 原子性、一貫性、独立性、永続性の保証
- **分離レベル**: 適切な分離レベルの選択
- **デッドロック対策**: デッドロック発生の予防と対処
- **長時間トランザクション**: 適切な粒度でのトランザクション分割

### 3. データ整合性
- **外部キー制約**: 参照整合性の保証
- **チェック制約**: ビジネスルールの実装
- **一意制約**: データの一意性保証
- **楽観的ロック**: 同時更新制御

```sql
-- 良い例（適切な制約設定）
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version INTEGER DEFAULT 1 -- 楽観的ロック用
);

CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    skill_name VARCHAR(100) NOT NULL,
    level INTEGER CHECK (level >= 1 AND level <= 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## セキュリティ設計

### 1. 認証・認可
- **JWT（JSON Web Token）**: ステートレスな認証
- **OAuth 2.0**: 第三者認証の標準
- **RBAC（Role-Based Access Control）**: ロールベースアクセス制御
- **最小権限の原則**: 必要最小限の権限付与

### 2. 入力値検証
- **サーバーサイドバリデーション**: 必須の検証処理
- **SQLインジェクション対策**: パラメータ化クエリの使用
- **XSS対策**: 出力時のエスケープ処理
- **CSRF対策**: CSRFトークンの実装

```javascript
// 良い例（入力値検証）
const validateUserInput = (userData) => {
  const errors = [];
  
  // 必須項目チェック
  if (!userData.email || !userData.email.trim()) {
    errors.push({ field: 'email', message: 'メールアドレスは必須です' });
  }
  
  // 形式チェック
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (userData.email && !emailRegex.test(userData.email)) {
    errors.push({ field: 'email', message: '有効なメールアドレスを入力してください' });
  }
  
  // 文字数制限
  if (userData.name && userData.name.length > 100) {
    errors.push({ field: 'name', message: '名前は100文字以内で入力してください' });
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
};

// パラメータ化クエリの例
const getUserById = async (userId) => {
  const query = 'SELECT * FROM users WHERE id = $1';
  const result = await db.query(query, [userId]);
  return result.rows[0];
};
```

### 3. データ保護
- **暗号化**: 機密データの暗号化保存
- **ハッシュ化**: パスワードの安全な保存
- **TLS/SSL**: 通信の暗号化
- **ログ管理**: 機密情報のログ出力制御

## エラーハンドリング

### 1. 例外処理戦略
- **カスタム例外**: ビジネスロジック固有の例外定義
- **例外の階層化**: 例外の種類による分類
- **適切なログ出力**: エラー情報の記録
- **ユーザーフレンドリーなメッセージ**: 分かりやすいエラー通知

```javascript
// カスタム例外の例
class ValidationError extends Error {
  constructor(message, field) {
    super(message);
    this.name = 'ValidationError';
    this.field = field;
    this.statusCode = 400;
  }
}

class AuthenticationError extends Error {
  constructor(message) {
    super(message);
    this.name = 'AuthenticationError';
    this.statusCode = 401;
  }
}

class AuthorizationError extends Error {
  constructor(message) {
    super(message);
    this.name = 'AuthorizationError';
    this.statusCode = 403;
  }
}

// エラーハンドリングミドルウェア
const errorHandler = (error, req, res, next) => {
  logger.error('API Error:', {
    error: error.message,
    stack: error.stack,
    url: req.url,
    method: req.method,
    userId: req.user?.id
  });

  if (error instanceof ValidationError) {
    return res.status(400).json({
      success: false,
      error: {
        code: 'VALIDATION_ERROR',
        message: error.message,
        field: error.field
      }
    });
  }

  if (error instanceof AuthenticationError) {
    return res.status(401).json({
      success: false,
      error: {
        code: 'AUTHENTICATION_ERROR',
        message: 'ログインが必要です'
      }
    });
  }

  // デフォルトエラー
  res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_SERVER_ERROR',
      message: 'システムエラーが発生しました'
    }
  });
};
```

## パフォーマンス最適化

### 1. データベース最適化
- **クエリ最適化**: 効率的なSQL文の作成
- **インデックス活用**: 適切なインデックス設計
- **N+1問題の解決**: 効率的なデータ取得
- **コネクションプール**: データベース接続の最適化

### 2. キャッシュ戦略
- **メモリキャッシュ**: 頻繁にアクセスされるデータのキャッシュ
- **Redis**: 分散キャッシュの活用
- **CDN**: 静的コンテンツの配信最適化
- **キャッシュ無効化**: 適切なキャッシュ更新戦略

```javascript
// キャッシュ実装例
const cache = require('redis').createClient();

const getUserWithCache = async (userId) => {
  const cacheKey = `user:${userId}`;
  
  // キャッシュから取得を試行
  const cachedUser = await cache.get(cacheKey);
  if (cachedUser) {
    return JSON.parse(cachedUser);
  }
  
  // データベースから取得
  const user = await getUserFromDatabase(userId);
  
  // キャッシュに保存（1時間）
  await cache.setex(cacheKey, 3600, JSON.stringify(user));
  
  return user;
};
```

### 3. 非同期処理
- **メッセージキュー**: 重い処理の非同期実行
- **バックグラウンドジョブ**: 定期実行タスクの管理
- **イベント駆動**: 疎結合なシステム設計
- **ストリーミング**: リアルタイムデータ処理

## テスト戦略

### 1. テストの種類
- **ユニットテスト**: 個別の関数・メソッドのテスト
- **統合テスト**: モジュール間の連携テスト
- **APIテスト**: エンドポイントの動作テスト
- **パフォーマンステスト**: 性能要件の検証

### 2. テスト実装
- **テストデータ**: 一貫したテストデータの管理
- **モック・スタブ**: 外部依存の分離
- **テストカバレッジ**: 適切なカバレッジ目標
- **継続的テスト**: CI/CDパイプラインでの自動実行

```javascript
// APIテストの例
describe('User API', () => {
  beforeEach(async () => {
    await setupTestDatabase();
  });

  afterEach(async () => {
    await cleanupTestDatabase();
  });

  describe('POST /api/v1/users', () => {
    it('should create a new user with valid data', async () => {
      const userData = {
        name: '山田太郎',
        email: 'yamada@example.com',
        department: '開発部'
      };

      const response = await request(app)
        .post('/api/v1/users')
        .send(userData)
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data.user.name).toBe(userData.name);
      expect(response.body.data.user.email).toBe(userData.email);
    });

    it('should return validation error for invalid email', async () => {
      const userData = {
        name: '山田太郎',
        email: 'invalid-email',
        department: '開発部'
      };

      const response = await request(app)
        .post('/api/v1/users')
        .send(userData)
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('VALIDATION_ERROR');
    });
  });
});
```

## ログ・監視

### 1. ログ設計
- **構造化ログ**: JSON形式での統一
- **ログレベル**: 適切なレベル分け
- **コンテキスト情報**: トレーサビリティの確保
- **機密情報の除外**: セキュリティ配慮

### 2. 監視・メトリクス
- **ヘルスチェック**: システム状態の監視
- **パフォーマンスメトリクス**: レスポンス時間、スループット
- **エラー率**: エラー発生状況の監視
- **アラート**: 異常時の通知

```javascript
// 構造化ログの例
const logger = require('winston');

const logFormat = winston.format.combine(
  winston.format.timestamp(),
  winston.format.errors({ stack: true }),
  winston.format.json()
);

const logger = winston.createLogger({
  format: logFormat,
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

// 使用例
logger.info('User login successful', {
  userId: user.id,
  email: user.email,
  ipAddress: req.ip,
  userAgent: req.get('User-Agent'),
  timestamp: new Date().toISOString()
});

logger.error('Database connection failed', {
  error: error.message,
  stack: error.stack,
  database: 'users_db',
  timestamp: new Date().toISOString()
});
```

## デプロイメント・運用

### 1. 環境管理
- **設定の外部化**: 環境変数による設定管理
- **環境分離**: 開発・テスト・本番環境の分離
- **シークレット管理**: 機密情報の安全な管理
- **設定検証**: 起動時の設定値チェック

### 2. CI/CD
- **自動テスト**: コミット時の自動テスト実行
- **自動デプロイ**: 承認後の自動デプロイ
- **ロールバック**: 問題発生時の迅速な復旧
- **ブルーグリーンデプロイ**: ダウンタイムなしのデプロイ

### 3. 運用監視
- **ヘルスチェックエンドポイント**: システム状態の確認
- **メトリクス収集**: パフォーマンス指標の収集
- **ログ集約**: 分散ログの一元管理
- **アラート設定**: 異常時の自動通知

```javascript
// ヘルスチェックエンドポイント
app.get('/health', async (req, res) => {
  const health = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    checks: {}
  };

  try {
    // データベース接続チェック
    await db.query('SELECT 1');
    health.checks.database = 'ok';
  } catch (error) {
    health.checks.database = 'error';
    health.status = 'error';
  }

  try {
    // Redis接続チェック
    await cache.ping();
    health.checks.cache = 'ok';
  } catch (error) {
    health.checks.cache = 'error';
    health.status = 'error';
  }

  const statusCode = health.status === 'ok' ? 200 : 503;
  res.status(statusCode).json(health);
});
