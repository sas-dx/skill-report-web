# テーブル定義書_MST_TrainingProgram_研修プログラム

## テーブル概要

| 項目 | 内容 |
|------|------|
| テーブル名（物理） | MST_TrainingProgram |
| テーブル名（論理） | 研修プログラム |
| 用途 | 研修プログラムの基本情報を管理するマスタテーブル |
| カテゴリ | マスタ系 |
| 主な利用機能 | 研修・教育管理 |
| 主な利用API | API-016, API-017 |
| 主な利用バッチ | BATCH-011 |
| 優先度 | 中 |

## カラム定義

| No | カラム名（物理） | カラム名（論理） | データ型 | 桁数 | NULL許可 | デフォルト値 | 主キー | 外部キー | 説明 |
|----|------------------|------------------|----------|------|----------|--------------|--------|----------|------|
| 1 | training_program_id | 研修プログラムID | VARCHAR | 20 | × | - | ○ | - | 研修プログラムの一意識別子 |
| 2 | tenant_id | テナントID | VARCHAR | 20 | × | - | - | MST_Tenant.tenant_id | テナント識別子 |
| 3 | program_code | プログラムコード | VARCHAR | 20 | × | - | - | - | 研修プログラムのコード |
| 4 | program_name | プログラム名 | VARCHAR | 100 | × | - | - | - | 研修プログラムの名称 |
| 5 | program_description | プログラム説明 | TEXT | - | ○ | NULL | - | - | 研修プログラムの詳細説明 |
| 6 | program_category | プログラムカテゴリ | VARCHAR | 50 | × | - | - | - | 研修カテゴリ（技術研修/ビジネス研修/資格取得等） |
| 7 | program_type | プログラム種別 | VARCHAR | 20 | × | - | - | - | 研修種別（集合研修/eラーニング/OJT/外部研修等） |
| 8 | target_audience | 対象者 | VARCHAR | 100 | ○ | NULL | - | - | 研修対象者の説明 |
| 9 | prerequisite | 受講前提条件 | TEXT | - | ○ | NULL | - | - | 受講に必要な前提条件 |
| 10 | learning_objectives | 学習目標 | TEXT | - | ○ | NULL | - | - | 研修の学習目標 |
| 11 | duration_hours | 研修時間 | DECIMAL | 5,2 | ○ | NULL | - | - | 研修時間（時間） |
| 12 | max_participants | 最大受講者数 | INT | - | ○ | NULL | - | - | 最大受講可能人数 |
| 13 | instructor_name | 講師名 | VARCHAR | 100 | ○ | NULL | - | - | 講師の名前 |
| 14 | instructor_profile | 講師プロフィール | TEXT | - | ○ | NULL | - | - | 講師の経歴・プロフィール |
| 15 | cost_per_person | 一人当たり費用 | DECIMAL | 10,2 | ○ | NULL | - | - | 受講者一人当たりの費用 |
| 16 | venue_type | 会場種別 | VARCHAR | 20 | ○ | NULL | - | - | 会場種別（社内/社外/オンライン等） |
| 17 | venue_details | 会場詳細 | VARCHAR | 200 | ○ | NULL | - | - | 会場の詳細情報 |
| 18 | materials_required | 必要教材 | TEXT | - | ○ | NULL | - | - | 研修に必要な教材・機材 |
| 19 | certification_available | 認定証発行 | BOOLEAN | - | × | FALSE | - | - | 修了認定証の発行有無 |
| 20 | pdu_points | PDUポイント | DECIMAL | 5,2 | ○ | NULL | - | - | 取得可能なPDUポイント |
| 21 | external_provider | 外部提供者 | VARCHAR | 100 | ○ | NULL | - | - | 外部研修の場合の提供者名 |
| 22 | external_url | 外部URL | VARCHAR | 500 | ○ | NULL | - | - | 外部研修の場合のURL |
| 23 | is_active | 有効フラグ | BOOLEAN | - | × | TRUE | - | - | プログラムの有効/無効状態 |
| 24 | display_order | 表示順序 | INT | - | × | 0 | - | - | 画面表示時の順序 |
| 25 | created_at | 作成日時 | TIMESTAMP | - | × | CURRENT_TIMESTAMP | - | - | レコード作成日時 |
| 26 | created_by | 作成者ID | VARCHAR | 20 | × | - | - | MST_UserAuth.user_id | レコード作成者 |
| 27 | updated_at | 更新日時 | TIMESTAMP | - | × | CURRENT_TIMESTAMP | - | - | レコード更新日時 |
| 28 | updated_by | 更新者ID | VARCHAR | 20 | × | - | - | MST_UserAuth.user_id | レコード更新者 |
| 29 | version | バージョン | INT | - | × | 1 | - | - | 楽観的排他制御用 |

## インデックス定義

| インデックス名 | 種別 | 対象カラム | 説明 |
|----------------|------|------------|------|
| PK_MST_TrainingProgram | PRIMARY KEY | training_program_id | 主キー |
| IDX_MST_TrainingProgram_tenant | INDEX | tenant_id | テナント検索用 |
| IDX_MST_TrainingProgram_code | INDEX | program_code | プログラムコード検索用 |
| IDX_MST_TrainingProgram_category | INDEX | program_category | カテゴリ検索用 |
| IDX_MST_TrainingProgram_type | INDEX | program_type | 種別検索用 |
| IDX_MST_TrainingProgram_active | INDEX | is_active | 有効フラグ検索用 |
| IDX_MST_TrainingProgram_display | INDEX | display_order | 表示順序用 |
| UNQ_MST_TrainingProgram_code | UNIQUE | tenant_id, program_code | テナント内プログラムコード一意制約 |

## 制約定義

| 制約名 | 種別 | 対象カラム | 説明 |
|--------|------|------------|------|
| PK_MST_TrainingProgram | PRIMARY KEY | training_program_id | 主キー制約 |
| FK_MST_TrainingProgram_tenant | FOREIGN KEY | tenant_id | テナントマスタ参照制約 |
| FK_MST_TrainingProgram_created_by | FOREIGN KEY | created_by | 作成者参照制約 |
| FK_MST_TrainingProgram_updated_by | FOREIGN KEY | updated_by | 更新者参照制約 |
| UNQ_MST_TrainingProgram_code | UNIQUE | tenant_id, program_code | テナント内プログラムコード一意制約 |
| CHK_MST_TrainingProgram_category | CHECK | program_category | program_category IN ('技術研修','ビジネス研修','資格取得','マネジメント','コンプライアンス','その他') |
| CHK_MST_TrainingProgram_type | CHECK | program_type | program_type IN ('集合研修','eラーニング','OJT','外部研修','セミナー','ワークショップ') |
| CHK_MST_TrainingProgram_venue | CHECK | venue_type | venue_type IN ('社内','社外','オンライン','ハイブリッド') |
| CHK_MST_TrainingProgram_duration | CHECK | duration_hours | duration_hours > 0 |
| CHK_MST_TrainingProgram_participants | CHECK | max_participants | max_participants > 0 |
| CHK_MST_TrainingProgram_cost | CHECK | cost_per_person | cost_per_person >= 0 |
| CHK_MST_TrainingProgram_pdu | CHECK | pdu_points | pdu_points >= 0 |
| CHK_MST_TrainingProgram_display_order | CHECK | display_order | display_order >= 0 |
| CHK_MST_TrainingProgram_version | CHECK | version | version > 0 |

## 関連テーブル

### 参照先テーブル
- MST_Tenant（テナント管理）
- MST_UserAuth（ユーザー認証情報）

### 参照元テーブル
- TRN_TrainingHistory（研修履歴）
- TRN_PDU（継続教育ポイント）

## 備考・注意事項

### 業務ルール
1. プログラムコードは同一テナント内で一意である必要がある
2. 研修時間は0より大きい値である必要がある
3. 最大受講者数は1以上である必要がある
4. 費用は0以上である必要がある
5. PDUポイントは0以上である必要がある
6. 削除は論理削除（is_active = FALSE）で行う

### 運用上の注意
- 研修プログラムの変更は既存の受講履歴に影響するため慎重に行う
- 外部研修の場合は提供者との契約状況を確認する
- 認定証発行の場合は発行プロセスを明確にする
- 費用情報は予算管理と連携する

### パフォーマンス考慮事項
- テナントIDでの検索が頻繁に行われるためインデックスを設定
- カテゴリ、種別での絞り込みが多いためインデックスを設定
- 有効フラグでの絞り込みが多いためインデックスを設定

### セキュリティ考慮事項
- テナント分離を確実に行い、他テナントのプログラムにアクセスできないようにする
- 研修プログラムの作成・更新には適切な権限チェックを行う
- 外部URLの安全性を確認する

### データ品質管理
- プログラム名、説明の入力内容を適切に検証する
- 講師情報の正確性を定期的に確認する
- 費用情報の妥当性をチェックする
- 外部研修の場合は提供者情報を最新に保つ
