# テーブル定義書：スキル階層マスタ (MST_SkillHierarchy)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-009 |
| **テーブル名** | MST_SkillHierarchy |
| **論理名** | スキル階層マスタ |
| **カテゴリ** | マスタ系 |
| **優先度** | 高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-31 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
スキル階層マスタテーブル（MST_SkillHierarchy）は、システムで管理するスキル項目の階層構造を定義するマスタテーブルです。スキルカテゴリ、サブカテゴリ、スキル項目の3階層構造を管理し、スキル評価や検索の基盤となります。このテーブルは管理者によって維持され、技術トレンドや組織のニーズに応じて定期的に更新されます。

### 2.2 関連API
- [API-007](../api/specs/API仕様書_API-007.md) - スキル階層管理API

### 2.3 関連バッチ
- [BATCH-005](../batch/specs/バッチ定義書_BATCH-005.md) - スキルマスタ同期バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | skill_id | スキルID | VARCHAR | 50 | × | ○ | - | - | スキル項目を一意に識別するID |
| 2 | skill_name | スキル名 | VARCHAR | 200 | × | - | - | - | スキル項目の名称 |
| 3 | parent_skill_id | 親スキルID | VARCHAR | 50 | ○ | - | ○ | NULL | 親スキル項目のID（階層構造用） |
| 4 | hierarchy_level | 階層レベル | INTEGER | 1 | × | - | - | - | 階層レベル（1:カテゴリ、2:サブカテゴリ、3:スキル項目） |
| 5 | display_order | 表示順 | INTEGER | 4 | × | - | - | 9999 | 同一階層内での表示順序 |
| 6 | description | スキル説明 | TEXT | - | ○ | - | - | NULL | スキル項目の詳細説明 |
| 7 | criteria_none | 評価基準× | TEXT | - | ○ | - | - | NULL | 評価「×」（未経験）の基準説明 |
| 8 | criteria_basic | 評価基準△ | TEXT | - | ○ | - | - | NULL | 評価「△」（基礎知識あり）の基準説明 |
| 9 | criteria_intermediate | 評価基準○ | TEXT | - | ○ | - | - | NULL | 評価「○」（実務経験あり）の基準説明 |
| 10 | criteria_advanced | 評価基準◎ | TEXT | - | ○ | - | - | NULL | 評価「◎」（高度な知識・経験あり）の基準説明 |
| 11 | related_certifications | 関連資格 | TEXT | - | ○ | - | - | NULL | 関連する資格情報（カンマ区切り） |
| 12 | related_trainings | 関連研修 | TEXT | - | ○ | - | - | NULL | 関連する研修情報（カンマ区切り） |
| 13 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | 所属テナントのID |
| 14 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | スキル項目が有効かどうか |
| 15 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 16 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 17 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 18 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | skill_id | 主キー |
| idx_skill_name | INDEX | skill_name | スキル名による検索用 |
| idx_parent_skill | INDEX | parent_skill_id | 親スキルによる検索用 |
| idx_hierarchy_level | INDEX | hierarchy_level | 階層レベルによる検索用 |
| idx_display_order | INDEX | display_order | 表示順による検索用 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_active | INDEX | is_active | 有効フラグによる検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_skill_hierarchy | PRIMARY KEY | skill_id | 主キー制約 |
| fk_parent_skill | FOREIGN KEY | parent_skill_id | MST_SkillHierarchy.skill_id |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_hierarchy_level | CHECK | hierarchy_level | hierarchy_level IN (1, 2, 3) |
| chk_display_order | CHECK | display_order | display_order >= 0 |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_SkillHierarchy | parent_skill_id | 1:N | 親スキル項目（自己参照） |
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_SkillHierarchy | skill_id | 1:N | 子スキル項目（自己参照） |
| TRN_SkillRecord | skill_id | 1:N | スキル評価記録 |
| SYS_SkillIndex | skill_id | 1:N | スキル検索インデックス |
| SYS_SkillMatrix | skill_id | 1:N | スキルマップ |

## 5. データ仕様

### 5.1 階層レベル定義
| レベル | 名称 | 説明 | 例 |
|--------|------|------|-----|
| 1 | カテゴリ | 大分類 | プログラミング言語、データベース、フレームワーク |
| 2 | サブカテゴリ | 中分類 | Webフロントエンド、バックエンド、モバイル |
| 3 | スキル項目 | 小分類 | Java、Python、React、Spring |

### 5.2 評価基準定義
| 評価 | 記号 | 説明 |
|------|------|------|
| 未経験 | × | 知識・経験なし |
| 基礎知識 | △ | 基本的な知識あり |
| 実務経験 | ○ | 実務での使用経験あり |
| 高度 | ◎ | 高度な知識・豊富な経験あり |

### 5.3 データ例
```sql
-- カテゴリレベル
INSERT INTO MST_SkillHierarchy (
    skill_id, skill_name, parent_skill_id, hierarchy_level,
    display_order, description, tenant_id, created_by, updated_by
) VALUES (
    'CAT_001',
    'プログラミング言語',
    NULL,
    1,
    1,
    'プログラミング言語に関するスキル',
    'TENANT_001',
    'system',
    'system'
);

-- サブカテゴリレベル
INSERT INTO MST_SkillHierarchy (
    skill_id, skill_name, parent_skill_id, hierarchy_level,
    display_order, description, tenant_id, created_by, updated_by
) VALUES (
    'SUB_001',
    'Webバックエンド',
    'CAT_001',
    2,
    1,
    'Webアプリケーションのサーバーサイド開発',
    'TENANT_001',
    'system',
    'system'
);

-- スキル項目レベル
INSERT INTO MST_SkillHierarchy (
    skill_id, skill_name, parent_skill_id, hierarchy_level,
    display_order, description, criteria_none, criteria_basic,
    criteria_intermediate, criteria_advanced, tenant_id, created_by, updated_by
) VALUES (
    'SKILL_001',
    'Java',
    'SUB_001',
    3,
    1,
    'Java言語を使用したアプリケーション開発',
    '全く知識がない状態',
    '基本的な文法を理解している',
    '実際のプロジェクトで開発経験がある',
    'フレームワークを使いこなし、設計も可能',
    'TENANT_001',
    'system',
    'system'
);
```

### 5.4 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 500件 | カテゴリ50、サブカテゴリ150、スキル項目300 |
| 年間増加件数 | 50件 | 新技術・新スキルの追加 |
| 5年後想定件数 | 750件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし（データ量が少ないため）

### 6.3 アーカイブ
- アーカイブ条件：論理削除から2年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | hierarchy_level, is_active | 階層別スキル一覧 |
| SELECT | 高 | parent_skill_id | 子スキル一覧 |
| SELECT | 中 | skill_name | スキル名検索 |
| SELECT | 中 | tenant_id | テナント別スキル |
| INSERT | 低 | - | 新規スキル追加 |
| UPDATE | 低 | skill_id | スキル情報更新 |

### 7.2 パフォーマンス要件
- SELECT：10ms以内
- INSERT：50ms以内
- UPDATE：50ms以内
- DELETE：50ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| skill_admin | ○ | ○ | ○ | × | スキル管理者 |
| manager | ○ | × | × | × | 管理職 |
| employee | ○ | × | × | × | 一般社員 |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含まない
- 機密情報：含まない（スキル定義情報）
- 暗号化：不要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存スキルマスタ
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 移行スクリプト例
```sql
-- 既存データの移行
INSERT INTO MST_SkillHierarchy (
    skill_id, skill_name, parent_skill_id, hierarchy_level,
    display_order, description, tenant_id, created_by, updated_by
)
SELECT 
    skill_code,
    skill_name,
    parent_skill_code,
    level_no,
    sort_order,
    description,
    'TENANT_001',
    'migration',
    'migration'
FROM old_skill_master
WHERE is_valid = 1;
```

### 9.3 DDL
```sql
CREATE TABLE MST_SkillHierarchy (
    skill_id VARCHAR(50) NOT NULL,
    skill_name VARCHAR(200) NOT NULL,
    parent_skill_id VARCHAR(50) NULL,
    hierarchy_level INTEGER NOT NULL,
    display_order INTEGER NOT NULL DEFAULT 9999,
    description TEXT NULL,
    criteria_none TEXT NULL,
    criteria_basic TEXT NULL,
    criteria_intermediate TEXT NULL,
    criteria_advanced TEXT NULL,
    related_certifications TEXT NULL,
    related_trainings TEXT NULL,
    tenant_id VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    PRIMARY KEY (skill_id),
    INDEX idx_skill_name (skill_name),
    INDEX idx_parent_skill (parent_skill_id),
    INDEX idx_hierarchy_level (hierarchy_level),
    INDEX idx_display_order (display_order),
    INDEX idx_tenant (tenant_id),
    INDEX idx_active (is_active),
    CONSTRAINT fk_skill_parent FOREIGN KEY (parent_skill_id) REFERENCES MST_SkillHierarchy(skill_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_skill_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_skill_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_skill_hierarchy_level CHECK (hierarchy_level IN (1, 2, 3)),
    CONSTRAINT chk_skill_display_order CHECK (display_order >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 10. 特記事項

1. **階層構造**: 3レベル（カテゴリ/サブカテゴリ/スキル項目）の階層構造を自己参照で実現
2. **評価基準**: 各スキル項目に4段階評価（×/△/○/◎）の基準を定義
3. **表示順制御**: display_orderにより同一階層内での表示順序を制御
4. **関連情報**: 関連資格・研修情報をテキストで管理（将来的には正規化を検討）
5. **論理削除**: is_activeフラグによる論理削除で既存評価データを保護
6. **テナント分離**: マルチテナント対応でテナント別のスキル体系を管理
7. **自己参照制約**: 親子関係の循環参照を防ぐためのアプリケーション制御が必要
8. **技術トレンド対応**: 定期的なスキル項目の見直しと追加が必要
9. **移行考慮**: 既存システムからの段階的移行に対応
10. **検索最適化**: スキル名、階層レベル等の検索パフォーマンスを重視

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-31 | システムアーキテクト | 初版作成（階層構造スキル管理対応） |
