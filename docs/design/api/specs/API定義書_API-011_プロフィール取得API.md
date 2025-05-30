# API定義書: API-011 プロフィール取得API

## 基本情報

| 項目 | 内容 |
|------|------|
| API ID | API-011 |
| API名称 | プロフィール取得API |
| エンドポイント | /api/profiles/{user_id} |
| 概要 | ユーザープロフィール情報取得 |
| 利用画面 | SCR-PROFILE |
| 優先度 | 最高 |
| 実装予定 | Week 1-2 |

---

## エンドポイント詳細

### 1. ユーザープロフィール取得

#### リクエスト
```http
GET /api/profiles/{user_id}
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
| includeHistory | boolean | × | 更新履歴含有フラグ | true, false |
| includeSkillSummary | boolean | × | スキルサマリー含有フラグ | true, false |
| includeGoalSummary | boolean | × | 目標サマリー含有フラグ | true, false |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "profile": {
      "id": "user_001",
      "email": "tanaka@company-a.com",
      "employeeId": "EMP001",
      "personalInfo": {
        "lastName": "田中",
        "firstName": "太郎",
        "lastNameKana": "タナカ",
        "firstNameKana": "タロウ",
        "displayName": "田中太郎",
        "phoneNumber": "090-1234-5678",
        "emergencyContact": {
          "name": "田中花子",
          "relationship": "配偶者",
          "phoneNumber": "090-8765-4321"
        }
      },
      "organizationInfo": {
        "tenantId": "tenant_001",
        "tenantName": "株式会社A",
        "departmentId": "dept_001",
        "departmentName": "開発部",
        "divisionId": "div_001",
        "divisionName": "システム開発課",
        "positionId": "pos_001",
        "positionName": "シニアエンジニア",
        "employmentType": "正社員",
        "hireDate": "2020-04-01",
        "managerUserId": "user_manager_001",
        "managerName": "佐藤部長"
      },
      "workInfo": {
        "workLocation": "東京本社",
        "workStyle": "hybrid",
        "contractHours": 8.0,
        "overtimeAllowed": true,
        "remoteWorkAllowed": true,
        "flexTimeAllowed": true
      },
      "systemInfo": {
        "status": "active",
        "role": "user",
        "permissions": [
          "profile:read",
          "profile:write",
          "skills:read",
          "skills:write",
          "goals:read",
          "goals:write"
        ],
        "lastLoginAt": "2025-05-30T20:57:00Z",
        "createdAt": "2020-04-01T09:00:00Z",
        "updatedAt": "2025-05-30T15:30:00Z"
      },
      "preferences": {
        "language": "ja",
        "timezone": "Asia/Tokyo",
        "dateFormat": "YYYY-MM-DD",
        "notifications": {
          "email": true,
          "inApp": true,
          "skillExpiry": true,
          "goalReminder": true
        },
        "privacy": {
          "profileVisibility": "team",
          "skillVisibility": "department",
          "goalVisibility": "manager"
        }
      }
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
      "certifications": {
        "total": 5,
        "active": 4,
        "expiringSoon": 1
      },
      "lastUpdated": "2025-05-30T20:55:00Z"
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
          "daysRemaining": 93
        }
      ],
      "lastUpdated": "2025-05-25T14:20:00Z"
    },
    "updateHistory": [
      {
        "id": "hist_001",
        "fieldName": "organizationInfo.positionName",
        "previousValue": "エンジニア",
        "newValue": "シニアエンジニア",
        "changeReason": "昇進",
        "updatedBy": "user_manager_001",
        "updatedByName": "佐藤部長",
        "updatedAt": "2025-05-30T15:30:00Z",
        "approvedBy": "user_hr_001",
        "approvedByName": "人事部",
        "approvedAt": "2025-05-30T16:00:00Z"
      },
      {
        "id": "hist_002",
        "fieldName": "personalInfo.phoneNumber",
        "previousValue": "090-1111-2222",
        "newValue": "090-1234-5678",
        "changeReason": "個人情報更新",
        "updatedBy": "user_001",
        "updatedByName": "田中太郎",
        "updatedAt": "2025-05-15T10:15:00Z",
        "approvedBy": null,
        "approvedByName": null,
        "approvedAt": null
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

### 2. 自分のプロフィール取得

#### リクエスト
```http
GET /api/profiles/me
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "profile": {
      "id": "user_001",
      "email": "tanaka@company-a.com",
      "employeeId": "EMP001",
      "personalInfo": {
        "lastName": "田中",
        "firstName": "太郎",
        "lastNameKana": "タナカ",
        "firstNameKana": "タロウ",
        "displayName": "田中太郎",
        "phoneNumber": "090-1234-5678",
        "emergencyContact": {
          "name": "田中花子",
          "relationship": "配偶者",
          "phoneNumber": "090-8765-4321"
        }
      },
      "organizationInfo": {
        "tenantId": "tenant_001",
        "tenantName": "株式会社A",
        "departmentId": "dept_001",
        "departmentName": "開発部",
        "divisionId": "div_001",
        "divisionName": "システム開発課",
        "positionId": "pos_001",
        "positionName": "シニアエンジニア",
        "employmentType": "正社員",
        "hireDate": "2020-04-01",
        "managerUserId": "user_manager_001",
        "managerName": "佐藤部長"
      },
      "workInfo": {
        "workLocation": "東京本社",
        "workStyle": "hybrid",
        "contractHours": 8.0,
        "overtimeAllowed": true,
        "remoteWorkAllowed": true,
        "flexTimeAllowed": true
      },
      "systemInfo": {
        "status": "active",
        "role": "user",
        "permissions": [
          "profile:read",
          "profile:write",
          "skills:read",
          "skills:write",
          "goals:read",
          "goals:write"
        ],
        "lastLoginAt": "2025-05-30T20:57:00Z",
        "createdAt": "2020-04-01T09:00:00Z",
        "updatedAt": "2025-05-30T15:30:00Z"
      },
      "preferences": {
        "language": "ja",
        "timezone": "Asia/Tokyo",
        "dateFormat": "YYYY-MM-DD",
        "notifications": {
          "email": true,
          "inApp": true,
          "skillExpiry": true,
          "goalReminder": true
        },
        "privacy": {
          "profileVisibility": "team",
          "skillVisibility": "department",
          "goalVisibility": "manager"
        }
      }
    }
  }
}
```

### 3. プロフィール検索

#### リクエスト
```http
GET /api/profiles/search
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### クエリパラメータ
| パラメータ名 | 型 | 必須 | 説明 | 例 |
|-------------|---|------|------|---|
| q | string | × | 検索キーワード | 田中 |
| department | string | × | 部署フィルタ | 開発部 |
| position | string | × | 役職フィルタ | エンジニア |
| skill | string | × | スキルフィルタ | JavaScript |
| page | number | × | ページ番号（デフォルト: 1） | 1 |
| limit | number | × | 取得件数（デフォルト: 20） | 20 |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "profiles": [
      {
        "id": "user_001",
        "displayName": "田中太郎",
        "email": "tanaka@company-a.com",
        "departmentName": "開発部",
        "positionName": "シニアエンジニア",
        "topSkills": [
          "JavaScript",
          "React",
          "AWS"
        ],
        "skillCount": 45,
        "lastLoginAt": "2025-05-30T20:57:00Z"
      },
      {
        "id": "user_002",
        "displayName": "佐藤花子",
        "email": "sato@company-a.com",
        "departmentName": "開発部",
        "positionName": "エンジニア",
        "topSkills": [
          "Python",
          "Django",
          "PostgreSQL"
        ],
        "skillCount": 32,
        "lastLoginAt": "2025-05-30T18:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 45,
      "totalPages": 3
    },
    "filters": {
      "departments": [
        { "id": "dept_001", "name": "開発部", "count": 25 },
        { "id": "dept_002", "name": "営業部", "count": 15 },
        { "id": "dept_003", "name": "人事部", "count": 5 }
      ],
      "positions": [
        { "id": "pos_001", "name": "エンジニア", "count": 20 },
        { "id": "pos_002", "name": "シニアエンジニア", "count": 8 },
        { "id": "pos_003", "name": "マネージャー", "count": 5 }
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
| FORBIDDEN | 403 | アクセス権限なし | 自分のプロフィールまたは管理権限が必要 |
| USER_NOT_FOUND | 404 | ユーザーが見つからない | 正しいユーザーIDを指定 |
| TENANT_MISMATCH | 403 | テナント不一致 | 同一テナント内のユーザーのみアクセス可能 |
| PROFILE_NOT_FOUND | 404 | プロフィールが見つからない | プロフィール情報が未登録 |
| INVALID_PARAMETER | 400 | パラメータエラー | クエリパラメータを確認 |
| PRIVACY_RESTRICTION | 403 | プライバシー制限 | ユーザーのプライバシー設定により閲覧不可 |
| INTERNAL_SERVER_ERROR | 500 | サーバー内部エラー | システム管理者に連絡 |

---

## セキュリティ要件

### 認証・認可
- **認証**: JWT Bearer Token必須
- **権限**: 自分のプロフィールまたは管理者権限
- **テナント分離**: テナント内ユーザーのみアクセス可能

### プライバシー保護
- **可視性制御**: ユーザーのプライバシー設定に基づく情報制限
- **個人情報保護**: 機密情報は権限に応じて表示制御
- **アクセスログ**: 全アクセスを監査ログに記録

---

## パフォーマンス要件

| 項目 | 要件 |
|------|------|
| レスポンス時間 | 95%のリクエストが500ms以内 |
| スループット | 300 req/sec |
| データサイズ | 1プロフィールあたり最大1MB |
| キャッシュ | Redis使用、TTL 600秒 |

---

## テスト仕様

### 単体テスト
```typescript
describe('Profile API', () => {
  test('GET /api/profiles/{user_id} - 正常取得', async () => {
    const response = await request(app)
      .get('/api/profiles/user_001')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.profile.id).toBe('user_001');
    expect(response.body.data.profile.personalInfo).toBeDefined();
    expect(response.body.data.profile.organizationInfo).toBeDefined();
  });
  
  test('GET /api/profiles/me - 自分のプロフィール取得', async () => {
    const response = await request(app)
      .get('/api/profiles/me')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.profile.email).toBe('tanaka@company-a.com');
  });
  
  test('GET /api/profiles/search - プロフィール検索', async () => {
    const response = await request(app)
      .get('/api/profiles/search?q=田中&department=開発部')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.profiles).toBeInstanceOf(Array);
    expect(response.body.data.pagination).toBeDefined();
  });
  
  test('GET /api/profiles/{user_id} - 権限チェック', async () => {
    const response = await request(app)
      .get('/api/profiles/other_user_001')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(403);
    
    expect(response.body.success).toBe(false);
    expect(response.body.error.code).toBe('FORBIDDEN');
  });
});
```

### 統合テスト
```typescript
describe('Profile Integration', () => {
  test('プロフィール情報の完全性確認', async () => {
    // 1. プロフィール取得
    const profileResponse = await getProfile('user_001');
    
    // 2. スキルサマリー確認
    expect(profileResponse.data.skillSummary).toBeDefined();
    expect(profileResponse.data.skillSummary.totalSkills).toBeGreaterThan(0);
    
    // 3. 目標サマリー確認
    expect(profileResponse.data.goalSummary).toBeDefined();
    expect(profileResponse.data.goalSummary.currentGoals).toBeGreaterThanOrEqual(0);
  });
  
  test('プライバシー設定確認', async () => {
    // 1. プライバシー設定を制限に変更
    await updatePrivacySettings('user_001', { profileVisibility: 'private' });
    
    // 2. 他のユーザーからアクセス
    const response = await request(app)
      .get('/api/profiles/user_001')
      .set('Authorization', `Bearer ${otherUserToken}`)
      .expect(403);
    
    expect(response.body.error.code).toBe('PRIVACY_RESTRICTION');
  });
  
  test('テナント分離確認', async () => {
    const tenantAToken = await loginAsUser('company-a');
    const tenantBToken = await loginAsUser('company-b');
    
    // テナントAのユーザーでテナントBのプロフィールにアクセス
    const response = await request(app)
      .get('/api/profiles/tenant-b-user')
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
CREATE TABLE user_profiles (
  id VARCHAR(50) PRIMARY KEY,
  user_id VARCHAR(50) NOT NULL,
  employee_id VARCHAR(50) UNIQUE NOT NULL,
  personal_info JSONB NOT NULL,
  organization_info JSONB NOT NULL,
  work_info JSONB,
  preferences JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  UNIQUE(user_id)
);

CREATE TABLE profile_update_history (
  id VARCHAR(50) PRIMARY KEY,
  user_id VARCHAR(50) NOT NULL,
  field_name VARCHAR(100) NOT NULL,
  previous_value TEXT,
  new_value TEXT,
  change_reason TEXT,
  updated_by VARCHAR(50) NOT NULL,
  approved_by VARCHAR(50),
  approved_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (updated_by) REFERENCES users(id),
  FOREIGN KEY (approved_by) REFERENCES users(id)
);

CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_employee_id ON user_profiles(employee_id);
CREATE INDEX idx_profile_update_history_user_id ON profile_update_history(user_id);
CREATE INDEX idx_profile_update_history_updated_by ON profile_update_history(updated_by);
```

### Next.js実装例
```typescript
// pages/api/profiles/[user_id].ts
import { NextApiRequest, NextApiResponse } from 'next';
import { authenticateToken, checkProfileAccess } from '@/lib/auth';
import { ProfileService } from '@/services/ProfileService';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ success: false, error: 'Method not allowed' });
  }
  
  try {
    const { user_id } = req.query;
    const { includeHistory, includeSkillSummary, includeGoalSummary } = req.query;
    
    // 認証・認可チェック
    const currentUser = await authenticateToken(req);
    await checkProfileAccess(currentUser, user_id as string);
    
    const profileService = new ProfileService();
    
    // プロフィール情報取得
    const profileData = await profileService.getProfile(user_id as string, {
      includeHistory: includeHistory === 'true',
      includeSkillSummary: includeSkillSummary === 'true',
      includeGoalSummary: includeGoalSummary === 'true',
      requesterId: currentUser.id
    });
    
    return res.status(200).json({
      success: true,
      data: profileData
    });
    
  } catch (error) {
    console.error('Profile fetch error:', error);
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

### プロフィールサービス実装例
```typescript
// services/ProfileService.ts
export class ProfileService {
  async getProfile(userId: string, options: ProfileQueryOptions) {
    const user = await this.userRepository.findById(userId);
    if (!user) {
      throw new NotFoundError('USER_NOT_FOUND', 'ユーザーが見つかりません');
    }
    
    // プロフィール情報取得
    const profile = await this.profileRepository.findByUserId(userId);
    if (!profile) {
      throw new NotFoundError('PROFILE_NOT_FOUND', 'プロフィールが見つかりません');
    }
    
    // プライバシー設定チェック
    const filteredProfile = await this.applyPrivacyFilter(profile, options.requesterId);
    
    // 追加情報取得
    let skillSummary = null;
    let goalSummary = null;
    let updateHistory = null;
    
    if (options.includeSkillSummary) {
      skillSummary = await this.skillService.getSkillSummary(userId);
    }
    
    if (options.includeGoalSummary) {
      goalSummary = await this.goalService.getGoalSummary(userId);
    }
    
    if (options.includeHistory) {
      updateHistory = await this.profileHistoryRepository.findByUserId(userId);
    }
    
    return {
      profile: filteredProfile,
      skillSummary,
      goalSummary,
      updateHistory
    };
  }
  
  private async applyPrivacyFilter(profile: any, requesterId: string) {
    const privacySettings = profile.preferences?.privacy;
    
    if (!privacySettings) {
      return profile;
    }
    
    // プライバシー設定に基づく情報フィルタリング
    const filteredProfile = { ...profile };
    
    if (privacySettings.profileVisibility === 'private' && profile.id !== requesterId) {
      // プライベート設定の場合、基本情報のみ表示
      filteredProfile.personalInfo = {
        displayName: profile.personalInfo.displayName
      };
      delete filteredProfile.workInfo;
      delete filteredProfile.preferences;
    }
    
    return filteredProfile;
  }
}
```

---

## 変更履歴

| 日付 | バージョン | 変更内容 | 変更者 |
|------|-----------|----------|--------|
| 2025-05-30 | 1.0.0 | 初版作成 | システムアーキテクト |
