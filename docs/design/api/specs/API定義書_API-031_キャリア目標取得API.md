# API仕様書：キャリア目標取得API

| 項目                | 内容                                                                                |
|---------------------|------------------------------------------------------------------------------------|
| **API ID**          | API-031                                                                            |
| **API名称**         | キャリア目標取得API                                                                |
| **エンドポイント**  | /api/career-goals/{user_id}                                                       |
| **HTTPメソッド**    | GET                                                                                |
| **概要・目的**      | ユーザーのキャリア目標情報を取得し、進捗状況と達成度を提供する                      |
| **利用画面**        | SCR-CAREER                                                                         |
| **優先度**          | 中                                                                                  |
| **認証要件**        | 必須（本人または管理者権限）                                                        |
| **レート制限**      | 200 req/min                                                                        |

## 1. エンドポイント詳細

### 1.1 キャリア目標取得

#### リクエスト
```http
GET /api/career-goals/{user_id}?includeProgress=true&includeHistory=false&year=2025
Authorization: Bearer {jwt_token}
```

#### パスパラメータ
| パラメータ名 | 型     | 必須 | 説明       |
|--------------|--------|------|------------|
| user_id      | String | Yes  | ユーザーID |

#### クエリパラメータ
| パラメータ名    | 型      | 必須 | 説明                                           |
|-----------------|---------|------|------------------------------------------------|
| includeProgress | Boolean | No   | 進捗情報を含める（デフォルト: true）           |
| includeHistory  | Boolean | No   | 履歴情報を含める（デフォルト: false）          |
| year            | Integer | No   | 対象年度（デフォルト: 現在年度）               |
| status          | String  | No   | ステータスフィルタ（active/completed/all）     |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_001",
      "name": "田中太郎",
      "department": "エンジニアリング部",
      "position": "シニアエンジニア",
      "currentLevel": "L3"
    },
    "careerGoals": {
      "year": 2025,
      "overallProgress": {
        "completionRate": 0.65,
        "totalGoals": 8,
        "completedGoals": 3,
        "inProgressGoals": 4,
        "notStartedGoals": 1,
        "lastUpdated": "2025-05-30T10:30:00Z"
      },
      "categories": [
        {
          "id": "technical_skills",
          "name": "技術スキル",
          "description": "技術的な能力向上",
          "weight": 0.4,
          "progress": 0.7,
          "goals": [
            {
              "id": "goal_001",
              "title": "React.js マスター",
              "description": "React.jsの上級レベルまでスキルアップし、チームのテックリードとして活動する",
              "category": "technical_skills",
              "priority": "high",
              "status": "in_progress",
              "targetLevel": "advanced",
              "currentLevel": "intermediate",
              "progress": {
                "percentage": 0.75,
                "milestones": [
                  {
                    "id": "milestone_001",
                    "title": "基礎学習完了",
                    "description": "React基礎コースの受講完了",
                    "status": "completed",
                    "completedAt": "2025-02-15T09:00:00Z",
                    "weight": 0.2
                  },
                  {
                    "id": "milestone_002",
                    "title": "実践プロジェクト参加",
                    "description": "Reactを使用した実際のプロジェクトに参加",
                    "status": "completed",
                    "completedAt": "2025-04-20T15:30:00Z",
                    "weight": 0.3
                  },
                  {
                    "id": "milestone_003",
                    "title": "上級機能習得",
                    "description": "Context API、Hooks、パフォーマンス最適化の習得",
                    "status": "in_progress",
                    "targetDate": "2025-07-31",
                    "weight": 0.3
                  },
                  {
                    "id": "milestone_004",
                    "title": "チーム指導",
                    "description": "チームメンバーへのReact指導・メンタリング",
                    "status": "not_started",
                    "targetDate": "2025-09-30",
                    "weight": 0.2
                  }
                ]
              },
              "targetDate": "2025-09-30",
              "createdAt": "2025-01-10T09:00:00Z",
              "updatedAt": "2025-05-30T10:30:00Z",
              "metrics": {
                "skillAssessmentScore": 3.2,
                "targetScore": 4.0,
                "projectsCompleted": 2,
                "targetProjects": 3,
                "mentoringSessions": 0,
                "targetSessions": 5
              }
            },
            {
              "id": "goal_002",
              "title": "AWS認定取得",
              "description": "AWS Solutions Architect Associate認定を取得する",
              "category": "technical_skills",
              "priority": "medium",
              "status": "in_progress",
              "progress": {
                "percentage": 0.4,
                "milestones": [
                  {
                    "id": "milestone_005",
                    "title": "学習計画策定",
                    "status": "completed",
                    "completedAt": "2025-03-01T09:00:00Z"
                  },
                  {
                    "id": "milestone_006",
                    "title": "模擬試験合格",
                    "status": "in_progress",
                    "targetDate": "2025-07-15"
                  },
                  {
                    "id": "milestone_007",
                    "title": "本試験受験",
                    "status": "not_started",
                    "targetDate": "2025-08-31"
                  }
                ]
              },
              "targetDate": "2025-08-31",
              "metrics": {
                "studyHours": 45,
                "targetHours": 120,
                "practiceTestScore": 65,
                "targetScore": 80
              }
            }
          ]
        },
        {
          "id": "leadership",
          "name": "リーダーシップ",
          "description": "チームリーダーとしての能力向上",
          "weight": 0.3,
          "progress": 0.5,
          "goals": [
            {
              "id": "goal_003",
              "title": "プロジェクトリーダー経験",
              "description": "中規模プロジェクトのリーダーとして成功を収める",
              "category": "leadership",
              "priority": "high",
              "status": "in_progress",
              "progress": {
                "percentage": 0.6,
                "milestones": [
                  {
                    "id": "milestone_008",
                    "title": "リーダーシップ研修受講",
                    "status": "completed",
                    "completedAt": "2025-03-15T14:00:00Z"
                  },
                  {
                    "id": "milestone_009",
                    "title": "プロジェクト開始",
                    "status": "completed",
                    "completedAt": "2025-04-01T09:00:00Z"
                  },
                  {
                    "id": "milestone_010",
                    "title": "中間評価",
                    "status": "in_progress",
                    "targetDate": "2025-06-30"
                  },
                  {
                    "id": "milestone_011",
                    "title": "プロジェクト完了",
                    "status": "not_started",
                    "targetDate": "2025-09-30"
                  }
                ]
              },
              "targetDate": "2025-09-30",
              "metrics": {
                "teamSize": 5,
                "projectProgress": 0.6,
                "teamSatisfaction": 4.2,
                "targetSatisfaction": 4.0
              }
            }
          ]
        },
        {
          "id": "business_skills",
          "name": "ビジネススキル",
          "description": "ビジネス理解と提案力の向上",
          "weight": 0.2,
          "progress": 0.3,
          "goals": [
            {
              "id": "goal_004",
              "title": "ビジネス分析スキル習得",
              "description": "要件定義とビジネス分析の基礎スキルを習得する",
              "category": "business_skills",
              "priority": "medium",
              "status": "not_started",
              "progress": {
                "percentage": 0.0,
                "milestones": [
                  {
                    "id": "milestone_012",
                    "title": "BA研修受講",
                    "status": "not_started",
                    "targetDate": "2025-07-01"
                  },
                  {
                    "id": "milestone_013",
                    "title": "実践演習",
                    "status": "not_started",
                    "targetDate": "2025-08-31"
                  }
                ]
              },
              "targetDate": "2025-10-31"
            }
          ]
        },
        {
          "id": "personal_development",
          "name": "自己啓発",
          "description": "個人的な成長と学習",
          "weight": 0.1,
          "progress": 0.8,
          "goals": [
            {
              "id": "goal_005",
              "title": "英語力向上",
              "description": "TOEIC 800点以上を達成する",
              "category": "personal_development",
              "priority": "low",
              "status": "completed",
              "progress": {
                "percentage": 1.0,
                "completedAt": "2025-04-15T10:00:00Z"
              },
              "targetDate": "2025-06-30",
              "metrics": {
                "currentScore": 820,
                "targetScore": 800,
                "improvementFromStart": 120
              }
            }
          ]
        }
      ],
      "recommendations": [
        {
          "type": "skill_gap",
          "priority": "high",
          "title": "React.js学習加速",
          "description": "目標達成のため、週末の学習時間を増やすことを推奨",
          "targetGoal": "goal_001",
          "suggestedActions": [
            "週末の学習時間を2時間増加",
            "オンライン勉強会への参加",
            "実践プロジェクトでのアウトプット強化"
          ]
        },
        {
          "type": "timeline_adjustment",
          "priority": "medium",
          "title": "AWS認定スケジュール見直し",
          "description": "現在の進捗では目標達成が困難。スケジュール調整を検討",
          "targetGoal": "goal_002",
          "suggestedActions": [
            "目標日を1ヶ月延期",
            "学習時間の確保（週5時間→8時間）",
            "メンターのサポート依頼"
          ]
        }
      ],
      "nextReviewDate": "2025-06-30",
      "managerFeedback": {
        "lastReviewDate": "2025-05-15T14:00:00Z",
        "overallRating": 4.2,
        "comments": "技術スキルの向上が顕著。リーダーシップ面でも成長が見られる。",
        "suggestions": [
          "プロジェクトマネジメントスキルの強化",
          "後輩指導の機会を増やす"
        ],
        "nextReviewDate": "2025-06-30T14:00:00Z"
      }
    }
  }
}
```

### 1.2 キャリア目標履歴取得

#### リクエスト
```http
GET /api/career-goals/{user_id}/history?years=2024,2025&limit=10
Authorization: Bearer {jwt_token}
```

#### クエリパラメータ
| パラメータ名 | 型      | 必須 | 説明                                           |
|--------------|---------|------|------------------------------------------------|
| years        | String  | No   | 対象年度（カンマ区切り）                       |
| limit        | Integer | No   | 取得件数（デフォルト: 10、最大: 50）           |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "history": [
      {
        "year": 2025,
        "status": "in_progress",
        "overallProgress": 0.65,
        "totalGoals": 8,
        "completedGoals": 3,
        "lastUpdated": "2025-05-30T10:30:00Z"
      },
      {
        "year": 2024,
        "status": "completed",
        "overallProgress": 0.85,
        "totalGoals": 6,
        "completedGoals": 5,
        "lastUpdated": "2024-12-31T23:59:59Z"
      }
    ]
  }
}
```

## 2. エラーレスポンス

### 2.1 共通エラーフォーマット
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "エラーメッセージ",
    "details": "詳細情報"
  }
}
```

### 2.2 エラーコード一覧
| エラーコード | HTTPステータス | 説明 |
|-------------|---------------|------|
| USER_NOT_FOUND | 404 | ユーザーが見つからない |
| GOALS_NOT_FOUND | 404 | キャリア目標が設定されていない |
| INSUFFICIENT_PERMISSIONS | 403 | アクセス権限不足 |
| INVALID_YEAR | 400 | 無効な年度指定 |
| INVALID_STATUS | 400 | 無効なステータス指定 |

## 3. 実装仕様

### 3.1 進捗計算ロジック
- **目標進捗**: マイルストーンの重み付き平均
- **カテゴリ進捗**: カテゴリ内目標の平均
- **全体進捗**: カテゴリの重み付き平均

### 3.2 ステータス定義
- **not_started**: 未開始
- **in_progress**: 進行中
- **completed**: 完了
- **on_hold**: 保留
- **cancelled**: キャンセル

### 3.3 権限制御
- 本人: 全データ閲覧可能
- 直属上司: 全データ閲覧可能
- 人事: 全データ閲覧可能
- その他: アクセス不可

## 4. パフォーマンス要件

| 項目 | 要件 |
|------|------|
| レスポンス時間 | 500ms以内 |
| 同時アクセス数 | 100ユーザー |
| データ更新頻度 | リアルタイム |

## 5. 改訂履歴

| 改訂日     | 改訂者 | 改訂内容                                         |
|------------|--------|--------------------------------------------------|
| 2025/05/30 | 初版   | 初版作成                                         |
