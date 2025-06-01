# テーブル定義書: TRN_PDU

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_PDU |
| 論理名 | 継続教育ポイント |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-01 20:40:26 |

## 概要

TRN_PDU（継続教育ポイント）は、社員が取得した継続教育ポイント（Professional Development Units）を管理するトランザクションテーブルです。

主な目的：
- PDU取得履歴の記録・管理
- 資格維持要件の追跡
- 学習活動の定量化
- 継続教育計画の進捗管理
- 資格更新の支援

このテーブルにより、社員の継続的な学習活動を体系的に記録し、
資格維持や専門性向上の支援を効率的に行うことができます。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  | マルチテナント識別子 |
| pdu_id | PDU ID | VARCHAR | 50 | ○ |  | PDU記録を一意に識別するID |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | PDUを取得した社員のID（MST_Employeeへの外部キー） |
| certification_id | 資格ID | VARCHAR | 50 | ○ |  | 関連する資格のID（MST_Certificationへの外部キー） |
| activity_type | 活動種別 | ENUM |  | ○ |  | PDU取得活動の種別（TRAINING:研修、CONFERENCE:カンファレンス、SEMINAR:セミナー、SELF_STUDY:自己学習、TEACHING:指導、VOLUNTEER:ボランティア、OTHER:その他） |
| activity_name | 活動名 | VARCHAR | 200 | ○ |  | PDU取得活動の名称 |
| activity_description | 活動説明 | TEXT |  | ○ |  | 活動の詳細説明・内容 |
| provider_name | 提供機関名 | VARCHAR | 100 | ○ |  | 活動を提供する機関・組織名 |
| activity_date | 活動日 | DATE |  | ○ |  | PDU取得活動を実施した日 |
| start_time | 開始時刻 | TIME |  | ○ |  | 活動開始時刻 |
| end_time | 終了時刻 | TIME |  | ○ |  | 活動終了時刻 |
| duration_hours | 活動時間 | DECIMAL | 5,1 | ○ |  | 活動の総時間数 |
| pdu_points | PDUポイント | DECIMAL | 5,1 | ○ |  | 取得したPDUポイント数 |
| pdu_category | PDUカテゴリ | ENUM |  | ○ |  | PDUのカテゴリ（TECHNICAL:技術、LEADERSHIP:リーダーシップ、STRATEGIC:戦略、BUSINESS:ビジネス） |
| pdu_subcategory | PDUサブカテゴリ | VARCHAR | 50 | ○ |  | PDUの詳細カテゴリ |
| location | 開催場所 | VARCHAR | 200 | ○ |  | 活動実施場所 |
| cost | 費用 | DECIMAL | 10,2 | ○ |  | 活動参加費用（円） |
| cost_covered_by | 費用負担者 | ENUM |  | ○ |  | 費用の負担者（COMPANY:会社、EMPLOYEE:個人、SHARED:折半） |
| evidence_type | 証跡種別 | ENUM |  | ○ |  | PDU取得の証跡種別（CERTIFICATE:修了証、ATTENDANCE:出席証明、RECEIPT:領収書、REPORT:レポート、OTHER:その他） |
| evidence_file_path | 証跡ファイルパス | VARCHAR | 500 | ○ |  | 証跡ファイルの保存パス |
| certificate_number | 証明書番号 | VARCHAR | 100 | ○ |  | 修了証・認定証の番号 |
| instructor_name | 講師名 | VARCHAR | 100 | ○ |  | 講師・指導者の名前 |
| learning_objectives | 学習目標 | TEXT |  | ○ |  | 活動の学習目標・目的 |
| learning_outcomes | 学習成果 | TEXT |  | ○ |  | 実際の学習成果・習得内容 |
| skills_developed | 向上スキル | TEXT |  | ○ |  | 活動により向上したスキル（JSON形式） |
| approval_status | 承認状況 | ENUM |  | ○ | PENDING | PDU承認状況（PENDING:承認待ち、APPROVED:承認済み、REJECTED:却下、UNDER_REVIEW:審査中） |
| approved_by | 承認者 | VARCHAR | 50 | ○ |  | PDUを承認した担当者のID |
| approval_date | 承認日 | DATE |  | ○ |  | PDU承認日 |
| approval_comment | 承認コメント | TEXT |  | ○ |  | 承認・却下時のコメント |
| expiry_date | 有効期限 | DATE |  | ○ |  | PDUの有効期限 |
| is_recurring | 定期活動フラグ | BOOLEAN |  | ○ | False | 定期的に実施される活動かどうか |
| recurrence_pattern | 繰り返しパターン | VARCHAR | 50 | ○ |  | 定期活動の繰り返しパターン（WEEKLY、MONTHLY等） |
| related_training_id | 関連研修ID | VARCHAR | 50 | ○ |  | 関連する研修履歴のID（TRN_TrainingHistoryへの外部キー） |
| related_project_id | 関連案件ID | VARCHAR | 50 | ○ |  | 関連するプロジェクトのID（TRN_ProjectRecordへの外部キー） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

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

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_pdu_employee | employee_id | MST_Employee | id | CASCADE | RESTRICT | 社員への外部キー |
| fk_pdu_certification | certification_id | MST_Certification | id | CASCADE | SET NULL | 資格への外部キー |
| fk_pdu_approver | approved_by | MST_Employee | id | CASCADE | SET NULL | 承認者への外部キー |
| fk_pdu_training | related_training_id | TRN_TrainingHistory | training_history_id | CASCADE | SET NULL | 関連研修への外部キー |
| fk_pdu_project | related_project_id | TRN_ProjectRecord | project_record_id | CASCADE | SET NULL | 関連案件への外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_pdu_id | UNIQUE |  | PDU ID一意制約 |
| chk_activity_type | CHECK | activity_type IN ('TRAINING', 'CONFERENCE', 'SEMINAR', 'SELF_STUDY', 'TEACHING', 'VOLUNTEER', 'OTHER') | 活動種別値チェック制約 |
| chk_pdu_category | CHECK | pdu_category IN ('TECHNICAL', 'LEADERSHIP', 'STRATEGIC', 'BUSINESS') | PDUカテゴリ値チェック制約 |
| chk_cost_covered_by | CHECK | cost_covered_by IN ('COMPANY', 'EMPLOYEE', 'SHARED') | 費用負担者値チェック制約 |
| chk_evidence_type | CHECK | evidence_type IN ('CERTIFICATE', 'ATTENDANCE', 'RECEIPT', 'REPORT', 'OTHER') | 証跡種別値チェック制約 |
| chk_approval_status | CHECK | approval_status IN ('PENDING', 'APPROVED', 'REJECTED', 'UNDER_REVIEW') | 承認状況値チェック制約 |
| chk_duration_hours | CHECK | duration_hours > 0 | 活動時間正数チェック制約 |
| chk_pdu_points | CHECK | pdu_points > 0 | PDUポイント正数チェック制約 |
| chk_cost | CHECK | cost IS NULL OR cost >= 0 | 費用非負数チェック制約 |
| chk_time_range | CHECK | start_time IS NULL OR end_time IS NULL OR start_time <= end_time | 開始・終了時刻の整合性チェック制約 |

## サンプルデータ

| pdu_id | employee_id | certification_id | activity_type | activity_name | activity_description | provider_name | activity_date | start_time | end_time | duration_hours | pdu_points | pdu_category | pdu_subcategory | location | cost | cost_covered_by | evidence_type | evidence_file_path | certificate_number | instructor_name | learning_objectives | learning_outcomes | skills_developed | approval_status | approved_by | approval_date | approval_comment | expiry_date | is_recurring | recurrence_pattern | related_training_id | related_project_id |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| PDU_001 | EMP000001 | CERT_PMP_001 | TRAINING | アジャイル開発手法研修 | スクラム・カンバンを中心としたアジャイル開発手法の実践研修 | アジャイル協会 | 2024-03-15 | 09:00:00 | 17:00:00 | 8.0 | 8.0 | TECHNICAL | Development Methods | 東京研修センター | 50000 | COMPANY | CERTIFICATE | /evidence/pdu/PDU_001_certificate.pdf | AGILE-2024-001 | 山田講師 | アジャイル開発手法の理解と実践スキル習得 | スクラム・カンバンの基礎理解、実際のプロジェクトへの適用方法を習得 | ["アジャイル開発", "スクラム", "カンバン", "チーム運営"] | APPROVED | EMP000020 | 2024-03-20 | PMP資格維持に適切なPDU活動として承認 | 2027-03-15 | False | None | TRN_HIS_003 | None |
| PDU_002 | EMP000002 | CERT_AWS_001 | CONFERENCE | AWS re:Invent 2024 | AWSの最新技術動向とベストプラクティスに関するカンファレンス | Amazon Web Services | 2024-11-28 | None | None | 32.0 | 32.0 | TECHNICAL | Cloud Technologies | ラスベガス（オンライン参加） | 200000 | COMPANY | ATTENDANCE | /evidence/pdu/PDU_002_attendance.pdf | None | None | AWS最新技術の習得とクラウドアーキテクチャスキル向上 | 最新のAWSサービス理解、セキュリティベストプラクティス習得 | ["AWS最新技術", "クラウドセキュリティ", "サーバーレス", "機械学習"] | APPROVED | EMP000020 | 2024-12-05 | AWS認定維持に有効なPDU活動として承認 | 2027-11-28 | False | None | None | PRJ_REC_002 |

## 特記事項

- PDUポイントは活動時間と内容に基づいて算出
- 証跡ファイルは必須（承認の根拠として使用）
- 有効期限は資格の更新サイクルに基づいて設定
- 承認プロセスは資格維持の要件確認に重要
- 関連研修・案件との紐付けで学習の一貫性を管理
- 定期活動は継続的な学習習慣の支援に活用

## 業務ルール

- PDU IDは一意である必要がある
- 活動時間とPDUポイントは正数である必要がある
- 承認済みPDUのみが資格維持に有効
- 証跡ファイルは承認の必須条件
- 有効期限内のPDUのみが資格更新に使用可能
- 同一活動での重複PDU取得は不可
- 費用が発生する活動は事前承認推奨
- 定期活動は繰り返しパターンを明確に設定

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 継続教育ポイントテーブルの詳細定義 |
