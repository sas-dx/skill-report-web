/**
 * 要求仕様ID: TNT.1-MGMT
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_TNT_Admin_テナント管理画面.md
 * 実装内容: テナント管理API（一覧取得・作成）
 */

import { NextRequest, NextResponse } from 'next/server';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// テナント一覧取得
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const page = parseInt(searchParams.get('page') || '1');
    const limit = parseInt(searchParams.get('limit') || '20');
    const search = searchParams.get('search') || '';
    const status = searchParams.get('status') || '';

    const skip = (page - 1) * limit;

    // 検索条件の構築
    const where: any = {};

    if (search) {
      where.OR = [
        { tenant_name: { contains: search, mode: 'insensitive' } },
        { tenant_code: { contains: search, mode: 'insensitive' } },
        { domain_name: { contains: search, mode: 'insensitive' } },
      ];
    }

    if (status) {
      where.status = status;
    }

    // テナント一覧取得
    const [tenants, total] = await Promise.all([
      prisma.tenant.findMany({
        where,
        skip,
        take: limit,
        orderBy: { created_at: 'desc' },
      }),
      prisma.tenant.count({ where }),
    ]);

    const totalPages = Math.ceil(total / limit);

    return NextResponse.json({
      success: true,
      tenants,
      pagination: {
        page,
        limit,
        total,
        totalPages,
        hasNext: page < totalPages,
        hasPrev: page > 1,
      },
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('テナント一覧取得エラー:', error);
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'TENANT_LIST_ERROR',
          message: 'テナント一覧の取得に失敗しました',
        },
        timestamp: new Date().toISOString(),
      },
      { status: 500 }
    );
  }
}

// テナント作成
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const {
      tenant_code,
      tenant_name,
      tenant_short_name,
      domain_name,
      admin_email,
      max_users = 100,
      max_storage_gb = 10,
      subscription_plan = 'basic',
    } = body;

    console.log('テナント作成リクエスト:', {
      tenant_code,
      tenant_name,
      domain_name,
      admin_email,
    });

    // 入力値検証
    if (!tenant_code || !tenant_name || !domain_name || !admin_email) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message: '必須項目が不足しています',
            details: [
              { field: 'tenant_code', message: 'テナントコードは必須です' },
              { field: 'tenant_name', message: 'テナント名は必須です' },
              { field: 'domain_name', message: 'ドメイン名は必須です' },
              { field: 'admin_email', message: '管理者メールアドレスは必須です' },
            ],
          },
          timestamp: new Date().toISOString(),
        },
        { status: 400 }
      );
    }

    // データベース接続テスト
    try {
      await prisma.$connect();
      console.log('データベース接続成功');
    } catch (dbError) {
      console.error('データベース接続エラー:', dbError);
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'DATABASE_CONNECTION_ERROR',
            message: 'データベースに接続できません',
          },
          timestamp: new Date().toISOString(),
        },
        { status: 500 }
      );
    }

    // 重複チェック
    try {
      const existingTenant = await prisma.tenant.findFirst({
        where: {
          OR: [
            { tenant_code: tenant_code },
            { domain_name: domain_name },
          ],
        },
      });

      if (existingTenant) {
        return NextResponse.json(
          {
            success: false,
            error: {
              code: 'TENANT_DUPLICATE',
              message: 'テナントコードまたはドメイン名が既に使用されています',
            },
            timestamp: new Date().toISOString(),
          },
          { status: 409 }
        );
      }
    } catch (checkError) {
      console.error('重複チェックエラー:', checkError);
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'DUPLICATE_CHECK_ERROR',
            message: '重複チェックに失敗しました',
            details: checkError instanceof Error ? checkError.message : String(checkError),
          },
          timestamp: new Date().toISOString(),
        },
        { status: 500 }
      );
    }

    // テナント作成
    try {
      const tenant = await prisma.tenant.create({
        data: {
          tenant_id: `tenant_${Date.now()}`,
          tenant_code,
          tenant_name,
          tenant_short_name: tenant_short_name || tenant_name,
          domain_name,
          admin_email,
          max_users,
          max_storage_gb,
          subscription_plan,
          status: 'active',
          timezone: 'Asia/Tokyo',
          locale: 'ja-JP',
          currency_code: 'JPY',
          primary_color: '#3B82F6',
          secondary_color: '#6B7280',
        },
      });

      console.log('テナント作成成功:', tenant);

      return NextResponse.json(
        {
          success: true,
          data: { tenant },
          message: 'テナントが正常に作成されました',
          timestamp: new Date().toISOString(),
        },
        { status: 201 }
      );
    } catch (createError) {
      console.error('テナント作成エラー:', createError);
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'TENANT_CREATE_ERROR',
            message: 'テナントの作成に失敗しました',
            details: createError instanceof Error ? createError.message : String(createError),
          },
          timestamp: new Date().toISOString(),
        },
        { status: 500 }
      );
    }
  } catch (error) {
    console.error('テナント作成API全体エラー:', error);
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'INTERNAL_SERVER_ERROR',
          message: 'サーバー内部エラーが発生しました',
          details: error instanceof Error ? error.message : String(error),
        },
        timestamp: new Date().toISOString(),
      },
      { status: 500 }
    );
  } finally {
    await prisma.$disconnect();
  }
}
