-- ============================================
-- テーブル: TRN_PDU
-- 論理名: 継続教育ポイント
-- 説明: TRN_PDU（継続教育ポイント）は、社員が取得した継続教育ポイント（Professional Development Units）を管理するトランザクションテーブルです。

主な目的：
- PDU取得履歴の記録・管理
- 資格維持要件の追跡
- 学習活動の定量化
- 継続教育計画の進捗管理
- 資格更新の支援

このテーブルにより、社員の継続的な学習活動を体系的に記録し、
資格維持や専門性向上の支援を効率的に行うことができます。

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS TRN_PDU;

CREATE TABLE TRN_PDU (
    pdu_id SERIAL NOT NULL COMMENT 'TRN_PDUの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    created_by VARCHAR(50) NOT NULL COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) NOT NULL COMMENT 'レコード更新者のユーザーID',
    PRIMARY KEY (pdu_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_trn_pdu_tenant_id ON TRN_PDU (tenant_id);

-- 外部キー制約
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_employee FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_certification FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_approver FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_training FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_project FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
