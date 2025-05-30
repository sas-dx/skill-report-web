# API定義書: API-091 ダッシュボードデータ取得API

## 基本情報

| 項目 | 内容 |
|------|------|
| API ID | API-091 |
| API名称 | ダッシュボードデータ取得API |
| エンドポイント | /api/dashboard |
| 概要 | ダッシュボード表示データ取得 |
| 利用画面 | SCR-HOME |
| 優先度 | 最高 |
| 実装予定 | Week 1-2 |

---

## エンドポイント詳細

### 1. ダッシュボード全体データ取得

#### リクエスト
```http
GET /api/dashboard
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### クエリパラメータ
| パラメータ名 | 型 | 必須 | 説明 | 例 |
|-------------|---|------|------|---|
| period | string | × | 期間指定（デフォルト: current_quarter） | current_quarter, last_quarter, current_year |
| includeTeamData | boolean | × | チームデータ含有フラグ | true, false |
| includeNotifications | boolean | × | 通知データ含有フラグ | true, false |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_001",
      "displayName": "田中太郎",
      "email": "tanaka@company-a.com",
      "employeeId": "EMP001",
      "departmentName": "開発部",
      "positionName": "シニアエンジニア",
      "avatarUrl": "https://storage.example.com/avatars/user_001.jpg",
      "lastLoginAt": "2025-05-30T21:07:00Z"
    },
    "skillSummary": {
      "totalSkills": 45,
      "skillsByLevel": {
        "×": 5,
        "△": 15,
        "○": 20,
        "◎": 5
      },
      "skillsByCategory": {
        "technical": 25,
        "business": 12,
        "management": 8
      },
      "recentUpdates": [
        {
          "skillId": "skill_001",
          "skillName": "JavaScript",
          "previousLevel": "○",
          "currentLevel": "◎",
          "updatedAt": "2025-05-28T14:30:00Z"
        },
        {
          "skillId": "skill_015",
          "skillName": "TypeScript",
          "previousLevel": "△",
          "currentLevel": "○",
          "updatedAt": "2025-05-25T10:15:00Z"
        }
      ],
      "topSkills": [
        {
          "skillId": "skill_001",
          "skillName": "JavaScript",
          "level": "◎",
          "categoryName": "プログラミング言語"
        },
        {
          "skillId": "skill_003",
          "skillName": "React",
          "level": "◎",
          "categoryName": "フレームワーク"
        },
        {
          "skillId": "skill_004",
          "skillName": "AWS",
          "level": "○",
          "categoryName": "クラウド"
        }
      ],
      "skillGrowthTrend": {
        "thisQuarter": 8,
        "lastQuarter": 5,
        "growthRate": 60.0
      }
    },
    "goalSummary": {
      "currentGoals": 3,
      "completedGoals": 8,
      "overallProgress": 75.5,
      "goalsByStatus": {
        "not_started": 0,
        "in_progress": 2,
        "completed": 1,
        "on_hold": 0
      },
      "upcomingDeadlines": [
        {
          "goalId": "goal_001",
          "goalTitle": "AWS Professional資格取得",
          "deadline": "2025-08-31",
          "progress": 60,
          "daysRemaining": 93,
          "priority": "high"
        },
        {
          "goalId": "goal_002",
          "goalTitle": "React Native習得",
          "deadline": "2025-07-15",
          "progress": 30,
          "daysRemaining": 46,
          "priority": "medium"
        }
      ],
      "recentAchievements": [
        {
          "goalId": "goal_003",
          "goalTitle": "Docker基礎習得",
          "completedAt": "2025-05-20T16:00:00Z",
          "category": "技術スキル"
        }
      ],
      "goalProgressTrend": {
        "thisQuarter": 75.5,
        "lastQuarter": 60.2,
        "improvementRate": 25.4
      }
    },
    "certificationSummary": {
      "totalCertifications": 5,
      "activeCertifications": 4,
      "expiringSoon": [
        {
          "certificationId": "cert_001",
          "certificationName": "AWS Solutions Architect Associate",
          "expiryDate": "2025-09-15",
          "daysUntilExpiry": 108,
          "renewalRequired": true
        }
      ],
      "recentCertifications": [
        {
          "certificationId": "cert_005",
          "certificationName": "Google Cloud Professional",
          "obtainedDate": "2025-05-10",
          "validUntil": "2028-05-10"
        }
      ]
    },
    "workSummary": {
      "thisMonth": {
        "totalHours": 168,
        "projectHours": 140,
        "trainingHours": 20,
        "meetingHours": 8
      },
      "recentProjects": [
        {
          "projectId": "proj_001",
          "projectName": "ECサイトリニューアル",
          "role": "フロントエンドリード",
          "startDate": "2025-04-01",
          "endDate": "2025-07-31",
          "progress": 65,
          "usedSkills": ["React", "TypeScript", "AWS"]
        },
        {
          "projectId": "proj_002",
          "projectName": "API基盤構築",
          "role": "バックエンドエンジニア",
          "startDate": "2025-03-15",
          "endDate": "2025-06-30",
          "progress": 80,
          "usedSkills": ["Node.js", "PostgreSQL", "Docker"]
        }
      ],
      "skillUtilization": {
        "mostUsedSkills": [
          { "skillName": "JavaScript", "usageHours": 45 },
          { "skillName": "React", "usageHours": 38 },
          { "skillName": "TypeScript", "usageHours": 32 }
        ]
      }
    },
    "teamSummary": {
      "teamMembers": 8,
      "teamSkillCoverage": 85.5,
      "teamGoalProgress": 72.3,
      "skillGaps": [
        {
          "skillName": "Kubernetes",
          "currentLevel": "△",
          "targetLevel": "○",
          "priority": "high"
        },
        {
          "skillName": "GraphQL",
          "currentLevel": "×",
          "targetLevel": "△",
          "priority": "medium"
        }
      ],
      "topPerformers": [
        {
          "userId": "user_002",
          "displayName": "佐藤花子",
          "skillGrowth": 12,
          "goalCompletion": 90
        }
      ]
    },
    "notifications": {
      "unreadCount": 3,
      "recentNotifications": [
        {
          "id": "notif_001",
          "type": "skill_expiry",
          "title": "資格期限のお知らせ",
          "message": "AWS Solutions Architect Associateの期限が近づいています",
          "createdAt": "2025-05-30T09:00:00Z",
          "priority": "high",
          "isRead": false
        },
        {
          "id": "notif_002",
          "type": "goal_reminder",
          "title": "目標進捗確認",
          "message": "四半期目標の進捗確認をお願いします",
          "createdAt": "2025-05-29T10:00:00Z",
          "priority": "medium",
          "isRead": false
        }
      ]
    },
    "analytics": {
      "skillGrowthChart": {
        "labels": ["1月", "2月", "3月", "4月", "5月"],
        "data": [40, 42, 43, 44, 45],
        "trend": "increasing"
      },
      "goalProgressChart": {
        "labels": ["Q1", "Q2", "Q3", "Q4"],
        "data": [45, 60, 75, 85],
        "trend": "increasing"
      },
      "skillDistribution": {
        "technical": 55.6,
        "business": 26.7,
        "management": 17.7
      }
    },
    "recommendations": [
      {
        "type": "skill_improvement",
        "title": "Kubernetes学習の推奨",
        "description": "チームのスキルギャップ解消のため、Kubernetesの学習を推奨します",
        "priority": "high",
        "estimatedHours": 40,
        "resources": [
          {
            "type": "course",
            "title": "Kubernetes基礎コース",
            "url": "https://learning.example.com/kubernetes-basics"
          }
        ]
      },
      {
        "type": "certification",
        "title": "AWS Professional資格取得",
        "description": "現在の目標に基づき、AWS Professional資格の取得を推奨します",
        "priority": "medium",
        "deadline": "2025-08-31"
      }
    ],
    "lastUpdated": "2025-05-30T21:07:00Z"
  }
}
```

### 2. ダッシュボード部分データ取得

#### リクエスト
```http
GET /api/dashboard/{section}
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### パスパラメータ
| パラメータ名 | 型 | 必須 | 説明 |
|-------------|---|------|------|
| section | string | ○ | 取得セクション（skills, goals, certifications, work, team, notifications, analytics） |

#### レスポンス例（skills セクション）
```json
{
  "success": true,
  "data": {
    "skillSummary": {
      "totalSkills": 45,
      "skillsByLevel": {
        "×": 5,
        "△": 15,
        "○": 20,
        "◎": 5
      },
      "skillsByCategory": {
        "technical": 25,
        "business": 12,
        "management": 8
      },
      "recentUpdates": [
        {
          "skillId": "skill_001",
          "skillName": "JavaScript",
          "previousLevel": "○",
          "currentLevel": "◎",
          "updatedAt": "2025-05-28T14:30:00Z"
        }
      ],
      "topSkills": [
        {
          "skillId": "skill_001",
          "skillName": "JavaScript",
          "level": "◎",
          "categoryName": "プログラミング言語"
        }
      ],
      "skillGrowthTrend": {
        "thisQuarter": 8,
        "lastQuarter": 5,
        "growthRate": 60.0
      }
    },
    "lastUpdated": "2025-05-30T21:07:00Z"
  }
}
```

### 3. ダッシュボード設定取得

#### リクエスト
```http
GET /api/dashboard/settings
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "dashboardSettings": {
      "layout": "default",
      "visibleSections": [
        "skillSummary",
        "goalSummary",
        "certificationSummary",
        "workSummary",
        "notifications"
      ],
      "sectionOrder": [
        "skillSummary",
        "goalSummary",
        "workSummary",
        "certificationSummary",
        "notifications"
      ],
      "refreshInterval": 300,
      "theme": "light",
      "chartType": "line",
      "showTeamData": true,
      "showRecommendations": true,
      "notificationSettings": {
        "showUnreadOnly": false,
        "maxNotifications": 5
      }
    },
    "lastUpdated": "2025-05-30T15:30:00Z"
  }
}
```

### 4. ダッシュボード設定更新

#### リクエスト
```http
PUT /api/dashboard/settings
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "dashboardSettings": {
    "layout": "compact",
    "visibleSections": [
      "skillSummary",
      "goalSummary",
      "notifications"
    ],
    "sectionOrder": [
      "goalSummary",
      "skillSummary",
      "notifications"
    ],
    "refreshInterval": 600,
    "theme": "dark",
    "chartType": "bar",
    "showTeamData": false,
    "showRecommendations": true,
    "notificationSettings": {
      "showUnreadOnly": true,
      "maxNotifications": 3
    }
  }
}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "message": "ダッシュボード設定が更新されました",
    "dashboardSettings": {
      "layout": "compact",
      "visibleSections": [
        "skillSummary",
        "goalSummary",
        "notifications"
      ],
      "sectionOrder": [
        "goalSummary",
        "skillSummary",
        "notifications"
      ],
      "refreshInterval": 600,
      "theme": "dark",
      "chartType": "bar",
      "showTeamData": false,
      "showRecommendations": true,
      "notificationSettings": {
        "showUnreadOnly": true,
        "maxNotifications": 3
      }
    },
    "updatedAt": "2025-05-30T21:10:00Z"
  }
}
```

---

## エラーコード一覧

| エラーコード | HTTPステータス | 説明 | 対処法 |
|-------------|---------------|------|--------|
| UNAUTHORIZED | 401 | 認証エラー | 有効なJWTトークンを設定 |
| FORBIDDEN | 403 | アクセス権限なし | ダッシュボード閲覧権限が必要 |
| INVALID_SECTION | 400 | 無効なセクション指定 | 有効なセクション名を指定 |
| INVALID_PERIOD | 400 | 無効な期間指定 | 有効な期間を指定 |
| DATA_NOT_FOUND | 404 | データが見つからない | データが存在しない可能性 |
| SETTINGS_VALIDATION_ERROR | 400 | 設定バリデーションエラー | 設定値を確認 |
| TENANT_MISMATCH | 403 | テナント不一致 | 正しいテナントでアクセス |
| CACHE_ERROR | 500 | キャッシュエラー | 一時的なエラー、再試行 |
| INTERNAL_SERVER_ERROR | 500 | サーバー内部エラー | システム管理者に連絡 |

---

## セキュリティ要件

### 認証・認可
- **認証**: JWT Bearer Token必須
- **権限**: ダッシュボード閲覧権限（dashboard:read）
- **テナント分離**: テナント内データのみアクセス可能

### データ保護
- **個人情報保護**: 権限に応じたデータフィルタリング
- **チームデータ**: 管理者権限またはチーム所属確認
- **機密データ**: 給与・評価情報は除外

---

## パフォーマンス要件

| 項目 | 要件 |
|------|------|
| レスポンス時間 | 95%のリクエストが1秒以内 |
| スループット | 500 req/sec |
| データサイズ | 1レスポンスあたり最大2MB |
| キャッシュ | Redis使用、TTL 300秒 |

---

## テスト仕様

### 単体テスト
```typescript
describe('Dashboard API', () => {
  test('GET /api/dashboard - 全体データ取得', async () => {
    const response = await request(app)
      .get('/api/dashboard')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.user).toBeDefined();
    expect(response.body.data.skillSummary).toBeDefined();
    expect(response.body.data.goalSummary).toBeDefined();
    expect(response.body.data.certificationSummary).toBeDefined();
  });
  
  test('GET /api/dashboard/skills - スキルセクション取得', async () => {
    const response = await request(app)
      .get('/api/dashboard/skills')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.skillSummary).toBeDefined();
    expect(response.body.data.skillSummary.totalSkills).toBeGreaterThan(0);
  });
  
  test('GET /api/dashboard/settings - 設定取得', async () => {
    const response = await request(app)
      .get('/api/dashboard/settings')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.dashboardSettings).toBeDefined();
    expect(response.body.data.dashboardSettings.visibleSections).toBeInstanceOf(Array);
  });
  
  test('PUT /api/dashboard/settings - 設定更新', async () => {
    const settingsData = {
      dashboardSettings: {
        layout: 'compact',
        visibleSections: ['skillSummary', 'goalSummary'],
        theme: 'dark'
      }
    };
    
    const response = await request(app)
      .put('/api/dashboard/settings')
      .set('Authorization', `Bearer ${userToken}`)
      .send(settingsData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.dashboardSettings.layout).toBe('compact');
    expect(response.body.data.dashboardSettings.theme).toBe('dark');
  });
});
```

### 統合テスト
```typescript
describe('Dashboard Integration', () => {
  test('ダッシュボードデータの整合性確認', async () => {
    // 1. 全体データ取得
    const dashboardResponse = await getDashboardData();
    
    // 2. 個別セクションデータ取得
    const skillsResponse = await getDashboardSection('skills');
    const goalsResponse = await getDashboardSection('goals');
    
    // 3. データ整合性確認
    expect(dashboardResponse.data.skillSummary.totalSkills)
      .toBe(skillsResponse.data.skillSummary.totalSkills);
    expect(dashboardResponse.data.goalSummary.currentGoals)
      .toBe(goalsResponse.data.goalSummary.currentGoals);
  });
  
  test('キャッシュ動作確認', async () => {
    // 1. 初回リクエスト
    const start1 = Date.now();
    const response1 = await getDashboardData();
    const time1 = Date.now() - start1;
    
    // 2. 2回目リクエスト（キャッシュから）
    const start2 = Date.now();
    const response2 = await getDashboardData();
    const time2 = Date.now() - start2;
    
    // キャッシュにより高速化されることを確認
    expect(time2).toBeLessThan(time1 * 0.5);
    expect(response1.data.lastUpdated).toBe(response2.data.lastUpdated);
  });
  
  test('権限制御確認', async () => {
    // 一般ユーザーでチームデータアクセス
    const response = await request(app)
      .get('/api/dashboard?includeTeamData=true')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(200);
    
    // チームデータが制限されることを確認
    expect(response.body.data.teamSummary).toBeUndefined();
  });
});
```

---

## 実装メモ

### データベーススキーマ
```sql
CREATE TABLE dashboard_settings (
  id VARCHAR(50) PRIMARY KEY,
  user_id VARCHAR(50) NOT NULL,
  tenant_id VARCHAR(50) NOT NULL,
  settings JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id),
  UNIQUE(user_id, tenant_id)
);

CREATE TABLE dashboard_cache (
  id VARCHAR(50) PRIMARY KEY,
  user_id VARCHAR(50) NOT NULL,
  tenant_id VARCHAR(50) NOT NULL,
  cache_key VARCHAR(255) NOT NULL,
  cache_data JSONB NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id),
  UNIQUE(user_id, tenant_id, cache_key)
);

CREATE INDEX idx_dashboard_settings_user_id ON dashboard_settings(user_id);
CREATE INDEX idx_dashboard_settings_tenant_id ON dashboard_settings(tenant_id);
CREATE INDEX idx_dashboard_cache_user_id ON dashboard_cache(user_id);
CREATE INDEX idx_dashboard_cache_expires_at ON dashboard_cache(expires_at);
```

### Next.js実装例
```typescript
// pages/api/dashboard/index.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { authenticateToken } from '@/lib/auth';
import { DashboardService } from '@/services/DashboardService';
import { CacheService } from '@/services/CacheService';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ success: false, error: 'Method not allowed' });
  }
  
  try {
    const user = await authenticateToken(req);
    const { period, includeTeamData, includeNotifications } = req.query;
    
    const dashboardService = new DashboardService();
    const cacheService = new CacheService();
    
    // キャッシュキー生成
    const cacheKey = `dashboard:${user.id}:${user.tenantId}:${period || 'current_quarter'}:${includeTeamData}:${includeNotifications}`;
    
    // キャッシュ確認
    let dashboardData = await cacheService.get(cacheKey);
    
    if (!dashboardData) {
      // データ取得
      dashboardData = await dashboardService.getDashboardData(user.id, user.tenantId, {
        period: period as string || 'current_quarter',
        includeTeamData: includeTeamData === 'true',
        includeNotifications: includeNotifications === 'true'
      });
      
      // キャッシュ保存（5分間）
      await cacheService.set(cacheKey, dashboardData, 300);
    }
    
    return res.status(200).json({
      success: true,
      data: dashboardData
    });
    
  } catch (error) {
    console.error('Dashboard fetch error:', error);
    return res.status(error.statusCode || 500).json({
      success: false,
      error: {
        code: error.code || 'INTERNAL_SERVER_ERROR',
        message: error.message
      }
    });
  }
}
```

### ダッシュボードサービス実装例
```typescript
// services/DashboardService.ts
export class DashboardService {
  async getDashboardData(userId: string, tenantId: string, options: DashboardOptions) {
    const user = await this.userRepository.findById(userId);
    if (!user) {
      throw new NotFoundError('USER_NOT_FOUND', 'ユーザーが見つかりません');
    }
    
    // 並行してデータ取得
    const [
      skillSummary,
      goalSummary,
      certificationSummary,
      workSummary,
      teamSummary,
      notifications,
      analytics,
      recommendations
    ] = await Promise.all([
      this.getSkillSummary(userId, tenantId, options.period),
      this.getGoalSummary(userId, tenantId, options.period),
      this.getCertificationSummary(userId, tenantId),
      this.getWorkSummary(userId, tenantId, options.period),
      options.includeTeamData ? this.getTeamSummary(userId, tenantId) : null,
      options.includeNotifications ? this.getNotifications(userId, tenantId) : null,
      this.getAnalytics(userId, tenantId, options.period),
      this.getRecommendations(userId, tenantId)
    ]);
    
    return {
      user: this.sanitizeUser(user),
      skillSummary,
      goalSummary,
      certificationSummary,
      workSummary,
      teamSummary,
      notifications,
      analytics,
      recommendations,
      lastUpdated: new Date().toISOString()
    };
  }
  
  private async getSkillSummary(userId: string, tenantId: string, period: string) {
    const skills = await this.skillRepository.findByUserId(userId);
    const recentUpdates = await this.skillHistoryRepository.findRecentUpdates(userId, 5);
    
    const skillsByLevel = skills.reduce((acc, skill) => {
      acc[skill.level] = (acc[skill.level] || 0) + 1;
      return acc;
    }, {});
    
    const skillsByCategory = skills.reduce((acc, skill) => {
      acc[skill.category] = (acc[skill.category] || 0) + 1;
      return acc;
    }, {});
    
    const topSkills = skills
      .filter(skill => skill.level === '◎')
      .slice(0, 5)
      .map(skill => ({
        skillId: skill.id,
        skillName: skill.name,
        level: skill.level,
        categoryName: skill.categoryName
      }));
    
    const skillGrowthTrend = await this.calculateSkillGrowthTrend(userId, period);
    
    return {
      totalSkills: skills.length,
      skillsByLevel,
      skillsByCategory,
      recentUpdates,
      topSkills,
      skillGrowthTrend
    };
  }
  
  private async getGoalSummary(userId: string, tenantId: string, period: string) {
    const goals = await this.goalRepository.findByUserId(userId);
    const currentGoals = goals.filter(goal => goal.status !== 'completed');
    const completedGoals = goals.filter(goal => goal.status === 'completed');
    
    const goalsByStatus = goals.reduce((acc, goal) => {
      acc[goal.status] = (acc[goal.status] || 0) + 1;
      return acc;
    }, {});
    
    const upcomingDeadlines = currentGoals
      .filter(goal => goal.deadline)
      .sort((a, b) => new Date(a.deadline).getTime() - new Date(b.deadline).getTime())
      .slice(0, 3)
      .map(goal => ({
        goalId: goal.id,
        goalTitle: goal.title,
        deadline: goal.deadline,
        progress: goal.progress,
        daysRemaining: this.calculateDaysRemaining(goal.deadline),
        priority: goal.priority
      }));
    
    const recentAchievements = completedGoals
      .filter(goal => this.isRecentlyCompleted(goal.completedAt, 30))
      .slice(0, 3);
    
    const overallProgress = this.calculateOverallProgress(currentGoals);
    const goalProgressTrend = await this.calculateGoalProgressTrend(userId, period);
    
    return {
      currentGoals: currentGoals.length,
      completedGoals: completedGoals.length,
      overallProgress,
      goalsByStatus,
      upcomingDeadlines,
      recentAchievements,
      goalProgressTrend
    };
  }
  
  private async getRecommendations(userId: string, tenantId: string) {
    const recommendations = [];
    
    // スキルギャップ分析
    const skillGaps = await this.analyzeSkillGaps(userId, tenant
