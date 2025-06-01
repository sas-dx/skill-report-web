# テーブル定義書: MST_TenantSettings

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_TenantSettings |
| 論理名 | テナント設定 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-01 20:40:25 |

## 概要

MST_TenantSettings（テナント設定）は、マルチテナントシステムにおける各テナント固有の設定情報を管理するマスタテーブルです。

主な目的：
- テナント別システム設定の管理
- 機能有効/無効の制御設定
- UI・表示設定のカスタマイズ
- 業務ルール・制限値の設定
- 外部連携設定の管理

このテーブルは、マルチテナント管理機能において各テナントの個別要件に対応する重要なマスタデータです。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  | マルチテナント識別子 |
| id | ID | VARCHAR | 50 | ○ |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | 設定対象のテナントID（MST_Tenantへの参照） |
| setting_category | 設定カテゴリ | ENUM |  | ○ |  | 設定の分類（SYSTEM:システム、UI:ユーザーインターフェース、BUSINESS:業務、SECURITY:セキュリティ、INTEGRATION:連携） |
| setting_key | 設定キー | VARCHAR | 100 | ○ |  | 設定項目の識別キー（例：max_users、theme_color、skill_approval_required等） |
| setting_name | 設定名 | VARCHAR | 200 | ○ |  | 設定項目の表示名 |
| setting_description | 設定説明 | TEXT |  | ○ |  | 設定項目の詳細説明 |
| data_type | データ型 | ENUM |  | ○ |  | 設定値のデータ型（STRING:文字列、INTEGER:整数、BOOLEAN:真偽値、JSON:JSON、DECIMAL:小数） |
| setting_value | 設定値 | TEXT |  | ○ |  | 実際の設定値（文字列として格納、data_typeに応じて解釈） |
| default_value | デフォルト値 | TEXT |  | ○ |  | 設定のデフォルト値 |
| validation_rules | バリデーションルール | TEXT |  | ○ |  | 設定値のバリデーションルール（JSON形式） |
| is_required | 必須フラグ | BOOLEAN |  | ○ | False | 設定が必須かどうか |
| is_encrypted | 暗号化フラグ | BOOLEAN |  | ○ | False | 設定値を暗号化するかどうか |
| is_system_managed | システム管理フラグ | BOOLEAN |  | ○ | False | システムが自動管理する設定かどうか |
| is_user_configurable | ユーザー設定可能フラグ | BOOLEAN |  | ○ | True | テナント管理者が変更可能かどうか |
| display_order | 表示順序 | INTEGER |  | ○ | 0 | 管理画面での表示順序 |
| effective_from | 有効開始日時 | TIMESTAMP |  | ○ |  | 設定が有効になる日時 |
| effective_until | 有効終了日時 | TIMESTAMP |  | ○ |  | 設定が無効になる日時 |
| last_modified_by | 最終更新者 | VARCHAR | 50 | ○ |  | 設定を最後に更新したユーザーID |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_tenant_settings_tenant_key | tenant_id, setting_key | ○ | テナント別設定キー検索用（一意） |
| idx_tenant_settings_category | setting_category | × | 設定カテゴリ別検索用 |
| idx_tenant_settings_configurable | is_user_configurable | × | ユーザー設定可能フラグ検索用 |
| idx_tenant_settings_system_managed | is_system_managed | × | システム管理フラグ検索用 |
| idx_tenant_settings_display_order | tenant_id, setting_category, display_order | × | 表示順序検索用 |
| idx_tenant_settings_effective | effective_from, effective_until | × | 有効期間検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_tenant_settings_tenant | tenant_id | MST_Tenant | id | CASCADE | CASCADE | テナント管理への外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_tenant_settings_tenant_key | UNIQUE |  | テナント内設定キー一意制約 |
| chk_tenant_settings_category | CHECK | setting_category IN ('SYSTEM', 'UI', 'BUSINESS', 'SECURITY', 'INTEGRATION') | 設定カテゴリ値チェック制約 |
| chk_tenant_settings_data_type | CHECK | data_type IN ('STRING', 'INTEGER', 'BOOLEAN', 'JSON', 'DECIMAL') | データ型値チェック制約 |
| chk_tenant_settings_effective_period | CHECK | effective_until IS NULL OR effective_from IS NULL OR effective_until >= effective_from | 有効期間整合性チェック制約 |
| chk_tenant_settings_display_order_positive | CHECK | display_order >= 0 | 表示順序正数チェック制約 |

## サンプルデータ

| id | tenant_id | setting_category | setting_key | setting_name | setting_description | data_type | setting_value | default_value | validation_rules | is_required | is_encrypted | is_system_managed | is_user_configurable | display_order | effective_from | effective_until | last_modified_by |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| TS001 | TENANT001 | SYSTEM | max_users | 最大ユーザー数 | このテナントで作成可能な最大ユーザー数 | INTEGER | 100 | 50 | {"min": 1, "max": 1000} | True | False | False | False | 1 | 2025-01-01 00:00:00 | None | SYSTEM |
| TS002 | TENANT001 | UI | theme_color | テーマカラー | システムのメインテーマカラー | STRING | #2563eb | #3b82f6 | {"pattern": "^#[0-9a-fA-F]{6}$"} | False | False | False | True | 1 | None | None | USER001 |
| TS003 | TENANT001 | BUSINESS | skill_approval_required | スキル承認必須 | スキル登録時に承認が必要かどうか | BOOLEAN | true | false | None | True | False | False | True | 1 | None | None | USER001 |

## 特記事項

- 設定はテナント・キーの組み合わせで一意
- setting_valueは文字列として格納し、data_typeに応じて解釈
- 暗号化フラグがtrueの場合、setting_valueは暗号化して保存
- validation_rulesはJSON Schema形式で設定値の検証ルールを定義
- 有効期間により時限的な設定変更に対応
- システム管理フラグによりシステム専用設定を区別
- 表示順序により管理画面での設定項目の並び順を制御

## 業務ルール

- 同一テナント内で設定キーは重複不可
- 必須設定は削除不可
- システム管理設定はユーザーによる変更不可
- 暗号化設定の値は復号化して表示
- 有効期間外の設定は無効として扱う
- バリデーションルールに違反する設定値は保存不可
- デフォルト値は設定値が未設定の場合に使用
- 設定変更時は最終更新者を記録

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - テナント設定マスタテーブルの詳細定義 |
