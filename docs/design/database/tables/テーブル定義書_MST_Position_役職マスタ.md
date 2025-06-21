# テーブル定義書: MST_Position

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Position |
| 論理名 | 役職マスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 17:21:48 |

## 概要

MST_Position（役職マスタ）は、組織内の役職・職位の階層構造と基本情報を管理するマスタテーブルです。
主な目的：
- 役職階層の構造管理（社長、部長、課長、主任等の階層関係）
- 役職基本情報の管理（役職名、役職コード、権限レベル等）
- 人事評価・昇進管理の基盤
- 給与・手当計算の基礎データ
- 権限・アクセス制御の役職単位設定
- 組織図・名刺作成の基礎データ
- 人事制度・キャリアパス管理
このテーブルは、人事管理、権限管理、給与計算、組織運営など、
企業の階層的組織運営の基盤となる重要なマスタデータです。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| position_code |  | VARCHAR |  | ○ |  |  |
| position_name |  | VARCHAR |  | ○ |  |  |
| position_name_short |  | VARCHAR |  | ○ |  |  |
| position_level |  | INT |  | ○ |  |  |
| position_rank |  | INT |  | ○ |  |  |
| position_category |  | ENUM |  | ○ |  |  |
| authority_level |  | INT |  | ○ |  |  |
| approval_limit |  | DECIMAL |  | ○ |  |  |
| salary_grade |  | VARCHAR |  | ○ |  |  |
| allowance_amount |  | DECIMAL |  | ○ |  |  |
| is_management |  | BOOLEAN |  | ○ | False |  |
| is_executive |  | BOOLEAN |  | ○ | False |  |
| requires_approval |  | BOOLEAN |  | ○ | False |  |
| can_hire |  | BOOLEAN |  | ○ | False |  |
| can_evaluate |  | BOOLEAN |  | ○ | False |  |
| position_status |  | ENUM |  | ○ | ACTIVE |  |
| sort_order |  | INT |  | ○ |  |  |
| description |  | TEXT |  | ○ |  |  |
| created_at | レコード作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | レコード更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_position_code | position_code | ○ |  |
| idx_position_level | position_level | × |  |
| idx_position_rank | position_rank | × |  |
| idx_position_category | position_category | × |  |
| idx_authority_level | authority_level | × |  |
| idx_salary_grade | salary_grade | × |  |
| idx_status | position_status | × |  |
| idx_management_flags | is_management, is_executive | × |  |
| idx_sort_order | sort_order | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_position_code | UNIQUE |  | position_code一意制約 |
| chk_position_level | CHECK | position_level > 0 | position_level正値チェック制約 |
| chk_authority_level | CHECK | authority_level > 0 | authority_level正値チェック制約 |
| chk_position_status | CHECK | position_status IN (...) | position_status値チェック制約 |

## サンプルデータ

| position_code | position_name | position_name_short | position_level | position_rank | position_category | authority_level | approval_limit | salary_grade | allowance_amount | is_management | is_executive | requires_approval | can_hire | can_evaluate | position_status | sort_order | description |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| POS001 | 代表取締役社長 | 社長 | 1 | 1 | EXECUTIVE | 10 | 999999999.99 | E1 | 500000.0 | True | True | True | True | True | ACTIVE | 1 | 会社の最高責任者として経営全般を統括 |
| POS002 | 取締役 | 取締役 | 2 | 1 | EXECUTIVE | 9 | 100000000.0 | E2 | 300000.0 | True | True | True | True | True | ACTIVE | 2 | 取締役会メンバーとして経営方針決定に参画 |
| POS003 | 部長 | 部長 | 3 | 1 | MANAGER | 7 | 10000000.0 | M1 | 100000.0 | True | False | True | True | True | ACTIVE | 3 | 部門の責任者として業務全般を管理 |

## 特記事項

- 役職レベルは階層の深さを表す（1が最上位）
- 同レベル内の序列は役職ランクで管理
- 権限レベルはシステムアクセス制御に使用
- 承認限度額は稟議・決裁システムと連携
- 管理職フラグは労働基準法上の管理監督者判定に使用
- 給与等級は給与計算システムと連携

## 業務ルール

- 役職コードは新設時に自動採番（POS + 3桁連番）
- 役員は必ず管理職フラグがtrueである必要がある
- 承認権限を持つ役職は承認限度額の設定が必要
- 廃止時は position_status を ABOLISHED に変更
- 役職レベルと権限レベルは原則として対応関係にある
- 管理職は評価権限を持つことを原則とする
- 役職手当は月額で設定し、給与計算時に使用

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 役職マスタテーブルの詳細定義 |