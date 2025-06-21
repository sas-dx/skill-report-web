# テーブル定義書: MST_SystemConfig

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_SystemConfig |
| 論理名 | システム設定 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 17:20:35 |

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
| config_key |  | VARCHAR |  | ○ |  |  |
| config_name |  | VARCHAR |  | ○ |  |  |
| config_value |  | TEXT |  | ○ |  |  |
| config_type |  | ENUM |  | ○ |  |  |
| config_category |  | ENUM |  | ○ |  |  |
| default_value |  | TEXT |  | ○ |  |  |
| validation_rule |  | TEXT |  | ○ |  |  |
| description |  | TEXT |  | ○ |  |  |
| is_encrypted |  | BOOLEAN |  | ○ | False |  |
| is_system_only |  | BOOLEAN |  | ○ | False |  |
| is_user_configurable |  | BOOLEAN |  | ○ | True |  |
| requires_restart |  | BOOLEAN |  | ○ | False |  |
| environment |  | ENUM |  | ○ | ALL |  |
| tenant_specific |  | BOOLEAN |  | ○ | False |  |
| last_modified_by |  | VARCHAR |  | ○ |  |  |
| last_modified_reason |  | TEXT |  | ○ |  |  |
| sort_order |  | INTEGER |  | ○ | 0 |  |
| is_active |  | BOOLEAN |  | ○ | True |  |
| created_at | レコード作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | レコード更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード更新日時 |

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

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
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