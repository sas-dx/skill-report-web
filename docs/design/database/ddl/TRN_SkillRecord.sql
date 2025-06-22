-- ============================================
-- テーブル: TRN_SkillRecord
-- 論理名: スキル情報
-- 説明: TRN_SkillRecord（スキル情報）は、組織内の全社員が保有するスキル・技術・資格等の詳細情報を管理するトランザクションテーブルです。

主な目的：
- 社員個人のスキルポートフォリオ管理（技術スキル、ビジネススキル、資格等）
- スキルレベルの客観的評価・管理（5段階評価システム）
- 自己評価と上司評価による多面的スキル評価
- プロジェクトアサインメントのためのスキルマッチング
- 人材育成計画・キャリア開発支援
- 組織全体のスキル可視化・分析
- 資格取得状況・有効期限管理

このテーブルは、人材配置の最適化、教育研修計画の策定、組織のスキルギャップ分析など、
戦略的人材マネジメントの基盤となる重要なデータを提供します。

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS TRN_SkillRecord;

CREATE TABLE TRN_SkillRecord (
    skillrecord_id SERIAL NOT NULL COMMENT 'TRN_SkillRecordの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    created_by VARCHAR(50) NOT NULL COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) NOT NULL COMMENT 'レコード更新者のユーザーID',
    PRIMARY KEY (skillrecord_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_trn_skillrecord_tenant_id ON TRN_SkillRecord (tenant_id);

-- 外部キー制約
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_employee FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_item FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_certification FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_category FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_assessor FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
