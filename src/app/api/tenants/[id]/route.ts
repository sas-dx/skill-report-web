/**
 * 要求仕様ID: TNT.1-MGMT
 * 対応設計書: docs/design/api/specs/API定義書_API-025_テナント管理API.md
 * 実装内容: 個別テナント操作API（取得・更新・削除）
 */

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { createAuditLog } from '@/lib/auditLogger';

// 個別テナント取得
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const tenantId = params.id;

    const tenant = await prisma.tenant.findUnique({
      where: {
        tenant_id: tenantId
      }
    });

    if (!tenant) {
      return NextResponse.json({
        success: false,
        error: 'テナントが見つかりません'
      }, { status: 404 });
    }

    return NextResponse.json({
      success: true,
      tenant
    });

  } catch (error) {
    console.error('テナント取得エラー:', error);
    return NextResponse.json({
      success: false,
      error: 'テナント取得に失敗しました'
    }, { status: 500 });
  }
}

// テナント更新
export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const tenantId = params.id;
    const body = await request.json();

    const {
      tenant_code,
      tenant_name,
      tenant_short_name,
      tenant_type,
      domain_name,
      admin_email,
      max_users,
      subscription_plan
    } = body;

    // 必須フィールドの検証
    if (!tenant_code || !tenant_name || !tenant_type || !domain_name || !admin_email) {
      return NextResponse.json({
        success: false,
        error: '必須フィールドが不足しています'
      }, { status: 400 });
    }

    // 既存テナントの確認
    const existingTenant = await prisma.tenant.findUnique({
      where: { tenant_id: tenantId }
    });

    if (!existingTenant) {
      return NextResponse.json({
        success: false,
        error: 'テナントが見つかりません'
      }, { status: 404 });
    }

    // テナントコードの重複チェック（自分以外）
    if (tenant_code !== existingTenant.tenant_code) {
      const duplicateCode = await prisma.tenant.findFirst({
        where: {
          tenant_code,
          tenant_id: { not: tenantId }
        }
      });

      if (duplicateCode) {
        return NextResponse.json({
          success: false,
          error: 'このテナントコードは既に使用されています'
        }, { status: 400 });
      }
    }

    // テナント更新
    const updatedTenant = await prisma.tenant.update({
      where: { tenant_id: tenantId },
      data: {
        tenant_code,
        tenant_name,
        tenant_short_name,
        tenant_type,
        domain_name,
        admin_email,
        max_users: max_users || 100,
        subscription_plan: subscription_plan || 'standard',
        updated_at: new Date()
      }
    });

    // 監査ログ記録
    await createAuditLog({
      userId: 'system', // TODO: 実際のユーザーIDに置き換え
      actionType: 'UPDATE',
      targetTable: 'tenant',
      targetId: tenantId,
      oldValues: existingTenant,
      newValues: body,
      changeReason: 'テナント情報更新',
      ipAddress: request.headers.get('x-forwarded-for') || 'unknown',
      userAgent: request.headers.get('user-agent') || 'unknown'
    });

    return NextResponse.json({
      success: true,
      tenant: updatedTenant,
      message: 'テナントが正常に更新されました'
    });

  } catch (error) {
    console.error('テナント更新エラー:', error);
    return NextResponse.json({
      success: false,
      error: 'テナント更新に失敗しました'
    }, { status: 500 });
  }
}

// テナント削除
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const tenantId = params.id;

    // 既存テナントの確認
    const existingTenant = await prisma.tenant.findUnique({
      where: { tenant_id: tenantId }
    });

    if (!existingTenant) {
      return NextResponse.json({
        success: false,
        error: 'テナントが見つかりません'
      }, { status: 404 });
    }

    // テナント削除（論理削除）
    const deletedTenant = await prisma.tenant.update({
      where: { tenant_id: tenantId },
      data: {
        status: 'deleted',
        updated_at: new Date()
      }
    });

    // 監査ログ記録
    await createAuditLog({
      userId: 'system', // TODO: 実際のユーザーIDに置き換え
      actionType: 'DELETE',
      targetTable: 'tenant',
      targetId: tenantId,
      oldValues: existingTenant,
      newValues: { status: 'deleted' },
      changeReason: 'テナント削除（論理削除）',
      ipAddress: request.headers.get('x-forwarded-for') || 'unknown',
      userAgent: request.headers.get('user-agent') || 'unknown'
    });

    return NextResponse.json({
      success: true,
      message: 'テナントが正常に削除されました'
    });

  } catch (error) {
    console.error('テナント削除エラー:', error);
    return NextResponse.json({
      success: false,
      error: 'テナント削除に失敗しました'
    }, { status: 500 });
  }
}
