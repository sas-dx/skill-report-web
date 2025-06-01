# テーブル定義書: MST_SystemConfig (システム設定)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_SystemConfig |
| 論理名 | システム設定 |
| カテゴリ | マスタ系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/MST_SystemConfig_details.yaml` で行ってください。


## 📝 改版履歴

> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：
> `table-details/TABLE_NAME_details.yaml`

| バージョン | 更新日 | 更新者 | 主な変更内容 |
|------------|--------|--------|-------------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - システム設定マスタテーブルの詳細定義 |


## 📝 テーブル概要

MST_SystemConfig（システム設定）は、システム全体の設定値・パラメータを管理するマスタテーブルです。

主な目的：
- システム運用パラメータの一元管理
- 機能ON/OFF設定の管理
- 業務ルール・閾値の設定管理
- 外部連携設定の管理
- セキュリティ設定の管理

このテーブルにより、システムの動作を柔軟に制御し、
運用環境に応じた設定変更を効率的に行うことができます。


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  |  |  | マルチテナント識別子 |
| config_key | 設定キー | VARCHAR | 100 | ○ |  |  |  | 設定項目を一意に識別するキー（例：MAX_LOGIN_ATTEMPTS、SESSION_TIMEOUT） |
| config_name | 設定名 | VARCHAR | 200 | ○ |  |  |  | 設定項目の表示名・説明 |
| config_value | 設定値 | TEXT |  | ○ |  |  |  | 設定の値（文字列、数値、JSON等） |
| config_type | 設定タイプ | ENUM |  | ○ |  |  |  | 設定値のデータタイプ（STRING:文字列、INTEGER:整数、DECIMAL:小数、BOOLEAN:真偽値、JSON:JSON、ENCRYPTED:暗号化） |
| config_category | 設定カテゴリ | ENUM |  | ○ |  |  |  | 設定の分類（SECURITY:セキュリティ、SYSTEM:システム、BUSINESS:業務、UI:ユーザーインターフェース、INTEGRATION:連携） |
| default_value | デフォルト値 | TEXT |  | ○ |  |  |  | 設定のデフォルト値 |
| validation_rule | 検証ルール | TEXT |  | ○ |  |  |  | 設定値の検証ルール（正規表現、範囲等） |
| description | 説明 | TEXT |  | ○ |  |  |  | 設定項目の詳細説明・用途 |
| is_encrypted | 暗号化フラグ | BOOLEAN |  | ○ |  |  |  | 設定値が暗号化されているかどうか |
| is_system_only | システム専用フラグ | BOOLEAN |  | ○ |  |  |  | システム内部でのみ使用される設定かどうか |
| is_user_configurable | ユーザー設定可能フラグ | BOOLEAN |  | ○ |  |  | True | 管理者がUI経由で変更可能かどうか |
| requires_restart | 再起動要否 | BOOLEAN |  | ○ |  |  |  | 設定変更時にシステム再起動が必要かどうか |
| environment | 環境 | ENUM |  | ○ |  |  | ALL | 設定が適用される環境（DEV:開発、TEST:テスト、PROD:本番、ALL:全環境） |
| tenant_specific | テナント固有フラグ | BOOLEAN |  | ○ |  |  |  | テナントごとに異なる値を持つ設定かどうか |
| last_modified_by | 最終更新者 | VARCHAR | 50 | ○ |  |  |  | 設定を最後に更新したユーザーID |
| last_modified_reason | 更新理由 | TEXT |  | ○ |  |  |  | 設定変更の理由・目的 |
| sort_order | 表示順序 | INTEGER |  | ○ |  |  |  | 設定一覧での表示順序 |
| is_active | 有効フラグ | BOOLEAN |  | ○ |  |  | True | 設定が有効かどうか |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_config_key | config_key | ○ | 設定キー検索用（一意） |
| idx_config_category | config_category | × | 設定カテゴリ検索用 |
| idx_config_type | config_type | × | 設定タイプ検索用 |
| idx_user_configurable | is_user_configurable, is_active | × | ユーザー設定可能項目検索用 |
| idx_environment | environment, is_active | × | 環境別設定検索用 |
| idx_tenant_specific | tenant_specific, is_active | × | テナント固有設定検索用 |
| idx_sort_order | sort_order | × | 表示順序検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_config_key | UNIQUE | config_key |  | 設定キー一意制約 |
| chk_config_type | CHECK |  | config_type IN ('STRING', 'INTEGER', 'DECIMAL', 'BOOLEAN', 'JSON', 'ENCRYPTED') | 設定タイプ値チェック制約 |
| chk_config_category | CHECK |  | config_category IN ('SECURITY', 'SYSTEM', 'BUSINESS', 'UI', 'INTEGRATION') | 設定カテゴリ値チェック制約 |
| chk_environment | CHECK |  | environment IN ('DEV', 'TEST', 'PROD', 'ALL') | 環境値チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|

## 📊 サンプルデータ

```json
[
  {
    "config_key": "MAX_LOGIN_ATTEMPTS",
    "config_name": "最大ログイン試行回数",
    "config_value": "5",
    "config_type": "INTEGER",
    "config_category": "SECURITY",
    "default_value": "3",
    "validation_rule": "^[1-9][0-9]*$",
    "description": "アカウントロックまでの最大ログイン失敗回数",
    "is_encrypted": false,
    "is_system_only": false,
    "is_user_configurable": true,
    "requires_restart": false,
    "environment": "ALL",
    "tenant_specific": true,
    "last_modified_by": "admin",
    "last_modified_reason": "セキュリティ強化のため",
    "sort_order": 1,
    "is_active": true
  },
  {
    "config_key": "SESSION_TIMEOUT_MINUTES",
    "config_name": "セッションタイムアウト時間（分）",
    "config_value": "30",
    "config_type": "INTEGER",
    "config_category": "SECURITY",
    "default_value": "60",
    "validation_rule": "^[1-9][0-9]*$",
    "description": "ユーザーセッションの自動タイムアウト時間",
    "is_encrypted": false,
    "is_system_only": false,
    "is_user_configurable": true,
    "requires_restart": false,
    "environment": "ALL",
    "tenant_specific": true,
    "last_modified_by": "admin",
    "last_modified_reason": "セキュリティポリシー変更",
    "sort_order": 2,
    "is_active": true
  },
  {
    "config_key": "SKILL_EVALUATION_PERIOD_MONTHS",
    "config_name": "スキル評価期間（月）",
    "config_value": "6",
    "config_type": "INTEGER",
    "config_category": "BUSINESS",
    "default_value": "12",
    "validation_rule": "^[1-9][0-9]*$",
    "description": "スキル評価の実施間隔",
    "is_encrypted": false,
    "is_system_only": false,
    "is_user_configurable": true,
    "requires_restart": false,
    "environment": "ALL",
    "tenant_specific": true,
    "last_modified_by": "hr_admin",
    "last_modified_reason": "評価頻度の見直し",
    "sort_order": 10,
    "is_active": true
  },
  {
    "config_key": "EMAIL_SMTP_PASSWORD",
    "config_name": "SMTP認証パスワード",
    "config_value": "encrypted_password_value",
    "config_type": "ENCRYPTED",
    "config_category": "INTEGRATION",
    "default_value": null,
    "validation_rule": null,
    "description": "メール送信用SMTP認証パスワード",
    "is_encrypted": true,
    "is_system_only": true,
    "is_user_configurable": false,
    "requires_restart": true,
    "environment": "PROD",
    "tenant_specific": false,
    "last_modified_by": "system",
    "last_modified_reason": "初期設定",
    "sort_order": 100,
    "is_active": true
  }
]
```

## 📌 特記事項

- 設定キーは英大文字・数字・アンダースコアのみ使用可能
- 暗号化設定は config_type = 'ENCRYPTED' かつ is_encrypted = true で管理
- テナント固有設定は別途テナント設定テーブルとの連携が必要
- システム専用設定は管理画面に表示しない
- 再起動要否フラグは運用時の注意喚起に使用
- 論理削除は is_active フラグで管理

## 📋 業務ルール

- 設定キーは一意である必要がある
- 暗号化設定は config_type = 'ENCRYPTED' に設定
- システム専用設定は is_user_configurable = false に設定
- 検証ルールは設定値の妥当性チェックに使用
- 環境固有設定は適切な environment 値を設定
- テナント固有設定は tenant_specific = true に設定
- 設定変更時は last_modified_by と last_modified_reason を必須記録
