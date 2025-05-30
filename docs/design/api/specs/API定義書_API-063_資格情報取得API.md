# API定義書: API-063 資格情報取得API

## 基本情報

| 項目 | 内容 |
|------|------|
| API ID | API-063 |
| API名称 | 資格情報取得API |
| エンドポイント | /api/certifications/{user_id} |
| 概要 | 資格情報取得 |
| 利用画面 | SCR-TRAINING |
| 優先度 | 中 |
| 実装予定 | Week 3-4 |

---

## エンドポイント詳細

### 1. ユーザー資格情報取得

#### リクエスト
```http
GET /api/certifications/{user_id}
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
| status | string | × | 資格ステータスフィルタ | active, expired, pending |
| category | string | × | 資格カテゴリフィルタ | IT, 語学, 業務 |
| includeExpired | boolean | × | 期限切れ資格を含む | true, false |
| sortBy | string | × | ソート項目 | obtainedDate, expiryDate, name |
| sortOrder | string | × | ソート順 | asc, desc |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "userInfo": {
      "userId": "user_001",
      "displayName": "田中太郎",
      "email": "tanaka@company-a.com",
      "department": "開発部",
      "position": "シニアエンジニア"
    },
    "certifications": [
      {
        "certificationId": "cert_001",
        "certificationName": "AWS Solutions Architect Associate",
        "certificationCode": "SAA-C03",
        "category": "クラウド",
        "provider": "Amazon Web Services",
        "level": "Associate",
        "obtainedDate": "2024-03-15",
        "expiryDate": "2027-03-15",
        "status": "active",
        "credentialId": "AWS-SAA-12345678",
        "verificationUrl": "https://aws.amazon.com/verification/AWS-SAA-12345678",
        "certificateUrl": "https://storage.example.com/certificates/aws_saa_cert_001.pdf",
        "score": 850,
        "maxScore": 1000,
        "passingScore": 720,
        "studyHours": 120,
        "examLocation": "オンライン",
        "examLanguage": "日本語",
        "renewalRequired": true,
        "renewalDate": "2026-12-15",
        "cpdPoints": 15,
        "skills": [
          {
            "skillName": "AWS EC2",
            "proficiencyLevel": "上級"
          },
          {
            "skillName": "AWS VPC",
            "proficiencyLevel": "上級"
          },
          {
            "skillName": "AWS S3",
            "proficiencyLevel": "上級"
          }
        ],
        "relatedProjects": [
          {
            "projectName": "クラウド移行プロジェクト",
            "role": "インフラ設計",
            "period": "2024-04-01 - 2024-09-30"
          }
        ],
        "notes": "実務でのAWS活用経験も豊富。チームのクラウド移行をリード。",
        "tags": ["AWS", "クラウド", "インフラ", "アーキテクチャ"],
        "createdAt": "2024-03-16T10:30:00Z",
        "updatedAt": "2024-03-16T10:30:00Z"
      },
      {
        "certificationId": "cert_002",
        "certificationName": "TOEIC Listening & Reading Test",
        "certificationCode": "TOEIC-LR",
        "category": "語学",
        "provider": "Educational Testing Service",
        "level": "スコア制",
        "obtainedDate": "2024-01-20",
        "expiryDate": "2026-01-20",
        "status": "active",
        "credentialId": "TOEIC-2024-001234",
        "verificationUrl": null,
        "certificateUrl": "https://storage.example.com/certificates/toeic_cert_002.pdf",
        "score": 885,
        "maxScore": 990,
        "passingScore": null,
        "studyHours": 80,
        "examLocation": "東京テストセンター",
        "examLanguage": "英語",
        "renewalRequired": false,
        "renewalDate": null,
        "cpdPoints": 0,
        "skills": [
          {
            "skillName": "英語リスニング",
            "proficiencyLevel": "上級"
          },
          {
            "skillName": "英語リーディング",
            "proficiencyLevel": "上級"
          }
        ],
        "relatedProjects": [
          {
            "projectName": "海外クライアント対応",
            "role": "技術コミュニケーション",
            "period": "2024-02-01 - 継続中"
          }
        ],
        "notes": "海外クライアントとの技術的なコミュニケーションで活用。",
        "tags": ["英語", "語学", "コミュニケーション"],
        "createdAt": "2024-01-21T14:15:00Z",
        "updatedAt": "2024-01-21T14:15:00Z"
      },
      {
        "certificationId": "cert_003",
        "certificationName": "情報処理安全確保支援士",
        "certificationCode": "SC",
        "category": "情報処理",
        "provider": "情報処理推進機構（IPA）",
        "level": "高度",
        "obtainedDate": "2023-10-15",
        "expiryDate": "2026-04-01",
        "status": "active",
        "credentialId": "SC-2023-001234",
        "verificationUrl": "https://www.ipa.go.jp/verification/SC-2023-001234",
        "certificateUrl": "https://storage.example.com/certificates/sc_cert_003.pdf",
        "score": null,
        "maxScore": null,
        "passingScore": 60,
        "studyHours": 200,
        "examLocation": "東京会場",
        "examLanguage": "日本語",
        "renewalRequired": true,
        "renewalDate": "2025-04-01",
        "cpdPoints": 20,
        "skills": [
          {
            "skillName": "情報セキュリティ",
            "proficiencyLevel": "専門"
          },
          {
            "skillName": "リスク管理",
            "proficiencyLevel": "上級"
          },
          {
            "skillName": "セキュリティ監査",
            "proficiencyLevel": "上級"
          }
        ],
        "relatedProjects": [
          {
            "projectName": "セキュリティ強化プロジェクト",
            "role": "セキュリティアーキテクト",
            "period": "2023-11-01 - 2024-03-31"
          }
        ],
        "notes": "継続研修の受講が必要。来年度の更新に向けて準備中。",
        "tags": ["セキュリティ", "情報処理", "国家資格"],
        "createdAt": "2023-10-16T09:45:00Z",
        "updatedAt": "2024-05-30T16:20:00Z"
      },
      {
        "certificationId": "cert_004",
        "certificationName": "Oracle Certified Professional, Java SE 11 Developer",
        "certificationCode": "OCP-Java11",
        "category": "プログラミング",
        "provider": "Oracle Corporation",
        "level": "Professional",
        "obtainedDate": "2023-06-10",
        "expiryDate": null,
        "status": "active",
        "credentialId": "OCP-2023-567890",
        "verificationUrl": "https://catalog-education.oracle.com/pls/certview/sharebadge?id=OCP-2023-567890",
        "certificateUrl": "https://storage.example.com/certificates/ocp_java_cert_004.pdf",
        "score": null,
        "maxScore": null,
        "passingScore": 68,
        "studyHours": 150,
        "examLocation": "オンライン",
        "examLanguage": "英語",
        "renewalRequired": false,
        "renewalDate": null,
        "cpdPoints": 0,
        "skills": [
          {
            "skillName": "Java",
            "proficiencyLevel": "専門"
          },
          {
            "skillName": "オブジェクト指向プログラミング",
            "proficiencyLevel": "専門"
          },
          {
            "skillName": "Java SE API",
            "proficiencyLevel": "上級"
          }
        ],
        "relatedProjects": [
          {
            "projectName": "基幹システム刷新",
            "role": "Javaアーキテクト",
            "period": "2023-07-01 - 2024-02-29"
          }
        ],
        "notes": "Java開発の中核メンバーとして活躍。後輩の指導も担当。",
        "tags": ["Java", "プログラミング", "Oracle"],
        "createdAt": "2023-06-11T11:30:00Z",
        "updatedAt": "2023-06-11T11:30:00Z"
      }
    ],
    "summary": {
      "totalCertifications": 4,
      "activeCertifications": 4,
      "expiredCertifications": 0,
      "pendingRenewal": 1,
      "categorySummary": {
        "クラウド": 1,
        "語学": 1,
        "情報処理": 1,
        "プログラミング": 1
      },
      "upcomingRenewals": [
        {
          "certificationId": "cert_003",
          "certificationName": "情報処理安全確保支援士",
          "renewalDate": "2025-04-01",
          "daysUntilRenewal": 306
        }
      ],
      "upcomingExpirations": [
        {
          "certificationId": "cert_002",
          "certificationName": "TOEIC Listening & Reading Test",
          "expiryDate": "2026-01-20",
          "daysUntilExpiry": 600
        }
      ],
      "totalStudyHours": 550,
      "totalCpdPoints": 35,
      "skillsCovered": [
        "AWS EC2", "AWS VPC", "AWS S3", "英語リスニング", "英語リーディング",
        "情報セキュリティ", "リスク管理", "Java", "オブジェクト指向プログラミング"
      ],
      "lastUpdated": "2024-05-30T16:20:00Z"
    },
    "recommendations": [
      {
        "type": "renewal_reminder",
        "title": "資格更新の準備",
        "description": "情報処理安全確保支援士の更新が近づいています。継続研修の受講をお忘れなく。",
        "priority": "high",
        "dueDate": "2025-04-01"
      },
      {
        "type": "skill_enhancement",
        "title": "関連資格の取得",
        "description": "AWS Professional レベルの資格取得を検討してみてください。",
        "priority": "medium",
        "suggestedCertifications": ["AWS Solutions Architect Professional"]
      },
      {
        "type": "knowledge_update",
        "title": "技術トレンドの追跡",
        "description": "クラウドネイティブ技術の最新動向をキャッチアップしましょう。",
        "priority": "low"
      }
    ]
  }
}
```

### 2. 資格カテゴリ別統計取得

#### リクエスト
```http
GET /api/certifications/{user_id}/statistics
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### クエリパラメータ
| パラメータ名 | 型 | 必須 | 説明 | 例 |
|-------------|---|------|------|---|
| period | string | × | 集計期間 | last_year, current_year, all_time |
| groupBy | string | × | グループ化項目 | category, provider, level |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "certificationStatistics": {
      "period": "all_time",
      "totalCertifications": 4,
      "activeCertifications": 4,
      "expiredCertifications": 0,
      "categoryBreakdown": {
        "クラウド": {
          "count": 1,
          "percentage": 25.0,
          "averageScore": 850,
          "totalStudyHours": 120,
          "certifications": ["AWS Solutions Architect Associate"]
        },
        "語学": {
          "count": 1,
          "percentage": 25.0,
          "averageScore": 885,
          "totalStudyHours": 80,
          "certifications": ["TOEIC Listening & Reading Test"]
        },
        "情報処理": {
          "count": 1,
          "percentage": 25.0,
          "averageScore": null,
          "totalStudyHours": 200,
          "certifications": ["情報処理安全確保支援士"]
        },
        "プログラミング": {
          "count": 1,
          "percentage": 25.0,
          "averageScore": null,
          "totalStudyHours": 150,
          "certifications": ["Oracle Certified Professional, Java SE 11 Developer"]
        }
      },
      "providerBreakdown": {
        "Amazon Web Services": 1,
        "Educational Testing Service": 1,
        "情報処理推進機構（IPA）": 1,
        "Oracle Corporation": 1
      },
      "levelBreakdown": {
        "Associate": 1,
        "Professional": 1,
        "高度": 1,
        "スコア制": 1
      },
      "yearlyTrend": [
        {
          "year": 2023,
          "certificationsObtained": 2,
          "totalStudyHours": 350,
          "categories": ["情報処理", "プログラミング"]
        },
        {
          "year": 2024,
          "certificationsObtained": 2,
          "totalStudyHours": 200,
          "categories": ["語学", "クラウド"]
        }
      ],
      "skillsCoverage": {
        "technical": 75.0,
        "language": 25.0,
        "management": 0.0,
        "business": 0.0
      },
      "renewalSchedule": [
        {
          "year": 2025,
          "renewalsRequired": 1,
          "certifications": ["情報処理安全確保支援士"]
        },
        {
          "year": 2026,
          "renewalsRequired": 1,
          "certifications": ["AWS Solutions Architect Associate"]
        },
        {
          "year": 2027,
          "renewalsRequired": 0,
          "certifications": []
        }
      ],
      "generatedAt": "2025-05-30T21:50:00Z"
    }
  }
}
```

### 3. 資格検索

#### リクエスト
```http
GET /api/certifications/search
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### クエリパラメータ
| パラメータ名 | 型 | 必須 | 説明 | 例 |
|-------------|---|------|------|---|
| q | string | × | 検索キーワード | AWS, Java, TOEIC |
| category | string | × | カテゴリフィルタ | IT, 語学, 業務 |
| provider | string | × | 提供者フィルタ | AWS, Oracle, IPA |
| level | string | × | レベルフィルタ | Associate, Professional |
| department | string | × | 部署フィルタ | 開発部, QA部 |
| limit | number | × | 取得件数 | 20 |
| offset | number | × | オフセット | 0 |

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
          "department": "開発部",
          "position": "シニアエンジニア"
        },
        "certification": {
          "certificationId": "cert_001",
          "certificationName": "AWS Solutions Architect Associate",
          "category": "クラウド",
          "provider": "Amazon Web Services",
          "obtainedDate": "2024-03-15",
          "status": "active",
          "score": 850
        },
        "relevanceScore": 95.5
      },
      {
        "userId": "user_002",
        "userInfo": {
          "displayName": "佐藤花子",
          "department": "開発部",
          "position": "エンジニア"
        },
        "certification": {
          "certificationId": "cert_005",
          "certificationName": "AWS Developer Associate",
          "category": "クラウド",
          "provider": "Amazon Web Services",
          "obtainedDate": "2024-01-10",
          "status": "active",
          "score": 780
        },
        "relevanceScore": 88.2
      }
    ],
    "searchSummary": {
      "totalResults": 15,
      "displayedResults": 2,
      "searchQuery": "AWS",
      "filters": {
        "category": "クラウド"
      },
      "categorySummary": {
        "クラウド": 15,
        "プログラミング": 0,
        "語学": 0
      }
    },
    "pagination": {
      "limit": 20,
      "offset": 0,
      "total": 15,
      "hasMore": false
    }
  }
}
```

---

## エラーコード一覧

| エラーコード | HTTPステータス | 説明 | 対処法 |
|-------------|---------------|------|--------|
| UNAUTHORIZED | 401 | 認証エラー | 有効なJWTトークンを設定 |
| FORBIDDEN | 403 | アクセス権限なし | 資格情報参照権限が必要 |
| USER_NOT_FOUND | 404 | ユーザーが見つからない | 正しいユーザーIDを指定 |
| CERTIFICATION_NOT_FOUND | 404 | 資格情報が見つからない | 正しい資格IDを指定 |
| INVALID_QUERY_PARAMETER | 400 | 無効なクエリパラメータ | パラメータ値を確認 |
| TENANT_MISMATCH | 403 | テナント不一致 | 同一テナント内のデータのみ参照可能 |
| INTERNAL_SERVER_ERROR | 500 | サーバー内部エラー | システム管理者に連絡 |

---

## セキュリティ要件

### 認証・認可
- **認証**: JWT Bearer Token必須
- **権限**: 資格情報参照権限（certification:read）
- **テナント分離**: テナント内データのみ参照可能

### データ保護
- **個人情報保護**: 本人または管理者のみ詳細情報参照可能
- **機密情報**: 資格証明書URLは一時的なアクセストークン付与
- **検索制限**: 部署・役職に応じた検索範囲制限

---

## パフォーマンス要件

| 項目 | 要件 |
|------|------|
| レスポンス時間 | 95%のリクエストが1秒以内 |
| スループット | 200 req/sec |
| 検索結果 | 最大1000件 |
| 同時接続 | 500セッション |

---

## テスト仕様

### 単体テスト
```typescript
describe('Certification Information API', () => {
  test('GET /api/certifications/{user_id} - 資格情報取得', async () => {
    const response = await request(app)
      .get('/api/certifications/user_001')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.certifications).toBeInstanceOf(Array);
    expect(response.body.data.summary).toBeDefined();
    expect(response.body.data.recommendations).toBeInstanceOf(Array);
  });
  
  test('GET /api/certifications/{user_id}?status=active - ステータスフィルタ', async () => {
    const response = await request(app)
      .get('/api/certifications/user_001?status=active')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.certifications.every(cert => 
      cert.status === 'active'
    )).toBe(true);
  });
  
  test('GET /api/certifications/{user_id}/statistics - 統計情報取得', async () => {
    const response = await request(app)
      .get('/api/certifications/user_001/statistics')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.certificationStatistics).toBeDefined();
    expect(response.body.data.certificationStatistics.categoryBreakdown).toBeDefined();
  });
  
  test('GET /api/certifications/search - 資格検索', async () => {
    const response = await request(app)
      .get('/api/certifications/search?q=AWS&category=クラウド')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.searchResults).toBeInstanceOf(Array);
    expect(response.body.data.searchSummary).toBeDefined();
  });
});
```

### 統合テスト
```typescript
describe('Certification Integration', () => {
  test('資格情報の完全性確認', async () => {
    // 1. 資格情報取得
    const certResponse = await getCertifications('user_001');
    expect(certResponse.data.certifications.length).toBeGreaterThan(0);
    
    // 2. 統計情報との整合性確認
    const statsResponse = await getCertificationStatistics('user_001');
    expect(statsResponse.data.certificationStatistics.totalCertifications)
      .toBe(certResponse.data.summary.totalCertifications);
    
    // 3. 検索結果との整合性確認
    const searchResponse = await searchCertifications({
      q: certResponse.data.certifications[0].certificationName
    });
    expect(searchResponse.data.searchResults.some(result => 
      result.userId === 'user_001'
    )).toBe(true);
  });
  
  test('権限制御確認', async () => {
    // 他ユーザーの資格情報参照試行
    const response = await request(app)
      .get('/api/certifications/other_user')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(403);
    
    expect(response.body.error.code).toBe('FORBIDDEN');
  });
  
  test('期限切れ資格の処理確認', async () => {
    // 期限切れ資格を含む取得
    const response = await request(app)
      .get('/api/certifications/user_001?includeExpired=true')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(200);
    
    const expiredCerts = response.body.data.certifications.filter(cert => 
      cert.status === 'expired'
    );
    
    expect(response.body.data.summary.expiredCertifications)
      .toBe(expiredCerts.length);
  });
});
```

---

## 実装メモ

### データベーススキーマ
```sql
CREATE TABLE user_certifications (
  id VARCHAR(50) PRIMARY KEY,
  user_id VARCHAR(50) NOT NULL,
  tenant_id VARCHAR(50) NOT NULL,
  certification_name VARCHAR(255) NOT NULL,
  certification_code VARCHAR(100),
  category VARCHAR(100) NOT NULL,
  provider VARCHAR(255) NOT NULL,
  level VARCHAR(100),
  obtained_date DATE NOT NULL,
  expiry_date DATE,
  status VARCHAR(50) DEFAULT 'active',
  credential_id VARCHAR(255),
  verification_url TEXT,
  certificate_url TEXT,
  score INTEGER,
  max_score INTEGER,
  passing_score INTEGER,
  study_hours INTEGER,
  exam_location VARCHAR(255),
  exam_language VARCHAR(100),
  renewal_required BOOLEAN DEFAULT FALSE,
  renewal_date DATE,
  cpd_points INTEGER DEFAULT 0,
  notes TEXT,
  tags JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

CREATE TABLE certification_skills (
  id VARCHAR(50) PRIMARY KEY,
  certification_id VARCHAR(50) NOT NULL,
  skill_name VARCHAR(255) NOT NULL,
  proficiency_level VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (certification_id) REFERENCES user_certifications(id)
);

CREATE INDEX idx_user_certifications_user_id ON user_certifications(user_id);
CREATE INDEX idx_user_certifications_status ON user_certifications(status);
CREATE INDEX idx_user_certifications_category ON user_certifications(category);
CREATE INDEX idx_user_certifications_expiry_date ON user_certifications(expiry_date);
CREATE INDEX idx_certification_skills_cert_id ON certification_skills(certification_id);
```

### Next.js実装例
```typescript
// pages/api/certifications/[user_id]/index.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { authenticateToken, requirePermission } from '@/lib/auth';
import { CertificationService } from '@/services/CertificationService';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const user = await authenticateToken(req);
    await requirePermission(user, 'certification:read');
    
    const { user_id } = req.query;
    const certificationService = new CertificationService();
    
    switch (req.method) {
      case 'GET':
        const certifications = await certificationService.getCertifications(
          user.tenantId,
          user_id as string,
          req.query
        );
        
        return res.status(200).json({ success: true, data: certifications });
        
      default:
        return res.status(405).json({ success: false, error: 'Method not allowed' });
    }
  } catch (error) {
    console.error('Certification API error:', error);
    return res.status(error.statusCode || 500).json({
      success: false,
      error: {
        code: error.code || 'INTERNAL_SERVER_ERROR',
        message: error.message
      }
    });
  }
}
