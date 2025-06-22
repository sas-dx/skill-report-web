# テーブル定義書: TRN_TrainingHistory

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_TrainingHistory |
| 論理名 | 研修参加履歴 |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-21 22:02:17 |

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
| traininghistory_id | TRN_TrainingHistoryの主キー | SERIAL |  | × |  | TRN_TrainingHistoryの主キー |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_by | レコード作成者のユーザーID | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | レコード更新者のユーザーID | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_trn_traininghistory_tenant_id | tenant_id | × | テナントID検索用インデックス |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_training_history_employee | None | None | None | CASCADE | RESTRICT | 外部キー制約 |
| fk_training_history_program | None | None | None | CASCADE | SET NULL | 外部キー制約 |
| fk_training_history_approver | None | None | None | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_trn_traininghistory | PRIMARY KEY | traininghistory_id, id | 主キー制約 |

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