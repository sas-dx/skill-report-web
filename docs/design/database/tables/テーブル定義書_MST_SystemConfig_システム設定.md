# テーブル定義書: MST_SystemConfig

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_SystemConfig |
| 論理名 | システム設定 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:02:18 |

## 概要

MST_SystemConfig（システム設定）は、システム全体の設定値・パラメータを管理するマスタテーブルです。
主な目的：
- システム運用パラメータの一元管理
- 機能ON/OFF設定の管理
- 業務ルール・閾値の設定管理
- 外部連携設定の管理
- セキュリティ設定の管理
このテーブルにより、システムの動作を柔軟に制御し、
運用環境に応じた設定変更を効率的に行うことができます。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| config_key | 設定キー | VARCHAR | 100 | ○ |  | 設定キー |
| config_category | 設定カテゴリ | ENUM |  | ○ |  | 設定カテゴリ |
| config_name | 設定名 | VARCHAR | 200 | ○ |  | 設定名 |
| config_type | 設定タイプ | ENUM |  | ○ |  | 設定タイプ |
| config_value | 設定値 | TEXT |  | ○ |  | 設定値 |
| default_value | デフォルト値 | TEXT |  | ○ |  | デフォルト値 |
| description | 説明 | TEXT |  | ○ |  | 説明 |
| environment | 環境 | ENUM |  | ○ | ALL | 環境 |
| is_active | 有効フラグ | BOOLEAN |  | ○ | True | 有効フラグ |
| is_encrypted | 暗号化フラグ | BOOLEAN |  | ○ | False | 暗号化フラグ |
| is_system_only | システム専用フラグ | BOOLEAN |  | ○ | False | システム専用フラグ |
| is_user_configurable | ユーザー設定可能フラグ | BOOLEAN |  | ○ | True | ユーザー設定可能フラグ |
| last_modified_by | 最終更新者 | VARCHAR | 50 | ○ |  | 最終更新者 |
| last_modified_reason | 更新理由 | TEXT |  | ○ |  | 更新理由 |
| requires_restart | 再起動要否 | BOOLEAN |  | ○ | False | 再起動要否 |
| sort_order | 表示順序 | INTEGER |  | ○ | 0 | 表示順序 |
| systemconfig_id | MST_SystemConfigの主キー | SERIAL |  | × |  | MST_SystemConfigの主キー |
| tenant_specific | テナント固有フラグ | BOOLEAN |  | ○ | False | テナント固有フラグ |
| validation_rule | 検証ルール | TEXT |  | ○ |  | 検証ルール |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_config_key | config_key | ○ |  |
| idx_config_category | config_category | × |  |
| idx_config_type | config_type | × |  |
| idx_user_configurable | is_user_configurable, is_active | × |  |
| idx_environment | environment, is_active | × |  |
| idx_tenant_specific | tenant_specific, is_active | × |  |
| idx_sort_order | sort_order | × |  |
| idx_mst_systemconfig_tenant_id | tenant_id | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_config_key | UNIQUE |  | config_key一意制約 |
| chk_config_type | CHECK | config_type IN (...) | config_type値チェック制約 |

## サンプルデータ

| config_key | config_name | config_value | config_type | config_category | default_value | validation_rule | description | is_encrypted | is_system_only | is_user_configurable | requires_restart | environment | tenant_specific | last_modified_by | last_modified_reason | sort_order | is_active |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| MAX_LOGIN_ATTEMPTS | 最大ログイン試行回数 | 5 | INTEGER | SECURITY | 3 | ^[1-9][0-9]*$ | アカウントロックまでの最大ログイン失敗回数 | False | False | True | False | ALL | True | admin | セキュリティ強化のため | 1 | True |
| SESSION_TIMEOUT_MINUTES | セッションタイムアウト時間（分） | 30 | INTEGER | SECURITY | 60 | ^[1-9][0-9]*$ | ユーザーセッションの自動タイムアウト時間 | False | False | True | False | ALL | True | admin | セキュリティポリシー変更 | 2 | True |
| SKILL_EVALUATION_PERIOD_MONTHS | スキル評価期間（月） | 6 | INTEGER | BUSINESS | 12 | ^[1-9][0-9]*$ | スキル評価の実施間隔 | False | False | True | False | ALL | True | hr_admin | 評価頻度の見直し | 10 | True |

## 特記事項

- 設定キーは英大文字・数字・アンダースコアのみ使用可能
- 暗号化設定は config_type = 'ENCRYPTED' かつ is_encrypted = true で管理
- テナント固有設定は別途テナント設定テーブルとの連携が必要
- システム専用設定は管理画面に表示しない
- 再起動要否フラグは運用時の注意喚起に使用
- 論理削除は is_active フラグで管理
- 設定キーは一意である必要がある
- 暗号化設定は config_type = 'ENCRYPTED' に設定
- システム専用設定は is_user_configurable = false に設定
- 検証ルールは設定値の妥当性チェックに使用
- 環境固有設定は適切な environment 値を設定
- テナント固有設定は tenant_specific = true に設定
- 設定変更時は last_modified_by と last_modified_reason を必須記録

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - システム設定マスタテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214907 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215000 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215053 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223432 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |