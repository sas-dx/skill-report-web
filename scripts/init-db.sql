-- 要求仕様ID: PLT.1-DB.1 - データベース初期化スクリプト
-- PostgreSQL 15 用初期化スクリプト

-- データベースの文字エンコーディング確認
SELECT current_setting('server_encoding');

-- 拡張機能の有効化
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- タイムゾーンの設定
SET timezone = 'Asia/Tokyo';

-- 初期化完了ログ
INSERT INTO pg_stat_statements_info (dealloc) VALUES (0) ON CONFLICT DO NOTHING;

-- データベース初期化完了メッセージ
DO $$
BEGIN
    RAISE NOTICE 'スキル報告書WEBシステム データベース初期化完了';
    RAISE NOTICE 'データベース名: skill_report_db';
    RAISE NOTICE 'ユーザー: skill_user';
    RAISE NOTICE 'タイムゾーン: %', current_setting('timezone');
END $$;
