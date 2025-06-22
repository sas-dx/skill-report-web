# テーブル定義書: TRN_GoalProgress

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_GoalProgress |
| 論理名 | 目標進捗 |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-21 22:02:18 |

## 概要

TRN_GoalProgress（目標進捗）は、社員個人の目標設定と進捗状況を管理するトランザクションテーブルです。
主な目的：
- 個人目標の設定・管理（業務目標、スキル向上目標等）
- 目標達成度の定期的な進捗管理
- 上司・部下間での目標共有・フィードバック
- 人事評価・査定の基礎データ
- 組織目標と個人目標の連携管理
- 目標設定から達成までのプロセス管理
- 成果測定・KPI管理
- 人材育成計画の基礎データ
このテーブルは、人事評価制度、目標管理制度（MBO）、人材育成など、
組織の成果管理と人材開発の基盤となる重要なデータを提供します。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| goalprogress_id | TRN_GoalProgressの主キー | SERIAL |  | × |  | TRN_GoalProgressの主キー |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_by | レコード作成者のユーザーID | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | レコード更新者のユーザーID | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_trn_goalprogress_tenant_id | tenant_id | × | テナントID検索用インデックス |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_TRN_GoalProgress_employee | None | None | None | CASCADE | CASCADE | 外部キー制約 |
| fk_TRN_GoalProgress_supervisor | None | None | None | CASCADE | SET NULL | 外部キー制約 |
| fk_TRN_GoalProgress_approved_by | None | None | None | CASCADE | SET NULL | 外部キー制約 |
| fk_TRN_GoalProgress_career_plan | None | None | None | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_trn_goalprogress | PRIMARY KEY | goalprogress_id, id | 主キー制約 |

## サンプルデータ

| goal_id | employee_id | goal_title | goal_description | goal_category | goal_type | priority_level | target_value | current_value | unit | start_date | target_date | progress_rate | achievement_status | supervisor_id | approval_status | approved_at | approved_by | completion_date | achievement_rate | self_evaluation | supervisor_evaluation | evaluation_comments | related_career_plan_id | related_skill_items | milestones | obstacles | support_needed | last_updated_at | next_review_date |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| GOAL000001 | EMP000001 | Java技術習得 | Spring Frameworkを使用したWebアプリケーション開発技術の習得 | SKILL | QUALITATIVE | HIGH | None | None | None | 2025-01-01 | 2025-12-31 | 50.0 | IN_PROGRESS | EMP000010 | APPROVED | 2025-01-05 10:00:00 | EMP000010 | None | None | None | None | None | CP000001 | ["JAVA", "SPRING", "WEB_DEVELOPMENT"] | ["基礎学習完了", "実践プロジェクト参加", "技術認定取得"] | None | 外部研修参加、メンター指導 | 2025-06-01 09:00:00 | 2025-07-01 |
| GOAL000002 | EMP000002 | 売上目標達成 | 第2四半期の個人売上目標1000万円の達成 | BUSINESS | QUANTITATIVE | HIGH | 10000000.0 | 6500000.0 | 円 | 2025-04-01 | 2025-06-30 | 65.0 | IN_PROGRESS | EMP000011 | APPROVED | 2025-03-25 14:00:00 | EMP000011 | None | None | None | None | None | None | ["SALES", "NEGOTIATION", "CUSTOMER_MANAGEMENT"] | ["4月目標達成", "5月目標達成", "6月目標達成"] | ["競合他社の価格競争", "新規顧客開拓の困難"] | マーケティング支援、価格戦略見直し | 2025-06-01 17:00:00 | 2025-06-15 |
| GOAL000003 | EMP000003 | チームリーダー昇進 | リーダーシップスキル向上とチーム管理経験の積み重ね | CAREER | MILESTONE | MEDIUM | None | None | None | 2025-01-01 | 2025-12-31 | 30.0 | IN_PROGRESS | EMP000012 | APPROVED | 2025-01-10 11:00:00 | EMP000012 | None | None | None | None | None | CP000002 | ["LEADERSHIP", "TEAM_MANAGEMENT", "COMMUNICATION"] | ["リーダーシップ研修受講", "プロジェクトリーダー経験", "昇進面談"] | None | リーダーシップ研修、メンタリング | 2025-06-01 12:00:00 | 2025-08-01 |

## 特記事項

- 目標IDは自動採番または手動設定
- 進捗率は定期的に更新
- 承認フローにより目標の妥当性を担保
- 定量目標は目標値・現在値で進捗管理
- 定性目標は進捗率とコメントで管理
- マイルストーン目標は段階的な達成管理
- 関連スキル・キャリアプランとの連携
- 論理削除は is_deleted フラグで管理

## 業務ルール

- 進捗率は0-100%の範囲で設定
- 目標期限は開始日より未来の日付
- 承認済み目標のみ進捗管理対象
- 期限超過時は自動的にOVERDUE状態に変更
- 完了時は達成率・評価の入力必須
- 自己評価・上司評価は1-5段階
- 定量目標は目標値・現在値・単位の設定必須
- 優先度HIGH目標は週次レビュー推奨
- キャリア目標は年次評価と連動
- 目標変更時は承認フロー再実行

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 目標進捗トランザクションテーブルの詳細定義 |