# テーブル定義書: SYS_TokenStore

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_TokenStore |
| 論理名 | トークン管理 |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-24 22:56:15 |

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
| id | ID | VARCHAR | 50 | ○ |  | ID |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | テナントID |
| client_ip | クライアントIP | VARCHAR | 45 | ○ |  | クライアントIP |
| device_fingerprint | デバイスフィンガープリント | VARCHAR | 255 | ○ |  | デバイスフィンガープリント |
| expires_at | 有効期限 | TIMESTAMP |  | ○ |  | 有効期限 |
| is_revoked | 無効化フラグ | BOOLEAN |  | ○ | False | 無効化フラグ |
| issued_at | 発行日時 | TIMESTAMP |  | ○ |  | 発行日時 |
| last_used_at | 最終使用日時 | TIMESTAMP |  | ○ |  | 最終使用日時 |
| revoked_at | 無効化日時 | TIMESTAMP |  | ○ |  | 無効化日時 |
| revoked_reason | 無効化理由 | ENUM |  | ○ |  | 無効化理由 |
| scope | スコープ | TEXT |  | ○ |  | スコープ |
| token_hash | トークンハッシュ | VARCHAR | 255 | ○ |  | トークンハッシュ |
| token_type | トークンタイプ | ENUM |  | ○ |  | トークンタイプ |
| token_value | トークン値 | TEXT |  | ○ |  | トークン値 |
| tokenstore_id | SYS_TokenStoreの主キー | SERIAL |  | × |  | SYS_TokenStoreの主キー |
| user_agent | ユーザーエージェント | TEXT |  | ○ |  | ユーザーエージェント |
| user_id | ユーザーID | VARCHAR | 50 | ○ |  | ユーザーID |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_token_store_hash | token_hash | ○ |  |
| idx_token_store_user_type | user_id, token_type | × |  |
| idx_token_store_expires | expires_at, is_revoked | × |  |
| idx_token_store_tenant_user | tenant_id, user_id | × |  |
| idx_token_store_issued | issued_at | × |  |
| idx_token_store_last_used | last_used_at | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_token_store_user | user_id | MST_UserAuth | user_id | CASCADE | CASCADE | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_token_hash | UNIQUE |  | token_hash一意制約 |
| chk_token_type | CHECK | token_type IN (...) | token_type値チェック制約 |

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
- トークンハッシュは全システムで一意である必要がある
- 有効期限切れのトークンは自動的に無効化される
- 無効化されたトークンは再利用不可
- 同一ユーザーの同一タイプトークンは複数発行可能
- リフレッシュトークンの有効期限はアクセストークンより長期
- セッショントークンはブラウザセッション管理用
- トークン使用時は最終使用日時を更新
- セキュリティ上の理由で無効化されたトークンは即座に削除対象

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - トークン管理システムテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214007 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214908 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215001 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215054 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223433 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |