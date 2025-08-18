/**
 * 個別研修記録操作API
 * 要求仕様ID: TRN.1-ATT.1
 */
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { createErrorResponse, createSuccessResponse } from '@/lib/api-utils';

// 研修記録更新API
export async function PUT(
  request: NextRequest,
  { params }: { params: { recordId: string } }
) {
  try {
    const { recordId } = params;
    const body = await request.json();

    // 研修記録の存在確認
    const existingTraining = await prisma.trainingHistory.findUnique({
      where: { id: recordId }
    });

    if (!existingTraining) {
      return createErrorResponse(
        'TRAINING_NOT_FOUND',
        '指定された研修記録が見つかりません',
        `Training ID: ${recordId}`,
        404
      );
    }

    // 更新データの準備
    const updateData: any = {
      updated_by: 'system', // TODO: 認証から取得
      updated_at: new Date()
    };

    // 更新可能なフィールドのマッピング
    const updateableFields: Record<string, string> = {
      'trainingName': 'training_name',
      'trainingCategory': 'training_category',
      'trainingType': 'training_type',
      'providerName': 'provider_name',
      'instructorName': 'instructor_name',
      'startDate': 'start_date',
      'endDate': 'end_date',
      'durationHours': 'duration_hours',
      'location': 'location',
      'cost': 'cost',
      'attendanceStatus': 'attendance_status',
      'completionRate': 'completion_rate',
      'testScore': 'test_score',
      'grade': 'grade',
      'certificateObtained': 'certificate_obtained',
      'certificateNumber': 'certificate_number',
      'skillsAcquired': 'skills_acquired',
      'feedback': 'feedback',
      'satisfactionScore': 'satisfaction_score'
    };

    // 各フィールドの更新
    for (const [clientField, dbField] of Object.entries(updateableFields)) {
      if (body[clientField] !== undefined) {
        // 日付フィールドの処理
        if (clientField === 'startDate' || clientField === 'endDate') {
          updateData[dbField] = new Date(body[clientField]);
        } 
        // 数値フィールドの処理
        else if (['durationHours', 'cost', 'completionRate', 'testScore', 'satisfactionScore'].includes(clientField)) {
          updateData[dbField] = body[clientField] !== null ? Number(body[clientField]) : null;
        }
        // ブール値フィールドの処理
        else if (clientField === 'certificateObtained') {
          updateData[dbField] = Boolean(body[clientField]);
        }
        else {
          updateData[dbField] = body[clientField];
        }
      }
    }

    // 日付の検証
    if (updateData.start_date && updateData.end_date) {
      if (updateData.start_date > updateData.end_date) {
        return createErrorResponse(
          'INVALID_PARAMETER',
          '開始日は終了日以前の日付を指定してください',
          `Start: ${body.startDate}, End: ${body.endDate}`,
          400
        );
      }
    }

    // 研修記録の更新
    const updatedTraining = await prisma.trainingHistory.update({
      where: { id: recordId },
      data: updateData
    });

    // レスポンスの生成
    const response = {
      id: updatedTraining.id,
      trainingName: updatedTraining.training_name,
      trainingCategory: updatedTraining.training_category,
      trainingType: updatedTraining.training_type,
      providerName: updatedTraining.provider_name,
      instructorName: updatedTraining.instructor_name,
      startDate: updatedTraining.start_date?.toISOString().split('T')[0],
      endDate: updatedTraining.end_date?.toISOString().split('T')[0],
      durationHours: Number(updatedTraining.duration_hours),
      location: updatedTraining.location,
      attendanceStatus: updatedTraining.attendance_status,
      completionRate: Number(updatedTraining.completion_rate || 0),
      testScore: updatedTraining.test_score ? Number(updatedTraining.test_score) : null,
      certificateObtained: Boolean(updatedTraining.certificate_obtained),
      certificateNumber: updatedTraining.certificate_number,
      skillsAcquired: updatedTraining.skills_acquired,
      feedback: updatedTraining.feedback,
      satisfactionScore: updatedTraining.satisfaction_score ? Number(updatedTraining.satisfaction_score) : null,
      updatedAt: updatedTraining.updated_at.toISOString()
    };

    return createSuccessResponse(response);

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

// 研修記録削除API
export async function DELETE(
  request: NextRequest,
  { params }: { params: { recordId: string } }
) {
  try {
    const { recordId } = params;

    // 研修記録の存在確認
    const existingTraining = await prisma.trainingHistory.findUnique({
      where: { id: recordId }
    });

    if (!existingTraining) {
      return createErrorResponse(
        'TRAINING_NOT_FOUND',
        '指定された研修記録が見つかりません',
        `Training ID: ${recordId}`,
        404
      );
    }

    // 論理削除
    await prisma.trainingHistory.update({
      where: { id: recordId },
      data: {
        is_deleted: true,
        updated_by: 'system', // TODO: 認証から取得
        updated_at: new Date()
      }
    });

    return createSuccessResponse({
      message: '研修記録を削除しました',
      deleted_id: recordId
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

// 研修記録取得API（個別）
export async function GET(
  request: NextRequest,
  { params }: { params: { recordId: string } }
) {
  try {
    const { recordId } = params;

    // 研修記録の取得
    const training = await prisma.trainingHistory.findUnique({
      where: { 
        id: recordId,
        is_deleted: false 
      }
    });

    if (!training) {
      return createErrorResponse(
        'TRAINING_NOT_FOUND',
        '指定された研修記録が見つかりません',
        `Training ID: ${recordId}`,
        404
      );
    }

    // レスポンスの生成
    const response = {
      id: training.id,
      trainingName: training.training_name,
      trainingCategory: training.training_category,
      trainingType: training.training_type,
      providerName: training.provider_name,
      instructorName: training.instructor_name,
      startDate: training.start_date?.toISOString().split('T')[0],
      endDate: training.end_date?.toISOString().split('T')[0],
      durationHours: Number(training.duration_hours),
      location: training.location,
      cost: training.cost ? Number(training.cost) : null,
      attendanceStatus: training.attendance_status,
      completionRate: Number(training.completion_rate || 0),
      testScore: training.test_score ? Number(training.test_score) : null,
      grade: training.grade,
      certificateObtained: Boolean(training.certificate_obtained),
      certificateNumber: training.certificate_number,
      skillsAcquired: training.skills_acquired,
      learningObjectives: training.learning_objectives,
      learningOutcomes: training.learning_outcomes,
      feedback: training.feedback,
      satisfactionScore: training.satisfaction_score ? Number(training.satisfaction_score) : null,
      recommendationScore: training.recommendation_score ? Number(training.recommendation_score) : null,
      followUpRequired: Boolean(training.follow_up_required),
      followUpDate: training.follow_up_date?.toISOString().split('T')[0],
      managerApproval: Boolean(training.manager_approval),
      approvedBy: training.approved_by,
      createdAt: training.created_at.toISOString(),
      updatedAt: training.updated_at.toISOString()
    };

    return createSuccessResponse(response);

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