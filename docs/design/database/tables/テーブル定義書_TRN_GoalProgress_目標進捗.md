# テーブル定義書_TRN_GoalProgress_目標進捗

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | TRN_GoalProgress |
| 論理名 | 目標進捗 |
| 用途 | キャリアプラン目標の進捗管理 |
| カテゴリ | トランザクション系 |
| 作成日 | 2024-12-19 |
| 最終更新日 | 2024-12-19 |

## テーブル概要

社員のキャリアプランに設定された目標の進捗状況を管理するトランザクションテーブルです。
目標ごとの進捗率、達成状況、進捗コメント、次のアクションなどを記録し、
定期的な進捗確認と評価のサイクルをサポートします。
このテーブルにより、目標達成に向けたPDCAサイクルを効果的に回すことができます。

## テーブル構造

| # | カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | PK | FK | インデックス | 説明 |
|---|----------|--------|----------|------|------|------------|----|----|--------------|------|
| 1 | progress_id | 進捗ID | VARCHAR | 50 | NOT NULL | - | ○ | - | PK | 進捗記録の一意識別子 |
| 2 | tenant_id | テナントID | VARCHAR | 50 | NOT NULL | - | - | ○ | IDX | テナント識別子 |
| 3 | career_plan_id | キャリアプランID | VARCHAR | 50 | NOT NULL | - | - | ○ | IDX | 関連するキャリアプランID |
| 4 | emp_no | 社員番号 | VARCHAR | 20 | NOT NULL | - | - | ○ | IDX | 社員識別番号 |
| 5 | goal_type | 目標種別 | VARCHAR | 10 | NOT NULL | - | - | - | IDX | 目標の種別 |
| 6 | check_date | 進捗確認日 | DATE | - | NOT NULL | - | - | - | IDX | 進捗確認を行った日付 |
| 7 | progress_rate | 進捗率 | INTEGER | 3 | NOT NULL | 0 | - | - | - | 目標の進捗率（0-100%） |
| 8 | achievement_status | 達成状況 | VARCHAR | 20 | NOT NULL | '未着手' | - | - | IDX | 達成状況 |
| 9 | progress_comment | 進捗コメント | TEXT | - | NULL | - | - | - | - | 進捗に関するコメント |
| 10 | next_action | 次のアクション | TEXT | - | NULL | - | - | - | - | 次に実施するアクション |
| 11 | issues | 課題・障害 | TEXT | - | NULL | - | - | - | - | 目標達成における課題や障害 |
| 12 | self_assessment | 自己評価 | TEXT | - | NULL | - | - | - | - | 進捗に対する自己評価 |
| 13 | manager_assessment | 上長評価 | TEXT | - | NULL | - | - | - | - | 進捗に対する上長評価 |
| 14 | manager_confirmed | 上長確認フラグ | BOOLEAN | - | NOT NULL | false | - | - | IDX | 上長による確認完了フラグ |
| 15 | manager_confirmed_at | 上長確認日時 | TIMESTAMP | - | NULL | - | - | - | - | 上長による確認日時 |
| 16 | related_skill_id | 関連スキルID | VARCHAR | 50 | NULL | - | - | ○ | IDX | 進捗に関連するスキルID |
| 17 | related_cert_id | 関連資格ID | VARCHAR | 50 | NULL | - | - | ○ | IDX | 進捗に関連する資格ID |
| 18 | related_training_id | 関連研修ID | VARCHAR | 50 | NULL | - | - | ○ | IDX | 進捗に関連する研修ID |
| 19 | created_at | 作成日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | - | レコード作成日時 |
| 20 | created_by | 作成者 | VARCHAR | 50 | NOT NULL | - | - | ○ | - | レコード作成者 |
| 21 | updated_at | 更新日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | - | レコード更新日時 |
| 22 | updated_by | 更新者 | VARCHAR | 50 | NOT NULL | - | - | ○ | - | レコード更新者 |

## リレーション

### 参照先テーブル
- MST_Tenant (tenant_id)
- MST_CareerPlan (career_plan_id)
- MST_Employee (emp_no)
- MST_SkillHierarchy (related_skill_id)
- MST_Certification (related_cert_id)
- TRN_TrainingHistory (related_training_id)
- MST_UserAuth (created_by, updated_by)

### 参照元テーブル
- HIS_GoalProgressHistory (progress_id)

## データ仕様

### goal_type（目標種別）
- 短期: 短期目標（1年以内）
- 中期: 中期目標（1-3年）
- 長期: 長期目標（3年以上）

### achievement_status（達成状況）
- 未着手: まだ取り組みを開始していない
- 進行中: 現在取り組み中
- 達成済: 目標を達成済み
- 中止: 目標を中止・変更

### progress_rate（進捗率）
- 0-100の整数値
- パーセンテージで表現

## 運用仕様

### データ保持期間
- 5年間（キャリア開発履歴として保持）

### バックアップ
- 日次バックアップ対象
- 月次アーカイブ対象

### メンテナンス
- 定期的な進捗状況の確認
- 古い進捗データのアーカイブ

## パフォーマンス

### 想定レコード数
- 初期: 500件
- 1年後: 5,000件
- 3年後: 20,000件

### アクセスパターン
- 社員別進捗参照: 高頻度
- 期間別進捗集計: 中頻度
- 目標達成分析: 低頻度

### インデックス設計
- PRIMARY KEY: progress_id
- INDEX: tenant_id, career_plan_id, emp_no, goal_type, check_date
- INDEX: achievement_status, manager_confirmed
- INDEX: related_skill_id, related_cert_id, related_training_id

## セキュリティ

### アクセス制御
- 参照: 本人、上長、人事担当者、システム管理者
- 更新: 本人、人事担当者、システム管理者
- 削除: システム管理者のみ

### 機密情報
- 個人の目標進捗情報の適切な管理
- 評価コメントの機密性確保

## 移行仕様

### 初期データ
- 既存システムからの進捗データ移行
- キャリアプランとの整合性確保

### データ移行
- 関連スキル・資格・研修との紐付け
- 進捗履歴の継承

## 特記事項

### 制約事項
- 進捗率は0〜100の範囲内
- 目標種別は定義された値のみ
- 達成状況は定義された値のみ
- 上長確認後は基本的に変更不可

### 拡張予定
- 進捗自動更新機能
- 目標達成予測機能
- 進捗アラート機能

### 関連システム
- キャリア管理システム
- 人事評価システム
- スキル管理システム
- 研修管理システム
- 通知システム
