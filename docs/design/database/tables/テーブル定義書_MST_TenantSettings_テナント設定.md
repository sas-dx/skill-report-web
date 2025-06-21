# テーブル定義書: MST_TenantSettings

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_TenantSettings |
| 論理名 | テナント設定 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 17:20:34 |

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
| id |  | VARCHAR |  | ○ |  |  |
| tenant_id |  | VARCHAR |  | ○ |  |  |
| setting_category |  | ENUM |  | ○ |  |  |
| setting_key |  | VARCHAR |  | ○ |  |  |
| setting_name |  | VARCHAR |  | ○ |  |  |
| setting_description |  | TEXT |  | ○ |  |  |
| data_type |  | ENUM |  | ○ |  |  |
| setting_value |  | TEXT |  | ○ |  |  |
| default_value |  | TEXT |  | ○ |  |  |
| validation_rules |  | TEXT |  | ○ |  |  |
| is_required |  | BOOLEAN |  | ○ | False |  |
| is_encrypted |  | BOOLEAN |  | ○ | False |  |
| is_system_managed |  | BOOLEAN |  | ○ | False |  |
| is_user_configurable |  | BOOLEAN |  | ○ | True |  |
| display_order |  | INTEGER |  | ○ | 0 |  |
| effective_from |  | TIMESTAMP |  | ○ |  |  |
| effective_until |  | TIMESTAMP |  | ○ |  |  |
| last_modified_by |  | VARCHAR |  | ○ |  |  |
| created_at | レコード作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | レコード更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_tenant_settings_tenant_key | tenant_id, setting_key | ○ |  |
| idx_tenant_settings_category | setting_category | × |  |
| idx_tenant_settings_configurable | is_user_configurable | × |  |
| idx_tenant_settings_system_managed | is_system_managed | × |  |
| idx_tenant_settings_display_order | tenant_id, setting_category, display_order | × |  |
| idx_tenant_settings_effective | effective_from, effective_until | × |  |

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