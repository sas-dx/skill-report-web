# テーブル定義書: MST_Department

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Department |
| 論理名 | 部署マスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 22:56:16 |

## 概要

MST_Department（部署マスタ）は、組織の部署・組織単位の階層構造と基本情報を管理するマスタテーブルです。
主な目的：
- 組織階層の構造管理（部署、課、チーム等の階層関係）
- 部署基本情報の管理（部署名、部署コード、責任者等）
- 組織変更履歴の管理（統廃合、新設、移管等）
- 予算・コスト管理の組織単位設定
- 権限・アクセス制御の組織単位設定
- 人事異動・配置管理の基盤
- 組織図・レポート作成の基礎データ
このテーブルは、人事管理、権限管理、予算管理、レポート作成など、
組織運営の様々な業務プロセスの基盤となる重要なマスタデータです。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| abolition_date | 廃止日 | DATE |  | ○ |  | 廃止日 |
| budget_amount | 予算額 | DECIMAL | 15,2 | ○ |  | 予算額 |
| cost_center_code | コストセンターコード | VARCHAR | 20 | ○ |  | コストセンターコード |
| department_code | 部署コード | VARCHAR | 20 | ○ |  | 部署コード |
| department_id | MST_Departmentの主キー | SERIAL |  | × |  | MST_Departmentの主キー |
| department_level | 部署レベル | INT |  | ○ |  | 部署レベル |
| department_name | 部署名 | VARCHAR | 100 | ○ |  | 部署名 |
| department_name_short | 部署名略称 | VARCHAR | 50 | ○ |  | 部署名略称 |
| department_status | 部署状態 | ENUM |  | ○ | ACTIVE | 部署状態 |
| department_type | 部署種別 | ENUM |  | ○ |  | 部署種別 |
| deputy_manager_id | 副部署長ID | VARCHAR | 50 | ○ |  | 副部署長ID |
| description | 部署説明 | TEXT |  | ○ |  | 部署説明 |
| email_address | 代表メールアドレス | VARCHAR | 255 | ○ |  | 代表メールアドレス |
| establishment_date | 設立日 | DATE |  | ○ |  | 設立日 |
| location | 所在地 | VARCHAR | 200 | ○ |  | 所在地 |
| manager_id | 部署長ID | VARCHAR | 50 | ○ |  | 部署長ID |
| parent_department_id | 親部署ID | VARCHAR | 50 | ○ |  | 親部署ID |
| phone_number | 代表電話番号 | VARCHAR | 20 | ○ |  | 代表電話番号 |
| sort_order | 表示順序 | INT |  | ○ |  | 表示順序 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_department_code | department_code | ○ |  |
| idx_parent_department | parent_department_id | × |  |
| idx_department_level | department_level | × |  |
| idx_department_type | department_type | × |  |
| idx_manager | manager_id | × |  |
| idx_status | department_status | × |  |
| idx_cost_center | cost_center_code | × |  |
| idx_sort_order | sort_order | × |  |
| idx_mst_department_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_department_parent | parent_department_id | MST_Department | id | CASCADE | SET NULL | 外部キー制約 |
| fk_department_manager | manager_id | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |
| fk_department_deputy | deputy_manager_id | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_department_code | UNIQUE |  | department_code一意制約 |
| chk_department_level | CHECK | department_level > 0 | department_level正値チェック制約 |
| chk_department_status | CHECK | department_status IN (...) | department_status値チェック制約 |
| chk_department_type | CHECK | department_type IN (...) | department_type値チェック制約 |

## サンプルデータ

| department_code | department_name | department_name_short | parent_department_id | department_level | department_type | manager_id | deputy_manager_id | cost_center_code | budget_amount | location | phone_number | email_address | establishment_date | abolition_date | department_status | sort_order | description |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| DEPT001 | 経営企画本部 | 経営企画 | None | 1 | HEADQUARTERS | EMP000001 | None | CC001 | 50000000.0 | 本社ビル 10F | 03-1234-5678 | planning@company.com | 2020-04-01 | None | ACTIVE | 1 | 会社全体の経営戦略立案・推進を担当 |
| DEPT002 | システム開発部 | システム開発 | DEPT001 | 2 | DEPARTMENT | EMP000002 | EMP000003 | CC002 | 120000000.0 | 本社ビル 8F | 03-1234-5679 | dev@company.com | 2020-04-01 | None | ACTIVE | 2 | 社内システムの開発・保守・運用を担当 |

## 特記事項

- 組織階層は自己参照外部キーで表現
- 部署レベルは階層の深さを表す（1が最上位）
- 廃止された部署も履歴として保持（論理削除）
- コストセンターコードは予算管理システムと連携
- 部署長・副部署長は必須ではない（空席の場合もある）
- 表示順序は組織図作成時に使用
- 部署コードは設立時に自動採番（DEPT + 3桁連番）
- 親部署が廃止される場合は子部署の再配置が必要
- 部署長は当該部署または上位部署の社員のみ設定可能
- 廃止時は department_status を ABOLISHED に変更
- 統合時は department_status を MERGED に変更
- 予算額は年度初めに設定・更新
- 組織変更は月初めに実施することを原則とする

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 部署マスタテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214905 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_214959 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215052 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222630 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223432 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |