# API仕様書: API-064 資格情報更新API

## 基本情報

| 項目 | 内容 |
|------|------|
| API ID | API-064 |
| API名称 | 資格情報更新API |
| エンドポイント | /api/certifications/{user_id} |
| 概要 | 資格情報更新 |
| 利用画面 | SCR-TRAINING |
| 優先度 | 中 |
| 実装予定 | Week 3-4 |

---

## エンドポイント詳細

### 1. 資格情報更新

#### リクエスト
```http
PUT /api/certifications/{user_id}
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
      "tags": ["AWS", "クラウド", "インフラ", "アーキテクチャ"]
    },
    {
      "certificationId": "cert_005",
      "certificationName": "AWS Solutions Architect Professional",
      "certificationCode": "SAP-C02",
      "category": "クラウド",
      "provider": "Amazon Web Services",
      "level": "Professional",
      "obtainedDate": "2025-05-30",
      "expiryDate": "2028-05-30",
      "status": "active",
      "credentialId": "AWS-SAP-87654321",
      "verificationUrl": "https://aws.amazon.com/verification/AWS-SAP-87654321",
      "certificateUrl": "https://storage.example.com/certificates/aws_sap_cert_005.pdf",
      "score": 780,
      "maxScore": 1000,
      "passingScore": 750,
      "studyHours": 200,
      "examLocation": "オンライン",
      "examLanguage": "英語",
      "renewalRequired": true,
      "renewalDate": "2027-02-28",
      "cpdPoints": 25,
      "skills": [
        {
          "skillName": "AWS アーキテクチャ設計",
          "proficiencyLevel": "専門"
        },
        {
          "skillName": "AWS セキュリティ",
          "proficiencyLevel": "上級"
        },
        {
          "skillName": "AWS コスト最適化",
          "proficiencyLevel": "上級"
        }
      ],
      "relatedProjects": [
        {
          "projectName": "エンタープライズクラウド戦略",
          "role": "クラウドアーキテクト",
          "period": "2025-01-01 - 継続中"
        }
      ],
      "notes": "Professional レベル取得により、より高度なアーキテクチャ設計が可能に。",
      "tags": ["AWS", "Professional", "アーキテクチャ", "エンタープライズ"]
    }
  ],
  "updateReason": "新規資格取得および既存資格情報の更新",
  "notifyManager": true,
  "updateSkillProfile": true
}
```

#### バリデーションルール
| フィールド | ルール |
|-----------|--------|
| certificationName | 必須、文字列、最大255文字 |
| category | 必須、有効なカテゴリ名 |
| provider | 必須、文字列、最大255文字 |
| obtainedDate | 必須、日付、未来日不可 |
| expiryDate | 任意、日付、obtainedDate以降 |
| status | 必須、active/expired/pending/revoked |
| score | 任意、数値、0以上 |
| maxScore | 任意、数値、score以上 |
| studyHours | 任意、数値、0以上 |
| skills[].skillName | 必須、文字列、最大100文字 |
| skills[].proficiencyLevel | 必須、初級/中級/上級/専門 |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "updatedCertifications": [
      {
        "certificationId": "cert_001",
        "certificationName": "AWS Solutions Architect Associate",
        "status": "updated",
        "changes": [
          "notes",
          "relatedProjects"
        ],
        "lastUpdated": "2025-05-30T22:00:00Z"
      },
      {
        "certificationId": "cert_005",
        "certificationName": "AWS Solutions Architect Professional",
        "status": "created",
        "changes": [
          "new_certification"
        ],
        "lastUpdated": "2025-05-30T22:00:00Z"
      }
    ],
    "updateSummary": {
      "totalCertifications": 5,
      "newCertifications": 1,
      "updatedCertifications": 1,
      "deletedCertifications": 0,
      "skillsUpdated": 6,
      "cpdPointsAdded": 25
    },
    "skillProfileUpdates": [
      {
        "skillName": "AWS アーキテクチャ設計",
        "oldLevel": "上級",
        "newLevel": "専門",
        "source": "certification"
      },
      {
        "skillName": "AWS セキュリティ",
        "oldLevel": null,
        "newLevel": "上級",
        "source": "certification"
      }
    ],
    "notifications": [
      {
        "type": "manager_notification",
        "recipient": "manager_001",
        "message": "田中太郎さんがAWS Solutions Architect Professionalを取得しました",
        "sent": true
      },
      {
        "type": "team_notification",
        "recipient": "team_dev",
        "message": "チームメンバーの新しい資格取得をお知らせします",
        "sent": true
      }
    ],
    "recommendations": [
      {
        "type": "career_path",
        "title": "キャリアパスの提案",
        "description": "AWS Professional資格を活かして、クラウドアーキテクト職への転向を検討してみてください",
        "priority": "medium"
      },
      {
        "type": "next_certification",
        "title": "次の資格取得提案",
        "description": "AWS DevOps Engineer Professionalの取得を推奨します",
        "suggestedCertifications": ["AWS DevOps Engineer Professional"],
        "priority": "low"
      }
    ],
    "updatedAt": "2025-05-30T22:00:00Z"
  }
}
```

### 2. 単一資格情報更新

#### リクエスト
```http
PUT /api/certifications/{user_id}/{certification_id}
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### パスパラメータ
| パラメータ名 | 型 | 必須 | 説明 |
|-------------|---|------|------|
| user_id | string | ○ | ユーザーID |
| certification_id | string | ○ | 資格ID |

#### リクエストボディ
```json
{
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
    }
  ],
  "relatedProjects": [
    {
      "projectName": "クラウド移行プロジェクト",
      "role": "インフラ設計",
      "period": "2024-04-01 - 2024-09-30"
    }
  ],
  "notes": "更新されたノート内容",
  "tags": ["AWS", "クラウド", "インフラ", "アーキテクチャ"],
  "updateReason": "資格情報の詳細更新"
}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "updatedCertification": {
      "certificationId": "cert_001",
      "certificationName": "AWS Solutions Architect Associate",
      "status": "updated",
      "changes": [
        "notes",
        "skills",
        "relatedProjects"
      ],
      "previousValues": {
        "notes": "実務でのAWS活用経験も豊富。",
        "skillsCount": 3
      },
      "newValues": {
        "notes": "更新されたノート内容",
        "skillsCount": 2
      },
      "lastUpdated": "2025-05-30T22:05:00Z"
    },
    "impactAnalysis": {
      "skillProfileChanges": 2,
      "relatedProjectsUpdated": 1,
      "notificationsTriggered": 0
    },
    "updatedAt": "2025-05-30T22:05:00Z"
  }
}
```

### 3. 資格ステータス更新

#### リクエスト
```http
PATCH /api/certifications/{user_id}/{certification_id}/status
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "status": "expired",
  "statusReason": "有効期限切れ",
  "effectiveDate": "2025-05-30",
  "renewalPlan": {
    "planned": true,
    "targetDate": "2025-08-31",
    "studyPlan": "継続研修受講予定"
  },
  "notifyManager": true
}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "statusUpdate": {
      "certificationId": "cert_003",
      "certificationName": "情報処理安全確保支援士",
      "previousStatus": "active",
      "newStatus": "expired",
      "effectiveDate": "2025-05-30",
      "statusReason": "有効期限切れ"
    },
    "renewalPlan": {
      "planned": true,
      "targetDate": "2025-08-31",
      "studyPlan": "継続研修受講予定",
      "reminderScheduled": true
    },
    "skillImpact": {
      "affectedSkills": [
        {
          "skillName": "情報セキュリティ",
          "currentLevel": "専門",
          "statusNote": "資格期限切れにより要注意"
        }
      ],
      "recommendedActions": [
        "早期の資格更新",
        "代替資格の検討"
      ]
    },
    "notifications": [
      {
        "type": "manager_notification",
        "message": "田中太郎さんの情報処理安全確保支援士が期限切れになりました",
        "sent": true
      },
      {
        "type": "renewal_reminder",
        "scheduledDate": "2025-07-01",
        "message": "資格更新の準備を開始してください"
      }
    ],
    "updatedAt": "2025-05-30T22:10:00Z"
  }
}
```

### 4. 資格証明書アップロード

#### リクエスト
```http
POST /api/certifications/{user_id}/{certification_id}/certificate
Authorization: Bearer {jwt_token}
Content-Type: multipart/form-data
```

#### リクエストボディ（multipart/form-data）
```
certificate: [ファイル] (PDF, JPG, PNG)
description: "AWS Solutions Architect Associate 合格証明書"
isPublic: false
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "uploadResult": {
      "certificateId": "cert_file_001",
      "certificationId": "cert_001",
      "fileName": "aws_saa_certificate.pdf",
      "fileSize": 1024000,
      "mimeType": "application/pdf",
      "uploadedUrl": "https://storage.example.com/certificates/aws_saa_cert_001.pdf",
      "thumbnailUrl": "https://storage.example.com/thumbnails/aws_saa_cert_001_thumb.jpg",
      "description": "AWS Solutions Architect Associate 合格証明書",
      "isPublic": false,
      "uploadedAt": "2025-05-30T22:15:00Z"
    },
    "securityScan": {
      "status": "clean",
      "scanDate": "2025-05-30T22:15:30Z",
      "threats": []
    },
    "verification": {
      "autoVerified": true,
      "verificationMethod": "ocr_text_analysis",
      "confidence": 95.5,
      "extractedData": {
        "candidateName": "田中太郎",
        "certificationName": "AWS Solutions Architect Associate",
        "issueDate": "2024-03-15",
        "credentialId": "AWS-SAA-12345678"
      }
    },
    "updatedAt": "2025-05-30T22:15:00Z"
  }
}
```

### 5. 一括資格インポート

#### リクエスト
```http
POST /api/certifications/{user_id}/import
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "importSource": "external_system",
  "importFormat": "json",
  "certifications": [
    {
      "externalId": "ext_cert_001",
      "certificationName": "Microsoft Azure Fundamentals",
      "certificationCode": "AZ-900",
      "category": "クラウド",
      "provider": "Microsoft",
      "level": "Fundamentals",
      "obtainedDate": "2024-02-10",
      "expiryDate": null,
      "credentialId": "MS-AZ900-123456",
      "verificationUrl": "https://learn.microsoft.com/api/credentials/share/ja-jp/123456",
      "score": 850,
      "maxScore": 1000,
      "studyHours": 40
    },
    {
      "externalId": "ext_cert_002",
      "certificationName": "Google Cloud Professional Cloud Architect",
      "certificationCode": "PCA",
      "category": "クラウド",
      "provider": "Google Cloud",
      "level": "Professional",
      "obtainedDate": "2024-04-20",
      "expiryDate": "2026-04-20",
      "credentialId": "GCP-PCA-789012",
      "verificationUrl": "https://www.credential.net/789012",
      "score": null,
      "maxScore": null,
      "studyHours": 150
    }
  ],
  "importOptions": {
    "skipDuplicates": true,
    "updateExisting": false,
    "validateCredentials": true,
    "notifyOnCompletion": true
  }
}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "importResult": {
      "totalSubmitted": 2,
      "successfulImports": 2,
      "failedImports": 0,
      "skippedDuplicates": 0,
      "updatedExisting": 0
    },
    "importedCertifications": [
      {
        "externalId": "ext_cert_001",
        "certificationId": "cert_006",
        "certificationName": "Microsoft Azure Fundamentals",
        "status": "imported",
        "verificationStatus": "verified"
      },
      {
        "externalId": "ext_cert_002",
        "certificationId": "cert_007",
        "certificationName": "Google Cloud Professional Cloud Architect",
        "status": "imported",
        "verificationStatus": "pending"
      }
    ],
    "validationResults": [
      {
        "certificationId": "cert_006",
        "credentialVerified": true,
        "verificationMethod": "api_check",
        "verificationDate": "2025-05-30T22:20:00Z"
      },
      {
        "certificationId": "cert_007",
        "credentialVerified": false,
        "verificationMethod": "manual_review_required",
        "verificationNote": "Google Cloud APIでの自動検証に失敗"
      }
    ],
    "skillUpdates": [
      {
        "skillName": "Microsoft Azure",
        "newLevel": "中級",
        "source": "cert_006"
      },
      {
        "skillName": "Google Cloud Platform",
        "newLevel": "上級",
        "source": "cert_007"
      }
    ],
    "importedAt": "2025-05-30T22:20:00Z"
  }
}
```

---

## エラーコード一覧

| エラーコード | HTTPステータス | 説明 | 対処法 |
|-------------|---------------|------|--------|
| UNAUTHORIZED | 401 | 認証エラー | 有効なJWTトークンを設定 |
| FORBIDDEN | 403 | アクセス権限なし | 資格情報更新権限が必要 |
| USER_NOT_FOUND | 404 | ユーザーが見つからない | 正しいユーザーIDを指定 |
| CERTIFICATION_NOT_FOUND | 404 | 資格情報が見つからない | 正しい資格IDを指定 |
| VALIDATION_ERROR | 400 | バリデーションエラー | 入力データを確認 |
| DUPLICATE_CERTIFICATION | 409 | 重複する資格情報 | 既存の資格情報を確認 |
| INVALID_DATE_RANGE | 400 | 無効な日付範囲 | 取得日と有効期限を確認 |
| FILE_UPLOAD_ERROR | 400 | ファイルアップロードエラー | ファイル形式・サイズを確認 |
| VIRUS_DETECTED | 400 | ウイルス検出 | 安全なファイルを使用 |
| CREDENTIAL_VERIFICATION_FAILED | 422 | 資格認証失敗 | 認証情報を確認 |
| IMPORT_FORMAT_ERROR | 400 | インポート形式エラー | データ形式を確認 |
| TENANT_MISMATCH | 403 | テナント不一致 | 同一テナント内のデータのみ更新可能 |
| CONCURRENT_UPDATE_ERROR | 409 | 同時更新エラー | 最新データを取得して再試行 |
| INTERNAL_SERVER_ERROR | 500 | サーバー内部エラー | システム管理者に連絡 |

---

## セキュリティ要件

### 認証・認可
- **認証**: JWT Bearer Token必須
- **権限**: 資格情報更新権限（certification:update）
- **テナント分離**: テナント内データのみ更新可能

### データ保護
- **個人情報保護**: 本人または管理者のみ更新可能
- **ファイル保護**: アップロードファイルのウイルススキャン
- **更新履歴**: 全更新操作を監査ログに記録

### 資格認証
- **自動検証**: 可能な場合は外部APIで資格認証
- **手動確認**: 自動検証不可の場合は管理者確認
- **偽造防止**: 証明書画像の改ざん検出

---

## パフォーマンス要件

| 項目 | 要件 |
|------|------|
| レスポンス時間 | 95%のリクエストが2秒以内 |
| スループット | 100 req/sec |
| ファイルアップロード | 最大10MB |
| 一括インポート | 最大100件 |

---

## テスト仕様

### 単体テスト
```typescript
describe('Certification Update API', () => {
  test('PUT /api/certifications/{user_id} - 資格情報更新', async () => {
    const certificationData = {
      certifications: [
        {
          certificationId: 'cert_001',
          certificationName: 'AWS Solutions Architect Associate',
          category: 'クラウド',
          provider: 'Amazon Web Services',
          obtainedDate: '2024-03-15',
          status: 'active',
          notes: '更新されたノート'
        }
      ],
      updateReason: 'テスト更新'
    };
    
    const response = await request(app)
      .put('/api/certifications/user_001')
      .set('Authorization', `Bearer ${userToken}`)
      .send(certificationData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.updatedCertifications).toBeInstanceOf(Array);
    expect(response.body.data.updateSummary).toBeDefined();
  });
  
  test('PUT /api/certifications/{user_id}/{certification_id} - 単一資格更新', async () => {
    const updateData = {
      notes: '更新されたノート内容',
      tags: ['AWS', 'クラウド', '更新済み'],
      updateReason: '詳細情報の更新'
    };
    
    const response = await request(app)
      .put('/api/certifications/user_001/cert_001')
      .set('Authorization', `Bearer ${userToken}`)
      .send(updateData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.updatedCertification).toBeDefined();
    expect(response.body.data.impactAnalysis).toBeDefined();
  });
  
  test('PATCH /api/certifications/{user_id}/{certification_id}/status - ステータス更新', async () => {
    const statusData = {
      status: 'expired',
      statusReason: 'テスト期限切れ',
      effectiveDate: '2025-05-30'
    };
    
    const response = await request(app)
      .patch('/api/certifications/user_001/cert_001/status')
      .set('Authorization', `Bearer ${userToken}`)
      .send(statusData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.statusUpdate).toBeDefined();
    expect(response.body.data.skillImpact).toBeDefined();
  });
  
  test('POST /api/certifications/{user_id}/import - 一括インポート', async () => {
    const importData = {
      importSource: 'test_system',
      certifications: [
        {
          externalId: 'test_001',
          certificationName: 'Test Certification',
          category: 'テスト',
          provider: 'Test Provider',
          obtainedDate: '2024-01-01'
        }
      ],
      importOptions: {
        skipDuplicates: true,
        validateCredentials: false
      }
    };
    
    const response = await request(app)
      .post('/api/certifications/user_001/import')
      .set('Authorization', `Bearer ${userToken}`)
      .send(importData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.importResult).toBeDefined();
    expect(response.body.data.importedCertifications).toBeInstanceOf(Array);
  });
});
```

### 統合テスト
```typescript
describe('Certification Update Integration', () => {
  test('資格更新からスキルプロファイル更新まで', async () => {
    // 1. 新規資格追加
    const addResponse = await updateCertifications('user_001', {
      certifications: [{
        certificationName: 'New Test Certification',
        category: 'テスト',
        provider: 'Test Provider',
        obtainedDate: '2025-05-30',
        skills: [{ skillName: 'テストスキル', proficiencyLevel: '上級' }]
      }],
      updateSkillProfile: true
    });
    
    expect(addResponse.data.updateSummary.newCertifications).toBe(1);
    expect(addResponse.data.skillProfileUpdates.length).toBeGreaterThan(0);
    
    // 2. スキルプロファイルの確認
    const skillResponse = await getSkills('user_001');
    expect(skillResponse.data.skills.some(skill => 
      skill.skillName === 'テストスキル'
    )).toBe(true);
    
    // 3. 資格ステータス更新
    const statusResponse = await updateCertificationStatus(
      'user_001', 
      addResponse.data.updatedCertifications[0].certificationId,
      { status: 'expired' }
    );
    
    expect(statusResponse.data.statusUpdate.newStatus).toBe('expired');
  });
  
  test('権限制御確認', async () => {
    // 他ユーザーの資格更新試行
    const response = await request(app)
      .put('/api/certifications/other_user')
      .set('Authorization', `Bearer ${userToken}`)
      .send({
        certifications: [{ certificationName: 'Test' }]
      })
      .expect(403);
    
    expect(response.body.error.code).toBe('FORBIDDEN');
  });
  
  test('ファイルアップロード確認', async () => {
    // 証明書ファイルアップロード
    const response = await request(app)
      .post('/api/certifications/user_001/cert_001/certificate')
      .set('Authorization', `Bearer ${userToken}`)
      .attach('certificate', 'test/fixtures/test_certificate.pdf')
      .field('description', 'テスト証明書')
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.uploadResult).toBeDefined();
    expect(response.body.data.securityScan.status).toBe('clean');
  });
});
```

---

## 実装メモ

### Next.js実装例
```typescript
// pages/api/certifications/[user_id]/index.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { authenticateToken, requirePermission } from '@/lib/auth';
import { CertificationUpdateService } from '@/services/CertificationUpdateService';
import { validateCertificationUpdate } from '@/lib/validation';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const user = await authenticateToken(req);
    await requirePermission(user
