# API仕様書: API-044 目標進捗更新API

## 基本情報

| 項目 | 内容 |
|------|------|
| API ID | API-044 |
| API名称 | 目標進捗更新API |
| エンドポイント | /api/goal-progress/{user_id} |
| 概要 | 目標進捗情報更新 |
| 利用画面 | SCR-CAREER |
| 優先度 | 中 |
| 実装予定 | Week 3-4 |

---

## エンドポイント詳細

### 1. 目標進捗更新

#### リクエスト
```http
PUT /api/goal-progress/{user_id}
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### パスパラメータ
| パラメータ名 | 型 | 必須 | 説明 |
|-------------|---|------|------|
| user_id | string | ○ | ユーザーID |

#### リクエストボディ
```json
{
  "goalProgress": [
    {
      "goalId": "goal_001",
      "progressPercentage": 75.5,
      "status": "in_progress",
      "milestones": [
        {
          "milestoneId": "milestone_001",
          "title": "基礎学習完了",
          "description": "AWS基礎コースの受講完了",
          "targetDate": "2025-06-15",
          "completedDate": "2025-06-10",
          "status": "completed",
          "evidence": {
            "type": "certificate",
            "url": "https://storage.example.com/certificates/aws_basics.pdf",
            "description": "AWS基礎コース修了証"
          }
        },
        {
          "milestoneId": "milestone_002",
          "title": "模擬試験合格",
          "description": "AWS Solutions Architect模擬試験で80%以上",
          "targetDate": "2025-07-15",
          "completedDate": null,
          "status": "in_progress",
          "currentScore": 72,
          "targetScore": 80,
          "evidence": null
        },
        {
          "milestoneId": "milestone_003",
          "title": "本試験受験",
          "description": "AWS Solutions Architect Associate本試験",
          "targetDate": "2025-08-31",
          "completedDate": null,
          "status": "not_started",
          "evidence": null
        }
      ],
      "achievements": [
        {
          "achievementId": "achievement_001",
          "title": "継続学習達成",
          "description": "30日連続で学習を継続",
          "earnedDate": "2025-05-30",
          "badgeUrl": "https://storage.example.com/badges/continuous_learning.png"
        }
      ],
      "timeTracking": {
        "totalHoursSpent": 45.5,
        "thisWeekHours": 8.0,
        "averageWeeklyHours": 6.5,
        "lastActivityDate": "2025-05-30"
      },
      "notes": [
        {
          "noteId": "note_001",
          "content": "AWSのVPCについて理解が深まった。実際のプロジェクトでも活用できそう。",
          "createdAt": "2025-05-28T14:30:00Z",
          "tags": ["AWS", "VPC", "ネットワーク"]
        },
        {
          "noteId": "note_002",
          "content": "模擬試験で間違えた問題を復習。セキュリティ分野が弱いので重点的に学習する。",
          "createdAt": "2025-05-30T10:15:00Z",
          "tags": ["模擬試験", "セキュリティ", "復習"]
        }
      ],
      "challenges": [
        {
          "challengeId": "challenge_001",
          "title": "時間確保の困難",
          "description": "プロジェクトが忙しく、学習時間の確保が難しい",
          "severity": "medium",
          "status": "active",
          "proposedSolution": "朝の時間を活用した学習スケジュールに変更",
          "createdAt": "2025-05-25T09:00:00Z"
        }
      ],
      "nextActions": [
        {
          "actionId": "action_001",
          "title": "セキュリティ分野の集中学習",
          "description": "模擬試験で弱点となったセキュリティ分野を重点的に学習",
          "priority": "high",
          "dueDate": "2025-06-15",
          "estimatedHours": 10,
          "status": "planned"
        },
        {
          "actionId": "action_002",
          "title": "実践演習の実施",
          "description": "AWSコンソールでの実際の操作練習",
          "priority": "medium",
          "dueDate": "2025-06-30",
          "estimatedHours": 15,
          "status": "planned"
        }
      ],
      "lastUpdated": "2025-05-30T21:30:00Z",
      "updatedBy": "user_001"
    },
    {
      "goalId": "goal_002",
      "progressPercentage": 30.0,
      "status": "in_progress",
      "milestones": [
        {
          "milestoneId": "milestone_004",
          "title": "React Native環境構築",
          "description": "開発環境のセットアップ完了",
          "targetDate": "2025-06-01",
          "completedDate": "2025-05-28",
          "status": "completed",
          "evidence": {
            "type": "screenshot",
            "url": "https://storage.example.com/screenshots/rn_setup.png",
            "description": "React Native開発環境構築完了"
          }
        },
        {
          "milestoneId": "milestone_005",
          "title": "基本アプリ作成",
          "description": "Hello Worldアプリの作成",
          "targetDate": "2025-06-15",
          "completedDate": null,
          "status": "in_progress",
          "evidence": null
        }
      ],
      "timeTracking": {
        "totalHoursSpent": 12.0,
        "thisWeekHours": 4.0,
        "averageWeeklyHours": 3.0,
        "lastActivityDate": "2025-05-29"
      },
      "notes": [
        {
          "noteId": "note_003",
          "content": "React Nativeの環境構築は思ったより複雑だった。Expoを使うことで簡単になった。",
          "createdAt": "2025-05-28T16:45:00Z",
          "tags": ["React Native", "Expo", "環境構築"]
        }
      ],
      "challenges": [],
      "nextActions": [
        {
          "actionId": "action_003",
          "title": "基本コンポーネントの学習",
          "description": "View, Text, StyleSheetなどの基本コンポーネント習得",
          "priority": "high",
          "dueDate": "2025-06-10",
          "estimatedHours": 8,
          "status": "planned"
        }
      ],
      "lastUpdated": "2025-05-29T18:20:00Z",
      "updatedBy": "user_001"
    }
  ],
  "overallSummary": {
    "totalGoals": 3,
    "activeGoals": 2,
    "completedGoals": 1,
    "averageProgress": 52.75,
    "totalHoursThisWeek": 12.0,
    "totalHoursOverall": 57.5,
    "upcomingDeadlines": [
      {
        "goalId": "goal_001",
        "milestoneTitle": "模擬試験合格",
        "dueDate": "2025-07-15",
        "daysRemaining": 46
      },
      {
        "goalId": "goal_002",
        "milestoneTitle": "基本アプリ作成",
        "dueDate": "2025-06-15",
        "daysRemaining": 16
      }
    ],
    "recentAchievements": [
      {
        "goalId": "goal_001",
        "achievementTitle": "継続学習達成",
        "earnedDate": "2025-05-30"
      }
    ]
  }
}
```

#### バリデーションルール
| フィールド | ルール |
|-----------|--------|
| goalId | 必須、有効な目標ID |
| progressPercentage | 必須、数値、0-100 |
| status | 必須、not_started/in_progress/completed/on_hold |
| milestones[].status | 必須、not_started/in_progress/completed |
| timeTracking.totalHoursSpent | 必須、数値、0以上 |
| notes[].content | 必須、文字列、最大1000文字 |
| challenges[].severity | 必須、low/medium/high |
| nextActions[].priority | 必須、low/medium/high |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "updatedGoals": [
      {
        "goalId": "goal_001",
        "title": "AWS Professional資格取得",
        "progressPercentage": 75.5,
        "status": "in_progress",
        "lastUpdated": "2025-05-30T21:30:00Z",
        "nextMilestone": {
          "title": "模擬試験合格",
          "dueDate": "2025-07-15",
          "daysRemaining": 46
        }
      },
      {
        "goalId": "goal_002",
        "title": "React Native習得",
        "progressPercentage": 30.0,
        "status": "in_progress",
        "lastUpdated": "2025-05-29T18:20:00Z",
        "nextMilestone": {
          "title": "基本アプリ作成",
          "dueDate": "2025-06-15",
          "daysRemaining": 16
        }
      }
    ],
    "progressSummary": {
      "totalGoalsUpdated": 2,
      "averageProgressIncrease": 5.25,
      "newAchievements": 1,
      "completedMilestones": 1,
      "hoursLoggedThisUpdate": 12.0
    },
    "recommendations": [
      {
        "type": "time_management",
        "title": "学習時間の最適化",
        "description": "現在の学習ペースを維持するため、週8時間の学習時間確保を推奨",
        "priority": "medium"
      },
      {
        "type": "skill_focus",
        "title": "弱点分野の強化",
        "description": "AWS セキュリティ分野の集中学習を推奨",
        "priority": "high"
      }
    ],
    "updatedAt": "2025-05-30T21:30:00Z"
  }
}
```

### 2. 目標進捗一括更新

#### リクエスト
```http
PUT /api/goal-progress/{user_id}/bulk
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "bulkUpdates": [
    {
      "goalId": "goal_001",
      "progressPercentage": 80.0,
      "hoursSpent": 5.0,
      "note": "今週は集中的に学習できた"
    },
    {
      "goalId": "goal_002",
      "progressPercentage": 35.0,
      "hoursSpent": 3.0,
      "note": "基本コンポーネントの理解が進んだ"
    },
    {
      "goalId": "goal_003",
      "progressPercentage": 15.0,
      "hoursSpent": 2.0,
      "note": "Docker基礎の学習を開始"
    }
  ],
  "weeklyReflection": {
    "achievements": "AWS模擬試験で目標スコアを達成",
    "challenges": "時間確保が困難だった",
    "nextWeekFocus": "React Nativeの実践的な学習に集中",
    "overallSatisfaction": 4
  }
}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "bulkUpdateSummary": {
      "totalGoalsUpdated": 3,
      "successfulUpdates": 3,
      "failedUpdates": 0,
      "totalHoursLogged": 10.0,
      "averageProgressIncrease": 6.67
    },
    "weeklyProgress": {
      "weekStartDate": "2025-05-26",
      "weekEndDate": "2025-06-01",
      "totalHours": 10.0,
      "goalsProgressed": 3,
      "milestonesCompleted": 0,
      "overallSatisfaction": 4
    },
    "updatedGoals": [
      {
        "goalId": "goal_001",
        "newProgress": 80.0,
        "progressIncrease": 4.5,
        "status": "in_progress"
      },
      {
        "goalId": "goal_002",
        "newProgress": 35.0,
        "progressIncrease": 5.0,
        "status": "in_progress"
      },
      {
        "goalId": "goal_003",
        "newProgress": 15.0,
        "progressIncrease": 15.0,
        "status": "in_progress"
      }
    ],
    "updatedAt": "2025-05-30T21:35:00Z"
  }
}
```

### 3. マイルストーン完了

#### リクエスト
```http
PUT /api/goal-progress/{user_id}/milestone/{milestone_id}/complete
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### パスパラメータ
| パラメータ名 | 型 | 必須 | 説明 |
|-------------|---|------|------|
| user_id | string | ○ | ユーザーID |
| milestone_id | string | ○ | マイルストーンID |

#### リクエストボディ
```json
{
  "completedDate": "2025-05-30T21:40:00Z",
  "evidence": {
    "type": "certificate",
    "url": "https://storage.example.com/certificates/milestone_completion.pdf",
    "description": "マイルストーン完了証明書",
    "metadata": {
      "fileSize": 1024000,
      "mimeType": "application/pdf"
    }
  },
  "reflection": {
    "learnings": "予想以上に難しかったが、基礎がしっかり身についた",
    "challenges": "時間管理が課題だった",
    "nextSteps": "次のマイルストーンに向けて計画を見直す",
    "satisfaction": 4
  },
  "actualHours": 12.5,
  "skillsGained": ["AWS VPC", "セキュリティグループ", "ルートテーブル"]
}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "completedMilestone": {
      "milestoneId": "milestone_002",
      "title": "模擬試験合格",
      "goalId": "goal_001",
      "goalTitle": "AWS Professional資格取得",
      "completedDate": "2025-05-30T21:40:00Z",
      "plannedDate": "2025-07-15T00:00:00Z",
      "daysAhead": 46,
      "actualHours": 12.5,
      "plannedHours": 15.0
    },
    "goalUpdate": {
      "goalId": "goal_001",
      "newProgressPercentage": 85.0,
      "progressIncrease": 9.5,
      "status": "in_progress",
      "nextMilestone": {
        "milestoneId": "milestone_003",
        "title": "本試験受験",
        "targetDate": "2025-08-31"
      }
    },
    "achievements": [
      {
        "achievementId": "achievement_002",
        "title": "早期達成",
        "description": "予定より46日早くマイルストーンを達成",
        "badgeUrl": "https://storage.example.com/badges/early_achiever.png",
        "earnedDate": "2025-05-30T21:40:00Z"
      }
    ],
    "recommendations": [
      {
        "type": "acceleration",
        "title": "目標期限の前倒し",
        "description": "現在のペースなら本試験も前倒しで受験可能",
        "suggestedDate": "2025-07-31"
      }
    ],
    "updatedAt": "2025-05-30T21:40:00Z"
  }
}
```

### 4. 進捗レポート生成

#### リクエスト
```http
POST /api/goal-progress/{user_id}/report
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "reportType": "weekly",
  "period": {
    "startDate": "2025-05-26",
    "endDate": "2025-06-01"
  },
  "includeDetails": true,
  "format": "json"
}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "progressReport": {
      "reportId": "report_001",
      "userId": "user_001",
      "reportType": "weekly",
      "period": {
        "startDate": "2025-05-26",
        "endDate": "2025-06-01"
      },
      "summary": {
        "totalGoals": 3,
        "activeGoals": 2,
        "goalsProgressed": 2,
        "milestonesCompleted": 1,
        "totalHoursLogged": 12.0,
        "averageProgressIncrease": 6.67,
        "overallSatisfaction": 4.2
      },
      "goalDetails": [
        {
          "goalId": "goal_001",
          "goalTitle": "AWS Professional資格取得",
          "startProgress": 70.5,
          "endProgress": 85.0,
          "progressIncrease": 14.5,
          "hoursSpent": 8.0,
          "milestonesCompleted": 1,
          "status": "ahead_of_schedule"
        },
        {
          "goalId": "goal_002",
          "goalTitle": "React Native習得",
          "startProgress": 25.0,
          "endProgress": 35.0,
          "progressIncrease": 10.0,
          "hoursSpent": 4.0,
          "milestonesCompleted": 0,
          "status": "on_track"
        }
      ],
      "achievements": [
        {
          "achievementId": "achievement_002",
          "title": "早期達成",
          "earnedDate": "2025-05-30"
        }
      ],
      "challenges": [
        {
          "challengeId": "challenge_001",
          "title": "時間確保の困難",
          "status": "resolved",
          "resolution": "朝の時間活用で解決"
        }
      ],
      "insights": {
        "strengths": ["継続的な学習習慣", "計画的な進行"],
        "improvements": ["より具体的な時間管理", "弱点分野の集中学習"],
        "trends": {
          "learningVelocity": "increasing",
          "timeEfficiency": "stable",
          "goalAlignment": "high"
        }
      },
      "nextWeekRecommendations": [
        {
          "type": "goal_acceleration",
          "description": "AWS試験の前倒し受験を検討",
          "priority": "medium"
        },
        {
          "type": "skill_diversification",
          "description": "React Nativeの実践プロジェクト開始",
          "priority": "high"
        }
      ],
      "generatedAt": "2025-05-30T21:45:00Z"
    }
  }
}
```

---

## エラーコード一覧

| エラーコード | HTTPステータス | 説明 | 対処法 |
|-------------|---------------|------|--------|
| UNAUTHORIZED | 401 | 認証エラー | 有効なJWTトークンを設定 |
| FORBIDDEN | 403 | アクセス権限なし | 目標進捗更新権限が必要 |
| USER_NOT_FOUND | 404 | ユーザーが見つからない | 正しいユーザーIDを指定 |
| GOAL_NOT_FOUND | 404 | 目標が見つからない | 正しい目標IDを指定 |
| MILESTONE_NOT_FOUND | 404 | マイルストーンが見つからない | 正しいマイルストーンIDを指定 |
| VALIDATION_ERROR | 400 | バリデーションエラー | 入力データを確認 |
| INVALID_PROGRESS_VALUE | 400 | 無効な進捗値 | 進捗は0-100の範囲で指定 |
| MILESTONE_ALREADY_COMPLETED | 409 | マイルストーンが既に完了済み | 完了済みマイルストーンは更新不可 |
| EVIDENCE_UPLOAD_FAILED | 500 | エビデンスアップロード失敗 | ファイルサイズ・形式を確認 |
| TENANT_MISMATCH | 403 | テナント不一致 | 同一テナント内のデータのみ更新可能 |
| CONCURRENT_UPDATE_ERROR | 409 | 同時更新エラー | 最新データを取得して再試行 |
| INTERNAL_SERVER_ERROR | 500 | サーバー内部エラー | システム管理者に連絡 |

---

## セキュリティ要件

### 認証・認可
- **認証**: JWT Bearer Token必須
- **権限**: 目標進捗更新権限（goal_progress:update）
- **テナント分離**: テナント内データのみ更新可能

### データ保護
- **個人情報保護**: 本人または管理者のみ更新可能
- **エビデンス保護**: アップロードファイルのウイルススキャン
- **更新履歴**: 全更新操作を監査ログに記録

---

## パフォーマンス要件

| 項目 | 要件 |
|------|------|
| レスポンス時間 | 95%のリクエストが2秒以内 |
| スループット | 100 req/sec |
| ファイルアップロード | 最大10MB |
| 一括更新 | 最大50件 |

---

## テスト仕様

### 単体テスト
```typescript
describe('Goal Progress Update API', () => {
  test('PUT /api/goal-progress/{user_id} - 進捗更新', async () => {
    const progressData = {
      goalProgress: [
        {
          goalId: 'goal_001',
          progressPercentage: 75.5,
          status: 'in_progress',
          timeTracking: {
            totalHoursSpent: 45.5,
            thisWeekHours: 8.0
          }
        }
      ]
    };
    
    const response = await request(app)
      .put('/api/goal-progress/user_001')
      .set('Authorization', `Bearer ${userToken}`)
      .send(progressData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.updatedGoals).toBeInstanceOf(Array);
    expect(response.body.data.progressSummary).toBeDefined();
  });
  
  test('PUT /api/goal-progress/{user_id}/bulk - 一括更新', async () => {
    const bulkData = {
      bulkUpdates: [
        {
          goalId: 'goal_001',
          progressPercentage: 80.0,
          hoursSpent: 5.0,
          note: 'テスト更新'
        }
      ],
      weeklyReflection: {
        achievements: 'テスト達成',
        overallSatisfaction: 4
      }
    };
    
    const response = await request(app)
      .put('/api/goal-progress/user_001/bulk')
      .set('Authorization', `Bearer ${userToken}`)
      .send(bulkData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.bulkUpdateSummary).toBeDefined();
    expect(response.body.data.updatedGoals).toBeInstanceOf(Array);
  });
  
  test('PUT /api/goal-progress/{user_id}/milestone/{milestone_id}/complete - マイルストーン完了', async () => {
    const completionData = {
      completedDate: '2025-05-30T21:40:00Z',
      evidence: {
        type: 'certificate',
        url: 'https://example.com/cert.pdf',
        description: 'テスト証明書'
      },
      actualHours: 12.5,
      skillsGained: ['テストスキル']
    };
    
    const response = await request(app)
      .put('/api/goal-progress/user_001/milestone/milestone_001/complete')
      .set('Authorization', `Bearer ${userToken}`)
      .send(completionData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.completedMilestone).toBeDefined();
    expect(response.body.data.goalUpdate).toBeDefined();
  });
  
  test('POST /api/goal-progress/{user_id}/report - 進捗レポート生成', async () => {
    const reportData = {
      reportType: 'weekly',
      period: {
        startDate: '2025-05-26',
        endDate: '2025-06-01'
      },
      includeDetails: true
    };
    
    const response = await request(app)
      .post('/api/goal-progress/user_001/report')
      .set('Authorization', `Bearer ${userToken}`)
      .send(reportData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.progressReport).toBeDefined();
    expect(response.body.data.progressReport.summary).toBeDefined();
  });
});
```

### 統合テスト
```typescript
describe('Goal Progress Integration', () => {
  test('進捗更新からレポート生成まで', async () => {
    // 1. 進捗更新
    const updateResponse = await updateGoalProgress('user_001', {
      goalProgress: [{
        goalId: 'goal_001',
        progressPercentage: 80.0,
        status: 'in_progress'
      }]
    });
    
    expect(updateResponse.data.updatedGoals[0].progressPercentage).toBe(80.0);
    
    // 2. マイルストーン完了
    const milestoneResponse = await completeMilestone('user_001', 'milestone_001', {
      completedDate: new Date().toISOString(),
      actualHours: 10.0
    });
    
    expect(milestoneResponse.data.completedMilestone).toBeDefined();
    
    // 3. レポート生成
    const reportResponse = await generateProgressReport('user_001', {
      reportType: 'weekly',
      period: { startDate: '2025-05-26', endDate: '2025-06-01' }
    });
    
    expect(reportResponse.data.progressReport.summary.milestonesCompleted).toBeGreaterThan(0);
  });
  
  test('権限制御確認', async () => {
    // 他ユーザーの進捗更新試行
    const response = await request(app)
      .put('/api/goal-progress/other_user')
      .set('Authorization', `Bearer ${userToken}`)
      .send({
        goalProgress: [{ goalId: 'goal_001', progressPercentage: 50.0 }]
      })
      .expect(403);
    
    expect(response.body.error.code).toBe('FORBIDDEN');
  });
  
  test('同時更新制御確認', async () => {
    // 同じ目標に対する同時更新
    const updatePromises = [
      updateGoalProgress('user_001', {
        goalProgress: [{ goalId: 'goal_001', progressPercentage: 70.0 }]
      }),
      updateGoalProgress('user_001', {
        goalProgress: [{ goalId: 'goal_001', progressPercentage: 75.0 }]
      })
    ];
    
    const results = await Promise.allSettled(updatePromises);
    
    // 一方は成功、一方は競合エラー
    expect(results.some(r => r
