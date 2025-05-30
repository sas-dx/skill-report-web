# API仕様書: API-084 マスタデータ更新API

## 基本情報

| 項目 | 内容 |
|------|------|
| API ID | API-084 |
| API名称 | マスタデータ更新API |
| エンドポイント | /api/system/masters/{master_type} |
| 概要 | システムで使用するマスタデータの一括更新・追加・削除 |
| 利用画面 | SCR-ADMIN |
| 優先度 | 中 |
| 実装予定 | Week 8 |

---

## エンドポイント詳細

### 1. マスタデータ一括更新

#### リクエスト
```http
PUT /api/system/masters/{master_type}
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### パスパラメータ
| パラメータ | 型 | 必須 | 説明 |
|-----------|---|------|------|
| master_type | string | ○ | マスタデータタイプ |

#### リクエストボディ
```json
{
  "operation": "bulk_update",
  "items": [
    {
      "action": "create",
      "data": {
        "code": "NEW-DEPT-001",
        "name": "新規部署",
        "displayName": "新規部署",
        "description": "新しく設立された部署",
        "parentId": "org_001",
        "level": 2,
        "sortOrder": 10,
        "status": "active",
        "attributes": {
          "manager": "佐藤次郎",
          "memberCount": 5
        }
      }
    },
    {
      "action": "update",
      "id": "dept_002",
      "data": {
        "name": "更新された部署名",
        "description": "部署の説明を更新",
        "attributes": {
          "manager": "田中太郎",
          "memberCount": 30
        }
      }
    },
    {
      "action": "delete",
      "id": "dept_003"
    }
  ],
  "options": {
    "validateOnly": false,
    "skipDuplicates": true,
    "preserveHierarchy": true
  }
}
```

#### バリデーションルール
| フィールド | ルール |
|-----------|--------|
| operation | 必須、"bulk_update"固定 |
| items | 必須、配列、最大1000件 |
| items[].action | 必須、"create"/"update"/"delete" |
| items[].data.code | create時必須、3-100文字、英数字とハイフン |
| items[].data.name | create/update時必須、1-200文字 |
| items[].id | update/delete時必須 |

#### 対応マスタタイプ
| master_type | 説明 | 対応する要求仕様ID |
|-------------|------|------------------|
| organizations | 組織マスタ | PLT.1-WEB.1 |
| departments | 部署マスタ | PLT.1-WEB.1 |
| job_types | 職種マスタ | PRO.1-BASE.1 |
| skill_categories | スキルカテゴリマスタ | SKL.1-HIER.1 |
| skill_subcategories | スキルサブカテゴリマスタ | SKL.1-HIER.1 |
| skill_items | スキル項目マスタ | SKL.1-HIER.1 |
| training_types | 研修種別マスタ | TRN.1-MGMT.1 |
| certification_types | 資格種別マスタ | TRN.1-MGMT.1 |
| notification_types | 通知種別マスタ | PLT.1-WEB.1 |
| user_roles | ユーザー役割マスタ | ACC.1-AUTH.1 |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "masterType": "departments",
    "operation": "bulk_update",
    "summary": {
      "totalItems": 3,
      "created": 1,
      "updated": 1,
      "deleted": 1,
      "skipped": 0,
      "errors": 0
    },
    "results": [
      {
        "action": "create",
        "status": "success",
        "data": {
          "id": "dept_new_001",
          "code": "NEW-DEPT-001",
          "name": "新規部署",
          "createdAt": "2025-05-30T21:00:00Z"
        }
      },
      {
        "action": "update",
        "id": "dept_002",
        "status": "success",
        "data": {
          "id": "dept_002",
          "name": "更新された部署名",
          "updatedAt": "2025-05-30T21:00:00Z"
        }
      },
      {
        "action": "delete",
        "id": "dept_003",
        "status": "success",
        "data": {
          "id": "dept_003",
          "deletedAt": "2025-05-30T21:00:00Z"
        }
      }
    ],
    "metadata": {
      "processedAt": "2025-05-30T21:00:00Z",
      "processedBy": "admin_001",
      "version": "1.0.0"
    }
  }
}
```

#### レスポンス（部分エラー時）
```json
{
  "success": true,
  "data": {
    "masterType": "departments",
    "operation": "bulk_update",
    "summary": {
      "totalItems": 3,
      "created": 1,
      "updated": 0,
      "deleted": 1,
      "skipped": 0,
      "errors": 1
    },
    "results": [
      {
        "action": "create",
        "status": "success",
        "data": {
          "id": "dept_new_001",
          "code": "NEW-DEPT-001",
          "name": "新規部署"
        }
      },
      {
        "action": "update",
        "id": "dept_002",
        "status": "error",
        "error": {
          "code": "ITEM_NOT_FOUND",
          "message": "更新対象のアイテムが見つかりません",
          "details": "ID: dept_002 は存在しません"
        }
      },
      {
        "action": "delete",
        "id": "dept_003",
        "status": "success",
        "data": {
          "id": "dept_003",
          "deletedAt": "2025-05-30T21:00:00Z"
        }
      }
    ],
    "warnings": [
      {
        "code": "PARTIAL_SUCCESS",
        "message": "一部の操作でエラーが発生しました",
        "affectedItems": ["dept_002"]
      }
    ]
  }
}
```

### 2. マスタデータバリデーション

#### リクエスト
```http
POST /api/system/masters/{master_type}/validate
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "operation": "bulk_update",
  "items": [
    {
      "action": "create",
      "data": {
        "code": "TEST-DEPT",
        "name": "テスト部署",
        "parentId": "org_001"
      }
    }
  ]
}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "validation": {
      "isValid": true,
      "totalItems": 1,
      "validItems": 1,
      "invalidItems": 0
    },
    "results": [
      {
        "action": "create",
        "status": "valid",
        "data": {
          "code": "TEST-DEPT",
          "name": "テスト部署"
        }
      }
    ],
    "warnings": [],
    "errors": []
  }
}
```

### 3. マスタデータ単体操作

#### 単体作成
```http
POST /api/system/masters/{master_type}/items
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "code": "SINGLE-ITEM",
  "name": "単体作成アイテム",
  "displayName": "単体作成アイテム",
  "description": "単体で作成されるアイテム",
  "parentId": "parent_001",
  "level": 2,
  "sortOrder": 5,
  "status": "active",
  "attributes": {
    "customField1": "値1",
    "customField2": "値2"
  }
}
```

#### 単体更新
```http
PUT /api/system/masters/{master_type}/items/{item_id}
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### 単体削除
```http
DELETE /api/system/masters/{master_type}/items/{item_id}
Authorization: Bearer {jwt_token}
```

### 4. マスタデータ並び順更新

#### リクエスト
```http
PUT /api/system/masters/{master_type}/sort-order
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "items": [
    {
      "id": "item_001",
      "sortOrder": 1
    },
    {
      "id": "item_002",
      "sortOrder": 2
    },
    {
      "id": "item_003",
      "sortOrder": 3
    }
  ]
}
```

---

## エラーコード一覧

| エラーコード | HTTPステータス | 説明 | 対処法 |
|-------------|---------------|------|--------|
| MASTER_TYPE_NOT_FOUND | 404 | マスタタイプが見つからない | 対応するマスタタイプを指定 |
| MASTER_TYPE_READONLY | 403 | 読み取り専用マスタタイプ | 更新不可のマスタタイプ |
| INSUFFICIENT_PERMISSIONS | 403 | 権限不足 | システム管理者権限が必要 |
| TENANT_ACCESS_DENIED | 403 | テナントアクセス拒否 | 正しいテナントでアクセス |
| BULK_LIMIT_EXCEEDED | 400 | 一括処理件数超過 | 1000件以下に分割 |
| VALIDATION_ERROR | 400 | バリデーションエラー | リクエストデータを確認 |
| DUPLICATE_CODE | 409 | コード重複 | 一意のコードを指定 |
| ITEM_NOT_FOUND | 404 | アイテムが見つからない | 存在するIDを指定 |
| HIERARCHY_VIOLATION | 400 | 階層構造違反 | 正しい親子関係を設定 |
| CIRCULAR_REFERENCE | 400 | 循環参照エラー | 親子関係の循環を解消 |
| ITEM_IN_USE | 409 | アイテムが使用中 | 使用中のアイテムは削除不可 |
| CONCURRENT_MODIFICATION | 409 | 同時更新エラー | 最新データで再試行 |
| DATABASE_CONSTRAINT_ERROR | 400 | データベース制約エラー | 制約条件を確認 |
| INTERNAL_SERVER_ERROR | 500 | サーバー内部エラー | システム管理者に連絡 |

---

## セキュリティ要件

### 認証・認可
- **認証**: JWT Bearer Token必須
- **権限**: システム管理者権限（admin）必須
- **操作権限**: マスタタイプ別の細かい権限制御

### データ整合性
- **トランザクション**: 一括操作は全てトランザクション内で実行
- **ロック制御**: 同時更新防止のための楽観的ロック
- **バックアップ**: 更新前データの自動バックアップ

### 監査・ログ
- **操作ログ**: 全ての更新操作を詳細記録
- **変更履歴**: 変更前後の値を保存
- **承認フロー**: 重要なマスタは承認後に反映

---

## パフォーマンス要件

| 項目 | 要件 |
|------|------|
| レスポンス時間 | 95%のリクエストが2秒以内 |
| 一括処理 | 1000件まで10秒以内 |
| 同時更新 | 10セッション |
| トランザクション | 30秒以内でタイムアウト |
| ロールバック | 5秒以内 |

---

## テスト仕様

### 単体テスト
```typescript
describe('Master Data Update API', () => {
  test('PUT /api/system/masters/departments - 一括更新成功', async () => {
    const updateData = {
      operation: 'bulk_update',
      items: [
        {
          action: 'create',
          data: {
            code: 'TEST-DEPT',
            name: 'テスト部署',
            parentId: 'org_001'
          }
        }
      ]
    };
    
    const response = await request(app)
      .put('/api/system/masters/departments')
      .set('Authorization', `Bearer ${adminToken}`)
      .send(updateData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.summary.created).toBe(1);
    expect(response.body.data.results[0].status).toBe('success');
  });
  
  test('PUT /api/system/masters/departments - バリデーションエラー', async () => {
    const invalidData = {
      operation: 'bulk_update',
      items: [
        {
          action: 'create',
          data: {
            code: '', // 空のコード
            name: 'テスト部署'
          }
        }
      ]
    };
    
    const response = await request(app)
      .put('/api/system/masters/departments')
      .set('Authorization', `Bearer ${adminToken}`)
      .send(invalidData)
      .expect(400);
    
    expect(response.body.success).toBe(false);
    expect(response.body.error.code).toBe('VALIDATION_ERROR');
  });
  
  test('PUT /api/system/masters/departments - 権限不足', async () => {
    const updateData = {
      operation: 'bulk_update',
      items: []
    };
    
    const response = await request(app)
      .put('/api/system/masters/departments')
      .set('Authorization', `Bearer ${userToken}`)
      .send(updateData)
      .expect(403);
    
    expect(response.body.success).toBe(false);
    expect(response.body.error.code).toBe('INSUFFICIENT_PERMISSIONS');
  });
  
  test('POST /api/system/masters/departments/validate - バリデーション', async () => {
    const validateData = {
      operation: 'bulk_update',
      items: [
        {
          action: 'create',
          data: {
            code: 'VALID-DEPT',
            name: '有効な部署'
          }
        }
      ]
    };
    
    const response = await request(app)
      .post('/api/system/masters/departments/validate')
      .set('Authorization', `Bearer ${adminToken}`)
      .send(validateData)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.validation.isValid).toBe(true);
  });
});
```

### 統合テスト
```typescript
describe('Master Data Integration', () => {
  test('階層構造の整合性テスト', async () => {
    // 親カテゴリ作成
    const parentData = {
      operation: 'bulk_update',
      items: [
        {
          action: 'create',
          data: {
            code: 'PARENT-CAT',
            name: '親カテゴリ',
            level: 1
          }
        }
      ]
    };
    
    const parentResponse = await request(app)
      .put('/api/system/masters/skill_categories')
      .set('Authorization', `Bearer ${adminToken}`)
      .send(parentData)
      .expect(200);
    
    const parentId = parentResponse.body.data.results[0].data.id;
    
    // 子カテゴリ作成
    const childData = {
      operation: 'bulk_update',
      items: [
        {
          action: 'create',
          data: {
            code: 'CHILD-CAT',
            name: '子カテゴリ',
            parentId: parentId,
            level: 2
          }
        }
      ]
    };
    
    const childResponse = await request(app)
      .put('/api/system/masters/skill_categories')
      .set('Authorization', `Bearer ${adminToken}`)
      .send(childData)
      .expect(200);
    
    expect(childResponse.body.success).toBe(true);
    
    // 階層構造確認
    const hierarchyResponse = await request(app)
      .get('/api/system/masters/skill_categories/hierarchy')
      .set('Authorization', `Bearer ${adminToken}`)
      .expect(200);
    
    const parentNode = hierarchyResponse.body.data.hierarchy.find(
      (node: any) => node.id === parentId
    );
    expect(parentNode.children).toHaveLength(1);
    expect(parentNode.children[0].code).toBe('CHILD-CAT');
  });
  
  test('同時更新競合テスト', async () => {
    const updateData = {
      operation: 'bulk_update',
      items: [
        {
          action: 'update',
          id: 'existing_item',
          data: {
            name: '更新されたアイテム'
          }
        }
      ]
    };
    
    // 同時に2つのリクエストを送信
    const [response1, response2] = await Promise.all([
      request(app)
        .put('/api/system/masters/departments')
        .set('Authorization', `Bearer ${adminToken}`)
        .send(updateData),
      request(app)
        .put('/api/system/masters/departments')
        .set('Authorization', `Bearer ${adminToken}`)
        .send(updateData)
    ]);
    
    // 一方は成功、もう一方は競合エラー
    const successCount = [response1, response2].filter(r => r.status === 200).length;
    const conflictCount = [response1, response2].filter(r => r.status === 409).length;
    
    expect(successCount).toBe(1);
    expect(conflictCount).toBe(1);
  });
});
```

---

## 実装メモ

### データベーススキーマ
```sql
-- マスタデータ変更履歴テーブル
CREATE TABLE master_data_history (
  id VARCHAR(50) PRIMARY KEY,
  master_data_id VARCHAR(50) NOT NULL,
  operation VARCHAR(20) NOT NULL, -- create/update/delete
  old_data JSONB,
  new_data JSONB,
  changed_by VARCHAR(50) NOT NULL,
  changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  tenant_id VARCHAR(50) NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data(id),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

-- バージョン管理用カラム追加
ALTER TABLE master_data ADD COLUMN version INTEGER DEFAULT 1;
ALTER TABLE master_data ADD COLUMN last_modified_by VARCHAR(50);

-- インデックス
CREATE INDEX idx_master_data_history_data_id ON master_data_history(master_data_id);
CREATE INDEX idx_master_data_history_changed_at ON master_data_history(changed_at);
CREATE INDEX idx_master_data_version ON master_data(version);
```

### Next.js実装例
```typescript
// pages/api/system/masters/[master_type].ts
import { NextApiRequest, NextApiResponse } from 'next';
import { MasterDataUpdateService } from '@/services/MasterDataUpdateService';
import { AuthService } from '@/services/AuthService';
import { validateBulkUpdateRequest } from '@/utils/validation';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'PUT') {
    return res.status(405).json({ success: false, error: 'Method not allowed' });
  }
  
  try {
    // 認証チェック
    const authService = new AuthService();
    const user = await authService.validateToken(req);
    
    if (!user || !user.permissions.includes('system:admin')) {
      return res.status(403).json({
        success: false,
        error: { code: 'INSUFFICIENT_PERMISSIONS', message: 'システム管理者権限が必要です' }
      });
    }
    
    const { master_type } = req.query;
    const requestData = req.body;
    
    // バリデーション
    const validationResult = validateBulkUpdateRequest(master_type as string, requestData);
    if (!validationResult.isValid) {
      return res.status(400).json({
        success: false,
        error: { 
          code: 'VALIDATION_ERROR', 
          message: 'リクエストデータが無効です',
          details: validationResult.errors
        }
      });
    }
    
    const updateService = new MasterDataUpdateService();
    
    // 一括更新実行
    const result = await updateService.bulkUpdate({
      masterType: master_type as string,
      tenantId: user.tenantId,
      userId: user.id,
      operation: requestData.operation,
      items: requestData.items,
      options: requestData.options || {}
    });
    
    return res.status(200).json({
      success: true,
      data: result
    });
    
  } catch (error) {
    console.error('Master data update error:', error);
    
    if (error.code === 'BULK_LIMIT_EXCEEDED') {
      return res.status(400).json({
        success: false,
        error: { code: error.code, message: error.message }
      });
    }
    
    if (error.code === 'CONCURRENT_MODIFICATION') {
      return res.status(409).json({
        success: false,
        error: { code: error.code, message: error.message }
      });
    }
    
    return res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_SERVER_ERROR', message: 'サーバーエラーが発生しました' }
    });
  }
}
```

### サービス実装例
```typescript
// services/MasterDataUpdateService.ts
export class MasterDataUpdateService {
  async bulkUpdate(params: {
    masterType: string;
    tenantId: string;
    userId: string;
    operation: string;
    items: any[];
    options: any;
  }): Promise<BulkUpdateResponse> {
    const { masterType, tenantId, userId, items, options } = params;
    
    // 件数制限チェック
    if (items.length > 1000) {
      throw new Error('BULK_LIMIT_EXCEEDED');
    }
    
    const results: any[] = [];
    const summary = {
      totalItems: items.length,
      created: 0,
      updated: 0,
      deleted: 0,
      skipped: 0,
      errors: 0
    };
    
    // トランザクション開始
    const trx = await this.db.transaction();
    
    try {
      for (const item of items) {
        try {
          let result;
          
          switch (item.action) {
            case 'create':
              result = await this.createItem(trx, {
                masterType,
                tenantId,
                userId,
                data: item.data
              });
              summary.created++;
              break;
              
            case 'update':
              result = await this.updateItem(trx, {
                masterType,
                tenantId,
                userId,
                id: item.id,
                data: item.data
              });
              summary.updated++;
              break;
              
            case 'delete':
              result = await this.deleteItem(trx, {
                masterType,
                tenantId,
                userId,
                id: item.id
              });
              summary.deleted++;
              break;
              
            default:
              throw new Error(`Invalid action: ${item.action}`);
          }
          
          results.push({
            action: item.action,
            id: item.id,
            status: 'success',
            data: result
          });
          
        } catch (error) {
          summary.errors++;
          results.push({
            action: item.action,
            id: item.id,
            status: 'error',
            error: {
              code: error.code || 'UNKNOWN_ERROR',
              message: error.message,
              details: error.details
            }
          });
          
          // エラー時の処理方針
          if (!options.continueOnError) {
            throw error;
          }
        }
      }
      
      // コミット
      await trx.commit();
      
      return {
        masterType,
        operation: 'bulk_update',
        summary,
        results,
        metadata: {
          processedAt: new Date().toISOString(),
          processedBy: userId,
          version: '1.0.0'
        }
      };
      
    } catch (error) {
      // ロールバック
      await trx.rollback();
      throw error;
    }
  }
  
  private async createItem(trx: any, params: {
    masterType: string;
    tenantId: string;
    userId: string;
    data: any;
  }): Promise<any> {
    const { masterType, tenantId, userId, data } = params;
    
    // 重複チェック
    const existing = await trx
      .select('id')
      .from('master_data')
      .where('master_type', masterType)
      .andWhere('tenant_id', tenantId)
      .andWhere('code', data.code)
      .first();
    
    if (existing) {
      throw new Error('DUPLICATE_CODE');
    }
    
    // 新規作成
    const newItem = {
      id: generateId(),
      master_type: masterType,
      tenant_id: tenantId,
      code: data.code,
      name: data.name,
      display_name: data.displayName || data.name,
      description: data.description,
      parent_id: data.parentId,
      level: data.level || 1,
      sort_order: data.sortOrder || 0,
      status: data.status || 'active',
      attributes: data.attributes ? JSON.stringify(data.attributes) : null,
      version: 1,
      created_by: userId,
      updated_by: userId,
      created_at: new Date(),
      updated_at: new Date()
    };
    
    await trx('master_data').insert(newItem);
    
    // 履歴記録
    await this.recordHistory(trx, {
      masterDataId: newItem.id,
      operation: 'create',
      oldData: null,
      newData: newItem,
      changedBy: userId,
      tenantId
    });
    
    return newItem;
  }
  
  private async updateItem(trx: any, params: {
    masterType: string;
    tenantId: string;
    userId: string;
    id: string;
    data: any;
  }): Promise<any> {
    const { masterType, tenantId, userId, id, data } = params;
    
    // 既存データ取得
    const existing = await trx
      .select('*')
      .from('master_data')
      .where('id', id)
      .andWhere('master_type', masterType)
      .andWhere('tenant_id', tenantId)
      .first();
    
    if (!existing) {
      throw new Error('ITEM_NOT_FOUND');
    }
    
    // 楽観的ロックチェック
    if (data.version && data.version !== existing.version) {
      throw new Error('CONCURRENT_MODIFICATION');
    }
    
    // 更新データ準備
    const updateData: any = {
      version: existing.version + 1,
      updated_by: userId,
      updated_at: new Date()
    };
    
    if (data.name !== undefined) updateData.name = data.name;
    if (data.displayName !== undefined) updateData.display_name = data.displayName;
    if (data.description !== undefined) updateData.description = data.description;
    if (data.parentId !== undefined) updateData.parent_id = data.parentId;
    if (data.level !== undefined) updateData.level = data.level;
    if (data.sortOrder !== undefined) updateData.sort_order = data.sortOrder;
    if (data.status !== undefined) updateData.status = data.status;
    if (data.attributes !== undefined) {
      updateData.attributes = data.attributes ? JSON.stringify(data.attributes) : null;
    }
    
    // 更新実行
    await trx('master_data')
      .where('id', id)
      .update(updateData);
    
    // 履歴記録
    await this.recordHistory(trx, {
      masterDataId: id,
      operation: 'update',
      oldData: existing,
      newData: { ...existing, ...updateData },
      changedBy: userId,
      tenantId
    });
    
    return { ...existing, ...updateData };
  }
  
  private async deleteItem(trx: any, params: {
    masterType: string;
    tenantId: string;
    userId: string;
    id: string;
  }): Promise<any> {
    const { masterType, tenantId, userId, id } = params;
    
    // 既存データ取得
    const existing = await trx
      .select('*')
      .from('master_data')
      .where('id', id)
      .andWhere('master_type', masterType)
      .andWhere('tenant_id', tenantId)
      .first();
    
    if (!existing) {
      throw new Error('ITEM_NOT_FOUND');
    }
    
    // 使用中チェック
    const isInUse = await this.checkItemInUse(trx, id, masterType);
    if (isInUse) {
      throw new Error('ITEM_IN_USE');
    }
    
    // 子要素チェック
    const hasChildren = await trx
      .select('id')
      .from('master_data')
      .where('parent_id', id)
      .first();
    
    if (hasChildren) {
      throw new Error('HIERARCHY_VIOLATION');
    }
    
    // 削除実行（論理削除）
    await trx('master_data')
      .where('id', id)
      .update({
        status: 'deleted',
        updated_by: userId,
        updated_at: new Date()
      });
    
    // 履歴記録
    await this.recordHistory(trx, {
      masterDataId: id,
      operation: 'delete',
      oldData: existing,
      newData: null,
      changedBy: userId,
      tenantId
    });
    
    return {
      id,
      deletedAt: new Date().toISOString()
    };
  }
  
  private async recordHistory(trx: any, params: {
    masterDataId: string;
    operation: string;
    oldData: any;
    newData: any;
    changedBy: string;
    tenantId: string;
  }): Promise<void> {
    const { masterDataId, operation, oldData, newData, changedBy, tenantId } = params;
    
    await trx('master_data_history').insert({
      id: generateId(),
      master_data_id: masterDataId,
      operation,
      old_data: oldData ? JSON.stringify(oldData) : null,
      new_data: newData ? JSON.stringify(newData) : null,
      changed_by: changedBy,
      changed_at: new Date(),
      tenant_id: tenantId
    });
  }
  
  private async checkItemInUse(trx: any, itemId: string, masterType: string): Promise<boolean> {
    // マスタタイプに応じて使用中チェック
    switch (masterType) {
      case 'organizations':
      case 'departments':
        const userCount = await trx
          .count('* as count')
          .from('users')
          .where('organization_id', itemId)
          .orWhere('department_id', itemId)
          .first();
        return Number(userCount.count) > 0;
        
      case 'skill_categories':
      case 'skill_subcategories':
      case 'skill_items':
        const skillCount = await trx
          .count('* as count')
          .from('user_skills')
          .where('skill_id', itemId)
          .first();
        return Number(skillCount.count) > 0;
        
      case 'job_types':
        const jobCount = await trx
          .count('* as count')
          .from('users')
          .where('job_type_id', itemId)
          .first();
        return Number(jobCount.count) > 0;
        
      default:
        return false;
    }
  }
}

function generateId(): string {
  return 'id_' + Math.random().toString(36).substr(2, 9) + Date.now().toString(36);
}
```

---

## 変更履歴

| 日付 | バージョン | 変更内容 | 変更者 |
|------|-----------|----------|--------|
| 2025-05-30 | 1.0.0 | 初版作成 | システムアーキテクト |
