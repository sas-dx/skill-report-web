# テーブル定義書: TRN_PDU (継続教育ポイント)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | TRN_PDU |
| 論理名 | 継続教育ポイント |
| カテゴリ | トランザクション系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/TRN_PDU_details.yaml` で行ってください。


## 📝 改版履歴

> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：
> `table-details/TABLE_NAME_details.yaml`

| バージョン | 更新日 | 更新者 | 主な変更内容 |
|------------|--------|--------|-------------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 継続教育ポイントテーブルの詳細定義 |


## 📝 テーブル概要

TRN_PDU（継続教育ポイント）は、社員が取得した継続教育ポイント（Professional Development Units）を管理するトランザクションテーブルです。

主な目的：
- PDU取得履歴の記録・管理
- 資格維持要件の追跡
- 学習活動の定量化
- 継続教育計画の進捗管理
- 資格更新の支援

このテーブルにより、社員の継続的な学習活動を体系的に記録し、
資格維持や専門性向上の支援を効率的に行うことができます。


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  |  |  | マルチテナント識別子 |
| pdu_id | PDU ID | VARCHAR | 50 | ○ |  |  |  | PDU記録を一意に識別するID |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | ● |  | PDUを取得した社員のID（MST_Employeeへの外部キー） |
| certification_id | 資格ID | VARCHAR | 50 | ○ |  | ● |  | 関連する資格のID（MST_Certificationへの外部キー） |
| activity_type | 活動種別 | ENUM |  | ○ |  |  |  | PDU取得活動の種別（TRAINING:研修、CONFERENCE:カンファレンス、SEMINAR:セミナー、SELF_STUDY:自己学習、TEACHING:指導、VOLUNTEER:ボランティア、OTHER:その他） |
| activity_name | 活動名 | VARCHAR | 200 | ○ |  |  |  | PDU取得活動の名称 |
| activity_description | 活動説明 | TEXT |  | ○ |  |  |  | 活動の詳細説明・内容 |
| provider_name | 提供機関名 | VARCHAR | 100 | ○ |  |  |  | 活動を提供する機関・組織名 |
| activity_date | 活動日 | DATE |  | ○ |  |  |  | PDU取得活動を実施した日 |
| start_time | 開始時刻 | TIME |  | ○ |  |  |  | 活動開始時刻 |
| end_time | 終了時刻 | TIME |  | ○ |  |  |  | 活動終了時刻 |
| duration_hours | 活動時間 | DECIMAL | 5,1 | ○ |  |  |  | 活動の総時間数 |
| pdu_points | PDUポイント | DECIMAL | 5,1 | ○ |  |  |  | 取得したPDUポイント数 |
| pdu_category | PDUカテゴリ | ENUM |  | ○ |  |  |  | PDUのカテゴリ（TECHNICAL:技術、LEADERSHIP:リーダーシップ、STRATEGIC:戦略、BUSINESS:ビジネス） |
| pdu_subcategory | PDUサブカテゴリ | VARCHAR | 50 | ○ |  |  |  | PDUの詳細カテゴリ |
| location | 開催場所 | VARCHAR | 200 | ○ |  |  |  | 活動実施場所 |
| cost | 費用 | DECIMAL | 10,2 | ○ |  |  |  | 活動参加費用（円） |
| cost_covered_by | 費用負担者 | ENUM |  | ○ |  |  |  | 費用の負担者（COMPANY:会社、EMPLOYEE:個人、SHARED:折半） |
| evidence_type | 証跡種別 | ENUM |  | ○ |  |  |  | PDU取得の証跡種別（CERTIFICATE:修了証、ATTENDANCE:出席証明、RECEIPT:領収書、REPORT:レポート、OTHER:その他） |
| evidence_file_path | 証跡ファイルパス | VARCHAR | 500 | ○ |  |  |  | 証跡ファイルの保存パス |
| certificate_number | 証明書番号 | VARCHAR | 100 | ○ |  |  |  | 修了証・認定証の番号 |
| instructor_name | 講師名 | VARCHAR | 100 | ○ |  |  |  | 講師・指導者の名前 |
| learning_objectives | 学習目標 | TEXT |  | ○ |  |  |  | 活動の学習目標・目的 |
| learning_outcomes | 学習成果 | TEXT |  | ○ |  |  |  | 実際の学習成果・習得内容 |
| skills_developed | 向上スキル | TEXT |  | ○ |  |  |  | 活動により向上したスキル（JSON形式） |
| approval_status | 承認状況 | ENUM |  | ○ |  |  | PENDING | PDU承認状況（PENDING:承認待ち、APPROVED:承認済み、REJECTED:却下、UNDER_REVIEW:審査中） |
| approved_by | 承認者 | VARCHAR | 50 | ○ |  | ● |  | PDUを承認した担当者のID |
| approval_date | 承認日 | DATE |  | ○ |  |  |  | PDU承認日 |
| approval_comment | 承認コメント | TEXT |  | ○ |  |  |  | 承認・却下時のコメント |
| expiry_date | 有効期限 | DATE |  | ○ |  |  |  | PDUの有効期限 |
| is_recurring | 定期活動フラグ | BOOLEAN |  | ○ |  |  |  | 定期的に実施される活動かどうか |
| recurrence_pattern | 繰り返しパターン | VARCHAR | 50 | ○ |  |  |  | 定期活動の繰り返しパターン（WEEKLY、MONTHLY等） |
| related_training_id | 関連研修ID | VARCHAR | 50 | ○ |  | ● |  | 関連する研修履歴のID（TRN_TrainingHistoryへの外部キー） |
| related_project_id | 関連案件ID | VARCHAR | 50 | ○ |  | ● |  | 関連するプロジェクトのID（TRN_ProjectRecordへの外部キー） |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_pdu_id | pdu_id | ○ | PDU ID検索用（一意） |
| idx_employee_id | employee_id | × | 社員ID検索用 |
| idx_certification_id | certification_id | × | 資格ID検索用 |
| idx_activity_type | activity_type | × | 活動種別検索用 |
| idx_activity_date | activity_date | × | 活動日検索用 |
| idx_pdu_category | pdu_category | × | PDUカテゴリ検索用 |
| idx_approval_status | approval_status | × | 承認状況検索用 |
| idx_employee_period | employee_id, activity_date | × | 社員別期間検索用 |
| idx_expiry_date | expiry_date | × | 有効期限検索用 |
| idx_certification_employee | certification_id, employee_id, approval_status | × | 資格別社員PDU検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_pdu_id | UNIQUE | pdu_id |  | PDU ID一意制約 |
| chk_activity_type | CHECK |  | activity_type IN ('TRAINING', 'CONFERENCE', 'SEMINAR', 'SELF_STUDY', 'TEACHING', 'VOLUNTEER', 'OTHER') | 活動種別値チェック制約 |
| chk_pdu_category | CHECK |  | pdu_category IN ('TECHNICAL', 'LEADERSHIP', 'STRATEGIC', 'BUSINESS') | PDUカテゴリ値チェック制約 |
| chk_cost_covered_by | CHECK |  | cost_covered_by IN ('COMPANY', 'EMPLOYEE', 'SHARED') | 費用負担者値チェック制約 |
| chk_evidence_type | CHECK |  | evidence_type IN ('CERTIFICATE', 'ATTENDANCE', 'RECEIPT', 'REPORT', 'OTHER') | 証跡種別値チェック制約 |
| chk_approval_status | CHECK |  | approval_status IN ('PENDING', 'APPROVED', 'REJECTED', 'UNDER_REVIEW') | 承認状況値チェック制約 |
| chk_duration_hours | CHECK |  | duration_hours > 0 | 活動時間正数チェック制約 |
| chk_pdu_points | CHECK |  | pdu_points > 0 | PDUポイント正数チェック制約 |
| chk_cost | CHECK |  | cost IS NULL OR cost >= 0 | 費用非負数チェック制約 |
| chk_time_range | CHECK |  | start_time IS NULL OR end_time IS NULL OR start_time <= end_time | 開始・終了時刻の整合性チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_pdu_employee | employee_id | MST_Employee | id | CASCADE | RESTRICT | 社員への外部キー |
| fk_pdu_certification | certification_id | MST_Certification | id | CASCADE | SET NULL | 資格への外部キー |
| fk_pdu_approver | approved_by | MST_Employee | id | CASCADE | SET NULL | 承認者への外部キー |
| fk_pdu_training | related_training_id | TRN_TrainingHistory | training_history_id | CASCADE | SET NULL | 関連研修への外部キー |
| fk_pdu_project | related_project_id | TRN_ProjectRecord | project_record_id | CASCADE | SET NULL | 関連案件への外部キー |

## 📊 サンプルデータ

```json
[
  {
    "pdu_id": "PDU_001",
    "employee_id": "EMP000001",
    "certification_id": "CERT_PMP_001",
    "activity_type": "TRAINING",
    "activity_name": "アジャイル開発手法研修",
    "activity_description": "スクラム・カンバンを中心としたアジャイル開発手法の実践研修",
    "provider_name": "アジャイル協会",
    "activity_date": "2024-03-15",
    "start_time": "09:00:00",
    "end_time": "17:00:00",
    "duration_hours": 8.0,
    "pdu_points": 8.0,
    "pdu_category": "TECHNICAL",
    "pdu_subcategory": "Development Methods",
    "location": "東京研修センター",
    "cost": 50000,
    "cost_covered_by": "COMPANY",
    "evidence_type": "CERTIFICATE",
    "evidence_file_path": "/evidence/pdu/PDU_001_certificate.pdf",
    "certificate_number": "AGILE-2024-001",
    "instructor_name": "山田講師",
    "learning_objectives": "アジャイル開発手法の理解と実践スキル習得",
    "learning_outcomes": "スクラム・カンバンの基礎理解、実際のプロジェクトへの適用方法を習得",
    "skills_developed": "[\"アジャイル開発\", \"スクラム\", \"カンバン\", \"チーム運営\"]",
    "approval_status": "APPROVED",
    "approved_by": "EMP000020",
    "approval_date": "2024-03-20",
    "approval_comment": "PMP資格維持に適切なPDU活動として承認",
    "expiry_date": "2027-03-15",
    "is_recurring": false,
    "recurrence_pattern": null,
    "related_training_id": "TRN_HIS_003",
    "related_project_id": null
  },
  {
    "pdu_id": "PDU_002",
    "employee_id": "EMP000002",
    "certification_id": "CERT_AWS_001",
    "activity_type": "CONFERENCE",
    "activity_name": "AWS re:Invent 2024",
    "activity_description": "AWSの最新技術動向とベストプラクティスに関するカンファレンス",
    "provider_name": "Amazon Web Services",
    "activity_date": "2024-11-28",
    "start_time": null,
    "end_time": null,
    "duration_hours": 32.0,
    "pdu_points": 32.0,
    "pdu_category": "TECHNICAL",
    "pdu_subcategory": "Cloud Technologies",
    "location": "ラスベガス（オンライン参加）",
    "cost": 200000,
    "cost_covered_by": "COMPANY",
    "evidence_type": "ATTENDANCE",
    "evidence_file_path": "/evidence/pdu/PDU_002_attendance.pdf",
    "certificate_number": null,
    "instructor_name": null,
    "learning_objectives": "AWS最新技術の習得とクラウドアーキテクチャスキル向上",
    "learning_outcomes": "最新のAWSサービス理解、セキュリティベストプラクティス習得",
    "skills_developed": "[\"AWS最新技術\", \"クラウドセキュリティ\", \"サーバーレス\", \"機械学習\"]",
    "approval_status": "APPROVED",
    "approved_by": "EMP000020",
    "approval_date": "2024-12-05",
    "approval_comment": "AWS認定維持に有効なPDU活動として承認",
    "expiry_date": "2027-11-28",
    "is_recurring": false,
    "recurrence_pattern": null,
    "related_training_id": null,
    "related_project_id": "PRJ_REC_002"
  }
]
```

## 📌 特記事項

- PDUポイントは活動時間と内容に基づいて算出
- 証跡ファイルは必須（承認の根拠として使用）
- 有効期限は資格の更新サイクルに基づいて設定
- 承認プロセスは資格維持の要件確認に重要
- 関連研修・案件との紐付けで学習の一貫性を管理
- 定期活動は継続的な学習習慣の支援に活用

## 📋 業務ルール

- PDU IDは一意である必要がある
- 活動時間とPDUポイントは正数である必要がある
- 承認済みPDUのみが資格維持に有効
- 証跡ファイルは承認の必須条件
- 有効期限内のPDUのみが資格更新に使用可能
- 同一活動での重複PDU取得は不可
- 費用が発生する活動は事前承認推奨
- 定期活動は繰り返しパターンを明確に設定
