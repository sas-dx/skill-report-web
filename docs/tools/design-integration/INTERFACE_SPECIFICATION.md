# 🔌 設計統合ツール - インターフェース仕様書

## エグゼクティブサマリー

この文書は設計統合ツールの包括的なインターフェース仕様を定義します。CLI・Web UI・RESTful API・プラグインAPIの詳細仕様、統一されたデータ形式、エラーハンドリング、認証・認可システムを提供し、一貫性のあるユーザーエクスペリエンスと開発者エクスペリエンスを実現します。標準化されたインターフェースにより、異なるクライアントからの統一的なアクセスと、サードパーティ製プラグインの容易な開発を支援します。

## 🎯 インターフェース設計原則

### 基本原則
- **一貫性**: 全インターフェースで統一されたデータ形式・エラー処理
- **直感性**: 予測可能で理解しやすいAPI設計
- **拡張性**: 将来の機能追加に対応可能な設計
- **互換性**: バージョン間の後方互換性保証
- **セキュリティ**: 適切な認証・認可・入力検証

### 設計パターン
- **RESTful設計**: リソース指向のAPI設計
- **統一レスポンス**: 成功・エラー共通のレスポンス形式
- **バージョニング**: URLパスによるAPIバージョン管理
- **ページネーション**: 大量データの効率的な取得
- **フィルタリング**: 柔軟な検索・絞り込み機能

## 🖥️ CLI インターフェース仕様

### 基本コマンド構造
```bash
design-tools [GLOBAL_OPTIONS] <command> [SUBCOMMAND] [OPTIONS] [ARGS]
```

### グローバルオプション
```bash
# 設定・出力制御
--config PATH              # 設定ファイルパス（デフォルト: config/default.yaml）
--verbose, -v               # 詳細出力モード
--quiet, -q                 # 静寂モード（エラーのみ出力）
--debug                     # デバッグモード（詳細ログ出力）

# ログ制御
--log-level LEVEL           # ログレベル（DEBUG|INFO|WARNING|ERROR）
--log-file PATH             # ログファイル出力先
--no-color                  # カラー出力無効化

# 出力形式
--output-format FORMAT     # 出力形式（table|json|yaml|csv）
--output-file PATH          # 出力ファイル指定
--pretty                    # 整形された出力

# 並列処理
--parallel                  # 並列処理有効化
--max-workers N             # 最大ワーカー数（デフォルト: 4）

# その他
--version                   # バージョン情報表示
--help, -h                  # ヘルプ表示
```

### データベース管理コマンド
```bash
# YAML検証
design-tools database validate [OPTIONS] [FILES...]
  --strict                  # 厳密モード（警告もエラー扱い）
  --schema PATH             # カスタムスキーマファイル
  --fix                     # 自動修復可能な問題を修正
  --report PATH             # 検証レポート出力先

# DDL生成
design-tools database generate ddl [OPTIONS] [FILES...]
  --output-dir PATH         # 出力ディレクトリ
  --database-type TYPE      # データベース種別（postgresql|mysql|sqlite）
  --include-indexes         # インデックス定義を含める
  --include-constraints     # 制約定義を含める
  --template PATH           # カスタムテンプレート

# 定義書生成
design-tools database generate docs [OPTIONS] [FILES...]
  --output-dir PATH         # 出力ディレクトリ
  --format FORMAT           # 出力形式（markdown|html|pdf）
  --template PATH           # カスタムテンプレート
  --include-samples         # サンプルデータを含める

# 整合性チェック
design-tools database check [OPTIONS]
  --fix                     # 自動修復実行
  --report PATH             # チェック結果レポート
  --ignore-warnings         # 警告を無視

# テーブル一覧
design-tools database list [OPTIONS]
  --filter PATTERN          # フィルタパターン
  --sort FIELD              # ソートフィールド
  --category CATEGORY       # カテゴリフィルタ

# テーブル詳細
design-tools database show TABLE_NAME [OPTIONS]
  --format FORMAT           # 出力形式
  --include-relations       # 関連テーブル情報を含める
```

### API管理コマンド
```bash
# API仕様検証
design-tools api validate [OPTIONS] [FILES...]
  --openapi-version VERSION # OpenAPIバージョン指定
  --strict                  # 厳密モード
  --check-examples          # サンプルデータ検証

# OpenAPI生成
design-tools api generate openapi [OPTIONS] [FILES...]
  --output-file PATH        # 出力ファイル
  --version VERSION         # API バージョン
  --title TITLE             # API タイトル
  --description DESC        # API 説明

# API ドキュメント生成
design-tools api generate docs [OPTIONS] [FILES...]
  --output-dir PATH         # 出力ディレクトリ
  --format FORMAT           # 出力形式（html|pdf|markdown）
  --theme THEME             # ドキュメントテーマ

# エンドポイント一覧
design-tools api list [OPTIONS]
  --method METHOD           # HTTPメソッドフィルタ
  --path-pattern PATTERN    # パスパターンフィルタ
  --tag TAG                 # タグフィルタ

# エンドポイント詳細
design-tools api show ENDPOINT [OPTIONS]
  --include-examples        # サンプルを含める
  --include-schemas         # スキーマ定義を含める
```

### 画面管理コマンド
```bash
# 画面仕様検証
design-tools screen validate [OPTIONS] [FILES...]
  --check-accessibility     # アクセシビリティチェック
  --check-responsive        # レスポンシブデザインチェック
  --check-components        # コンポーネント整合性チェック

# HTML生成
design-tools screen generate html [OPTIONS] [FILES...]
  --output-dir PATH         # 出力ディレクトリ
  --template PATH           # HTMLテンプレート
  --include-css             # CSS ファイル生成
  --include-js              # JavaScript ファイル生成

# コンポーネント一覧
design-tools screen list [OPTIONS]
  --type TYPE               # コンポーネントタイプフィルタ
  --status STATUS           # ステータスフィルタ

# コンポーネント詳細
design-tools screen show COMPONENT [OPTIONS]
  --include-usage           # 使用例を含める
  --include-props           # プロパティ定義を含める
```

### 統合チェックコマンド
```bash
# 統合整合性チェック
design-tools integration check [OPTIONS]
  --scope SCOPE             # チェック範囲（database|api|screen|all）
  --fix                     # 自動修復実行
  --report PATH             # チェック結果レポート
  --parallel                # 並列チェック実行

# 整合性レポート生成
design-tools integration report [OPTIONS]
  --format FORMAT           # レポート形式（html|pdf|json）
  --output PATH             # 出力先
  --include-suggestions     # 改善提案を含める

# 自動修復
design-tools integration fix [OPTIONS]
  --dry-run                 # 実行せずに変更内容を表示
  --backup                  # 修復前にバックアップ作成
  --scope SCOPE             # 修復範囲
```

### レポート生成コマンド
```bash
# 総合レポート生成
design-tools report generate [OPTIONS]
  --type TYPE               # レポートタイプ（summary|detailed|metrics）
  --format FORMAT           # 出力形式（html|pdf|json）
  --output PATH             # 出力先
  --period PERIOD           # 対象期間

# ダッシュボード起動
design-tools report dashboard [OPTIONS]
  --port PORT               # ポート番号（デフォルト: 8080）
  --host HOST               # ホスト名（デフォルト: localhost）
  --auto-refresh SECONDS    # 自動更新間隔

# メトリクス出力
design-tools report metrics [OPTIONS]
  --format FORMAT           # 出力形式（json|csv|prometheus）
  --output PATH             # 出力先
```

### CLI出力例
```bash
# 成功時の出力例
$ design-tools database validate
✅ 検証完了: 42個のテーブル定義を検証しました
📊 結果: 成功 40個, 警告 2個, エラー 0個
⚠️  警告:
  - MST_Employee: overview セクションが短すぎます (25文字 < 50文字)
  - TRN_SkillRecord: notes セクションの項目数が不足しています (2項目 < 3項目)

# エラー時の出力例
$ design-tools database validate
❌ 検証失敗: 3個のエラーが見つかりました
📊 結果: 成功 39個, 警告 2個, エラー 3個
🚨 エラー:
  - MST_Department: 必須セクション 'revision_history' が見つかりません
  - TRN_WorkRecord: 無効なデータ型 'INVALID_TYPE' が指定されています
  - HIS_AuditLog: 外部キー参照先テーブル 'MST_NonExistent' が存在しません

# 進捗表示例
$ design-tools database generate ddl --parallel
🔄 DDL生成中...
████████████████████████████████████████ 100% (42/42) [00:03<00:00, 14.2 tables/s]
✅ DDL生成完了: docs/design/database/ddl/ に42個のファイルを生成しました
```

## 🌐 Web UI インターフェース仕様

### アプリケーション構造
```
Web UI Application
├── Dashboard                    # ダッシュボード
│   ├── Overview                 # 概要・統計情報
│   ├── Recent Activity          # 最近の活動
│   └── Quick Actions            # クイックアクション
├── Database Management          # データベース管理
│   ├── Table List               # テーブル一覧
│   ├── Table Editor             # テーブル編集
│   ├── Validation Results       # 検証結果
│   └── DDL Generator            # DDL生成
├── API Management               # API管理
│   ├── Endpoint List            # エンドポイント一覧
│   ├── API Editor               # API編集
│   ├── OpenAPI Generator        # OpenAPI生成
│   └── Documentation            # ドキュメント
├── Screen Management            # 画面管理
│   ├── Component List           # コンポーネント一覧
│   ├── Screen Editor            # 画面編集
│   ├── HTML Generator           # HTML生成
│   └── Preview                  # プレビュー
├── Integration                  # 統合管理
│   ├── Consistency Check        # 整合性チェック
│   ├── Cross References         # 相互参照
│   └── Auto Fix                 # 自動修復
├── Reports                      # レポート
│   ├── Summary Report           # サマリーレポート
│   ├── Detailed Report          # 詳細レポート
│   ├── Metrics Dashboard        # メトリクスダッシュボード
│   └── Export                   # エクスポート
└── Settings                     # 設定
    ├── Configuration            # 設定管理
    ├── Plugins                  # プラグイン管理
    ├── Users                    # ユーザー管理
    └── System                   # システム設定
```

### ページ仕様

#### ダッシュボード (`/`)
```html
<!-- レイアウト構造 -->
<div class="dashboard">
  <!-- ヘッダー -->
  <header class="header">
    <nav class="navigation">
      <div class="logo">Design Integration Tools</div>
      <ul class="nav-menu">
        <li><a href="/database">Database</a></li>
        <li><a href="/api">API</a></li>
        <li><a href="/screen">Screen</a></li>
        <li><a href="/integration">Integration</a></li>
        <li><a href="/reports">Reports</a></li>
      </ul>
      <div class="user-menu">
        <span class="user-name">Admin User</span>
        <button class="logout">Logout</button>
      </div>
    </nav>
  </header>

  <!-- メインコンテンツ -->
  <main class="main-content">
    <!-- 統計カード -->
    <section class="stats-cards">
      <div class="card">
        <h3>Tables</h3>
        <div class="count">42</div>
        <div class="status">✅ All Valid</div>
      </div>
      <div class="card">
        <h3>APIs</h3>
        <div class="count">28</div>
        <div class="status">⚠️ 2 Warnings</div>
      </div>
      <div class="card">
        <h3>Screens</h3>
        <div class="count">15</div>
        <div class="status">✅ All Valid</div>
      </div>
      <div class="card">
        <h3>Integration</h3>
        <div class="count">98%</div>
        <div class="status">✅ Consistent</div>
      </div>
    </section>

    <!-- 最近の活動 -->
    <section class="recent-activity">
      <h2>Recent Activity</h2>
      <ul class="activity-list">
        <li>
          <span class="timestamp">2025-06-27 06:30</span>
          <span class="action">Table MST_Employee updated</span>
          <span class="user">by Admin</span>
        </li>
        <!-- 他の活動項目 -->
      </ul>
    </section>

    <!-- クイックアクション -->
    <section class="quick-actions">
      <h2>Quick Actions</h2>
      <div class="action-buttons">
        <button class="btn btn-primary">Validate All</button>
        <button class="btn btn-secondary">Generate DDL</button>
        <button class="btn btn-secondary">Check Integration</button>
        <button class="btn btn-secondary">Generate Report</button>
      </div>
    </section>
  </main>
</div>
```

#### データベース管理 (`/database`)
```html
<div class="database-management">
  <!-- サイドバー -->
  <aside class="sidebar">
    <nav class="sidebar-nav">
      <ul>
        <li><a href="/database/tables">Tables</a></li>
        <li><a href="/database/validate">Validation</a></li>
        <li><a href="/database/generate">Generation</a></li>
        <li><a href="/database/settings">Settings</a></li>
      </ul>
    </nav>
  </aside>

  <!-- メインコンテンツ -->
  <main class="content">
    <!-- テーブル一覧 -->
    <section class="table-list">
      <header class="section-header">
        <h1>Database Tables</h1>
        <div class="actions">
          <button class="btn btn-primary">Add Table</button>
          <button class="btn btn-secondary">Validate All</button>
          <button class="btn btn-secondary">Generate DDL</button>
        </div>
      </header>

      <!-- フィルター・検索 -->
      <div class="filters">
        <input type="text" placeholder="Search tables..." class="search-input">
        <select class="category-filter">
          <option value="">All Categories</option>
          <option value="マスタ系">マスタ系</option>
          <option value="トランザクション系">トランザクション系</option>
          <option value="履歴系">履歴系</option>
        </select>
        <select class="status-filter">
          <option value="">All Status</option>
          <option value="valid">Valid</option>
          <option value="warning">Warning</option>
          <option value="error">Error</option>
        </select>
      </div>

      <!-- テーブル一覧表 -->
      <table class="table-grid">
        <thead>
          <tr>
            <th>Table Name</th>
            <th>Category</th>
            <th>Columns</th>
            <th>Status</th>
            <th>Last Updated</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><a href="/database/tables/MST_Employee">MST_Employee</a></td>
            <td>マスタ系</td>
            <td>12</td>
            <td><span class="status-badge valid">✅ Valid</span></td>
            <td>2025-06-27 06:30</td>
            <td>
              <button class="btn-icon" title="Edit">✏️</button>
              <button class="btn-icon" title="Validate">🔍</button>
              <button class="btn-icon" title="Generate">⚙️</button>
            </td>
          </tr>
          <!-- 他のテーブル行 -->
        </tbody>
      </table>

      <!-- ページネーション -->
      <div class="pagination">
        <button class="btn btn-sm">Previous</button>
        <span class="page-info">Page 1 of 3</span>
        <button class="btn btn-sm">Next</button>
      </div>
    </section>
  </main>
</div>
```

### JavaScript API クライアント
```javascript
// Web UI用 JavaScript APIクライアント
class DesignToolsAPI {
  constructor(baseURL = '/api/v1') {
    this.baseURL = baseURL;
  }

  // データベース管理API
  async validateTables(options = {}) {
    const response = await fetch(`${this.baseURL}/database/validate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(options)
    });
    return await response.json();
  }

  async generateDDL(tableNames = [], options = {}) {
    const response = await fetch(`${this.baseURL}/database/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tables: tableNames, ...options })
    });
    return await response.json();
  }

  async getTables(filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${this.baseURL}/database/tables?${params}`);
    return await response.json();
  }

  async getTable(tableName) {
    const response = await fetch(`${this.baseURL}/database/tables/${tableName}`);
    return await response.json();
  }

  // API管理API
  async validateAPIs(options = {}) {
    const response = await fetch(`${this.baseURL}/api/validate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(options)
    });
    return await response.json();
  }

  async getEndpoints(filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${this.baseURL}/api/endpoints?${params}`);
    return await response.json();
  }

  // 統合チェックAPI
  async checkIntegration(options = {}) {
    const response = await fetch(`${this.baseURL}/integration/check`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(options)
    });
    return await response.json();
  }

  // レポート生成API
  async generateReport(type, options = {}) {
    const response = await fetch(`${this.baseURL}/reports/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type, ...options })
    });
    return await response.json();
  }
}

// 使用例
const api = new DesignToolsAPI();

// テーブル一覧取得
api.getTables({ category: 'マスタ系', status: 'valid' })
  .then(data => {
    console.log('Tables:', data.tables);
    updateTableList(data.tables);
  })
  .catch(error => {
    console.error('Error:', error);
    showErrorMessage('Failed to load tables');
  });

// 検証実行
api.validateTables({ strict: true })
  .then(result => {
    console.log('Validation result:', result);
    updateValidationStatus(result);
  });
```

## 🔗 RESTful API インターフェース仕様

### API基本情報
```yaml
# OpenAPI 3.0 基本情報
openapi: 3.0.0
info:
  title: Design Integration Tools API
  description: 設計統合ツール RESTful API
  version: 1.0.0
  contact:
    name: Development Team
    email: dev@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: http://localhost:8080/api/v1
    description: Development server
  - url: https://design-tools.example.com/api/v1
    description: Production server

# セキュリティ設定
security:
  - BearerAuth: []
  - ApiKeyAuth: []

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
```

### 共通レスポンス形式
```json
// 成功レスポンス
{
  "success": true,
  "data": {
    // 実際のデータ
  },
  "meta": {
    "timestamp": "2025-06-27T06:30:00Z",
    "request_id": "req_123456789",
    "version": "1.0.0"
  }
}

// エラーレスポンス
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "入力値に誤りがあります",
    "details": [
      {
        "field": "table_name",
        "message": "テーブル名は必須です",
        "code": "REQUIRED_FIELD"
      }
    ]
  },
  "meta": {
    "timestamp": "2025-06-27T06:30:00Z",
    "request_id": "req_123456789",
    "version": "1.0.0"
  }
}

// ページネーション付きレスポンス
{
  "success": true,
  "data": {
    "items": [
      // データ配列
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100,
      "total_pages": 5,
      "has_next": true,
      "has_prev": false
    }
  },
  "meta": {
    "timestamp": "2025-06-27T06:30:00Z",
    "request_id": "req_123456789",
    "version": "1.0.0"
  }
}
```

### データベース管理API

#### テーブル一覧取得
```http
GET /api/v1/database/tables
```

**クエリパラメータ:**
```yaml
parameters:
  - name: page
    in: query
    schema:
      type: integer
      default: 1
    description: ページ番号
  - name: limit
    in: query
    schema:
      type: integer
      default: 20
      maximum: 100
    description: 1ページあたりの件数
  - name: category
    in: query
    schema:
      type: string
      enum: [マスタ系, トランザクション系, 履歴系, システム系]
    description: テーブルカテゴリフィルタ
  - name: status
    in: query
    schema:
      type: string
      enum: [valid, warning, error]
    description: 検証ステータスフィルタ
  - name: search
    in: query
    schema:
      type: string
    description: テーブル名検索
  - name: sort
    in: query
    schema:
      type: string
      enum: [name, category, updated_at, status]
      default: name
    description: ソートフィールド
  - name: order
    in: query
    schema:
      type: string
      enum: [asc, desc]
      default: asc
    description: ソート順
```

**レスポンス例:**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "table_name": "MST_Employee",
        "logical_name": "社員マスタ",
        "category": "マスタ系",
        "priority": "最高",
        "column_count": 12,
        "status": "valid",
        "last_validated": "2025-06-27T06:30:00Z",
        "created_at": "2025-06-01T00:00:00Z",
        "updated_at": "2025-06-27T06:30:00Z",
        "requirement_id": "USR.1-BASE.1"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 42,
      "total_pages": 3,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

#### テーブル詳細取得
```http
GET /api/v1/database/tables/{table_name}
```

**パスパラメータ:**
- `table_name`: テーブル名（例: MST_Employee）

**レスポンス例:**
```json
{
  "success": true,
  "data": {
    "table_name": "MST_Employee",
    "logical_name": "社員マスタ",
    "category": "マスタ系",
    "priority": "最高",
    "requirement_id": "USR.1-BASE.1",
    "comment": "社員の基本情報を管理するマスタテーブル",
    "revision_history": [
      {
        "version": "1.0.0",
        "date": "2025-06-01",
        "author": "開発チーム",
        "changes": "初版作成"
      }
    ],
    "overview": "このテーブルは社員の基本情報を管理し...",
    "columns": [
      {
        "name": "emp_id",
        "type": "SERIAL",
        "nullable": false,
        "primary_key": true,
        "comment": "社員ID（自動採番）",
        "requirement_id": "USR.1-BASE.1"
      }
    ],
    "indexes": [
      {
        "name": "idx_employee_emp_no",
        "columns": ["emp_no"],
        "unique": true,
        "comment": "社員番号の一意制約"
      }
    ],
    "foreign_keys": [
      {
        "name": "fk_employee_department",
        "columns": ["dept_id"],
        "references": {
          "table": "MST_Department",
          "columns": ["dept_id"]
        },
        "on_update": "CASCADE",
        "on_delete": "RESTRICT"
      }
    ],
    "notes": [
      "社員情報の変更は人事部門の承認が必要",
      "退職者の情報は論理削除で管理",
      "個人情報のため暗号化して保存"
    ],
    "rules": [
      "社員番号は入社年度+連番の形式",
      "メールアドレスは会社ドメインのみ許可",
      "パスワードは定期的な変更を強制"
    ]
  }
}
```

#### YAML検証
```http
POST /api/v1/database/validate
```

**リクエストボディ:**
```json
{
  "files": ["MST_Employee", "MST_Department"],  // 空の場合は全ファイル
  "options": {
    "strict": true,                              // 厳密モード
    "fix": false,                               // 自動修復
    "schema": "custom_schema.yaml"              // カスタムスキーマ
  }
}
```

**レスポンス例:**
```json
{
  "success": true,
  "data": {
    "summary": {
      "total": 42,
      "valid": 40,
      "warnings": 2,
      "errors": 0,
      "duration": "2.5s"
    },
    "results": [
      {
        "file": "MST_Employee",
        "status": "valid",
        "messages": []
      },
      {
        "file": "MST_Department",
        "status": "warning",
        "messages": [
          {
            "type": "warning",
            "code": "SHORT_OVERVIEW",
            "message": "overview セクションが短すぎます (25文字 < 50文字)",
            "line": 15,
            "column": 1
          }
        ]
      }
    ]
  }
}
```

#### DDL生成
```http
POST /api/v1/database/generate
```

**リクエストボディ:**
```json
{
  "tables": ["MST_Employee", "MST_Department"],  // 空の場合は全テーブル
  "options": {
    "database_type": "postgresql",               // データベース種別
    "output_dir": "docs/design/database/ddl",   // 出力ディレクトリ
    "include_indexes": true,                     // インデックス含める
    "include_constraints": true,                 // 制約含める
    "template": "custom_template.sql"            // カスタムテンプレート
  }
}
```

**レスポンス例:**
```json
{
  "success": true,
  "data": {
    "summary": {
      "total": 2,
      "generated": 2,
      "failed": 0,
      "duration": "1.2s"
    },
    "files": [
      {
        "table": "MST_Employee",
        "file_path": "docs/design/database/ddl/MST_Employee.sql",
        "size": 2048,
        "status": "generated"
      },
      {
        "table": "MST_Department",
        "file_path": "docs/design/database/ddl/MST_Department.sql",
        "size": 1024,
        "status": "generated"
      }
    ]
  }
}
```

### API管理API

#### エンドポイント一覧取得
```http
GET /api/v1/api/endpoints
```

**クエリパラメータ:**
```yaml
parameters:
  - name: method
    in: query
    schema:
      type: string
      enum: [GET, POST, PUT, DELETE, PATCH]
    description: HTTPメソッドフィルタ
  - name: path_pattern
    in: query
    schema:
      type: string
    description: パスパターンフィルタ（正規表現）
  - name: tag
    in: query
    schema:
      type: string
    description: タグフィルタ
  - name: status
    in: query
    schema:
      type: string
      enum: [valid, warning, error]
    description: 検証ステータスフィルタ
```

**レスポンス例:**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "endpoint_id": "API-011",
        "method": "GET",
        "path": "/api/v1/users/{id}",
        "summary": "ユーザー情報取得",
        "description": "指定されたIDのユーザー情報を取得します",
        "tags": ["users", "profile"],
        "status": "valid",
        "last_validated": "2025-06-27T06:30:00Z",
        "requirement_id": "PRO.1-BASE.1"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 28,
      "total_pages": 2,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

#### API仕様検証
```http
POST /api/v1/api/validate
```

**リクエストボディ:**
```json
{
  "files": ["API-011", "API-012"],              // 空の場合は全ファイル
  "options": {
    "openapi_version": "3.0.0",                 // OpenAPIバージョン
    "strict": true,                             // 厳密モード
    "check_examples": true,                     // サンプルデータ検証
    "check_schemas": true                       // スキーマ検証
  }
}
```

### 画面管理API

#### コンポーネント一覧取得
```http
GET /api/v1/screen/components
```

**レスポンス例:**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "component_id": "SCR-LOGIN",
        "name": "LoginForm",
        "type": "form",
        "category": "authentication",
        "status": "valid",
        "accessibility_score": 95,
        "responsive": true,
        "last_updated": "2025-06-27T06:30:00Z",
        "requirement_id": "PLT.1-WEB.1"
      }
    ]
  }
}
```

### 統合チェックAPI

#### 統合整合性チェック
```http
POST /api/v1/integration/check
```

**リクエストボディ:**
```json
{
  "scope": "all",                               // チェック範囲
  "options": {
    "fix": false,                               // 自動修復
    "parallel": true,                           // 並列実行
    "check_cross_references": true,             // 相互参照チェック
    "check_naming_consistency": true,           // 命名一貫性チェック
    "check_data_flow": true                     // データフロー整合性
  }
}
```

**レスポンス例:**
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_checks": 150,
      "passed": 145,
      "warnings": 3,
      "errors": 2,
      "duration": "5.2s"
    },
    "results": {
      "database_api_consistency": {
        "status": "warning",
        "issues": [
          {
            "type": "missing_api_endpoint",
            "message": "テーブル MST_Employee に対応するAPI エンドポイントが見つかりません",
            "table": "MST_Employee",
            "suggested_endpoint": "GET /api/v1/employees"
          }
        ]
      },
      "api_screen_consistency": {
        "status": "passed",
        "issues": []
      },
      "naming_consistency": {
        "status": "error",
        "issues": [
          {
            "type": "inconsistent_naming",
            "message": "命名規則が一致しません",
            "database": "emp_id",
            "api": "employeeId",
            "screen": "employee_id"
          }
        ]
      }
    }
  }
}
```

## 🔌 プラグインAPI仕様

### プラグインインターフェース
```python
# プラグインベースクラス
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BasePlugin(ABC):
    """プラグインベースクラス"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """プラグイン名"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """プラグインバージョン"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """プラグイン説明"""
        pass
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """プラグイン初期化"""
        pass
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """プラグイン実行"""
        pass
    
    def cleanup(self) -> None:
        """プラグインクリーンアップ（オプション）"""
        pass

# バリデータープラグイン例
class CustomValidatorPlugin(BasePlugin):
    """カスタムバリデータープラグイン"""
    
    @property
    def name(self) -> str:
        return "custom_validator"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "カスタムバリデーションルールを提供"
    
    def initialize(self, config: Dict[str, Any]) -> None:
        self.rules = config.get('validation_rules', [])
        self.strict_mode = config.get('strict_mode', False)
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """バリデーション実行"""
        data = context.get('data', {})
        results = []
        
        for rule in self.rules:
            result = self._validate_rule(data, rule)
            results.append(result)
        
        return {
            'success': all(r['valid'] for r in results),
            'results': results
        }
    
    def _validate_rule(self, data: Dict[str, Any], rule: Dict[str, Any]) -> Dict[str, Any]:
        """個別ルール検証"""
        # カスタムバリデーションロジック
        pass

# ジェネレータープラグイン例
class CustomGeneratorPlugin(BasePlugin):
    """カスタムジェネレータープラグイン"""
    
    @property
    def name(self) -> str:
        return "custom_generator"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "カスタム形式でファイル生成"
    
    def initialize(self, config: Dict[str, Any]) -> None:
        self.template_path = config.get('template_path')
        self.output_format = config.get('output_format', 'custom')
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """生成実行"""
        data = context.get('data', {})
        template = self._load_template()
        
        generated_content = self._generate_content(data, template)
        
        return {
            'success': True,
            'content': generated_content,
            'format': self.output_format
        }
```

### プラグイン登録・管理API
```http
# プラグイン一覧取得
GET /api/v1/plugins

# プラグイン詳細取得
GET /api/v1/plugins/{plugin_name}

# プラグイン有効化
POST /api/v1/plugins/{plugin_name}/enable

# プラグイン無効化
POST /api/v1/plugins/{plugin_name}/disable

# プラグイン設定更新
PUT /api/v1/plugins/{plugin_name}/config
```

### プラグイン設定例
```yaml
# プラグイン設定ファイル
plugins:
  custom_validator:
    enabled: true
    config:
      validation_rules:
        - name: "table_name_format"
          pattern: "^[A-Z]{3}_[A-Za-z]+$"
          message: "テーブル名は 'MST_TableName' 形式で入力してください"
        - name: "column_comment_required"
          required: true
          message: "全カラムにコメントが必要です"
      strict_mode: true
  
  custom_generator:
    enabled: true
    config:
      template_path: "templates/custom_ddl.sql.j2"
      output_format: "custom_sql"
      include_metadata: true
```

## 🔐 認証・認可システム

### JWT認証
```http
# ログイン
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "password"
}

# レスポンス
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 3600,
    "token_type": "Bearer"
  }
}

# API呼び出し時のヘッダー
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### APIキー認証
```http
# APIキー生成
POST /api/v1/auth/api-keys
Authorization: Bearer <jwt_token>

{
  "name": "Integration Tool",
  "permissions": ["database:read", "database:write", "api:read"],
  "expires_at": "2025-12-31T23:59:59Z"
}

# API呼び出し時のヘッダー
X-API-Key: sk_live_1234567890abcdef...
```

### 権限システム
```yaml
# 権限定義
permissions:
  database:
    - read          # データベース情報読み取り
    - write         # データベース情報更新
    - validate      # 検証実行
    - generate      # DDL生成
  
  api:
    - read          # API情報読み取り
    - write         # API情報更新
    - validate      # API検証
    - generate      # OpenAPI生成
  
  screen:
    - read          # 画面情報読み取り
    - write         # 画面情報更新
    - validate      # 画面検証
    - generate      # HTML生成
  
  integration:
    - check         # 整合性チェック
    - fix           # 自動修復
    - report        # レポート生成
  
  admin:
    - user_manage   # ユーザー管理
    - plugin_manage # プラグイン管理
    - system_config # システム設定

# ロール定義
roles:
  viewer:
    permissions:
      - database:read
      - api:read
      - screen:read
  
  editor:
    permissions:
      - database:read
      - database:write
      - database:validate
      - api:read
      - api:write
      - api:validate
      - screen:read
      - screen:write
      - screen:validate
  
  developer:
    permissions:
      - database:*
      - api:*
      - screen:*
      - integration:check
      - integration:report
  
  admin:
    permissions:
      - "*"
```

## 📊 エラーコード体系

### エラーコード分類
```python
ERROR_CODES = {
    # 認証・認可エラー (1000-1099)
    1000: "AUTHENTICATION_REQUIRED",
    1001: "INVALID_CREDENTIALS",
    1002: "TOKEN_EXPIRED",
    1003: "INSUFFICIENT_PERMISSIONS",
    1004: "API_KEY_INVALID",
    
    # 入力検証エラー (1100-1199)
    1100: "VALIDATION_ERROR",
    1101: "REQUIRED_FIELD_MISSING",
    1102: "INVALID_FORMAT",
    1103: "VALUE_OUT_OF_RANGE",
    1104: "INVALID_ENUM_VALUE",
    
    # リソースエラー (1200-1299)
    1200: "RESOURCE_NOT_FOUND",
    1201: "RESOURCE_ALREADY_EXISTS",
    1202: "RESOURCE_LOCKED",
    1203: "RESOURCE_DELETED",
    
    # システムエラー (1300-1399)
    1300: "INTERNAL_SERVER_ERROR",
    1301: "DATABASE_CONNECTION_ERROR",
    1302: "FILE_SYSTEM_ERROR",
    1303: "EXTERNAL_SERVICE_ERROR",
    
    # 業務ロジックエラー (1400-1499)
    1400: "BUSINESS_RULE_VIOLATION",
    1401: "CONSISTENCY_CHECK_FAILED",
    1402: "GENERATION_FAILED",
    1403: "PLUGIN_EXECUTION_ERROR",
}
```

### 多言語エラーメッセージ
```json
{
  "ja": {
    "1000": "認証が必要です",
    "1001": "ユーザー名またはパスワードが正しくありません",
    "1002": "トークンの有効期限が切れています",
    "1003": "この操作を実行する権限がありません",
    "1100": "入力値に誤りがあります",
    "1200": "指定されたリソースが見つかりません",
    "1300": "システムエラーが発生しました"
  },
  "en": {
    "1000": "Authentication required",
    "1001": "Invalid username or password",
    "1002": "Token has expired",
    "1003": "Insufficient permissions for this operation",
    "1100": "Validation error in input data",
    "1200": "Specified resource not found",
    "1300": "Internal server error occurred"
  }
}
```

## 📈 レート制限・クォータ

### レート制限設定
```yaml
rate_limits:
  # 認証済みユーザー
  authenticated:
    requests_per_minute: 1000
    requests_per_hour: 10000
    requests_per_day: 100000
  
  # APIキー認証
  api_key:
    requests_per_minute: 2000
    requests_per_hour: 20000
    requests_per_day: 200000
  
  # 未認証ユーザー
  anonymous:
    requests_per_minute: 100
    requests_per_hour: 1000
    requests_per_day: 5000

# エンドポイント別制限
endpoint_limits:
  "/api/v1/database/validate":
    requests_per_minute: 10
    concurrent_requests: 2
  
  "/api/v1/database/generate":
    requests_per_minute: 5
    concurrent_requests: 1
  
  "/api/v1/integration/check":
    requests_per_minute: 3
    concurrent_requests: 1
```

### レート制限ヘッダー
```http
# レスポンスヘッダー
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
X-RateLimit-Retry-After: 60

# 制限超過時のレスポンス
HTTP/1.1 429 Too Many Requests
Content-Type: application/json

{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "リクエスト制限を超過しました",
    "retry_after": 60
  }
}
```

---

この包括的なインターフェース仕様により、一貫性のあるユーザーエクスペリエンスと開発者エクスペリエンスを提供し、設計統合ツールの効果的な活用を実現します。
