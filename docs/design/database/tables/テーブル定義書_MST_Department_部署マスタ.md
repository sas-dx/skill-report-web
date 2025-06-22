# テーブル定義書: MST_Department

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Department |
| 論理名 | 部署マスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 23:07:48 |

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
| department_id | MST_Departmentの主キー | SERIAL |  | × |  | MST_Departmentの主キー |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_mst_department_tenant_id | tenant_id | × | テナントID検索用インデックス |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_department_parent | None | None | None | CASCADE | SET NULL | 外部キー制約 |
| fk_department_manager | None | None | None | CASCADE | SET NULL | 外部キー制約 |
| fk_department_deputy | None | None | None | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_mst_department | PRIMARY KEY | department_id | 主キー制約 |
| uk_id | UNIQUE |  | id一意制約 |

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