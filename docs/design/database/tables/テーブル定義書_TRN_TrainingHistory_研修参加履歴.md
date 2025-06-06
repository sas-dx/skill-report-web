# テーブル定義書: TRN_TrainingHistory

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_TrainingHistory |
| 論理名 | 研修参加履歴 |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-04 06:57:02 |

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
| training_history_id | 研修履歴ID | VARCHAR | 50 | ○ |  | 研修参加履歴を一意に識別するID |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 参加した社員のID（MST_Employeeへの外部キー） |
| training_program_id | 研修プログラムID | VARCHAR | 50 | ○ |  | 研修プログラムのID（MST_TrainingProgramへの外部キー） |
| training_name | 研修名 | VARCHAR | 200 | ○ |  | 研修・教育プログラムの名称 |
| training_type | 研修種別 | ENUM |  | ○ |  | 研修の種別（INTERNAL:社内研修、EXTERNAL:社外研修、ONLINE:オンライン、CERTIFICATION:資格取得、CONFERENCE:カンファレンス） |
| training_category | 研修カテゴリ | ENUM |  | ○ |  | 研修の分野（TECHNICAL:技術、BUSINESS:ビジネス、MANAGEMENT:マネジメント、SOFT_SKILL:ソフトスキル、COMPLIANCE:コンプライアンス） |
| provider_name | 提供機関名 | VARCHAR | 100 | ○ |  | 研修を提供する機関・会社名 |
| instructor_name | 講師名 | VARCHAR | 100 | ○ |  | 研修講師の名前 |
| start_date | 開始日 | DATE |  | ○ |  | 研修開始日 |
| end_date | 終了日 | DATE |  | ○ |  | 研修終了日（単日の場合は開始日と同じ） |
| duration_hours | 研修時間 | DECIMAL | 5,1 | ○ |  | 研修の総時間数 |
| location | 開催場所 | VARCHAR | 200 | ○ |  | 研修開催場所（オンラインの場合は「オンライン」） |
| cost | 費用 | DECIMAL | 10,2 | ○ |  | 研修参加費用（円） |
| cost_covered_by | 費用負担者 | ENUM |  | ○ |  | 費用の負担者（COMPANY:会社、EMPLOYEE:個人、SHARED:折半） |
| attendance_status | 出席状況 | ENUM |  | ○ | COMPLETED | 出席状況（COMPLETED:完了、PARTIAL:部分参加、ABSENT:欠席、CANCELLED:中止） |
| completion_rate | 完了率 | DECIMAL | 5,2 | ○ |  | 研修の完了率（%） |
| test_score | テスト点数 | DECIMAL | 5,2 | ○ |  | 研修テストの点数 |
| grade | 成績 | VARCHAR | 10 | ○ |  | 研修の成績（A、B、C、合格、不合格等） |
| certificate_obtained | 修了証取得 | BOOLEAN |  | ○ | False | 修了証・認定証を取得したかどうか |
| certificate_number | 証明書番号 | VARCHAR | 100 | ○ |  | 修了証・認定証の番号 |
| pdu_earned | 獲得PDU | DECIMAL | 5,1 | ○ |  | 研修で獲得した継続教育ポイント（PDU） |
| skills_acquired | 習得スキル | TEXT |  | ○ |  | 研修で習得したスキル（JSON形式） |
| learning_objectives | 学習目標 | TEXT |  | ○ |  | 研修の学習目標・目的 |
| learning_outcomes | 学習成果 | TEXT |  | ○ |  | 実際の学習成果・習得内容 |
| feedback | フィードバック | TEXT |  | ○ |  | 研修に対するフィードバック・感想 |
| satisfaction_score | 満足度 | DECIMAL | 3,1 | ○ |  | 研修に対する満足度（1.0-5.0） |
| recommendation_score | 推奨度 | DECIMAL | 3,1 | ○ |  | 他者への推奨度（1.0-5.0） |
| follow_up_required | フォローアップ要否 | BOOLEAN |  | ○ | False | 追加のフォローアップが必要かどうか |
| follow_up_date | フォローアップ予定日 | DATE |  | ○ |  | フォローアップの予定日 |
| manager_approval | 上司承認 | BOOLEAN |  | ○ | False | 上司による参加承認があったかどうか |
| approved_by | 承認者 | VARCHAR | 50 | ○ |  | 研修参加を承認した上司のID |
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  | マルチテナント識別子 |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_training_history_id | training_history_id | ○ | 研修履歴ID検索用（一意） |
| idx_employee_id | employee_id | × | 社員ID検索用 |
| idx_training_program_id | training_program_id | × | 研修プログラムID検索用 |
| idx_training_type | training_type | × | 研修種別検索用 |
| idx_training_category | training_category | × | 研修カテゴリ検索用 |
| idx_date_range | start_date, end_date | × | 期間検索用 |
| idx_attendance_status | attendance_status | × | 出席状況検索用 |
| idx_employee_period | employee_id, start_date, end_date | × | 社員別期間検索用 |
| idx_certificate | certificate_obtained, certificate_number | × | 修了証検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_training_history_employee | employee_id | MST_Employee | id | CASCADE | RESTRICT | 社員への外部キー |
| fk_training_history_program | training_program_id | MST_TrainingProgram | id | CASCADE | SET NULL | 研修プログラムへの外部キー |
| fk_training_history_approver | approved_by | MST_Employee | id | CASCADE | SET NULL | 承認者への外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_training_history_id | UNIQUE |  | 研修履歴ID一意制約 |
| chk_training_type | CHECK | training_type IN ('INTERNAL', 'EXTERNAL', 'ONLINE', 'CERTIFICATION', 'CONFERENCE') | 研修種別値チェック制約 |
| chk_training_category | CHECK | training_category IN ('TECHNICAL', 'BUSINESS', 'MANAGEMENT', 'SOFT_SKILL', 'COMPLIANCE') | 研修カテゴリ値チェック制約 |
| chk_cost_covered_by | CHECK | cost_covered_by IN ('COMPANY', 'EMPLOYEE', 'SHARED') | 費用負担者値チェック制約 |
| chk_attendance_status | CHECK | attendance_status IN ('COMPLETED', 'PARTIAL', 'ABSENT', 'CANCELLED') | 出席状況値チェック制約 |
| chk_date_range | CHECK | end_date IS NULL OR start_date <= end_date | 開始日・終了日の整合性チェック制約 |
| chk_duration_hours | CHECK | duration_hours IS NULL OR duration_hours > 0 | 研修時間正数チェック制約 |
| chk_completion_rate | CHECK | completion_rate IS NULL OR (completion_rate >= 0 AND completion_rate <= 100) | 完了率範囲チェック制約 |
| chk_test_score | CHECK | test_score IS NULL OR test_score >= 0 | テスト点数非負数チェック制約 |
| chk_satisfaction_score | CHECK | satisfaction_score IS NULL OR (satisfaction_score >= 1.0 AND satisfaction_score <= 5.0) | 満足度範囲チェック制約 |
| chk_recommendation_score | CHECK | recommendation_score IS NULL OR (recommendation_score >= 1.0 AND recommendation_score <= 5.0) | 推奨度範囲チェック制約 |
| chk_cost | CHECK | cost IS NULL OR cost >= 0 | 費用非負数チェック制約 |
| chk_pdu_earned | CHECK | pdu_earned IS NULL OR pdu_earned >= 0 | 獲得PDU非負数チェック制約 |

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

## 業務ルール

- 研修履歴IDは一意である必要がある
- 開始日は終了日以前である必要がある
- 完了率は0-100%の範囲で設定
- 満足度・推奨度は1.0-5.0の範囲で設定
- 修了証取得時は証明書番号を記録
- PDU対象研修は獲得ポイントを必須記録
- 費用が発生する研修は上司承認必須
- フォローアップ要否に応じて予定日を設定

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 研修参加履歴テーブルの詳細定義 |
