/**
 * 要求仕様ID: TRN.1-ATT.1
 * 対応設計書: docs/design/api/specs/API定義書_API-051_研修記録取得API.md
 * 実装内容: ユーザーIDに基づいて研修記録を取得するAPI
 */
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { createErrorResponse, createSuccessResponse } from '@/lib/api-utils';

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
