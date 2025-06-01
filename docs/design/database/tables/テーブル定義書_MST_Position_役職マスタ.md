# テーブル定義書: MST_Position (役職マスタ)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_Position |
| 論理名 | 役職マスタ |
| カテゴリ | マスタ系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/MST_Position_details.yaml` で行ってください。



## 📝 テーブル概要

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


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  |  |  | マルチテナント識別子 |
| position_code | 役職コード | VARCHAR | 20 | ○ |  |  |  | 役職を一意に識別するコード（例：POS001） |
| position_name | 役職名 | VARCHAR | 100 | ○ |  |  |  | 役職の正式名称 |
| position_name_short | 役職名略称 | VARCHAR | 50 | ○ |  |  |  | 役職の略称・短縮名 |
| position_level | 役職レベル | INT |  | ○ |  |  |  | 役職の階層レベル（1:最上位、数値が大きいほど下位） |
| position_rank | 役職ランク | INT |  | ○ |  |  |  | 同レベル内での序列・ランク |
| position_category | 役職カテゴリ | ENUM |  | ○ |  |  |  | 役職のカテゴリ（EXECUTIVE:役員、MANAGER:管理職、SUPERVISOR:監督職、STAFF:一般職） |
| authority_level | 権限レベル | INT |  | ○ |  |  |  | システム権限レベル（1-10、数値が大きいほど高権限） |
| approval_limit | 承認限度額 | DECIMAL | 15,2 | ○ |  |  |  | 承認可能な金額の上限（円） |
| salary_grade | 給与等級 | VARCHAR | 10 | ○ |  |  |  | 給与計算用の等級コード |
| allowance_amount | 役職手当額 | DECIMAL | 10,2 | ○ |  |  |  | 月額役職手当（円） |
| is_management | 管理職フラグ | BOOLEAN |  | ○ |  |  |  | 管理職かどうか（労働基準法上の管理監督者判定） |
| is_executive | 役員フラグ | BOOLEAN |  | ○ |  |  |  | 役員かどうか |
| requires_approval | 承認権限フラグ | BOOLEAN |  | ○ |  |  |  | 承認権限を持つかどうか |
| can_hire | 採用権限フラグ | BOOLEAN |  | ○ |  |  |  | 採用権限を持つかどうか |
| can_evaluate | 評価権限フラグ | BOOLEAN |  | ○ |  |  |  | 人事評価権限を持つかどうか |
| position_status | 役職状態 | ENUM |  | ○ |  |  | ACTIVE | 役職の状態（ACTIVE:有効、INACTIVE:無効、ABOLISHED:廃止） |
| sort_order | 表示順序 | INT |  | ○ |  |  |  | 組織図等での表示順序 |
| description | 役職説明 | TEXT |  | ○ |  |  |  | 役職の責任・権限・業務内容の説明 |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_position_code | position_code | ○ | 役職コード検索用（一意） |
| idx_position_level | position_level | × | 役職レベル別検索用 |
| idx_position_rank | position_rank | × | 役職ランク別検索用 |
| idx_position_category | position_category | × | 役職カテゴリ別検索用 |
| idx_authority_level | authority_level | × | 権限レベル別検索用 |
| idx_salary_grade | salary_grade | × | 給与等級別検索用 |
| idx_status | position_status | × | 役職状態別検索用 |
| idx_management_flags | is_management, is_executive | × | 管理職・役員フラグ検索用 |
| idx_sort_order | sort_order | × | 表示順序検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_position_code | UNIQUE | position_code |  | 役職コード一意制約 |
| chk_position_level | CHECK |  | position_level > 0 | 役職レベル正値チェック制約 |
| chk_position_rank | CHECK |  | position_rank > 0 | 役職ランク正値チェック制約 |
| chk_authority_level | CHECK |  | authority_level BETWEEN 1 AND 10 | 権限レベル範囲チェック制約 |
| chk_position_category | CHECK |  | position_category IN ('EXECUTIVE', 'MANAGER', 'SUPERVISOR', 'STAFF') | 役職カテゴリ値チェック制約 |
| chk_position_status | CHECK |  | position_status IN ('ACTIVE', 'INACTIVE', 'ABOLISHED') | 役職状態値チェック制約 |
| chk_approval_limit | CHECK |  | approval_limit IS NULL OR approval_limit >= 0 | 承認限度額非負値チェック制約 |
| chk_allowance_amount | CHECK |  | allowance_amount IS NULL OR allowance_amount >= 0 | 役職手当額非負値チェック制約 |
| chk_sort_order | CHECK |  | sort_order IS NULL OR sort_order >= 0 | 表示順序非負値チェック制約 |

## 📊 サンプルデータ

```json
[
  {
    "position_code": "POS001",
    "position_name": "代表取締役社長",
    "position_name_short": "社長",
    "position_level": 1,
    "position_rank": 1,
    "position_category": "EXECUTIVE",
    "authority_level": 10,
    "approval_limit": 999999999.99,
    "salary_grade": "E1",
    "allowance_amount": 500000.0,
    "is_management": true,
    "is_executive": true,
    "requires_approval": true,
    "can_hire": true,
    "can_evaluate": true,
    "position_status": "ACTIVE",
    "sort_order": 1,
    "description": "会社の最高責任者として経営全般を統括"
  },
  {
    "position_code": "POS002",
    "position_name": "取締役",
    "position_name_short": "取締役",
    "position_level": 2,
    "position_rank": 1,
    "position_category": "EXECUTIVE",
    "authority_level": 9,
    "approval_limit": 100000000.0,
    "salary_grade": "E2",
    "allowance_amount": 300000.0,
    "is_management": true,
    "is_executive": true,
    "requires_approval": true,
    "can_hire": true,
    "can_evaluate": true,
    "position_status": "ACTIVE",
    "sort_order": 2,
    "description": "取締役会メンバーとして経営方針決定に参画"
  },
  {
    "position_code": "POS003",
    "position_name": "部長",
    "position_name_short": "部長",
    "position_level": 3,
    "position_rank": 1,
    "position_category": "MANAGER",
    "authority_level": 7,
    "approval_limit": 10000000.0,
    "salary_grade": "M1",
    "allowance_amount": 100000.0,
    "is_management": true,
    "is_executive": false,
    "requires_approval": true,
    "can_hire": true,
    "can_evaluate": true,
    "position_status": "ACTIVE",
    "sort_order": 3,
    "description": "部門の責任者として業務全般を管理"
  }
]
```

## 📌 特記事項

- 役職レベルは階層の深さを表す（1が最上位）
- 同レベル内の序列は役職ランクで管理
- 権限レベルはシステムアクセス制御に使用
- 承認限度額は稟議・決裁システムと連携
- 管理職フラグは労働基準法上の管理監督者判定に使用
- 給与等級は給与計算システムと連携

## 📋 業務ルール

- 役職コードは新設時に自動採番（POS + 3桁連番）
- 役員は必ず管理職フラグがtrueである必要がある
- 承認権限を持つ役職は承認限度額の設定が必要
- 廃止時は position_status を ABOLISHED に変更
- 役職レベルと権限レベルは原則として対応関係にある
- 管理職は評価権限を持つことを原則とする
- 役職手当は月額で設定し、給与計算時に使用
