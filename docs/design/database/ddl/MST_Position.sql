-- ============================================
-- テーブル: MST_Position
-- 論理名: 役職マスタ
-- 説明: MST_Position（役職マスタ）は、組織内の役職・職位の階層構造と基本情報を管理するマスタテーブルです。

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

-- 作成日: 2025-06-21 23:07:48
-- ============================================

DROP TABLE IF EXISTS MST_Position;

CREATE TABLE MST_Position (
    position_id SERIAL NOT NULL COMMENT 'MST_Positionの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT 'False' COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (position_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_position_tenant_id ON MST_Position (tenant_id);
