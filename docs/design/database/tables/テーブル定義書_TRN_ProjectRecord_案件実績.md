# テーブル定義書: TRN_ProjectRecord

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_ProjectRecord |
| 論理名 | 案件実績 |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-04 06:57:02 |

## 概要

TRN_ProjectRecord（案件実績）は、社員が参加したプロジェクト・案件の実績情報を管理するトランザクションテーブルです。

主な目的：
- プロジェクト参加履歴の記録・管理
- 担当役割・責任範囲の記録
- 使用技術・スキルの実績記録
- 成果・評価の記録
- キャリア形成・スキル証明の基盤

このテーブルにより、社員の実務経験を体系的に記録し、
スキル評価やキャリア開発の判断材料として活用できます。



## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| project_record_id | 案件実績ID | VARCHAR | 50 | ○ |  | 案件実績を一意に識別するID |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 参加した社員のID（MST_Employeeへの外部キー） |
| project_name | プロジェクト名 | VARCHAR | 200 | ○ |  | プロジェクト・案件の名称 |
| project_code | プロジェクトコード | VARCHAR | 50 | ○ |  | 社内プロジェクト管理コード |
| client_name | 顧客名 | VARCHAR | 100 | ○ |  | 顧客・クライアント名（機密情報のため暗号化） |
| project_type | プロジェクト種別 | ENUM |  | ○ |  | プロジェクトの種別（DEVELOPMENT:開発、MAINTENANCE:保守、CONSULTING:コンサル、RESEARCH:研究、OTHER:その他） |
| project_scale | プロジェクト規模 | ENUM |  | ○ |  | プロジェクトの規模（SMALL:小規模、MEDIUM:中規模、LARGE:大規模、ENTERPRISE:エンタープライズ） |
| start_date | 開始日 | DATE |  | ○ |  | プロジェクト参加開始日 |
| end_date | 終了日 | DATE |  | ○ |  | プロジェクト参加終了日（進行中の場合はNULL） |
| participation_rate | 参画率 | DECIMAL | 5,2 | ○ |  | プロジェクトへの参画率（%） |
| role_title | 担当役職 | VARCHAR | 100 | ○ |  | プロジェクト内での役職・ポジション |
| responsibilities | 担当業務 | TEXT |  | ○ |  | 具体的な担当業務・責任範囲 |
| technologies_used | 使用技術 | TEXT |  | ○ |  | プロジェクトで使用した技術・ツール（JSON形式） |
| skills_applied | 適用スキル | TEXT |  | ○ |  | プロジェクトで活用したスキル（JSON形式） |
| achievements | 成果・実績 | TEXT |  | ○ |  | プロジェクトでの具体的な成果・実績 |
| challenges_faced | 課題・困難 | TEXT |  | ○ |  | 直面した課題や困難とその対応 |
| lessons_learned | 学んだこと | TEXT |  | ○ |  | プロジェクトから学んだ知識・経験 |
| team_size | チーム規模 | INTEGER |  | ○ |  | プロジェクトチームの人数 |
| budget_range | 予算規模 | ENUM |  | ○ |  | プロジェクトの予算規模（UNDER_1M:100万円未満、UNDER_10M:1000万円未満、UNDER_100M:1億円未満、OVER_100M:1億円以上） |
| project_status | プロジェクト状況 | ENUM |  | ○ | ONGOING | プロジェクトの状況（ONGOING:進行中、COMPLETED:完了、SUSPENDED:中断、CANCELLED:中止） |
| evaluation_score | 評価点数 | DECIMAL | 3,1 | ○ |  | プロジェクトでの評価点数（1.0-5.0） |
| evaluation_comment | 評価コメント | TEXT |  | ○ |  | 上司・PMからの評価コメント |
| is_confidential | 機密フラグ | BOOLEAN |  | ○ | False | 機密プロジェクトかどうか |
| is_public_reference | 公開参照可能フラグ | BOOLEAN |  | ○ | False | 社外への参照情報として公開可能か |
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
| idx_project_record_id | project_record_id | ○ | 案件実績ID検索用（一意） |
| idx_employee_id | employee_id | × | 社員ID検索用 |
| idx_project_name | project_name | × | プロジェクト名検索用 |
| idx_project_code | project_code | × | プロジェクトコード検索用 |
| idx_project_type | project_type | × | プロジェクト種別検索用 |
| idx_date_range | start_date, end_date | × | 期間検索用 |
| idx_project_status | project_status | × | プロジェクト状況検索用 |
| idx_employee_period | employee_id, start_date, end_date | × | 社員別期間検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_project_record_employee | employee_id | MST_Employee | id | CASCADE | RESTRICT | 社員への外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_project_record_id | UNIQUE |  | 案件実績ID一意制約 |
| chk_project_type | CHECK | project_type IN ('DEVELOPMENT', 'MAINTENANCE', 'CONSULTING', 'RESEARCH', 'OTHER') | プロジェクト種別値チェック制約 |
| chk_project_scale | CHECK | project_scale IN ('SMALL', 'MEDIUM', 'LARGE', 'ENTERPRISE') | プロジェクト規模値チェック制約 |
| chk_budget_range | CHECK | budget_range IN ('UNDER_1M', 'UNDER_10M', 'UNDER_100M', 'OVER_100M') | 予算規模値チェック制約 |
| chk_project_status | CHECK | project_status IN ('ONGOING', 'COMPLETED', 'SUSPENDED', 'CANCELLED') | プロジェクト状況値チェック制約 |
| chk_date_range | CHECK | end_date IS NULL OR start_date <= end_date | 開始日・終了日の整合性チェック制約 |
| chk_participation_rate | CHECK | participation_rate IS NULL OR (participation_rate >= 0 AND participation_rate <= 100) | 参画率範囲チェック制約 |
| chk_evaluation_score | CHECK | evaluation_score IS NULL OR (evaluation_score >= 1.0 AND evaluation_score <= 5.0) | 評価点数範囲チェック制約 |
| chk_team_size | CHECK | team_size IS NULL OR team_size > 0 | チーム規模正数チェック制約 |

## サンプルデータ

| project_record_id | employee_id | project_name | project_code | client_name | project_type | project_scale | start_date | end_date | participation_rate | role_title | responsibilities | technologies_used | skills_applied | achievements | challenges_faced | lessons_learned | team_size | budget_range | project_status | evaluation_score | evaluation_comment | is_confidential | is_public_reference |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| PRJ_REC_001 | EMP000001 | 顧客管理システム刷新プロジェクト | CRM2024_001 | 株式会社サンプル | DEVELOPMENT | LARGE | 2024-01-15 | 2024-12-31 | 80.0 | テックリード | システム設計、開発チームリード、技術選定 | ["Java", "Spring Boot", "PostgreSQL", "React", "Docker"] | ["システム設計", "チームマネジメント", "技術選定"] | 予定より2週間早期リリース、性能要件120%達成 | レガシーシステムとの連携、短納期対応 | マイクロサービス設計の重要性、チーム間コミュニケーション | 8 | UNDER_100M | COMPLETED | 4.5 | 技術リーダーシップを発揮し、プロジェクトを成功に導いた | False | True |
| PRJ_REC_002 | EMP000002 | AI画像解析システム開発 | AI2024_002 | 機密プロジェクト | RESEARCH | MEDIUM | 2024-03-01 | None | 100.0 | AIエンジニア | 機械学習モデル開発、データ前処理、精度改善 | ["Python", "TensorFlow", "OpenCV", "AWS SageMaker"] | ["機械学習", "画像処理", "データ分析"] | 認識精度95%達成、処理速度30%向上 | 学習データ不足、モデル精度向上 | データ品質の重要性、MLOpsの必要性 | 4 | UNDER_10M | ONGOING | None | None | True | False |

## 特記事項

- 顧客名は機密情報のため暗号化必須
- 使用技術・適用スキルはJSON形式で柔軟に管理
- 進行中プロジェクトは end_date = NULL で管理
- 機密プロジェクトは is_confidential = true で管理
- 評価は完了後に記録（進行中は NULL）
- 参画率は工数ベースでの参加割合

## 業務ルール

- 案件実績IDは一意である必要がある
- 開始日は終了日以前である必要がある
- 進行中プロジェクトは終了日をNULLに設定
- 参画率は0-100%の範囲で設定
- 評価点数は1.0-5.0の範囲で設定
- 機密プロジェクトは公開参照不可
- 使用技術・スキルはスキルマスタとの整合性を保つ
- チーム規模は1人以上で設定

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 案件実績テーブルの詳細定義 |
