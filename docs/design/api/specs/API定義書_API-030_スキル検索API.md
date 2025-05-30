# API定義書: API-030 スキル検索API

## 基本情報

| 項目 | 内容 |
|------|------|
| API ID | API-030 |
| API名称 | スキル検索API |
| エンドポイント | /api/skills/search |
| 概要 | 条件指定によるスキル検索 |
| 利用画面 | SCR-SKILL-SEARCH |
| 優先度 | 高 |
| 実装予定 | Week 3-4 |

---

## エンドポイント詳細

### 1. スキル検索実行

#### リクエスト
```http
POST /api/skills/search
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "searchCriteria": {
    "keywords": ["JavaScript", "React", "TypeScript"],
    "skillLevels": ["○", "◎"],
    "categories": ["プログラミング言語", "フレームワーク"],
    "departments": ["開発部", "QA部"],
    "positions": ["エンジニア", "シニアエンジニア"],
    "experienceYears": {
      "min": 2,
      "max": 10
    },
    "lastUpdated": {
      "from": "2025-01-01",
      "to": "2025-05-30"
    },
    "certifications": ["AWS Solutions Architect", "Google Cloud Professional"],
    "projectExperience": ["ECサイト", "API開発"],
    "availabilityStatus": "available"
  },
  "searchOptions": {
    "searchMode": "and",
    "includeInactiveUsers": false,
    "includeTeamMembers": true,
    "sortBy": "skillLevel",
    "sortOrder": "desc",
    "groupBy": "department"
  },
  "pagination": {
    "page": 1,
    "limit": 20
  }
}
```

#### バリデーションルール
| フィールド | ルール |
|-----------|--------|
| keywords | 任意、配列、最大10件 |
| skillLevels | 任意、配列、×/△/○/◎ |
| categories | 任意、配列、有効なカテゴリ名 |
| departments | 任意、配列、有効な部署名 |
| positions | 任意、配列、有効な役職名 |
| experienceYears.min | 任意、数値、0以上 |
| experienceYears.max | 任意、数値、min以上 |
| searchMode | 任意、and/or |
| page | 任意、数値、1以上 |
| limit | 任意、数値、1-100 |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "searchResults": [
      {
        "userId": "user_001",
        "userInfo": {
          "displayName": "田中太郎",
          "email": "tanaka@company-a.com",
          "employeeId": "EMP001",
          "avatarUrl": "https://storage.example.com/avatars/user_001.jpg",
          "department": "開発部",
          "position": "シニアエンジニア",
          "experienceYears": 5.2,
          "availabilityStatus": "available",
          "lastLoginAt": "2025-05-30T21:00:00Z"
        },
        "matchedSkills": [
          {
            "skillId": "skill_001",
            "skillName": "JavaScript",
            "level": "◎",
            "categoryName": "プログラミング言語",
            "lastUpdated": "2025-05-28T14:30:00Z",
            "experienceMonths": 60,
            "projectCount": 15,
            "matchScore": 95.5
          },
          {
            "skillId": "skill_003",
            "skillName": "React",
            "level": "◎",
            "categoryName": "フレームワーク",
            "lastUpdated": "2025-05-25T10:15:00Z",
            "experienceMonths": 36,
            "projectCount": 8,
            "matchScore": 92.3
          },
          {
            "skillId": "skill_015",
            "skillName": "TypeScript",
            "level": "○",
            "categoryName": "プログラミング言語",
            "lastUpdated": "2025-05-20T16:45:00Z",
            "experienceMonths": 24,
            "projectCount": 5,
            "matchScore": 88.7
          }
        ],
        "skillSummary": {
          "totalMatchedSkills": 3,
          "averageLevel": 3.3,
          "averageMatchScore": 92.2,
          "strongestCategory": "プログラミング言語",
          "recentActivity": "高"
        },
        "certifications": [
          {
            "certificationName": "AWS Solutions Architect Associate",
            "obtainedDate": "2024-03-15",
            "expiryDate": "2027-03-15",
            "status": "active"
          }
        ],
        "projectExperience": [
          {
            "projectName": "ECサイトリニューアル",
            "role": "フロントエンドリード",
            "period": "2025-04-01 - 2025-07-31",
            "usedSkills": ["JavaScript", "React", "TypeScript"]
          }
        ],
        "overallMatchScore": 91.8,
        "recommendationReason": "JavaScript、Reactで高いスキルレベルを持ち、実プロジェクト経験も豊富"
      },
      {
        "userId": "user_002",
        "userInfo": {
          "displayName": "佐藤花子",
          "email": "sato@company-a.com",
          "employeeId": "EMP002",
          "avatarUrl": "https://storage.example.com/avatars/user_002.jpg",
          "department": "開発部",
          "position": "エンジニア",
          "experienceYears": 3.1,
          "availabilityStatus": "available",
          "lastLoginAt": "2025-05-30T18:30:00Z"
        },
        "matchedSkills": [
          {
            "skillId": "skill_001",
            "skillName": "JavaScript",
            "level": "○",
            "categoryName": "プログラミング言語",
            "lastUpdated": "2025-05-22T11:20:00Z",
            "experienceMonths": 30,
            "projectCount": 8,
            "matchScore": 82.4
          },
          {
            "skillId": "skill_015",
            "skillName": "TypeScript",
            "level": "△",
            "categoryName": "プログラミング言語",
            "lastUpdated": "2025-05-18T09:30:00Z",
            "experienceMonths": 12,
            "projectCount": 3,
            "matchScore": 65.8
          }
        ],
        "skillSummary": {
          "totalMatchedSkills": 2,
          "averageLevel": 2.5,
          "averageMatchScore": 74.1,
          "strongestCategory": "プログラミング言語",
          "recentActivity": "中"
        },
        "certifications": [],
        "projectExperience": [
          {
            "projectName": "社内システム改修",
            "role": "バックエンドエンジニア",
            "period": "2025-02-01 - 2025-05-31",
            "usedSkills": ["JavaScript", "Node.js"]
          }
        ],
        "overallMatchScore": 74.1,
        "recommendationReason": "JavaScriptの実務経験があり、TypeScriptも学習中"
      }
    ],
    "searchSummary": {
      "totalResults": 25,
      "matchedUsers": 2,
      "searchCriteria": {
        "keywords": ["JavaScript", "React", "TypeScript"],
        "skillLevels": ["○", "◎"],
        "searchMode": "and"
      },
      "averageMatchScore": 82.95,
      "topMatchScore": 91.8,
      "resultsByDepartment": {
        "開発部": 20,
        "QA部": 3,
        "インフラ部": 2
      },
      "resultsBySkillLevel": {
        "◎": 8,
        "○": 12,
        "△": 5
      },
      "searchExecutedAt": "2025-05-30T21:15:00Z",
      "searchDuration": "0.245s"
    },
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 25,
      "totalPages": 2,
      "hasNext": true,
      "hasPrev": false
    },
    "suggestions": {
      "relatedSkills": ["Vue.js", "Angular", "Node.js"],
      "alternativeKeywords": ["フロントエンド", "Webアプリケーション"],
      "recommendedFilters": {
        "experienceYears": { "min": 2, "max": 8 },
        "departments": ["開発部", "フロントエンド部"]
      }
    }
  }
}
```

### 2. 保存済み検索条件取得

#### リクエスト
```http
GET /api/skills/search/saved
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "savedSearches": [
      {
        "id": "search_001",
        "name": "React開発者検索",
        "description": "React経験者の検索条件",
        "searchCriteria": {
          "keywords": ["React", "JavaScript"],
          "skillLevels": ["○", "◎"],
          "categories": ["フレームワーク"]
        },
        "createdAt": "2025-05-25T10:00:00Z",
        "lastUsed": "2025-05-30T15:30:00Z",
        "useCount": 12
      },
      {
        "id": "search_002",
        "name": "AWS専門家検索",
        "description": "AWS関連スキル保有者",
        "searchCriteria": {
          "keywords": ["AWS"],
          "certifications": ["AWS Solutions Architect"],
          "skillLevels": ["○", "◎"]
        },
        "createdAt": "2025-05-20T14:20:00Z",
        "lastUsed": "2025-05-29T11:45:00Z",
        "useCount": 8
      }
    ],
    "totalCount": 2
  }
}
```

### 3. 検索条件保存

#### リクエスト
```http
POST /api/skills/search/save
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "name": "フルスタック開発者検索",
  "description": "フロントエンド・バックエンド両方のスキルを持つ開発者",
  "searchCriteria": {
    "keywords": ["JavaScript", "React", "Node.js", "PostgreSQL"],
    "skillLevels": ["○", "◎"],
    "categories": ["プログラミング言語", "フレームワーク", "データベース"],
    "experienceYears": { "min": 3, "max": 10 }
  },
  "isPublic": false
}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "savedSearch": {
      "id": "search_003",
      "name": "フルスタック開発者検索",
      "description": "フロントエンド・バックエンド両方のスキルを持つ開発者",
      "searchCriteria": {
        "keywords": ["JavaScript", "React", "Node.js", "PostgreSQL"],
        "skillLevels": ["○", "◎"],
        "categories": ["プログラミング言語", "フレームワーク", "データベース"],
        "experienceYears": { "min": 3, "max": 10 }
      },
      "isPublic": false,
      "createdBy": "user_001",
      "createdAt": "2025-05-30T21:20:00Z"
    }
  }
}
```

### 4. スキル統計取得

#### リクエスト
```http
GET /api/skills/search/statistics
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### クエリパラメータ
| パラメータ名 | 型 | 必須 | 説明 | 例 |
|-------------|---|------|------|---|
| department | string | × | 部署フィルタ | 開発部 |
| period | string | × | 期間指定 | last_quarter, current_year |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "skillStatistics": {
      "totalUsers": 150,
      "totalSkills": 1250,
      "averageSkillsPerUser": 8.3,
      "skillDistribution": {
        "×": { "count": 450, "percentage": 36.0 },
        "△": { "count": 400, "percentage": 32.0 },
        "○": { "count": 300, "percentage": 24.0 },
        "◎": { "count": 100, "percentage": 8.0 }
      },
      "topSkills": [
        {
          "skillName": "JavaScript",
          "userCount": 85,
          "averageLevel": 2.8,
          "trend": "increasing"
        },
        {
          "skillName": "Python",
          "userCount": 72,
          "averageLevel": 2.5,
          "trend": "stable"
        },
        {
          "skillName": "AWS",
          "userCount": 68,
          "averageLevel": 2.3,
          "trend": "increasing"
        }
      ],
      "categoryDistribution": {
        "プログラミング言語": { "count": 420, "percentage": 33.6 },
        "フレームワーク": { "count": 280, "percentage": 22.4 },
        "データベース": { "count": 180, "percentage": 14.4 },
        "クラウド": { "count": 150, "percentage": 12.0 },
        "その他": { "count": 220, "percentage": 17.6 }
      },
      "departmentComparison": [
        {
          "department": "開発部",
          "userCount": 80,
          "averageSkillCount": 12.5,
          "topSkills": ["JavaScript", "React", "AWS"]
        },
        {
          "department": "QA部",
          "userCount": 25,
          "averageSkillCount": 6.8,
          "topSkills": ["テスト自動化", "Selenium", "Python"]
        }
      ],
      "skillGaps": [
        {
          "skillName": "Kubernetes",
          "currentUsers": 15,
          "targetUsers": 40,
          "gap": 25,
          "priority": "high"
        },
        {
          "skillName": "GraphQL",
          "currentUsers": 8,
          "targetUsers": 25,
          "gap": 17,
          "priority": "medium"
        }
      ],
      "generatedAt": "2025-05-30T21:25:00Z"
    }
  }
}
```

---

## エラーコード一覧

| エラーコード | HTTPステータス | 説明 | 対処法 |
|-------------|---------------|------|--------|
| UNAUTHORIZED | 401 | 認証エラー | 有効なJWTトークンを設定 |
| FORBIDDEN | 403 | アクセス権限なし | スキル検索権限が必要 |
| VALIDATION_ERROR | 400 | バリデーションエラー | 検索条件を確認 |
| INVALID_SEARCH_CRITERIA | 400 | 無効な検索条件 | 検索条件の形式を確認 |
| SEARCH_TIMEOUT | 408 | 検索タイムアウト | 検索条件を絞り込み |
| TOO_MANY_RESULTS | 400 | 結果数上限超過 | より具体的な検索条件を指定 |
| SAVED_SEARCH_NOT_FOUND | 404 | 保存済み検索が見つからない | 正しい検索IDを指定 |
| SAVED_SEARCH_LIMIT_EXCEEDED | 400 | 保存検索数上限超過 | 不要な保存検索を削除 |
| TENANT_MISMATCH | 403 | テナント不一致 | 同一テナント内のデータのみ検索可能 |
| INTERNAL_SERVER_ERROR | 500 | サーバー内部エラー | システム管理者に連絡 |

---

## セキュリティ要件

### 認証・認可
- **認証**: JWT Bearer Token必須
- **権限**: スキル検索権限（skill:search）
- **テナント分離**: テナント内データのみ検索可能

### データ保護
- **個人情報保護**: 権限に応じたデータフィルタリング
- **検索ログ**: 検索履歴の記録と監査
- **結果制限**: 大量データ取得の防止

---

## パフォーマンス要件

| 項目 | 要件 |
|------|------|
| レスポンス時間 | 95%のリクエストが3秒以内 |
| スループット | 50 req/sec |
| 検索結果 | 最大1000件 |
| 同時検索 | 100セッション |

---

## テスト仕様

### 単体テスト
```typescript
describe('Skill Search API', () => {
  test('POST /api/skills/search - 基本検索', async () => {
    const searchData = {
      searchCriteria: {
        keywords: ['JavaScript', 'React'],
        skillLevels: ['○', '◎']
      },
      pagination: { page: 1, limit: 10 }
    };
    
    const response = await request(app)
      .post('/api/skills/search')
      .set('Authorization', `Bearer ${userToken}`)
      .send(searchData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.searchResults).toBeInstanceOf(Array);
    expect(response.body.data.searchSummary).toBeDefined();
    expect(response.body.data.pagination).toBeDefined();
  });
  
  test('POST /api/skills/search - 複合条件検索', async () => {
    const complexSearch = {
      searchCriteria: {
        keywords: ['AWS'],
        departments: ['開発部'],
        experienceYears: { min: 3, max: 8 },
        certifications: ['AWS Solutions Architect']
      },
      searchOptions: {
        searchMode: 'and',
        sortBy: 'skillLevel',
        sortOrder: 'desc'
      }
    };
    
    const response = await request(app)
      .post('/api/skills/search')
      .set('Authorization', `Bearer ${userToken}`)
      .send(complexSearch)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.searchResults.length).toBeGreaterThan(0);
    
    // ソート確認
    const results = response.body.data.searchResults;
    for (let i = 0; i < results.length - 1; i++) {
      expect(results[i].overallMatchScore).toBeGreaterThanOrEqual(results[i + 1].overallMatchScore);
    }
  });
  
  test('GET /api/skills/search/saved - 保存済み検索取得', async () => {
    const response = await request(app)
      .get('/api/skills/search/saved')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.savedSearches).toBeInstanceOf(Array);
  });
  
  test('POST /api/skills/search/save - 検索条件保存', async () => {
    const saveData = {
      name: 'テスト検索',
      description: 'テスト用の検索条件',
      searchCriteria: {
        keywords: ['Test'],
        skillLevels: ['○']
      }
    };
    
    const response = await request(app)
      .post('/api/skills/search/save')
      .set('Authorization', `Bearer ${userToken}`)
      .send(saveData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.savedSearch.id).toBeDefined();
    expect(response.body.data.savedSearch.name).toBe('テスト検索');
  });
  
  test('GET /api/skills/search/statistics - スキル統計取得', async () => {
    const response = await request(app)
      .get('/api/skills/search/statistics')
      .set('Authorization', `Bearer ${managerToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.skillStatistics).toBeDefined();
    expect(response.body.data.skillStatistics.totalUsers).toBeGreaterThan(0);
    expect(response.body.data.skillStatistics.topSkills).toBeInstanceOf(Array);
  });
});
```

### 統合テスト
```typescript
describe('Skill Search Integration', () => {
  test('検索結果の精度確認', async () => {
    // 1. 特定スキルを持つユーザーを作成
    await createTestUser({
      skills: [
        { name: 'JavaScript', level: '◎' },
        { name: 'React', level: '○' }
      ]
    });
    
    // 2. 検索実行
    const searchResponse = await searchSkills({
      keywords: ['JavaScript', 'React'],
      skillLevels: ['○', '◎'],
      searchMode: 'and'
    });
    
    // 3. 結果確認
    expect(searchResponse.data.searchResults.length).toBeGreaterThan(0);
    const firstResult = searchResponse.data.searchResults[0];
    expect(firstResult.matchedSkills.some(s => s.skillName === 'JavaScript')).toBe(true);
    expect(firstResult.matchedSkills.some(s => s.skillName === 'React')).toBe(true);
  });
  
  test('権限制御確認', async () => {
    // 一般ユーザーで他部署検索
    const response = await request(app)
      .post('/api/skills/search')
      .set('Authorization', `Bearer ${userToken}`)
      .send({
        searchCriteria: { departments: ['機密部署'] }
      })
      .expect(200);
    
    // 権限外部署の結果が含まれないことを確認
    expect(response.body.data.searchResults.every(r => 
      r.userInfo.department !== '機密部署'
    )).toBe(true);
  });
  
  test('パフォーマンス確認', async () => {
    const startTime = Date.now();
    
    const response = await searchSkills({
      keywords: ['JavaScript'],
      pagination: { page: 1, limit: 100 }
    });
    
    const endTime = Date.now();
    const duration = endTime - startTime;
    
    expect(duration).toBeLessThan(3000); // 3秒以内
    expect(response.data.searchSummary.searchDuration).toBeDefined();
  });
});
```

---

## 実装メモ

### データベーススキーマ
```sql
CREATE TABLE skill_search_logs (
  id VARCHAR(50) PRIMARY KEY,
  user_id VARCHAR(50) NOT NULL,
  tenant_id VARCHAR(50) NOT NULL,
  search_criteria JSONB NOT NULL,
  result_count INTEGER NOT NULL,
  search_duration DECIMAL(10,3) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

CREATE TABLE saved_skill_searches (
  id VARCHAR(50) PRIMARY KEY,
  user_id VARCHAR(50) NOT NULL,
  tenant_id VARCHAR(50) NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  search_criteria JSONB NOT NULL,
  is_public BOOLEAN DEFAULT FALSE,
  use_count INTEGER DEFAULT 0,
  last_used_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

CREATE INDEX idx_skill_search_logs_user_id ON skill_search_logs(user_id);
CREATE INDEX idx_skill_search_logs_created_at ON skill_search_logs(created_at);
CREATE INDEX idx_saved_skill_searches_user_id ON saved_skill_searches(user_id);
CREATE INDEX idx_saved_skill_searches_is_public ON saved_skill_searches(is_public);

-- 検索用インデックス
CREATE INDEX idx_user_skills_search ON user_skills(skill_name, skill_level, tenant_id);
CREATE INDEX idx_users_department_position ON users(department_id, position_id, tenant_id);
```

### Next.js実装例
```typescript
// pages/api/skills/search/index.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { authenticateToken, requirePermission } from '@/lib/auth';
import { SkillSearchService } from '@/services/SkillSearchService';
import { validateSearchRequest } from '@/lib/validation';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const user = await authenticateToken(req);
    await requirePermission(user, 'skill:search');
    
    const skillSearchService = new SkillSearchService();
    
    switch (req.method) {
      case 'POST':
        // バリデーション
        const validationResult = validateSearchRequest(req.body);
        if (!validationResult.isValid) {
          return res.status(400).json({
            success: false,
            error: { code: 'VALIDATION_ERROR', message: validationResult.errors }
          });
        }
        
        // 検索実行
        const searchResult = await skillSearchService.searchSkills(
          user.tenantId,
          user.id,
          req.body
        );
        
        return res.status(200).json({ success: true, data: searchResult });
        
      default:
        return res.status(405).json({ success: false, error: 'Method not allowed' });
    }
  } catch (error) {
    console.error('Skill search error:', error);
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

### スキル検索サービス実装例
```typescript
// services/SkillSearchService.ts
export class SkillSearchService {
  async searchSkills(tenantId: string, userId: string, searchRequest: any) {
    const startTime = Date.now();
    
    try {
      // 1. 検索クエリ構築
      const query = this.buildSearchQuery(tenantId, searchRequest.searchCriteria);
      
      // 2. 権限フィルタ適用
      const filteredQuery = await this.applyPermissionFilter(query, userId, tenantId);
      
      // 3. 検索実行
      const searchResults = await this.executeSearch(filteredQuery, searchRequest.searchOptions);
      
      // 4. マッチスコア計算
      const scoredResults = await this.calculateMatchScores(searchResults, searchRequest.searchCriteria);
      
      // 5. ソート・ページング
      const paginatedResults = this.applyPaginationAndSort(
        scoredResults,
        searchRequest.pagination,
        searchRequest.searchOptions
      );
      
      // 6. 検索ログ記録
      await this.logSearch(userId, tenantId, searchRequest, paginatedResults.length, Date.now() - startTime);
      
      // 7. レスポンス構築
      return {
        searchResults: paginatedResults.results,
        searchSummary: this.buildSearchSummary(searchRequest, paginatedResults, startTime),
        pagination: paginatedResults.pagination,
        suggestions: await this.generateSuggestions(searchRequest.searchCriteria)
      };
      
    } catch (error) {
      await this.logSearchError(userId, tenantId, searchRequest, error);
      throw error;
    }
  }
  
  private buildSearchQuery(tenantId: string, criteria: any) {
    let query = this.userRepository.createQueryBuilder('user')
      .leftJoinAndSelect('user.skills', 'skill')
      .leftJoinAndSelect('user.certifications', 'cert')
      .leftJoinAndSelect('user.projectExperiences', 'project')
      .where('user.tenantId = :tenantId', { tenantId });
    
    // キーワード検索
    if (criteria.keywords?.length > 0) {
