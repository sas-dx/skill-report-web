/**
 * 要求仕様ID: SKL.1-CRUD.1
 * 対応設計書: docs/design/api/specs/API定義書_API-022_スキルCRUD API.md
 * 実装内容: スキルの新規登録・更新・削除API
 */

import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import { createAuditLog, getObjectDiff } from '@/lib/auditLogger';
import { 
  createSuccessResponse, 
  createAuthErrorResponse, 
  createNotFoundErrorResponse, 
  createValidationErrorResponse,
  createSystemErrorResponse 
} from '@/lib/api-utils';

/**
 * スキル新規登録API
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

    console.log('Skills POST API - Request body:', JSON.stringify(body, null, 2));

    // バリデーション
    const errors: Array<{ field: string; message: string }> = [];

    if (!body.skillItemId || typeof body.skillItemId !== 'string') {
      errors.push({ field: 'skillItemId', message: 'スキルアイテムIDは必須です' });
    }

    if (!body.skillCategoryId || typeof body.skillCategoryId !== 'string') {
      errors.push({ field: 'skillCategoryId', message: 'スキルカテゴリIDは必須です' });
    }

    if (body.skillLevel !== undefined && (typeof body.skillLevel !== 'number' || body.skillLevel < 1 || body.skillLevel > 5)) {
      errors.push({ field: 'skillLevel', message: 'スキルレベルは1〜5の範囲で指定してください' });
    }

    if (body.selfAssessment !== undefined && (typeof body.selfAssessment !== 'number' || body.selfAssessment < 1 || body.selfAssessment > 5)) {
      errors.push({ field: 'selfAssessment', message: '自己評価は1〜5の範囲で指定してください' });
    }

    if (errors.length > 0) {
      return createValidationErrorResponse(errors);
    }

    // スキルアイテムの存在確認または作成
    let skillItem = await prisma.skillItem.findUnique({
      where: { skill_code: body.skillItemId }
    });

    if (!skillItem) {
      // スキルアイテムが存在しない場合は作成
      console.log('スキルアイテムが存在しないため、新規作成します:', body.skillItemId);
      
      // スキル名を抽出（skillItemIdが「SKILL_XXX_timestamp」形式の場合）
      let skillName = body.skillItemId;
      if (skillName.startsWith('SKILL_')) {
        // SKILL_XXX_timestamp 形式からスキル名を抽出
        const parts = skillName.split('_');
        // 最後のタイムスタンプを除いたSKILL_以降をスキル名とする
        if (parts.length > 2) {
          parts.pop(); // タイムスタンプを削除
          skillName = parts.slice(1).join(' '); // SKILL_を除いた部分をスペースで結合
        }
      }
      
      // スキル名がリクエストに含まれている場合はそれを使用
      if (body.skillName) {
        skillName = body.skillName;
      }
      
      try {
        skillItem = await prisma.skillItem.create({
          data: {
            skill_code: body.skillItemId,
            skill_name: skillName,
            skill_category_id: body.skillCategoryId,
            skill_type: 'technical',
            difficulty_level: 2,  // 中程度の難易度
            importance_level: 2   // 中程度の重要度
          }
        });
      } catch (createError) {
        console.error('スキルアイテム作成エラー:', createError);
        return createSystemErrorResponse(createError as Error);
      }
    }

    // スキルカテゴリの存在確認
    const skillCategory = await prisma.skillCategory.findUnique({
      where: { category_code: body.skillCategoryId }
    });

    if (!skillCategory) {
      return createNotFoundErrorResponse('スキルカテゴリ', body.skillCategoryId);
    }

    // 重複チェック
    const existingSkill = await prisma.skillRecord.findFirst({
      where: {
        employee_id: currentEmployeeId,
        skill_item_id: body.skillItemId,
        is_deleted: false
      }
    });

    if (existingSkill) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'DUPLICATE_SKILL',
            message: 'このスキルは既に登録されています'
          }
        },
        { status: 409 }
      );
    }

    // 新規スキルレコードの作成
    const newSkillRecord = await prisma.skillRecord.create({
      data: {
        id: `skill_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        employee_id: currentEmployeeId,
        skill_item_id: body.skillItemId,
        skill_category_id: body.skillCategoryId,
        skill_level: body.skillLevel || null,
        self_assessment: body.selfAssessment || null,
        manager_assessment: body.managerAssessment || null,
        evidence_description: body.evidenceDescription || null,
        acquisition_date: body.acquisitionDate ? new Date(body.acquisitionDate) : null,
        last_used_date: body.lastUsedDate ? new Date(body.lastUsedDate) : null,
        expiry_date: body.expiryDate ? new Date(body.expiryDate) : null,
        certification_id: body.certificationId || null,
        skill_status: body.skillStatus || 'active',
        learning_hours: body.learningHours || 0,
        project_experience_count: body.projectExperienceCount || 0,
        assessment_date: body.assessmentDate ? new Date(body.assessmentDate) : null,
        assessor_id: body.assessorId || null,
        tenant_id: 'tenant_001', // 現在はシングルテナント
        created_by: currentEmployeeId,
        updated_by: currentEmployeeId
      }
    });

    // AuditLog記録
    try {
      await createAuditLog({
        userId: currentEmployeeId,
        actionType: 'CREATE',
        targetTable: 'SkillRecord',
        targetId: newSkillRecord.id,
        oldValues: {},
        newValues: {
          employee_id: newSkillRecord.employee_id,
          skill_item_id: newSkillRecord.skill_item_id,
          skill_level: newSkillRecord.skill_level,
          self_assessment: newSkillRecord.self_assessment
        },
        changeReason: 'スキル新規登録',
        ipAddress: request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown',
        userAgent: request.headers.get('user-agent') || 'unknown'
      });
    } catch (auditError) {
      console.error('AuditLog記録エラー:', auditError);
    }

    const responseData = {
      skillRecordId: newSkillRecord.id,
      skillItemId: newSkillRecord.skill_item_id,
      skillCategoryId: newSkillRecord.skill_category_id,
      skillLevel: newSkillRecord.skill_level,
      selfAssessment: newSkillRecord.self_assessment,
      managerAssessment: newSkillRecord.manager_assessment,
      skillStatus: newSkillRecord.skill_status,
      createdAt: newSkillRecord.created_at.toISOString(),
      updatedAt: newSkillRecord.updated_at.toISOString()
    };

    return createSuccessResponse(responseData, 201);

  } catch (error) {
    console.error('Skills POST error:', error);
    return createSystemErrorResponse(error as Error);
  }
}

/**
 * スキル更新API
 * @param request NextRequest
 * @returns NextResponse
 */
export async function PUT(request: NextRequest) {
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

    console.log('Skills PUT API - Request body:', JSON.stringify(body, null, 2));

    // バリデーション
    const errors: Array<{ field: string; message: string }> = [];

    if (!body.skillRecordId || typeof body.skillRecordId !== 'string') {
      errors.push({ field: 'skillRecordId', message: 'スキルレコードIDは必須です' });
    }

    if (body.skillLevel !== undefined && (typeof body.skillLevel !== 'number' || body.skillLevel < 1 || body.skillLevel > 5)) {
      errors.push({ field: 'skillLevel', message: 'スキルレベルは1〜5の範囲で指定してください' });
    }

    if (body.selfAssessment !== undefined && (typeof body.selfAssessment !== 'number' || body.selfAssessment < 1 || body.selfAssessment > 5)) {
      errors.push({ field: 'selfAssessment', message: '自己評価は1〜5の範囲で指定してください' });
    }

    if (errors.length > 0) {
      return createValidationErrorResponse(errors);
    }

    // 既存のスキルレコードの取得
    const existingSkillRecord = await prisma.skillRecord.findFirst({
      where: {
        id: body.skillRecordId,
        employee_id: currentEmployeeId,
        is_deleted: false
      }
    });

    if (!existingSkillRecord) {
      return createNotFoundErrorResponse('スキルレコード', body.skillRecordId);
    }

    // 更新データの構築
    const updateData: any = {
      updated_by: currentEmployeeId,
      updated_at: new Date()
    };

    if (body.skillLevel !== undefined) updateData.skill_level = body.skillLevel;
    if (body.selfAssessment !== undefined) updateData.self_assessment = body.selfAssessment;
    if (body.managerAssessment !== undefined) updateData.manager_assessment = body.managerAssessment;
    if (body.evidenceDescription !== undefined) updateData.evidence_description = body.evidenceDescription;
    if (body.acquisitionDate !== undefined) updateData.acquisition_date = body.acquisitionDate ? new Date(body.acquisitionDate) : null;
    if (body.lastUsedDate !== undefined) updateData.last_used_date = body.lastUsedDate ? new Date(body.lastUsedDate) : null;
    if (body.expiryDate !== undefined) updateData.expiry_date = body.expiryDate ? new Date(body.expiryDate) : null;
    if (body.certificationId !== undefined) updateData.certification_id = body.certificationId;
    if (body.skillStatus !== undefined) updateData.skill_status = body.skillStatus;
    if (body.learningHours !== undefined) updateData.learning_hours = body.learningHours;
    if (body.projectExperienceCount !== undefined) updateData.project_experience_count = body.projectExperienceCount;
    if (body.assessmentDate !== undefined) updateData.assessment_date = body.assessmentDate ? new Date(body.assessmentDate) : null;
    if (body.assessorId !== undefined) updateData.assessor_id = body.assessorId;

    // スキルレコードの更新
    const updatedSkillRecord = await prisma.skillRecord.update({
      where: { id: body.skillRecordId },
      data: updateData
    });

    // AuditLog記録
    try {
      const { oldValues, newValues } = getObjectDiff(
        {
          skill_level: existingSkillRecord.skill_level,
          self_assessment: existingSkillRecord.self_assessment,
          manager_assessment: existingSkillRecord.manager_assessment,
          evidence_description: existingSkillRecord.evidence_description,
          skill_status: existingSkillRecord.skill_status
        },
        {
          skill_level: updatedSkillRecord.skill_level,
          self_assessment: updatedSkillRecord.self_assessment,
          manager_assessment: updatedSkillRecord.manager_assessment,
          evidence_description: updatedSkillRecord.evidence_description,
          skill_status: updatedSkillRecord.skill_status
        }
      );

      if (Object.keys(newValues).length > 0) {
        await createAuditLog({
          userId: currentEmployeeId,
          actionType: 'UPDATE',
          targetTable: 'SkillRecord',
          targetId: updatedSkillRecord.id,
          oldValues,
          newValues,
          changeReason: 'スキル情報更新',
          ipAddress: request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown',
          userAgent: request.headers.get('user-agent') || 'unknown'
        });
      }
    } catch (auditError) {
      console.error('AuditLog記録エラー:', auditError);
    }

    const responseData = {
      skillRecordId: updatedSkillRecord.id,
      skillItemId: updatedSkillRecord.skill_item_id,
      skillCategoryId: updatedSkillRecord.skill_category_id,
      skillLevel: updatedSkillRecord.skill_level,
      selfAssessment: updatedSkillRecord.self_assessment,
      managerAssessment: updatedSkillRecord.manager_assessment,
      skillStatus: updatedSkillRecord.skill_status,
      updatedAt: updatedSkillRecord.updated_at.toISOString()
    };

    return createSuccessResponse(responseData);

  } catch (error) {
    console.error('Skills PUT error:', error);
    return createSystemErrorResponse(error as Error);
  }
}

/**
 * スキル削除API（論理削除）
 * @param request NextRequest
 * @returns NextResponse
 */
export async function DELETE(request: NextRequest) {
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

    // クエリパラメータからスキルレコードIDを取得
    const { searchParams } = new URL(request.url);
    const skillRecordId = searchParams.get('skillRecordId');

    if (!skillRecordId) {
      return createValidationErrorResponse([
        { field: 'skillRecordId', message: 'スキルレコードIDは必須です' }
      ]);
    }

    // 既存のスキルレコードの取得
    const existingSkillRecord = await prisma.skillRecord.findFirst({
      where: {
        id: skillRecordId,
        employee_id: currentEmployeeId,
        is_deleted: false
      }
    });

    if (!existingSkillRecord) {
      return createNotFoundErrorResponse('スキルレコード', skillRecordId);
    }

    // 論理削除の実行
    const deletedSkillRecord = await prisma.skillRecord.update({
      where: { id: skillRecordId },
      data: {
        is_deleted: true,
        updated_by: currentEmployeeId,
        updated_at: new Date()
      }
    });

    // AuditLog記録
    try {
      await createAuditLog({
        userId: currentEmployeeId,
        actionType: 'DELETE',
        targetTable: 'SkillRecord',
        targetId: deletedSkillRecord.id,
        oldValues: {
          is_deleted: false
        },
        newValues: {
          is_deleted: true
        },
        changeReason: 'スキル削除',
        ipAddress: request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown',
        userAgent: request.headers.get('user-agent') || 'unknown'
      });
    } catch (auditError) {
      console.error('AuditLog記録エラー:', auditError);
    }

    const responseData = {
      skillRecordId: deletedSkillRecord.id,
      deleted: true,
      deletedAt: deletedSkillRecord.updated_at.toISOString()
    };

    return createSuccessResponse(responseData);

  } catch (error) {
    console.error('Skills DELETE error:', error);
    return createSystemErrorResponse(error as Error);
  }
}