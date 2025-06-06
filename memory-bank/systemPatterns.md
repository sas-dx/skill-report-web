# システムアーキテクチャ・パターン

## 現在の実装アーキテクチャ

### Next.js 14統合アーキテクチャ（実装済み）
```
┌─────────────────────────────────────────────────────────────┐
│                    Next.js 14 App Router                    │
├─────────────────────────────────────────────────────────────┤
│  Frontend (React 18)          │  Backend (API Routes)       │
│  ├─ Pages & Components ✅     │  ├─ API Endpoints 🔄        │
│  ├─ State Management 🔄       │  ├─ Business Logic ❌        │
│  ├─ UI Components ✅          │  ├─ Data Access Layer 🔄    │
│  └─ Client-side Logic ✅      │  └─ Authentication 🔄       │
├─────────────────────────────────────────────────────────────┤
│                    Prisma ORM ✅                            │
├─────────────────────────────────────────────────────────────┤
│              PostgreSQL 15 (シングルテナント) ✅            │
└─────────────────────────────────────────────────────────────┘
```

**凡例**: ✅実装済み / 🔄部分実装 / ❌未実装

### 現在の実装状況
- **シングルテナント設計**: tenant_idカラムなし
- **基本認証**: 簡易ログイン機能のみ
- **フロントエンド**: 基本画面・コンポーネント実装済み
- **バックエンド**: 基本API構造のみ

## データアーキテクチャパターン

### 現在のデータ構造（シングルテナント）
```sql
-- 現在の実装パターン
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    emp_no VARCHAR(20) UNIQUE,
    email VARCHAR(255) UNIQUE,
    name VARCHAR(100),
    -- tenant_id なし（シングルテナント）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 設計書のマルチテナントパターン（未実装）
```sql
-- 設計書のパターン（未実装）
CREATE TABLE example_table (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES MST_Tenant(tenant_id),
    -- ビジネスデータ
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Row Level Security 設定（未実装）
ALTER TABLE example_table ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON example_table
    FOR ALL TO authenticated
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);
```

### 実装済みテーブル構造

#### 実装済みテーブル（シングルテナント版）
- **User**: ユーザー基本情報
- **UserAuth**: 認証情報
- **Role/Permission**: 権限管理
- **Department/Position**: 組織管理
- **SkillMaster/SkillCategory**: スキル管理
- **UserSkill**: ユーザースキル評価
- **CareerPlan/CareerProgress**: キャリア管理
- **WorkRecord**: 作業実績
- **Training/UserTraining**: 研修管理
- **AuditLog**: 監査ログ

#### 未実装テーブル（マルチテナント関連）
- **MST_Tenant**: テナント基本情報
- **MST_TenantSettings**: テナント設定
- **HIS_LoginHistory**: ログイン履歴
- **HIS_NotificationLog**: 通知送信履歴
- **HIS_TenantBilling**: テナント課金履歴

## APIアーキテクチャパターン

### 現在のAPI構造（実装済み）
```typescript
// 基本API構造
/api/auth/login          // ✅ 実装済み

// 未実装API
/api/v1/{resource}       // ❌ 未実装
├─ GET    /api/v1/users
├─ GET    /api/v1/users/{id}
├─ POST   /api/v1/users
├─ PUT    /api/v1/users/{id}
└─ DELETE /api/v1/users/{id}
```

### 設計書のマルチテナントAPI（未実装）
```typescript
// マルチテナント対応API（設計のみ）
/api/v1/tenants/{tenant_id}/{resource}
```

### 現在の認証パターン（部分実装）
```typescript
// 実装済み: 基本認証
export async function POST(request: NextRequest) {
  // 基本的なログイン処理のみ
}

// 未実装: マルチテナント認証
// 1. ログイン → JWT トークン発行
// 2. テナント選択 → テナント情報をセッションに保存
// 3. API リクエスト → テナント情報を自動付与
// 4. データアクセス → RLS による自動フィルタリング
```

### レスポンス形式（未統一）
```typescript
// 設計書の統一形式（未実装）
interface SuccessResponse<T> {
  success: true;
  data: T;
  pagination?: PaginationInfo;
  timestamp: string;
}

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

### 実装済みコンポーネント構造
```
src/
├─ app/                    # Next.js App Router ✅
│  ├─ dashboard/page.tsx   # ダッシュボード ✅
│  ├─ profile/page.tsx     # プロフィール ✅
│  ├─ skills/page.tsx      # スキル管理 ✅
│  ├─ career/page.tsx      # キャリア ✅
│  ├─ work/page.tsx        # 作業実績 ✅
│  ├─ training/page.tsx    # 研修 ✅
│  ├─ reports/page.tsx     # レポート ✅
│  └─ api/auth/login/      # 認証API ✅
├─ components/             # 共通コンポーネント ✅
│  ├─ ui/                 # UIコンポーネント ✅
│  ├─ dashboard/          # ダッシュボード関連 ✅
│  ├─ training/           # 研修関連 ✅
│  └─ reports/            # レポート関連 ✅
├─ lib/                   # ユーティリティ ✅
│  ├─ auth.ts            # 認証ロジック ✅
│  ├─ utils.ts           # 共通ユーティリティ ✅
│  └─ mockData.ts        # モックデータ ✅
```

### 未実装コンポーネント（マルチテナント関連）
```
src/
├─ app/
│  ├─ (auth)/             # 認証関連ページ ❌
│  ├─ (tenant)/           # テナント管理 ❌
│  └─ tenant-select/      # テナント選択 ❌
├─ components/
│  ├─ tenant/             # テナント関連 ❌
│  └─ auth/               # 認証関連 ❌
```

### 状態管理パターン（未実装）
```typescript
// 設計書の状態管理（未実装）
interface AppState {
  // 認証状態
  auth: {
    user: User | null;
    isAuthenticated: boolean;
  };
  
  // テナント状態（未実装）
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

### 現在の実装パターン
```typescript
// 実装済み: 基本的なページコンポーネント
export default function DashboardPage() {
  return <DashboardContent />;
}

// 未実装: テナント切り替えパターン
const switchTenant = async (tenantId: string) => {
  // 1. テナント情報検証
  // 2. セッション更新
  // 3. 画面リロード
  // 4. データ再取得
};
```

## バックエンドアーキテクチャパターン

### 現在の実装構造
```
API Routes (Next.js) ✅
├─ Controllers/        # リクエスト処理 🔄
├─ Services/          # ビジネスロジック ❌
├─ Repositories/      # データアクセス ❌
└─ Models/           # データモデル ✅ (Prisma)
```

### 実装済みサービス層（基本のみ）
```typescript
// 基本的な認証のみ実装
export async function authenticateUser(credentials: LoginCredentials) {
  // 基本的なログイン処理
}

// 未実装: ビジネスロジック分離
class UserService {
  constructor(
    private userRepository: UserRepository,
    private tenantService: TenantService // 未実装
  ) {}
  
  async createUser(userData: CreateUserData): Promise<User> {
    // 1. バリデーション
    // 2. テナント権限チェック（未実装）
    // 3. ビジネスルール適用
    // 4. データ保存
    // 5. 通知送信（未実装）
  }
}
```

### リポジトリパターン（未実装）
```typescript
// 設計書のパターン（未実装）
interface UserRepository {
  findById(id: string): Promise<User | null>;
  findByTenant(tenantId: string): Promise<User[]>;
  create(userData: CreateUserData): Promise<User>;
  update(id: string, userData: UpdateUserData): Promise<User>;
  delete(id: string): Promise<void>;
}
```

## セキュリティパターン

### 現在の実装（基本のみ）
```typescript
// 実装済み: 基本認証
export async function POST(request: NextRequest) {
  const { email, password } = await request.json();
  // 基本的なパスワード検証のみ
}

// 未実装: 多層防御パターン
// 1. フロントエンド: ルートガード
// 2. API Gateway: JWT検証
// 3. ビジネス層: 権限チェック
// 4. データ層: RLS適用
```

### データ保護パターン（部分実装）
```typescript
// 実装済み: 基本設定
- パスワード: bcrypt ハッシュ化 ✅
- 環境変数: .env管理 ✅

// 未実装: 高度なセキュリティ
- 保存時暗号化: AES-256 ❌
- 通信時暗号化: TLS 1.3 ❌
- 機密データ管理: 専用暗号化 ❌
```

## バッチ処理パターン

### 設計書のバッチアーキテクチャ（未実装）
```
Cron Scheduler ❌
├─ システム監視バッチ群 (BATCH-001~007) ❌
├─ データ管理バッチ群 (BATCH-101~105) ❌
├─ レポート生成バッチ群 (BATCH-201~205) ❌
├─ テナント管理バッチ群 (BATCH-301~307) ❌
├─ 通知・連携バッチ群 (BATCH-401~409) ❌
└─ 監視・最適化バッチ群 (BATCH-501~508) ❌
```

### バッチ実行パターン（未実装）
```typescript
// 設計書の共通バッチ基盤（未実装）
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

### 現在の実装（基本のみ）
```typescript
// 基本的なconsole.log使用
console.log('User logged in');

// 未実装: 構造化ログ
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

### メトリクス収集（未実装）
```typescript
// 未実装: パフォーマンス監視
- レスポンス時間 ❌
- スループット ❌
- エラー率 ❌
- リソース使用率 ❌
- テナント別使用量 ❌
```

## デプロイメントパターン

### 現在の環境構成
```
Development Environment ✅
├─ Next.js Application (Docker) ✅
├─ PostgreSQL Database (Docker) ✅
├─ pgAdmin (Docker) ✅
└─ Local Development ✅

Production Environment ❌
├─ Next.js Application (Vercel) ❌
├─ PostgreSQL Database (Vercel Postgres) ❌
├─ File Storage (Vercel Blob) ❌
├─ Monitoring (Vercel Analytics) ❌
└─ CDN (Vercel Edge Network) ❌
```

### CI/CD パイプライン（未実装）
```
GitHub Actions ❌
├─ Code Quality Check ❌
├─ Unit Tests ❌
├─ Integration Tests ❌
├─ Security Scan ❌
├─ Build & Deploy ❌
└─ Post-deployment Tests ❌
```

## 実装方針の選択肢

### 選択肢1: マルチテナント対応実装
**必要な変更**:
- 全テーブルにtenant_id追加
- Row Level Security実装
- 認証システム拡張
- フロントエンド修正

### 選択肢2: シングルテナント継続
**現在の実装活用**:
- 既存スキーマ継続使用
- API実装完成
- 機能完成度向上

### 選択肢3: 段階的移行
**Phase 1**: シングルテナント完成
**Phase 2**: マルチテナント化

## 拡張性パターン

### 水平スケーリング（未実装）
- **アプリケーション**: Vercel Serverless Functions ❌
- **データベース**: PostgreSQL Read Replicas ❌
- **ファイル**: Vercel Blob Storage ❌
- **CDN**: Vercel Edge Network ❌

### 垂直スケーリング（未実装）
- **コンピュート**: Vercel Pro Plan ❌
- **データベース**: PostgreSQL スケールアップ ❌
- **ストレージ**: 容量拡張 ❌
- **帯域**: 帯域幅拡張 ❌

## 次回実装時の重点項目

### 実装方針決定後の作業
1. **マルチテナント選択時**: スキーマ全面改修
2. **シングルテナント選択時**: API・機能実装完成
3. **段階的移行選択時**: Phase 1完成後にマルチテナント化

### 共通実装項目
1. **API実装**: CRUD操作の完全実装
2. **認証強化**: セキュリティ向上
3. **テスト実装**: 品質保証
4. **デプロイ準備**: 本番環境構築

この現実的なシステムパターン情報により、実装方針決定と今後の開発計画策定を適切に行うことができます。
