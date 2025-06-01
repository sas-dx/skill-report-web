# テーブル定義書: MST_SystemConfig

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_SystemConfig |
| 論理名 | システム設定 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-01 20:40:25 |

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
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  | マルチテナント識別子 |
| config_key | 設定キー | VARCHAR | 100 | ○ |  | 設定項目を一意に識別するキー（例：MAX_LOGIN_ATTEMPTS、SESSION_TIMEOUT） |
| config_name | 設定名 | VARCHAR | 200 | ○ |  | 設定項目の表示名・説明 |
| config_value | 設定値 | TEXT |  | ○ |  | 設定の値（文字列、数値、JSON等） |
| config_type | 設定タイプ | ENUM |  | ○ |  | 設定値のデータタイプ（STRING:文字列、INTEGER:整数、DECIMAL:小数、BOOLEAN:真偽値、JSON:JSON、ENCRYPTED:暗号化） |
| config_category | 設定カテゴリ | ENUM |  | ○ |  | 設定の分類（SECURITY:セキュリティ、SYSTEM:システム、BUSINESS:業務、UI:ユーザーインターフェース、INTEGRATION:連携） |
| default_value | デフォルト値 | TEXT |  | ○ |  | 設定のデフォルト値 |
| validation_rule | 検証ルール | TEXT |  | ○ |  | 設定値の検証ルール（正規表現、範囲等） |
| description | 説明 | TEXT |  | ○ |  | 設定項目の詳細説明・用途 |
| is_encrypted | 暗号化フラグ | BOOLEAN |  | ○ | False | 設定値が暗号化されているかどうか |
| is_system_only | システム専用フラグ | BOOLEAN |  | ○ | False | システム内部でのみ使用される設定かどうか |
| is_user_configurable | ユーザー設定可能フラグ | BOOLEAN |  | ○ | True | 管理者がUI経由で変更可能かどうか |
| requires_restart | 再起動要否 | BOOLEAN |  | ○ | False | 設定変更時にシステム再起動が必要かどうか |
| environment | 環境 | ENUM |  | ○ | ALL | 設定が適用される環境（DEV:開発、TEST:テスト、PROD:本番、ALL:全環境） |
| tenant_specific | テナント固有フラグ | BOOLEAN |  | ○ | False | テナントごとに異なる値を持つ設定かどうか |
| last_modified_by | 最終更新者 | VARCHAR | 50 | ○ |  | 設定を最後に更新したユーザーID |
| last_modified_reason | 更新理由 | TEXT |  | ○ |  | 設定変更の理由・目的 |
| sort_order | 表示順序 | INTEGER |  | ○ | 0 | 設定一覧での表示順序 |
| is_active | 有効フラグ | BOOLEAN |  | ○ | True | 設定が有効かどうか |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_config_key | config_key | ○ | 設定キー検索用（一意） |
| idx_config_category | config_category | × | 設定カテゴリ検索用 |
| idx_config_type | config_type | × | 設定タイプ検索用 |
| idx_user_configurable | is_user_configurable, is_active | × | ユーザー設定可能項目検索用 |
| idx_environment | environment, is_active | × | 環境別設定検索用 |
| idx_tenant_specific | tenant_specific, is_active | × | テナント固有設定検索用 |
| idx_sort_order | sort_order | × | 表示順序検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_config_key | UNIQUE |  | 設定キー一意制約 |
| chk_config_type | CHECK | config_type IN ('STRING', 'INTEGER', 'DECIMAL', 'BOOLEAN', 'JSON', 'ENCRYPTED') | 設定タイプ値チェック制約 |
| chk_config_category | CHECK | config_category IN ('SECURITY', 'SYSTEM', 'BUSINESS', 'UI', 'INTEGRATION') | 設定カテゴリ値チェック制約 |
| chk_environment | CHECK | environment IN ('DEV', 'TEST', 'PROD', 'ALL') | 環境値チェック制約 |

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

## 業務ルール

- 設定キーは一意である必要がある
- 暗号化設定は config_type = 'ENCRYPTED' に設定
- システム専用設定は is_user_configurable = false に設定
- 検証ルールは設定値の妥当性チェックに使用
- 環境固有設定は適切な environment 値を設定
- テナント固有設定は tenant_specific = true に設定
- 設定変更時は last_modified_by と last_modified_reason を必須記録

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - システム設定マスタテーブルの詳細定義 |
