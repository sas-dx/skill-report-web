/**
 * 要求仕様ID: RPT.1-HIST.1
 * 対応設計書: docs/design/api/specs/API定義書_API-062_レポート取得API.md
 * 実装内容: ユーザーのレポート生成履歴取得API
 */

import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import { 
  createSuccessResponse, 
  createAuthErrorResponse, 
  createValidationErrorResponse,
  createSystemErrorResponse 
} from '@/lib/api-utils';

/**
 * ユーザーのレポート生成履歴取得API
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

    const currentEmployeeId = authResult.employeeId || authResult.userId;

    // クエリパラメータの取得
    const { searchParams } = new URL(request.url);
    const page = parseInt(searchParams.get('page') || '1', 10);
    const limit = parseInt(searchParams.get('limit') || '20', 10);
    const status = searchParams.get('status');
    const category = searchParams.get('category');
    const format = searchParams.get('format');
    const startDate = searchParams.get('startDate');
    const endDate = searchParams.get('endDate');

    // バリデーション
    const errors: Array<{ field: string; message: string }> = [];

    if (page < 1) {
      errors.push({ field: 'page', message: 'ページ番号は1以上である必要があります' });
    }

    if (limit < 1 || limit > 100) {
      errors.push({ field: 'limit', message: '取得件数は1〜100の範囲で指定してください' });
    }

    if (errors.length > 0) {
      return createValidationErrorResponse(errors);
    }

    // 検索条件の構築
    const whereConditions: any = {
      requested_by: currentEmployeeId,
      is_deleted: false
    };

    if (status) {
      whereConditions.generation_status = status;
    }

    if (category) {
      whereConditions.report_category = category;
    }

    if (format) {
      whereConditions.output_format = format;
    }

    if (startDate || endDate) {
      whereConditions.requested_at = {};
      if (startDate) {
        whereConditions.requested_at.gte = new Date(startDate);
      }
      if (endDate) {
        whereConditions.requested_at.lte = new Date(endDate + 'T23:59:59.999Z');
      }
    }

    // テナントID追加
    whereConditions.tenant_id = (authResult as any).tenantId || 'default-tenant';

    console.log('ReportHistory GET API - Where conditions:', JSON.stringify(whereConditions, null, 2));

    // ページネーション計算
    const skip = (page - 1) * limit;

    // 総件数とレポート履歴を並行取得
    const [totalCount, reportHistory] = await Promise.all([
      prisma.reportGeneration.count({
        where: whereConditions
      }),
      prisma.reportGeneration.findMany({
        where: whereConditions,
        select: {
          id: true,
          template_id: true,
          report_title: true,
          report_category: true,
          output_format: true,
          generation_status: true,
          parameters: true,
          file_path: true,
          file_size: true,
          download_count: true,
          last_downloaded_at: true,
          requested_at: true,
          started_at: true,
          completed_at: true,
          processing_time_ms: true,
          error_message: true,
          expires_at: true,
          created_at: true,
          updated_at: true
        },
        orderBy: {
          requested_at: 'desc'
        },
        skip,
        take: limit
      })
    ]);

    console.log(`Found ${totalCount} total reports, returning ${reportHistory.length} for page ${page}`);

    // ページネーション情報の計算
    const totalPages = Math.ceil(totalCount / limit);
    const hasNextPage = page < totalPages;
    const hasPreviousPage = page > 1;

    // レスポンスデータの整形
    const responseData = {
      reports: reportHistory.map(report => ({
        id: report.id,
        templateId: report.template_id,
        title: report.report_title,
        fileName: report.file_path ? report.file_path.split('/').pop() : null,
        category: report.report_category,
        format: report.output_format,
        status: report.generation_status,
        parameters: report.parameters ? JSON.parse(report.parameters) : null,
        fileSize: report.file_size,
        downloadCount: report.download_count || 0,
        lastDownloadedAt: report.last_downloaded_at?.toISOString(),
        requestedAt: report.requested_at?.toISOString(),
        startedAt: report.started_at?.toISOString(),
        completedAt: report.completed_at?.toISOString(),
        processingTimeMs: report.processing_time_ms,
        errorMessage: report.error_message,
        expiresAt: report.expires_at?.toISOString(),
        createdAt: report.created_at?.toISOString(),
        updatedAt: report.updated_at?.toISOString()
      })),
      pagination: {
        currentPage: page,
        totalPages,
        totalCount,
        limit,
        hasNextPage,
        hasPreviousPage
      },
      filters: {
        status,
        category,
        format,
        startDate,
        endDate
      }
    };

    return createSuccessResponse(responseData);

  } catch (error) {
    console.error('ReportHistory GET error:', error);
    return createSystemErrorResponse(error as Error);
  }
}