# API仕様書: API-021 スキル情報取得API

## 基本情報

| 項目 | 内容 |
|------|------|
| API ID | API-021 |
| API名称 | スキル情報取得API |
| エンドポイント | /api/skills/{user_id} |
| 概要 | ユーザーのスキル情報取得、階層構造対応 |
| 利用画面 | SCR-SKILL |
| 優先度 | 最高 |
| 実装予定 | Week 2 |

---

## エンドポイント詳細

### 1. ユーザースキル情報取得

#### リクエスト
```http
GET /api/skills/{user_id}
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### パスパラメータ
| パラメータ名 | 型 | 必須 | 説明 |
|-------------|---|------|------|
| user_id | string | ○ | ユーザーID |

#### クエリパラメータ
| パラメータ名 | 型 | 必須 | 説明 | 例 |
|-------------|---|------|------|---|
| category | string | × | スキルカテゴリフィルタ | technical, business, management |
| level | string | × | スキルレベルフィルタ | beginner, intermediate, advanced |
| includeHistory | boolean | × | 履歴情報含有フラグ | true, false |
| format | string | × | レスポンス形式 | flat, hierarchical |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_001",
      "name": "田中太郎",
      "email": "tanaka@company-a.com",
      "department": "開発部",
      "position": "シニアエンジニア",
      "tenantId": "tenant_001"
    },
    "skillSummary": {
      "totalSkills": 45,
      "skillsByCategory": {
        "technical": 25,
        "business": 12,
        "management": 8
      },
      "skillsByLevel": {
        "×": 5,
        "△": 15,
        "○": 20,
        "◎": 5
      },
      "lastUpdated": "2025-05-30T20:55:00Z"
    },
    "skills": {
      "technical": {
        "programming": {
          "categoryId": "tech_prog",
          "categoryName": "プログラミング",
          "subcategories": {
            "languages": {
              "subcategoryId": "tech_prog_lang",
              "subcategoryName": "プログラミング言語",
              "skills": [
                {
                  "skillId": "skill_001",
                  "skillName": "JavaScript",
                  "level": "◎",
                  "levelValue": 4,
                  "experience": "5年以上",
                  "lastUsed": "2025-05-30",
                  "certifications": [
                    {
                      "name": "JavaScript認定試験",
                      "level": "上級",
                      "obtainedDate": "2024-03-15",
                      "expiryDate": null
                    }
                  ],
                  "projects": [
                    {
                      "projectName": "ECサイト構築",
                      "role": "フロントエンド開発",
                      "period": "2024-01-01 to 2024-06-30"
                    }
                  ],
                  "selfAssessment": "フレームワークを含めて高度な開発が可能",
                  "updatedAt": "2025-05-30T20:55:00Z"
                },
                {
                  "skillId": "skill_002",
                  "skillName": "Python",
                  "level": "○",
                  "levelValue": 3,
                  "experience": "2年",
                  "lastUsed": "2025-04-15",
                  "certifications": [],
                  "projects": [
                    {
                      "projectName": "データ分析システム",
                      "role": "バックエンド開発",
                      "period": "2024-07-01 to 2024-12-31"
                    }
                  ],
                  "selfAssessment": "基本的な開発は問題なく実施可能",
                  "updatedAt": "2025-04-20T10:30:00Z"
                }
              ]
            },
            "frameworks": {
              "subcategoryId": "tech_prog_fw",
              "subcategoryName": "フレームワーク",
              "skills": [
                {
                  "skillId": "skill_003",
                  "skillName": "React",
                  "level": "◎",
                  "levelValue": 4,
                  "experience": "3年",
                  "lastUsed": "2025-05-30",
                  "certifications": [],
                  "projects": [
                    {
                      "projectName": "社内管理システム",
                      "role": "フロントエンド設計・開発",
                      "period": "2024-01-01 to 2025-03-31"
                    }
                  ],
                  "selfAssessment": "複雑なSPAの設計・実装が可能",
                  "updatedAt": "2025-05-30T20:55:00Z"
                }
              ]
            }
          }
        },
        "infrastructure": {
          "categoryId": "tech_infra",
          "categoryName": "インフラストラクチャ",
          "subcategories": {
            "cloud": {
              "subcategoryId": "tech_infra_cloud",
              "subcategoryName": "クラウド",
              "skills": [
                {
                  "skillId": "skill_004",
                  "skillName": "AWS",
                  "level": "○",
                  "levelValue": 3,
                  "experience": "1年",
                  "lastUsed": "2025-03-15",
                  "certifications": [
                    {
                      "name": "AWS Solutions Architect Associate",
                      "level": "Associate",
                      "obtainedDate": "2024-09-15",
                      "expiryDate": "2027-09-15"
                    }
                  ],
                  "projects": [
                    {
                      "projectName": "システム移行プロジェクト",
                      "role": "インフラ設計",
                      "period": "2024-06-01 to 2024-11-30"
                    }
                  ],
                  "selfAssessment": "基本的なサービスの構築・運用が可能",
                  "updatedAt": "2025-03-20T14:20:00Z"
                }
              ]
            }
          }
        }
      },
      "business": {
        "communication": {
          "categoryId": "bus_comm",
          "categoryName": "コミュニケーション",
          "subcategories": {
            "presentation": {
              "subcategoryId": "bus_comm_pres",
              "subcategoryName": "プレゼンテーション",
              "skills": [
                {
                  "skillId": "skill_005",
                  "skillName": "技術プレゼンテーション",
                  "level": "○",
                  "levelValue": 3,
                  "experience": "3年",
                  "lastUsed": "2025-05-15",
                  "certifications": [],
                  "projects": [],
                  "selfAssessment": "技術的な内容を分かりやすく説明できる",
                  "updatedAt": "2025-05-20T09:15:00Z"
                }
              ]
            }
          }
        }
      }
    },
    "skillHistory": [
      {
        "skillId": "skill_001",
        "skillName": "JavaScript",
        "changes": [
          {
            "date": "2025-05-30T20:55:00Z",
            "previousLevel": "○",
            "newLevel": "◎",
            "reason": "新プロジェクトでの実績評価",
            "updatedBy": "user_001"
          },
          {
            "date": "2024-12-15T10:30:00Z",
            "previousLevel": "△",
            "newLevel": "○",
            "reason": "フレームワーク習得完了",
            "updatedBy": "user_001"
          }
        ]
      }
    ]
  }
}
```

#### レスポンス（エラー時）
```json
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "指定されたユーザーが見つかりません",
    "details": "ユーザーID: user_999"
  }
}
```

### 2. スキル統計情報取得

#### リクエスト
```http
GET /api/skills/{user_id}/statistics
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "statistics": {
      "skillDistribution": {
        "technical": {
          "total": 25,
          "levels": { "×": 2, "△": 8, "○": 12, "◎": 3 }
        },
        "business": {
          "total": 12,
          "levels": { "×": 1, "△": 4, "○": 6, "◎": 1 }
        },
        "management": {
          "total": 8,
          "levels": { "×": 2, "△": 3, "○": 2, "◎": 1 }
        }
      },
      "skillGrowth": {
        "lastMonth": {
          "improved": 3,
          "maintained": 40,
          "declined": 2
        },
        "lastQuarter": {
          "improved": 8,
          "maintained": 35,
          "declined": 2
        }
      },
      "certifications": {
        "total": 5,
        "active": 4,
        "expiringSoon": 1,
        "expired": 0
      },
      "recommendations": [
        {
          "type": "skill_improvement",
          "skillId": "skill_002",
          "skillName": "Python",
          "suggestion": "上級レベル習得のため、機械学習ライブラリの学習を推奨",
          "priority": "medium"
        },
        {
          "type": "certification",
          "skillId": "skill_004",
          "skillName": "AWS",
          "suggestion": "AWS Professional レベル資格の取得を推奨",
          "priority": "high"
        }
      ]
    }
  }
}
```

---

## エラーコード一覧

| エラーコード | HTTPステータス | 説明 | 対処法 |
|-------------|---------------|------|--------|
| UNAUTHORIZED | 401 | 認証エラー | 有効なJWTトークンを設定 |
| FORBIDDEN | 403 | アクセス権限なし | 自分のスキル情報または管理権限が必要 |
| USER_NOT_FOUND | 404 | ユーザーが見つからない | 正しいユーザーIDを指定 |
| TENANT_MISMATCH | 403 | テナント不一致 | 同一テナント内のユーザーのみアクセス可能 |
| SKILL_DATA_NOT_FOUND | 404 | スキルデータが見つからない | スキル情報が未登録 |
| INVALID_PARAMETER | 400 | パラメータエラー | クエリパラメータを確認 |
| INTERNAL_SERVER_ERROR | 500 | サーバー内部エラー | システム管理者に連絡 |

---

## セキュリティ要件

### 認証・認可
- **認証**: JWT Bearer Token必須
- **権限**: 自分のスキル情報または管理者権限
- **テナント分離**: テナント内ユーザーのみアクセス可能

### データ保護
- **個人情報保護**: スキル情報は個人情報として厳重管理
- **アクセスログ**: 全アクセスを監査ログに記録
- **データ暗号化**: 機密スキル情報はAES-256で暗号化

---

## パフォーマンス要件

| 項目 | 要件 |
|------|------|
| レスポンス時間 | 95%のリクエストが800ms以内 |
| スループット | 200 req/sec |
| データサイズ | 1ユーザーあたり最大2MB |
| キャッシュ | Redis使用、TTL 300秒 |

---

## テスト仕様

### 単体テスト
```typescript
describe('Skill Information API', () => {
  test('GET /api/skills/{user_id} - 正常取得', async () => {
    const response = await request(app)
      .get('/api/skills/user_001')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.user.id).toBe('user_001');
    expect(response.body.data.skills).toBeDefined();
    expect(response.body.data.skillSummary.totalSkills).toBeGreaterThan(0);
  });
  
  test('GET /api/skills/{user_id} - 階層構造確認', async () => {
    const response = await request(app)
      .get('/api/skills/user_001?format=hierarchical')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(200);
    
    expect(response.body.data.skills.technical).toBeDefined();
    expect(response.body.data.skills.technical.programming).toBeDefined();
    expect(response.body.data.skills.technical.programming.subcategories).toBeDefined();
  });
  
  test('GET /api/skills/{user_id} - 権限チェック', async () => {
    const response = await request(app)
      .get('/api/skills/other_user_001')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(403);
    
    expect(response.body.success).toBe(false);
    expect(response.body.error.code).toBe('FORBIDDEN');
  });
});
```

### 統合テスト
```typescript
describe('Skill Information Integration', () => {
  test('スキル情報の完全性確認', async () => {
    // 1. スキル情報取得
    const skillResponse = await getSkillInfo('user_001');
    
    // 2. 統計情報取得
    const statsResponse = await getSkillStatistics('user_001');
    
    // 3. データ整合性確認
    expect(skillResponse.data.skillSummary.totalSkills)
      .toBe(statsResponse.data.statistics.skillDistribution.technical.total +
            statsResponse.data.statistics.skillDistribution.business.total +
            statsResponse.data.statistics.skillDistribution.management.total);
  });
  
  test('テナント分離確認', async () => {
    const tenantAToken = await loginAsUser('company-a');
    const tenantBToken = await loginAsUser('company-b');
    
    // テナントAのユーザーでテナントBのスキル情報にアクセス
    const response = await request(app)
      .get('/api/skills/tenant-b-user')
      .set('Authorization', `Bearer ${tenantAToken}`)
      .expect(403);
    
    expect(response.body.error.code).toBe('TENANT_MISMATCH');
  });
});
```

---

## 実装メモ

### データベーススキーマ
```sql
CREATE TABLE user_skills (
  id VARCHAR(50) PRIMARY KEY,
  user_id VARCHAR(50) NOT NULL,
  skill_id VARCHAR(50) NOT NULL,
  level VARCHAR(10) NOT NULL, -- ×, △, ○, ◎
  level_value INTEGER NOT NULL, -- 1, 2, 3, 4
  experience VARCHAR(100),
  last_used DATE,
  self_assessment TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (skill_id) REFERENCES skill_masters(id),
  UNIQUE(user_id, skill_id)
);

CREATE TABLE skill_history (
  id VARCHAR(50) PRIMARY KEY,
  user_skill_id VARCHAR(50) NOT NULL,
  previous_level VARCHAR(10),
  new_level VARCHAR(10) NOT NULL,
  change_reason TEXT,
  updated_by VARCHAR(50) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_skill_id) REFERENCES user_skills(id),
  FOREIGN KEY (updated_by) REFERENCES users(id)
);

CREATE INDEX idx_user_skills_user_id ON user_skills(user_id);
CREATE INDEX idx_user_skills_skill_id ON user_skills(skill_id);
CREATE INDEX idx_skill_history_user_skill_id ON skill_history(user_skill_id);
```

### Next.js実装例
```typescript
// pages/api/skills/[user_id].ts
import { NextApiRequest, NextApiResponse } from 'next';
import { authenticateToken, checkTenantAccess } from '@/lib/auth';
import { SkillService } from '@/services/SkillService';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ success: false, error: 'Method not allowed' });
  }
  
  try {
    const { user_id } = req.query;
    const { category, level, includeHistory, format } = req.query;
    
    // 認証・認可チェック
    const currentUser = await authenticateToken(req);
    await checkTenantAccess(currentUser, user_id as string);
    
    const skillService = new SkillService();
    
    // スキル情報取得
    const skillData = await skillService.getUserSkills(user_id as string, {
      category: category as string,
      level: level as string,
      includeHistory: includeHistory === 'true',
      format: format as 'flat' | 'hierarchical' || 'hierarchical'
    });
    
    return res.status(200).json({
      success: true,
      data: skillData
    });
    
  } catch (error) {
    console.error('Skill fetch error:', error);
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

### スキルサービス実装例
```typescript
// services/SkillService.ts
export class SkillService {
  async getUserSkills(userId: string, options: SkillQueryOptions) {
    const user = await this.userRepository.findById(userId);
    if (!user) {
      throw new NotFoundError('USER_NOT_FOUND', 'ユーザーが見つかりません');
    }
    
    // スキル情報取得
    const skills = await this.skillRepository.findByUserId(userId, options);
    
    // 階層構造に変換
    const hierarchicalSkills = this.buildSkillHierarchy(skills);
    
    // 統計情報計算
    const skillSummary = this.calculateSkillSummary(skills);
    
    // 履歴情報取得（オプション）
    let skillHistory = [];
    if (options.includeHistory) {
      skillHistory = await this.skillHistoryRepository.findByUserId(userId);
    }
    
    return {
      user: {
        id: user.id,
        name: user.name,
        email: user.email,
        department: user.department,
        position: user.position,
        tenantId: user.tenantId
      },
      skillSummary,
      skills: hierarchicalSkills,
      skillHistory
    };
  }
  
  private buildSkillHierarchy(skills: UserSkill[]) {
    // スキルを階層構造に変換するロジック
    const hierarchy = {};
    
    skills.forEach(skill => {
      const category = skill.category;
      const subcategory = skill.subcategory;
      
      if (!hierarchy[category]) {
        hierarchy[category] = {};
      }
      
      if (!hierarchy[category][subcategory]) {
        hierarchy[category][subcategory] = {
          subcategoryId: skill.subcategoryId,
          subcategoryName: skill.subcategoryName,
          skills: []
        };
      }
      
      hierarchy[category][subcategory].skills.push({
        skillId: skill.id,
        skillName: skill.name,
        level: skill.level,
        levelValue: skill.levelValue,
        experience: skill.experience,
        lastUsed: skill.lastUsed,
        certifications: skill.certifications,
        projects: skill.projects,
        selfAssessment: skill.selfAssessment,
        updatedAt: skill.updatedAt
      });
    });
    
    return hierarchy;
  }
}
```

---

## 変更履歴

| 日付 | バージョン | 変更内容 | 変更者 |
|------|-----------|----------|--------|
| 2025-05-30 | 1.0.0 | 初版作成 | システムアーキテクト |
