# テーブル定義書_TRN_TrainingHistory_研修履歴

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | TRN_TrainingHistory |
| 論理名 | 研修履歴 |
| 用途 | 社員の研修参加履歴管理 |
| カテゴリ | トランザクション系 |
| 作成日 | 2024-12-19 |
| 最終更新日 | 2024-12-19 |

## テーブル概要

社員の研修・セミナー・勉強会などへの参加履歴を管理するトランザクションテーブルです。
研修名、期間、主催者、内容、評価、取得スキルなどの情報を記録し、
社員の教育・成長記録として活用されます。継続的な学習活動の記録と、
PDU（継続教育ポイント）の管理基盤となります。

## テーブル構造

| # | カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | PK | FK | インデックス | 説明 |
|---|----------|--------|----------|------|------|------------|----|----|--------------|------|
| 1 | training_id | 研修ID | VARCHAR | 50 | NOT NULL | - | ○ | - | PK | 研修参加記録の一意識別子 |
| 2 | tenant_id | テナントID | VARCHAR | 50 | NOT NULL | - | - | ○ | IDX | テナント識別子 |
| 3 | emp_no | 社員番号 | VARCHAR | 20 | NOT NULL | - | - | ○ | IDX | 研修参加者の社員番号 |
| 4 | program_id | プログラムID | VARCHAR | 50 | NULL | - | - | ○ | IDX | 研修プログラムID |
| 5 | training_name | 研修名 | VARCHAR | 200 | NOT NULL | - | - | - | IDX | 研修・セミナー・勉強会の名称 |
| 6 | training_type | 研修種別 | VARCHAR | 50 | NOT NULL | - | - | - | IDX | 研修の種別 |
| 7 | start_date | 開始日 | DATE | - | NOT NULL | - | - | - | IDX | 研修の開始日 |
| 8 | end_date | 終了日 | DATE | - | NULL | - | - | - | IDX | 研修の終了日 |
| 9 | hours | 時間数 | DECIMAL | 4,1 | NULL | - | - | - | - | 研修の時間数 |
| 10 | organizer | 主催者 | VARCHAR | 100 | NULL | - | - | - | - | 研修の主催者・提供元 |
| 11 | location | 開催場所 | VARCHAR | 200 | NULL | - | - | - | - | 研修の開催場所 |
| 12 | description | 研修内容 | TEXT | - | NULL | - | - | - | - | 研修の内容・カリキュラム |
| 13 | acquired_skill_id1 | 取得スキルID1 | VARCHAR | 50 | NULL | - | - | ○ | IDX | 研修で取得したスキルID1 |
| 14 | acquired_skill_id2 | 取得スキルID2 | VARCHAR | 50 | NULL | - | - | ○ | IDX | 研修で取得したスキルID2 |
| 15 | acquired_skill_id3 | 取得スキルID3 | VARCHAR | 50 | NULL | - | - | ○ | IDX | 研修で取得したスキルID3 |
| 16 | related_cert_id | 関連資格ID | VARCHAR | 50 | NULL | - | - | ○ | IDX | 研修に関連する資格ID |
| 17 | cost | 受講料 | DECIMAL | 10,2 | NULL | - | - | - | - | 研修の受講料 |
| 18 | currency_code | 通貨コード | VARCHAR | 3 | NOT NULL | 'JPY' | - | - | - | 通貨コード（ISO 4217） |
| 19 | cost_bearer | 費用負担 | VARCHAR | 50 | NOT NULL | '会社' | - | - | - | 費用負担者 |
| 20 | pdu_points | PDUポイント | INTEGER | - | NULL | - | - | - | - | 取得したPDU |
| 21 | certificate_no | 修了証番号 | VARCHAR | 50 | NULL | - | - | - | - | 修了証・認定証の番号 |
| 22 | self_assessment | 自己評価 | TEXT | - | NULL | - | - | - | - | 研修に対する自己評価 |
| 23 | manager_assessment | 上長評価 | TEXT | - | NULL | - | - | - | - | 研修に対する上長評価 |
| 24 | manager_confirmed | 上長確認フラグ | BOOLEAN | - | NOT NULL | false | - | - | IDX | 上長による確認完了フラグ |
| 25 | manager_confirmed_at | 上長確認日時 | TIMESTAMP | - | NULL | - | - | - | - | 上長による確認日時 |
| 26 | attachment_url | 添付資料URL | VARCHAR | 500 | NULL | - | - | - | - | 修了証や資料の添付ファイルURL |
| 27 | created_at | 作成日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | - | レコード作成日時 |
| 28 | created_by | 作成者 | VARCHAR | 50 | NOT NULL | - | - | ○ | - | レコード作成者 |
| 29 | updated_at | 更新日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | - | レコード更新日時 |
| 30 | updated_by | 更新者 | VARCHAR | 50 | NOT NULL | - | - | ○ | - | レコード更新者 |

## リレーション

### 参照先テーブル
- MST_Tenant (tenant_id)
- MST_Employee (emp_no)
- MST_TrainingProgram (program_id)
- MST_SkillHierarchy (acquired_skill_id1, acquired_skill_id2, acquired_skill_id3)
- MST_Certification (related_cert_id)
- MST_UserAuth (created_by, updated_by)

### 参照元テーブル
- TRN_SkillRecord (related_training_id)
- TRN_PDU (training_id)

## データ仕様

### training_type（研修種別）
- INTERNAL: 社内研修
- EXTERNAL: 外部研修
- ONLINE: オンライン研修
- CERTIFICATION: 資格取得研修
- SEMINAR: セミナー
- WORKSHOP: ワークショップ
- CONFERENCE: カンファレンス

### cost_bearer（費用負担）
- 会社: 会社負担
- 自己: 自己負担
- 一部負担: 会社・個人の一部負担

### currency_code（通貨コード）
- JPY: 日本円
- USD: 米ドル
- EUR: ユーロ

## 運用仕様

### データ保持期間
- 7年間（法定保存期間に準拠）

### バックアップ
- 日次バックアップ対象
- 月次アーカイブ対象

### メンテナンス
- 定期的な古いデータのアーカイブ
- 添付ファイルの整理

## パフォーマンス

### 想定レコード数
- 初期: 1,000件
- 1年後: 10,000件
- 3年後: 50,000件

### アクセスパターン
- 社員別研修履歴参照: 高頻度
- 期間別研修実績集計: 中頻度
- 研修効果分析: 低頻度

### インデックス設計
- PRIMARY KEY: training_id
- INDEX: tenant_id, emp_no, program_id, training_type, start_date, end_date
- INDEX: acquired_skill_id1, acquired_skill_id2, acquired_skill_id3, related_cert_id
- INDEX: manager_confirmed

## セキュリティ

### アクセス制御
- 参照: 本人、上長、人事担当者、システム管理者
- 更新: 本人、人事担当者、システム管理者
- 削除: システム管理者のみ

### 機密情報
- 個人の研修履歴情報の適切な管理
- 受講料情報の機密性確保

## 移行仕様

### 初期データ
- 既存システムからの研修履歴移行
- 社員マスタとの整合性確保

### データ移行
- 研修プログラムマスタとの紐付け
- スキル・資格マスタとの関連付け

## 特記事項

### 制約事項
- 終了日は開始日以降である必要がある
- 時間数、受講料、PDUポイントは0以上の値
- 上長確認後は基本的に変更不可

### 拡張予定
- 研修効果測定機能
- 自動PDU計算機能
- 研修推奨機能

### 関連システム
- 研修管理システム
- 人事システム
- スキル管理システム
- PDU管理システム
- ファイル管理システム
