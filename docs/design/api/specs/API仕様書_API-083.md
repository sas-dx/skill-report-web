# API仕様書: API-083 マスタデータ取得API

## 基本情報

| 項目 | 内容 |
|------|------|
| API ID | API-083 |
| API名称 | マスタデータ取得API |
| エンドポイント | /api/system/masters/{master_type} |
| 概要 | システムで使用するマスタデータの取得 |
| 利用画面 | SCR-ADMIN |
| 優先度 | 中 |
| 実装予定 | Week 8 |

---

## エンドポイント詳細

### 1. マスタデータ取得

#### リクエスト
```http
GET /api/system/masters/{master_type}
Authorization: Bearer {jwt_token}
```

#### パスパラメータ
| パラメータ | 型 | 必須 | 説明 |
|-----------|---|------|------|
| master_type | string | ○ | マスタデータタイプ |

#### クエリパラメータ
| パラメータ | 型 | 必須 | 説明 | デフォルト |
|-----------|---|------|------|----------|
| page | number | × | ページ番号 | 1 |
| limit | number | × | 1ページあたりの件数 | 100 |
| search | string | × | 検索キーワード | - |
| status | string | × | ステータス（active/inactive/all） | active |
| sort | string | × | ソート項目 | id |
| order | string | × | ソート順（asc/desc） | asc |

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
    "masterType": "organizations",
    "items": [
      {
        "id": "org_001",
        "code": "COMPANY-A",
        "name": "株式会社A",
        "displayName": "株式会社A",
        "description": "メインオフィス",
        "parentId": null,
        "level": 1,
        "sortOrder": 1,
        "status": "active",
        "attributes": {
          "address": "東京都千代田区...",
          "phone": "03-1234-5678",
          "email": "info@company-a.com"
        },
        "createdAt": "2025-05-30T20:54:00Z",
        "updatedAt": "2025-05-30T20:54:00Z"
      },
      {
        "id": "org_002",
        "code": "DEPT-DEV",
        "name": "開発部",
        "displayName": "開発部",
        "description": "システム開発部門",
        "parentId": "org_001",
        "level": 2,
        "sortOrder": 1,
        "status": "active",
        "attributes": {
          "manager": "田中太郎",
          "memberCount": 25
        },
        "createdAt": "2025-05-30T20:54:00Z",
        "updatedAt": "2025-05-30T20:54:00Z"
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 3,
      "totalItems": 250,
      "itemsPerPage": 100,
      "hasNext": true,
      "hasPrev": false
    },
    "metadata": {
      "lastUpdated": "2025-05-30T20:54:00Z",
      "version": "1.0.0",
      "schema": {
        "requiredFields": ["id", "code", "name", "status"],
        "optionalFields": ["description", "parentId", "level", "sortOrder", "attributes"]
      }
    }
  }
}
```

#### レスポンス（エラー時）
```json
{
  "success": false,
  "error": {
    "code": "MASTER_TYPE_NOT_FOUND",
    "message": "指定されたマスタタイプが見つかりません",
    "details": "master_type: invalid_type は対応していません",
    "supportedTypes": [
      "organizations",
      "departments",
      "job_types",
      "skill_categories",
      "skill_subcategories",
      "skill_items",
      "training_types",
      "certification_types",
      "notification_types",
      "user_roles"
    ]
  }
}
```

### 2. マスタデータ階層構造取得

#### リクエスト
```http
GET /api/system/masters/{master_type}/hierarchy
Authorization: Bearer {jwt_token}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "masterType": "skill_categories",
    "hierarchy": [
      {
        "id": "cat_001",
        "code": "TECH",
        "name": "技術スキル",
        "level": 1,
        "children": [
          {
            "id": "subcat_001",
            "code": "PROG",
            "name": "プログラミング",
            "level": 2,
            "children": [
              {
                "id": "item_001",
                "code": "JAVA",
                "name": "Java",
                "level": 3,
                "children": []
              },
              {
                "id": "item_002",
                "code": "PYTHON",
                "name": "Python",
                "level": 3,
                "children": []
              }
            ]
          }
        ]
      }
    ],
    "metadata": {
      "maxLevel": 3,
      "totalNodes": 156,
      "lastUpdated": "2025-05-30T20:54:00Z"
    }
  }
}
```

### 3. マスタデータ統計情報取得

#### リクエスト
```http
GET /api/system/masters/{master_type}/stats
Authorization: Bearer {jwt_token}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "masterType": "skill_items",
    "statistics": {
      "totalItems": 1250,
      "activeItems": 1180,
      "inactiveItems": 70,
      "byCategory": {
        "技術スキル": 650,
        "ビジネススキル": 380,
        "ヒューマンスキル": 220
      },
      "recentlyUpdated": 15,
      "lastUpdateDate": "2025-05-30T20:54:00Z"
    },
    "usage": {
      "mostUsedItems": [
        {
          "id": "item_001",
          "name": "Java",
          "usageCount": 450
        },
        {
          "id": "item_002",
          "name": "Python",
          "usageCount": 380
        }
      ],
      "leastUsedItems": [
        {
          "id": "item_999",
          "name": "COBOL",
          "usageCount": 2
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
| MASTER_TYPE_NOT_FOUND | 404 | マスタタイプが見つからない | 対応するマスタタイプを指定 |
| MASTER_TYPE_INVALID | 400 | マスタタイプが無効 | 有効なマスタタイプを指定 |
| INSUFFICIENT_PERMISSIONS | 403 | 権限不足 | システム管理者権限が必要 |
| TENANT_ACCESS_DENIED | 403 | テナントアクセス拒否 | 正しいテナントでアクセス |
| PAGINATION_INVALID | 400 | ページネーション設定が無効 | page, limitの値を確認 |
| SEARCH_QUERY_INVALID | 400 | 検索クエリが無効 | 検索キーワードの形式を確認 |
| SORT_PARAMETER_INVALID | 400 | ソートパラメータが無効 | 有効なソート項目を指定 |
| MASTER_DATA_CORRUPTED | 500 | マスタデータが破損 | システム管理者に連絡 |
| DATABASE_CONNECTION_ERROR | 500 | データベース接続エラー | システム管理者に連絡 |
| INTERNAL_SERVER_ERROR | 500 | サーバー内部エラー | システム管理者に連絡 |

---

## セキュリティ要件

### 認証・認可
- **認証**: JWT Bearer Token必須
- **権限**: システム管理者権限（admin）必須
- **テナント分離**: マルチテナント対応、テナント間データ分離

### データアクセス制御
- **読み取り専用**: マスタデータの参照のみ
- **監査ログ**: 全アクセスログを記録
- **レート制限**: 1分間に100リクエストまで

### データ保護
- **暗号化**: 通信はTLS1.3必須
- **データマスキング**: 機密情報の適切なマスキング
- **キャッシュ制御**: 適切なキャッシュヘッダー設定

---

## パフォーマンス要件

| 項目 | 要件 |
|------|------|
| レスポンス時間 | 95%のリクエストが500ms以内 |
| スループット | 200 req/sec |
| 同時接続数 | 100セッション |
| データ取得 | 10,000件まで1秒以内 |
| キャッシュ | 5分間キャッシュ |

---

## テスト仕様

### 単体テスト
```typescript
describe('Master Data Retrieval API', () => {
  test('GET /api/system/masters/organizations - 組織マスタ取得', async () => {
    const response = await request(app)
      .get('/api/system/masters/organizations')
      .set('Authorization', `Bearer ${adminToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.masterType).toBe('organizations');
    expect(response.body.data.items).toBeInstanceOf(Array);
    expect(response.body.data.pagination).toBeDefined();
  });
  
  test('GET /api/system/masters/invalid_type - 無効なマスタタイプ', async () => {
    const response = await request(app)
      .get('/api/system/masters/invalid_type')
      .set('Authorization', `Bearer ${adminToken}`)
      .expect(404);
    
    expect(response.body.success).toBe(false);
    expect(response.body.error.code).toBe('MASTER_TYPE_NOT_FOUND');
  });
  
  test('GET /api/system/masters/organizations - 権限不足', async () => {
    const response = await request(app)
      .get('/api/system/masters/organizations')
      .set('Authorization', `Bearer ${userToken}`)
      .expect(403);
    
    expect(response.body.success).toBe(false);
    expect(response.body.error.code).toBe('INSUFFICIENT_PERMISSIONS');
  });
  
  test('GET /api/system/masters/skill_categories/hierarchy - 階層構造取得', async () => {
    const response = await request(app)
      .get('/api/system/masters/skill_categories/hierarchy')
      .set('Authorization', `Bearer ${adminToken}`)
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.hierarchy).toBeInstanceOf(Array);
    expect(response.body.data.metadata.maxLevel).toBeDefined();
  });
});
```

### パフォーマンステスト
```typescript
describe('Master Data Performance', () => {
  test('大量データ取得パフォーマンス', async () => {
    const startTime = Date.now();
    
    const response = await request(app)
      .get('/api/system/masters/skill_items?limit=1000')
      .set('Authorization', `Bearer ${adminToken}`)
      .expect(200);
    
    const endTime = Date.now();
    const responseTime = endTime - startTime;
    
    expect(responseTime).toBeLessThan(1000); // 1秒以内
    expect(response.body.data.items.length).toBeLessThanOrEqual(1000);
  });
  
  test('検索機能パフォーマンス', async () => {
    const startTime = Date.now();
    
    const response = await request(app)
      .get('/api/system/masters/skill_items?search=Java&limit=100')
      .set('Authorization', `Bearer ${adminToken}`)
      .expect(200);
    
    const endTime = Date.now();
    const responseTime = endTime - startTime;
    
    expect(responseTime).toBeLessThan(500); // 500ms以内
  });
});
```

---

## 実装メモ

### データベーススキーマ
```sql
-- マスタデータ共通テーブル
CREATE TABLE master_data (
  id VARCHAR(50) PRIMARY KEY,
  master_type VARCHAR(50) NOT NULL,
  tenant_id VARCHAR(50) NOT NULL,
  code VARCHAR(100) NOT NULL,
  name VARCHAR(200) NOT NULL,
  display_name VARCHAR(200),
  description TEXT,
  parent_id VARCHAR(50),
  level INTEGER DEFAULT 1,
  sort_order INTEGER DEFAULT 0,
  status VARCHAR(20) DEFAULT 'active',
  attributes JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by VARCHAR(50),
  updated_by VARCHAR(50),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id),
  FOREIGN KEY (parent_id) REFERENCES master_data(id)
);

-- インデックス
CREATE INDEX idx_master_data_type_tenant ON master_data(master_type, tenant_id);
CREATE INDEX idx_master_data_parent ON master_data(parent_id);
CREATE INDEX idx_master_data_code ON master_data(code);
CREATE INDEX idx_master_data_status ON master_data(status);
CREATE INDEX idx_master_data_sort ON master_data(sort_order);

-- 全文検索用インデックス
CREATE INDEX idx_master_data_search ON master_data USING gin(to_tsvector('japanese', name || ' ' || COALESCE(description, '')));
```

### Next.js実装例
```typescript
// pages/api/system/masters/[master_type].ts
import { NextApiRequest, NextApiResponse } from 'next';
import { MasterDataService } from '@/services/MasterDataService';
import { AuthService } from '@/services/AuthService';
import { validateMasterType, validatePagination } from '@/utils/validation';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
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
    const { page = 1, limit = 100, search, status = 'active', sort = 'id', order = 'asc' } = req.query;
    
    // バリデーション
    if (!validateMasterType(master_type as string)) {
      return res.status(404).json({
        success: false,
        error: { 
          code: 'MASTER_TYPE_NOT_FOUND', 
          message: '指定されたマスタタイプが見つかりません',
          supportedTypes: MasterDataService.getSupportedTypes()
        }
      });
    }
    
    if (!validatePagination(Number(page), Number(limit))) {
      return res.status(400).json({
        success: false,
        error: { code: 'PAGINATION_INVALID', message: 'ページネーション設定が無効です' }
      });
    }
    
    const masterDataService = new MasterDataService();
    
    // マスタデータ取得
    const result = await masterDataService.getMasterData({
      masterType: master_type as string,
      tenantId: user.tenantId,
      page: Number(page),
      limit: Number(limit),
      search: search as string,
      status: status as string,
      sort: sort as string,
      order: order as 'asc' | 'desc'
    });
    
    return res.status(200).json({
      success: true,
      data: result
    });
    
  } catch (error) {
    console.error('Master data retrieval error:', error);
    return res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_SERVER_ERROR', message: 'サーバーエラーが発生しました' }
    });
  }
}
```

### サービス実装例
```typescript
// services/MasterDataService.ts
export class MasterDataService {
  private static readonly SUPPORTED_TYPES = [
    'organizations',
    'departments', 
    'job_types',
    'skill_categories',
    'skill_subcategories',
    'skill_items',
    'training_types',
    'certification_types',
    'notification_types',
    'user_roles'
  ];
  
  static getSupportedTypes(): string[] {
    return this.SUPPORTED_TYPES;
  }
  
  async getMasterData(params: {
    masterType: string;
    tenantId: string;
    page: number;
    limit: number;
    search?: string;
    status: string;
    sort: string;
    order: 'asc' | 'desc';
  }): Promise<MasterDataResponse> {
    const { masterType, tenantId, page, limit, search, status, sort, order } = params;
    
    let query = this.db
      .select()
      .from('master_data')
      .where('master_type', masterType)
      .andWhere('tenant_id', tenantId);
    
    // ステータスフィルタ
    if (status !== 'all') {
      query = query.andWhere('status', status);
    }
    
    // 検索フィルタ
    if (search) {
      query = query.andWhere(function() {
        this.where('name', 'ilike', `%${search}%`)
          .orWhere('code', 'ilike', `%${search}%`)
          .orWhere('description', 'ilike', `%${search}%`);
      });
    }
    
    // ソート
    query = query.orderBy(sort, order);
    
    // ページネーション
    const offset = (page - 1) * limit;
    const items = await query.limit(limit).offset(offset);
    
    // 総件数取得
    const totalQuery = this.db
      .count('* as count')
      .from('master_data')
      .where('master_type', masterType)
      .andWhere('tenant_id', tenantId);
    
    if (status !== 'all') {
      totalQuery.andWhere('status', status);
    }
    
    if (search) {
      totalQuery.andWhere(function() {
        this.where('name', 'ilike', `%${search}%`)
          .orWhere('code', 'ilike', `%${search}%`)
          .orWhere('description', 'ilike', `%${search}%`);
      });
    }
    
    const [{ count }] = await totalQuery;
    const totalItems = Number(count);
    const totalPages = Math.ceil(totalItems / limit);
    
    return {
      masterType,
      items,
      pagination: {
        currentPage: page,
        totalPages,
        totalItems,
        itemsPerPage: limit,
        hasNext: page < totalPages,
        hasPrev: page > 1
      },
      metadata: {
        lastUpdated: new Date().toISOString(),
        version: '1.0.0',
        schema: {
          requiredFields: ['id', 'code', 'name', 'status'],
          optionalFields: ['description', 'parentId', 'level', 'sortOrder', 'attributes']
        }
      }
    };
  }
  
  async getHierarchy(masterType: string, tenantId: string): Promise<HierarchyResponse> {
    const items = await this.db
      .select()
      .from('master_data')
      .where('master_type', masterType)
      .andWhere('tenant_id', tenantId)
      .andWhere('status', 'active')
      .orderBy('level')
      .orderBy('sort_order');
    
    const hierarchy = this.buildHierarchy(items);
    
    return {
      masterType,
      hierarchy,
      metadata: {
        maxLevel: Math.max(...items.map(item => item.level)),
        totalNodes: items.length,
        lastUpdated: new Date().toISOString()
      }
    };
  }
  
  private buildHierarchy(items: any[]): any[] {
    const itemMap = new Map();
    const rootItems: any[] = [];
    
    // アイテムマップ作成
    items.forEach(item => {
      itemMap.set(item.id, { ...item, children: [] });
    });
    
    // 階層構造構築
    items.forEach(item => {
      const node = itemMap.get(item.id);
      if (item.parent_id) {
        const parent = itemMap.get(item.parent_id);
        if (parent) {
          parent.children.push(node);
        }
      } else {
        rootItems.push(node);
      }
    });
    
    return rootItems;
  }
}
```

---

## 変更履歴

| 日付 | バージョン | 変更内容 | 変更者 |
|------|-----------|----------|--------|
| 2025-05-30 | 1.0.0 | 初版作成 | システムアーキテクト |
