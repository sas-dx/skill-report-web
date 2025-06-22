# テーブル定義書: SYS_TokenStore

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_TokenStore |
| 論理名 | トークン管理 |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-21 22:02:17 |

## 概要

SYS_TokenStore（トークン管理）は、認証・認可システムで使用するトークン情報を管理するシステムテーブルです。
主な目的：
- JWTアクセストークンの管理
- リフレッシュトークンの管理
- セッション管理
- トークンの有効期限管理
- セキュリティ監査のためのトークン履歴管理
このテーブルは、認証・認可システムの基盤となる重要なシステムデータです。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| tokenstore_id | SYS_TokenStoreの主キー | SERIAL |  | × |  | SYS_TokenStoreの主キー |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_token_store_user | None | None | None | CASCADE | CASCADE | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_sys_tokenstore | PRIMARY KEY | tokenstore_id, id | 主キー制約 |

## サンプルデータ

| id | tenant_id | user_id | token_type | token_value | token_hash | expires_at | issued_at | last_used_at | client_ip | user_agent | device_fingerprint | scope | is_revoked | revoked_at | revoked_reason |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| TS001 | TENANT001 | USER001 | ACCESS | eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... | a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0 | 2025-06-01 20:00:00 | 2025-06-01 19:00:00 | 2025-06-01 19:30:00 | 192.168.1.100 | Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 | fp_abc123def456 | ["read:profile", "write:skills", "read:goals"] | False | None | None |
| TS002 | TENANT001 | USER001 | REFRESH | rt_xyz789abc123def456ghi789jkl012mno345 | b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1 | 2025-06-08 19:00:00 | 2025-06-01 19:00:00 | None | 192.168.1.100 | Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 | fp_abc123def456 | ["refresh"] | False | None | None |

## 特記事項

- トークン値は暗号化必須、検索にはハッシュ値を使用
- 有効期限は作成から1日経過で自動削除される
- セキュリティ監査のため発行・使用履歴を記録
- デバイスフィンガープリントによる不正アクセス検知に対応
- スコープ情報はJSON形式で柔軟な権限管理に対応
- 無効化されたトークンも監査のため一定期間保持
- IPv6アドレスに対応したクライアントIP管理

## 業務ルール

- トークンハッシュは全システムで一意である必要がある
- 有効期限切れのトークンは自動的に無効化される
- 無効化されたトークンは再利用不可
- 同一ユーザーの同一タイプトークンは複数発行可能
- リフレッシュトークンの有効期限はアクセストークンより長期
- セッショントークンはブラウザセッション管理用
- トークン使用時は最終使用日時を更新
- セキュリティ上の理由で無効化されたトークンは即座に削除対象

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - トークン管理システムテーブルの詳細定義 |