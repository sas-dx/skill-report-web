# テーブル定義書_MST_SkillItem_スキル項目マスタ

## テーブル概要

| 項目 | 内容 |
|------|------|
| テーブル名（物理） | MST_SkillItem |
| テーブル名（論理） | スキル項目マスタ |
| 用途 | 個別のスキル項目を管理するマスタテーブル |
| カテゴリ | マスタ系 |
| 主な利用機能 | スキル管理 |
| 主な利用API | API-008, API-011 |
| 主な利用バッチ | BATCH-005, BATCH-006 |
| 優先度 | 高 |

## カラム定義

| No | カラム名（物理） | カラム名（論理） | データ型 | 桁数 | NULL許可 | デフォルト値 | 主キー | 外部キー | 説明 |
|----|------------------|------------------|----------|------|----------|--------------|--------|----------|------|
| 1 | skill_item_id | スキル項目ID | VARCHAR | 20 | × | - | ○ | - | スキル項目の一意識別子 |
| 2 | tenant_id | テナントID | VARCHAR | 20 | × | - | - | MST_Tenant.tenant_id | テナント識別子 |
| 3 | skill_category_id | スキルカテゴリID | VARCHAR | 20 | × | - | - | MST_SkillCategory.skill_category_id | スキルカテゴリ識別子 |
| 4 | skill_hierarchy_id | スキル階層ID | VARCHAR | 20 | ○ | NULL | - | MST_SkillHierarchy.skill_hierarchy_id | スキル階層識別子 |
| 5 | skill_item_name | スキル項目名 | VARCHAR | 100 | × | - | - | - | スキル項目の名称 |
| 6 | skill_item_description | スキル項目説明 | TEXT | - | ○ | NULL | - | - | スキル項目の詳細説明 |
| 7 | skill_level_max | 最大スキルレベル | INT | - | × | 5 | - | - | このスキル項目の最大評価レベル |
| 8 | evaluation_criteria | 評価基準 | TEXT | - | ○ | NULL | - | - | スキル評価の基準 |
| 9 | required_evidence | 必要証跡 | VARCHAR | 500 | ○ | NULL | - | - | スキル証明に必要な証跡の説明 |
| 10 | display_order | 表示順序 | INT | - | × | 0 | - | - | 画面表示時の順序 |
| 11 | is_active | 有効フラグ | BOOLEAN | - | × | TRUE | - | - | スキル項目の有効/無効状態 |
| 12 | created_at | 作成日時 | TIMESTAMP | - | × | CURRENT_TIMESTAMP | - | - | レコード作成日時 |
| 13 | created_by | 作成者ID | VARCHAR | 20 | × | - | - | MST_UserAuth.user_id | レコード作成者 |
| 14 | updated_at | 更新日時 | TIMESTAMP | - | × | CURRENT_TIMESTAMP | - | - | レコード更新日時 |
| 15 | updated_by | 更新者ID | VARCHAR | 20 | × | - | - | MST_UserAuth.user_id | レコード更新者 |
| 16 | version | バージョン | INT | - | × | 1 | - | - | 楽観的排他制御用 |

## インデックス定義

| インデックス名 | 種別 | 対象カラム | 説明 |
|----------------|------|------------|------|
| PK_MST_SkillItem | PRIMARY KEY | skill_item_id | 主キー |
| IDX_MST_SkillItem_tenant | INDEX | tenant_id | テナント検索用 |
| IDX_MST_SkillItem_category | INDEX | skill_category_id | カテゴリ検索用 |
| IDX_MST_SkillItem_hierarchy | INDEX | skill_hierarchy_id | 階層検索用 |
| IDX_MST_SkillItem_active | INDEX | is_active | 有効フラグ検索用 |
| IDX_MST_SkillItem_display | INDEX | display_order | 表示順序用 |

## 制約定義

| 制約名 | 種別 | 対象カラム | 説明 |
|--------|------|------------|------|
| PK_MST_SkillItem | PRIMARY KEY | skill_item_id | 主キー制約 |
| FK_MST_SkillItem_tenant | FOREIGN KEY | tenant_id | テナントマスタ参照制約 |
| FK_MST_SkillItem_category | FOREIGN KEY | skill_category_id | スキルカテゴリマスタ参照制約 |
| FK_MST_SkillItem_hierarchy | FOREIGN KEY | skill_hierarchy_id | スキル階層マスタ参照制約 |
| FK_MST_SkillItem_created_by | FOREIGN KEY | created_by | 作成者参照制約 |
| FK_MST_SkillItem_updated_by | FOREIGN KEY | updated_by | 更新者参照制約 |
| CHK_MST_SkillItem_level_max | CHECK | skill_level_max | skill_level_max > 0 AND skill_level_max <= 10 |
| CHK_MST_SkillItem_display_order | CHECK | display_order | display_order >= 0 |
| CHK_MST_SkillItem_version | CHECK | version | version > 0 |

## 関連テーブル

### 参照先テーブル
- MST_Tenant（テナント管理）
- MST_SkillCategory（スキルカテゴリマスタ）
- MST_SkillHierarchy（スキル階層マスタ）
- MST_UserAuth（ユーザー認証情報）

### 参照元テーブル
- TRN_SkillRecord（スキル評価記録）
- TRN_SkillEvidence（スキル証跡）
- SYS_SkillIndex（スキル検索インデックス）
- SYS_SkillMatrix（スキルマップ）

## 備考・注意事項

### 業務ルール
1. スキル項目は必ずスキルカテゴリに属する必要がある
2. スキル階層は任意だが、設定する場合は有効な階層である必要がある
3. 最大スキルレベルは1-10の範囲で設定可能
4. 同一テナント内でのスキル項目名の重複は許可しない
5. 削除は論理削除（is_active = FALSE）で行う

### 運用上の注意
- スキル項目の変更は既存の評価データに影響するため慎重に行う
- 評価基準は明確に定義し、評価者間での認識齟齬を防ぐ
- 表示順序は管理画面での操作性を考慮して設定する

### パフォーマンス考慮事項
- テナントIDでの検索が頻繁に行われるためインデックスを設定
- カテゴリ別、階層別の検索も多いためインデックスを設定
- 有効フラグでの絞り込みが多いためインデックスを設定

### セキュリティ考慮事項
- テナント分離を確実に行い、他テナントのデータにアクセスできないようにする
- スキル項目の作成・更新には適切な権限チェックを行う
