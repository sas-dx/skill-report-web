# データベース設計ガイドライン

## エグゼクティブサマリー

この文書はデータベース設計における基本原則と実装ガイドラインを定義します。現実的なシングルテナント設計から将来のマルチテナント化への移行戦略、YAMLフォーマット統一、品質保証プロセス、自動化ツール活用を提供し、効率的で保守性の高いデータベースシステムの構築を支援します。技術スタック非依存の基本原則は00-core-rules.mdを参照し、このファイルではPostgreSQL + Prisma固有の実装パターンと品質管理手法に焦点を当てています。

## 基本設計原則

### 1. 現実的な実装方針（2025年6月時点）
- **現在の実装**: シングルテナント設計で開発中
- **設計書**: マルチテナント対応として設計済み
- **段階的移行**: 現在のシングルテナント実装を完成させ、将来的にマルチテナント化を検討
- **実用性重視**: 7週間での完成を重視した実用的な設計
- **AI駆動開発**: 効率的な開発プロセスを重視

### 2. テーブル命名規則
- **MST_**: マスタ系テーブル（社員、部署、スキル階層等）
- **TRN_**: トランザクション系テーブル（スキル情報、目標進捗、案件実績等）
- **HIS_**: 履歴系テーブル（監査ログ、操作履歴等）
- **SYS_**: システム系テーブル（検索インデックス、システムログ等）
- **WRK_**: ワーク系テーブル（一括登録ジョブログ、バッチワーク等）

### 3. パフォーマンス要件
- **API〜UI**: 1秒以内のレスポンス時間
- **データベースアクセス**: 効率的なインデックス設計
- **同時接続**: 100ユーザー同時利用対応
- **データ量**: 1000ユーザー×5年分のデータ処理

### 4. 品質保証方針
- **整合性チェック**: 自動化ツールによる定期チェック
- **設計書準拠**: YAMLファイルと実装の整合性保証
- **AI活用**: 効率的な開発とドキュメント生成
- **段階的改善**: 継続的な品質向上

## YAMLフォーマット統一

### 統一フォーマット（MST_TEMPLATE_details.yamlベース）

**重要**: 全てのテーブル定義は `docs/design/database/table-details/MST_TEMPLATE_details.yaml` をベースとして作成してください。

#### 実際のテーブル定義ファイル構造（MST_Employee_details.yaml準拠）

**注意**: 現在のMST_Employee_details.yamlは簡素化された形式ですが、品質管理・監査要件のため、以下の必須セクションを含む完全な形式を使用してください。

```yaml
# MST_Employee テーブル詳細定義
table_name: "MST_Employee"
logical_name: "社員基本情報"
category: "マスタ系"
priority: "最高"
requirement_id: "PRO.1-BASE.1"
comment: "組織に所属する全社員の基本的な個人情報と組織情報を一元管理するマスタテーブル"

# 改版履歴（必須）
revision_history:
  - version: "1.0.0"
    date: "2025-06-01"
    author: "開発チーム"
    changes: "初版作成 - MST_Employeeテーブルの詳細定義"
  - version: "1.1.0"
    date: "2025-06-12"
    author: "開発チーム"
    changes: "カラム追加 - manager_id, job_type_idを追加"

# テーブル概要・目的（必須）
overview: |
  組織に所属する全社員の基本的な個人情報と組織情報を一元管理するマスタテーブル。
  
  主な目的：
  - 社員の基本情報（氏名、連絡先、入社日等）の管理
  - 組織構造（部署、役職、上司関係）の管理
  - 認証・権限管理のためのユーザー情報提供
  - 人事システムとの連携データ基盤
  
  このテーブルは年間スキル報告書システムの中核となるマスタデータであり、
  スキル管理、目標管理、作業実績管理の全ての機能で参照される。

# カラム定義
columns:
  - name: "id"
    type: "VARCHAR(50)"
    nullable: false
    primary_key: true
    comment: "プライマリキー（UUID）"
    requirement_id: "PLT.1-WEB.1"
  
  - name: "employee_code"
    type: "VARCHAR(30)"
    nullable: false
    unique: true
    comment: "社員番号（例：EMP000001）"
    requirement_id: "PRO.1-BASE.1"
    
  - name: "full_name"
    type: "VARCHAR(100)"
    nullable: false
    comment: "氏名（暗号化対象）"
    requirement_id: "PRO.1-BASE.1"
    
  - name: "full_name_kana"
    type: "VARCHAR(100)"
    nullable: false
    comment: "氏名カナ（暗号化対象）"
    requirement_id: "PRO.1-BASE.1"
    
  - name: "email"
    type: "VARCHAR(255)"
    nullable: false
    unique: true
    comment: "メールアドレス（ログイン認証用）"
    requirement_id: "ACC.1-AUTH.1"
    
  - name: "phone"
    type: "VARCHAR(20)"
    nullable: true
    comment: "電話番号（暗号化対象）"
    requirement_id: "PRO.1-BASE.1"
    
  - name: "hire_date"
    type: "DATE"
    nullable: false
    comment: "入社日"
    requirement_id: "PRO.1-BASE.1"
    
  - name: "birth_date"
    type: "DATE"
    nullable: true
    comment: "生年月日（暗号化対象）"
    requirement_id: "PRO.1-BASE.1"
    
  - name: "gender"
    type: "VARCHAR(1)"
    nullable: true
    comment: "性別（M:男性、F:女性、O:その他）"
    requirement_id: "PRO.1-BASE.1"
    
  - name: "department_id"
    type: "VARCHAR(50)"
    nullable: false
    comment: "所属部署ID"
    requirement_id: "PRO.1-BASE.1"
    
  - name: "position_id"
    type: "VARCHAR(50)"
    nullable: true
    comment: "役職ID"
    requirement_id: "PRO.1-BASE.1"
    
  - name: "job_type_id"
    type: "VARCHAR(50)"
    nullable: true
    comment: "職種ID"
    requirement_id: "PRO.1-BASE.1"
    
  - name: "employment_status"
    type: "VARCHAR(20)"
    nullable: false
    default: "FULL_TIME"
    comment: "雇用形態（FULL_TIME:正社員、PART_TIME:パート、CONTRACT:契約社員）"
    requirement_id: "PRO.1-BASE.1"
    
  - name: "manager_id"
    type: "VARCHAR(50)"
    nullable: true
    comment: "直属の上司ID（自己参照）"
    requirement_id: "PRO.1-BASE.1"
    
  - name: "employee_status"
    type: "VARCHAR(20)"
    nullable: false
    default: "ACTIVE"
    comment: "在籍状況（ACTIVE:在籍、RETIRED:退職、SUSPENDED:休職）"
    requirement_id: "PRO.1-BASE.1"
    
  - name: "created_at"
    type: "TIMESTAMP"
    nullable: false
    default: "CURRENT_TIMESTAMP"
    comment: "作成日時"
    requirement_id: "PLT.1-WEB.1"
    
  - name: "updated_at"
    type: "TIMESTAMP"
    nullable: false
    default: "CURRENT_TIMESTAMP"
    comment: "更新日時"
    requirement_id: "PLT.1-WEB.1"
    
  - name: "is_deleted"
    type: "BOOLEAN"
    nullable: false
    default: false
    comment: "論理削除フラグ"
    requirement_id: "PLT.1-WEB.1"

# インデックス定義
indexes:
  - name: "idx_employee_code"
    columns: ["employee_code"]
    unique: true
    comment: "社員番号検索用（一意）"
    
  - name: "idx_email"
    columns: ["email"]
    unique: true
    comment: "メールアドレス検索用（一意）"
    
  - name: "idx_department"
    columns: ["department_id"]
    unique: false
    comment: "部署別検索用"
    
  - name: "idx_manager"
    columns: ["manager_id"]
    unique: false
    comment: "上司別検索用"
    
  - name: "idx_status"
    columns: ["employee_status"]
    unique: false
    comment: "在籍状況別検索用"
    
  - name: "idx_hire_date"
    columns: ["hire_date"]
    unique: false
    comment: "入社日検索用"

# 外部キー定義
foreign_keys:
  - name: "fk_employee_department"
    columns: ["department_id"]
    references:
      table: "MST_Department"
      columns: ["id"]
    on_update: "CASCADE"
    on_delete: "RESTRICT"
    
  - name: "fk_employee_position"
    columns: ["position_id"]
    references:
      table: "MST_Position"
      columns: ["id"]
    on_update: "CASCADE"
    on_delete: "SET NULL"
    
  - name: "fk_employee_job_type"
    columns: ["job_type_id"]
    references:
      table: "MST_JobType"
      columns: ["id"]
    on_update: "CASCADE"
    on_delete: "SET NULL"
    
  - name: "fk_employee_manager"
    columns: ["manager_id"]
    references:
      table: "MST_Employee"
      columns: ["id"]
    on_update: "CASCADE"
    on_delete: "SET NULL"

# 特記事項（必須）
notes:
  - "個人情報（氏名、氏名カナ、電話番号、生年月日）は暗号化対象"
  - "論理削除は is_deleted フラグで管理"
  - "manager_idによる自己参照で組織階層を表現"
  - "人事システムとの連携でマスタデータを同期"
  - "認証・権限管理システムの基盤テーブル"
  - "スキル管理・目標管理・作業実績管理の全機能で参照される"

# 業務ルール（必須）
business_rules:
  - "社員番号（employee_code）は一意で変更不可"
  - "メールアドレス（email）は認証用のため一意制約必須"
  - "在籍状況（employee_status）がRETIREDの場合、論理削除フラグをtrueに設定"
  - "直属の上司（manager_id）は同一部署内の上位役職者のみ設定可能"
  - "雇用形態（employment_status）に応じた権限・機能制限を適用"
  - "個人情報の暗号化は法的要件に基づく必須対応"
  - "監査証跡として作成日時・更新日時は自動設定"

# サンプルデータ（推奨）
sample_data:
  - id: "emp_001"
    employee_code: "EMP000001"
    full_name: "山田太郎"
    full_name_kana: "ヤマダタロウ"
    email: "yamada.taro@example.com"
    phone: "090-1234-5678"
    hire_date: "2020-04-01"
    birth_date: "1990-01-15"
    gender: "M"
    department_id: "dept_001"
    position_id: "pos_003"
    job_type_id: "job_001"
    employment_status: "FULL_TIME"
    manager_id: "emp_002"
    employee_status: "ACTIVE"
    is_deleted: false
    
  - id: "emp_002"
    employee_code: "EMP000002"
    full_name: "佐藤花子"
    full_name_kana: "サトウハナコ"
    email: "sato.hanako@example.com"
    phone: "090-2345-6789"
    hire_date: "2018-04-01"
    birth_date: "1985-03-20"
    gender: "F"
    department_id: "dept_001"
    position_id: "pos_002"
    job_type_id: "job_001"
    employment_status: "FULL_TIME"
    manager_id: null
    employee_status: "ACTIVE"
    is_deleted: false
```

#### カラム定義の各属性説明

| 属性 | 説明 | 必須 | 例 |
|------|------|------|------|
| name | 物理カラム名 | ✅ | "employee_code" |
| type | データ型（PostgreSQL準拠、長さ含む） | ✅ | "VARCHAR(50)", "INTEGER", "TIMESTAMP" |
| nullable | NULL許可フラグ | ✅ | true/false |
| primary_key | 主キーフラグ | ❌ | true/false |
| unique | 一意制約フラグ | ❌ | true/false |
| default | デフォルト値 | ❌ | "CURRENT_TIMESTAMP", "0", "'ACTIVE'" |
| comment | カラム説明 | ✅ | "社員番号（例：EMP000001）" |
| requirement_id | 要求仕様ID | ✅ | "PRO.1-BASE.1" |

#### 要求仕様IDの設定

各カラムには必ず対応する要求仕様IDを設定してください。要求仕様IDは以下の形式に従います：

- **カテゴリ.シリーズ-機能**: 例 "PRO.1-BASE.1"
- **カテゴリ一覧**:
  - PLT: Platform (システム基盤要件)
  - ACC: Access Control (ユーザー権限管理)
  - PRO: Profile (個人プロフィール管理)
  - SKL: Skill (スキル情報管理)
  - CAR: Career (目標・キャリア管理)
  - WPM: Work Performance Mgmt (作業実績管理)
  - TRN: Training (研修・セミナー管理)
  - RPT: Report (レポート出力)

要求仕様IDが不明な場合は、関連する機能の要求仕様IDを調査するか、新規IDの発行を検討してください。

#### テンプレートファイルとの違い

**MST_TEMPLATE_details.yaml**は詳細なテンプレートファイルであり、実際の実装でも以下の項目を含む完全な形式を使用する必要があります：

## 🚨 **絶対必須セクション - 省略禁止** 🚨

以下の4つのセクションは品質管理・監査・運用保守の観点から**いかなる場合も省略禁止**です。これらのセクションが欠けているテーブル定義は、自動検証ツールによって拒否され、コミットできません：

| セクション | 目的 | 省略時のリスク | 最低要件 | 重要度 |
|------------|------|----------------|----------|---------|
| `revision_history` | 変更履歴の追跡・監査証跡 | 監査不能、変更管理の崩壊 | 最低1エントリ必須 | 🔴 **必須** |
| `overview` | テーブルの目的・設計意図の明確化 | 設計意図の喪失、誤用 | 最低50文字以上 | 🔴 **必須** |
| `notes` | 運用・保守に必要な特記事項 | 運用障害、保守困難化 | 最低3項目以上 | 🔴 **必須** |
| `business_rules` | 業務ルール・制約の明文化 | 要件逸脱、整合性喪失 | 最低3項目以上 | 🔴 **必須** |

### ⚠️ **重要な警告** ⚠️
- これらのセクションを省略したテーブル定義は**品質基準を満たさない**と判定されます
- 自動検証ツールによって**コミットが拒否**されます
- 運用・保守時に**重大な問題**を引き起こす可能性があります
- **例外は一切認められません** - 全てのテーブル定義で必須です

**必須セクションの検証方法**:
```bash
# 全テーブル検証
python docs/design/database/tools/yaml_validator/validate_yaml_format.py --all --verbose

# 特定テーブル検証
python docs/design/database/tools/yaml_validator/validate_yaml_format.py --table MST_Employee --verbose
```

詳細なガイドラインは `docs/design/database/tools/yaml_validator/README_REQUIRED_SECTIONS.md` を参照してください。

**必須セクション（省略不可）**：
- `table_name`、`logical_name`、`category`：基本情報
- 🔴 **`revision_history`**：変更履歴の追跡（品質管理・監査要件）**※絶対省略禁止**
- 🔴 **`overview`**：テーブルの目的と概要（設計意図の明確化）**※絶対省略禁止**
- `columns`：業務固有カラム定義
- `business_indexes`/`indexes`：検索最適化
- `business_constraints`/制約：データ整合性保証
- `foreign_keys`：テーブル間関係定義
- 🔴 **`notes`**：特記事項・考慮点（運用・保守要件）**※絶対省略禁止**
- 🔴 **`business_rules`**：業務ルール・制約（要件トレーサビリティ）**※絶対省略禁止**

### 🚨 必須セクション詳細ガイドライン

必須セクションの詳細なガイドラインは `docs/design/database/tools/yaml_validator/README_REQUIRED_SECTIONS.md` に移動しました。このドキュメントには、各必須セクションの目的、必須要素、記述スタイル、例などが詳細に記載されています。

以下は各必須セクションの概要です：

#### 🔴 revision_history（改版履歴）- 【絶対省略禁止】
- **目的**: 変更管理・監査の基盤となる重要情報
- **内容**: バージョン番号、日付、変更者、変更内容を記録
- **運用**: テーブル定義変更時に必ず更新（最新の変更を先頭に追加）
- **最低要件**: 最低1エントリ必須
- **省略時のリスク**: 監査証跡の欠如、変更管理の破綻、コンプライアンス違反

#### 🔴 overview（概要・目的）- 【絶対省略禁止】
- **目的**: テーブルの存在理由と使用方法を明確にする基本情報
- **内容**: 主な目的、関連する業務プロセス、他テーブルとの関係を説明
- **記述方法**: 箇条書きと説明文の組み合わせで記述
- **最低要件**: 最低50文字以上必須
- **省略時のリスク**: 設計意図の喪失、テーブル誤用、保守困難化

#### 🔴 notes（特記事項）- 【絶対省略禁止】
- **目的**: 運用・保守・セキュリティに関わる重要な補足情報
- **内容**: 暗号化要件、論理削除方針、特殊な制約条件を記録
- **記述方法**: 箇条書きで簡潔に記述
- **最低要件**: 最低3項目以上必須
- **省略時のリスク**: 運用障害、セキュリティ問題、保守困難化

#### 🔴 business_rules（業務ルール）- 【絶対省略禁止】
- **目的**: データの整合性と業務要件を保証するための制約条件
- **内容**: 一意性制約、参照整合性、業務固有の制約条件を明文化
- **記述方法**: 箇条書きで明確に記述
- **最低要件**: 最低3項目以上必須
- **省略時のリスク**: 要件逸脱、データ整合性喪失、業務ルール違反

**必須セクションの自動検証**:
```bash
# Git コミット前に自動検証を有効化
cd docs/design/database/tools/yaml_validator
./install_git_hook.sh
```

**推奨セクション**：
- `sample_data`：テスト・検証用データ

**実装での簡素化項目**：
- `logical`属性は使用せず、`comment`で説明
- `length`属性は使用せず、`type`に含める（例：`VARCHAR(50)`）
- `encrypted`属性は使用せず、`comment`で明記

#### テンプレートファイルの主要セクション

**必須セクション（省略不可）**：
- **table_name**: 物理テーブル名
- **logical_name**: 論理テーブル名（日本語）
- **category**: テーブル分類（マスタ系/トランザクション系）
- **revision_history**: 改版履歴管理（品質管理・監査要件）
- **overview**: テーブルの概要と目的（設計意図の明確化）
- **columns**: 業務固有カラム定義（詳細な型・制約情報）
- **business_indexes**: 業務固有インデックス定義（検索最適化）
- **business_constraints**: 業務固有制約定義（データ整合性保証）
- **foreign_keys**: 外部キー関係定義（テーブル間関係）
- **notes**: 特記事項（運用・保守要件）
- **business_rules**: 業務ルール（要件トレーサビリティ）

**推奨セクション**：
- **sample_data**: サンプルデータ（テスト・検証用）

## 簡素化された開発フロー

### 新規テーブル追加（簡素版）
```bash
# 1. テンプレートファイルをコピー（必須）
cp docs/design/database/table-details/MST_TEMPLATE_details.yaml \
   docs/design/database/table-details/NEW_TABLE_details.yaml

# 2. YAML内容を編集（必須セクション確認）
# - table_name: "NEW_TABLE"
# - logical_name: "新規テーブル論理名"
# - category: "マスタ系" または "トランザクション系"
# - 🔴 revision_history: 改版履歴（絶対省略禁止・最低1エントリ）
# - 🔴 overview: テーブルの概要と目的（絶対省略禁止・最低50文字）
# - columns: 業務固有カラム定義
# - business_indexes: 必要なインデックス
# - foreign_keys: 外部キー関係
# - 🔴 notes: 特記事項・考慮点（絶対省略禁止・最低3項目）
# - 🔴 business_rules: 業務ルール・制約（絶対省略禁止・最低3項目）
# - sample_data: サンプルデータ（推奨）

# 2.5 必須セクション検証
python docs/design/database/tools/yaml_validator/validate_yaml_format.py --table NEW_TABLE --verbose

# 3. テーブル一覧.mdに追加
# 新規テーブルをテーブル一覧に追加

# 4. 自動生成実行
cd docs/design/database/tools
python3 -m table_generator --table NEW_TABLE --verbose

# 5. 整合性チェック
python3 database_consistency_checker/run_check.py --tables NEW_TABLE

# 6. Git コミット
git add .
git commit -m "✨ feat: NEW_TABLEテーブル追加

要求仕様ID: XXX.X-XXX.X
- MST_TEMPLATE_details.yamlベースで作成
- 業務固有カラム・インデックス・制約を定義
- 自動生成ツールで定義書・DDL・サンプルデータ生成
- 整合性チェック通過確認"
```

### 既存テーブル修正（簡素版）
```bash
# 1. 影響範囲調査
# 修正対象テーブルの参照関係・依存関係を確認

# 2. YAML詳細定義修正（必須セクション確認）
# table-details/{テーブル名}_details.yamlを更新
# - 🔴 revision_history: 改版履歴を更新（絶対省略禁止・変更内容記録）
# - 🔴 overview: 変更に伴う概要更新（必要に応じて・設計意図明確化）
# - columns: カラム追加・修正・削除
# - business_indexes: インデックス追加・修正
# - foreign_keys: 外部キー関係の変更
# - 🔴 notes: 特記事項・考慮点の更新（絶対省略禁止・運用影響確認）
# - 🔴 business_rules: 業務ルール・制約の更新（絶対省略禁止・制約変更確認）

# 2.5 必須セクション検証
python docs/design/database/tools/yaml_validator/validate_yaml_format.py --table MODIFIED_TABLE --verbose

# 3. 該当テーブルのみ再生成
cd docs/design/database/tools
python3 -m table_generator --table MODIFIED_TABLE --verbose

# 4. 整合性チェック
python3 database_consistency_checker/run_check.py --tables MODIFIED_TABLE

# 5. 関連テーブルの整合性確認（必要に応じて）
python3 database_consistency_checker/run_check.py --checks foreign_key_consistency

# 6. Git コミット
git add .
git commit -m "🔧 fix: MODIFIED_TABLEテーブル修正

要求仕様ID: XXX.X-XXX.X
- カラム追加/修正: {変更内容}
- 影響範囲: {関連テーブル・機能}
- 破壊的変更: なし/あり（詳細）
- 整合性チェック通過確認"
```

## 品質保証（簡素版）

### 自動チェック項目
- **テーブル存在整合性**: YAML ↔ DDL ↔ 定義書の一致
- **カラム定義整合性**: データ型・制約の一致
- **外部キー整合性**: 参照関係の妥当性
- **命名規則チェック**: プレフィックス・命名規則の準拠
- **必須セクション確認**: 🔴 revision_history、🔴 overview、🔴 notes、🔴 business_rulesの存在と内容チェック
  ```bash
  # 必須セクション検証（全テーブル）
  python docs/design/database/tools/yaml_validator/validate_yaml_format.py --all --verbose
  
  # 特定テーブルの必須セクション検証
  python docs/design/database/tools/yaml_validator/validate_yaml_format.py --table MST_Employee --verbose
  
  # 必須セクション不備の詳細確認
  python docs/design/database/tools/yaml_validator/validate_yaml_format.py --check-required-only
  ```

### 手動レビュー項目
- **業務要件との整合性**: 機能要件との一致
- **Prisma対応**: Prisma ORM との整合性
- **パフォーマンス**: インデックス設計の妥当性
- **セキュリティ**: 暗号化・制約の適切性
- **必須セクション内容確認**: 以下のチェックリストを使用
  ```
  # 🔴 必須セクション内容チェックリスト（省略禁止）
  - [ ] 🔴 revision_history: 最新の変更が記録されているか（最低1エントリ）
  - [ ] 🔴 overview: テーブルの目的と使用コンテキストが明確か（最低50文字）
  - [ ] 🔴 notes: 運用・保守・セキュリティの考慮点が記載されているか（最低3項目）
  - [ ] 🔴 business_rules: 業務ルール・制約が明確に定義されているか（最低3項目）
  
  # ⚠️ 警告: これらのセクションが不備の場合、コミットが拒否されます
  ```

## 実践的な開発フロー

### 新規テーブル追加時の標準フロー
```bash
# 1. 要求仕様ID確認・割当
# 要求仕様書で対応するIDを確認

# 2. テンプレートベースでYAML詳細定義作成
# MST_TEMPLATE_details.yamlをコピーして作成
cp docs/design/database/table-details/MST_TEMPLATE_details.yaml \
   docs/design/database/table-details/{テーブル名}_details.yaml

# 3. テーブル一覧.md更新
# 新規テーブルをテーブル一覧に追加

# 4. 自動生成実行
cd ~/skill-report-web/docs/design/database/tools
python3 -m table_generator --table NEW_TABLE --verbose

# 5. 個別整合性チェック
python3 database_consistency_checker/run_check.py --tables NEW_TABLE

# 6. 全体整合性確認
python3 database_consistency_checker/run_check.py --verbose

# 7. 設計レビュー実施
# 業務要件・非機能要件・マルチテナント対応の確認

# 8. Git コミット
cd ~/skill-report-web
git add .
git commit -m "🆕 feat: NEW_TABLEテーブル追加

要求仕様ID: XXX.X-XXX.X
- YAML詳細定義作成
- 自動生成ツールによる定義書・DDL・サンプルデータ生成
- 整合性チェック通過確認
- Prisma スキーマとの整合性確認"
```

### 既存テーブル修正時の標準フロー
```bash
# 1. 影響範囲調査
# 修正対象テーブルの参照関係・依存関係を確認

# 2. YAML詳細定義修正
# table-details/{テーブル名}_details.yamlを更新
# ※MST_TEMPLATE_details.yamlの構造に従って修正

# 3. 該当テーブルのみ再生成
python3 -m table_generator --table MODIFIED_TABLE --verbose

# 4. 影響範囲チェック
python3 database_consistency_checker/run_check.py --checks foreign_key_consistency

# 5. 関連テーブルの整合性確認
python3 database_consistency_checker/run_check.py --tables MODIFIED_TABLE,RELATED_TABLE

# 6. 破壊的変更チェック
# 既存データ・既存機能への影響を確認

# 7. Git コミット
git add .
git commit -m "🔧 fix: MODIFIED_TABLEテーブル修正

要求仕様ID: XXX.X-XXX.X
- カラム追加/修正: {変更内容}
- 影響範囲: {関連テーブル・機能}
- 破壊的変更: なし/あり（詳細）
- 整合性チェック通過確認
- Prisma スキーマ更新確認"
```

### 一括メンテナンス作業
```bash
# 全テーブル再生成（大規模変更時）
python3 -m table_generator --verbose

# 全体整合性チェック（レポート出力）
python3 database_consistency_checker/run_check.py --verbose --output-format markdown --output-file consistency_report.md

# 孤立ファイル検出・クリーンアップ
python3 database_consistency_checker/run_check.py --checks orphaned_files

# パフォーマンス監視レポート生成
# 想定データ量との乖離・応答時間の確認
```

## 品質保証・整合性チェック

### 自動チェック詳細

#### 1. テーブル存在整合性チェック
```python
# チェック対象
- テーブル一覧.md
- entity_relationships.yaml
- DDLファイル (ddl/*.sql)
- テーブル詳細定義ファイル (table-details/*.yaml)

# エラー例
❌ テーブル一覧.mdに定義されていません
❌ DDLファイルが存在しません
⚠️ エンティティ関連定義に存在しません
```

#### 2. カラム定義整合性チェック
```python
# チェック対象
- YAML詳細定義のカラム定義
- DDLファイルのCREATE TABLE文
- Markdown定義書のカラム一覧

# エラー例
❌ データ型が一致しません: YAML(VARCHAR(50)) ≠ DDL(VARCHAR(100))
❌ NOT NULL制約が一致しません
❌ デフォルト値が一致しません
```

#### 3. 外部キー整合性チェック
```python
# チェック対象
- 参照先テーブルの存在確認
- 参照先カラムのデータ型一致確認
- CASCADE/RESTRICT設定の妥当性確認

# エラー例
❌ 参照先テーブル 'MST_Department' が存在しません
❌ 参照先カラムのデータ型が一致しません
⚠️ CASCADE設定により意図しないデータ削除の可能性
```

### 手動レビューチェックリスト

#### 業務要件との整合性
- [ ] 要求仕様IDが全テーブル・全カラムに割り当てられている
- [ ] 業務ルールがテーブル制約として適切に実装されている
- [ ] データ項目の定義が業務要件と一致している
- [ ] 必須項目・任意項目の設定が適切である

#### 🔴 必須セクション内容確認（省略禁止）
- [ ] 🔴 revision_historyに適切な改版履歴が記録されている（最低1エントリ必須）
- [ ] 🔴 overviewにテーブルの目的と概要が明確に記載されている（最低50文字必須）
- [ ] 🔴 notesに運用・保守に必要な特記事項が記載されている（最低3項目必須）
- [ ] 🔴 business_rulesに業務ルール・制約が要件と整合している（最低3項目必須）

#### ⚠️ 必須セクション不備時の対応
- **自動検証エラー**: Git pre-commitフックで自動的に検出・拒否
- **手動確認**: レビュー時に必須セクションの内容品質を確認
- **修正必須**: 不備が発見された場合は即座に修正が必要
- **例外なし**: いかなる理由でも省略は認められない

#### エンティティ関連の妥当性
- [ ] 正規化が適切に行われている（第3正規形まで）
- [ ] 非正規化の判断が妥当である（パフォーマンス要件に基づく）
- [ ] エンティティ間の関連が適切に定義されている
- [ ] 循環参照が発生していない

#### パフォーマンス要件
- [ ] インデックス設計が検索パターンに適している
- [ ] 複合インデックスの列順序が最適化されている
- [ ] 不要なインデックスが存在しない
- [ ] パーティショニングの検討が必要な大量データテーブルを特定

#### セキュリティ要件
- [ ] 個人情報含有テーブルで暗号化が設定されている
- [ ] 機密情報レベルに応じたアクセス制御が設計されている
- [ ] 監査証跡テーブルで改ざん防止策が実装されている
- [ ] パスワード等の機密データがハッシュ化されている

#### 実装整合性
- [ ] Prisma スキーマとの整合性が確保されている
- [ ] 設計書と実装の乖離が文書化されている
- [ ] 将来のマルチテナント化への移行計画が明確である
- [ ] シングルテナント設計での制約が適切に設定されている

## 定期メンテナンス指針

### 月次作業
```bash
# 1. 全体整合性チェック実行
python3 database_consistency_checker/run_check.py --verbose --output-file monthly_check.log

# 2. 新規追加テーブルの品質確認
# 要求仕様IDとの対応確認
# 命名規則準拠確認
# マルチテナント対応確認

# 3. パフォーマンス監視
# 想定データ量との乖離チェック
# 応答時間の監視結果確認
# スロークエリの分析

# 4. セキュリティ監査
# 個人情報・機密情報含有テーブルの確認
# アクセスログの分析
# 暗号化設定の確認
```

### 四半期作業
```bash
# 1. 孤立ファイル・重複ファイルのクリーンアップ
python3 database_consistency_checker/run_check.py --checks orphaned_files
# 検出されたファイルの手動確認・削除

# 2. パフォーマンス要件の見直し
# 応答時間・データ量の再評価
# インデックス設計の最適化
# パーティショニング戦略の検討

# 3. セキュリティ監査
# 個人情報・機密情報含有テーブルの棚卸
# アクセス権限の見直し
# 暗号化アルゴリズムの更新検討

# 4. アーカイブ実行計画
# 各テーブルの保持期間確認
# アーカイブ対象データの特定
# アーカイブ実行スケジュール策定
```

### 半期作業
```bash
# 1. ツール機能の見直し・改善
# table_generatorの機能拡張検討
# database_consistency_checkerの新機能追加
# 自動化スクリプトの改善

# 2. 設計方針の更新
# 技術トレンドへの対応
# 業務要件変化への対応
# パフォーマンス要件の見直し

# 3. アーカイブ実行
# 各テーブルの条件に従ったデータアーカイブ
# アーカイブデータの検証
# 本番環境からの削除実行

# 4. 災害復旧テスト
# バックアップデータからの復旧テスト
# データ整合性の確認
# 復旧手順の見直し
```

## 品質指標・成功基準

### 設計品質指標
- **整合性チェック通過率**: 100%維持（必須）
- **要求仕様ID対応率**: 100%（全テーブル・全カラム）
- **命名規則準拠率**: 100%（プレフィックス・命名規則）
- **ドキュメント自動生成率**: 95%以上
- **Prisma整合性**: 100%（設計書とPrismaスキーマの整合性）

### 開発効率指標
- **新規テーブル追加時間**: 30分以内（設計〜生成〜チェック完了）
- **既存テーブル修正時間**: 15分以内（修正〜チェック完了）
- **整合性チェック実行時間**: 5分以内（全テーブル）
- **エラー修正時間**: 問題発見から修正完了まで1時間以内
- **自動生成成功率**: 95%以上（エラーなしでの生成）

### 運用品質指標
- **データ量監視**: 想定値の150%を超えた場合はアラート
- **パフォーマンス監視**: 応答時間が設定値の120%を超えた場合は調査
- **セキュリティ監査**: 個人情報・機密情報含有テーブルは月次監査
- **アーカイブ実行**: 各テーブルの条件に従い自動実行
- **可用性**: 99.5%以上を維持

## トラブルシューティング・FAQ

### よくある問題と解決方法

#### 1. 整合性チェックエラー
```bash
# 問題: テーブル存在整合性エラー
❌ MST_Department: DDLファイルが存在しません

# 解決方法
# 1. エラー詳細確認
python3 database_consistency_checker/run_check.py --verbose --tables MST_Department

# 2. 個別ファイル確認
ls -la table-details/MST_Department_details.yaml
ls -la ddl/MST_Department.sql
ls -la tables/テーブル定義書_MST_Department_*.md

# 3. 再生成実行
python3 -m table_generator --table MST_Department --verbose

# 4. 再チェック
python3 database_consistency_checker/run_check.py --tables MST_Department
```

#### 2. DDL生成エラー
```bash
# 問題: YAML構文エラー
❌ YAML解析エラー: mapping values are not allowed here

# 解決方法
# 1. YAML構文チェック
python3 -c "import yaml; yaml.safe_load(open('table-details/MST_Employee_details.yaml'))"

# 2. インデント・構文確認
# - インデントはスペース2文字で統一
# - コロン後にスペース必須
# - 文字列は引用符で囲む

# 3. 再生成実行
python3 -m table_generator --table MST_Employee --verbose
```

#### 3. 外部キー制約エラー
```bash
# 問題: 外部キー制約違反
❌ 参照先テーブル 'MST_Department' が存在しません

# 解決方法
# 1. 参照先テーブルの存在確認
python3 database_consistency_checker/run_check.py --tables MST_Department

# 2. 参照先テーブルの生成
python3 -m table_generator --table MST_Department

# 3. 参照元テーブルの再生成
python3 -m table_generator --table MST_Employee

# 4. 外部キー整合性チェック
python3 database_consistency_checker/run_check.py --checks foreign_key_consistency
```

#### 4. パフォーマンス問題
```bash
# 問題: 応答時間が設定値を超過
⚠️ MST_Employee: SELECT応答時間 15ms > 設定値 10ms

# 解決方法
# 1. インデックス設計の見直し
# - 検索条件に使用されるカラムにインデックス追加
# - 複合インデックスの列順序最適化

# 2. クエリの最適化
# - WHERE句の条件見直し
# - JOINの最適化
# - 不要なカラムの除外

# 3. データ量の確認
# - 想定データ量との乖離確認
# - パーティショニングの検討
```

### 緊急時対応フロー
```
1. 問題発見
   ↓
2. 影響範囲特定
   - 関連テーブル・機能の確認
   - ユーザー影響度の評価
   ↓
3. 根本原因分析
   - ログ・エラーメッセージの確認
   - 設定・データの確認
   ↓
4. 応急処置
   - サービス継続のための一時対応
   - ユーザー通知
   ↓
5. 恒久対策
   - YAML修正
   - 再生成実行
   - 整合性確認
   ↓
6. 再発防止策
   - チェック項目の追加
   - 手順の見直し
   ↓
7. Git コミット
   - 修正内容の記録
   - 影響範囲の明記
```

## 関連ドキュメント

### 内部ドキュメント
- **テーブル一覧**: `docs/design/database/テーブル一覧.md`
- **エンティティ関連図**: `docs/design/database/エンティティ関連図.md`
- **ツール詳細ガイド**: `docs/design/database/tools/README.md`

### 外部参照
- **PostgreSQL公式ドキュメント**: https://www.postgresql.org/docs/
- **Prisma公式ドキュメント**: https://www.prisma.io/docs/
- **マルチテナント設計パターン**: 06-multitenant-development.md（将来対応）
- **バックエンド設計ガイドライン**: 04-backend-guidelines.md

## 現在の実装状況と今後の方針

### 実装済みテーブル（Prismaスキーマベース）
- **マスタ系**: 22テーブル（MST_Employee, MST_Department等）
- **トランザクション系**: 8テーブル（TRN_SkillRecord, TRN_GoalProgress等）
- **履歴系**: 3テーブル（HIS_AuditLog, HIS_NotificationLog等）
- **システム系**: 8テーブル（SYS_SkillMatrix, SYS_SystemLog等）
- **ワーク系**: 1テーブル（WRK_BatchJobLog）

### 設計書との主な乖離点
1. **テナント対応**: 設計書はマルチテナント、実装はシングルテナント
2. **カラム構成**: 一部テーブルで設計書と実装のカラム構成が異なる
3. **制約設定**: 外部キー制約の設定方法が異なる

### 今後の対応方針
1. **Phase 1**: 現在のシングルテナント実装を完成
2. **Phase 2**: 設計書と実装の乖離を文書化
3. **Phase 3**: 将来のマルチテナント化計画を策定
4. **Phase 4**: 段階的なマルチテナント化実装（必要に応じて）

---

このガイドラインに従って、効率的で品質の高いDB設計・開発を実現してください。
