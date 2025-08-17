/**
 * 研修記録管理API
 * 要求仕様ID: TRN.1-ATT.1, API-901, API-902
 */

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { getTenantFromRequest } from '@/lib/tenant-context';
import { verifyAuth } from '@/lib/auth';

interface TrainingRecord {
  id?: string;
  trainingProgramId?: string;
  trainingName: string;
  trainingType: string;
  trainingCategory: string;
  providerName: string;
  instructorName?: string;
  startDate: string;
  endDate: string;
  durationHours: number;
  location?: string;
  cost?: number;
  costCoveredBy?: string;
  attendanceStatus: string;
  completionRate: number;
  testScore?: number;
  grade?: string;
  certificateObtained: boolean;
  certificateNumber?: string;
  pduEarned?: number;
  skillsAcquired?: string[];
  learningObjectives?: string;
  learningOutcomes?: string;
  feedback?: string;
  satisfactionScore?: number;
  recommendationScore?: number;
  followUpRequired: boolean;
  followUpDate?: string;
}

interface TrainingRecordsResponse {
  success: boolean;
  data?: {
    records: TrainingRecord[];
    totalCount: number;
    categories: string[];
    statistics: {
      totalHours: number;
      completedCourses: number;
      averageScore: number;
      totalCost: number;
    };
  };
  error?: {
    code: string;
    message: string;
  };
  timestamp: string;
}

/**
 * 研修記録一覧取得API
 * GET /api/trainings/records
 */
export async function GET(
  request: NextRequest
): Promise<NextResponse<TrainingRecordsResponse>> {
  try {
    // 認証チェック
    const authResult = await verifyAuth(request);
    if (!authResult.success) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'AUTHENTICATION_ERROR',
            message: '認証が必要です'
          },
          timestamp: new Date().toISOString()
        },
        { status: 401 }
      );
    }

    // テナント情報を取得
    const tenantContext = await getTenantFromRequest(request);
    const tenantId = tenantContext?.tenantId || authResult.tenantId;

    // クエリパラメータを取得
    const { searchParams } = new URL(request.url);
    const userId = searchParams.get('userId');
    const employeeId = userId || authResult.employeeId;
    const year = searchParams.get('year');
    const category = searchParams.get('category');
    const status = searchParams.get('status');

    // 研修記録を取得
    const whereConditions: any = {
      employee_id: employeeId,
      tenant_id: tenantId
    };

    if (year) {
      const yearNum = parseInt(year);
      whereConditions.start_date = {
        gte: new Date(yearNum, 0, 1),
        lt: new Date(yearNum + 1, 0, 1)
      };
    }

    if (category) {
      whereConditions.training_category = category;
    }

    if (status) {
      whereConditions.attendance_status = status;
    }

    const trainingRecords = await prisma.trainingHistory.findMany({
      where: {
        ...whereConditions,
        is_deleted: false
      },
      orderBy: {
        start_date: 'desc'
      }
    });

    // 研修プログラム情報を取得
    const programIds = [...new Set(trainingRecords.map(r => r.training_program_id).filter(Boolean))];
    const programs = await prisma.trainingProgram.findMany({
      where: {
        training_program_id: { in: programIds as string[] }
      }
    });

    const programMap = new Map(programs.map(p => [p.training_program_id, p]));

    // レスポンス用に変換
    const records: TrainingRecord[] = trainingRecords.map(record => {
      const program = record.training_program_id ? programMap.get(record.training_program_id) : null;
      
      return {
        id: record.id,
        trainingProgramId: record.training_program_id || undefined,
        trainingName: record.training_name || program?.program_name || '',
        trainingType: record.training_type || program?.program_type || '',
        trainingCategory: record.training_category || program?.category || '',
        providerName: record.provider_name || program?.provider || '',
        instructorName: record.instructor_name || undefined,
        startDate: record.start_date?.toISOString() || '',
        endDate: record.end_date?.toISOString() || '',
        durationHours: Number(record.duration_hours) || 0,
        location: record.location || undefined,
        cost: record.cost ? Number(record.cost) : undefined,
        costCoveredBy: record.cost_covered_by || undefined,
        attendanceStatus: record.attendance_status || 'NOT_STARTED',
        completionRate: Number(record.completion_rate) || 0,
        testScore: record.test_score ? Number(record.test_score) : undefined,
        grade: record.grade || undefined,
        certificateObtained: record.certificate_obtained || false,
        certificateNumber: record.certificate_number || undefined,
        pduEarned: record.pdu_earned ? Number(record.pdu_earned) : undefined,
        skillsAcquired: record.skills_acquired ? record.skills_acquired.split(',') : [],
        learningObjectives: record.learning_objectives || undefined,
        learningOutcomes: record.learning_outcomes || undefined,
        feedback: record.feedback || undefined,
        satisfactionScore: record.satisfaction_score ? Number(record.satisfaction_score) : undefined,
        recommendationScore: record.recommendation_score ? Number(record.recommendation_score) : undefined,
        followUpRequired: record.follow_up_required || false,
        followUpDate: record.follow_up_date?.toISOString() || undefined
      };
    });

    // カテゴリ一覧を取得
    const categories = [...new Set(records.map(r => r.trainingCategory))].filter(Boolean);

    // 統計情報を計算
    const statistics = {
      totalHours: records.reduce((sum, r) => sum + (r.durationHours || 0), 0),
      completedCourses: records.filter(r => r.attendanceStatus === 'COMPLETED').length,
      averageScore: records.filter(r => r.testScore).reduce((sum, r) => sum + (r.testScore || 0), 0) / 
                    (records.filter(r => r.testScore).length || 1),
      totalCost: records.reduce((sum, r) => sum + (r.cost || 0), 0)
    };

    return NextResponse.json(
      {
        success: true,
        data: {
          records,
          totalCount: records.length,
          categories,
          statistics
        },
        timestamp: new Date().toISOString()
      },
      { status: 200 }
    );

  } catch (error) {
    console.error('研修記録取得APIエラー:', error);
    
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'INTERNAL_ERROR',
          message: '研修記録の取得に失敗しました'
        },
        timestamp: new Date().toISOString()
      },
      { status: 500 }
    );
  }
}

/**
 * 研修記録保存API
 * POST /api/trainings/records
 */
export async function POST(
  request: NextRequest
): Promise<NextResponse> {
  try {
    // 認証チェック
    const authResult = await verifyAuth(request);
    if (!authResult.success) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'AUTHENTICATION_ERROR',
            message: '認証が必要です'
          },
          timestamp: new Date().toISOString()
        },
        { status: 401 }
      );
    }

    // テナント情報を取得
    const tenantContext = await getTenantFromRequest(request);
    const tenantId = tenantContext?.tenantId || authResult.tenantId;

    const body: TrainingRecord = await request.json();

    // 入力検証
    if (!body.trainingName || !body.trainingType || !body.startDate || !body.endDate) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message: '必須項目が入力されていません'
          },
          timestamp: new Date().toISOString()
        },
        { status: 400 }
      );
    }

    // 研修記録を作成
    const newRecord = await prisma.trainingHistory.create({
      data: {
        id: `training_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        training_history_id: `TRN_${Date.now()}`,
        employee_id: authResult.employeeId || authResult.userId || '',
        training_program_id: body.trainingProgramId,
        training_name: body.trainingName,
        training_type: body.trainingType,
        training_category: body.trainingCategory,
        provider_name: body.providerName,
        instructor_name: body.instructorName,
        start_date: new Date(body.startDate),
        end_date: new Date(body.endDate),
        duration_hours: body.durationHours,
        location: body.location,
        cost: body.cost,
        cost_covered_by: body.costCoveredBy,
        attendance_status: body.attendanceStatus || 'REGISTERED',
        completion_rate: body.completionRate || 0,
        test_score: body.testScore,
        grade: body.grade,
        certificate_obtained: body.certificateObtained || false,
        certificate_number: body.certificateNumber,
        pdu_earned: body.pduEarned,
        skills_acquired: body.skillsAcquired?.join(','),
        learning_objectives: body.learningObjectives,
        learning_outcomes: body.learningOutcomes,
        feedback: body.feedback,
        satisfaction_score: body.satisfactionScore,
        recommendation_score: body.recommendationScore,
        follow_up_required: body.followUpRequired || false,
        follow_up_date: body.followUpDate ? new Date(body.followUpDate) : null,
        tenant_id: tenantId,
        created_by: authResult.userId || '',
        updated_by: authResult.userId || '',
        is_deleted: false
      }
    });

    // 監査ログを記録（AuditLogテーブルが存在しない場合はスキップ）
    try {
      await prisma.auditLog.create({
        data: {
          id: `audit_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          user_id: authResult.userId || '',
          action_type: 'CREATE',
          target_table: 'TrainingHistory',
          target_id: newRecord.id,
          new_values: JSON.stringify(body),
          result_status: 'SUCCESS',
          tenant_id: tenantId,
          created_at: new Date(),
          created_by: authResult.userId || ''
        }
      });
    } catch (auditError) {
      console.log('監査ログ記録をスキップ:', auditError);
    }

    return NextResponse.json(
      {
        success: true,
        data: {
          id: newRecord.id,
          message: '研修記録を登録しました'
        },
        timestamp: new Date().toISOString()
      },
      { status: 201 }
    );

  } catch (error) {
    console.error('研修記録保存APIエラー:', error);
    
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'INTERNAL_ERROR',
          message: '研修記録の保存に失敗しました'
        },
        timestamp: new Date().toISOString()
      },
      { status: 500 }
    );
  }
}

/**
 * 研修記録更新API
 * PUT /api/trainings/records
 */
export async function PUT(
  request: NextRequest
): Promise<NextResponse> {
  try {
    // 認証チェック
    const authResult = await verifyAuth(request);
    if (!authResult.success) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'AUTHENTICATION_ERROR',
            message: '認証が必要です'
          },
          timestamp: new Date().toISOString()
        },
        { status: 401 }
      );
    }

    // テナント情報を取得
    const tenantContext = await getTenantFromRequest(request);
    const tenantId = tenantContext?.tenantId || authResult.tenantId;

    const body: TrainingRecord = await request.json();

    if (!body.id) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message: '更新対象のIDが指定されていません'
          },
          timestamp: new Date().toISOString()
        },
        { status: 400 }
      );
    }

    // 既存記録の確認
    const existingRecord = await prisma.trainingHistory.findFirst({
      where: {
        id: body.id,
        tenant_id: tenantId,
        is_deleted: false
      }
    });

    if (!existingRecord) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'NOT_FOUND',
            message: '研修記録が見つかりません'
          },
          timestamp: new Date().toISOString()
        },
        { status: 404 }
      );
    }

    // 研修記録を更新
    const updatedRecord = await prisma.trainingHistory.update({
      where: { id: body.id },
      data: {
        training_name: body.trainingName,
        training_type: body.trainingType,
        training_category: body.trainingCategory,
        provider_name: body.providerName,
        instructor_name: body.instructorName,
        start_date: new Date(body.startDate),
        end_date: new Date(body.endDate),
        duration_hours: body.durationHours,
        location: body.location,
        cost: body.cost,
        cost_covered_by: body.costCoveredBy,
        attendance_status: body.attendanceStatus,
        completion_rate: body.completionRate,
        test_score: body.testScore,
        grade: body.grade,
        certificate_obtained: body.certificateObtained,
        certificate_number: body.certificateNumber,
        pdu_earned: body.pduEarned,
        skills_acquired: body.skillsAcquired?.join(','),
        learning_objectives: body.learningObjectives,
        learning_outcomes: body.learningOutcomes,
        feedback: body.feedback,
        satisfaction_score: body.satisfactionScore,
        recommendation_score: body.recommendationScore,
        follow_up_required: body.followUpRequired,
        follow_up_date: body.followUpDate ? new Date(body.followUpDate) : null,
        updated_by: authResult.userId || '',
        updated_at: new Date()
      }
    });

    // 監査ログを記録（AuditLogテーブルが存在しない場合はスキップ）
    try {
      await prisma.auditLog.create({
        data: {
          id: `audit_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          user_id: authResult.userId || '',
          action_type: 'UPDATE',
          target_table: 'TrainingHistory',
          target_id: updatedRecord.id,
          old_values: JSON.stringify(existingRecord),
          new_values: JSON.stringify(body),
          result_status: 'SUCCESS',
          tenant_id: tenantId,
          created_at: new Date(),
          created_by: authResult.userId || ''
        }
      });
    } catch (auditError) {
      console.log('監査ログ記録をスキップ:', auditError);
    }

    return NextResponse.json(
      {
        success: true,
        data: {
          id: updatedRecord.id,
          message: '研修記録を更新しました'
        },
        timestamp: new Date().toISOString()
      },
      { status: 200 }
    );

  } catch (error) {
    console.error('研修記録更新APIエラー:', error);
    
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'INTERNAL_ERROR',
          message: '研修記録の更新に失敗しました'
        },
        timestamp: new Date().toISOString()
      },
      { status: 500 }
    );
  }
}

/**
 * 研修記録削除API
 * DELETE /api/trainings/records
 */
export async function DELETE(
  request: NextRequest
): Promise<NextResponse> {
  try {
    // 認証チェック
    const authResult = await verifyAuth(request);
    if (!authResult.success) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'AUTHENTICATION_ERROR',
            message: '認証が必要です'
          },
          timestamp: new Date().toISOString()
        },
        { status: 401 }
      );
    }

    // テナント情報を取得
    const tenantContext = await getTenantFromRequest(request);
    const tenantId = tenantContext?.tenantId || authResult.tenantId;

    const { searchParams } = new URL(request.url);
    const recordId = searchParams.get('id');

    if (!recordId) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message: '削除対象のIDが指定されていません'
          },
          timestamp: new Date().toISOString()
        },
        { status: 400 }
      );
    }

    // 既存記録の確認
    const existingRecord = await prisma.trainingHistory.findFirst({
      where: {
        id: recordId,
        tenant_id: tenantId,
        is_deleted: false
      }
    });

    if (!existingRecord) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'NOT_FOUND',
            message: '研修記録が見つかりません'
          },
          timestamp: new Date().toISOString()
        },
        { status: 404 }
      );
    }

    // 論理削除
    await prisma.trainingHistory.update({
      where: { id: recordId },
      data: {
        is_deleted: true,
        updated_by: authResult.userId || '',
        updated_at: new Date()
      }
    });

    // 監査ログを記録（AuditLogテーブルが存在しない場合はスキップ）
    try {
      await prisma.auditLog.create({
        data: {
          id: `audit_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          user_id: authResult.userId || '',
          action_type: 'DELETE',
          target_table: 'TrainingHistory',
          target_id: recordId,
          old_values: JSON.stringify(existingRecord),
          result_status: 'SUCCESS',
          tenant_id: tenantId,
          created_at: new Date(),
          created_by: authResult.userId || ''
        }
      });
    } catch (auditError) {
      console.log('監査ログ記録をスキップ:', auditError);
    }

    return NextResponse.json(
      {
        success: true,
        data: {
          id: recordId,
          message: '研修記録を削除しました'
        },
        timestamp: new Date().toISOString()
      },
      { status: 200 }
    );

  } catch (error) {
    console.error('研修記録削除APIエラー:', error);
    
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'INTERNAL_ERROR',
          message: '研修記録の削除に失敗しました'
        },
        timestamp: new Date().toISOString()
      },
      { status: 500 }
    );
  }
}

/**
 * OPTIONS メソッド（CORS対応）
 */
export async function OPTIONS(request: NextRequest): Promise<NextResponse> {
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, x-tenant-id, x-user-id',
    },
  });
}