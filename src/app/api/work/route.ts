/**
 * 要求仕様ID: WPM.1-DET.1
 * 対応設計書: docs/design/api/specs/API定義書_API-042_作業実績登録API.md
 * 実装内容: 作業実績CRUD API (POST/PUT/DELETE)
 */

import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import {
  createSuccessResponse,
  createErrorResponse,
  createAuthErrorResponse,
  createValidationErrorResponse,
  createNotFoundErrorResponse
} from '@/lib/api-utils';

// 作業実績登録API
export async function POST(request: NextRequest) {
  try {
    // 認証チェック（オプショナル）
    const authResult = await verifyAuth(request);
    
    // トークンがない場合はデフォルトユーザーを使用（開発用）
    const employeeId = authResult.success 
      ? (authResult.employeeId || authResult.userId)
      : '000001';
    
    console.log('Work POST - employeeId:', employeeId, 'authResult:', authResult);

    const body = await request.json();
    console.log('Work POST - Request body:', body);

    // 必須項目のバリデーション
    const validationErrors = [];
    if (!body.project_name) {
      validationErrors.push({ field: 'project_name', message: 'プロジェクト名は必須です' });
    }
    if (!body.project_code) {
      validationErrors.push({ field: 'project_code', message: 'プロジェクトコードは必須です' });
    }
    if (!body.role) {
      validationErrors.push({ field: 'role', message: '役割は必須です' });
    }
    if (!body.start_date) {
      validationErrors.push({ field: 'start_date', message: '開始日は必須です' });
    }

    if (validationErrors.length > 0) {
      return createValidationErrorResponse(validationErrors);
    }

    // 日付の妥当性チェック
    const startDate = new Date(body.start_date);
    const endDate = body.end_date ? new Date(body.end_date) : null;
    
    if (endDate && startDate > endDate) {
      return createErrorResponse(
        'INVALID_DATE_RANGE',
        '開始日は終了日より前である必要があります',
        undefined,
        400
      );
    }

    // プロジェクトコードの重複チェック
    if (!employeeId) {
      return createErrorResponse(
        'EMPLOYEE_ID_REQUIRED',
        '従業員IDが必要です',
        undefined,
        400
      );
    }
    
    const existingProject = await prisma.projectRecord.findFirst({
      where: {
        employee_id: employeeId,
        project_code: body.project_code,
        is_deleted: false
      }
    });

    if (existingProject) {
      return createErrorResponse(
        'DUPLICATE_PROJECT_CODE',
        '同じプロジェクトコードの実績が既に存在します',
        `プロジェクトコード: ${body.project_code}`,
        409
      );
    }

    // 新規作業実績の作成
    const recordId = `PR_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    console.log('Work POST - Creating record with ID:', recordId);
    
    const newRecord = await prisma.projectRecord.create({
      data: {
        id: recordId,  // 主キーとして必須
        project_record_id: recordId,
        employee_id: employeeId,
        project_name: body.project_name,
        project_code: body.project_code,
        role_title: body.role,  // DBカラム名に合わせる
        start_date: startDate,
        end_date: endDate,
        project_status: body.status || 'active',  // DBカラム名に合わせる
        responsibilities: body.description || '',  // DBカラム名に合わせる
        technologies_used: body.technologies ? JSON.stringify(body.technologies) : '',  // DBカラム名に合わせる
        achievements: body.achievements ? JSON.stringify(body.achievements) : '',  // DBカラム名に合わせる
        team_size: body.team_size || 1,
        tenant_id: 'default',  // 必須フィールド
        is_deleted: false,
        created_by: employeeId,
        updated_by: employeeId,  // 必須フィールド
        created_at: new Date(),
        updated_at: new Date()
      }
    });

    return createSuccessResponse({
      id: newRecord.project_record_id,
      message: '作業実績を登録しました'
    }, 201);

  } catch (error) {
    console.error('作業実績登録エラー - 詳細:', {
      error: error,
      message: error instanceof Error ? error.message : '不明なエラー',
      stack: error instanceof Error ? error.stack : undefined
    });
    return createErrorResponse(
      'INTERNAL_SERVER_ERROR',
      'サーバーエラーが発生しました',
      error instanceof Error ? error.message : '不明なエラー',
      500
    );
  }
}

// 作業実績更新API
export async function PUT(request: NextRequest) {
  try {
    // 認証チェック（オプショナル）
    const authResult = await verifyAuth(request);
    
    // トークンがない場合はデフォルトユーザーを使用（開発用）
    const employeeId = authResult.success 
      ? (authResult.employeeId || authResult.userId)
      : '000001';
    
    console.log('Work PUT - employeeId:', employeeId, 'authResult:', authResult);

    const body = await request.json();

    // 必須項目のバリデーション
    if (!body.id) {
      return createErrorResponse(
        'INVALID_PARAMETER',
        '更新対象のIDが指定されていません',
        undefined,
        400
      );
    }

    // 既存レコードの確認
    if (!employeeId) {
      return createErrorResponse(
        'EMPLOYEE_ID_REQUIRED',
        '従業員IDが必要です',
        undefined,
        400
      );
    }
    
    const existingRecord = await prisma.projectRecord.findFirst({
      where: {
        project_record_id: body.id,
        employee_id: employeeId,
        is_deleted: false
      }
    });

    if (!existingRecord) {
      return createNotFoundErrorResponse('指定された作業実績が見つかりません');
    }

    // 日付の妥当性チェック
    if (body.start_date && body.end_date) {
      const startDate = new Date(body.start_date);
      const endDate = new Date(body.end_date);
      
      if (startDate > endDate) {
        return createErrorResponse(
          'INVALID_DATE_RANGE',
          '開始日は終了日より前である必要があります',
          undefined,
          400
        );
      }
    }

    // プロジェクトコードの重複チェック（自分以外）
    if (body.project_code && body.project_code !== existingRecord.project_code) {
      const duplicateProject = await prisma.projectRecord.findFirst({
        where: {
          employee_id: employeeId,
          project_code: body.project_code,
          project_record_id: { not: body.id },
          is_deleted: false
        }
      });

      if (duplicateProject) {
        return createErrorResponse(
          'DUPLICATE_PROJECT_CODE',
          '同じプロジェクトコードの実績が既に存在します',
          `プロジェクトコード: ${body.project_code}`,
          409
        );
      }
    }

    // 更新データの準備
    const updateData: any = {
      updated_by: employeeId,
      updated_at: new Date()
    };

    // 更新可能なフィールドのマッピング
    const fieldMapping: { [key: string]: string } = {
      'project_name': 'project_name',
      'project_code': 'project_code',
      'role': 'role_title',
      'start_date': 'start_date',
      'end_date': 'end_date',
      'status': 'project_status',
      'description': 'responsibilities',
      'technologies': 'technologies_used',
      'achievements': 'achievements',
      'team_size': 'team_size'
    };

    Object.keys(fieldMapping).forEach(apiField => {
      const dbField = fieldMapping[apiField];
      if (dbField && body[apiField] !== undefined) {
        if (apiField === 'start_date' || apiField === 'end_date') {
          updateData[dbField] = body[apiField] ? new Date(body[apiField]) : null;
        } else if (apiField === 'technologies' || apiField === 'achievements') {
          updateData[dbField] = body[apiField] ? JSON.stringify(body[apiField]) : '';
        } else {
          updateData[dbField] = body[apiField];
        }
      }
    });

    // 作業実績の更新
    const updatedRecord = await prisma.projectRecord.update({
      where: {
        project_record_id: body.id
      },
      data: updateData
    });

    return createSuccessResponse({
      id: updatedRecord.project_record_id,
      message: '作業実績を更新しました'
    });

  } catch (error) {
    console.error('作業実績更新エラー:', error);
    return createErrorResponse(
      'INTERNAL_SERVER_ERROR',
      'サーバーエラーが発生しました',
      error instanceof Error ? error.message : '不明なエラー',
      500
    );
  }
}

// 作業実績削除API
export async function DELETE(request: NextRequest) {
  try {
    // 認証チェック（オプショナル）
    const authResult = await verifyAuth(request);
    
    // トークンがない場合はデフォルトユーザーを使用（開発用）
    const employeeId = authResult.success 
      ? (authResult.employeeId || authResult.userId)
      : '000001';
    
    console.log('Work DELETE - employeeId:', employeeId, 'authResult:', authResult);

    const { searchParams } = new URL(request.url);
    const id = searchParams.get('id');

    if (!id) {
      return createErrorResponse(
        'INVALID_PARAMETER',
        '削除対象のIDが指定されていません',
        undefined,
        400
      );
    }

    // 既存レコードの確認
    if (!employeeId) {
      return createErrorResponse(
        'EMPLOYEE_ID_REQUIRED',
        '従業員IDが必要です',
        undefined,
        400
      );
    }
    
    const existingRecord = await prisma.projectRecord.findFirst({
      where: {
        project_record_id: id,
        employee_id: employeeId,
        is_deleted: false
      }
    });

    if (!existingRecord) {
      return createNotFoundErrorResponse('指定された作業実績が見つかりません');
    }

    // 論理削除
    await prisma.projectRecord.update({
      where: {
        project_record_id: id
      },
      data: {
        is_deleted: true,
        updated_by: employeeId,
        updated_at: new Date()
      }
    });

    return createSuccessResponse({
      message: '作業実績を削除しました'
    });

  } catch (error) {
    console.error('作業実績削除エラー:', error);
    return createErrorResponse(
      'INTERNAL_SERVER_ERROR',
      'サーバーエラーが発生しました',
      error instanceof Error ? error.message : '不明なエラー',
      500
    );
  }
}