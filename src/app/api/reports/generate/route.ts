/**
 * 要求仕様ID: RPT.1-GEN.1
 * 対応設計書: docs/design/api/specs/API定義書_API-061_レポート生成API.md
 * 実装内容: レポート生成リクエスト処理API
 */

import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import { createAuditLog } from '@/lib/auditLogger';
import { 
  createSuccessResponse, 
  createAuthErrorResponse, 
  createValidationErrorResponse,
  createNotFoundErrorResponse,
  createSystemErrorResponse 
} from '@/lib/api-utils';

/**
 * レポート生成リクエスト処理API
 * @param request NextRequest
 * @returns NextResponse
 */
export async function POST(request: NextRequest) {
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

    // リクエストボディの取得
    let body;
    try {
      body = await request.json();
    } catch (error) {
      return createValidationErrorResponse([
        { field: 'body', message: 'リクエストボディのJSONが不正です' }
      ]);
    }

    console.log('ReportGenerate POST API - Request body:', JSON.stringify(body, null, 2));

    // バリデーション
    const errors: Array<{ field: string; message: string }> = [];

    if (!body.templateId || typeof body.templateId !== 'string') {
      errors.push({ field: 'templateId', message: 'テンプレートIDは必須です' });
    }

    if (!body.reportTitle || typeof body.reportTitle !== 'string') {
      errors.push({ field: 'reportTitle', message: 'レポートタイトルは必須です' });
    }

    if (body.parameters && typeof body.parameters !== 'object') {
      errors.push({ field: 'parameters', message: 'パラメータはオブジェクト形式である必要があります' });
    }

    // 期間パラメータのバリデーション
    if (body.parameters) {
      if (body.parameters.startDate && !isValidDate(body.parameters.startDate)) {
        errors.push({ field: 'parameters.startDate', message: '開始日の形式が正しくありません' });
      }

      if (body.parameters.endDate && !isValidDate(body.parameters.endDate)) {
        errors.push({ field: 'parameters.endDate', message: '終了日の形式が正しくありません' });
      }

      if (body.parameters.startDate && body.parameters.endDate) {
        const startDate = new Date(body.parameters.startDate);
        const endDate = new Date(body.parameters.endDate);
        if (startDate > endDate) {
          errors.push({ field: 'parameters', message: '開始日は終了日より前である必要があります' });
        }
      }
    }

    if (errors.length > 0) {
      return createValidationErrorResponse(errors);
    }

    // テンプレートの存在確認
    const template = await prisma.reportTemplate.findFirst({
      where: {
        id: body.templateId,
        is_active: true,
        is_deleted: false,
        tenant_id: authResult.tenantId || 'default-tenant'
      }
    });

    if (!template) {
      return createNotFoundErrorResponse('レポートテンプレート', body.templateId);
    }

    // レポート生成レコードの作成
    const reportGenerationId = `report_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    // 生成ファイルのパス（実際のファイル生成は非同期で行われる）
    const fileName = `${body.reportTitle}_${new Date().toISOString().slice(0, 10)}.${template.output_format?.toLowerCase() || 'pdf'}`;
    const filePath = `/reports/generated/${currentEmployeeId}/${fileName}`;
    
    // 有効期限を30日後に設定
    const expiresAt = new Date();
    expiresAt.setDate(expiresAt.getDate() + 30);

    const newReportGeneration = await prisma.reportGeneration.create({
      data: {
        id: reportGenerationId,
        tenant_id: 'tenant_001', // 現在はシングルテナント
        template_id: body.templateId,
        requested_by: currentEmployeeId,
        report_title: body.reportTitle,
        report_category: template.report_category,
        output_format: template.output_format,
        generation_status: 'PENDING', // 初期状態は待機中
        parameters: body.parameters ? JSON.stringify(body.parameters) : null,
        file_path: filePath,
        file_size: null, // 生成後に更新
        download_count: 0,
        last_downloaded_at: null,
        requested_at: new Date(),
        started_at: null, // バッチ処理開始時に更新
        completed_at: null, // バッチ処理完了時に更新
        processing_time_ms: null, // バッチ処理完了時に更新
        error_message: null,
        error_details: null,
        expires_at: expiresAt
      }
    });

    // TODO: ここで実際の生成ジョブをキューに登録する
    // 現在は模擬的にジョブ登録をログ出力のみで代替
    console.log('Report generation job queued:', {
      reportId: reportGenerationId,
      templateId: body.templateId,
      requestedBy: currentEmployeeId,
      parameters: body.parameters
    });

    // AuditLog記録
    try {
      await createAuditLog({
        userId: currentEmployeeId,
        actionType: 'CREATE',
        targetTable: 'ReportGeneration',
        targetId: newReportGeneration.id,
        oldValues: {},
        newValues: {
          template_id: newReportGeneration.template_id,
          report_title: newReportGeneration.report_title,
          generation_status: newReportGeneration.generation_status,
          requested_by: newReportGeneration.requested_by
        },
        changeReason: 'レポート生成リクエスト',
        ipAddress: request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown',
        userAgent: request.headers.get('user-agent') || 'unknown'
      });
    } catch (auditError) {
      console.error('AuditLog記録エラー:', auditError);
    }

    const responseData = {
      reportId: newReportGeneration.id,
      templateId: newReportGeneration.template_id,
      reportTitle: newReportGeneration.report_title,
      category: newReportGeneration.report_category,
      format: newReportGeneration.output_format,
      status: newReportGeneration.generation_status,
      requestedAt: newReportGeneration.requested_at?.toISOString(),
      expiresAt: newReportGeneration.expires_at?.toISOString(),
      estimatedCompletionTime: '5-10分', // 固定値（実際の実装では動的に算出）
      message: 'レポート生成リクエストを受け付けました。生成が完了次第、通知いたします。'
    };

    return createSuccessResponse(responseData, 201);

  } catch (error) {
    console.error('ReportGenerate POST error:', error);
    return createSystemErrorResponse(error as Error);
  }
}

/**
 * 日付文字列の妥当性をチェック
 * @param dateString 日付文字列
 * @returns boolean
 */
function isValidDate(dateString: string): boolean {
  const date = new Date(dateString);
  return date instanceof Date && !isNaN(date.getTime());
}