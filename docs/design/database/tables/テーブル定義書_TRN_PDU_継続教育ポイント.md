# テーブル定義書_TRN_PDU_継続教育ポイント

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | TRN_PDU |
| 論理名 | 継続教育ポイント |
| 用途 | 資格維持に必要なPDU・継続教育ポイント管理 |
| カテゴリ | トランザクション系 |
| 作成日 | 2024-12-19 |
| 最終更新日 | 2024-12-19 |

## テーブル概要

資格維持に必要なPDU（Professional Development Unit）や継続教育ポイントを管理するトランザクションテーブルです。
取得ポイント、取得日、有効期限、関連資格、取得方法などの情報を記録し、
資格の更新要件を満たすための活動を追跡します。
このテーブルにより、資格保持者の継続的な専門能力開発を支援し、資格の有効期限管理を効率化します。

## テーブル構造

| # | カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | PK | FK | インデックス | 説明 |
|---|----------|--------|----------|------|------|------------|----|----|--------------|------|
| 1 | pdu_id | PDU ID | VARCHAR | 50 | NOT NULL | - | ○ | - | PK | PDUレコードの一意識別子 |
| 2 | tenant_id | テナントID | VARCHAR | 50 | NOT NULL | - | - | ○ | IDX | テナント識別子 |
| 3 | emp_no | 社員番号 | VARCHAR | 20 | NOT NULL | - | - | ○ | IDX | PDU取得者の社員番号 |
| 4 | cert_id | 資格ID | VARCHAR | 50 | NOT NULL | - | - | ○ | IDX | 関連する資格ID |
| 5 | pdu_category | PDUカテゴリ | VARCHAR | 50 | NOT NULL | - | - | - | IDX | PDUのカテゴリ |
| 6 | points | 取得ポイント | DECIMAL | 5,1 | NOT NULL | - | - | - | - | 取得したPDUポイント |
| 7 | acquisition_date | 取得日 | DATE | - | NOT NULL | - | - | - | IDX | PDUを取得した日付 |
| 8 | expiry_date | 有効期限 | DATE | - | NULL | - | - | - | IDX | PDUの有効期限 |
| 9 | activity_name | 活動名 | VARCHAR | 200 | NOT NULL | - | - | - | - | PDU取得活動の名称 |
| 10 | activity_description | 活動内容 | TEXT | - | NULL | - | - | - | - | 活動の詳細内容 |
| 11 | training_id | 研修ID | VARCHAR | 50 | NULL | - | - | ○ | IDX | 関連する研修ID |
| 12 | project_id | 案件ID | VARCHAR | 50 | NULL | - | - | ○ | IDX | 関連する案件ID |
| 13 | certificate_no | 証明書番号 | VARCHAR | 50 | NULL | - | - | - | - | PDU証明書の番号 |
| 14 | certificate_url | 証明書URL | VARCHAR | 500 | NULL | - | - | - | - | PDU証明書の添付ファイルURL |
| 15 | manager_confirmed | 上長確認フラグ | BOOLEAN | - | NOT NULL | false | - | - | IDX | 上長による確認完了フラグ |
| 16 | manager_confirmed_at | 上長確認日時 | TIMESTAMP | - | NULL | - | - | - | - | 上長による確認日時 |
| 17 | created_at | 作成日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | - | レコード作成日時 |
| 18 | created_by | 作成者 | VARCHAR | 50 | NOT NULL | - | - | ○ | - | レコード作成者 |
| 19 | updated_at | 更新日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | - | レコード更新日時 |
| 20 | updated_by | 更新者 | VARCHAR | 50 | NOT NULL | - | - | ○ | - | レコード更新者 |

## リレーション

### 参照先テーブル
- MST_Tenant (tenant_id)
- MST_Employee (emp_no)
- MST_Certification (cert_id)
- TRN_TrainingHistory (training_id)
- TRN_ProjectRecord (project_id)
- MST_UserAuth (created_by, updated_by)

### 参照元テーブル
- HIS_PDUHistory (pdu_id)

## データ仕様

### pdu_category（PDUカテゴリ）
- 教育: 研修・セミナー・講習会への参加
- 実務: 実務経験による学習
- 貢献: 専門分野への貢献活動
- 自己学習: 書籍・オンライン学習等
- その他: その他の継続教育活動

### points（取得ポイント）
- 0.1〜999.9の範囲
- 小数点第1位まで記録可能

### 活動例
- 研修参加: 外部研修・社内研修への参加
- 資格取得: 新規資格の取得
- 論文発表: 学会・雑誌への論文投稿
- 講師活動: セミナー・研修の講師担当

## 運用仕様

### データ保持期間
- 5年間（資格更新サイクルに対応）

### バックアップ
- 日次バックアップ対象
- 月次アーカイブ対象

### メンテナンス
- 有効期限切れPDUの定期チェック
- 資格更新要件の充足状況確認

## パフォーマンス

### 想定レコード数
- 初期: 500件
- 1年後: 5,000件
- 3年後: 20,000件

### アクセスパターン
- 社員別PDU参照: 高頻度
- 資格別PDU集計: 中頻度
- 有効期限チェック: 中頻度

### インデックス設計
- PRIMARY KEY: pdu_id
- INDEX: tenant_id, emp_no, cert_id, pdu_category
- INDEX: acquisition_date, expiry_date
- INDEX: training_id, project_id, manager_confirmed

## セキュリティ

### アクセス制御
- 参照: 本人、上長、人事担当者、システム管理者
- 更新: 本人、人事担当者、システム管理者
- 削除: システム管理者のみ

### 機密情報
- 個人の継続教育情報の適切な管理
- 証明書類の機密性確保

## 移行仕様

### 初期データ
- 既存システムからのPDUデータ移行
- 資格との関連付け

### データ移行
- 研修・案件との紐付け
- 証明書類の電子化

## 特記事項

### 制約事項
- 取得ポイントは0より大きい値のみ
- 有効期限は取得日より後である必要がある
- 上長確認後は基本的に変更不可

### 拡張予定
- PDU自動計算機能
- 資格更新アラート機能
- PDU不足予測機能

### 関連システム
- 資格管理システム
- 研修管理システム
- 案件管理システム
- 通知システム
- 証明書管理システム
