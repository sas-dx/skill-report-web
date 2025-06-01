# テーブル定義書: MST_JobType

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_JobType |
| 論理名 | 職種マスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-01 20:40:25 |

## 概要

MST_JobType（職種マスタ）は、組織内の職種分類と各職種の基本情報を管理するマスタテーブルです。

主な目的：
- 職種の体系的な分類・管理
- 職種別スキル要件の定義基盤
- 人材配置・採用計画の基準
- キャリアパス・昇進要件の管理
- 職種別評価基準の設定

このテーブルにより、社員のキャリア開発や適材適所の人材配置、
職種別スキル要件の管理を効率的に行うことができます。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  | マルチテナント識別子 |
| job_type_code | 職種コード | VARCHAR | 20 | ○ |  | 職種を一意に識別するコード（例：SE、PM、QA、BA） |
| job_type_name | 職種名 | VARCHAR | 100 | ○ |  | 職種の正式名称 |
| job_type_name_en | 職種名（英語） | VARCHAR | 100 | ○ |  | 英語での職種名称 |
| job_category | 職種カテゴリ | ENUM |  | ○ |  | 職種の大分類（ENGINEERING:エンジニアリング、MANAGEMENT:マネジメント、SALES:営業、SUPPORT:サポート、OTHER:その他） |
| job_level | 職種レベル | ENUM |  | ○ |  | 職種の階層レベル（JUNIOR:ジュニア、SENIOR:シニア、LEAD:リード、MANAGER:マネージャー、DIRECTOR:ディレクター） |
| description | 職種説明 | TEXT |  | ○ |  | 職種の詳細説明・役割・責任範囲 |
| required_experience_years | 必要経験年数 | INTEGER |  | ○ |  | 職種に就くために必要な経験年数（目安） |
| salary_grade_min | 給与グレード下限 | INTEGER |  | ○ |  | 職種の給与グレード下限値 |
| salary_grade_max | 給与グレード上限 | INTEGER |  | ○ |  | 職種の給与グレード上限値 |
| career_path | キャリアパス | TEXT |  | ○ |  | 職種からの一般的なキャリアパス・昇進ルート |
| required_certifications | 必要資格 | TEXT |  | ○ |  | 職種に必要または推奨される資格（JSON形式で複数格納） |
| required_skills | 必要スキル | TEXT |  | ○ |  | 職種に必要なスキル（JSON形式で複数格納） |
| department_affinity | 部署親和性 | TEXT |  | ○ |  | 職種が配属されやすい部署（JSON形式で複数格納） |
| remote_work_eligible | リモートワーク可否 | BOOLEAN |  | ○ | False | リモートワークが可能な職種かどうか |
| travel_frequency | 出張頻度 | ENUM |  | ○ |  | 出張の頻度（NONE:なし、LOW:低、MEDIUM:中、HIGH:高） |
| sort_order | 表示順序 | INTEGER |  | ○ | 0 | 職種一覧での表示順序 |
| is_active | 有効フラグ | BOOLEAN |  | ○ | True | 職種が有効かどうか |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_job_type_code | job_type_code | ○ | 職種コード検索用（一意） |
| idx_job_type_name | job_type_name | × | 職種名検索用 |
| idx_job_category | job_category | × | 職種カテゴリ検索用 |
| idx_job_level | job_level | × | 職種レベル検索用 |
| idx_category_level | job_category, job_level | × | カテゴリ・レベル複合検索用 |
| idx_remote_eligible | remote_work_eligible, is_active | × | リモートワーク可能職種検索用 |
| idx_sort_order | sort_order | × | 表示順序検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_job_type_code | UNIQUE |  | 職種コード一意制約 |
| chk_job_category | CHECK | job_category IN ('ENGINEERING', 'MANAGEMENT', 'SALES', 'SUPPORT', 'OTHER') | 職種カテゴリ値チェック制約 |
| chk_job_level | CHECK | job_level IN ('JUNIOR', 'SENIOR', 'LEAD', 'MANAGER', 'DIRECTOR') | 職種レベル値チェック制約 |
| chk_travel_frequency | CHECK | travel_frequency IN ('NONE', 'LOW', 'MEDIUM', 'HIGH') | 出張頻度値チェック制約 |
| chk_experience_years | CHECK | required_experience_years IS NULL OR required_experience_years >= 0 | 必要経験年数非負数チェック制約 |
| chk_salary_grade | CHECK | salary_grade_min IS NULL OR salary_grade_max IS NULL OR salary_grade_min <= salary_grade_max | 給与グレード範囲チェック制約 |

## サンプルデータ

| job_type_code | job_type_name | job_type_name_en | job_category | job_level | description | required_experience_years | salary_grade_min | salary_grade_max | career_path | required_certifications | required_skills | department_affinity | remote_work_eligible | travel_frequency | sort_order | is_active |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| SE | システムエンジニア | Systems Engineer | ENGINEERING | SENIOR | システムの設計・開発・テストを担当するエンジニア | 3 | 3 | 6 | SE → シニアSE → テックリード → エンジニアリングマネージャー | ["基本情報技術者", "応用情報技術者"] | ["Java", "SQL", "システム設計", "要件定義"] | ["開発部", "システム部"] | True | LOW | 1 | True |
| PM | プロジェクトマネージャー | Project Manager | MANAGEMENT | MANAGER | プロジェクトの計画・実行・管理を統括する責任者 | 5 | 5 | 8 | SE → リーダー → PM → 部門マネージャー | ["PMP", "プロジェクトマネージャ試験"] | ["プロジェクト管理", "リーダーシップ", "コミュニケーション", "リスク管理"] | ["開発部", "PMO"] | True | MEDIUM | 2 | True |
| QA | 品質保証エンジニア | Quality Assurance Engineer | ENGINEERING | SENIOR | ソフトウェアの品質保証・テスト設計・実行を担当 | 2 | 3 | 6 | QA → シニアQA → QAリード → QAマネージャー | ["JSTQB", "ソフトウェア品質技術者資格"] | ["テスト設計", "自動化テスト", "品質管理", "バグ分析"] | ["品質保証部", "開発部"] | True | NONE | 3 | True |

## 特記事項

- 職種コードは組織内で一意である必要がある
- 必要資格・スキル・部署親和性はJSON形式で柔軟に管理
- 給与グレードは人事制度との連携で使用
- キャリアパスは社員のキャリア開発指針として活用
- リモートワーク可否は働き方改革・採用要件で参照
- 論理削除は is_active フラグで管理

## 業務ルール

- 職種コードは英数字・アンダースコアのみ使用可能
- 職種レベルは組織の階層構造と整合性を保つ
- 給与グレードは下限 ≤ 上限の関係を維持
- 必要経験年数は職種レベルと整合性を保つ
- リモートワーク可否は業務特性を考慮して設定
- 出張頻度は職種の業務内容に応じて適切に設定
- 表示順序は職種の重要度・階層に応じて設定

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 職種マスタテーブルの詳細定義 |
