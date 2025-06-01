# テーブル定義書: MST_TenantSettings (テナント設定)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_TenantSettings |
| 論理名 | テナント設定 |
| カテゴリ | マスタ系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/MST_TenantSettings_details.yaml` で行ってください。


## 📝 改版履歴

> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：
> `table-details/TABLE_NAME_details.yaml`

| バージョン | 更新日 | 更新者 | 主な変更内容 |
|------------|--------|--------|-------------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - テナント設定マスタテーブルの詳細定義 |


## 📝 テーブル概要

MST_TenantSettings（テナント設定）は、マルチテナントシステムにおける各テナント固有の設定情報を管理するマスタテーブルです。

主な目的：
- テナント別システム設定の管理
- 機能有効/無効の制御設定
- UI・表示設定のカスタマイズ
- 業務ルール・制限値の設定
- 外部連携設定の管理

このテーブルは、マルチテナント管理機能において各テナントの個別要件に対応する重要なマスタデータです。


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  | ● |  | マルチテナント識別子 |
| id | ID | VARCHAR | 50 | ○ |  |  |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | ● |  | 設定対象のテナントID（MST_Tenantへの参照） |
| setting_category | 設定カテゴリ | ENUM |  | ○ |  |  |  | 設定の分類（SYSTEM:システム、UI:ユーザーインターフェース、BUSINESS:業務、SECURITY:セキュリティ、INTEGRATION:連携） |
| setting_key | 設定キー | VARCHAR | 100 | ○ |  |  |  | 設定項目の識別キー（例：max_users、theme_color、skill_approval_required等） |
| setting_name | 設定名 | VARCHAR | 200 | ○ |  |  |  | 設定項目の表示名 |
| setting_description | 設定説明 | TEXT |  | ○ |  |  |  | 設定項目の詳細説明 |
| data_type | データ型 | ENUM |  | ○ |  |  |  | 設定値のデータ型（STRING:文字列、INTEGER:整数、BOOLEAN:真偽値、JSON:JSON、DECIMAL:小数） |
| setting_value | 設定値 | TEXT |  | ○ |  |  |  | 実際の設定値（文字列として格納、data_typeに応じて解釈） |
| default_value | デフォルト値 | TEXT |  | ○ |  |  |  | 設定のデフォルト値 |
| validation_rules | バリデーションルール | TEXT |  | ○ |  |  |  | 設定値のバリデーションルール（JSON形式） |
| is_required | 必須フラグ | BOOLEAN |  | ○ |  |  |  | 設定が必須かどうか |
| is_encrypted | 暗号化フラグ | BOOLEAN |  | ○ |  |  |  | 設定値を暗号化するかどうか |
| is_system_managed | システム管理フラグ | BOOLEAN |  | ○ |  |  |  | システムが自動管理する設定かどうか |
| is_user_configurable | ユーザー設定可能フラグ | BOOLEAN |  | ○ |  |  | True | テナント管理者が変更可能かどうか |
| display_order | 表示順序 | INTEGER |  | ○ |  |  |  | 管理画面での表示順序 |
| effective_from | 有効開始日時 | TIMESTAMP |  | ○ |  |  |  | 設定が有効になる日時 |
| effective_until | 有効終了日時 | TIMESTAMP |  | ○ |  |  |  | 設定が無効になる日時 |
| last_modified_by | 最終更新者 | VARCHAR | 50 | ○ |  |  |  | 設定を最後に更新したユーザーID |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_tenant_settings_tenant_key | tenant_id, setting_key | ○ | テナント別設定キー検索用（一意） |
| idx_tenant_settings_category | setting_category | × | 設定カテゴリ別検索用 |
| idx_tenant_settings_configurable | is_user_configurable | × | ユーザー設定可能フラグ検索用 |
| idx_tenant_settings_system_managed | is_system_managed | × | システム管理フラグ検索用 |
| idx_tenant_settings_display_order | tenant_id, setting_category, display_order | × | 表示順序検索用 |
| idx_tenant_settings_effective | effective_from, effective_until | × | 有効期間検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_tenant_settings_tenant_key | UNIQUE | tenant_id, setting_key |  | テナント内設定キー一意制約 |
| chk_tenant_settings_category | CHECK |  | setting_category IN ('SYSTEM', 'UI', 'BUSINESS', 'SECURITY', 'INTEGRATION') | 設定カテゴリ値チェック制約 |
| chk_tenant_settings_data_type | CHECK |  | data_type IN ('STRING', 'INTEGER', 'BOOLEAN', 'JSON', 'DECIMAL') | データ型値チェック制約 |
| chk_tenant_settings_effective_period | CHECK |  | effective_until IS NULL OR effective_from IS NULL OR effective_until >= effective_from | 有効期間整合性チェック制約 |
| chk_tenant_settings_display_order_positive | CHECK |  | display_order >= 0 | 表示順序正数チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_tenant_settings_tenant | tenant_id | MST_Tenant | id | CASCADE | CASCADE | テナント管理への外部キー |

## 📊 サンプルデータ

```json
[
  {
    "id": "TS001",
    "tenant_id": "TENANT001",
    "setting_category": "SYSTEM",
    "setting_key": "max_users",
    "setting_name": "最大ユーザー数",
    "setting_description": "このテナントで作成可能な最大ユーザー数",
    "data_type": "INTEGER",
    "setting_value": "100",
    "default_value": "50",
    "validation_rules": "{\"min\": 1, \"max\": 1000}",
    "is_required": true,
    "is_encrypted": false,
    "is_system_managed": false,
    "is_user_configurable": false,
    "display_order": 1,
    "effective_from": "2025-01-01 00:00:00",
    "effective_until": null,
    "last_modified_by": "SYSTEM"
  },
  {
    "id": "TS002",
    "tenant_id": "TENANT001",
    "setting_category": "UI",
    "setting_key": "theme_color",
    "setting_name": "テーマカラー",
    "setting_description": "システムのメインテーマカラー",
    "data_type": "STRING",
    "setting_value": "#2563eb",
    "default_value": "#3b82f6",
    "validation_rules": "{\"pattern\": \"^#[0-9a-fA-F]{6}$\"}",
    "is_required": false,
    "is_encrypted": false,
    "is_system_managed": false,
    "is_user_configurable": true,
    "display_order": 1,
    "effective_from": null,
    "effective_until": null,
    "last_modified_by": "USER001"
  },
  {
    "id": "TS003",
    "tenant_id": "TENANT001",
    "setting_category": "BUSINESS",
    "setting_key": "skill_approval_required",
    "setting_name": "スキル承認必須",
    "setting_description": "スキル登録時に承認が必要かどうか",
    "data_type": "BOOLEAN",
    "setting_value": "true",
    "default_value": "false",
    "validation_rules": null,
    "is_required": true,
    "is_encrypted": false,
    "is_system_managed": false,
    "is_user_configurable": true,
    "display_order": 1,
    "effective_from": null,
    "effective_until": null,
    "last_modified_by": "USER001"
  },
  {
    "id": "TS004",
    "tenant_id": "TENANT001",
    "setting_category": "SECURITY",
    "setting_key": "password_policy",
    "setting_name": "パスワードポリシー",
    "setting_description": "パスワードの複雑性要件",
    "data_type": "JSON",
    "setting_value": "{\"min_length\": 8, \"require_uppercase\": true, \"require_lowercase\": true, \"require_numbers\": true, \"require_symbols\": false}",
    "default_value": "{\"min_length\": 6, \"require_uppercase\": false, \"require_lowercase\": false, \"require_numbers\": false, \"require_symbols\": false}",
    "validation_rules": "{\"type\": \"object\", \"properties\": {\"min_length\": {\"type\": \"integer\", \"minimum\": 4, \"maximum\": 128}}}",
    "is_required": true,
    "is_encrypted": false,
    "is_system_managed": false,
    "is_user_configurable": true,
    "display_order": 1,
    "effective_from": null,
    "effective_until": null,
    "last_modified_by": "USER001"
  }
]
```

## 📌 特記事項

- 設定はテナント・キーの組み合わせで一意
- setting_valueは文字列として格納し、data_typeに応じて解釈
- 暗号化フラグがtrueの場合、setting_valueは暗号化して保存
- validation_rulesはJSON Schema形式で設定値の検証ルールを定義
- 有効期間により時限的な設定変更に対応
- システム管理フラグによりシステム専用設定を区別
- 表示順序により管理画面での設定項目の並び順を制御

## 📋 業務ルール

- 同一テナント内で設定キーは重複不可
- 必須設定は削除不可
- システム管理設定はユーザーによる変更不可
- 暗号化設定の値は復号化して表示
- 有効期間外の設定は無効として扱う
- バリデーションルールに違反する設定値は保存不可
- デフォルト値は設定値が未設定の場合に使用
- 設定変更時は最終更新者を記録
