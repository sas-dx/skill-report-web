# テーブル定義書: TRN_PDU

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_PDU |
| 論理名 | 継続教育ポイント |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-21 17:20:35 |

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
| pdu_id |  | VARCHAR |  | ○ |  |  |
| employee_id |  | VARCHAR |  | ○ |  |  |
| certification_id |  | VARCHAR |  | ○ |  |  |
| activity_type |  | ENUM |  | ○ |  |  |
| activity_name |  | VARCHAR |  | ○ |  |  |
| activity_description |  | TEXT |  | ○ |  |  |
| provider_name |  | VARCHAR |  | ○ |  |  |
| activity_date |  | DATE |  | ○ |  |  |
| start_time |  | TIME |  | ○ |  |  |
| end_time |  | TIME |  | ○ |  |  |
| duration_hours |  | DECIMAL |  | ○ |  |  |
| pdu_points |  | DECIMAL |  | ○ |  |  |
| pdu_category |  | ENUM |  | ○ |  |  |
| pdu_subcategory |  | VARCHAR |  | ○ |  |  |
| location |  | VARCHAR |  | ○ |  |  |
| cost |  | DECIMAL |  | ○ |  |  |
| cost_covered_by |  | ENUM |  | ○ |  |  |
| evidence_type |  | ENUM |  | ○ |  |  |
| evidence_file_path |  | VARCHAR |  | ○ |  |  |
| certificate_number |  | VARCHAR |  | ○ |  |  |
| instructor_name |  | VARCHAR |  | ○ |  |  |
| learning_objectives |  | TEXT |  | ○ |  |  |
| learning_outcomes |  | TEXT |  | ○ |  |  |
| skills_developed |  | TEXT |  | ○ |  |  |
| approval_status |  | ENUM |  | ○ | PENDING |  |
| approved_by |  | VARCHAR |  | ○ |  |  |
| approval_date |  | DATE |  | ○ |  |  |
| approval_comment |  | TEXT |  | ○ |  |  |
| expiry_date |  | DATE |  | ○ |  |  |
| is_recurring |  | BOOLEAN |  | ○ | False |  |
| recurrence_pattern |  | VARCHAR |  | ○ |  |  |
| related_training_id |  | VARCHAR |  | ○ |  |  |
| related_project_id |  | VARCHAR |  | ○ |  |  |
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_by | レコード作成者のユーザーID | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | レコード更新者のユーザーID | VARCHAR | 50 | × |  | レコード更新者のユーザーID |
| created_at | レコード作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | レコード更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_pdu_id | pdu_id | ○ |  |
| idx_employee_id | employee_id | × |  |
| idx_certification_id | certification_id | × |  |
| idx_activity_type | activity_type | × |  |
| idx_activity_date | activity_date | × |  |
| idx_pdu_category | pdu_category | × |  |
| idx_approval_status | approval_status | × |  |
| idx_employee_period | employee_id, activity_date | × |  |
| idx_expiry_date | expiry_date | × |  |
| idx_certification_employee | certification_id, employee_id, approval_status | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_trn_pdu | PRIMARY KEY | id | 主キー制約 |
| uk_pdu_id | UNIQUE |  | pdu_id一意制約 |
| chk_activity_type | CHECK | activity_type IN (...) | activity_type値チェック制約 |
| chk_evidence_type | CHECK | evidence_type IN (...) | evidence_type値チェック制約 |
| chk_approval_status | CHECK | approval_status IN (...) | approval_status値チェック制約 |

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