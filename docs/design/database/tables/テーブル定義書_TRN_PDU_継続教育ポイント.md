# テーブル定義書: TRN_PDU

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_PDU |
| 論理名 | 継続教育ポイント |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-24 23:05:57 |

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
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| activity_date | 活動日 | DATE |  | ○ |  | 活動日 |
| activity_description | 活動説明 | TEXT |  | ○ |  | 活動説明 |
| activity_name | 活動名 | VARCHAR | 200 | ○ |  | 活動名 |
| activity_type | 活動種別 | ENUM |  | ○ |  | 活動種別 |
| approval_comment | 承認コメント | TEXT |  | ○ |  | 承認コメント |
| approval_date | 承認日 | DATE |  | ○ |  | 承認日 |
| approval_status | 承認状況 | ENUM |  | ○ | PENDING | 承認状況 |
| approved_by | 承認者 | VARCHAR | 50 | ○ |  | 承認者 |
| certificate_number | 証明書番号 | VARCHAR | 100 | ○ |  | 証明書番号 |
| certification_id | 資格ID | VARCHAR | 50 | ○ |  | 資格ID |
| cost | 費用 | DECIMAL | 10,2 | ○ |  | 費用 |
| cost_covered_by | 費用負担者 | ENUM |  | ○ |  | 費用負担者 |
| duration_hours | 活動時間 | DECIMAL | 5,1 | ○ |  | 活動時間 |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 社員ID |
| end_time | 終了時刻 | TIME |  | ○ |  | 終了時刻 |
| evidence_file_path | 証跡ファイルパス | VARCHAR | 500 | ○ |  | 証跡ファイルパス |
| evidence_type | 証跡種別 | ENUM |  | ○ |  | 証跡種別 |
| expiry_date | 有効期限 | DATE |  | ○ |  | 有効期限 |
| instructor_name | 講師名 | VARCHAR | 100 | ○ |  | 講師名 |
| is_recurring | 定期活動フラグ | BOOLEAN |  | ○ | False | 定期活動フラグ |
| learning_objectives | 学習目標 | TEXT |  | ○ |  | 学習目標 |
| learning_outcomes | 学習成果 | TEXT |  | ○ |  | 学習成果 |
| location | 開催場所 | VARCHAR | 200 | ○ |  | 開催場所 |
| pdu_category | PDUカテゴリ | ENUM |  | ○ |  | PDUカテゴリ |
| pdu_id | PDU ID | VARCHAR | 50 | ○ |  | PDU ID |
| pdu_points | PDUポイント | DECIMAL | 5,1 | ○ |  | PDUポイント |
| pdu_subcategory | PDUサブカテゴリ | VARCHAR | 50 | ○ |  | PDUサブカテゴリ |
| provider_name | 提供機関名 | VARCHAR | 100 | ○ |  | 提供機関名 |
| recurrence_pattern | 繰り返しパターン | VARCHAR | 50 | ○ |  | 繰り返しパターン |
| related_project_id | 関連案件ID | VARCHAR | 50 | ○ |  | 関連案件ID |
| related_training_id | 関連研修ID | VARCHAR | 50 | ○ |  | 関連研修ID |
| skills_developed | 向上スキル | TEXT |  | ○ |  | 向上スキル |
| start_time | 開始時刻 | TIME |  | ○ |  | 開始時刻 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| created_by | 作成者ID | VARCHAR | 50 | ○ |  | 作成者ID |
| updated_by | 更新者ID | VARCHAR | 50 | ○ |  | 更新者ID |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

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
| idx_trn_pdu_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_pdu_employee | employee_id | MST_Employee | id | CASCADE | RESTRICT | 外部キー制約 |
| fk_pdu_certification | certification_id | MST_Certification | id | CASCADE | SET NULL | 外部キー制約 |
| fk_pdu_approver | approved_by | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |
| fk_pdu_training | related_training_id | TRN_TrainingHistory | id | CASCADE | SET NULL | 外部キー制約 |
| fk_pdu_project | related_project_id | TRN_ProjectRecord | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_pdu_id | UNIQUE |  | pdu_id一意制約 |
| chk_activity_type | CHECK | activity_type IN (...) | activity_type値チェック制約 |
| chk_approval_status | CHECK | approval_status IN (...) | approval_status値チェック制約 |
| chk_evidence_type | CHECK | evidence_type IN (...) | evidence_type値チェック制約 |

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
- PDU IDは一意である必要がある
- 活動時間とPDUポイントは正数である必要がある
- 承認済みPDUのみが資格維持に有効
- 証跡ファイルは承認の必須条件
- 有効期限内のPDUのみが資格更新に使用可能
- 同一活動での重複PDU取得は不可
- 費用が発生する活動は事前承認推奨
- 定期活動は繰り返しパターンを明確に設定

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 継続教育ポイントテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214007 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214908 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215001 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215054 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222632 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223433 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |