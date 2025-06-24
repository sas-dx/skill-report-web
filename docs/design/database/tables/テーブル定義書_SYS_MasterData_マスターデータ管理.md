# テーブル定義書: SYS_MasterData

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_MasterData |
| 論理名 | マスターデータ管理 |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-24 23:05:57 |

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
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| data_type | データ型 | ENUM |  | ○ | STRING | データ型 |
| default_value | デフォルト値 | TEXT |  | ○ |  | デフォルト値 |
| description | 説明 | TEXT |  | ○ |  | 説明 |
| display_order | 表示順序 | INTEGER |  | ○ | 0 | 表示順序 |
| effective_from | 有効開始日 | DATE |  | ○ |  | 有効開始日 |
| effective_to | 有効終了日 | DATE |  | ○ |  | 有効終了日 |
| is_editable | 編集可能フラグ | BOOLEAN |  | ○ | True | 編集可能フラグ |
| is_system_managed | システム管理フラグ | BOOLEAN |  | ○ | False | システム管理フラグ |
| last_modified_at | 最終更新日時 | TIMESTAMP |  | ○ |  | 最終更新日時 |
| last_modified_by | 最終更新者 | VARCHAR | 100 | ○ |  | 最終更新者 |
| master_category | マスターカテゴリ | VARCHAR | 50 | ○ |  | マスターカテゴリ |
| master_key | マスターキー | VARCHAR | 100 | ○ |  | マスターキー |
| master_name | マスター名 | VARCHAR | 200 | ○ |  | マスター名 |
| master_value | マスター値 | TEXT |  | ○ |  | マスター値 |
| masterdata_id | SYS_MasterDataの主キー | SERIAL |  | × |  | SYS_MasterDataの主キー |
| validation_rule | バリデーションルール | TEXT |  | ○ |  | バリデーションルール |
| version | バージョン | INTEGER |  | ○ | 1 | バージョン |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_SYS_MasterData_master_key | master_key | ○ |  |
| idx_SYS_MasterData_category | master_category | × |  |
| idx_SYS_MasterData_category_order | master_category, display_order | × |  |
| idx_SYS_MasterData_effective_period | effective_from, effective_to | × |  |
| idx_SYS_MasterData_system_managed | is_system_managed | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_master_key | UNIQUE |  | master_key一意制約 |
| chk_data_type | CHECK | data_type IN (...) | data_type値チェック制約 |

## サンプルデータ

| master_key | master_category | master_name | master_value | data_type | default_value | validation_rule | is_system_managed | is_editable | display_order | description | effective_from | effective_to | last_modified_by | last_modified_at | version |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| SYSTEM.MAX_LOGIN_ATTEMPTS | SYSTEM | 最大ログイン試行回数 | 5 | INTEGER | 3 | ^[1-9][0-9]*$ | True | True | 1 | ログイン失敗時の最大試行回数。この回数を超えるとアカウントがロックされます。 | 2024-01-01 | None | system_admin | 2024-01-01 10:00:00 | 1 |
| SYSTEM.SESSION_TIMEOUT_MINUTES | SYSTEM | セッションタイムアウト時間 | 30 | INTEGER | 30 | ^[1-9][0-9]*$ | True | True | 2 | ユーザーセッションの有効時間（分）。この時間を過ぎると自動的にログアウトされます。 | 2024-01-01 | None | system_admin | 2024-01-01 10:00:00 | 1 |
| CODE.SKILL_LEVELS | CODE | スキルレベル定義 | {"1":"初級","2":"中級","3":"上級","4":"エキスパート","5":"マスター"} | JSON | {"1":"初級","2":"中級","3":"上級","4":"エキスパート","5":"マスター"} | None | False | True | 1 | スキル評価で使用するレベル定義。1-5の数値とその意味を定義します。 | 2024-01-01 | None | admin_user | 2024-01-01 10:00:00 | 1 |

## 特記事項

- マスターキーは一意である必要がある
- システム管理のマスターデータは慎重に変更する必要がある
- JSON形式の値は妥当性チェックを行う
- 有効期間を設定することで、時限的な設定変更が可能
- バージョン管理により楽観的排他制御を実現
- 変更履歴は別テーブルで管理する
- 論理削除は is_deleted フラグで管理
- マスターキーは「カテゴリ.項目名」形式で命名する
- システム管理のマスターデータ変更時は管理者承認が必要
- JSON形式の値は構文チェックを行う
- 有効期間外のマスターデータは使用しない
- バージョン番号は更新時に自動インクリメントする
- 重要な設定変更時は変更前後の値をログに記録する
- デフォルト値は必ず設定し、システム障害時の代替値として使用する
- バリデーションルールに違反する値は登録・更新を拒否する

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | システム | 初版作成 - SYS_MasterDataの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214007 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214907 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215000 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215054 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223433 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |