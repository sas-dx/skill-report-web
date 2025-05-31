# テーブル定義書_MST_TrainingProgram_研修プログラム

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_TrainingProgram |
| 論理名 | 研修プログラム |
| 用途 | 研修プログラムの基本情報管理 |
| カテゴリ | マスタ系 |
| 作成日 | 2024-12-19 |
| 最終更新日 | 2024-12-19 |

## テーブル概要

社員が受講可能な研修プログラムの基本情報を管理するマスタテーブルです。
内部研修、外部研修、オンライン研修等の各種研修プログラムの詳細情報を格納し、
研修管理機能の基盤となります。

## テーブル構造

| # | カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | PK | FK | インデックス | 説明 |
|---|----------|--------|----------|------|------|------------|----|----|--------------|------|
| 1 | program_id | プログラムID | VARCHAR | 50 | NOT NULL | - | ○ | - | PK | 研修プログラムの一意識別子 |
| 2 | tenant_id | テナントID | VARCHAR | 50 | NOT NULL | - | - | ○ | IDX | テナント識別子 |
| 3 | program_code | プログラムコード | VARCHAR | 20 | NOT NULL | - | - | - | UNQ | プログラムの識別コード |
| 4 | program_name | プログラム名 | VARCHAR | 200 | NOT NULL | - | - | - | IDX | 研修プログラムの名称 |
| 5 | program_type | プログラム種別 | VARCHAR | 20 | NOT NULL | - | - | - | IDX | INTERNAL/EXTERNAL/ONLINE/CERTIFICATION |
| 6 | category | カテゴリ | VARCHAR | 50 | NOT NULL | - | - | - | IDX | 研修カテゴリ（技術/ビジネス/マネジメント等） |
| 7 | level | レベル | VARCHAR | 20 | NOT NULL | - | - | - | IDX | BEGINNER/INTERMEDIATE/ADVANCED |
| 8 | duration_hours | 研修時間 | DECIMAL | 5,2 | NOT NULL | - | - | - | - | 研修時間（時間単位） |
| 9 | max_participants | 最大受講者数 | INTEGER | - | NULL | - | - | - | - | 最大受講可能人数 |
| 10 | description | 研修概要 | TEXT | - | NOT NULL | - | - | - | - | 研修内容の概要 |
| 11 | objectives | 研修目標 | TEXT | - | NULL | - | - | - | - | 研修の目標・到達点 |
| 12 | prerequisites | 受講前提条件 | TEXT | - | NULL | - | - | - | - | 受講に必要な前提知識・条件 |
| 13 | provider | 研修提供者 | VARCHAR | 100 | NULL | - | - | - | - | 研修提供会社・講師名 |
| 14 | cost | 受講費用 | DECIMAL | 10,2 | NULL | - | - | - | - | 1人あたりの受講費用 |
| 15 | certification_available | 認定証発行 | BOOLEAN | - | NOT NULL | false | - | - | - | 認定証発行の有無 |
| 16 | pdu_points | PDUポイント | INTEGER | - | NULL | - | - | - | - | 取得可能なPDUポイント |
| 17 | is_active | 有効フラグ | BOOLEAN | - | NOT NULL | true | - | - | IDX | プログラムの有効/無効 |
| 18 | start_date | 開始日 | DATE | - | NULL | - | - | - | - | プログラム開始日 |
| 19 | end_date | 終了日 | DATE | - | NULL | - | - | - | - | プログラム終了日 |
| 20 | created_at | 作成日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | - | レコード作成日時 |
| 21 | created_by | 作成者 | VARCHAR | 50 | NOT NULL | - | - | - | - | レコード作成者 |
| 22 | updated_at | 更新日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | - | レコード更新日時 |
| 23 | updated_by | 更新者 | VARCHAR | 50 | NOT NULL | - | - | - | - | レコード更新者 |

## リレーション

### 参照先テーブル
- MST_Tenant (tenant_id)

### 参照元テーブル
- TRN_TrainingHistory (program_id)
- TRN_PDU (program_id)

## データ仕様

### program_type（プログラム種別）
- INTERNAL: 社内研修
- EXTERNAL: 外部研修
- ONLINE: オンライン研修
- CERTIFICATION: 資格取得研修

### category（カテゴリ）
- TECHNICAL: 技術研修
- BUSINESS: ビジネススキル研修
- MANAGEMENT: マネジメント研修
- COMPLIANCE: コンプライアンス研修
- SAFETY: 安全研修
- LANGUAGE: 語学研修

### level（レベル）
- BEGINNER: 初級
- INTERMEDIATE: 中級
- ADVANCED: 上級

## 運用仕様

### データ保持期間
- 無期限（マスタデータのため）

### バックアップ
- 日次バックアップ対象
- 月次アーカイブ対象

### メンテナンス
- 定期的なプログラム内容の見直し
- 終了プログラムの無効化

## パフォーマンス

### 想定レコード数
- 初期: 50件
- 1年後: 200件
- 3年後: 500件

### アクセスパターン
- 研修一覧表示: 高頻度
- 研修詳細参照: 中頻度
- プログラム管理: 低頻度

### インデックス設計
- PRIMARY KEY: program_id
- UNIQUE: tenant_id, program_code
- INDEX: tenant_id, program_type, category, level, is_active

## セキュリティ

### アクセス制御
- 参照: 全ユーザー
- 更新: 研修管理者、システム管理者
- 削除: システム管理者のみ

### 機密情報
- 受講費用情報の適切な管理
- 外部研修提供者情報の保護

## 移行仕様

### 初期データ
- 既存研修プログラムの移行
- 標準的な研修カテゴリの設定

### データ移行
- 既存システムからのプログラム情報移行
- 研修履歴との整合性確保

## 特記事項

### 制約事項
- プログラムコードはテナント内で一意
- 開始日 ≤ 終了日の制約
- 最大受講者数は正の整数

### 拡張予定
- 研修スケジュール管理機能
- 前提条件の自動チェック機能
- 研修効果測定機能

### 関連システム
- 研修管理システム
- 人事システム
- 外部研修提供者システム
- 認定証発行システム
