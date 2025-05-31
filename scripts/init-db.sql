-- 要求仕様ID: PLT.1-DB.1 - データベース初期化スクリプト
-- PostgreSQL 15 用初期化スクリプト

-- データベースの文字エンコーディング確認
SELECT current_setting('server_encoding');

-- 拡張機能の有効化
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- タイムゾーンの設定
SET timezone = 'Asia/Tokyo';

-- アプリケーション用ユーザーの作成
DO $$
BEGIN
    -- skill_userが存在しない場合のみ作成
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'skill_user') THEN
        CREATE USER skill_user WITH PASSWORD 'skill_password';
        RAISE NOTICE 'ユーザー skill_user を作成しました';
    ELSE
        RAISE NOTICE 'ユーザー skill_user は既に存在します';
    END IF;
END $$;

-- データベースへの権限付与
GRANT ALL PRIVILEGES ON DATABASE skill_report_db TO skill_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO skill_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO skill_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO skill_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO skill_user;

-- 将来作成されるオブジェクトへの権限付与
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO skill_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO skill_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO skill_user;

-- データベース初期化完了メッセージ
DO $$
BEGIN
    RAISE NOTICE 'スキル報告書WEBシステム データベース初期化完了';
    RAISE NOTICE 'データベース名: skill_report_db';
    RAISE NOTICE 'ユーザー: skill_user';
    RAISE NOTICE 'タイムゾーン: %', current_setting('timezone');
END $$;
