# API定義書_API-700_キャリア初期データ取得API

## 基本情報

| 項目 | 内容 |
|------|------|
| API ID | API-700 |
| API名 | キャリア初期データ取得API |
| 概要 | キャリアプラン画面の初期表示に必要なデータを取得する |
| 要求仕様ID | CAR.1-PLAN.1 |
| 関連画面 | SCR-CAR-Plan (キャリアプラン画面) |
| 作成日 | 2025-06-24 |
| 更新日 | 2025-06-24 |

## API仕様

### エンドポイント
```
GET /api/career/init
```

### リクエスト

#### ヘッダー
| パラメータ名 | 型 | 必須 | 説明 |
|-------------|----|----|------|
| x-user-id | string | ○ | ユーザーID（認証情報から取得） |

#### パラメータ
なし

#### リクエスト例
```http
GET /api/career/init
x-user-id: emp_001
```

### レスポンス

#### 成功時 (200 OK)

```json
{
  "success": true,
  "data": {
    "career_goal": {
      "id": "plan_001",
      "target_position": "pos_001",
      "target_date": "2027-12-31",
      "target_description": "シニアエンジニアを目指す",
      "current_level": "JUNIOR",
      "target_level": "SENIOR",
      "progress_percentage": 30.5,
      "plan_status": "ACTIVE",
      "last_review_date": "2025-06-01",
      "next_review_date": "2025-12-01"
    },
    "skill_categories": [
      {
        "id": "CAT_001",
        "name": "プログラミング",
        "short_name": "プログラミング",
        "type": "TECHNICAL",
        "parent_id": null,
        "level": 1,
        "description": "プログラミングスキル",
        "icon_url": "/icons/programming.svg",
        "color_code": "#3399cc"
      }
    ],
    "positions": [
      {
        "id": "pos_001",
        "name": "シニアエンジニア",
        "short_name": "SE",
        "level": 3,
        "rank": 3,
        "category": "ENGINEER",
        "authority_level": 3,
        "is_management": false,
        "is_executive": false,
        "description": "シニアレベルのエンジニア"
      }
    ]
  },
  "timestamp": "2025-06-24T08:22:00.000Z"
}
```

#### エラー時 (500 Internal Server Error)

```json
{
  "success": false,
  "error": {
    "code": "CAREER_INIT_DATA_ERROR",
    "message": "キャリア初期データの取得に失敗しました",
    "details": "具体的なエラー内容"
  },
  "timestamp": "2025-06-24T08:22:00.000Z"
}
```

## データ構造詳細

### career_goal オブジェクト

| フィールド名 | 型 | 必須 | 説明 |
|-------------|----|----|------|
| id | string | ○ | キャリアプランID |
| target_position | string | ○ | 目標ポジションID |
| target_date | string | ○ | 目標達成日 (YYYY-MM-DD形式) |
| target_description | string | ○ | 目標の説明 |
| current_level | string | ○ | 現在のレベル |
| target_level | string | ○ | 目標レベル |
| progress_percentage | number | ○ | 進捗率 (0-100) |
| plan_status | string | ○ | プランステータス (ACTIVE/INACTIVE/COMPLETED) |
| last_review_date | string | △ | 最終レビュー日 (YYYY-MM-DD形式) |
| next_review_date | string | △ | 次回レビュー日 (YYYY-MM-DD形式) |

### skill_categories 配列要素

| フィールド名 | 型 | 必須 | 説明 |
|-------------|----|----|------|
| id | string | ○ | スキルカテゴリID |
| name | string | ○ | カテゴリ名 |
| short_name | string | ○ | カテゴリ短縮名 |
| type | string | ○ | カテゴリタイプ (TECHNICAL/BUSINESS/SOFT) |
| parent_id | string | △ | 親カテゴリID |
| level | number | ○ | カテゴリレベル |
| description | string | ○ | カテゴリ説明 |
| icon_url | string | △ | アイコンURL |
| color_code | string | ○ | カラーコード |

### positions 配列要素

| フィールド名 | 型 | 必須 | 説明 |
|-------------|----|----|------|
| id | string | ○ | ポジションID |
| name | string | ○ | ポジション名 |
| short_name | string | ○ | ポジション短縮名 |
| level | number | ○ | ポジションレベル |
| rank | number | ○ | ポジションランク |
| category | string | ○ | ポジションカテゴリ |
| authority_level | number | ○ | 権限レベル |
| is_management | boolean | ○ | 管理職フラグ |
| is_executive | boolean | ○ | 役員フラグ |
| description | string | ○ | ポジション説明 |

## 業務ルール

### キャリア目標情報
- ユーザーに対してアクティブなキャリアプランが存在しない場合、空のキャリア目標オブジェクトを返す
- 複数のキャリアプランが存在する場合、最新の開始日のプランを取得する
- 進捗率は0-100の範囲で返す

### スキルカテゴリ
- ステータスがACTIVEのカテゴリのみ取得する
- 表示順序に従ってソートして返す
- 階層構造を持つ場合、parent_idで親子関係を表現する

### ポジション情報
- ステータスがACTIVEのポジションのみ取得する
- ソート順序に従ってソートして返す
- 管理職・役員フラグで権限レベルを判定可能

## パフォーマンス要件

- レスポンス時間: 1秒以内
- 同時接続数: 100ユーザー
- データ取得は並列処理で最適化

## セキュリティ要件

- ユーザー認証必須
- ユーザーIDによるデータアクセス制御
- 個人情報の適切な取り扱い

## エラーハンドリング

### エラーコード一覧

| エラーコード | HTTPステータス | 説明 |
|-------------|---------------|------|
| CAREER_INIT_DATA_ERROR | 500 | キャリア初期データ取得エラー |

### エラー対応

- データベース接続エラー: 500エラーを返し、ログに記録
- データ不整合: 空のデータを返し、ログに警告を記録
- 認証エラー: 401エラーを返す（将来実装）

## テスト仕様

### 正常系テスト
- キャリア初期データの正常取得
- ユーザーIDなしの場合のデフォルト処理
- キャリアプラン未存在時の空データ返却

### 異常系テスト
- 不正なユーザーIDでのアクセス
- データベース接続エラー時の処理

### パフォーマンステスト
- レスポンス時間1秒以内の確認
- 複数リクエストの並列処理確認

## 実装ファイル

- API実装: `src/app/api/career/init/route.ts`
- テストファイル: `src/app/api/career/init/route.test.ts`

## 関連ドキュメント

- 画面設計書: `docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md`
- データベース設計: `docs/design/database/`
- 要件定義: `docs/requirements/要件定義.md`

## 変更履歴

| 日付 | バージョン | 変更内容 | 変更者 |
|------|-----------|----------|--------|
| 2025-06-24 | 1.0.0 | 初版作成 | システム開発チーム |
