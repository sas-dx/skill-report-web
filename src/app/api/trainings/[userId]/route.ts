/**
 * 要求仕様ID: TRN.1-ATT.1
 * 対応設計書: docs/design/api/specs/API定義書_API-051_研修記録取得API.md
 * 実装内容: ユーザーIDに基づいて研修記録を取得するAPI
 */
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { createErrorResponse, createSuccessResponse } from '@/lib/api-utils';
import { randomUUID } from 'crypto';

/**
 * 研修記録取得API
 * 
 * @param request - リクエスト
 * @param params - URLパラメータ（ユーザーID）
 * @returns 研修記録一覧
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { userId: string } }
) {
  try {
    const userId = params.userId;
    
    // 認証チェック（実際の実装では認証ミドルウェアを使用）
    // この部分は将来的に認証機能と連携
    
    // ユーザーの存在確認
    const employee = await prisma.employee.findUnique({
      where: { id: userId }
    });
    
    if (!employee) {
      return createErrorResponse(
        'USER_NOT_FOUND',
        '指定されたユーザーが見つかりません',
        `Employee ID: ${userId}`,
        404
      );
    }
    
    // クエリパラメータの取得
    const searchParams = request.nextUrl.searchParams;
    const year = searchParams.get('year');
    const category = searchParams.get('category');
    const status = searchParams.get('status');
    const limit = parseInt(searchParams.get('limit') || '50', 10);
    const offset = parseInt(searchParams.get('offset') || '0', 10);
    
    // 検索条件の構築
    const whereCondition: any = {
      employee_id: userId,
      is_deleted: false
    };
    
    // 年フィルター
    if (year) {
      const startDate = new Date(`${year}-01-01T00:00:00Z`);
      const endDate = new Date(`${parseInt(year) + 1}-01-01T00:00:00Z`);
      
      whereCondition.start_date = {
        gte: startDate,
        lt: endDate
      };
    }
    
    // カテゴリフィルター
    if (category) {
      whereCondition.training_category = category;
    }
    
    // ステータスフィルター
    if (status) {
      whereCondition.attendance_status = status;
    }
    
    // 研修記録の取得
    const trainings = await prisma.trainingHistory.findMany({
      where: whereCondition,
      orderBy: {
        start_date: 'desc'
      },
      skip: offset,
      take: limit
    });
    
    // 総件数の取得
    const totalCount = await prisma.trainingHistory.count({
      where: whereCondition
    });
    
    // 研修記録が見つからない場合でも空配列を返す
    if (trainings.length === 0) {
      console.log(`研修記録が見つかりません: Employee ID: ${userId}, Filters: ${JSON.stringify({ year, category, status })}`);
      // 404ではなく空の配列を返す
      return createSuccessResponse({
        trainings: [],
        pagination: {
          total: 0,
          offset: offset,
          limit: limit,
          has_more: false
        }
      });
    }
    
    // レスポンスの構築
    return createSuccessResponse({
      trainings: trainings.map(training => ({
        id: training.id,
        training_history_id: training.training_history_id,
        employee_id: training.employee_id,
        training_name: training.training_name,
        training_type: training.training_type,
        training_category: training.training_category,
        provider_name: training.provider_name,
        start_date: training.start_date,
        end_date: training.end_date,
        duration_hours: training.duration_hours,
        attendance_status: training.attendance_status,
        completion_rate: training.completion_rate,
        certificate_obtained: training.certificate_obtained,
        skills_acquired: training.skills_acquired
      })),
      pagination: {
        total: totalCount,
        offset: offset,
        limit: limit,
        has_more: offset + trainings.length < totalCount
      }
    });
  } catch (error) {
    console.error('研修記録取得エラー:', error);
    return createErrorResponse(
      'SYSTEM_ERROR',
      'システムエラーが発生しました',
      error instanceof Error ? error.message : '不明なエラー',
      500
    );
  }
}

// 研修記録登録API (API-052)
export async function POST(
  request: NextRequest,
  { params }: { params: { userId: string } }
) {
  try {
    const { userId } = params;
    const body = await request.json();

    // ユーザー存在確認
    const user = await prisma.employee.findUnique({
      where: { employee_code: userId }
    });

    if (!user) {
      return createErrorResponse(
        'USER_NOT_FOUND',
        'ユーザーが見つかりません',
        `Employee Code: ${userId}`,
        404
      );
    }

    // 必須パラメータの検証
    const requiredFields = ['name', 'category', 'start_date', 'end_date', 'duration_hours'];
    for (const field of requiredFields) {
      if (!body[field]) {
        return createErrorResponse(
          'INVALID_PARAMETER',
          `${field}は必須です`,
          `Missing field: ${field}`,
          400
        );
      }
    }

    // 日付の検証
    const startDate = new Date(body.start_date);
    const endDate = new Date(body.end_date);

    if (startDate > endDate) {
      return createErrorResponse(
        'INVALID_PARAMETER',
        '開始日は終了日以前の日付を指定してください',
        `Start: ${body.start_date}, End: ${body.end_date}`,
        400
      );
    }

    // 研修記録の登録
    const trainingRecord = await prisma.trainingHistory.create({
      data: {
        id: randomUUID(),
        employee_id: user.id,
        training_name: body.name,
        training_category: body.category,
        start_date: startDate,
        end_date: endDate,
        duration_hours: body.duration_hours,
        location: body.location || '',
        provider_name: body.provider || '',
        attendance_status: body.status || 'planned',
        completion_rate: body.completion_rate || null,
        test_score: body.score || null,
        feedback: body.feedback || null,
        created_by: userId,
        updated_by: userId,
        tenant_id: 'default' // 現在はシングルテナント
      }
    });

    // レスポンスの生成
    const response = {
      training_id: trainingRecord.id,
      user_id: userId,
      name: trainingRecord.training_name,
      category: trainingRecord.training_category,
      description: body.description || '',
      start_date: trainingRecord.start_date?.toISOString().split('T')[0],
      end_date: trainingRecord.end_date?.toISOString().split('T')[0],
      duration_hours: Number(trainingRecord.duration_hours),
      location: trainingRecord.location,
      format: body.format || 'offline',
      provider: trainingRecord.provider_name,
      status: trainingRecord.attendance_status,
      completion_date: trainingRecord.end_date?.toISOString().split('T')[0],
      score: trainingRecord.test_score,
      feedback: trainingRecord.feedback,
      created_at: trainingRecord.created_at.toISOString(),
      created_by: userId
    };

    return createSuccessResponse(response, 201);

  } catch (error) {
    console.error('研修記録登録エラー:', error);
    return createErrorResponse(
      'SYSTEM_ERROR',
      'システムエラーが発生しました',
      error instanceof Error ? error.message : '不明なエラー',
      500
    );
  }
}
