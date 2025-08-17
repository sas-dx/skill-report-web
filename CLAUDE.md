# 年間スキル報告書WEB化プロジェクト - Claude Code設定

## プロジェクト概要
Next.js 14を使用した年間スキル報告書管理システムのモック実装からDB接続への移行作業

## 技術スタック
- **フレームワーク**: Next.js 14 (App Router)
- **言語**: TypeScript
- **DB**: PostgreSQL + Prisma ORM
- **UI**: Material-UI, TailwindCSS
- **認証**: セッション管理（実装済み）

## 重要なディレクトリ構造
```
src/
├── app/                    # Next.js App Router
│   ├── api/               # API Routes
│   ├── work/              # 作業実績管理
│   ├── skills/            # スキル管理
│   └── reports/           # レポート管理
├── components/            # React Components
├── lib/                   # ユーティリティ
│   └── mockData.ts       # モックデータ（削除予定）
└── database/
    └── prisma/
        └── schema.prisma  # データベーススキーマ
```

## 開発規約

### コーディング規約
- TypeScriptの厳格な型定義を維持
- エラーハンドリングは必須（try-catch）
- API レスポンスは統一形式: `{ success: boolean, data?: any, error?: string }`
- 日本語コメントOK（ビジネスロジック説明時）

### API開発規約
- REST API準拠
- Route Handlers (Next.js 14 App Router形式)を使用
- Prisma ORMを使用したDB操作
- 適切なHTTPステータスコードを返す

### Git コミット規約
- コミットメッセージは日本語OK
- 形式: `<type>: <要求仕様ID> <変更内容>`
- 例: `feat: WPM.1-DET.1 作業実績APIの実装`

## 現在の作業内容
キャリアプラン機能の完全実装 ✅ 完了
1. ✅ キャリア目標CRUD機能
2. ✅ 進捗管理機能（career-progress）
3. ✅ スキルギャップ分析（skill-gap）
4. ✅ アクションプラン管理（action-plans）
5. ✅ 上司フィードバック（manager-feedback）
6. 🔧 キャリアパスタイムライン（オプション）

## 実装済み機能
### API
#### キャリアプラン関連
- ✅ `/api/career-goals/[userId]` - キャリア目標のCRUD
- ✅ `/api/career-progress/[userId]` - 進捗管理（GET/PUT）
- ✅ `/api/career/skill-gap` - スキルギャップ分析
- ✅ `/api/career/action-plans` - アクションプラン管理
- ✅ `/api/career/action-plan/[id]` - アクションプラン個別操作
- ✅ `/api/career/action-plans/order` - アクションプラン順序変更
- ✅ `/api/career/manager-comment` - 上司フィードバック

#### その他の機能
- ✅ `/api/work/[userId]` - 作業実績管理
- ✅ `/api/skills/[userId]` - スキル管理
- ✅ `/api/skill-categories` - スキルカテゴリマスタ
- ✅ `/api/reports/*` - レポート管理
- ✅ `/api/notifications/[userId]` - 通知機能

### データベース連携
- `TRN_GoalProgress` - 目標進捗管理
- `TRN_CareerPlan` - キャリアプラン
- `TRN_ProjectRecord` - 作業実績
- `MST_Skill*` - スキル関連マスタ

## テストコマンド
```bash
# 開発サーバー起動
npm run dev

# TypeScriptチェック
npm run type-check

# Lintチェック
npm run lint

# ビルド
npm run build
```

## 注意事項
- モックデータ削除は段階的に実施
- 既存の型定義（types/）は再利用
- API実装時は既存のprofiles, trainings APIを参考
- エラーハンドリングとローディング状態の実装必須

## 参考ドキュメント
- API仕様: `docs/design/api/`
- 画面仕様: `docs/design/screens/`
- DB設計: `docs/design/database/`