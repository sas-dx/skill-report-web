# テーブル定義書: MST_Department

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Department |
| 論理名 | 部署マスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-01 20:40:25 |

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
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  | マルチテナント識別子 |
| department_code | 部署コード | VARCHAR | 20 | ○ |  | 部署を一意に識別するコード（例：DEPT001） |
| department_name | 部署名 | VARCHAR | 100 | ○ |  | 部署の正式名称 |
| department_name_short | 部署名略称 | VARCHAR | 50 | ○ |  | 部署の略称・短縮名 |
| parent_department_id | 親部署ID | VARCHAR | 50 | ○ |  | 上位部署のID（MST_Departmentへの自己参照外部キー） |
| department_level | 部署レベル | INT |  | ○ |  | 組織階層のレベル（1:本部、2:部、3:課、4:チーム等） |
| department_type | 部署種別 | ENUM |  | ○ |  | 部署の種別（HEADQUARTERS:本部、DIVISION:事業部、DEPARTMENT:部、SECTION:課、TEAM:チーム） |
| manager_id | 部署長ID | VARCHAR | 50 | ○ |  | 部署長の社員ID（MST_Employeeへの外部キー） |
| deputy_manager_id | 副部署長ID | VARCHAR | 50 | ○ |  | 副部署長の社員ID（MST_Employeeへの外部キー） |
| cost_center_code | コストセンターコード | VARCHAR | 20 | ○ |  | 予算管理用のコストセンターコード |
| budget_amount | 予算額 | DECIMAL | 15,2 | ○ |  | 年間予算額（円） |
| location | 所在地 | VARCHAR | 200 | ○ |  | 部署の物理的な所在地・フロア等 |
| phone_number | 代表電話番号 | VARCHAR | 20 | ○ |  | 部署の代表電話番号 |
| email_address | 代表メールアドレス | VARCHAR | 255 | ○ |  | 部署の代表メールアドレス |
| establishment_date | 設立日 | DATE |  | ○ |  | 部署の設立・新設日 |
| abolition_date | 廃止日 | DATE |  | ○ |  | 部署の廃止・統合日 |
| department_status | 部署状態 | ENUM |  | ○ | ACTIVE | 部署の状態（ACTIVE:有効、INACTIVE:無効、MERGED:統合、ABOLISHED:廃止） |
| sort_order | 表示順序 | INT |  | ○ |  | 組織図等での表示順序 |
| description | 部署説明 | TEXT |  | ○ |  | 部署の役割・業務内容の説明 |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_department_code | department_code | ○ | 部署コード検索用（一意） |
| idx_parent_department | parent_department_id | × | 親部署別検索用 |
| idx_department_level | department_level | × | 部署レベル別検索用 |
| idx_department_type | department_type | × | 部署種別検索用 |
| idx_manager | manager_id | × | 部署長別検索用 |
| idx_status | department_status | × | 部署状態別検索用 |
| idx_cost_center | cost_center_code | × | コストセンター別検索用 |
| idx_sort_order | sort_order | × | 表示順序検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_department_parent | parent_department_id | MST_Department | id | CASCADE | SET NULL | 親部署への自己参照外部キー |
| fk_department_manager | manager_id | MST_Employee | id | CASCADE | SET NULL | 部署長への外部キー |
| fk_department_deputy | deputy_manager_id | MST_Employee | id | CASCADE | SET NULL | 副部署長への外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_department_code | UNIQUE |  | 部署コード一意制約 |
| chk_department_level | CHECK | department_level > 0 | 部署レベル正値チェック制約 |
| chk_department_type | CHECK | department_type IN ('HEADQUARTERS', 'DIVISION', 'DEPARTMENT', 'SECTION', 'TEAM') | 部署種別値チェック制約 |
| chk_department_status | CHECK | department_status IN ('ACTIVE', 'INACTIVE', 'MERGED', 'ABOLISHED') | 部署状態値チェック制約 |
| chk_budget_amount | CHECK | budget_amount IS NULL OR budget_amount >= 0 | 予算額非負値チェック制約 |
| chk_sort_order | CHECK | sort_order IS NULL OR sort_order >= 0 | 表示順序非負値チェック制約 |

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

## 業務ルール

- 部署コードは設立時に自動採番（DEPT + 3桁連番）
- 親部署が廃止される場合は子部署の再配置が必要
- 部署長は当該部署または上位部署の社員のみ設定可能
- 廃止時は department_status を ABOLISHED に変更
- 統合時は department_status を MERGED に変更
- 予算額は年度初めに設定・更新
- 組織変更は月初めに実施することを原則とする

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 部署マスタテーブルの詳細定義 |
