# API仕様書: API-092 ユーザーサマリー取得API

## 基本情報

| 項目 | 内容 |
|------|------|
| API ID | API-092 |
| API名称 | ユーザーサマリー取得API |
| エンドポイント | /api/dashboard/user-summary |
| 概要 | ユーザー情報サマリー取得 |
| 利用画面 | SCR-HOME |
| 優先度 | 最高 |
| 実装予定 | Week 1-2 |

---

## エンドポイント詳細

### 1. 自分のユーザーサマリー取得

#### リクエスト
```http
GET /api/dashboard/user-summary
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### クエリパラメータ
| パラメータ名 | 型 | 必須 | 説明 | 例 |
|-------------|---|------|------|---|
| includeStats | boolean | × | 統計情報含有フラグ | true, false |
| includeComparison | boolean | × | 比較データ含有フラグ | true, false |
| period | string | × | 期間指定（デフォルト: current_quarter） | current_quarter, last_quarter, current_year |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "userProfile": {
      "id": "user_001",
      "displayName": "田中太郎",
      "email": "tanaka@company-a.com",
      "employeeId": "EMP001",
      "avatarUrl": "https://storage.example.com/avatars/user_001.jpg",
      "organizationInfo": {
        "departmentName": "開発部",
        "divisionName": "システム開発課",
        "positionName": "シニアエンジニア",
        "managerName": "佐藤部長",
        "hireDate": "2020-04-01",
        "yearsOfService": 5.2
      },
      "contactInfo": {
        "phoneNumber": "090-1234-5678",
        "workLocation": "東京本社",
        "workStyle": "hybrid"
      },
      "systemInfo": {
        "lastLoginAt": "2025-05-30T21:09:00Z",
        "loginCount": 1247,
        "accountStatus": "active",
        "memberSince": "2020-04-01T09:00:00Z"
      }
    },
    "skillOverview": {
      "totalSkills": 45,
      "skillLevel": {
        "average": 2.8,
        "distribution": {
          "×": 5,
          "△": 15,
          "○": 20,
          "◎": 5
        }
      },
      "topCategories": [
        {
          "categoryName": "プログラミング言語",
          "skillCount": 8,
          "averageLevel": 3.2,
          "topSkills": ["JavaScript", "TypeScript", "Python"]
        },
        {
          "categoryName": "フレームワーク",
          "skillCount": 6,
          "averageLevel": 2.9,
          "topSkills": ["React", "Next.js", "Express"]
        },
        {
          "categoryName": "クラウド",
          "skillCount": 4,
          "averageLevel": 2.5,
          "topSkills": ["AWS", "Docker", "Kubernetes"]
        }
      ],
      "recentGrowth": {
        "skillsAdded": 3,
        "skillsImproved": 5,
        "period": "last_30_days"
      },
      "certifications": {
        "total": 5,
        "active": 4,
        "expiringSoon": 1,
        "recentlyObtained": [
          {
            "name": "Google Cloud Professional",
            "obtainedDate": "2025-05-10"
          }
        ]
      }
    },
    "goalOverview": {
      "currentGoals": 3,
      "completedGoals": 8,
      "overallProgress": 75.5,
      "goalsByPriority": {
        "high": 1,
        "medium": 2,
        "low": 0
      },
      "upcomingMilestones": [
        {
          "goalTitle": "AWS Professional資格取得",
          "milestone": "模擬試験完了",
          "dueDate": "2025-06-15",
          "progress": 60
        }
      ],
      "recentAchievements": [
        {
          "goalTitle": "Docker基礎習得",
          "completedDate": "2025-05-20",
          "category": "技術スキル"
        }
      ],
      "goalCompletion": {
        "thisQuarter": 2,
        "lastQuarter": 3,
        "thisYear": 8
      }
    },
    "workOverview": {
      "currentProjects": [
        {
          "projectName": "ECサイトリニューアル",
          "role": "フロントエンドリード",
          "progress": 65,
          "endDate": "2025-07-31",
          "teamSize": 6
        },
        {
          "projectName": "API基盤構築",
          "role": "バックエンドエンジニア",
          "progress": 80,
          "endDate": "2025-06-30",
          "teamSize": 4
        }
      ],
      "workloadSummary": {
        "thisMonth": {
          "totalHours": 168,
          "projectHours": 140,
          "trainingHours": 20,
          "meetingHours": 8
        },
        "utilizationRate": 85.5,
        "overtimeHours": 12
      },
      "skillUtilization": {
        "mostUsedSkills": [
          { "skillName": "JavaScript", "hours": 45, "percentage": 26.8 },
          { "skillName": "React", "hours": 38, "percentage": 22.6 },
          { "skillName": "TypeScript", "hours": 32, "percentage": 19.0 }
        ],
        "underutilizedSkills": [
          { "skillName": "Python", "lastUsed": "2025-03-15" },
          { "skillName": "GraphQL", "lastUsed": "2025-02-20" }
        ]
      }
    },
    "performanceMetrics": {
      "skillGrowthRate": {
        "thisQuarter": 8,
        "lastQuarter": 5,
        "yearToDate": 18,
        "trend": "increasing"
      },
      "goalAchievementRate": {
        "thisQuarter": 66.7,
        "lastQuarter": 75.0,
        "yearToDate": 72.7,
        "trend": "stable"
      },
      "learningActivity": {
        "coursesCompleted": 3,
        "trainingHours": 45,
        "certificationsObtained": 1,
        "period": "last_90_days"
      },
      "teamContribution": {
        "knowledgeSharing": 8,
        "mentoring": 2,
        "codeReviews": 24,
        "period": "last_30_days"
      }
    },
    "recommendations": [
      {
        "type": "skill_development",
        "title": "Kubernetes学習の推奨",
        "description": "現在のプロジェクトでKubernetesの需要が高まっています",
        "priority": "high",
        "estimatedBenefit": "プロジェクト効率向上",
        "resources": [
          {
            "type": "course",
            "title": "Kubernetes基礎コース",
            "duration": "40時間"
          }
        ]
      },
      {
        "type": "certification",
        "title": "AWS Professional資格更新",
        "description": "現在の目標に基づく資格取得を推奨",
        "priority": "medium",
        "deadline": "2025-08-31"
      },
      {
        "type": "career_development",
        "title": "リーダーシップスキル向上",
        "description": "チームリード経験を活かしたスキル向上",
        "priority": "medium",
        "estimatedBenefit": "キャリア発展"
      }
    ],
    "comparisonData": {
      "departmentAverage": {
        "skillCount": 38.2,
        "goalCompletionRate": 68.5,
        "learningHours": 32.1
      },
      "positionAverage": {
        "skillCount": 42.8,
        "goalCompletionRate": 71.3,
        "learningHours": 38.7
      },
      "userRanking": {
        "skillGrowth": {
          "rank": 3,
          "total": 25,
          "percentile": 88
        },
        "goalAchievement": {
          "rank": 5,
          "total": 25,
          "percentile": 80
        }
      }
    },
    "lastUpdated": "2025-05-30T21:09:00Z"
  }
}
```

### 2. 指定ユーザーのサマリー取得

#### リクエスト
```http
GET /api/dashboard/user-summary/{user_id}
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### パスパラメータ
| パラメータ名 | 型 | 必須 | 説明 |
|-------------|---|------|------|
| user_id | string | ○ | ユーザーID |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "userProfile": {
      "id": "user_002",
      "displayName": "佐藤花子",
      "email": "sato@company-a.com",
      "employeeId": "EMP002",
      "avatarUrl": "https://storage.example.com/avatars/user_002.jpg",
      "organizationInfo": {
        "departmentName": "開発部",
        "divisionName": "システム開発課",
        "positionName": "エンジニア",
        "managerName": "佐藤部長",
        "hireDate": "2022-04-01",
        "yearsOfService": 3.1
      },
      "systemInfo": {
        "lastLoginAt": "2025-05-30T18:30:00Z",
        "accountStatus": "active",
        "memberSince": "2022-04-01T09:00:00Z"
      }
    },
    "skillOverview": {
      "totalSkills": 32,
      "skillLevel": {
        "average": 2.4,
        "distribution": {
          "×": 8,
          "△": 12,
          "○": 10,
          "◎": 2
        }
      },
      "topCategories": [
        {
          "categoryName": "プログラミング言語",
          "skillCount": 6,
          "averageLevel": 2.8,
          "topSkills": ["Python", "JavaScript", "Java"]
        }
      ],
      "certifications": {
        "total": 3,
        "active": 3,
        "expiringSoon": 0
      }
    },
    "goalOverview": {
      "currentGoals": 2,
      "completedGoals": 5,
      "overallProgress": 82.5,
      "goalCompletion": {
        "thisQuarter": 2,
        "lastQuarter": 2,
        "thisYear": 5
      }
    },
    "performanceMetrics": {
      "skillGrowthRate": {
        "thisQuarter": 6,
        "trend": "increasing"
      },
      "goalAchievementRate": {
        "thisQuarter": 100.0,
        "trend": "excellent"
      }
    },
    "lastUpdated": "2025-05-30T21:09:00Z"
  }
}
```

### 3. チームメンバーサマリー一覧取得

#### リクエスト
```http
GET /api/dashboard/user-summary/team
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### クエリパラメータ
| パラメータ名 | 型 | 必須 | 説明 | 例 |
|-------------|---|------|------|---|
| department | string | × | 部署フィルタ | 開発部 |
| sortBy | string | × | ソート基準 | skillGrowth, goalCompletion, lastLogin |
| order | string | × | ソート順 | asc, desc |
| limit | number | × | 取得件数（デフォルト: 20） | 20 |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "teamMembers": [
      {
        "id": "user_002",
        "displayName": "佐藤花子",
        "email": "sato@company-a.com",
        "positionName": "エンジニア",
        "avatarUrl": "https://storage.example.com/avatars/user_002.jpg",
        "skillSummary": {
          "totalSkills": 32,
          "averageLevel": 2.4,
          "recentGrowth": 6
        },
        "goalSummary": {
          "currentGoals": 2,
          "completionRate": 100.0,
          "overallProgress": 82.5
        },
        "performance": {
          "skillGrowthRank": 1,
          "goalAchievementRank": 1,
          "lastLoginAt": "2025-05-30T18:30:00Z"
        }
      },
      {
        "id": "user_001",
        "displayName": "田中太郎",
        "email": "tanaka@company-a.com",
        "positionName": "シニアエンジニア",
        "avatarUrl": "https://storage.example.com/avatars/user_001.jpg",
        "skillSummary": {
          "totalSkills": 45,
          "averageLevel": 2.8,
          "recentGrowth": 8
        },
        "goalSummary": {
          "currentGoals": 3,
          "completionRate": 66.7,
          "overallProgress": 75.5
        },
        "performance": {
          "skillGrowthRank": 2,
          "goalAchievementRank": 3,
          "lastLoginAt": "2025-05-30T21:09:00Z"
        }
      }
    ],
    "teamStats": {
      "totalMembers": 8,
      "averageSkillCount": 38.2,
      "averageGoalCompletion": 72.8,
      "topPerformers": [
        {
          "userId": "user_002",
          "displayName": "佐藤花子",
          "metric": "goalAchievement",
          "value": 100.0
        }
      ]
    },
    "lastUpdated": "2025-05-30T21:09:00Z"
  }
}
```

---

## エラーコード一覧

| エラーコード | HTTPステータス | 説明 | 対処法 |
|-------------|---------------|------|--------|
| UNAUTHORIZED | 401 | 認証エラー | 有効なJWTトークンを設定 |
| FORBIDDEN | 403 | アクセス権限なし | ユーザーサマリー閲覧権限が必要 |
| USER_NOT_FOUND | 404 | ユーザーが見つからない | 正しいユーザーIDを指定 |
| TENANT_MISMATCH | 403 | テナント不一致 | 同一テナント内のユーザーのみアクセス可能 |
| INVALID_PARAMETER | 400 | パラメータエラー | クエリパラメータを確認 |
| PRIVACY_RESTRICTION | 403 | プライバシー制限 | ユーザーのプライバシー設定により閲覧不可 |
| DATA_NOT_AVAILABLE | 404 | データが利用できない | データが不足している可能性 |
| CACHE_ERROR | 500 | キャッシュエラー | 一時的なエラー、再試行 |
| INTERNAL_SERVER_ERROR | 500 | サーバー内部エラー | システム管理者に連絡 |

---

## セキュリティ要件

### 認証・認可
- **認証**: JWT Bearer Token必須
- **権限**: ユーザーサマリー閲覧権限（user_summary:read）
- **テナント分離**: テナント内ユーザーのみアクセス可能

### プライバシー保護
- **自分のデータ**: 全情報アクセス可能
- **他ユーザーのデータ**: プライバシー設定に基づく制限
- **チームデータ**: 管理者権限またはチーム所属確認

---

## パフォーマンス要件

| 項目 | 要件 |
|------|------|
| レスポンス時間 | 95%のリクエストが800ms以内 |
| スループット | 300 req/sec |
| データサイズ | 1レスポンスあたり最大1MB |
| キャッシュ | Redis使用、TTL 600秒 |

---

## テスト仕様

### 単体テスト
```typescript
describe('User Summary API', () => {
  test('GET /api/dashboard/user-summary - 自分のサマリー取得', async () => {
    const response = await request(app)
      .get('/api/dashboard/user-summary')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.userProfile).toBeDefined();
    expect(response.body.data.skillOverview).toBeDefined();
    expect(response.body.data.goalOverview).toBeDefined();
    expect(response.body.data.performanceMetrics).toBeDefined();
  });
  
  test('GET /api/dashboard/user-summary/{user_id} - 他ユーザーサマリー取得', async () => {
    const response = await request(app)
      .get('/api/dashboard/user-summary/user_002')
      .set('Authorization', `Bearer ${managerToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.userProfile.id).toBe('user_002');
    expect(response.body.data.skillOverview).toBeDefined();
  });
  
  test('GET /api/dashboard/user-summary/team - チームサマリー取得', async () => {
    const response = await request(app)
      .get('/api/dashboard/user-summary/team')
      .set('Authorization', `Bearer ${managerToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.teamMembers).toBeInstanceOf(Array);
    expect(response.body.data.teamStats).toBeDefined();
  });
  
  test('GET /api/dashboard/user-summary - 統計情報含有', async () => {
    const response = await request(app)
      .get('/api/dashboard/user-summary?includeStats=true&includeComparison=true')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.performanceMetrics).toBeDefined();
    expect(response.body.data.comparisonData).toBeDefined();
  });
});
```

### 統合テスト
```typescript
describe('User Summary Integration', () => {
  test('サマリーデータの整合性確認', async () => {
    // 1. ユーザーサマリー取得
    const summaryResponse = await getUserSummary('user_001');
    
    // 2. 個別データ取得
    const skillsResponse = await getSkills('user_001');
    const goalsResponse = await getGoals('user_001');
    
    // 3. データ整合性確認
    expect(summaryResponse.data.skillOverview.totalSkills)
      .toBe(skillsResponse.data.skills.length);
    expect(summaryResponse.data.goalOverview.currentGoals)
      .toBe(goalsResponse.data.goals.filter(g => g.status !== 'completed').length);
  });
  
  test('プライバシー制御確認', async () => {
    // プライベート設定のユーザーにアクセス
    const response = await request(app)
      .get('/api/dashboard/user-summary/private_user')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(403);
    
    expect(response.body.error.code).toBe('PRIVACY_RESTRICTION');
  });
  
  test('チーム権限確認', async () => {
    // 一般ユーザーでチームサマリーアクセス
    const response = await request(app)
      .get('/api/dashboard/user-summary/team')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(403);
    
    expect(response.body.error.code).toBe('FORBIDDEN');
  });
});
```

---

## 実装メモ

### データベーススキーマ
```sql
CREATE TABLE user_summary_cache (
  id VARCHAR(50) PRIMARY KEY,
  user_id VARCHAR(50) NOT NULL,
  tenant_id VARCHAR(50) NOT NULL,
  summary_type VARCHAR(50) NOT NULL,
  summary_data JSONB NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id),
  UNIQUE(user_id, tenant_id, summary_type)
);

CREATE TABLE user_performance_metrics (
  id VARCHAR(50) PRIMARY KEY,
  user_id VARCHAR(50) NOT NULL,
  tenant_id VARCHAR(50) NOT NULL,
  metric_type VARCHAR(50) NOT NULL,
  metric_value DECIMAL(10,2) NOT NULL,
  period_start DATE NOT NULL,
  period_end DATE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

CREATE INDEX idx_user_summary_cache_user_id ON user_summary_cache(user_id);
CREATE INDEX idx_user_summary_cache_expires_at ON user_summary_cache(expires_at);
CREATE INDEX idx_user_performance_metrics_user_id ON user_performance_metrics(user_id);
CREATE INDEX idx_user_performance_metrics_period ON user_performance_metrics(period_start, period_end);
```

### Next.js実装例
```typescript
// pages/api/dashboard/user-summary/index.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { authenticateToken } from '@/lib/auth';
import { UserSummaryService } from '@/services/UserSummaryService';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ success: false, error: 'Method not allowed' });
  }
  
  try {
    const user = await authenticateToken(req);
    const { includeStats, includeComparison, period } = req.query;
    
    const userSummaryService = new UserSummaryService();
    
    const summaryData = await userSummaryService.getUserSummary(user.id, user.tenantId, {
      includeStats: includeStats === 'true',
      includeComparison: includeComparison === 'true',
      period: period as string || 'current_quarter'
    });
    
    return res.status(200).json({
      success: true,
      data: summaryData
    });
    
  } catch (error) {
    console.error('User summary fetch error:', error);
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

### ユーザーサマリーサービス実装例
```typescript
// services/UserSummaryService.ts
export class UserSummaryService {
  async getUserSummary(userId: string, tenantId: string, options: UserSummaryOptions) {
    // キャッシュ確認
    const cacheKey = `user_summary:${userId}:${tenantId}:${JSON.stringify(options)}`;
    let summaryData = await this.cacheService.get(cacheKey);
    
    if (!summaryData) {
      // データ並行取得
      const [
        userProfile,
        skillOverview,
        goalOverview,
        workOverview,
        performanceMetrics,
        recommendations,
        comparisonData
      ] = await Promise.all([
        this.getUserProfile(userId, tenantId),
        this.getSkillOverview(userId, tenantId, options.period),
        this.getGoalOverview(userId, tenantId, options.period),
        this.getWorkOverview(userId, tenantId, options.period),
        options.includeStats ? this.getPerformanceMetrics(userId, tenantId, options.period) : null,
        this.getRecommendations(userId, tenantId),
        options.includeComparison ? this.getComparisonData(userId, tenantId) : null
      ]);
      
      summaryData = {
        userProfile,
        skillOverview,
        goalOverview,
        workOverview,
        performanceMetrics,
        recommendations,
        comparisonData,
        lastUpdated: new Date().toISOString()
      };
      
      // キャッシュ保存（10分間）
      await this.cacheService.set(cacheKey, summaryData, 600);
    }
    
    return summaryData;
  }
  
  private async getSkillOverview(userId: string, tenantId: string, period: string) {
    const skills = await this.skillRepository.findByUserId(userId);
    const skillHistory = await this.skillHistoryRepository.findByUserIdAndPeriod(userId, period);
    const certifications = await this.certificationRepository.findByUserId(userId);
    
    const skillsByLevel = skills.reduce((acc, skill) => {
      const levelValue = this.getLevelValue(skill.level);
      acc[skill.level] = (acc[skill.level] || 0) + 1;
      return acc;
    }, {});
    
    const averageLevel = skills.reduce((sum, skill) => sum + this.getLevelValue(skill.level), 0) / skills.length;
    
    const topCategories = this.groupSkillsByCategory(skills).slice(0, 3);
    
    const recentGrowth = this.calculateRecentGrowth(skillHistory, 30);
    
    return {
      totalSkills: skills.length,
      skillLevel: {
        average: Math.round(averageLevel * 10) / 10,
        distribution: skillsByLevel
      },
      topCategories,
      recentGrowth,
      certifications: {
        total: certifications.length,
        active: certifications.filter(c => c.status === 'active').length,
        expiringSoon: certifications.filter(c => this.isExpiringSoon(c.expiryDate)).length,
        recentlyObtained: certifications
          .filter(c => this.isRecentlyObtained(c.obtainedDate, 90))
          .slice(0, 3)
      }
    };
  }
  
  private async getPerformanceMetrics(userId: string, tenantId: string, period: string) {
    const metrics = await this.performanceRepository.findByUserIdAndPeriod(userId, period);
    
    const skillGrowthRate = this.calculateSkillGrowthRate(userId, period);
    const goalAchievementRate = this.calculateGoalAchievementRate(userId, period);
    const learningActivity = await this.getLearningActivity(userId, period);
    const teamContribution = await this.getTeamContribution(userId, period);
    
    return {
      skillGrowthRate,
      goalAchievementRate,
      learningActivity,
      teamContribution
    };
  }
  
  private async getComparisonData(userId: string, tenantId: string) {
    const user = await this.userRepository.findById(userId);
    
    const departmentAverage = await this.calculateDepartmentAverage(user.departmentId);
    const positionAverage = await this.calculatePositionAverage(user.positionId);
    const userRanking = await this.calculateUserRanking(userId, tenantId);
    
    return {
      departmentAverage,
      positionAverage,
      userRanking
    };
  }
  
  private getLevelValue(level: string): number {
    const levelMap = { '×': 1, '△': 2, '○': 3, '◎': 4 };
    return levelMap[level] || 0;
  }
  
  private groupSkillsByCategory(skills: any[]) {
    const categories = skills.reduce((acc, skill) => {
      if (!acc[skill.categoryName]) {
        acc[skill.categoryName] = [];
      }
      acc[skill.categoryName].push(skill);
      return acc;
    }, {});
    
    return Object.entries(categories)
      .map(([categoryName, categorySkills]: [string, any[]]) => ({
