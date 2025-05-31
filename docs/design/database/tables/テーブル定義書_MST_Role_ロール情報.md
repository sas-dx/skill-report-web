# テーブル定義書：ロール情報 (MST_Role)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-002 |
| **テーブル名** | MST_Role |
| **論理名** | ロール情報 |
| **カテゴリ** | マスタ系 |
| **優先度** | 高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-29 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
ロール情報テーブル（MST_Role）は、システム内で定義されるロール（役割）の情報を管理します。各ロールには権限レベルが設定され、ユーザーに割り当てることでアクセス制御を実現します。ロールは階層構造を持ち、上位ロールは下位ロールの権限を継承します。

### 2.2 関連API
- [API-003](../api/specs/API仕様書_API-003.md) - ロール管理API

### 2.3 関連バッチ
- [BATCH-003](../batch/specs/バッチ定義書_BATCH-003.md) - セキュリティスキャンバッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | role_id | ロールID | VARCHAR | 50 | × | ○ | - | - | ロールを一意に識別するID |
| 2 | role_name | ロール名 | VARCHAR | 100 | × | - | - | - | ロールの表示名 |
| 3 | description | 説明 | VARCHAR | 500 | ○ | - | - | NULL | ロールの説明文 |
| 4 | level | 権限レベル | INTEGER | 2 | × | - | - | 0 | ロールの権限レベル（数値が大きいほど権限が高い） |
| 5 | parent_role_id | 親ロールID | VARCHAR | 50 | ○ | - | ○ | NULL | 親ロールのID（階層構造用） |
| 6 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | ロールが有効かどうか |
| 7 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 8 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 9 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 10 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | role_id | 主キー |
| idx_role_name | UNIQUE | role_name | ロール名の一意性を保証するインデックス |
| idx_parent_role | INDEX | parent_role_id | 親ロールによる検索を高速化 |
| idx_level | INDEX | level | 権限レベルによる検索を高速化 |
| idx_active | INDEX | is_active | 有効フラグによる検索を高速化 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_role | PRIMARY KEY | role_id | 主キー制約 |
| uq_role_name | UNIQUE | role_name | ロール名の一意性を保証する制約 |
| fk_parent_role | FOREIGN KEY | parent_role_id | MST_Role.role_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_level | CHECK | level | 0以上の値のみ許可 |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Role | parent_role_id | 1:N | 自己参照（親ロール） |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_UserRole | role_id | 1:N | ロールに割り当てられたユーザー |
| MST_Permission | role_id | 1:N | ロールに割り当てられた権限 |
| MST_Role | parent_role_id | 1:N | 自己参照（子ロール） |

## 5. データ仕様

### 5.1 データ例
```sql
-- 基本ロールの初期データ
INSERT INTO MST_Role (
    role_id, role_name, description, level, parent_role_id, 
    is_active, created_by, updated_by
) VALUES 
('ADMIN', '管理者', 'システム全体の管理権限を持つロール', 100, NULL, TRUE, 'system', 'system'),
('MANAGER', '管理職', '部門管理や承認権限を持つロール', 50, NULL, TRUE, 'system', 'system'),
('USER', '一般ユーザー', '基本的な操作権限を持つロール', 10, NULL, TRUE, 'system', 'system'),
('GUEST', 'ゲスト', '参照のみ可能な制限付きロール', 1, NULL, TRUE, 'system', 'system');
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 10件 | 基本ロール + カスタムロール |
| 年間増加件数 | 5件 | 新規ロール追加 |
| 5年後想定件数 | 35件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：論理削除から3年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | role_id | ロール情報取得 |
| SELECT | 高 | is_active = TRUE | 有効ロール一覧取得 |
| SELECT | 中 | parent_role_id | 階層構造取得 |
| UPDATE | 低 | role_id | ロール情報更新 |
| INSERT | 低 | - | 新規ロール作成 |

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
| security_admin | ○ | ○ | ○ | × | セキュリティ管理者 |
| application | ○ | × | × | × | アプリケーション |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含まない
- 機密情報：含む（権限情報）
- 暗号化：不要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存権限管理システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE MST_Role (
    role_id VARCHAR(50) NOT NULL,
    role_name VARCHAR(100) NOT NULL,
    description VARCHAR(500) NULL,
    level INTEGER NOT NULL DEFAULT 0,
    parent_role_id VARCHAR(50) NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    PRIMARY KEY (role_id),
    UNIQUE KEY idx_role_name (role_name),
    INDEX idx_parent_role (parent_role_id),
    INDEX idx_level (level),
    INDEX idx_active (is_active),
    CONSTRAINT fk_role_parent FOREIGN KEY (parent_role_id) REFERENCES MST_Role(role_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_role_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_role_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_role_level CHECK (level >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 10. 特記事項

1. ロールの階層構造は、parent_role_idを使用して表現
2. 権限の継承は、アプリケーションロジックで実装（親ロールの権限を子ロールが継承）
3. システム初期構築時に基本ロール（ADMIN, MANAGER, USER, GUEST）を作成
4. ロールの削除は論理削除（is_active=FALSE）を基本とし、物理削除は慎重に行うこと
5. 権限レベルは数値が大きいほど高い権限を表す（ADMIN=100, MANAGER=50, USER=10, GUEST=1）

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-29 | システムアーキテクト | 初版作成 |
| 1.1 | 2025-05-31 | システムアーキテクト | 新フォーマットに変更、詳細情報追加 |
