-- ============================================
-- テーブル: SYS_SkillMatrix
-- 論理名: スキルマップ
-- 説明: スキルマップテーブルは、社員のスキル評価とスキル項目の関連を管理するシステムテーブルです。

主な目的：
- 社員とスキル項目の多対多関係を管理
- スキル評価レベルの記録
- スキル評価履歴の管理

このテーブルは、スキル管理システムの中核となるテーブルで、
社員のスキル可視化やスキル分析の基盤データを提供します。

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS SYS_SkillMatrix;

CREATE TABLE SYS_SkillMatrix (
    skillmatrix_id SERIAL NOT NULL COMMENT 'SYS_SkillMatrixの主キー',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (skillmatrix_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 外部キー制約
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT fk_SYS_SkillMatrix_employee FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT fk_SYS_SkillMatrix_skill FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
