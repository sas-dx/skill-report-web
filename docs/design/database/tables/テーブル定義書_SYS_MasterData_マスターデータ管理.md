# テーブル定義書: SYS_MasterData

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_MasterData |
| 論理名 | マスターデータ管理 |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-04 06:57:02 |

## 概要

マスターデータ管理テーブルは、システム全体で使用される各種マスターデータの管理を行うシステムテーブルです。

主な目的：
- システム設定値の一元管理
- 各種コードマスターの管理
- 動的な設定変更への対応
- マスターデータの変更履歴管理

このテーブルは、システムの柔軟性と保守性を向上させる重要なテーブルで、
ハードコーディングを避け、設定値の動的な変更を可能にします。



## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| master_key | マスターキー | VARCHAR | 100 | ○ |  | マスターデータの一意識別キー |
| master_category | マスターカテゴリ | VARCHAR | 50 | ○ |  | マスターデータのカテゴリ（SYSTEM:システム設定、CODE:コードマスター、CONFIG:設定値） |
| master_name | マスター名 | VARCHAR | 200 | ○ |  | マスターデータの表示名 |
| master_value | マスター値 | TEXT |  | ○ |  | マスターデータの値（JSON形式も可） |
| data_type | データ型 | ENUM |  | ○ | STRING | マスター値のデータ型（STRING:文字列、INTEGER:整数、DECIMAL:小数、BOOLEAN:真偽値、JSON:JSON、DATE:日付） |
| default_value | デフォルト値 | TEXT |  | ○ |  | マスターデータのデフォルト値 |
| validation_rule | バリデーションルール | TEXT |  | ○ |  | 値の妥当性チェック用の正規表現やルール |
| is_system_managed | システム管理フラグ | BOOLEAN |  | ○ | False | システムが管理するマスターデータかどうか（true:システム管理、false:ユーザー管理） |
| is_editable | 編集可能フラグ | BOOLEAN |  | ○ | True | 管理画面から編集可能かどうか |
| display_order | 表示順序 | INTEGER |  | ○ | 0 | 同一カテゴリ内での表示順序 |
| description | 説明 | TEXT |  | ○ |  | マスターデータの詳細説明 |
| effective_from | 有効開始日 | DATE |  | ○ |  | マスターデータの有効開始日 |
| effective_to | 有効終了日 | DATE |  | ○ |  | マスターデータの有効終了日 |
| last_modified_by | 最終更新者 | VARCHAR | 100 | ○ |  | 最後にマスターデータを更新したユーザー |
| last_modified_at | 最終更新日時 | TIMESTAMP |  | ○ |  | 最後にマスターデータを更新した日時 |
| version | バージョン | INTEGER |  | ○ | 1 | マスターデータのバージョン番号（楽観的排他制御用） |
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_SYS_MasterData_master_key | master_key | ○ | マスターキー検索用（一意） |
| idx_SYS_MasterData_category | master_category | × | マスターカテゴリ検索用 |
| idx_SYS_MasterData_category_order | master_category, display_order | × | カテゴリ別表示順序検索用 |
| idx_SYS_MasterData_effective_period | effective_from, effective_to | × | 有効期間検索用 |
| idx_SYS_MasterData_system_managed | is_system_managed | × | システム管理フラグ検索用 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_SYS_MasterData_master_key | UNIQUE |  | マスターキー一意制約 |
| chk_SYS_MasterData_data_type | CHECK | data_type IN ('STRING', 'INTEGER', 'DECIMAL', 'BOOLEAN', 'JSON', 'DATE') | データ型値チェック制約 |
| chk_SYS_MasterData_effective_period | CHECK | effective_to IS NULL OR effective_from IS NULL OR effective_to >= effective_from | 有効期間整合性チェック制約 |
| chk_SYS_MasterData_display_order | CHECK | display_order >= 0 | 表示順序非負数チェック制約 |
| chk_SYS_MasterData_version | CHECK | version > 0 | バージョン正数チェック制約 |

## サンプルデータ

| master_key | master_category | master_name | master_value | data_type | default_value | validation_rule | is_system_managed | is_editable | display_order | description | effective_from | effective_to | last_modified_by | last_modified_at | version |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| SYSTEM.MAX_LOGIN_ATTEMPTS | SYSTEM | 最大ログイン試行回数 | 5 | INTEGER | 3 | ^[1-9][0-9]*$ | True | True | 1 | ログイン失敗時の最大試行回数。この回数を超えるとアカウントがロックされます。 | 2024-01-01 | None | system_admin | 2024-01-01 10:00:00 | 1 |
| SYSTEM.SESSION_TIMEOUT_MINUTES | SYSTEM | セッションタイムアウト時間 | 30 | INTEGER | 30 | ^[1-9][0-9]*$ | True | True | 2 | ユーザーセッションの有効時間（分）。この時間を過ぎると自動的にログアウトされます。 | 2024-01-01 | None | system_admin | 2024-01-01 10:00:00 | 1 |
| CODE.SKILL_LEVELS | CODE | スキルレベル定義 | {"1":"初級","2":"中級","3":"上級","4":"エキスパート","5":"マスター"} | JSON | {"1":"初級","2":"中級","3":"上級","4":"エキスパート","5":"マスター"} | None | False | True | 1 | スキル評価で使用するレベル定義。1-5の数値とその意味を定義します。 | 2024-01-01 | None | admin_user | 2024-01-01 10:00:00 | 1 |
| CONFIG.BACKUP_RETENTION_DAYS | CONFIG | バックアップ保持日数 | 90 | INTEGER | 30 | ^[1-9][0-9]*$ | True | True | 1 | フルバックアップファイルの保持期間（日数）。この期間を過ぎたバックアップは自動削除されます。 | 2024-01-01 | None | system_admin | 2024-01-01 10:00:00 | 1 |

## 特記事項

- マスターキーは一意である必要がある
- システム管理のマスターデータは慎重に変更する必要がある
- JSON形式の値は妥当性チェックを行う
- 有効期間を設定することで、時限的な設定変更が可能
- バージョン管理により楽観的排他制御を実現
- 変更履歴は別テーブルで管理する
- 論理削除は is_deleted フラグで管理

## 業務ルール

- マスターキーは「カテゴリ.項目名」形式で命名する
- システム管理のマスターデータ変更時は管理者承認が必要
- JSON形式の値は構文チェックを行う
- 有効期間外のマスターデータは使用しない
- バージョン番号は更新時に自動インクリメントする
- 重要な設定変更時は変更前後の値をログに記録する
- デフォルト値は必ず設定し、システム障害時の代替値として使用する
- バリデーションルールに違反する値は登録・更新を拒否する

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | システム | 初版作成 - SYS_MasterDataの詳細定義 |
