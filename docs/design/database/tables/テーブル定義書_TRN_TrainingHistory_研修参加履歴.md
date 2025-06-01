# テーブル定義書: TRN_TrainingHistory (研修参加履歴)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | TRN_TrainingHistory |
| 論理名 | 研修参加履歴 |
| カテゴリ | トランザクション系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/TRN_TrainingHistory_details.yaml` で行ってください。


## 📝 改版履歴

> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：
> `table-details/TABLE_NAME_details.yaml`

| バージョン | 更新日 | 更新者 | 主な変更内容 |
|------------|--------|--------|-------------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 研修参加履歴テーブルの詳細定義 |


## 📝 テーブル概要

TRN_TrainingHistory（研修参加履歴）は、社員が参加した研修・教育プログラムの履歴を管理するトランザクションテーブルです。

主な目的：
- 研修参加履歴の記録・管理
- 学習成果・評価の記録
- スキル向上の追跡
- 継続教育ポイント（PDU）の管理
- 人材育成計画の進捗管理

このテーブルにより、社員の学習履歴を体系的に記録し、
スキル開発やキャリア形成の支援を効率的に行うことができます。


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  |  |  | マルチテナント識別子 |
| training_history_id | 研修履歴ID | VARCHAR | 50 | ○ |  |  |  | 研修参加履歴を一意に識別するID |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | ● |  | 参加した社員のID（MST_Employeeへの外部キー） |
| training_program_id | 研修プログラムID | VARCHAR | 50 | ○ |  | ● |  | 研修プログラムのID（MST_TrainingProgramへの外部キー） |
| training_name | 研修名 | VARCHAR | 200 | ○ |  |  |  | 研修・教育プログラムの名称 |
| training_type | 研修種別 | ENUM |  | ○ |  |  |  | 研修の種別（INTERNAL:社内研修、EXTERNAL:社外研修、ONLINE:オンライン、CERTIFICATION:資格取得、CONFERENCE:カンファレンス） |
| training_category | 研修カテゴリ | ENUM |  | ○ |  |  |  | 研修の分野（TECHNICAL:技術、BUSINESS:ビジネス、MANAGEMENT:マネジメント、SOFT_SKILL:ソフトスキル、COMPLIANCE:コンプライアンス） |
| provider_name | 提供機関名 | VARCHAR | 100 | ○ |  |  |  | 研修を提供する機関・会社名 |
| instructor_name | 講師名 | VARCHAR | 100 | ○ |  |  |  | 研修講師の名前 |
| start_date | 開始日 | DATE |  | ○ |  |  |  | 研修開始日 |
| end_date | 終了日 | DATE |  | ○ |  |  |  | 研修終了日（単日の場合は開始日と同じ） |
| duration_hours | 研修時間 | DECIMAL | 5,1 | ○ |  |  |  | 研修の総時間数 |
| location | 開催場所 | VARCHAR | 200 | ○ |  |  |  | 研修開催場所（オンラインの場合は「オンライン」） |
| cost | 費用 | DECIMAL | 10,2 | ○ |  |  |  | 研修参加費用（円） |
| cost_covered_by | 費用負担者 | ENUM |  | ○ |  |  |  | 費用の負担者（COMPANY:会社、EMPLOYEE:個人、SHARED:折半） |
| attendance_status | 出席状況 | ENUM |  | ○ |  |  | COMPLETED | 出席状況（COMPLETED:完了、PARTIAL:部分参加、ABSENT:欠席、CANCELLED:中止） |
| completion_rate | 完了率 | DECIMAL | 5,2 | ○ |  |  |  | 研修の完了率（%） |
| test_score | テスト点数 | DECIMAL | 5,2 | ○ |  |  |  | 研修テストの点数 |
| grade | 成績 | VARCHAR | 10 | ○ |  |  |  | 研修の成績（A、B、C、合格、不合格等） |
| certificate_obtained | 修了証取得 | BOOLEAN |  | ○ |  |  |  | 修了証・認定証を取得したかどうか |
| certificate_number | 証明書番号 | VARCHAR | 100 | ○ |  |  |  | 修了証・認定証の番号 |
| pdu_earned | 獲得PDU | DECIMAL | 5,1 | ○ |  |  |  | 研修で獲得した継続教育ポイント（PDU） |
| skills_acquired | 習得スキル | TEXT |  | ○ |  |  |  | 研修で習得したスキル（JSON形式） |
| learning_objectives | 学習目標 | TEXT |  | ○ |  |  |  | 研修の学習目標・目的 |
| learning_outcomes | 学習成果 | TEXT |  | ○ |  |  |  | 実際の学習成果・習得内容 |
| feedback | フィードバック | TEXT |  | ○ |  |  |  | 研修に対するフィードバック・感想 |
| satisfaction_score | 満足度 | DECIMAL | 3,1 | ○ |  |  |  | 研修に対する満足度（1.0-5.0） |
| recommendation_score | 推奨度 | DECIMAL | 3,1 | ○ |  |  |  | 他者への推奨度（1.0-5.0） |
| follow_up_required | フォローアップ要否 | BOOLEAN |  | ○ |  |  |  | 追加のフォローアップが必要かどうか |
| follow_up_date | フォローアップ予定日 | DATE |  | ○ |  |  |  | フォローアップの予定日 |
| manager_approval | 上司承認 | BOOLEAN |  | ○ |  |  |  | 上司による参加承認があったかどうか |
| approved_by | 承認者 | VARCHAR | 50 | ○ |  | ● |  | 研修参加を承認した上司のID |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

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

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_training_history_id | UNIQUE | training_history_id |  | 研修履歴ID一意制約 |
| chk_training_type | CHECK |  | training_type IN ('INTERNAL', 'EXTERNAL', 'ONLINE', 'CERTIFICATION', 'CONFERENCE') | 研修種別値チェック制約 |
| chk_training_category | CHECK |  | training_category IN ('TECHNICAL', 'BUSINESS', 'MANAGEMENT', 'SOFT_SKILL', 'COMPLIANCE') | 研修カテゴリ値チェック制約 |
| chk_cost_covered_by | CHECK |  | cost_covered_by IN ('COMPANY', 'EMPLOYEE', 'SHARED') | 費用負担者値チェック制約 |
| chk_attendance_status | CHECK |  | attendance_status IN ('COMPLETED', 'PARTIAL', 'ABSENT', 'CANCELLED') | 出席状況値チェック制約 |
| chk_date_range | CHECK |  | end_date IS NULL OR start_date <= end_date | 開始日・終了日の整合性チェック制約 |
| chk_duration_hours | CHECK |  | duration_hours IS NULL OR duration_hours > 0 | 研修時間正数チェック制約 |
| chk_completion_rate | CHECK |  | completion_rate IS NULL OR (completion_rate >= 0 AND completion_rate <= 100) | 完了率範囲チェック制約 |
| chk_test_score | CHECK |  | test_score IS NULL OR test_score >= 0 | テスト点数非負数チェック制約 |
| chk_satisfaction_score | CHECK |  | satisfaction_score IS NULL OR (satisfaction_score >= 1.0 AND satisfaction_score <= 5.0) | 満足度範囲チェック制約 |
| chk_recommendation_score | CHECK |  | recommendation_score IS NULL OR (recommendation_score >= 1.0 AND recommendation_score <= 5.0) | 推奨度範囲チェック制約 |
| chk_cost | CHECK |  | cost IS NULL OR cost >= 0 | 費用非負数チェック制約 |
| chk_pdu_earned | CHECK |  | pdu_earned IS NULL OR pdu_earned >= 0 | 獲得PDU非負数チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_training_history_employee | employee_id | MST_Employee | id | CASCADE | RESTRICT | 社員への外部キー |
| fk_training_history_program | training_program_id | MST_TrainingProgram | id | CASCADE | SET NULL | 研修プログラムへの外部キー |
| fk_training_history_approver | approved_by | MST_Employee | id | CASCADE | SET NULL | 承認者への外部キー |

## 📊 サンプルデータ

```json
[
  {
    "training_history_id": "TRN_HIS_001",
    "employee_id": "EMP000001",
    "training_program_id": "TRN_PROG_001",
    "training_name": "AWS認定ソリューションアーキテクト研修",
    "training_type": "EXTERNAL",
    "training_category": "TECHNICAL",
    "provider_name": "AWS Training",
    "instructor_name": "田中講師",
    "start_date": "2024-03-01",
    "end_date": "2024-03-03",
    "duration_hours": 24.0,
    "location": "東京研修センター",
    "cost": 150000,
    "cost_covered_by": "COMPANY",
    "attendance_status": "COMPLETED",
    "completion_rate": 100.0,
    "test_score": 85.0,
    "grade": "合格",
    "certificate_obtained": true,
    "certificate_number": "AWS-SAA-2024-001",
    "pdu_earned": 24.0,
    "skills_acquired": "[\"AWS設計\", \"クラウドアーキテクチャ\", \"セキュリティ設計\"]",
    "learning_objectives": "AWSでのソリューション設計スキル習得",
    "learning_outcomes": "クラウドアーキテクチャ設計の基礎を習得、実践的な設計手法を学習",
    "feedback": "実践的な内容で非常に有用だった。講師の説明も分かりやすい。",
    "satisfaction_score": 4.5,
    "recommendation_score": 5.0,
    "follow_up_required": true,
    "follow_up_date": "2024-06-01",
    "manager_approval": true,
    "approved_by": "EMP000010"
  },
  {
    "training_history_id": "TRN_HIS_002",
    "employee_id": "EMP000002",
    "training_program_id": null,
    "training_name": "プロジェクトマネジメント基礎",
    "training_type": "ONLINE",
    "training_category": "MANAGEMENT",
    "provider_name": "社内研修センター",
    "instructor_name": "佐藤部長",
    "start_date": "2024-02-15",
    "end_date": "2024-02-15",
    "duration_hours": 8.0,
    "location": "オンライン",
    "cost": 0,
    "cost_covered_by": "COMPANY",
    "attendance_status": "COMPLETED",
    "completion_rate": 100.0,
    "test_score": 92.0,
    "grade": "A",
    "certificate_obtained": true,
    "certificate_number": "PM-BASIC-2024-002",
    "pdu_earned": 8.0,
    "skills_acquired": "[\"プロジェクト計画\", \"リスク管理\", \"チームマネジメント\"]",
    "learning_objectives": "プロジェクトマネジメントの基礎知識習得",
    "learning_outcomes": "PMBOKの基礎理解、実際のプロジェクト運営に活用可能な知識を習得",
    "feedback": "基礎から体系的に学べて良かった。実例が豊富で理解しやすい。",
    "satisfaction_score": 4.0,
    "recommendation_score": 4.0,
    "follow_up_required": false,
    "follow_up_date": null,
    "manager_approval": true,
    "approved_by": "EMP000010"
  }
]
```

## 📌 特記事項

- 習得スキルはJSON形式で柔軟に管理
- PDU（継続教育ポイント）は資格維持に重要
- 修了証番号は資格証明に使用
- 満足度・推奨度は研修品質向上に活用
- フォローアップは学習効果の定着に重要
- 上司承認は研修参加の正当性を担保

## 📋 業務ルール

- 研修履歴IDは一意である必要がある
- 開始日は終了日以前である必要がある
- 完了率は0-100%の範囲で設定
- 満足度・推奨度は1.0-5.0の範囲で設定
- 修了証取得時は証明書番号を記録
- PDU対象研修は獲得ポイントを必須記録
- 費用が発生する研修は上司承認必須
- フォローアップ要否に応じて予定日を設定
