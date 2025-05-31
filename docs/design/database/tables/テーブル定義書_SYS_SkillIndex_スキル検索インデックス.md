# テーブル定義書_SYS_SkillIndex_スキル検索インデックス

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | SYS_SkillIndex |
| 論理名 | スキル検索インデックス |
| 用途 | スキル情報の高速検索を実現するためのシステムテーブル |
| カテゴリ | システム系 |
| 作成日 | 2024-12-19 |
| 最終更新日 | 2024-12-19 |

## テーブル概要

スキル検索インデックステーブル（SYS_SkillIndex）は、スキル情報の高速検索を実現するためのシステムテーブルです。
TRN_SkillRecordテーブルとMST_SkillHierarchyテーブルから必要な情報を抽出・加工し、検索に最適化された形式で保持します。
このテーブルにより、特定のスキルを持つ社員の検索や、複数のスキル条件を組み合わせた複雑な検索を効率的に実行できます。
検索パフォーマンス向上のため、正規化せずに冗長データ（部署名、役職名など）を保持し、全文検索用のテキストデータも格納します。

## テーブル構造

| # | カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | PK | FK | インデックス | 説明 |
|---|----------|--------|----------|------|------|------------|----|----|--------------|------|
| 1 | index_id | インデックスID | VARCHAR | 50 | NOT NULL | - | ○ | - | PK | インデックスを一意に識別するID |
| 2 | tenant_id | テナントID | VARCHAR | 50 | NOT NULL | - | - | ○ | IDX | テナント識別子 |
| 3 | emp_no | 社員番号 | VARCHAR | 20 | NOT NULL | - | - | ○ | IDX | 社員を一意に識別する番号 |
| 4 | skill_id | スキルID | VARCHAR | 50 | NOT NULL | - | - | ○ | IDX | スキル項目を一意に識別するID |
| 5 | report_year | 報告年度 | INTEGER | 4 | NOT NULL | - | - | - | IDX | スキル報告書の年度 |
| 6 | skill_level | 評価レベル | VARCHAR | 1 | NOT NULL | - | - | - | IDX | 評価レベル（×/△/○/◎） |
| 7 | experience_years | 経験年数 | DECIMAL | 3,1 | NULL | - | - | - | - | スキルの経験年数 |
| 8 | category_id | スキルカテゴリID | VARCHAR | 50 | NOT NULL | - | - | ○ | IDX | スキルカテゴリのID |
| 9 | subcategory_id | サブカテゴリID | VARCHAR | 50 | NULL | - | - | ○ | IDX | スキルサブカテゴリのID |
| 10 | skill_name | スキル名 | VARCHAR | 200 | NOT NULL | - | - | - | - | スキル項目の名称 |
| 11 | category_name | カテゴリ名 | VARCHAR | 200 | NOT NULL | - | - | - | - | スキルカテゴリの名称 |
| 12 | subcategory_name | サブカテゴリ名 | VARCHAR | 200 | NULL | - | - | - | - | スキルサブカテゴリの名称 |
| 13 | dept_id | 部署ID | VARCHAR | 20 | NOT NULL | - | - | ○ | IDX | 社員の所属部署ID |
| 14 | dept_name | 部署名 | VARCHAR | 100 | NOT NULL | - | - | - | - | 社員の所属部署名 |
| 15 | position_id | 役職ID | VARCHAR | 20 | NOT NULL | - | - | ○ | IDX | 社員の役職ID |
| 16 | position_name | 役職名 | VARCHAR | 100 | NOT NULL | - | - | - | - | 社員の役職名 |
| 17 | emp_name | 社員名 | VARCHAR | 100 | NOT NULL | - | - | - | - | 社員の氏名 |
| 18 | search_text | 検索用テキスト | TEXT | - | NOT NULL | - | - | - | FULLTEXT | 全文検索用のテキストデータ |
| 19 | last_updated | 最終更新日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | - | インデックス最終更新日時 |
| 20 | created_at | 作成日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | - | レコード作成日時 |
| 21 | updated_at | 更新日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | - | レコード更新日時 |

## リレーション

### 参照先テーブル
- MST_Tenant (tenant_id)
- MST_Employee (emp_no)
- MST_SkillHierarchy (skill_id)
- MST_SkillCategory (category_id, subcategory_id)
- MST_Department (dept_id)
- MST_Position (position_id)

### 参照元テーブル
- なし（検索専用テーブル）

## データ仕様

### skill_level（評価レベル）
- ×: 未経験・知識なし
- △: 基礎知識あり・指導下で実行可能
- ○: 一人で実行可能・経験豊富
- ◎: 指導・教育が可能・エキスパート

### experience_years（経験年数）
- 0.0〜99.9の範囲
- 小数点第1位まで記録可能

### search_text（検索用テキスト）
以下の情報を連結して格納：
- スキル名、カテゴリ名、サブカテゴリ名
- 社員名、部署名、役職名
- スキル説明文（MST_SkillHierarchyから）

## 運用仕様

### データ保持期間
- 3年間（検索パフォーマンス維持のため）

### バックアップ
- 日次バックアップ対象
- インデックス再構築時のバックアップ

### メンテナンス
- BATCH-006によるインデックス再構築
- 定期的な全文検索インデックス最適化

## パフォーマンス

### 想定レコード数
- 初期: 10,000件
- 1年後: 50,000件
- 3年後: 150,000件

### アクセスパターン
- スキル検索: 高頻度
- 社員検索: 高頻度
- 複合条件検索: 中頻度

### インデックス設計
- PRIMARY KEY: index_id
- INDEX: tenant_id, emp_no, skill_id, skill_level
- INDEX: report_year, category_id, subcategory_id
- INDEX: dept_id, position_id
- FULLTEXT INDEX: search_text

## セキュリティ

### アクセス制御
- 参照: 全ユーザー（検索機能）
- 更新: システムバッチのみ
- 削除: システム管理者のみ

### 機密情報
- 個人スキル情報の適切な管理
- 検索ログの監査

## 移行仕様

### 初期データ
- TRN_SkillRecordからのデータ抽出
- 関連マスタテーブルとの結合

### データ移行
- バッチ処理による自動生成
- 差分更新による効率化

## 特記事項

### 制約事項
- 直接の更新は禁止（バッチ処理のみ）
- 検索専用テーブルとして運用
- 最新年度のデータを優先的にインデックス化

### 拡張予定
- AI検索機能の追加
- スキルマッチング機能
- レコメンデーション機能

### 関連システム
- スキル管理システム
- 検索システム
- レポート生成システム
- バッチ処理システム

### パフォーマンス最適化
- インデックス再構築はシステム負荷の少ない時間帯に実行
- 全文検索インデックスの定期最適化
- 古いデータの自動アーカイブ
