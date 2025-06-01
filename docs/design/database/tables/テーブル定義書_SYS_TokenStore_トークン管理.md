# テーブル定義書: SYS_TokenStore

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_TokenStore |
| 論理名 | トークン管理 |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-01 20:40:26 |

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
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| id | ID | VARCHAR | 50 | ○ |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | マルチテナント識別子 |
| user_id | ユーザーID | VARCHAR | 50 | ○ |  | トークンの所有者ユーザーID（MST_UserAuthへの参照） |
| token_type | トークンタイプ | ENUM |  | ○ |  | トークンの種類（ACCESS:アクセストークン、REFRESH:リフレッシュトークン、SESSION:セッション） |
| token_value | トークン値 | TEXT |  | ○ |  | トークンの値（暗号化必須） |
| token_hash | トークンハッシュ | VARCHAR | 255 | ○ |  | トークン値のハッシュ値（検索用） |
| expires_at | 有効期限 | TIMESTAMP |  | ○ |  | トークンの有効期限 |
| issued_at | 発行日時 | TIMESTAMP |  | ○ |  | トークンの発行日時 |
| last_used_at | 最終使用日時 | TIMESTAMP |  | ○ |  | トークンの最終使用日時 |
| client_ip | クライアントIP | VARCHAR | 45 | ○ |  | トークン発行時のクライアントIPアドレス（IPv6対応） |
| user_agent | ユーザーエージェント | TEXT |  | ○ |  | トークン発行時のユーザーエージェント情報 |
| device_fingerprint | デバイスフィンガープリント | VARCHAR | 255 | ○ |  | デバイス識別用フィンガープリント |
| scope | スコープ | TEXT |  | ○ |  | トークンのアクセススコープ（JSON形式） |
| is_revoked | 無効化フラグ | BOOLEAN |  | ○ | False | トークンが無効化されているかどうか |
| revoked_at | 無効化日時 | TIMESTAMP |  | ○ |  | トークンが無効化された日時 |
| revoked_reason | 無効化理由 | ENUM |  | ○ |  | 無効化の理由（LOGOUT:ログアウト、EXPIRED:期限切れ、SECURITY:セキュリティ、ADMIN:管理者操作） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_token_store_hash | token_hash | ○ | トークンハッシュ検索用（一意） |
| idx_token_store_user_type | user_id, token_type | × | ユーザー別トークンタイプ検索用 |
| idx_token_store_expires | expires_at, is_revoked | × | 有効期限・無効化状態検索用 |
| idx_token_store_tenant_user | tenant_id, user_id | × | テナント別ユーザー検索用 |
| idx_token_store_issued | issued_at | × | 発行日時検索用 |
| idx_token_store_last_used | last_used_at | × | 最終使用日時検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_token_store_user | user_id | MST_UserAuth | id | CASCADE | CASCADE | ユーザー認証情報への外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_token_store_hash | UNIQUE |  | トークンハッシュ一意制約 |
| chk_token_store_type | CHECK | token_type IN ('ACCESS', 'REFRESH', 'SESSION') | トークンタイプ値チェック制約 |
| chk_token_store_revoked_reason | CHECK | revoked_reason IS NULL OR revoked_reason IN ('LOGOUT', 'EXPIRED', 'SECURITY', 'ADMIN') | 無効化理由値チェック制約 |
| chk_token_store_expires_after_issued | CHECK | expires_at > issued_at | 有効期限が発行日時より後であることをチェック |
| chk_token_store_revoked_consistency | CHECK | (is_revoked = false AND revoked_at IS NULL AND revoked_reason IS NULL) OR (is_revoked = true AND revoked_at IS NOT NULL) | 無効化フラグと無効化日時の整合性チェック |

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
