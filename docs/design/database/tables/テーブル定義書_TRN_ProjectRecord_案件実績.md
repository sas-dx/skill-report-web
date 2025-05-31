# テーブル定義書_TRN_ProjectRecord_案件実績

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | TRN_ProjectRecord |
| 論理名 | 案件実績 |
| 用途 | 社員の案件・プロジェクト実績管理 |
| カテゴリ | トランザクション系 |
| 作成日 | 2024-12-19 |
| 最終更新日 | 2024-12-19 |

## テーブル概要

社員が担当した案件・プロジェクトの実績情報を管理するトランザクションテーブルです。
案件名、期間、役割、使用技術、成果、工数などの情報を記録し、
社員のスキルプロファイルと実務経験を補完します。
このテーブルは経歴書作成やスキル評価の裏付け、リソース配置の参考情報として活用されます。

## テーブル構造

| # | カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | PK | FK | インデックス | 説明 |
|---|----------|--------|----------|------|------|------------|----|----|--------------|------|
| 1 | project_id | 案件ID | VARCHAR | 50 | NOT NULL | - | ○ | - | PK | 案件の一意識別子 |
| 2 | tenant_id | テナントID | VARCHAR | 50 | NOT NULL | - | - | ○ | IDX | テナント識別子 |
| 3 | emp_no | 社員番号 | VARCHAR | 20 | NOT NULL | - | - | ○ | IDX | 案件担当者の社員番号 |
| 4 | project_name | 案件名 | VARCHAR | 200 | NOT NULL | - | - | - | IDX | 案件の名称 |
| 5 | client_name | 顧客名 | VARCHAR | 100 | NULL | - | - | - | IDX | 顧客・発注元の名称 |
| 6 | start_date | 開始日 | DATE | - | NOT NULL | - | - | - | IDX | 案件の開始日 |
| 7 | end_date | 終了日 | DATE | - | NULL | - | - | - | IDX | 案件の終了日 |
| 8 | role | 役割 | VARCHAR | 100 | NOT NULL | - | - | - | IDX | 案件での役割 |
| 9 | process | 担当工程 | VARCHAR | 200 | NULL | - | - | - | - | 担当した工程 |
| 10 | team_size | チーム規模 | INTEGER | 3 | NULL | - | - | - | - | プロジェクトチームの人数 |
| 11 | technology1 | 使用技術1 | VARCHAR | 100 | NULL | - | - | - | IDX | 使用した技術・ツール1 |
| 12 | technology2 | 使用技術2 | VARCHAR | 100 | NULL | - | - | - | - | 使用した技術・ツール2 |
| 13 | technology3 | 使用技術3 | VARCHAR | 100 | NULL | - | - | - | - | 使用した技術・ツール3 |
| 14 | technology4 | 使用技術4 | VARCHAR | 100 | NULL | - | - | - | - | 使用した技術・ツール4 |
| 15 | technology5 | 使用技術5 | VARCHAR | 100 | NULL | - | - | - | - | 使用した技術・ツール5 |
| 16 | related_skill_id1 | 関連スキルID1 | VARCHAR | 50 | NULL | - | - | ○ | IDX | 案件に関連するスキルID1 |
| 17 | related_skill_id2 | 関連スキルID2 | VARCHAR | 50 | NULL | - | - | ○ | IDX | 案件に関連するスキルID2 |
| 18 | related_skill_id3 | 関連スキルID3 | VARCHAR | 50 | NULL | - | - | ○ | IDX | 案件に関連するスキルID3 |
| 19 | description | 業務内容 | TEXT | - | NOT NULL | - | - | - | - | 案件での業務内容の詳細 |
| 20 | achievements | 成果・実績 | TEXT | - | NULL | - | - | - | - | 案件での成果・実績 |
| 21 | man_months | 工数（人月） | DECIMAL | 4,1 | NULL | - | - | - | - | 投入工数（人月） |
| 22 | manager_confirmed | 上長確認フラグ | BOOLEAN | - | NOT NULL | false | - | - | IDX | 上長による確認完了フラグ |
| 23 | manager_confirmed_at | 上長確認日時 | TIMESTAMP | - | NULL | - | - | - | - | 上長による確認日時 |
| 24 | is_public | 公開フラグ | BOOLEAN | - | NOT NULL | true | - | - | IDX | 社内公開するかどうか |
| 25 | created_at | 作成日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | - | レコード作成日時 |
| 26 | created_by | 作成者 | VARCHAR | 50 | NOT NULL | - | - | ○ | - | レコード作成者 |
| 27 | updated_at | 更新日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | - | レコード更新日時 |
| 28 | updated_by | 更新者 | VARCHAR | 50 | NOT NULL | - | - | ○ | - | レコード更新者 |

## リレーション

### 参照先テーブル
- MST_Tenant (tenant_id)
- MST_Employee (emp_no)
- MST_SkillHierarchy (related_skill_id1, related_skill_id2, related_skill_id3)
- MST_UserAuth (created_by, updated_by)

### 参照元テーブル
- TRN_SkillRecord (related_project_id)
- WRK_BatchJobLog (project_id)
- HIS_ProjectRecordHistory (project_id)

## データ仕様

### role（役割）
- PM: プロジェクトマネージャー
- PL: プロジェクトリーダー
- SE: システムエンジニア
- PG: プログラマー
- テスター: テスト担当者
- その他: その他の役割

### process（担当工程）
- 要件定義: 要件定義工程
- 基本設計: 基本設計工程
- 詳細設計: 詳細設計工程
- 開発: 開発工程
- テスト: テスト工程
- 運用保守: 運用保守工程

### technology（使用技術）
- プログラミング言語、フレームワーク、データベース、ツールなど

## 運用仕様

### データ保持期間
- 永続保持（キャリア履歴として重要）

### バックアップ
- 日次バックアップ対象
- 月次アーカイブ対象

### メンテナンス
- 定期的な案件情報の更新
- 古い案件データの整理

## パフォーマンス

### 想定レコード数
- 初期: 1,000件
- 1年後: 10,000件
- 3年後: 50,000件

### アクセスパターン
- 社員別案件参照: 高頻度
- 技術別案件検索: 中頻度
- 期間別案件集計: 低頻度

### インデックス設計
- PRIMARY KEY: project_id
- INDEX: tenant_id, emp_no, project_name, client_name
- INDEX: start_date, end_date, role, technology1
- INDEX: related_skill_id1, related_skill_id2, related_skill_id3
- INDEX: manager_confirmed, is_public

## セキュリティ

### アクセス制御
- 参照: 本人、上長、人事担当者、システム管理者
- 更新: 本人、人事担当者、システム管理者
- 削除: システム管理者のみ

### 機密情報
- 顧客情報の適切な管理
- 機密案件の公開制御

## 移行仕様

### 初期データ
- 既存システムからの案件データ移行
- スキルとの関連付け

### データ移行
- 使用技術とスキルの紐付け
- 案件履歴の継承

## 特記事項

### 制約事項
- 終了日は開始日より後である必要がある
- 工数は0より大きい値のみ許可
- 上長確認後は基本的に変更不可

### 拡張予定
- 案件評価機能
- 技術トレンド分析機能
- 案件マッチング機能

### 関連システム
- スキル管理システム
- 人事評価システム
- プロジェクト管理システム
- 経歴書生成システム
- リソース配置システム
