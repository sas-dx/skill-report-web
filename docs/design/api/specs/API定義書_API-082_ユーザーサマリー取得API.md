# API定義書：API-082 ユーザーサマリー取得API

## 1. 基本情報

- **API ID**: API-082
- **API名称**: ユーザーサマリー取得API
- **概要**: ユーザーの基本情報とサマリーデータを取得する
- **エンドポイント**: `/api/dashboard/user-summary`
- **HTTPメソッド**: GET
- **リクエスト形式**: Query Parameter
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-HOME](画面設計書_SCR-HOME.md)
- **作成日**: 2025/05/29
- **作成者**: API設計担当
- **改訂履歴**: 2025/05/29 初版作成

---

## 2. リクエスト仕様

### 2.1 クエリパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| user_id | string | - | 取得対象のユーザーID | 半角英数字、4〜20文字<br>指定なしの場合は認証ユーザー自身 |
| year | number | - | 取得対象年度 | 西暦4桁<br>指定なしの場合は現在の年度 |
| include_details | boolean | - | 詳細情報を含めるか | デフォルト：false |

### 2.2 リクエスト例

```
GET /api/dashboard/user-summary?user_id=tanaka.taro&year=2025&include_details=true
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user | object | ユーザー基本情報 | 詳細は以下参照 |
| skills | object | スキルサマリー | 詳細は以下参照 |
| goals | object | 目標サマリー | 詳細は以下参照 |
| work_records | object | 作業実績サマリー | 詳細は以下参照 |
| trainings | object | 研修サマリー | 詳細は以下参照 |
| year | number | 対象年度 | |
| last_updated_at | string | 最終更新日時 | ISO 8601形式 |

#### user オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | ユーザーID | |
| user_name | string | ユーザー名 | |
| email | string | メールアドレス | |
| department | string | 所属部署 | |
| department_id | string | 部署ID | |
| position | string | 役職 | |
| position_id | string | 役職ID | |
| employee_number | string | 社員番号 | |
| hire_date | string | 入社日 | ISO 8601形式（YYYY-MM-DD） |
| profile_image_url | string | プロフィール画像URL | |
| manager | object | 上長情報 | 詳細は以下参照 |
| status | string | ステータス | "active", "inactive", "leave"のいずれか |
| last_login | string | 最終ログイン日時 | ISO 8601形式 |

#### manager オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | 上長ユーザーID | |
| user_name | string | 上長ユーザー名 | |
| position | string | 上長役職 | |
| email | string | 上長メールアドレス | |

#### skills オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| total_count | number | 総スキル数 | |
| evaluated_count | number | 評価済スキル数 | |
| average_level | number | 平均スキルレベル | 小数点第2位まで |
| level_distribution | object | レベル分布 | 詳細は以下参照 |
| top_categories | array | トップカテゴリ | 最大3件<br>詳細は以下参照 |
| evaluation_status | string | 評価ステータス | "not_started", "in_progress", "submitted", "reviewed", "approved"のいずれか |
| last_evaluation_date | string | 最終評価日 | ISO 8601形式（YYYY-MM-DD） |
| details | array | スキル詳細 | include_details=trueの場合のみ<br>詳細は以下参照 |

#### level_distribution オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| level0 | number | レベル0（未評価）の数 | |
| level1 | number | レベル1（初級）の数 | |
| level2 | number | レベル2（中級）の数 | |
| level3 | number | レベル3（上級）の数 | |
| level4 | number | レベル4（エキスパート）の数 | |

#### top_categories 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| category_id | string | カテゴリID | |
| category_name | string | カテゴリ名 | |
| average_level | number | カテゴリ平均レベル | 小数点第2位まで |
| skill_count | number | カテゴリ内スキル数 | |

#### skills.details 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| skill_id | string | スキルID | |
| skill_name | string | スキル名 | |
| category_id | string | カテゴリID | |
| category_name | string | カテゴリ名 | |
| level | number | スキルレベル | 0: 未評価, 1: 初級, 2: 中級, 3: 上級, 4: エキスパート |
| self_evaluation | number | 自己評価レベル | 0: 未評価, 1: 初級, 2: 中級, 3: 上級, 4: エキスパート |
| manager_evaluation | number | 上長評価レベル | 0: 未評価, 1: 初級, 2: 中級, 3: 上級, 4: エキスパート |
| last_updated_at | string | 最終更新日時 | ISO 8601形式 |

#### goals オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| total_count | number | 総目標数 | |
| completed_count | number | 達成済目標数 | |
| in_progress_count | number | 進行中目標数 | |
| not_started_count | number | 未着手目標数 | |
| overall_progress | number | 全体進捗率（%） | 小数点第1位まで |
| goal_status | string | 目標設定ステータス | "not_started", "in_progress", "submitted", "reviewed", "approved"のいずれか |
| last_updated_at | string | 最終更新日時 | ISO 8601形式 |
| details | array | 目標詳細 | include_details=trueの場合のみ<br>詳細は以下参照 |

#### goals.details 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| goal_id | string | 目標ID | |
| title | string | 目標タイトル | |
| category | string | 目標カテゴリ | "career", "skill", "performance", "other"のいずれか |
| priority | number | 優先度 | 1: 低, 2: 中, 3: 高 |
| progress | number | 進捗率（%） | 0-100 |
| status | string | ステータス | "not_started", "in_progress", "completed", "cancelled"のいずれか |
| start_date | string | 開始日 | ISO 8601形式（YYYY-MM-DD） |
| end_date | string | 終了日 | ISO 8601形式（YYYY-MM-DD） |
| last_updated_at | string | 最終更新日時 | ISO 8601形式 |

#### work_records オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| total_hours | number | 総作業時間 | |
| monthly_average | number | 月平均作業時間 | 小数点第1位まで |
| project_count | number | プロジェクト数 | |
| category_distribution | object | カテゴリ別分布 | カテゴリごとの作業時間割合（%） |
| last_record_date | string | 最終記録日 | ISO 8601形式（YYYY-MM-DD） |
| details | array | 作業実績詳細 | include_details=trueの場合のみ<br>詳細は以下参照 |

#### category_distribution オブジェクト

カテゴリ名をキー、割合（%）を値とするオブジェクト。例：
```json
{
  "開発": 45.5,
  "会議": 20.0,
  "調査": 15.5,
  "テスト": 10.0,
  "その他": 9.0
}
```

#### work_records.details 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| project_id | string | プロジェクトID | |
| project_name | string | プロジェクト名 | |
| total_hours | number | プロジェクト別総作業時間 | |
| start_date | string | 開始日 | ISO 8601形式（YYYY-MM-DD） |
| end_date | string | 終了日 | ISO 8601形式（YYYY-MM-DD） |
| status | string | ステータス | "in_progress", "completed", "cancelled"のいずれか |

#### trainings オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| total_count | number | 総研修数 | |
| completed_count | number | 修了済研修数 | |
| planned_count | number | 予定研修数 | |
| in_progress_count | number | 進行中研修数 | |
| total_hours | number | 総研修時間 | |
| category_distribution | object | カテゴリ別分布 | カテゴリごとの研修数割合（%） |
| last_completed_date | string | 最終修了日 | ISO 8601形式（YYYY-MM-DD） |
| details | array | 研修詳細 | include_details=trueの場合のみ<br>詳細は以下参照 |

#### trainings.details 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| training_id | string | 研修ID | |
| training_name | string | 研修名 | |
| category | string | 研修カテゴリ | |
| hours | number | 研修時間 | |
| start_date | string | 開始日 | ISO 8601形式（YYYY-MM-DD） |
| end_date | string | 終了日 | ISO 8601形式（YYYY-MM-DD） |
| status | string | ステータス | "planned", "in_progress", "completed", "cancelled"のいずれか |
| score | number | 評価スコア | 0-100 |

### 3.2 正常時レスポンス例

```json
{
  "user": {
    "user_id": "tanaka.taro",
    "user_name": "田中 太郎",
    "email": "tanaka.taro@example.com",
    "department": "開発部",
    "department_id": "dept_dev",
    "position": "主任",
    "position_id": "position_leader",
    "employee_number": "EMP001",
    "hire_date": "2020-04-01",
    "profile_image_url": "https://example.com/profiles/tanaka.jpg",
    "manager": {
      "user_id": "yamada.jiro",
      "user_name": "山田 次郎",
      "position": "部長",
      "email": "yamada.jiro@example.com"
    },
    "status": "active",
    "last_login": "2025-05-28T18:30:45+09:00"
  },
  "skills": {
    "total_count": 25,
    "evaluated_count": 22,
    "average_level": 2.64,
    "level_distribution": {
      "level0": 3,
      "level1": 5,
      "level2": 8,
      "level3": 7,
      "level4": 2
    },
    "top_categories": [
      {
        "category_id": "programming_languages",
        "category_name": "プログラミング言語",
        "average_level": 3.2,
        "skill_count": 5
      },
      {
        "category_id": "frameworks",
        "category_name": "フレームワーク",
        "average_level": 2.8,
        "skill_count": 4
      },
      {
        "category_id": "databases",
        "category_name": "データベース",
        "average_level": 2.5,
        "skill_count": 3
      }
    ],
    "evaluation_status": "approved",
    "last_evaluation_date": "2025-04-15"
  },
  "goals": {
    "total_count": 5,
    "completed_count": 2,
    "in_progress_count": 2,
    "not_started_count": 1,
    "overall_progress": 65.0,
    "goal_status": "approved",
    "last_updated_at": "2025-05-10T14:30:00+09:00"
  },
  "work_records": {
    "total_hours": 1250.5,
    "monthly_average": 156.3,
    "project_count": 3,
    "category_distribution": {
      "開発": 45.5,
      "会議": 20.0,
      "調査": 15.5,
      "テスト": 10.0,
      "その他": 9.0
    },
    "last_record_date": "2025-05-28"
  },
  "trainings": {
    "total_count": 8,
    "completed_count": 6,
    "planned_count": 1,
    "in_progress_count": 1,
    "total_hours": 48,
    "category_distribution": {
      "技術": 50.0,
      "マネジメント": 25.0,
      "ビジネススキル": 25.0
    },
    "last_completed_date": "2025-05-15"
  },
  "year": 2025,
  "last_updated_at": "2025-05-28T23:15:30+09:00"
}
```

### 3.3 詳細情報を含むレスポンス例（include_details=true）

```json
{
  "user": {
    "user_id": "tanaka.taro",
    "user_name": "田中 太郎",
    "email": "tanaka.taro@example.com",
    "department": "開発部",
    "department_id": "dept_dev",
    "position": "主任",
    "position_id": "position_leader",
    "employee_number": "EMP001",
    "hire_date": "2020-04-01",
    "profile_image_url": "https://example.com/profiles/tanaka.jpg",
    "manager": {
      "user_id": "yamada.jiro",
      "user_name": "山田 次郎",
      "position": "部長",
      "email": "yamada.jiro@example.com"
    },
    "status": "active",
    "last_login": "2025-05-28T18:30:45+09:00"
  },
  "skills": {
    "total_count": 25,
    "evaluated_count": 22,
    "average_level": 2.64,
    "level_distribution": {
      "level0": 3,
      "level1": 5,
      "level2": 8,
      "level3": 7,
      "level4": 2
    },
    "top_categories": [
      {
        "category_id": "programming_languages",
        "category_name": "プログラミング言語",
        "average_level": 3.2,
        "skill_count": 5
      },
      {
        "category_id": "frameworks",
        "category_name": "フレームワーク",
        "average_level": 2.8,
        "skill_count": 4
      },
      {
        "category_id": "databases",
        "category_name": "データベース",
        "average_level": 2.5,
        "skill_count": 3
      }
    ],
    "evaluation_status": "approved",
    "last_evaluation_date": "2025-04-15",
    "details": [
      {
        "skill_id": "java",
        "skill_name": "Java",
        "category_id": "programming_languages",
        "category_name": "プログラミング言語",
        "level": 4,
        "self_evaluation": 4,
        "manager_evaluation": 4,
        "last_updated_at": "2025-04-10T11:30:00+09:00"
      },
      {
        "skill_id": "spring",
        "skill_name": "Spring Framework",
        "category_id": "frameworks",
        "category_name": "フレームワーク",
        "level": 3,
        "self_evaluation": 3,
        "manager_evaluation": 3,
        "last_updated_at": "2025-04-10T11:35:00+09:00"
      },
      {
        "skill_id": "sql",
        "skill_name": "SQL",
        "category_id": "databases",
        "category_name": "データベース",
        "level": 3,
        "self_evaluation": 3,
        "manager_evaluation": 3,
        "last_updated_at": "2025-04-10T11:40:00+09:00"
      }
    ]
  },
  "goals": {
    "total_count": 5,
    "completed_count": 2,
    "in_progress_count": 2,
    "not_started_count": 1,
    "overall_progress": 65.0,
    "goal_status": "approved",
    "last_updated_at": "2025-05-10T14:30:00+09:00",
    "details": [
      {
        "goal_id": "goal-12345",
        "title": "Spring Boot 3の習得",
        "category": "skill",
        "priority": 3,
        "progress": 100,
        "status": "completed",
        "start_date": "2025-01-15",
        "end_date": "2025-03-31",
        "last_updated_at": "2025-04-01T10:00:00+09:00"
      },
      {
        "goal_id": "goal-23456",
        "title": "プロジェクトマネジメントスキルの向上",
        "category": "career",
        "priority": 2,
        "progress": 60,
        "status": "in_progress",
        "start_date": "2025-04-01",
        "end_date": "2025-09-30",
        "last_updated_at": "2025-05-10T14:30:00+09:00"
      }
    ]
  },
  "work_records": {
    "total_hours": 1250.5,
    "monthly_average": 156.3,
    "project_count": 3,
    "category_distribution": {
      "開発": 45.5,
      "会議": 20.0,
      "調査": 15.5,
      "テスト": 10.0,
      "その他": 9.0
    },
    "last_record_date": "2025-05-28",
    "details": [
      {
        "project_id": "proj-12345",
        "project_name": "顧客管理システム刷新",
        "total_hours": 520.5,
        "start_date": "2025-01-10",
        "end_date": "2025-04-30",
        "status": "completed"
      },
      {
        "project_id": "proj-23456",
        "project_name": "モバイルアプリ開発",
        "total_hours": 350.0,
        "start_date": "2025-03-01",
        "end_date": "2025-08-31",
        "status": "in_progress"
      }
    ]
  },
  "trainings": {
    "total_count": 8,
    "completed_count": 6,
    "planned_count": 1,
    "in_progress_count": 1,
    "total_hours": 48,
    "category_distribution": {
      "技術": 50.0,
      "マネジメント": 25.0,
      "ビジネススキル": 25.0
    },
    "last_completed_date": "2025-05-15",
    "details": [
      {
        "training_id": "train-12345",
        "training_name": "Spring Boot 3入門",
        "category": "技術",
        "hours": 8,
        "start_date": "2025-02-10",
        "end_date": "2025-02-10",
        "status": "completed",
        "score": 92
      },
      {
        "training_id": "train-23456",
        "training_name": "プロジェクトマネジメント基礎",
        "category": "マネジメント",
        "hours": 16,
        "start_date": "2025-04-15",
        "end_date": "2025-04-16",
        "status": "completed",
        "score": 85
      }
    ]
  },
  "year": 2025,
  "last_updated_at": "2025-05-28T23:15:30+09:00"
}
```

### 3.4 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | リクエストパラメータの形式不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他者のサマリー閲覧権限なし |
| 404 Not Found | USER_NOT_FOUND | 指定されたユーザーが見つかりません | 存在しないユーザーID |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.5 エラー時レスポンス例

```json
{
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "権限がありません",
    "details": "他のユーザーのサマリー情報を閲覧する権限がありません。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - サマリー閲覧権限の確認
   - 他者のサマリー閲覧権限の確認（自分以外のuser_idの場合）
2. リクエストパラメータの検証
   - user_idの形式チェック（指定されている場合）
   - yearの範囲チェック（指定されている場合）
3. ユーザーの存在確認
   - 指定されたuser_idのユーザーが存在するか確認
   - user_id未指定の場合は認証ユーザーを対象とする
4. ユーザー基本情報の取得
   - ユーザープロフィール情報を取得
   - 上長情報を取得
5. 各種サマリーデータの取得
   - スキルサマリーの取得
   - 目標サマリーの取得
   - 作業実績サマリーの取得
   - 研修サマリーの取得
   - include_details=trueの場合は詳細情報も取得
6. レスポンスの生成
   - 取得したデータを整形してJSONレスポンスを生成
7. レスポンス返却

### 4.2 アクセス制御ルール

- 自分自身のサマリー：閲覧可能
- 部下のサマリー：マネージャーは閲覧可能
- 同部署のサマリー：部署管理者は閲覧可能
- 全社員のサマリー：人事担当者・管理者は閲覧可能

### 4.3 パフォーマンス要件

- 応答時間：平均300ms以内
- タイムアウト：5秒
- キャッシュ：ユーザー別に10分キャッシュ
- 同時リクエスト：最大20リクエスト/秒

### 4.4 データ取得ルール

| データ種別 | 取得範囲 | 主な情報源 |
|-----------|---------|----------|
| ユーザー基本情報 | 最新のプロフィール情報 | ユーザー管理システム |
| スキルサマリー | 指定年度のスキル評価情報 | スキル評価システム |
| 目標サマリー | 指定年度の目標情報 | 目標管理システム |
| 作業実績サマリー | 指定年度の作業実績情報 | 作業実績管理システム |
| 研修サマリー | 指定年度の研修情報 | 研修管理システム |

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-081](API仕様書_API-081.md) | ダッシュボードデータ取得API | ダッシュボード表示データ取得 |
| [API-021](API仕様書_API-021.md) | スキル情報取得API | スキル情報取得 |
| [API-031](API仕様書_API-031.md) | キャリア目標取得API | キャリア目標情報取得 |
| [API-041](API仕様書_API-041.md) | 作業実績取得API | 作業実績情報取得 |
| [API-051](API仕様書_API-051.md) | 研修記録取得API | 研修記録情報取得 |
| [API-011](API仕様書_API-011.md) | ユーザー情報取得API | ユーザー情報取得 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| departments | 部署情報 | 参照（R） |
| positions | 役職情報 | 参照（R） |
| skills | スキル情報 | 参照（R） |
| skill_evaluations | スキル評価情報 | 参照（R） |
| skill_categories | スキルカテゴリ情報 | 参照（R） |
| goals | 目標情報 | 参照（R） |
| work_records | 作業実績情報 | 参照（R） |
| projects | プロジェクト情報 | 参照（R） |
| trainings | 研修情報 | 参照（R） |
| user_trainings | ユーザー研修履歴 |
