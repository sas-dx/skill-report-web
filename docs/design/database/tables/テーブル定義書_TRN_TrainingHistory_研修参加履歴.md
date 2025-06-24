# テーブル定義書: TRN_TrainingHistory

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_TrainingHistory |
| 論理名 | 研修参加履歴 |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-24 23:02:18 |

## 概要

TRN_TrainingHistory（研修参加履歴）は、社員が参加した研修・教育プログラムの履歴を管理するトランザクションテーブルです。
主な目的：
- 研修参加履歴の記録・管理
- 学習成果・評価の記録
- スキル向上の追跡
- 継続教育ポイント（PDU）の管理
- 人材育成計画の進捗管理
このテーブルにより、社員の学習履歴を体系的に記録し、
スキル開発やキャリア形成の支援を効率的に行うことができます。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| training_name | 研修名 | VARCHAR | 200 | ○ |  | 研修名 |
| approved_by | 承認者 | VARCHAR | 50 | ○ |  | 承認者 |
| attendance_status | 出席状況 | ENUM |  | ○ | COMPLETED | 出席状況 |
| certificate_number | 証明書番号 | VARCHAR | 100 | ○ |  | 証明書番号 |
| certificate_obtained | 修了証取得 | BOOLEAN |  | ○ | False | 修了証取得 |
| completion_rate | 完了率 | DECIMAL | 5,2 | ○ |  | 完了率 |
| cost | 費用 | DECIMAL | 10,2 | ○ |  | 費用 |
| cost_covered_by | 費用負担者 | ENUM |  | ○ |  | 費用負担者 |
| duration_hours | 研修時間 | DECIMAL | 5,1 | ○ |  | 研修時間 |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 社員ID |
| end_date | 終了日 | DATE |  | ○ |  | 終了日 |
| feedback | フィードバック | TEXT |  | ○ |  | フィードバック |
| follow_up_date | フォローアップ予定日 | DATE |  | ○ |  | フォローアップ予定日 |
| follow_up_required | フォローアップ要否 | BOOLEAN |  | ○ | False | フォローアップ要否 |
| grade | 成績 | VARCHAR | 10 | ○ |  | 成績 |
| instructor_name | 講師名 | VARCHAR | 100 | ○ |  | 講師名 |
| learning_objectives | 学習目標 | TEXT |  | ○ |  | 学習目標 |
| learning_outcomes | 学習成果 | TEXT |  | ○ |  | 学習成果 |
| location | 開催場所 | VARCHAR | 200 | ○ |  | 開催場所 |
| manager_approval | 上司承認 | BOOLEAN |  | ○ | False | 上司承認 |
| pdu_earned | 獲得PDU | DECIMAL | 5,1 | ○ |  | 獲得PDU |
| provider_name | 提供機関名 | VARCHAR | 100 | ○ |  | 提供機関名 |
| recommendation_score | 推奨度 | DECIMAL | 3,1 | ○ |  | 推奨度 |
| satisfaction_score | 満足度 | DECIMAL | 3,1 | ○ |  | 満足度 |
| skills_acquired | 習得スキル | TEXT |  | ○ |  | 習得スキル |
| start_date | 開始日 | DATE |  | ○ |  | 開始日 |
| test_score | テスト点数 | DECIMAL | 5,2 | ○ |  | テスト点数 |
| training_category | 研修カテゴリ | ENUM |  | ○ |  | 研修カテゴリ |
| training_history_id | 研修履歴ID | VARCHAR | 50 | ○ |  | 研修履歴ID |
| training_program_id | 研修プログラムID | VARCHAR | 50 | ○ |  | 研修プログラムID |
| training_type | 研修種別 | ENUM |  | ○ |  | 研修種別 |
| traininghistory_id | TRN_TrainingHistoryの主キー | SERIAL |  | × |  | TRN_TrainingHistoryの主キー |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| created_by | 作成者ID | VARCHAR | 50 | ○ |  | 作成者ID |
| updated_by | 更新者ID | VARCHAR | 50 | ○ |  | 更新者ID |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_training_history_id | training_history_id | ○ |  |
| idx_employee_id | employee_id | × |  |
| idx_training_program_id | training_program_id | × |  |
| idx_training_type | training_type | × |  |
| idx_training_category | training_category | × |  |
| idx_date_range | start_date, end_date | × |  |
| idx_attendance_status | attendance_status | × |  |
| idx_employee_period | employee_id, start_date, end_date | × |  |
| idx_certificate | certificate_obtained, certificate_number | × |  |
| idx_trn_traininghistory_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_training_history_employee | employee_id | MST_Employee | id | CASCADE | RESTRICT | 外部キー制約 |
| fk_training_history_program | training_program_id | MST_TrainingProgram | id | CASCADE | SET NULL | 外部キー制約 |
| fk_training_history_approver | approved_by | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_training_history_id | UNIQUE |  | training_history_id一意制約 |
| chk_attendance_status | CHECK | attendance_status IN (...) | attendance_status値チェック制約 |
| chk_training_type | CHECK | training_type IN (...) | training_type値チェック制約 |

## サンプルデータ

| training_history_id | employee_id | training_program_id | training_name | training_type | training_category | provider_name | instructor_name | start_date | end_date | duration_hours | location | cost | cost_covered_by | attendance_status | completion_rate | test_score | grade | certificate_obtained | certificate_number | pdu_earned | skills_acquired | learning_objectives | learning_outcomes | feedback | satisfaction_score | recommendation_score | follow_up_required | follow_up_date | manager_approval | approved_by |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| TRN_HIS_001 | EMP000001 | TRN_PROG_001 | AWS認定ソリューションアーキテクト研修 | EXTERNAL | TECHNICAL | AWS Training | 田中講師 | 2024-03-01 | 2024-03-03 | 24.0 | 東京研修センター | 150000 | COMPANY | COMPLETED | 100.0 | 85.0 | 合格 | True | AWS-SAA-2024-001 | 24.0 | ["AWS設計", "クラウドアーキテクチャ", "セキュリティ設計"] | AWSでのソリューション設計スキル習得 | クラウドアーキテクチャ設計の基礎を習得、実践的な設計手法を学習 | 実践的な内容で非常に有用だった。講師の説明も分かりやすい。 | 4.5 | 5.0 | True | 2024-06-01 | True | EMP000010 |
| TRN_HIS_002 | EMP000002 | None | プロジェクトマネジメント基礎 | ONLINE | MANAGEMENT | 社内研修センター | 佐藤部長 | 2024-02-15 | 2024-02-15 | 8.0 | オンライン | 0 | COMPANY | COMPLETED | 100.0 | 92.0 | A | True | PM-BASIC-2024-002 | 8.0 | ["プロジェクト計画", "リスク管理", "チームマネジメント"] | プロジェクトマネジメントの基礎知識習得 | PMBOKの基礎理解、実際のプロジェクト運営に活用可能な知識を習得 | 基礎から体系的に学べて良かった。実例が豊富で理解しやすい。 | 4.0 | 4.0 | False | None | True | EMP000010 |

## 特記事項

- 習得スキルはJSON形式で柔軟に管理
- PDU（継続教育ポイント）は資格維持に重要
- 修了証番号は資格証明に使用
- 満足度・推奨度は研修品質向上に活用
- フォローアップは学習効果の定着に重要
- 上司承認は研修参加の正当性を担保
- 研修履歴IDは一意である必要がある
- 開始日は終了日以前である必要がある
- 完了率は0-100%の範囲で設定
- 満足度・推奨度は1.0-5.0の範囲で設定
- 修了証取得時は証明書番号を記録
- PDU対象研修は獲得ポイントを必須記録
- 費用が発生する研修は上司承認必須
- フォローアップ要否に応じて予定日を設定

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 研修参加履歴テーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214007 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214908 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215001 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215054 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222632 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223433 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |