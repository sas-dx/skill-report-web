# API仕様書: API-028 通知設定API

## 基本情報

| 項目 | 内容 |
|------|------|
| API ID | API-028 |
| API名称 | 通知設定API |
| エンドポイント | /api/tenants/{tenant_id}/notifications |
| 概要 | テナント別通知設定取得・更新 |
| 利用画面 | SCR-NOTIFY-ADMIN |
| 優先度 | 高 |
| 実装予定 | Week 3 |

---

## エンドポイント詳細

### 1. 通知設定取得

#### リクエスト
```http
GET /api/tenants/{tenant_id}/notifications
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### パスパラメータ
| パラメータ名 | 型 | 必須 | 説明 |
|-------------|---|------|------|
| tenant_id | string | ○ | テナントID |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "tenantId": "tenant_001",
    "tenantName": "株式会社A",
    "notificationSettings": {
      "email": {
        "enabled": true,
        "smtpConfig": {
          "host": "smtp.company-a.com",
          "port": 587,
          "secure": true,
          "username": "notifications@company-a.com",
          "fromAddress": "notifications@company-a.com",
          "fromName": "スキル管理システム"
        },
        "templates": {
          "skillExpiry": {
            "enabled": true,
            "subject": "【重要】資格期限のお知らせ",
            "template": "{{userName}}様\n\n以下の資格の期限が近づいています：\n{{certificationName}}\n期限日：{{expiryDate}}\n\n更新手続きをお忘れなく。",
            "daysBeforeExpiry": [30, 7, 1]
          },
          "goalReminder": {
            "enabled": true,
            "subject": "目標進捗確認のお知らせ",
            "template": "{{userName}}様\n\n四半期の目標進捗確認の時期です。\n現在の達成率：{{progressRate}}%\n\n進捗を更新してください。",
            "reminderFrequency": "quarterly"
          },
          "systemAlert": {
            "enabled": true,
            "subject": "【システム】重要なお知らせ",
            "template": "{{userName}}様\n\nシステムからの重要なお知らせです：\n{{alertMessage}}\n\n詳細は管理者にお問い合わせください。"
          }
        }
      },
      "teams": {
        "enabled": true,
        "webhookUrl": "https://company-a.webhook.office.com/webhookb2/...",
        "channelName": "#skill-notifications",
        "templates": {
          "skillExpiry": {
            "enabled": true,
            "messageFormat": "adaptive_card",
            "template": {
              "type": "AdaptiveCard",
              "version": "1.3",
              "body": [
                {
                  "type": "TextBlock",
                  "text": "資格期限通知",
                  "weight": "Bolder",
                  "size": "Medium"
                },
                {
                  "type": "TextBlock",
                  "text": "{{userName}}さんの{{certificationName}}が{{daysLeft}}日後に期限切れになります。",
                  "wrap": true
                }
              ],
              "actions": [
                {
                  "type": "Action.OpenUrl",
                  "title": "詳細確認",
                  "url": "{{skillPageUrl}}"
                }
              ]
            }
          },
          "goalReminder": {
            "enabled": true,
            "messageFormat": "simple",
            "template": "📊 **目標進捗確認**\n{{userName}}さん、四半期の目標進捗確認をお願いします。\n現在の達成率：{{progressRate}}%"
          }
        }
      },
      "lineWorks": {
        "enabled": false,
        "botId": "",
        "apiToken": "",
        "templates": {
          "skillExpiry": {
            "enabled": false,
            "template": "{{userName}}さん\n{{certificationName}}の期限が{{daysLeft}}日後です。\n更新をお忘れなく！"
          }
        }
      },
      "inApp": {
        "enabled": true,
        "retentionDays": 30,
        "categories": {
          "skillExpiry": {
            "enabled": true,
            "priority": "high",
            "autoRead": false
          },
          "goalReminder": {
            "enabled": true,
            "priority": "medium",
            "autoRead": false
          },
          "systemAlert": {
            "enabled": true,
            "priority": "high",
            "autoRead": false
          }
        }
      }
    },
    "schedules": {
      "skillExpiryCheck": {
        "enabled": true,
        "frequency": "daily",
        "time": "09:00",
        "timezone": "Asia/Tokyo"
      },
      "goalReminderCheck": {
        "enabled": true,
        "frequency": "monthly",
        "dayOfMonth": 1,
        "time": "10:00",
        "timezone": "Asia/Tokyo"
      },
      "weeklyDigest": {
        "enabled": false,
        "frequency": "weekly",
        "dayOfWeek": "monday",
        "time": "08:00",
        "timezone": "Asia/Tokyo"
      }
    },
    "lastUpdated": "2025-05-30T20:56:00Z",
    "updatedBy": "admin@company-a.com"
  }
}
```

### 2. 通知設定更新

#### リクエスト
```http
PUT /api/tenants/{tenant_id}/notifications
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "notificationSettings": {
    "email": {
      "enabled": true,
      "smtpConfig": {
        "host": "smtp.company-a.com",
        "port": 587,
        "secure": true,
        "username": "notifications@company-a.com",
        "password": "encrypted_password",
        "fromAddress": "notifications@company-a.com",
        "fromName": "スキル管理システム"
      },
      "templates": {
        "skillExpiry": {
          "enabled": true,
          "subject": "【重要】資格期限のお知らせ",
          "template": "{{userName}}様\n\n以下の資格の期限が近づいています：\n{{certificationName}}\n期限日：{{expiryDate}}\n\n更新手続きをお忘れなく。",
          "daysBeforeExpiry": [30, 7, 1]
        }
      }
    },
    "teams": {
      "enabled": true,
      "webhookUrl": "https://company-a.webhook.office.com/webhookb2/...",
      "channelName": "#skill-notifications"
    }
  },
  "schedules": {
    "skillExpiryCheck": {
      "enabled": true,
      "frequency": "daily",
      "time": "09:00",
      "timezone": "Asia/Tokyo"
    }
  }
}
```

#### バリデーションルール
| フィールド | ルール |
|-----------|--------|
| email.smtpConfig.host | 必須（email.enabled=trueの場合）、有効なホスト名 |
| email.smtpConfig.port | 必須、1-65535の整数 |
| email.smtpConfig.fromAddress | 必須、有効なメールアドレス形式 |
| teams.webhookUrl | 必須（teams.enabled=trueの場合）、有効なURL形式 |
| schedules.*.time | 必須、HH:MM形式 |
| schedules.*.timezone | 必須、有効なタイムゾーン |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "message": "通知設定が正常に更新されました",
    "tenantId": "tenant_001",
    "updatedAt": "2025-05-30T21:00:00Z",
    "validationResults": {
      "email": {
        "smtpConnection": "success",
        "testEmailSent": true
      },
      "teams": {
        "webhookConnection": "success",
        "testMessageSent": true
      }
    }
  }
}
```

### 3. 通知テスト送信

#### リクエスト
```http
POST /api/tenants/{tenant_id}/notifications/test
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "notificationType": "email",
  "templateType": "skillExpiry",
  "testData": {
    "userName": "テストユーザー",
    "certificationName": "AWS Solutions Architect",
    "expiryDate": "2025-06-30",
    "daysLeft": 30
  },
  "recipients": ["admin@company-a.com"]
}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "message": "テスト通知を送信しました",
    "notificationType": "email",
    "recipients": ["admin@company-a.com"],
    "sentAt": "2025-05-30T21:05:00Z",
    "messageId": "test_msg_001"
  }
}
```

### 4. 通知履歴取得

#### リクエスト
```http
GET /api/tenants/{tenant_id}/notifications/history
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### クエリパラメータ
| パラメータ名 | 型 | 必須 | 説明 | 例 |
|-------------|---|------|------|---|
| page | number | × | ページ番号（デフォルト: 1） | 1 |
| limit | number | × | 取得件数（デフォルト: 50） | 50 |
| type | string | × | 通知タイプフィルタ | email, teams, lineWorks |
| status | string | × | 送信ステータスフィルタ | success, failed, pending |
| dateFrom | string | × | 開始日（YYYY-MM-DD） | 2025-05-01 |
| dateTo | string | × | 終了日（YYYY-MM-DD） | 2025-05-31 |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "notifications": [
      {
        "id": "notif_001",
        "type": "email",
        "templateType": "skillExpiry",
        "recipient": "user@company-a.com",
        "subject": "【重要】資格期限のお知らせ",
        "status": "success",
        "sentAt": "2025-05-30T09:00:00Z",
        "deliveredAt": "2025-05-30T09:00:15Z",
        "messageId": "msg_001",
        "errorMessage": null
      },
      {
        "id": "notif_002",
        "type": "teams",
        "templateType": "goalReminder",
        "recipient": "#skill-notifications",
        "subject": null,
        "status": "success",
        "sentAt": "2025-05-30T10:00:00Z",
        "deliveredAt": "2025-05-30T10:00:05Z",
        "messageId": "teams_msg_001",
        "errorMessage": null
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 50,
      "total": 125,
      "totalPages": 3
    },
    "statistics": {
      "totalSent": 125,
      "successRate": 98.4,
      "byType": {
        "email": { "sent": 80, "success": 79, "failed": 1 },
        "teams": { "sent": 35, "success": 35, "failed": 0 },
        "lineWorks": { "sent": 10, "success": 9, "failed": 1 }
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
| FORBIDDEN | 403 | 権限不足 | テナント管理者権限が必要 |
| TENANT_NOT_FOUND | 404 | テナントが見つからない | 正しいテナントIDを指定 |
| TENANT_MISMATCH | 403 | テナント不一致 | 自分のテナントの設定のみ変更可能 |
| VALIDATION_ERROR | 400 | バリデーションエラー | リクエストデータを確認 |
| SMTP_CONNECTION_ERROR | 400 | SMTP接続エラー | SMTP設定を確認 |
| WEBHOOK_CONNECTION_ERROR | 400 | Webhook接続エラー | WebhookURLを確認 |
| TEMPLATE_PARSE_ERROR | 400 | テンプレート解析エラー | テンプレート構文を確認 |
| NOTIFICATION_SEND_ERROR | 500 | 通知送信エラー | 設定を確認して再試行 |
| INTERNAL_SERVER_ERROR | 500 | サーバー内部エラー | システム管理者に連絡 |

---

## セキュリティ要件

### 認証・認可
- **認証**: JWT Bearer Token必須
- **権限**: テナント管理者（tenant_admin）権限必須
- **テナント分離**: 自分のテナントの設定のみアクセス可能

### データ保護
- **機密情報暗号化**: SMTP パスワード、API トークンはAES-256で暗号化
- **監査ログ**: 設定変更を監査ログに記録
- **アクセス制御**: テナント間の設定情報完全分離

---

## パフォーマンス要件

| 項目 | 要件 |
|------|------|
| レスポンス時間 | 95%のリクエストが1秒以内 |
| スループット | 50 req/sec |
| 通知送信 | 1000通/分 |
| 設定更新 | リアルタイム反映 |

---

## テスト仕様

### 単体テスト
```typescript
describe('Notification Settings API', () => {
  test('GET /api/tenants/{tenant_id}/notifications - 設定取得', async () => {
    const response = await request(app)
      .get('/api/tenants/tenant_001/notifications')
      .set('Authorization', `Bearer ${tenantAdminToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.tenantId).toBe('tenant_001');
    expect(response.body.data.notificationSettings).toBeDefined();
  });
  
  test('PUT /api/tenants/{tenant_id}/notifications - 設定更新', async () => {
    const updateData = {
      notificationSettings: {
        email: {
          enabled: true,
          smtpConfig: {
            host: 'smtp.test.com',
            port: 587,
            secure: true,
            username: 'test@test.com',
            password: 'testpass',
            fromAddress: 'test@test.com',
            fromName: 'Test System'
          }
        }
      }
    };
    
    const response = await request(app)
      .put('/api/tenants/tenant_001/notifications')
      .set('Authorization', `Bearer ${tenantAdminToken}`)
      .send(updateData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.validationResults.email.smtpConnection).toBe('success');
  });
  
  test('POST /api/tenants/{tenant_id}/notifications/test - テスト送信', async () => {
    const testData = {
      notificationType: 'email',
      templateType: 'skillExpiry',
      testData: {
        userName: 'テストユーザー',
        certificationName: 'Test Certification',
        expiryDate: '2025-06-30',
        daysLeft: 30
      },
      recipients: ['test@test.com']
    };
    
    const response = await request(app)
      .post('/api/tenants/tenant_001/notifications/test')
      .set('Authorization', `Bearer ${tenantAdminToken}`)
      .send(testData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.messageId).toBeDefined();
  });
});
```

### 統合テスト
```typescript
describe('Notification Settings Integration', () => {
  test('設定更新から通知送信まで', async () => {
    // 1. 通知設定更新
    await updateNotificationSettings('tenant_001', emailConfig);
    
    // 2. テスト通知送信
    const testResult = await sendTestNotification('tenant_001', 'email');
    expect(testResult.success).toBe(true);
    
    // 3. 通知履歴確認
    const history = await getNotificationHistory('tenant_001');
    expect(history.data.notifications).toContainEqual(
      expect.objectContaining({
        type: 'email',
        status: 'success'
      })
    );
  });
  
  test('テナント分離確認', async () => {
    const tenantAToken = await loginAsTenantAdmin('company-a');
    const tenantBToken = await loginAsTenantAdmin('company-b');
    
    // テナントAの管理者でテナントBの設定にアクセス
    const response = await request(app)
      .get('/api/tenants/tenant_b/notifications')
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
CREATE TABLE tenant_notification_settings (
  id VARCHAR(50) PRIMARY KEY,
  tenant_id VARCHAR(50) NOT NULL,
  settings JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by VARCHAR(50) NOT NULL,
  FOREIGN KEY (tenant_id) REFERENCES tenants(id),
  FOREIGN KEY (updated_by) REFERENCES users(id),
  UNIQUE(tenant_id)
);

CREATE TABLE notification_history (
  id VARCHAR(50) PRIMARY KEY,
  tenant_id VARCHAR(50) NOT NULL,
  notification_type VARCHAR(50) NOT NULL,
  template_type VARCHAR(50) NOT NULL,
  recipient VARCHAR(255) NOT NULL,
  subject VARCHAR(255),
  status VARCHAR(20) NOT NULL,
  message_id VARCHAR(255),
  error_message TEXT,
  sent_at TIMESTAMP NOT NULL,
  delivered_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

CREATE INDEX idx_tenant_notification_settings_tenant_id ON tenant_notification_settings(tenant_id);
CREATE INDEX idx_notification_history_tenant_id ON notification_history(tenant_id);
CREATE INDEX idx_notification_history_sent_at ON notification_history(sent_at);
CREATE INDEX idx_notification_history_status ON notification_history(status);
```

### Next.js実装例
```typescript
// pages/api/tenants/[tenant_id]/notifications.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { authenticateToken, requireTenantAdmin } from '@/lib/auth';
import { NotificationService } from '@/services/NotificationService';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const { tenant_id } = req.query;
    
    // 認証・認可チェック
    const user = await authenticateToken(req);
    await requireTenantAdmin(user, tenant_id as string);
    
    const notificationService = new NotificationService();
    
    switch (req.method) {
      case 'GET':
        const settings = await notificationService.getSettings(tenant_id as string);
        return res.status(200).json({ success: true, data: settings });
        
      case 'PUT':
        const updatedSettings = await notificationService.updateSettings(
          tenant_id as string,
          req.body,
          user.id
        );
        return res.status(200).json({ success: true, data: updatedSettings });
        
      default:
        return res.status(405).json({ success: false, error: 'Method not allowed' });
    }
  } catch (error) {
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

### 通知サービス実装例
```typescript
// services/NotificationService.ts
export class NotificationService {
  async updateSettings(tenantId: string, settings: any, updatedBy: string) {
    // バリデーション
    await this.validateSettings(settings);
    
    // 機密情報暗号化
    const encryptedSettings = await this.encryptSensitiveData(settings);
    
    // 設定保存
    const savedSettings = await this.settingsRepository.upsert({
      tenantId,
      settings: encryptedSettings,
      updatedBy
    });
    
    // 接続テスト
    const validationResults = await this.validateConnections(settings);
    
    // 監査ログ記録
    await this.auditLogger.log({
      action: 'notification_settings_updated',
      tenantId,
      userId: updatedBy,
      details: { settingsKeys: Object.keys(settings) }
    });
    
    return {
      message: '通知設定が正常に更新されました',
      tenantId,
      updatedAt: savedSettings.updatedAt,
      validationResults
    };
  }
  
  private async validateConnections(settings: any) {
    const results = {};
    
    // SMTP接続テスト
    if (settings.notificationSettings?.email?.enabled) {
      try {
        await this.emailService.testConnection(settings.notificationSettings.email.smtpConfig);
        results.email = { smtpConnection: 'success', testEmailSent: true };
      } catch (error) {
        results.email = { smtpConnection: 'failed', error: error.message };
      }
    }
    
    // Teams Webhook テスト
    if (settings.notificationSettings?.teams?.enabled) {
      try {
        await this.teamsService.testWebhook(settings.notificationSettings.teams.webhookUrl);
        results.teams = { webhookConnection: 'success', testMessageSent: true };
      } catch (error) {
        results.teams = { webhookConnection: 'failed', error: error.message };
      }
    }
    
    return results;
  }
}
```

---

## 変更履歴

| 日付 | バージョン | 変更内容 | 変更者 |
|------|-----------|----------|--------|
| 2025-05-30 | 1.0.0 | 初版作成 | システムアーキテクト |
