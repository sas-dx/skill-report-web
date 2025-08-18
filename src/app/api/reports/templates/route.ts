/**
 * 要求仕様ID: RPT.1-TMPL.1
 * 対応設計書: docs/design/api/specs/API定義書_API-061_レポート生成API.md
 * 実装内容: レポートテンプレート一覧取得API
 */

import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import { 
  createSuccessResponse, 
  createAuthErrorResponse, 
  createSystemErrorResponse 
} from '@/lib/api-utils';

/**
 * レポートテンプレート一覧取得API
 * @param request NextRequest
 * @returns NextResponse
 */
export async function GET(request: NextRequest) {
  try {
    // 認証チェック
    const authResult = await verifyAuth(request);
    if (!authResult.success) {
      return createAuthErrorResponse('認証が必要です');
    }

    if (!authResult.userId) {
      return createAuthErrorResponse('無効な認証トークンです');
    }

    // クエリパラメータの取得
    const { searchParams } = new URL(request.url);
    const category = searchParams.get('category');
    const format = searchParams.get('format');
    const language = searchParams.get('language') || 'ja';

    // 検索条件の構築
    const whereConditions: any = {
      is_active: true,
      is_deleted: false,
      language_code: language
    };

    if (category) {
      whereConditions.report_category = category;
    }

    if (format) {
      whereConditions.output_format = format;
    }

    // テナントID追加
    whereConditions.tenant_id = (authResult as any).tenantId || 'default-tenant';

    console.log('ReportTemplates GET API - Where conditions:', JSON.stringify(whereConditions, null, 2));

    // レポートテンプレート一覧を取得
    const reportTemplates = await prisma.reportTemplate.findMany({
      where: whereConditions,
      select: {
        id: true,
        template_key: true,
        template_name: true,
        report_category: true,
        output_format: true,
        language_code: true,
        parameters_schema: true,
        is_default: true,
        version: true,
        preview_image_url: true,
        created_at: true,
        updated_at: true
      },
      orderBy: [
        { report_category: 'asc' },
        { template_name: 'asc' }
      ]
    });

    console.log(`Found ${reportTemplates.length} report templates`);

    // レスポンスデータの整形
    const responseData = {
      templates: reportTemplates.map(template => ({
        id: template.id,
        templateKey: template.template_key,
        templateName: template.template_name,
        description: template.template_name, // 説明としてテンプレート名を使用
        category: template.report_category,
        format: template.output_format,
        language: template.language_code,
        parametersSchema: template.parameters_schema ? JSON.parse(template.parameters_schema) : null,
        isDefault: template.is_default,
        version: template.version,
        previewImageUrl: template.preview_image_url,
        createdAt: template.created_at?.toISOString(),
        updatedAt: template.updated_at?.toISOString()
      })),
      totalCount: reportTemplates.length,
      filters: {
        category,
        format,
        language
      }
    };

    return createSuccessResponse(responseData);

  } catch (error) {
    console.error('ReportTemplates GET error:', error);
    return createSystemErrorResponse(error as Error);
  }
}