# API仕様書：API-081 ダッシュボードデータ取得API

## 1. 基本情報

- **API ID**: API-081
- **API名称**: ダッシュボードデータ取得API
- **概要**: ユーザーのダッシュボード表示に必要なデータを取得する
- **エンドポイント**: `/api/dashboard`
- **HTTPメソッド**: GET
- **リクエスト形式**: Query Parameter
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-HOME](画面設計書_SCR-HOME.md)
- **作成日**: 2025/05/28
- **作成者**: API設計担当
- **改訂履歴**: 2025/05/28 初版作成

---

## 2. リクエスト仕様

### 2.1 クエリパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| user_id | string | - | 取得対象のユーザーID | 半角英数字、4〜20文字<br>指定なしの場合は認証ユーザー自身 |
| widgets | string | - | 取得するウィジェット | カンマ区切りで複数指定可能<br>指定なしの場合は全ウィジェット<br>指定可能な値: "tasks", "skills", "trainings", "work_records", "notifications", "goals", "team", "calendar" |
| year | number | - | 取得対象年度 | 西暦4桁<br>指定なしの場合は現在の年度 |
| month | number | - | 取得対象月 | 1〜12の整数<br>指定なしの場合は現在の月 |

### 2.2 リクエスト例

```
GET /api/dashboard?widgets=tasks,skills,notifications&year=2025&month=5
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | ユーザーID | |
| user_name | string | ユーザー名 | |
| department | string | 所属部署 | |
| position | string | 役職 | |
| last_login | string | 最終ログイン日時 | ISO 8601形式 |
| widgets | object | ウィジェットデータ | 詳細は以下参照 |
| system_notices | array | システムからのお知らせ | 詳細は以下参照 |

#### widgets オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| tasks | object | タスク情報 | リクエストに"tasks"が含まれる場合のみ<br>詳細は以下参照 |
| skills | object | スキル情報 | リクエストに"skills"が含まれる場合のみ<br>詳細は以下参照 |
| trainings | object | 研修情報 | リクエストに"trainings"が含まれる場合のみ<br>詳細は以下参照 |
| work_records | object | 作業実績情報 | リクエストに"work_records"が含まれる場合のみ<br>詳細は以下参照 |
| notifications | object | 通知情報 | リクエストに"notifications"が含まれる場合のみ<br>詳細は以下参照 |
| goals | object | 目標情報 | リクエストに"goals"が含まれる場合のみ<br>詳細は以下参照 |
| team | object | チーム情報 | リクエストに"team"が含まれる場合のみ<br>詳細は以下参照 |
| calendar | object | カレンダー情報 | リクエストに"calendar"が含まれる場合のみ<br>詳細は以下参照 |

#### tasks オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| total_count | number | 総タスク数 | |
| completed_count | number | 完了タスク数 | |
| overdue_count | number | 期限超過タスク数 | |
| upcoming_tasks | array | 直近のタスク | 最大5件<br>詳細は以下参照 |

#### upcoming_tasks 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| task_id | string | タスクID | |
| title | string | タスクタイトル | |
| due_date | string | 期限日 | ISO 8601形式（YYYY-MM-DD） |
| priority | number | 優先度 | 1: 低, 2: 中, 3: 高 |
| status | string | ステータス | "not_started", "in_progress", "completed", "waiting"のいずれか |
| category | string | カテゴリ | |

#### skills オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| total_skills | number | 総スキル数 | |
| average_level | number | 平均スキルレベル | 小数点第2位まで |
| top_skills | array | トップスキル | 最大3件<br>詳細は以下参照 |
| improvement_areas | array | 改善推奨スキル | 最大3件<br>詳細は以下参照 |
| skill_status | string | スキル評価ステータス | "draft", "submitted", "reviewed", "approved"のいずれか |
| last_updated_at | string | 最終更新日時 | ISO 8601形式 |

#### top_skills / improvement_areas 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| skill_id | string | スキルID | |
| skill_name | string | スキル名 | |
| level | number | スキルレベル | 0: 未評価, 1: 初級, 2: 中級, 3: 上級, 4: エキスパート |
| category | string | カテゴリ | |

#### trainings オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| completed_count | number | 修了済研修数 | |
| planned_count | number | 予定研修数 | |
| upcoming_trainings | array | 直近の研修 | 最大3件<br>詳細は以下参照 |
| recent_completions | array | 最近修了した研修 | 最大3件<br>詳細は以下参照 |

#### upcoming_trainings / recent_completions 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| training_id | string | 研修ID | |
| training_name | string | 研修名 | |
| start_date | string | 開始日 | ISO 8601形式（YYYY-MM-DD） |
| end_date | string | 終了日 | ISO 8601形式（YYYY-MM-DD） |
| status | string | ステータス | "planned", "registered", "completed", "cancelled"のいずれか |
| category | string | カテゴリ | |

#### work_records オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| monthly_hours | number | 月間作業時間 | |
| monthly_target | number | 月間目標時間 | |
| completion_rate | number | 達成率（%） | 小数点第1位まで |
| by_category | object | カテゴリ別作業時間 | カテゴリごとの作業時間 |
| recent_records | array | 最近の作業実績 | 最大5件<br>詳細は以下参照 |

#### recent_records 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| record_id | string | レコードID | |
| date | string | 作業日 | ISO 8601形式（YYYY-MM-DD） |
| project_name | string | プロジェクト名 | |
| task | string | 作業タスク | |
| hours | number | 作業時間（時間） | |
| category | string | カテゴリ | |

#### notifications オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| unread_count | number | 未読通知数 | |
| recent_notifications | array | 最近の通知 | 最大5件<br>詳細は以下参照 |

#### recent_notifications 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| notification_id | string | 通知ID | |
| type | string | 通知タイプ | "task", "approval", "reminder", "system", "other"のいずれか |
| title | string | 通知タイトル | |
| message | string | 通知メッセージ | |
| created_at | string | 作成日時 | ISO 8601形式 |
| is_read | boolean | 既読フラグ | |
| link | string | 関連リンク | |

#### goals オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| total_goals | number | 総目標数 | |
| completed_goals | number | 達成済目標数 | |
| progress_rate | number | 進捗率（%） | 小数点第1位まで |
| upcoming_milestones | array | 直近のマイルストーン | 最大3件<br>詳細は以下参照 |
| goal_status | string | 目標設定ステータス | "draft", "submitted", "reviewed", "approved"のいずれか |

#### upcoming_milestones 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| milestone_id | string | マイルストーンID | |
| goal_id | string | 目標ID | |
| title | string | タイトル | |
| due_date | string | 期限日 | ISO 8601形式（YYYY-MM-DD） |
| progress | number | 進捗率（%） | 0-100 |

#### team オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| team_name | string | チーム名 | |
| manager | object | マネージャー情報 | 詳細は以下参照 |
| member_count | number | メンバー数 | |
| recent_updates | array | 最近の更新情報 | 最大5件<br>詳細は以下参照 |

#### manager オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | ユーザーID | |
| user_name | string | ユーザー名 | |
| email | string | メールアドレス | |
| position | string | 役職 | |

#### recent_updates 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| update_id | string | 更新ID | |
| user_id | string | ユーザーID | |
| user_name | string | ユーザー名 | |
| type | string | 更新タイプ | "skill", "goal", "training", "work"のいずれか |
| title | string | タイトル | |
| updated_at | string | 更新日時 | ISO 8601形式 |

#### calendar オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| year | number | 年 | |
| month | number | 月 | |
| events | array | イベント情報 | 詳細は以下参照 |

#### events 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| event_id | string | イベントID | |
| title | string | タイトル | |
| start_date | string | 開始日時 | ISO 8601形式 |
| end_date | string | 終了日時 | ISO 8601形式 |
| type | string | イベントタイプ | "training", "meeting", "deadline", "holiday", "other"のいずれか |
| location | string | 場所 | |
| is_all_day | boolean | 終日フラグ | |

#### system_notices 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| notice_id | string | お知らせID | |
| title | string | タイトル | |
| content | string | 内容 | |
| importance | string | 重要度 | "high", "medium", "low"のいずれか |
| start_date | string | 掲載開始日 | ISO 8601形式（YYYY-MM-DD） |
| end_date | string | 掲載終了日 | ISO 8601形式（YYYY-MM-DD） |
| created_at | string | 作成日時 | ISO 8601形式 |

### 3.2 正常時レスポンス例

```json
{
  "user_id": "tanaka.taro",
  "user_name": "田中 太郎",
  "department": "開発部",
  "position": "主任",
  "last_login": "2025-05-27T18:30:45+09:00",
  "widgets": {
    "tasks": {
      "total_count": 15,
      "completed_count": 8,
      "overdue_count": 2,
      "upcoming_tasks": [
        {
          "task_id": "task-12345",
          "title": "スキル評価シートの提出",
          "due_date": "2025-05-31",
          "priority": 3,
          "status": "in_progress",
          "category": "評価"
        },
        {
          "task_id": "task-23456",
          "title": "プロジェクト進捗報告書作成",
          "due_date": "2025-06-05",
          "priority": 2,
          "status": "not_started",
          "category": "報告"
        },
        {
          "task_id": "task-34567",
          "title": "新人研修資料レビュー",
          "due_date": "2025-06-10",
          "priority": 2,
          "status": "not_started",
          "category": "研修"
        }
      ]
    },
    "skills": {
      "total_skills": 25,
      "average_level": 2.64,
      "top_skills": [
        {
          "skill_id": "java",
          "skill_name": "Java",
          "level": 4,
          "category": "プログラミング言語"
        },
        {
          "skill_id": "spring",
          "skill_name": "Spring Framework",
          "level": 3,
          "category": "フレームワーク"
        },
        {
          "skill_id": "sql",
          "skill_name": "SQL",
          "level": 3,
          "category": "データベース"
        }
      ],
      "improvement_areas": [
        {
          "skill_id": "kubernetes",
          "skill_name": "Kubernetes",
          "level": 1,
          "category": "インフラ"
        },
        {
          "skill_id": "react",
          "skill_name": "React",
          "level": 1,
          "category": "フロントエンド"
        }
      ],
      "skill_status": "submitted",
      "last_updated_at": "2025-05-15T14:30:45+09:00"
    },
    "notifications": {
      "unread_count": 3,
      "recent_notifications": [
        {
          "notification_id": "notif-12345",
          "type": "approval",
          "title": "スキル評価レビュー完了",
          "message": "山田部長があなたのスキル評価をレビューしました。",
          "created_at": "2025-05-28T09:15:30+09:00",
          "is_read": false,
          "link": "/skills/evaluation/2025"
        },
        {
          "notification_id": "notif-23456",
          "type": "task",
          "title": "新しいタスクが割り当てられました",
          "message": "「プロジェクト進捗報告書作成」が割り当てられました。期限：2025-06-05",
          "created_at": "2025-05-27T16:45:20+09:00",
          "is_read": false,
          "link": "/tasks/task-23456"
        },
        {
          "notification_id": "notif-34567",
          "type": "reminder",
          "title": "スキル評価シート提出期限間近",
          "message": "スキル評価シートの提出期限が3日後に迫っています。",
          "created_at": "2025-05-27T10:00:00+09:00",
          "is_read": false,
          "link": "/skills/evaluation/edit/2025"
        }
      ]
    }
  },
  "system_notices": [
    {
      "notice_id": "notice-12345",
      "title": "システムメンテナンスのお知らせ",
      "content": "6月1日（日）午前2時〜6時にシステムメンテナンスを実施します。この間はシステムをご利用いただけません。",
      "importance": "high",
      "start_date": "2025-05-25",
      "end_date": "2025-06-01",
      "created_at": "2025-05-20T10:00:00+09:00"
    },
    {
      "notice_id": "notice-23456",
      "title": "スキル評価期間のお知らせ",
      "content": "2025年度第1四半期のスキル評価期間は5月15日〜5月31日です。期間内に評価を完了してください。",
      "importance": "medium",
      "start_date": "2025-05-10",
      "end_date": "2025-05-31",
      "created_at": "2025-05-10T09:00:00+09:00"
    }
  ]
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | リクエストパラメータの形式不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他者のダッシュボード閲覧権限なし |
| 404 Not Found | USER_NOT_FOUND | 指定されたユーザーが見つかりません | 存在しないユーザーID |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "権限がありません",
    "details": "他のユーザーのダッシュボード情報を閲覧する権限がありません。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - ダッシュボード閲覧権限の確認
   - 他者のダッシュボード閲覧権限の確認（自分以外のuser_idの場合）
2. リクエストパラメータの検証
   - user_idの形式チェック（指定されている場合）
   - widgetsの値チェック（指定されている場合）
   - year/monthの範囲チェック（指定されている場合）
3. ユーザーの存在確認
   - 指定されたuser_idのユーザーが存在するか確認
   - user_id未指定の場合は認証ユーザーを対象とする
4. ウィジェットデータの取得
   - リクエストで指定されたウィジェット（または全ウィジェット）のデータを取得
   - 各ウィジェットのデータ取得は並行処理で実行
5. システムお知らせの取得
   - 現在有効なシステムお知らせを取得
6. レスポンスの生成
   - 取得したデータを整形してJSONレスポンスを生成
7. レスポンス返却

### 4.2 アクセス制御ルール

- 自分自身のダッシュボード：閲覧可能
- 部下のダッシュボード：マネージャーは閲覧可能
- 同部署のダッシュボードサマリー：部署管理者は閲覧可能
- 全社員のダッシュボードサマリー：人事担当者・管理者は閲覧可能

### 4.3 パフォーマンス要件

- 応答時間：平均500ms以内
- タイムアウト：5秒
- キャッシュ：ユーザー別・ウィジェット別に5分キャッシュ
- 同時リクエスト：最大50リクエスト/秒

### 4.4 ウィジェット取得ルール

| ウィジェット名 | 取得データ範囲 | 主な情報源 |
|--------------|-------------|----------|
| tasks | 未完了タスク + 直近1週間の完了タスク | タスク管理システム |
| skills | 最新のスキル評価情報 | スキル評価データ |
| trainings | 今後3ヶ月の予定研修 + 過去1ヶ月の修了研修 | 研修管理システム |
| work_records | 当月の作業実績 + 前月比較データ | 作業実績記録 |
| notifications | 未読通知 + 直近1週間の既読通知 | 通知システム |
| goals | 当年度の目標情報 | 目標管理システム |
| team | チームメンバー情報 + 直近1週間の更新情報 | 組織管理システム |
| calendar | 当月 + 翌月のイベント情報 | カレンダーシステム |

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-082](API仕様書_API-082.md) | ユーザーサマリー取得API | ユーザー情報サマリー取得 |
| [API-021](API仕様書_API-021.md) | スキル情報取得API | スキル情報取得 |
| [API-031](API仕様書_API-031.md) | キャリア目標取得API | キャリア目標情報取得 |
| [API-041](API仕様書_API-041.md) | 作業実績取得API | 作業実績情報取得 |
| [API-051](API仕様書_API-051.md) | 研修記録取得API | 研修記録情報取得 |
| [API-201](API仕様書_API-201.md) | 通知一覧取得API | 通知情報取得 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| departments | 部署情報 | 参照（R） |
| tasks | タスク情報 | 参照（R） |
| skills | スキル情報 | 参照（R） |
| skill_evaluations | スキル評価情報 | 参照（R） |
| trainings | 研修情報 | 参照（R） |
| user_trainings | ユーザー研修履歴 | 参照（R） |
| work_records | 作業実績情報 | 参照（R） |
| notifications | 通知情報 | 参照（R） |
| goals | 目標情報 | 参照（R） |
| goal_milestones | 目標マイルストーン | 参照（R） |
| teams | チーム情報 | 参照（R） |
| team_members | チームメンバー | 参照（R） |
| calendar_events | カレンダーイベント | 参照（R） |
| system_notices | システムお知らせ | 参照（R） |

### 5.3 注意事項・補足

- ダッシュボードデータは複数のシステムからの情報を集約
- パフォーマンス向上のため、各ウィジェットのデータ取得は並行処理
- ウィジェットごとにキャッシュ戦略を適用
- ユーザーごとにダッシュボードのカスタマイズ設定が可能
- 権限に応じて表示データが制限される場合あり
- システムお知らせは重要度順にソート

---

## 6. サンプルコード

### 6.1 ダッシュボードデータ取得例（JavaScript/Fetch API）

```javascript
/**
 * ダッシュボード情報を取得する関数
 * @param {Object} options - 取得オプション
 * @param {string} [options.userId] - 取得対象のユーザーID
 * @param {string|string[]} [options.widgets] - 取得するウィジェット（単一または配列）
 * @param {number} [options.year] - 取得対象年度
 * @param {number} [options.month] - 取得対象月
 * @returns {Promise<Object>} ダッシュボード情報
 */
async function getDashboardData(options = {}) {
  try {
    // クエリパラメータの構築
    const queryParams = new URLSearchParams();
    if (options.userId) queryParams.append('user_id', options.userId);
    
    // 配列パラメータの処理
    if (options.widgets) {
      const widgetsValue = Array.isArray(options.widgets) ? options.widgets.join(',') : options.widgets;
      queryParams.append('widgets', widgetsValue);
    }
    
    if (options.year) queryParams.append('year', options.year);
    if (options.month) queryParams.append('month', options.month);
    
    const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
    
    // APIリクエスト
    const response = await fetch(`https://api.example.com/api/dashboard${queryString}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`,
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error.message || 'ダッシュボード情報の取得に失敗しました');
    }
    
    return await response.json();
  } catch (error) {
    console.error('ダッシュボード情報取得エラー:', error);
    throw error;
  }
}
```

### 6.2 ダッ
