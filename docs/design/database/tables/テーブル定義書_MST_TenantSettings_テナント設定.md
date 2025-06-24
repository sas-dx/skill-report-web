# テーブル定義書: MST_TenantSettings

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_TenantSettings |
| 論理名 | テナント設定 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:02:18 |

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
| id | ID | VARCHAR | 50 | ○ |  | ID |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | テナントID |
| data_type | データ型 | ENUM |  | ○ |  | データ型 |
| default_value | デフォルト値 | TEXT |  | ○ |  | デフォルト値 |
| display_order | 表示順序 | INTEGER |  | ○ | 0 | 表示順序 |
| effective_from | 有効開始日時 | TIMESTAMP |  | ○ |  | 有効開始日時 |
| effective_until | 有効終了日時 | TIMESTAMP |  | ○ |  | 有効終了日時 |
| is_encrypted | 暗号化フラグ | BOOLEAN |  | ○ | False | 暗号化フラグ |
| is_required | 必須フラグ | BOOLEAN |  | ○ | False | 必須フラグ |
| is_system_managed | システム管理フラグ | BOOLEAN |  | ○ | False | システム管理フラグ |
| is_user_configurable | ユーザー設定可能フラグ | BOOLEAN |  | ○ | True | ユーザー設定可能フラグ |
| last_modified_by | 最終更新者 | VARCHAR | 50 | ○ |  | 最終更新者 |
| setting_category | 設定カテゴリ | ENUM |  | ○ |  | 設定カテゴリ |
| setting_description | 設定説明 | TEXT |  | ○ |  | 設定説明 |
| setting_key | 設定キー | VARCHAR | 100 | ○ |  | 設定キー |
| setting_name | 設定名 | VARCHAR | 200 | ○ |  | 設定名 |
| setting_value | 設定値 | TEXT |  | ○ |  | 設定値 |
| tenantsettings_id | MST_TenantSettingsの主キー | SERIAL |  | × |  | MST_TenantSettingsの主キー |
| validation_rules | バリデーションルール | TEXT |  | ○ |  | バリデーションルール |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_tenant_settings_tenant_key | tenant_id, setting_key | ○ |  |
| idx_tenant_settings_category | setting_category | × |  |
| idx_tenant_settings_configurable | is_user_configurable | × |  |
| idx_tenant_settings_system_managed | is_system_managed | × |  |
| idx_tenant_settings_display_order | tenant_id, setting_category, display_order | × |  |
| idx_tenant_settings_effective | effective_from, effective_until | × |  |
| idx_mst_tenantsettings_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_tenant_settings_tenant | tenant_id | MST_Tenant | id | CASCADE | CASCADE | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| chk_data_type | CHECK | data_type IN (...) | data_type値チェック制約 |

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
- 同一テナント内で設定キーは重複不可
- 必須設定は削除不可
- システム管理設定はユーザーによる変更不可
- 暗号化設定の値は復号化して表示
- 有効期間外の設定は無効として扱う
- バリデーションルールに違反する設定値は保存不可
- デフォルト値は設定値が未設定の場合に使用
- 設定変更時は最終更新者を記録

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - テナント設定マスタテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214907 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215000 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215053 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223432 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |