# プロジェクト固有ルール: 年間スキル報告書WEB化PJT

## エグゼクティブサマリー

この文書は年間スキル報告書WEB化プロジェクトに特化した開発ルールと技術仕様を定義します。Next.js 14 + TypeScript + PostgreSQL技術スタック、シングルテナント設計から将来のマルチテナント化への移行戦略、要求仕様ID体系、AI駆動開発手法を提供し、7週間での実用的なシステム完成を目指します。汎用的な開発ルールは00-core-rules.mdを参照し、このファイルではプロジェクト固有の技術的制約と業務要件に焦点を当てています。

## プロジェクト基本情報

### プロジェクト概要
- **プロジェクト名**: 年間スキル報告書WEB化PJT
- **目的**: AI駆動開発の知見獲得 + 業務効率化・可視化の実現
- **技術スタック**: Next.js 14 + TypeScript + React 18 + Tailwind CSS + PostgreSQL + Docker
- **開発期間**: 2025年5月開始（現在進行中）
- **現在の実装**: シングルテナント設計で開発中（将来的にマルチテナント化を検討）

### 開発体制
- **責任者**: 黒澤 (@yusuke-kurosawa)
- **PM**: 中島 (@SAS-nakajima)  
- **PL**: 笹尾 (@SAS-sasao)

### プロジェクト成功指標
- **開発期間**: 7週間での実用システム完成
- **品質目標**: テストカバレッジ80%以上、レスポンス時間1秒以内
- **AI活用目標**: 開発効率50%向上、コード生成率70%以上
- **業務改善目標**: 作業時間50%削減、エラー70%削減

## 現在の実装方針（シングルテナント）

### 基本方針
- **実用性重視**: 7週間での完成を重視した実用的な設計
- **段階的アプローチ**: シングルテナント実装を完成後、将来的にマルチテナント化を検討
- **AI駆動開発**: AI活用による開発効率化と知見獲得
- **品質確保**: 基本機能の確実な動作を優先

### 設計方針
- **シンプルな設計**: 複雑性を排除した理解しやすい構造
- **拡張性考慮**: 将来のマルチテナント化を見据えた設計
- **実装完成**: フロントエンド画面100%完成、バックエンドAPI実装中
- **段階的機能追加**: 基本機能から順次機能を拡張

### 将来のマルチテナント要件（Phase 2以降）
- **複数のホールディングス・グループ会社での独立したデータ管理**
- 各会社（テナント）のデータ・設定・UI・権限の完全分離
- 統合管理による全体最適化とコスト効率化
- 将来的な新規グループ会社追加への対応

## 要求仕様ID体系

### カテゴリ分類
- **TNT**: Multi-Tenant (マルチテナント基盤要件)
- **PLT**: Platform (システム基盤要件)
- **ACC**: Access Control (ユーザー権限管理)
- **PRO**: Profile (個人プロフィール管理)
- **SKL**: Skill (スキル情報管理)
- **CAR**: Career (目標・キャリア管理)
- **WPM**: Work Performance Mgmt (作業実績管理)
- **TRN**: Training (研修・セミナー管理)
- **RPT**: Report (レポート出力)
- **NTF**: Notification (通知・連携サービス)

### 具体的な要求仕様ID例とマッピング
```
PLT.1-WEB.1    → ログイン画面・ダッシュボード基盤
PRO.1-BASE.1   → プロフィール管理機能
SKL.1-HIER.1   → スキル階層管理・スキルマップ表示
CAR.1-PLAN.1   → キャリア目標設定・進捗管理
WPM.1-DET.1    → 作業実績入力・管理
TRN.1-ATT.1    → 研修履歴・資格管理
RPT.1-EXCEL.1  → レポート生成・Excel出力
ACC.1-AUTH.1   → 認証・認可システム
ACC.1-ROLE.1   → ロールベースアクセス制御
NTF.1-MAIL.1   → メール通知機能
```

### 設計書との対応関係
- **画面設計書**: `SCR-{画面ID}` ↔ 要求仕様ID
- **API仕様書**: `API-{API番号}` ↔ 要求仕様ID
- **テーブル定義書**: `TBL-{テーブル番号}` ↔ 要求仕様ID

### 優先度基準
- **最高**: 業務フロー起点（ログイン、基本情報・スキル管理、システム基盤）
- **高**: 最低限の非機能（認証、権限、セキュリティ）、スキル管理・検索
- **中**: 日常業務運用（目標管理、作業実績、研修管理）
- **低**: 補助的機能（一括登録、レポート出力、分析・可視化）

### 実装優先順序（現実ベース）
1. **Phase 1**: 最高優先度（PLT.1-WEB.1, PRO.1-BASE.1, SKL.1-HIER.1）
2. **Phase 2**: 高優先度（認証・権限、スキル検索）
3. **Phase 3**: 中優先度（目標管理、作業実績、研修管理）
4. **Phase 4**: 低優先度（レポート出力、分析機能）

## 技術スタック詳細仕様

### Next.js 14 + App Router
- **App Router必須**: Pages Routerは使用禁止
- **Server Actions活用**: フォーム処理・データ更新はServer Actions優先
- **API Routes**: 外部連携・複雑なロジックのみAPI Routes使用
- **TypeScript厳密モード**: strict: true, noImplicitAny: true必須
- **ファイル構成**: App Routerの規約に従った構成

### TypeScript統一ルール（絶対必須）
- **JavaScript使用禁止**: 全ての実装コードはTypeScript必須
- **型安全性の徹底**: any型の使用は原則禁止
- **型定義の明記**: 全ての関数・変数・プロパティに型定義必須
- **厳密設定**: tsconfig.jsonでstrict: true, noImplicitAny: true必須
- **例外規定**: 設定ファイル（next.config.js, tailwind.config.js等）のみJavaScript許可
- **ドキュメント統一**: 全てのコード例はTypeScriptで記載必須

#### Next.js設定詳細
```javascript
// next.config.js
const nextConfig = {
  experimental: {
    serverActions: true,
    typedRoutes: true
  },
  typescript: {
    ignoreBuildErrors: false
  },
  eslint: {
    ignoreDuringBuilds: false
  }
}
```

### PostgreSQL + Prisma
- **Prisma必須**: 生SQLは特別な場合のみ許可
- **シングルテナント設計**: 現在の実装に合わせたスキーマ設計
- **型安全性**: Prisma Clientの型を活用
- **マイグレーション**: prisma migrateによる管理

#### Prisma設定詳細
```typescript
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

### Docker環境詳細設定
- **Docker Compose**: 開発環境の統一
- **PostgreSQL**: コンテナ化されたデータベース
- **環境変数**: .env による設定管理
- **ホットリロード**: 開発効率化のための設定

#### Docker Compose設定
```yaml
version: '3.8'
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    volumes:
      - .:/app
      - /app/node_modules
  
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: skill_report
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

### マルチテナント対応（将来実装）
- **テナントID分離**: 全データアクセスでテナントID必須
- **JWT + テナント識別**: 認証トークンにテナント情報を含める
- **UI分離**: テナント別カラーテーマ・ロゴ設定
- **通知分離**: テナント別メール・Teams・LINE WORKS設定

## 開発環境・ツール設定

### 開発サーバー起動手順
```bash
# Docker環境での開発
./scripts/docker-dev.sh

# ローカル環境での開発
npm install
npm run dev

# データベース初期化
npm run db:migrate
npm run db:seed
```

### データベース管理
```bash
# Prismaスキーマ更新
npx prisma db push

# マイグレーション生成
npx prisma migrate dev --name migration_name

# シードデータ投入
npx prisma db seed
```

### 自動化スクリプト
- **docker-dev.sh**: Docker環境での開発サーバー起動
- **generate-seed-*.sh**: シードデータ生成
- **init-db.sql**: データベース初期化

## 開発・実装ルール

### 必須事項
1. **要求仕様IDの明記**: 全実装に対応する要求仕様IDをコメントで記載
2. **画面ID・API IDの統一**: 設計書と実装でIDを一致させる
3. **TypeScript型安全性**: 厳密な型定義を必須とする
4. **レスポンシブ対応**: 全画面でマルチデバイス対応を実装
5. **エラーハンドリング**: 適切なエラー処理とユーザーフィードバック

### 実装パターン

#### コンポーネント設計パターン
```typescript
/**
 * 要求仕様ID: PRO.1-BASE.1
 * 対応設計書: docs/design/screens/specs/画面設計書_SCR-PROFILE_プロフィール画面.md
 */
export function ProfileComponent() {
  // 実装内容
}
```

#### API実装パターン
```typescript
/**
 * 要求仕様ID: API-011
 * 対応設計書: docs/design/api/specs/API定義書_API-011_プロフィール取得API.md
 */
export async function GET(request: NextRequest) {
  // API実装
}
```

#### エラーハンドリング方針
```typescript
// 統一されたエラーレスポンス形式
{
  success: false,
  error: {
    code: "VALIDATION_ERROR",
    message: "入力値に誤りがあります",
    details: [...]
  },
  timestamp: "2025-06-21T11:42:00Z"
}
```

### 非機能要件の必須実装
- **パフォーマンス**: API〜UI まで1秒以内
- **アクセシビリティ**: WCAG 2.1 AA準拠
- **セキュリティ**: AES-256暗号化、TLS必須
- **監査証跡**: 90日間ログ保持
- **レスポンシブ**: モバイル・タブレット・デスクトップ対応

## ファイル構成・命名規則

### ドキュメント構造
```
docs/
├── requirements/           # 要件定義関連
├── design/                # 設計関連
│   ├── screens/           # 画面設計
│   ├── api/              # API設計
│   ├── database/         # データベース設計
│   ├── batch/            # バッチ設計
│   ├── architecture/     # アーキテクチャ設計
│   └── interfaces/       # インターフェース設計
└── testing/              # テスト関連
```

### 設計書命名規則
- **画面設計書**: `画面設計書_SCR-{画面ID}_{画面名称}.md`
- **API仕様書**: `API仕様書_API-{API番号}_{API名称}.md`
- **テーブル定義書**: `テーブル定義書_TBL-{テーブル番号}_{テーブル名称}.md`
- **バッチ仕様書**: `バッチ仕様書_BATCH-{バッチ番号}_{バッチ名称}.md`

### ソースコード構造
```
src/
├── app/                   # Next.js App Router
│   ├── (auth)/           # 認証関連ルート
│   ├── dashboard/        # ダッシュボード
│   ├── profile/          # プロフィール管理
│   ├── skills/           # スキル管理
│   ├── career/           # キャリア管理
│   ├── work/             # 作業実績
│   ├── training/         # 研修管理
│   ├── reports/          # レポート
│   ├── api/              # API Routes
│   └── globals.css       # グローバルスタイル
├── components/           # Reactコンポーネント
│   ├── ui/              # 共通UIコンポーネント
│   ├── dashboard/       # ダッシュボード関連
│   ├── forms/           # フォーム関連
│   └── charts/          # チャート関連
├── lib/                 # ユーティリティ・設定
│   ├── auth.ts          # 認証関連
│   ├── prisma.ts        # Prisma設定
│   ├── utils.ts         # 共通ユーティリティ
│   └── validations.ts   # バリデーション
├── types/               # TypeScript型定義
│   ├── auth.ts          # 認証関連型
│   ├── user.ts          # ユーザー関連型
│   └── api.ts           # API関連型
└── database/            # データベース関連
    └── prisma/          # Prismaスキーマ・シード
```

## AI駆動開発の実践ガイドライン

### AI活用必須領域
1. **コード生成**: 定型的なCRUD操作、バリデーション
2. **テスト生成**: ユニット・統合・E2Eテストケース
3. **ドキュメント生成**: API仕様書、コメント
4. **設計支援**: アーキテクチャ提案、技術選定

### AI活用の具体的手法
- **GitHub Copilot**: コード補完・生成
- **ChatGPT/Claude**: 設計相談・コードレビュー
- **自動生成ツール**: API仕様書・テストケース生成
- **コード解析**: 品質チェック・リファクタリング提案

### AI生成コードの品質保証
- **レビュー必須**: AI生成コードも同等の品質基準を適用
- **テスト実装**: AI生成コードに対する適切なテスト
- **セキュリティチェック**: 脆弱性・セキュリティホールの確認
- **パフォーマンス検証**: 性能要件の達成確認

## テスト戦略

### テストフレームワーク選定
- **ユニットテスト**: Jest + Testing Library
- **統合テスト**: Jest + Supertest
- **E2Eテスト**: Playwright
- **コンポーネントテスト**: Storybook + Chromatic

### テスト実装方針
```typescript
// ユニットテスト例
describe('ProfileComponent', () => {
  it('should render user profile correctly', () => {
    // テスト実装
  });
});

// API統合テスト例
describe('Profile API', () => {
  it('should return user profile', async () => {
    // API テスト実装
  });
});
```

### テストカバレッジ目標
- **全体**: 80%以上
- **重要機能**: 95%以上
- **API**: 90%以上
- **コンポーネント**: 85%以上

## 品質保証・成功指標

### 品質ゲート
- **テストカバレッジ**: 80%以上を維持
- **静的解析**: 重大な問題0件
- **セキュリティ**: 脆弱性スキャン通過
- **パフォーマンス**: レスポンス時間1秒以内
- **アクセシビリティ**: WCAG 2.1 AA準拠

### 成功指標（KPI）
- **開発効率**: AI活用率70%以上、開発速度50%向上
- **業務改善**: 作業時間50%削減、エラー70%削減、利用率90%以上
- **システム品質**: 可用性99.5%以上、レスポンス時間1秒以内95%達成
- **ユーザー満足度**: NPS 70以上、利用継続率90%以上

### 測定可能なメトリクス
- **開発メトリクス**: コミット数、PR数、レビュー時間
- **品質メトリクス**: バグ発生率、修正時間、テスト通過率
- **パフォーマンスメトリクス**: ページ読み込み時間、API応答時間
- **ユーザーメトリクス**: アクティブユーザー数、機能利用率

## デプロイメント戦略

### 環境別設定
- **開発環境**: Docker Compose、ホットリロード有効
- **ステージング環境**: 本番同等設定、テストデータ
- **本番環境**: 最適化設定、監視・ログ強化

### デプロイ手順
```bash
# ステージング環境デプロイ
npm run build
npm run test
npm run deploy:staging

# 本番環境デプロイ
npm run build:production
npm run test:e2e
npm run deploy:production
```

### 監視・ログ設定
- **アプリケーション監視**: New Relic / DataDog
- **ログ管理**: CloudWatch / ELK Stack
- **エラー追跡**: Sentry
- **パフォーマンス監視**: Lighthouse CI

## 必須確認事項・禁止事項

### 必須確認事項
1. **要求仕様ID**: 全実装で対応IDを明確化
2. **設計書整合性**: 画面・API・DB設計の一貫性
3. **非機能要件**: パフォーマンス・セキュリティ・アクセシビリティ
4. **テスト実装**: 適切なテストカバレッジの確保
5. **AI活用記録**: 効果・課題の継続的記録

### 禁止事項
- 要求仕様IDなしの実装
- 設計書との不整合
- 非機能要件の未実装
- Pages Routerの使用
- 生SQLの多用（Prisma優先）
- テストなしのコード実装
- セキュリティチェックなしのデプロイ

## 開発フロー・チェックリスト

### 新機能開発フロー
1. **要求仕様確認**: 対応する要求仕様IDの確認
2. **設計書確認**: 関連する設計書の確認・更新
3. **実装**: コード実装（要求仕様IDコメント必須）
4. **テスト実装**: ユニット・統合テストの実装
5. **品質チェック**: 静的解析・セキュリティチェック
6. **レビュー**: コードレビュー・設計レビュー
7. **デプロイ**: ステージング→本番環境デプロイ

### 実装チェックリスト
- [ ] 要求仕様IDが明記されている
- [ ] 設計書との整合性が確認されている
- [ ] TypeScript型安全性が確保されている
- [ ] レスポンシブ対応が実装されている
- [ ] エラーハンドリングが適切に実装されている
- [ ] テストが実装されている（カバレッジ80%以上）
- [ ] セキュリティチェックが完了している
- [ ] パフォーマンス要件を満たしている
- [ ] アクセシビリティ要件を満たしている

---

このプロジェクト固有ルールに従って、年間スキル報告書WEB化PJTの開発を効率的かつ高品質に進めてください。
