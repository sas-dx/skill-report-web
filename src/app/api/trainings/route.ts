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
        skills_acquired: body.skills_acquired ? 
          JSON.stringify(body.skills_acquired) : null,
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

/**
 * 研修記録更新API
 * 
 * @param request - リクエスト
 * @returns 更新結果
 */
export async function PUT(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const trainingId = searchParams.get('id');
    const body = await request.json();

    if (!trainingId) {
      return createErrorResponse(
        'INVALID_PARAMETER',
        '研修IDが必要です',
        'URLパラメータにidを指定してください',
        400
      );
    }

    // 必須項目の検証
    if (!body.training_name || !body.start_date) {
      return createErrorResponse(
        'INVALID_PARAMETER',
        '必須項目が不足しています',
        '研修名、開始日は必須です',
        400
      );
    }

    // 既存の研修記録を確認
    const existingTraining = await prisma.trainingHistory.findUnique({
      where: { id: trainingId }
    });

    if (!existingTraining) {
      return createErrorResponse(
        'RESOURCE_NOT_FOUND',
        '指定された研修記録が見つかりません',
        `Training ID: ${trainingId}`,
        404
      );
    }

    // 研修記録の更新
    const updatedTraining = await prisma.trainingHistory.update({
      where: { id: trainingId },
      data: {
        training_name: body.training_name,
        training_type: body.training_type || existingTraining.training_type,
        training_category: body.training_category || existingTraining.training_category,
        provider_name: body.provider_name || existingTraining.provider_name,
        start_date: new Date(body.start_date),
        end_date: body.end_date ? new Date(body.end_date) : existingTraining.end_date,
        duration_hours: body.duration_hours || existingTraining.duration_hours,
        attendance_status: body.attendance_status || existingTraining.attendance_status,
        completion_rate: body.completion_rate || existingTraining.completion_rate,
        certificate_obtained: body.certificate_obtained !== undefined ? body.certificate_obtained : existingTraining.certificate_obtained,
        skills_acquired: body.skills_acquired ? 
          JSON.stringify(body.skills_acquired) : existingTraining.skills_acquired,
        learning_objectives: body.learning_objectives || existingTraining.learning_objectives,
        learning_outcomes: body.learning_outcomes || existingTraining.learning_outcomes,
        feedback: body.feedback || existingTraining.feedback,
        updated_by: body.employee_id || existingTraining.employee_id,
        updated_at: new Date()
      }
    });

    // レスポンスの構築
    return createSuccessResponse({
      training: {
        id: updatedTraining.id,
        training_history_id: updatedTraining.training_history_id,
        employee_id: updatedTraining.employee_id,
        training_name: updatedTraining.training_name,
        training_type: updatedTraining.training_type,
        training_category: updatedTraining.training_category,
        provider_name: updatedTraining.provider_name,
        start_date: updatedTraining.start_date,
        end_date: updatedTraining.end_date,
        duration_hours: updatedTraining.duration_hours,
        attendance_status: updatedTraining.attendance_status,
        completion_rate: updatedTraining.completion_rate,
        certificate_obtained: updatedTraining.certificate_obtained,
        skills_acquired: updatedTraining.skills_acquired,
        updated_at: updatedTraining.updated_at
      }
    });
  } catch (error) {
    console.error('研修記録更新エラー:', error);
    return createErrorResponse(
      'SYSTEM_ERROR',
      'システムエラーが発生しました',
      error instanceof Error ? error.message : '不明なエラー',
      500
    );
  }
}

/**
 * 研修記録削除API
 * 
 * @param request - リクエスト
 * @returns 削除結果
 */
export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const trainingId = searchParams.get('id');

    if (!trainingId) {
      return createErrorResponse(
        'INVALID_PARAMETER',
        '研修IDが必要です',
        'URLパラメータにidを指定してください',
        400
      );
    }

    // 既存の研修記録を確認
    const existingTraining = await prisma.trainingHistory.findUnique({
      where: { id: trainingId }
    });

    if (!existingTraining) {
      return createErrorResponse(
        'RESOURCE_NOT_FOUND',
        '指定された研修記録が見つかりません',
        `Training ID: ${trainingId}`,
        404
      );
    }

    // 論理削除（is_deletedフラグを立てる）
    const deletedTraining = await prisma.trainingHistory.update({
      where: { id: trainingId },
      data: {
        is_deleted: true,
        updated_at: new Date()
      }
    });

    // レスポンスの構築
    return createSuccessResponse({
      message: '研修記録を削除しました',
      training_id: trainingId
    });
  } catch (error) {
    console.error('研修記録削除エラー:', error);
    return createErrorResponse(
      'SYSTEM_ERROR',
      'システムエラーが発生しました',
      error instanceof Error ? error.message : '不明なエラー',
      500
    );
  }
}
