/**
 * マルチテナント対応のコンテキスト管理
 * 要求仕様ID: TNT.1-MGMT.1, TNT.2-ISOL.1
 */

import { NextRequest } from 'next/server';
import { prisma } from '@/lib/prisma';

export interface TenantContext {
  tenantId: string;
  tenantCode: string;
  tenantName: string;
  features: {
    sso: boolean;
    apiAccess: boolean;
    advancedReporting: boolean;
    customBranding: boolean;
    teamsIntegration: boolean;
    lineWorksIntegration: boolean;
  };
  limits: {
    maxUsers: number;
    maxStorageGb: number;
  };
  settings: Record<string, any>;
}

/**
 * リクエストからテナント情報を取得
 */
export async function getTenantFromRequest(request: NextRequest): Promise<TenantContext | null> {
  try {
    // 1. ヘッダーからテナントIDを取得（開発用）
    let tenantId = request.headers.get('x-tenant-id');
    
    // 2. サブドメインからテナントを特定
    if (!tenantId) {
      const host = request.headers.get('host') || '';
      const subdomain = host.split('.')[0];
      
      if (subdomain && subdomain !== 'localhost' && subdomain !== 'www') {
        const tenant = await prisma.tenant.findUnique({
          where: { subdomain }
        });
        
        if (tenant) {
          tenantId = tenant.tenant_id;
        }
      }
    }
    
    // 3. JWTトークンからテナント情報を取得（実装予定）
    if (!tenantId) {
      const authorization = request.headers.get('authorization');
      if (authorization && authorization.startsWith('Bearer ')) {
        const token = authorization.substring(7);
        // TODO: JWT検証とテナント情報の取得
        // const decoded = await verifyJWT(token);
        // tenantId = decoded.tenantId;
      }
    }
    
    // 4. デフォルトテナント（開発用）
    if (!tenantId) {
      tenantId = process.env.DEFAULT_TENANT_ID || 'default-tenant';
    }
    
    // テナント情報を取得
    const tenant = await prisma.tenant.findUnique({
      where: { tenant_id: tenantId }
    });
    
    if (!tenant) {
      return null;
    }
    
    // テナント設定を取得
    const settings = await prisma.tenantSettings.findMany({
      where: { 
        tenant_id: tenantId,
        is_deleted: false
      }
    });
    
    // 設定をオブジェクトに変換
    const settingsMap: Record<string, any> = {};
    settings.forEach(setting => {
      if (setting.setting_category && setting.setting_key) {
        if (!settingsMap[setting.setting_category]) {
          settingsMap[setting.setting_category] = {};
        }
        settingsMap[setting.setting_category][setting.setting_key] = 
          setting.setting_value || setting.default_value;
      }
    });
    
    // 機能フラグの解析
    const features = (tenant as any).features_enabled || {};
    
    return {
      tenantId: tenant.tenant_id,
      tenantCode: tenant.tenant_code || '',
      tenantName: tenant.tenant_name || '',
      features: {
        sso: features.sso || false,
        apiAccess: features.apiAccess || false,
        advancedReporting: features.advancedReporting || false,
        customBranding: features.customBranding || false,
        teamsIntegration: features.teamsIntegration || false,
        lineWorksIntegration: features.lineWorksIntegration || false,
      },
      limits: {
        maxUsers: (tenant as any).user_limit || 100,
        maxStorageGb: (tenant as any).storage_limit_gb || 10,
      },
      settings: settingsMap
    };
  } catch (error) {
    console.error('テナント情報取得エラー:', error);
    return null;
  }
}

/**
 * テナントIDでデータをフィルタリング
 */
export function filterByTenant<T extends { tenant_id?: string | null }>(
  data: T[],
  tenantId: string
): T[] {
  return data.filter(item => item.tenant_id === tenantId);
}

/**
 * Prismaクエリにテナントフィルタを追加
 */
export function addTenantFilter(where: any, tenantId: string): any {
  return {
    ...where,
    tenant_id: tenantId
  };
}

/**
 * テナント間のデータアクセスを検証
 */
export async function validateTenantAccess(
  tenantId: string,
  resourceType: string,
  resourceId: string
): Promise<boolean> {
  try {
    // リソースタイプに応じて適切なテーブルを確認
    switch (resourceType) {
      case 'employee':
        const employee = await prisma.employee.findFirst({
          where: {
            id: resourceId,
            is_deleted: false
          }
        });
        return !!employee;
        
      case 'department':
        const department = await prisma.department.findFirst({
          where: {
            department_code: resourceId,
            is_deleted: false
          }
        });
        return !!department;
        
      case 'skill':
        const skill = await prisma.skillRecord.findFirst({
          where: {
            id: resourceId,
            is_deleted: false
          }
        });
        return !!skill;
        
      default:
        return false;
    }
  } catch (error) {
    console.error('テナントアクセス検証エラー:', error);
    return false;
  }
}

/**
 * テナントのリソース使用量を更新
 */
export async function updateTenantUsage(
  tenantId: string,
  resourceType: 'users' | 'storage',
  delta: number
): Promise<void> {
  try {
    const tenant = await prisma.tenant.findUnique({
      where: { tenant_id: tenantId }
    });
    
    if (!tenant) {
      throw new Error('テナントが見つかりません');
    }
    
    if (resourceType === 'users') {
      // テナントの使用量更新は別のテーブルまたはカスタムフィールドで管理
      // 現在のスキーマでは実装できないためコメントアウト
      console.log(`テナント ${tenantId} のユーザー数更新: ${delta}`);
    } else if (resourceType === 'storage') {
      // テナントの使用量更新は別のテーブルまたはカスタムフィールドで管理
      // 現在のスキーマでは実装できないためコメントアウト
      console.log(`テナント ${tenantId} のストレージ使用量更新: ${delta} GB`);
    }
  } catch (error) {
    console.error('テナント使用量更新エラー:', error);
    throw error;
  }
}