# テーブル定義書: TRN_ProjectRecord

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_ProjectRecord |
| 論理名 | 案件実績 |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-24 23:05:57 |

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
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| project_code | プロジェクトコード | VARCHAR | 50 | ○ |  | プロジェクトコード |
| project_name | プロジェクト名 | VARCHAR | 200 | ○ |  | プロジェクト名 |
| achievements | 成果・実績 | TEXT |  | ○ |  | 成果・実績 |
| budget_range | 予算規模 | ENUM |  | ○ |  | 予算規模 |
| challenges_faced | 課題・困難 | TEXT |  | ○ |  | 課題・困難 |
| client_name | 顧客名 | VARCHAR | 100 | ○ |  | 顧客名 |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 社員ID |
| end_date | 終了日 | DATE |  | ○ |  | 終了日 |
| evaluation_comment | 評価コメント | TEXT |  | ○ |  | 評価コメント |
| evaluation_score | 評価点数 | DECIMAL | 3,1 | ○ |  | 評価点数 |
| is_confidential | 機密フラグ | BOOLEAN |  | ○ | False | 機密フラグ |
| is_public_reference | 公開参照可能フラグ | BOOLEAN |  | ○ | False | 公開参照可能フラグ |
| lessons_learned | 学んだこと | TEXT |  | ○ |  | 学んだこと |
| participation_rate | 参画率 | DECIMAL | 5,2 | ○ |  | 参画率 |
| project_record_id | 案件実績ID | VARCHAR | 50 | ○ |  | 案件実績ID |
| project_scale | プロジェクト規模 | ENUM |  | ○ |  | プロジェクト規模 |
| project_status | プロジェクト状況 | ENUM |  | ○ | ONGOING | プロジェクト状況 |
| project_type | プロジェクト種別 | ENUM |  | ○ |  | プロジェクト種別 |
| projectrecord_id | TRN_ProjectRecordの主キー | SERIAL |  | × |  | TRN_ProjectRecordの主キー |
| responsibilities | 担当業務 | TEXT |  | ○ |  | 担当業務 |
| role_title | 担当役職 | VARCHAR | 100 | ○ |  | 担当役職 |
| skills_applied | 適用スキル | TEXT |  | ○ |  | 適用スキル |
| start_date | 開始日 | DATE |  | ○ |  | 開始日 |
| team_size | チーム規模 | INTEGER |  | ○ |  | チーム規模 |
| technologies_used | 使用技術 | TEXT |  | ○ |  | 使用技術 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| created_by | 作成者ID | VARCHAR | 50 | ○ |  | 作成者ID |
| updated_by | 更新者ID | VARCHAR | 50 | ○ |  | 更新者ID |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_project_record_id | project_record_id | ○ |  |
| idx_employee_id | employee_id | × |  |
| idx_project_name | project_name | × |  |
| idx_project_code | project_code | × |  |
| idx_project_type | project_type | × |  |
| idx_date_range | start_date, end_date | × |  |
| idx_project_status | project_status | × |  |
| idx_employee_period | employee_id, start_date, end_date | × |  |
| idx_trn_projectrecord_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_project_record_employee | employee_id | MST_Employee | id | CASCADE | RESTRICT | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_project_record_id | UNIQUE |  | project_record_id一意制約 |
| chk_project_status | CHECK | project_status IN (...) | project_status値チェック制約 |
| chk_project_type | CHECK | project_type IN (...) | project_type値チェック制約 |

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
- 案件実績IDは一意である必要がある
- 開始日は終了日以前である必要がある
- 進行中プロジェクトは終了日をNULLに設定
- 参画率は0-100%の範囲で設定
- 評価点数は1.0-5.0の範囲で設定
- 機密プロジェクトは公開参照不可
- 使用技術・スキルはスキルマスタとの整合性を保つ
- チーム規模は1人以上で設定

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 案件実績テーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214007 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214908 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215001 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215054 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222632 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223433 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |