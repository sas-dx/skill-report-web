# テーブル定義書: TRN_ProjectRecord

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_ProjectRecord |
| 論理名 | 案件実績 |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-21 17:20:34 |

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
| project_record_id |  | VARCHAR |  | ○ |  |  |
| employee_id |  | VARCHAR |  | ○ |  |  |
| project_name |  | VARCHAR |  | ○ |  |  |
| project_code |  | VARCHAR |  | ○ |  |  |
| client_name |  | VARCHAR |  | ○ |  |  |
| project_type |  | ENUM |  | ○ |  |  |
| project_scale |  | ENUM |  | ○ |  |  |
| start_date |  | DATE |  | ○ |  |  |
| end_date |  | DATE |  | ○ |  |  |
| participation_rate |  | DECIMAL |  | ○ |  |  |
| role_title |  | VARCHAR |  | ○ |  |  |
| responsibilities |  | TEXT |  | ○ |  |  |
| technologies_used |  | TEXT |  | ○ |  |  |
| skills_applied |  | TEXT |  | ○ |  |  |
| achievements |  | TEXT |  | ○ |  |  |
| challenges_faced |  | TEXT |  | ○ |  |  |
| lessons_learned |  | TEXT |  | ○ |  |  |
| team_size |  | INTEGER |  | ○ |  |  |
| budget_range |  | ENUM |  | ○ |  |  |
| project_status |  | ENUM |  | ○ | ONGOING |  |
| evaluation_score |  | DECIMAL |  | ○ |  |  |
| evaluation_comment |  | TEXT |  | ○ |  |  |
| is_confidential |  | BOOLEAN |  | ○ | False |  |
| is_public_reference |  | BOOLEAN |  | ○ | False |  |
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_by | レコード作成者のユーザーID | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | レコード更新者のユーザーID | VARCHAR | 50 | × |  | レコード更新者のユーザーID |
| created_at | レコード作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | レコード更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード更新日時 |

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

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_trn_projectrecord | PRIMARY KEY | id | 主キー制約 |
| uk_project_record_id | UNIQUE |  | project_record_id一意制約 |
| chk_project_type | CHECK | project_type IN (...) | project_type値チェック制約 |
| chk_project_status | CHECK | project_status IN (...) | project_status値チェック制約 |

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