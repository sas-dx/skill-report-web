# API仕様書: API-029 通知送信API

## 基本情報

| 項目 | 内容 |
|------|------|
| API ID | API-029 |
| API名称 | 通知送信API |
| エンドポイント | /api/notifications/send |
| 概要 | 通知送信実行 |
| 利用画面 | SCR-NOTIFY-ADMIN |
| 優先度 | 高 |
| 実装予定 | Week 2-3 |

---

## エンドポイント詳細

### 1. 即座通知送信

#### リクエスト
```http
POST /api/notifications/send
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "notificationType": "email",
  "templateType": "skill_expiry",
  "recipients": [
    {
      "userId": "user_001",
      "email": "tanaka@company-a.com",
      "displayName": "田中太郎"
    },
    {
      "userId": "user_002", 
      "email": "sato@company-a.com",
      "displayName": "佐藤花子"
    }
  ],
  "templateData": {
    "userName": "田中太郎",
    "certificationName": "AWS Solutions Architect Associate",
    "expiryDate": "2025-09-15",
    "daysLeft": 108,
    "renewalUrl": "https://aws.amazon.com/certification/recertification/"
  },
  "customMessage": "重要な資格の期限が近づいています。早めの更新をお願いします。",
  "priority": "high",
  "sendAt": "2025-05-30T21:15:00Z"
}
```

#### バリデーションルール
| フィールド | ルール |
|-----------|--------|
| notificationType | 必須、email/teams/lineWorks/inApp |
| templateType | 必須、有効なテンプレートタイプ |
| recipients | 必須、配列、最大100件 |
| recipients[].userId | 必須、有効なユーザーID |
| recipients[].email | 必須（email通知の場合）、有効なメールアドレス |
| templateData | 必須、オブジェクト |
| priority | 任意、low/medium/high |
| sendAt | 任意、ISO8601形式 |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "notificationId": "notif_batch_001",
    "status": "queued",
    "totalRecipients": 2,
    "estimatedDeliveryTime": "2025-05-30T21:16:00Z",
    "notifications": [
      {
        "id": "notif_001",
        "userId": "user_001",
        "email": "tanaka@company-a.com",
        "status": "queued",
        "scheduledAt": "2025-05-30T21:15:00Z"
      },
      {
        "id": "notif_002",
        "userId": "user_002",
        "email": "sato@company-a.com",
        "status": "queued",
        "scheduledAt": "2025-05-30T21:15:00Z"
      }
    ],
    "createdAt": "2025-05-30T21:10:00Z"
  }
}
```

### 2. 一括通知送信

#### リクエスト
```http
POST /api/notifications/send/bulk
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "notificationType": "email",
  "templateType": "goal_reminder",
  "recipientFilter": {
    "department": "開発部",
    "position": "エンジニア",
    "goalStatus": "in_progress",
    "lastLoginDays": 7
  },
  "templateData": {
    "quarterName": "2025年Q2",
    "reminderMessage": "四半期目標の進捗確認をお願いします",
    "deadlineDate": "2025-06-30"
  },
  "customMessage": "目標達成に向けて頑張りましょう！",
  "priority": "medium",
  "sendAt": "2025-05-31T09:00:00Z",
  "batchSize": 50,
  "intervalMinutes": 5
}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "batchId": "batch_001",
    "status": "scheduled",
    "totalRecipients": 25,
    "estimatedBatches": 1,
    "estimatedCompletionTime": "2025-05-31T09:05:00Z",
    "recipientSummary": {
      "byDepartment": {
        "開発部": 20,
        "QA部": 5
      },
      "byPosition": {
        "エンジニア": 18,
        "シニアエンジニア": 7
      }
    },
    "scheduledAt": "2025-05-31T09:00:00Z",
    "createdAt": "2025-05-30T21:10:00Z"
  }
}
```

### 3. 通知送信状況確認

#### リクエスト
```http
GET /api/notifications/send/{notification_id}/status
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### パスパラメータ
| パラメータ名 | 型 | 必須 | 説明 |
|-------------|---|------|------|
| notification_id | string | ○ | 通知ID |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "notificationId": "notif_batch_001",
    "status": "completed",
    "totalRecipients": 2,
    "deliveryStats": {
      "sent": 2,
      "delivered": 2,
      "failed": 0,
      "pending": 0
    },
    "notifications": [
      {
        "id": "notif_001",
        "userId": "user_001",
        "email": "tanaka@company-a.com",
        "status": "delivered",
        "sentAt": "2025-05-30T21:15:05Z",
        "deliveredAt": "2025-05-30T21:15:12Z",
        "messageId": "msg_001",
        "errorMessage": null
      },
      {
        "id": "notif_002",
        "userId": "user_002",
        "email": "sato@company-a.com",
        "status": "delivered",
        "sentAt": "2025-05-30T21:15:06Z",
        "deliveredAt": "2025-05-30T21:15:15Z",
        "messageId": "msg_002",
        "errorMessage": null
      }
    ],
    "createdAt": "2025-05-30T21:10:00Z",
    "completedAt": "2025-05-30T21:15:15Z"
  }
}
```

### 4. 通知送信キャンセル

#### リクエスト
```http
DELETE /api/notifications/send/{notification_id}
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "notificationId": "notif_batch_001",
    "status": "cancelled",
    "cancelledCount": 5,
    "alreadySentCount": 3,
    "message": "5件の通知をキャンセルしました（3件は既に送信済み）",
    "cancelledAt": "2025-05-30T21:12:00Z"
  }
}
```

### 5. 通知テンプレート取得

#### リクエスト
```http
GET /api/notifications/send/templates
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### クエリパラメータ
| パラメータ名 | 型 | 必須 | 説明 | 例 |
|-------------|---|------|------|---|
| notificationType | string | × | 通知タイプフィルタ | email, teams, lineWorks |
| category | string | × | カテゴリフィルタ | skill, goal, system |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "templates": [
      {
        "templateType": "skill_expiry",
        "templateName": "資格期限通知",
        "category": "skill",
        "supportedTypes": ["email", "teams", "inApp"],
        "requiredFields": [
          "userName",
          "certificationName", 
          "expiryDate",
          "daysLeft"
        ],
        "optionalFields": [
          "renewalUrl",
          "contactInfo"
        ],
        "preview": {
          "email": {
            "subject": "【重要】資格期限のお知らせ",
            "body": "{{userName}}様\n\n以下の資格の期限が近づいています：\n{{certificationName}}\n期限日：{{expiryDate}}\n\n更新手続きをお忘れなく。"
          },
          "teams": {
            "title": "資格期限通知",
            "body": "{{userName}}さんの{{certificationName}}が{{daysLeft}}日後に期限切れになります。"
          }
        }
      },
      {
        "templateType": "goal_reminder",
        "templateName": "目標進捗確認",
        "category": "goal",
        "supportedTypes": ["email", "teams", "inApp"],
        "requiredFields": [
          "userName",
          "quarterName",
          "reminderMessage"
        ],
        "optionalFields": [
          "deadlineDate",
          "progressRate"
        ],
        "preview": {
          "email": {
            "subject": "目標進捗確認のお知らせ",
            "body": "{{userName}}様\n\n{{quarterName}}の目標進捗確認の時期です。\n{{reminderMessage}}\n\n進捗を更新してください。"
          }
        }
      }
    ],
    "totalCount": 2
  }
}
```

### 6. 通知送信履歴取得

#### リクエスト
```http
GET /api/notifications/send/history
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### クエリパラメータ
| パラメータ名 | 型 | 必須 | 説明 | 例 |
|-------------|---|------|------|---|
| page | number | × | ページ番号（デフォルト: 1） | 1 |
| limit | number | × | 取得件数（デフォルト: 20） | 20 |
| notificationType | string | × | 通知タイプフィルタ | email, teams |
| status | string | × | ステータスフィルタ | sent, failed, pending |
| dateFrom | string | × | 開始日（YYYY-MM-DD） | 2025-05-01 |
| dateTo | string | × | 終了日（YYYY-MM-DD） | 2025-05-31 |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "notifications": [
      {
        "id": "notif_batch_001",
        "notificationType": "email",
        "templateType": "skill_expiry",
        "totalRecipients": 2,
        "status": "completed",
        "deliveryStats": {
          "sent": 2,
          "delivered": 2,
          "failed": 0
        },
        "createdBy": "admin@company-a.com",
        "createdAt": "2025-05-30T21:10:00Z",
        "completedAt": "2025-05-30T21:15:15Z"
      },
      {
        "id": "batch_001",
        "notificationType": "email",
        "templateType": "goal_reminder",
        "totalRecipients": 25,
        "status": "in_progress",
        "deliveryStats": {
          "sent": 15,
          "delivered": 12,
          "failed": 1,
          "pending": 10
        },
        "createdBy": "manager@company-a.com",
        "createdAt": "2025-05-30T20:00:00Z",
        "completedAt": null
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 45,
      "totalPages": 3
    },
    "statistics": {
      "totalSent": 125,
      "successRate": 96.8,
      "byType": {
        "email": { "sent": 80, "success": 78, "failed": 2 },
        "teams": { "sent": 35, "success": 35, "failed": 0 },
        "inApp": { "sent": 10, "success": 8, "failed": 2 }
      }
    }
  }
}
```

---

## エラーコード一覧

| エラーコード | HTTPステータス | 説明 | 対処法 |
|-------------|---------------|------|--------|
| UNAUTHORIZED | 401 | 認証エラー | 有効なJWTトークンを設定 |
| FORBIDDEN | 403 | 権限不足 | 通知送信権限が必要 |
| VALIDATION_ERROR | 400 | バリデーションエラー | リクエストデータを確認 |
| TEMPLATE_NOT_FOUND | 404 | テンプレートが見つからない | 有効なテンプレートタイプを指定 |
| RECIPIENT_LIMIT_EXCEEDED | 400 | 受信者数上限超過 | 受信者数を100件以下に制限 |
| NOTIFICATION_NOT_FOUND | 404 | 通知が見つからない | 正しい通知IDを指定 |
| NOTIFICATION_ALREADY_SENT | 409 | 通知が既に送信済み | 送信済み通知はキャンセル不可 |
| TEMPLATE_PARSE_ERROR | 400 | テンプレート解析エラー | テンプレートデータを確認 |
| DELIVERY_SERVICE_ERROR | 503 | 配信サービスエラー | 配信サービスの状態を確認 |
| RATE_LIMIT_EXCEEDED | 429 | レート制限超過 | 送信頻度を調整 |
| TENANT_MISMATCH | 403 | テナント不一致 | 同一テナント内のユーザーのみ送信可能 |
| INTERNAL_SERVER_ERROR | 500 | サーバー内部エラー | システム管理者に連絡 |

---

## セキュリティ要件

### 認証・認可
- **認証**: JWT Bearer Token必須
- **権限**: 通知送信権限（notification:send）
- **テナント分離**: テナント内ユーザーのみ送信可能

### データ保護
- **個人情報保護**: 受信者情報の適切な暗号化
- **送信制限**: レート制限による悪用防止
- **監査ログ**: 全送信操作を記録

---

## パフォーマンス要件

| 項目 | 要件 |
|------|------|
| レスポンス時間 | 95%のリクエストが2秒以内 |
| スループット | 100 req/sec |
| 送信処理 | 1000通/分 |
| 一括送信 | 最大10,000件/バッチ |

---

## テスト仕様

### 単体テスト
```typescript
describe('Notification Send API', () => {
  test('POST /api/notifications/send - 即座通知送信', async () => {
    const notificationData = {
      notificationType: 'email',
      templateType: 'skill_expiry',
      recipients: [
        {
          userId: 'user_001',
          email: 'test@company-a.com',
          displayName: 'テストユーザー'
        }
      ],
      templateData: {
        userName: 'テストユーザー',
        certificationName: 'Test Certification',
        expiryDate: '2025-06-30',
        daysLeft: 30
      },
      priority: 'high'
    };
    
    const response = await request(app)
      .post('/api/notifications/send')
      .set('Authorization', `Bearer ${adminToken}`)
      .send(notificationData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.notificationId).toBeDefined();
    expect(response.body.data.totalRecipients).toBe(1);
    expect(response.body.data.status).toBe('queued');
  });
  
  test('POST /api/notifications/send/bulk - 一括通知送信', async () => {
    const bulkData = {
      notificationType: 'email',
      templateType: 'goal_reminder',
      recipientFilter: {
        department: '開発部',
        goalStatus: 'in_progress'
      },
      templateData: {
        quarterName: '2025年Q2',
        reminderMessage: 'テスト通知'
      },
      priority: 'medium'
    };
    
    const response = await request(app)
      .post('/api/notifications/send/bulk')
      .set('Authorization', `Bearer ${adminToken}`)
      .send(bulkData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.batchId).toBeDefined();
    expect(response.body.data.totalRecipients).toBeGreaterThan(0);
  });
  
  test('GET /api/notifications/send/{id}/status - 送信状況確認', async () => {
    const response = await request(app)
      .get('/api/notifications/send/notif_001/status')
      .set('Authorization', `Bearer ${adminToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.notificationId).toBe('notif_001');
    expect(response.body.data.status).toBeDefined();
    expect(response.body.data.deliveryStats).toBeDefined();
  });
  
  test('DELETE /api/notifications/send/{id} - 送信キャンセル', async () => {
    const response = await request(app)
      .delete('/api/notifications/send/notif_pending_001')
      .set('Authorization', `Bearer ${adminToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.status).toBe('cancelled');
    expect(response.body.data.cancelledCount).toBeGreaterThan(0);
  });
});
```

### 統合テスト
```typescript
describe('Notification Send Integration', () => {
  test('通知送信から配信まで', async () => {
    // 1. 通知送信
    const sendResponse = await sendNotification({
      notificationType: 'email',
      templateType: 'skill_expiry',
      recipients: [{ userId: 'user_001', email: 'test@test.com' }],
      templateData: { userName: 'Test', certificationName: 'Test Cert' }
    });
    
    expect(sendResponse.data.status).toBe('queued');
    
    // 2. 送信状況確認（処理完了まで待機）
    let status = 'queued';
    let attempts = 0;
    while (status !== 'completed' && attempts < 10) {
      await new Promise(resolve => setTimeout(resolve, 1000));
      const statusResponse = await getNotificationStatus(sendResponse.data.notificationId);
      status = statusResponse.data.status;
      attempts++;
    }
    
    expect(status).toBe('completed');
    expect(statusResponse.data.deliveryStats.sent).toBeGreaterThan(0);
  });
  
  test('一括送信のバッチ処理', async () => {
    // 大量受信者での一括送信
    const bulkResponse = await sendBulkNotification({
      notificationType: 'email',
      templateType: 'goal_reminder',
      recipientFilter: { department: '開発部' },
      batchSize: 10,
      intervalMinutes: 1
    });
    
    expect(bulkResponse.data.estimatedBatches).toBeGreaterThan(1);
    
    // バッチ処理の進行確認
    const statusResponse = await getBatchStatus(bulkResponse.data.batchId);
    expect(statusResponse.data.status).toMatch(/scheduled|in_progress|completed/);
  });
  
  test('権限制御確認', async () => {
    // 一般ユーザーで通知送信試行
    const response = await request(app)
      .post('/api/notifications/send')
      .set('Authorization', `Bearer ${userToken}`)
      .send({
        notificationType: 'email',
        templateType: 'skill_expiry',
        recipients: [{ userId: 'user_001', email: 'test@test.com' }]
      })
      .expect(403);
    
    expect(response.body.error.code).toBe('FORBIDDEN');
  });
});
```

---

## 実装メモ

### データベーススキーマ
```sql
CREATE TABLE notification_batches (
  id VARCHAR(50) PRIMARY KEY,
  tenant_id VARCHAR(50) NOT NULL,
  notification_type VARCHAR(50) NOT NULL,
  template_type VARCHAR(50) NOT NULL,
  total_recipients INTEGER NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'queued',
  priority VARCHAR(10) NOT NULL DEFAULT 'medium',
  template_data JSONB NOT NULL,
  custom_message TEXT,
  scheduled_at TIMESTAMP,
  created_by VARCHAR(50) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP,
  FOREIGN KEY (tenant_id) REFERENCES tenants(id),
  FOREIGN KEY (created_by) REFERENCES users(id)
);

CREATE TABLE notification_queue (
  id VARCHAR(50) PRIMARY KEY,
  batch_id VARCHAR(50),
  tenant_id VARCHAR(50) NOT NULL,
  user_id VARCHAR(50) NOT NULL,
  notification_type VARCHAR(50) NOT NULL,
  template_type VARCHAR(50) NOT NULL,
  recipient_email VARCHAR(255),
  recipient_name VARCHAR(255),
  template_data JSONB NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'queued',
  priority VARCHAR(10) NOT NULL DEFAULT 'medium',
  scheduled_at TIMESTAMP NOT NULL,
  sent_at TIMESTAMP,
  delivered_at TIMESTAMP,
  message_id VARCHAR(255),
  error_message TEXT,
  retry_count INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (batch_id) REFERENCES notification_batches(id),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_notification_batches_tenant_id ON notification_batches(tenant_id);
CREATE INDEX idx_notification_batches_status ON notification_batches(status);
CREATE INDEX idx_notification_queue_batch_id ON notification_queue(batch_id);
CREATE INDEX idx_notification_queue_status ON notification_queue(status);
CREATE INDEX idx_notification_queue_scheduled_at ON notification_queue(scheduled_at);
```

### Next.js実装例
```typescript
// pages/api/notifications/send/index.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { authenticateToken, requirePermission } from '@/lib/auth';
import { NotificationSendService } from '@/services/NotificationSendService';
import { validateNotificationRequest } from '@/lib/validation';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const user = await authenticateToken(req);
    await requirePermission(user, 'notification:send');
    
    const notificationService = new NotificationSendService();
    
    switch (req.method) {
      case 'POST':
        // バリデーション
        const validationResult = validateNotificationRequest(req.body);
        if (!validationResult.isValid) {
          return res.status(400).json({
            success: false,
            error: { code: 'VALIDATION_ERROR', message: validationResult.errors }
          });
        }
        
        // 通知送信
        const result = await notificationService.sendNotification(
          user.tenantId,
          user.id,
          req.body
        );
        
        return res.status(200).json({ success: true, data: result });
        
      default:
        return res.status(405).json({ success: false, error: 'Method not allowed' });
    }
  } catch (error) {
    console.error('Notification send error:', error);
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

### 通知送信サービス実装例
```typescript
// services/NotificationSendService.ts
export class NotificationSendService {
  async sendNotification(tenantId: string, createdBy: string, notificationData: any) {
    // 1. 通知バッチ作成
    const batch = await this.createNotificationBatch(tenantId, createdBy, notificationData);
    
    // 2. 受信者リスト処理
    const recipients = await this.processRecipients(tenantId, notificationData.recipients);
    
    // 3. 通知キューに追加
    const notifications = await this.queueNotifications(batch.id, recipients, notificationData);
    
    // 4. 送信処理開始（非同期）
    this.processNotificationQueue(batch.id);
    
    return {
      notificationId: batch.id,
      status: 'queued',
      totalRecipients: recipients.length,
      estimatedDeliveryTime: this.calculateDeliveryTime(recipients.length),
      notifications: notifications.map(n => ({
        id: n.id,
        userId: n.userId,
        email: n.recipientEmail,
        status: n.status,
        scheduledAt: n.scheduledAt
      })),
      createdAt: batch.createdAt
    };
  }
  
  async sendBulkNotification(tenantId: string, createdBy: string, bulkData: any) {
    // 1. 受信者フィルタリング
    const recipients = await this.filterRecipients(tenantId, bulkData.recipientFilter);
    
    // 2. バッチ作成
    const batch = await this.createNotificationBatch(tenantId, createdBy, {
      ...bulkData,
      recipients: recipients
    });
    
    // 3. バッチ処理スケジュール
    await this.scheduleBatchProcessing(batch.id, bulkData.batchSize, bulkData.intervalMinutes);
    
    return {
      batchId: batch.id,
      status: 'scheduled',
      totalRecipients: recipients.length,
      estimatedBatches: Math.ceil(recipients.length / (bulkData.batchSize || 50)),
      estimatedCompletionTime: this.calculateBatchCompletionTime(recipients.length, bulkData),
      recipientSummary: this.summarizeRecipients(recipients),
      scheduledAt: bulkData.sendAt || new Date(),
      createdAt: batch.createdAt
    };
  }
  
  private async processNotificationQueue(batchId: string) {
    const notifications = await this.notificationQueueRepository.findByBatchId(batchId);
    
    for (const notification of notifications) {
      try {
        // 通知送信実行
        const result = await this.deliverNotification(notification);
        
        // 送信結果更新
        await this.updateNotificationStatus(notification.id, {
          status: result.success ? 'sent' : 'failed',
          sentAt: new Date(),
          deliveredAt: result.deliveredAt,
          messageId: result.messageId,
          errorMessage: result.error
        });
        
      } catch (error) {
        // エラー処理・リトライ
        await this.handleNotificationError(notification, error);
      }
    }
    
    // バッチ完了処理
    await this.completeBatch(batchId);
  }
  
  private async deliverNotification(notification: any) {
    switch (notification.notificationType) {
      case 'email':
        return await this.emailService.send({
          to: notification.recipientEmail,
          subject: this.renderTemplate(notification.templateType, 'subject', notification.templateData),
          body: this.renderTemplate(notification.templateType, 'body', notification.templateData)
        });
        
      case 'teams':
        return await this.teamsService.send({
          webhookUrl: await this.getTeamsWebhook(notification.tenantId),
          message: this.renderTeamsMessage(notification.templateType, notification.templateData)
        });
        
      case 'lineWorks':
        return await this.lineWorksService.send({
          userId: notification.userId,
          message: this.renderTemplate(notification.templateType, 'lineWorks', notification.templateData)
        });
        
      case 'inApp':
        return await this.inAppService.send({
          userId: notification.userId,
          title: this.renderTemplate(notification.templateType, 'title', notification.templateData),
          message: this.render
