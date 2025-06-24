# テーブル定義書: TRN_GoalProgress

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_GoalProgress |
| 論理名 | 目標進捗 |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-24 23:02:19 |

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
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| achievement_rate | 達成率 | DECIMAL | 5,2 | ○ |  | 達成率 |
| achievement_status | 達成状況 | ENUM |  | ○ | NOT_STARTED | 達成状況 |
| approval_status | 承認状況 | ENUM |  | ○ | DRAFT | 承認状況 |
| approved_at | 承認日時 | TIMESTAMP |  | ○ |  | 承認日時 |
| approved_by | 承認者ID | VARCHAR | 50 | ○ |  | 承認者ID |
| completion_date | 完了日 | DATE |  | ○ |  | 完了日 |
| current_value | 現在値 | DECIMAL | 15,2 | ○ |  | 現在値 |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 社員ID |
| evaluation_comments | 評価コメント | TEXT |  | ○ |  | 評価コメント |
| goal_category | 目標カテゴリ | ENUM |  | ○ |  | 目標カテゴリ |
| goal_description | 目標詳細 | TEXT |  | ○ |  | 目標詳細 |
| goal_id | 目標ID | VARCHAR | 50 | ○ |  | 目標ID |
| goal_title | 目標タイトル | VARCHAR | 200 | ○ |  | 目標タイトル |
| goal_type | 目標種別 | ENUM |  | ○ |  | 目標種別 |
| goalprogress_id | TRN_GoalProgressの主キー | SERIAL |  | × |  | TRN_GoalProgressの主キー |
| last_updated_at | 最終更新日時 | TIMESTAMP |  | ○ |  | 最終更新日時 |
| milestones | マイルストーン | TEXT |  | ○ |  | マイルストーン |
| next_review_date | 次回レビュー日 | DATE |  | ○ |  | 次回レビュー日 |
| obstacles | 障害・課題 | TEXT |  | ○ |  | 障害・課題 |
| priority_level | 優先度 | ENUM |  | ○ | MEDIUM | 優先度 |
| progress_rate | 進捗率 | DECIMAL | 5,2 | ○ | 0.0 | 進捗率 |
| related_career_plan_id | 関連キャリアプランID | VARCHAR | 50 | ○ |  | 関連キャリアプランID |
| related_skill_items | 関連スキル項目 | TEXT |  | ○ |  | 関連スキル項目 |
| self_evaluation | 自己評価 | INTEGER |  | ○ |  | 自己評価 |
| start_date | 開始日 | DATE |  | ○ |  | 開始日 |
| supervisor_evaluation | 上司評価 | INTEGER |  | ○ |  | 上司評価 |
| supervisor_id | 上司ID | VARCHAR | 50 | ○ |  | 上司ID |
| support_needed | 必要サポート | TEXT |  | ○ |  | 必要サポート |
| target_date | 目標期限 | DATE |  | ○ |  | 目標期限 |
| target_value | 目標値 | DECIMAL | 15,2 | ○ |  | 目標値 |
| unit | 単位 | VARCHAR | 50 | ○ |  | 単位 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| created_by | 作成者ID | VARCHAR | 50 | ○ |  | 作成者ID |
| updated_by | 更新者ID | VARCHAR | 50 | ○ |  | 更新者ID |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_TRN_GoalProgress_goal_id | goal_id | ○ |  |
| idx_TRN_GoalProgress_employee_id | employee_id | × |  |
| idx_TRN_GoalProgress_supervisor_id | supervisor_id | × |  |
| idx_TRN_GoalProgress_category | goal_category | × |  |
| idx_TRN_GoalProgress_status | achievement_status | × |  |
| idx_TRN_GoalProgress_approval_status | approval_status | × |  |
| idx_TRN_GoalProgress_target_date | target_date | × |  |
| idx_TRN_GoalProgress_priority | priority_level | × |  |
| idx_TRN_GoalProgress_employee_period | employee_id, start_date, target_date | × |  |
| idx_TRN_GoalProgress_next_review | next_review_date | × |  |
| idx_trn_goalprogress_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_TRN_GoalProgress_employee | employee_id | MST_Employee | id | CASCADE | CASCADE | 外部キー制約 |
| fk_TRN_GoalProgress_supervisor | supervisor_id | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |
| fk_TRN_GoalProgress_approved_by | approved_by | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |
| fk_TRN_GoalProgress_career_plan | related_career_plan_id | MST_CareerPlan | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_goal_id | UNIQUE |  | goal_id一意制約 |
| chk_achievement_status | CHECK | achievement_status IN (...) | achievement_status値チェック制約 |
| chk_approval_status | CHECK | approval_status IN (...) | approval_status値チェック制約 |
| chk_goal_type | CHECK | goal_type IN (...) | goal_type値チェック制約 |

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

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 目標進捗トランザクションテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214007 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214908 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215001 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215054 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223433 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |