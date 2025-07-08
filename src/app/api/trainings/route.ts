/**
 * 要求仕様ID: TRN.1-ATT.1
 * 対応設計書: docs/design/api/specs/API定義書_API-052_研修記録登録API.md
 * 実装内容: 研修記録を登録するAPI
 */
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { createErrorResponse, createSuccessResponse } from '@/lib/api-utils';

/**
 * 研修記録登録API
 * 
 * @param request - リクエスト
 * @returns 登録結果
 */
export async function POST(request: NextRequest) {
  try {
    // リクエストボディの取得
    const body = await request.json();
    
    // 必須項目の検証
    if (!body.employee_id || !body.training_name || !body.start_date) {
      return createErrorResponse(
        'INVALID_PARAMETER',
        '必須項目が不足しています',
        '社員ID、研修名、開始日は必須です',
        400
      );
    }
    
    // 認証チェック（実際の実装では認証ミドルウェアを使用）
    // この部分は将来的に認証機能と連携
    
    // ユーザーの存在確認
    const employee = await prisma.employee.findUnique({
      where: { id: body.employee_id }
    });
    
    if (!employee) {
      return createErrorResponse(
        'USER_NOT_FOUND',
        '指定されたユーザーが見つかりません',
        `Employee ID: ${body.employee_id}`,
        404
      );
    }
    
    // 研修記録IDの生成（実際の環境では自動生成される場合もある）
    const trainingHistoryId = `TRN${Date.now()}${Math.floor(Math.random() * 1000)}`;
    
    // 研修記録の登録
    const training = await prisma.trainingHistory.create({
      data: {
        id: `TRN-ID-${Date.now()}`, // IDを追加
        training_history_id: trainingHistoryId,
        employee_id: body.employee_id,
        training_name: body.training_name,
        training_type: body.training_type || '社内研修',
        training_category: body.training_category || '技術研修',
        provider_name: body.provider_name || '自社',
        start_date: new Date(body.start_date),
        end_date: body.end_date ? new Date(body.end_date) : null,
        duration_hours: body.duration_hours || 0,
        attendance_status: body.attendance_status || 'completed',
        completion_rate: body.completion_rate || 100,
        certificate_obtained: body.certificate_obtained || false,
        skills_acquired: body.skills_acquired || [],
        learning_objectives: body.learning_objectives || '',
        learning_outcomes: body.learning_outcomes || '',
        feedback: body.feedback || '',
        tenant_id: body.tenant_id || 'default', // テナントIDを追加
        created_by: body.employee_id,
        updated_by: body.employee_id,
        is_deleted: false
      }
    });
    
    // レスポンスの構築
    return createSuccessResponse({
      training: {
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
        skills_acquired: training.skills_acquired,
        created_at: training.created_at
      }
    }, 201);
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
