# システムアーキテクチャ・パターン

## 全体アーキテクチャ

### Next.js 14統合アーキテクチャ
```
┌─────────────────────────────────────────────────────────────┐
│                    Next.js 14 App Router                    │
├─────────────────────────────────────────────────────────────┤
│  Frontend (React 18)          │  Backend (API Routes)       │
│  ├─ Pages & Components        │  ├─ API Endpoints           │
│  ├─ State Management         │  ├─ Business Logic          │
│  ├─ UI Components            │  ├─ Data Access Layer       │
│  └─ Client-side Logic        │  └─ Authentication          │
├─────────────────────────────────────────────────────────────┤
│                    Prisma ORM                              │
├─────────────────────────────────────────────────────────────┤
│              PostgreSQL 15 + Row Level Security            │
└─────────────────────────────────────────────────────────────┘
```

### マルチテナントアーキテクチャ
- **論理分離方式**: Row Level Security (RLS) + tenant_id
- **認証統合**: NextAuth.js + マルチテナント対応
- **データ分離**: PostgreSQL RLS による自動フィルタリング
- **UI分離**: テナント選択・切り替え機能

## データアーキテクチャパターン

### マルチテナントデータ分離
```sql
-- 全テーブル共通パターン
CREATE TABLE example_table (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES MST_Tenant(tenant_id),
    -- ビジネスデータ
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Row Level Security 設定
ALTER TABLE example_table ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON example_table
    FOR ALL TO authenticated
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);
```

### テーブル設計パターン

#### マスタテーブル（MST_）
- **MST_Tenant**: テナント基本情報
- **MST_TenantSettings**: テナント設定
- **MST_Department**: 部署マスタ（テナント別）
- **MST_SkillCategory**: スキルカテゴリ（テナント別）

#### トランザクションテーブル（TRN_）
- **TRN_UserProfile**: ユーザープロフィール
- **TRN_SkillAssessment**: スキル評価
- **TRN_CareerPlan**: キャリアプラン
- **TRN_WorkExperience**: 作業実績

#### 履歴テーブル（HIS_）
- **HIS_LoginHistory**: ログイン履歴
- **HIS_NotificationLog**: 通知送信履歴
- **HIS_TenantBilling**: テナント課金履歴

## APIアーキテクチャパターン

### RESTful API設計
```typescript
// API構造パターン
/api/v1/{resource}
├─ GET    /api/v1/users          // 一覧取得
├─ GET    /api/v1/users/{id}     // 詳細取得
├─ POST   /api/v1/users          // 新規作成
├─ PUT    /api/v1/users/{id}     // 更新
└─ DELETE /api/v1/users/{id}     // 削除

// マルチテナント対応
/api/v1/tenants/{tenant_id}/{resource}
```

### API認証・認可パターン
```typescript
// 認証フロー
1. ログイン → JWT トークン発行
2. テナント選択 → テナント情報をセッションに保存
3. API リクエスト → テナント情報を自動付与
4. データアクセス → RLS による自動フィルタリング

// ミドルウェア構成
export async function middleware(request: NextRequest) {
  // 1. 認証チェック
  // 2. テナント情報取得
  // 3. RLS設定
  // 4. 権限チェック
}
```

### レスポンス形式統一
```typescript
// 成功レスポンス
interface SuccessResponse<T> {
  success: true;
  data: T;
  pagination?: PaginationInfo;
  timestamp: string;
}

// エラーレスポンス
interface ErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: any;
  };
  timestamp: string;
}
```

## フロントエンドアーキテクチャパターン

### コンポーネント設計パターン
```
src/
├─ app/                    # Next.js App Router
│  ├─ (auth)/             # 認証関連ページ
│  ├─ (dashboard)/        # ダッシュボード
│  ├─ (tenant)/           # テナント管理
│  └─ api/                # API Routes
├─ components/             # 共通コンポーネント
│  ├─ ui/                 # UIコンポーネント
│  ├─ business/           # ビジネスコンポーネント
│  └─ layout/             # レイアウトコンポーネント
├─ lib/                   # ユーティリティ
├─ hooks/                 # カスタムフック
└─ types/                 # 型定義
```

### 状態管理パターン
```typescript
// Zustand による状態管理
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
  
  // UI状態
  ui: {
    loading: boolean;
    notifications: Notification[];
  };
}
```

### テナント切り替えパターン
```typescript
// テナント切り替えフロー
const switchTenant = async (tenantId: string) => {
  // 1. テナント情報検証
  // 2. セッション更新
  // 3. 画面リロード
  // 4. データ再取得
};
```

## バックエンドアーキテクチャパターン

### レイヤードアーキテクチャ
```
API Routes (Next.js)
├─ Controllers/        # リクエスト処理
├─ Services/          # ビジネスロジック
├─ Repositories/      # データアクセス
└─ Models/           # データモデル
```

### サービス層パターン
```typescript
// ビジネスロジック分離
class UserService {
  constructor(
    private userRepository: UserRepository,
    private tenantService: TenantService
  ) {}
  
  async createUser(userData: CreateUserData): Promise<User> {
    // 1. バリデーション
    // 2. テナント権限チェック
    // 3. ビジネスルール適用
    // 4. データ保存
    // 5. 通知送信
  }
}
```

### リポジトリパターン
```typescript
// データアクセス抽象化
interface UserRepository {
  findById(id: string): Promise<User | null>;
  findByTenant(tenantId: string): Promise<User[]>;
  create(userData: CreateUserData): Promise<User>;
  update(id: string, userData: UpdateUserData): Promise<User>;
  delete(id: string): Promise<void>;
}
```

## セキュリティパターン

### 認証・認可フロー
```typescript
// 多層防御パターン
1. フロントエンド: ルートガード
2. API Gateway: JWT検証
3. ビジネス層: 権限チェック
4. データ層: RLS適用
```

### データ保護パターン
```typescript
// 暗号化パターン
- 保存時暗号化: AES-256
- 通信時暗号化: TLS 1.3
- パスワード: bcrypt ハッシュ化
- 機密データ: 環境変数管理
```

## バッチ処理パターン

### バッチアーキテクチャ
```
Cron Scheduler
├─ システム監視バッチ群 (BATCH-001~007)
├─ データ管理バッチ群 (BATCH-101~105)
├─ レポート生成バッチ群 (BATCH-201~205)
├─ テナント管理バッチ群 (BATCH-301~307)
├─ 通知・連携バッチ群 (BATCH-401~409)
└─ 監視・最適化バッチ群 (BATCH-501~508)
```

### バッチ実行パターン
```typescript
// 共通バッチ基盤
abstract class BaseBatch {
  abstract execute(): Promise<void>;
  
  async run(): Promise<void> {
    try {
      await this.beforeExecute();
      await this.execute();
      await this.afterExecute();
    } catch (error) {
      await this.handleError(error);
    }
  }
}
```

## 監視・ログパターン

### 構造化ログ
```typescript
// ログ出力パターン
interface LogEntry {
  timestamp: string;
  level: 'ERROR' | 'WARN' | 'INFO' | 'DEBUG';
  tenantId?: string;
  userId?: string;
  action: string;
  details: any;
  traceId: string;
}
```

### メトリクス収集
```typescript
// パフォーマンス監視
- レスポンス時間
- スループット
- エラー率
- リソース使用率
- テナント別使用量
```

## デプロイメントパターン

### Vercel Platform構成
```
Production Environment
├─ Next.js Application (Vercel)
├─ PostgreSQL Database (Vercel Postgres)
├─ File Storage (Vercel Blob)
├─ Monitoring (Vercel Analytics)
└─ CDN (Vercel Edge Network)
```

### CI/CD パイプライン
```
GitHub Actions
├─ Code Quality Check
├─ Unit Tests
├─ Integration Tests
├─ Security Scan
├─ Build & Deploy
└─ Post-deployment Tests
```

## 拡張性パターン

### 水平スケーリング
- **アプリケーション**: Vercel Serverless Functions
- **データベース**: PostgreSQL Read Replicas
- **ファイル**: Vercel Blob Storage
- **CDN**: Vercel Edge Network

### 垂直スケーリング
- **コンピュート**: Vercel Pro Plan
- **データベース**: PostgreSQL スケールアップ
- **ストレージ**: 容量拡張
- **帯域**: 帯域幅拡張

これらのパターンにより、スケーラブルで保守性の高いマルチテナントシステムを実現します。
