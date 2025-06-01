-- スキル項目マスタテーブル作成DDL
CREATE TABLE MST_SkillItem (
    id VARCHAR(50) NOT NULL COMMENT 'ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    skill_code VARCHAR(20) COMMENT 'スキルコード',
    skill_name VARCHAR(100) COMMENT 'スキル名',
    skill_category_id VARCHAR(50) COMMENT 'スキルカテゴリID',
    skill_type ENUM COMMENT 'スキル種別',
    difficulty_level INT COMMENT '習得難易度',
    importance_level INT COMMENT '重要度',
    PRIMARY KEY (id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_active (is_active),
    INDEX idx_created_at (created_at),
    UNIQUE INDEX idx_skill_code (skill_code),
    INDEX idx_skill_category (skill_category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='スキル項目マスタ';
