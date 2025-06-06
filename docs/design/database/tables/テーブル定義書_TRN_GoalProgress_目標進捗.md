# テーブル定義書: TRN_GoalProgress

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_GoalProgress |
| 論理名 | 目標進捗 |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-04 06:57:02 |

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
| goal_id | 目標ID | VARCHAR | 50 | ○ |  | 目標を一意に識別するID（例：GOAL000001） |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 目標を設定した社員のID（MST_Employeeへの外部キー） |
| goal_title | 目標タイトル | VARCHAR | 200 | ○ |  | 目標の簡潔なタイトル |
| goal_description | 目標詳細 | TEXT |  | ○ |  | 目標の詳細説明・背景・期待効果 |
| goal_category | 目標カテゴリ | ENUM |  | ○ |  | 目標のカテゴリ（BUSINESS:業務、SKILL:スキル、CAREER:キャリア、PERSONAL:個人） |
| goal_type | 目標種別 | ENUM |  | ○ |  | 目標種別（QUANTITATIVE:定量、QUALITATIVE:定性、MILESTONE:マイルストーン） |
| priority_level | 優先度 | ENUM |  | ○ | MEDIUM | 目標の優先度（HIGH:高、MEDIUM:中、LOW:低） |
| target_value | 目標値 | DECIMAL | 15,2 | ○ |  | 定量目標の目標値 |
| current_value | 現在値 | DECIMAL | 15,2 | ○ |  | 定量目標の現在値 |
| unit | 単位 | VARCHAR | 50 | ○ |  | 目標値・現在値の単位（件、円、%等） |
| start_date | 開始日 | DATE |  | ○ |  | 目標の開始日 |
| target_date | 目標期限 | DATE |  | ○ |  | 目標達成の期限日 |
| progress_rate | 進捗率 | DECIMAL | 5,2 | ○ | 0.0 | 目標の進捗率（0.00-100.00%） |
| achievement_status | 達成状況 | ENUM |  | ○ | NOT_STARTED | 達成状況（NOT_STARTED:未着手、IN_PROGRESS:進行中、COMPLETED:完了、OVERDUE:期限超過、CANCELLED:中止） |
| supervisor_id | 上司ID | VARCHAR | 50 | ○ |  | 目標を承認・管理する上司のID（MST_Employeeへの外部キー） |
| approval_status | 承認状況 | ENUM |  | ○ | DRAFT | 承認状況（DRAFT:下書き、PENDING:承認待ち、APPROVED:承認済み、REJECTED:却下） |
| approved_at | 承認日時 | TIMESTAMP |  | ○ |  | 目標が承認された日時 |
| approved_by | 承認者ID | VARCHAR | 50 | ○ |  | 目標を承認した人のID（MST_Employeeへの外部キー） |
| completion_date | 完了日 | DATE |  | ○ |  | 目標が完了した日 |
| achievement_rate | 達成率 | DECIMAL | 5,2 | ○ |  | 最終的な達成率（0.00-100.00%） |
| self_evaluation | 自己評価 | INTEGER |  | ○ |  | 本人による自己評価（1-5段階） |
| supervisor_evaluation | 上司評価 | INTEGER |  | ○ |  | 上司による評価（1-5段階） |
| evaluation_comments | 評価コメント | TEXT |  | ○ |  | 評価に関するコメント・フィードバック |
| related_career_plan_id | 関連キャリアプランID | VARCHAR | 50 | ○ |  | 関連するキャリアプランのID（MST_CareerPlanへの外部キー） |
| related_skill_items | 関連スキル項目 | TEXT |  | ○ |  | 関連するスキル項目のリスト（JSON形式） |
| milestones | マイルストーン | TEXT |  | ○ |  | 目標達成のマイルストーン（JSON形式） |
| obstacles | 障害・課題 | TEXT |  | ○ |  | 目標達成の障害・課題（JSON形式） |
| support_needed | 必要サポート | TEXT |  | ○ |  | 目標達成に必要なサポート・リソース |
| last_updated_at | 最終更新日時 | TIMESTAMP |  | ○ |  | 進捗が最後に更新された日時 |
| next_review_date | 次回レビュー日 | DATE |  | ○ |  | 次回の進捗レビュー予定日 |
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  | マルチテナント識別子 |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_TRN_GoalProgress_goal_id | goal_id | ○ | 目標ID検索用（一意） |
| idx_TRN_GoalProgress_employee_id | employee_id | × | 社員別目標検索用 |
| idx_TRN_GoalProgress_supervisor_id | supervisor_id | × | 上司別目標検索用 |
| idx_TRN_GoalProgress_category | goal_category | × | 目標カテゴリ別検索用 |
| idx_TRN_GoalProgress_status | achievement_status | × | 達成状況別検索用 |
| idx_TRN_GoalProgress_approval_status | approval_status | × | 承認状況別検索用 |
| idx_TRN_GoalProgress_target_date | target_date | × | 目標期限別検索用 |
| idx_TRN_GoalProgress_priority | priority_level | × | 優先度別検索用 |
| idx_TRN_GoalProgress_employee_period | employee_id, start_date, target_date | × | 社員・期間複合検索用 |
| idx_TRN_GoalProgress_next_review | next_review_date | × | 次回レビュー日検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_TRN_GoalProgress_employee | employee_id | MST_Employee | id | CASCADE | CASCADE | 社員への外部キー |
| fk_TRN_GoalProgress_supervisor | supervisor_id | MST_Employee | id | CASCADE | SET NULL | 上司への外部キー |
| fk_TRN_GoalProgress_approved_by | approved_by | MST_Employee | id | CASCADE | SET NULL | 承認者への外部キー |
| fk_TRN_GoalProgress_career_plan | related_career_plan_id | MST_CareerPlan | id | CASCADE | SET NULL | キャリアプランへの外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_TRN_GoalProgress_goal_id | UNIQUE |  | 目標ID一意制約 |
| chk_TRN_GoalProgress_category | CHECK | goal_category IN ('BUSINESS', 'SKILL', 'CAREER', 'PERSONAL') | 目標カテゴリ値チェック制約 |
| chk_TRN_GoalProgress_type | CHECK | goal_type IN ('QUANTITATIVE', 'QUALITATIVE', 'MILESTONE') | 目標種別値チェック制約 |
| chk_TRN_GoalProgress_priority | CHECK | priority_level IN ('HIGH', 'MEDIUM', 'LOW') | 優先度値チェック制約 |
| chk_TRN_GoalProgress_progress_rate | CHECK | progress_rate >= 0 AND progress_rate <= 100 | 進捗率範囲チェック制約 |
| chk_TRN_GoalProgress_achievement_status | CHECK | achievement_status IN ('NOT_STARTED', 'IN_PROGRESS', 'COMPLETED', 'OVERDUE', 'CANCELLED') | 達成状況値チェック制約 |
| chk_TRN_GoalProgress_approval_status | CHECK | approval_status IN ('DRAFT', 'PENDING', 'APPROVED', 'REJECTED') | 承認状況値チェック制約 |
| chk_TRN_GoalProgress_achievement_rate | CHECK | achievement_rate IS NULL OR (achievement_rate >= 0 AND achievement_rate <= 100) | 達成率範囲チェック制約 |
| chk_TRN_GoalProgress_self_evaluation | CHECK | self_evaluation IS NULL OR (self_evaluation >= 1 AND self_evaluation <= 5) | 自己評価範囲チェック制約 |
| chk_TRN_GoalProgress_supervisor_evaluation | CHECK | supervisor_evaluation IS NULL OR (supervisor_evaluation >= 1 AND supervisor_evaluation <= 5) | 上司評価範囲チェック制約 |
| chk_TRN_GoalProgress_date_range | CHECK | start_date <= target_date | 日付範囲整合性チェック制約 |
| chk_TRN_GoalProgress_target_value | CHECK | target_value IS NULL OR target_value >= 0 | 目標値非負値チェック制約 |
| chk_TRN_GoalProgress_current_value | CHECK | current_value IS NULL OR current_value >= 0 | 現在値非負値チェック制約 |

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
