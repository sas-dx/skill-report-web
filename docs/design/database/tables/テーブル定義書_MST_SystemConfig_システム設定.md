# テーブル定義書_MST_SystemConfig_システム設定

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_SystemConfig |
| 論理名 | システム設定 |
| 用途 | システム全体の動作制御設定管理 |
| カテゴリ | マスタ系 |
| 作成日 | 2024-12-19 |
| 最終更新日 | 2024-12-19 |

## テーブル概要

システム全体の動作を制御する各種設定値を管理するマスタテーブルです。
アプリケーション設定、セキュリティ設定、パフォーマンス設定、通知設定などを
キー・バリュー形式で格納し、システムの柔軟な運用と設定変更を可能にします。
設定値の変更履歴も管理し、設定変更による影響の追跡と復旧を支援します。

## テーブル構造

| # | カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | PK | FK | インデックス | 説明 |
|---|----------|--------|----------|------|------|------------|----|----|--------------|------|
| 1 | config_id | 設定ID | VARCHAR | 50 | NOT NULL | - | ○ | - | PK | 設定の一意識別子 |
| 2 | tenant_id | テナントID | VARCHAR | 50 | NOT NULL | - | - | ○ | IDX | テナント識別子 |
| 3 | config_category | 設定カテゴリ | VARCHAR | 50 | NOT NULL | - | - | - | IDX | 設定のカテゴリ |
| 4 | config_key | 設定キー | VARCHAR | 100 | NOT NULL | - | - | - | UNQ | 設定のキー名 |
| 5 | config_name | 設定名 | VARCHAR | 200 | NOT NULL | - | - | - | - | 設定の表示名 |
| 6 | config_value | 設定値 | TEXT | - | NOT NULL | - | - | - | - | 設定値 |
| 7 | default_value | デフォルト値 | TEXT | - | NOT NULL | - | - | - | - | デフォルト値 |
| 8 | data_type | データ型 | VARCHAR | 20 | NOT NULL | - | - | - | - | データ型 |
| 9 | description | 説明 | TEXT | - | NULL | - | - | - | - | 設定の説明 |
| 10 | config_group | 設定グループ | VARCHAR | 100 | NULL | - | - | - | IDX | 設定のグループ名 |
| 11 | display_order | 表示順序 | INTEGER | - | NOT NULL | 0 | - | - | IDX | 表示時の順序 |
| 12 | is_required | 必須フラグ | BOOLEAN | - | NOT NULL | false | - | - | - | 必須設定かどうか |
| 13 | is_editable | 編集可能フラグ | BOOLEAN | - | NOT NULL | true | - | - | - | 編集可能かどうか |
| 14 | is_public | 公開フラグ | BOOLEAN | - | NOT NULL | false | - | - | IDX | 一般ユーザーに公開するか |
| 15 | is_encrypted | 暗号化フラグ | BOOLEAN | - | NOT NULL | false | - | - | - | 値を暗号化するか |
| 16 | validation_rule | 検証ルール | TEXT | - | NULL | - | - | - | - | 入力値の検証ルール |
| 17 | min_value | 最小値 | DECIMAL | 15,2 | NULL | - | - | - | - | 数値型の最小値 |
| 18 | max_value | 最大値 | DECIMAL | 15,2 | NULL | - | - | - | - | 数値型の最大値 |
| 19 | options | 選択肢 | TEXT | - | NULL | - | - | - | - | 選択肢（JSON形式） |
| 20 | is_active | 有効フラグ | BOOLEAN | - | NOT NULL | true | - | - | IDX | 設定が有効かどうか |
| 21 | last_modified_by | 最終変更者 | VARCHAR | 50 | NOT NULL | - | - | ○ | - | 最終変更者のユーザーID |
| 22 | last_modified_at | 最終変更日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | - | 最終変更日時 |
| 23 | created_at | 作成日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | - | レコード作成日時 |
| 24 | created_by | 作成者 | VARCHAR | 50 | NOT NULL | - | - | ○ | - | レコード作成者 |
| 25 | updated_at | 更新日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | - | レコード更新日時 |
| 26 | updated_by | 更新者 | VARCHAR | 50 | NOT NULL | - | - | ○ | - | レコード更新者 |

## リレーション

### 参照先テーブル
- MST_Tenant (tenant_id)
- MST_UserAuth (last_modified_by, created_by, updated_by)

### 参照元テーブル
- HIS_ConfigHistory (config_id)
- SYS_SystemLog (config_id)

## データ仕様

### config_category（設定カテゴリ）
- SYSTEM: システム基本設定
- SECURITY: セキュリティ関連設定
- PERFORMANCE: パフォーマンス関連設定
- NOTIFICATION: 通知関連設定
- UI: ユーザーインターフェース設定
- INTEGRATION: 外部システム連携設定

### data_type（データ型）
- STRING: 文字列
- INTEGER: 整数
- DECIMAL: 小数
- BOOLEAN: 真偽値
- JSON: JSON形式データ
- DATE: 日付
- DATETIME: 日時

### 設定例
- app.name: アプリケーション名
- session.timeout: セッションタイムアウト（秒）
- db.connection.pool.size: DB接続プールサイズ
- email.smtp.enabled: メール通知有効フラグ

## 運用仕様

### データ保持期間
- 永続保持（システム運用に必要）

### バックアップ
- 日次バックアップ対象
- 設定変更前の自動バックアップ

### メンテナンス
- 設定変更時の影響範囲確認
- 設定値の妥当性チェック

## パフォーマンス

### 想定レコード数
- 初期: 100件
- 1年後: 200件
- 3年後: 500件

### アクセスパターン
- 設定値読み込み: 高頻度
- 設定値更新: 低頻度
- 設定一覧表示: 中頻度

### インデックス設計
- PRIMARY KEY: config_id
- UNIQUE: config_key
- INDEX: tenant_id, config_category, config_group, display_order
- INDEX: is_public, is_active

## セキュリティ

### アクセス制御
- 参照: システム管理者、一般ユーザー（公開設定のみ）
- 更新: システム管理者のみ
- 削除: システム管理者のみ（必須設定は削除不可）

### 機密情報
- パスワード、APIキーなどの暗号化
- 機密設定へのアクセス制御
- 設定変更の監査ログ記録

## 移行仕様

### 初期データ
- システム基本設定の投入
- デフォルト値の設定

### データ移行
- 既存システムからの設定移行
- 設定値の妥当性確認

## 特記事項

### 制約事項
- 設定キーは一意である必要がある
- 必須設定は削除できない
- 編集不可設定は管理者のみ変更可能
- 最大値は最小値以上である必要がある

### 拡張予定
- 設定値の履歴管理機能
- 設定変更の承認ワークフロー
- 設定値の自動検証機能

### 関連システム
- システム管理画面
- 設定変更履歴システム
- 監査ログシステム
- キャッシュシステム
