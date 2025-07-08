/**
 * 要求仕様ID: TRN.1-ATT.1
 * 対応設計書: docs/design/api/specs/API定義書_API-054_資格情報登録API.md
 * 実装内容: 資格情報を登録するAPI
 */
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { createErrorResponse, createSuccessResponse } from '@/lib/api-utils';

/**
 * 資格情報登録API
 * 
 * @param request - リクエスト
 * @returns 登録結果
 */
export async function POST(request: NextRequest) {
  try {
    // リクエストボディの取得
    const body = await request.json();
    
    // 必須項目の検証
    const requiredFields = ['employee_id', 'certification_id', 'activity_name', 'activity_date', 'pdu_points'];
    const missingFields = requiredFields.filter(field => !body[field]);
    
    if (missingFields.length > 0) {
      return createErrorResponse(
        'INVALID_PARAMETER',
        '必須項目が不足しています',
        `Missing fields: ${missingFields.join(', ')}`,
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
    
    // 資格の存在確認
    const certification = await prisma.certification.findUnique({
      where: { certification_code: body.certification_id }
    });
    
    if (!certification) {
      return createErrorResponse(
        'CERTIFICATION_NOT_FOUND',
        '指定された資格が見つかりません',
        `Certification ID: ${body.certification_id}`,
        404
      );
    }
    
    // 日付の検証
    const activityDate = new Date(body.activity_date);
    
    if (isNaN(activityDate.getTime())) {
      return createErrorResponse(
        'INVALID_PARAMETER',
        '無効な日付形式です',
        'Invalid date format',
        400
      );
    }
    
    // PDUポイントの検証
    if (typeof body.pdu_points !== 'number' || body.pdu_points <= 0) {
      return createErrorResponse(
        'INVALID_PARAMETER',
        'PDUポイントは正の数値である必要があります',
        `PDU Points: ${body.pdu_points}`,
        400
      );
    }
    
    // PDU IDの生成
    const pduId = `PDU-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
    
    // 現在のユーザー情報（実際の実装では認証情報から取得）
    const currentUser = 'system'; // 仮の値
    
    // PDU情報の登録
    const pdu = await prisma.pDU.create({
      data: {
        id: pduId,
        pdu_id: pduId,
        employee_id: body.employee_id,
        certification_id: body.certification_id,
        activity_type: body.activity_type || 'OTHER',
        activity_name: body.activity_name,
        activity_description: body.activity_description,
        provider_name: body.provider_name,
        activity_date: activityDate,
        duration_hours: body.duration_hours,
        pdu_points: body.pdu_points,
        pdu_category: body.pdu_category || 'EDUCATION',
        evidence_type: body.evidence_type,
        certificate_number: body.certificate_number,
        approval_status: body.approval_status || 'PENDING',
        related_training_id: body.related_training_id,
        tenant_id: body.tenant_id || 'default',
        created_by: currentUser,
        updated_by: currentUser,
        is_deleted: false
      }
    });
    
    // レスポンスの構築
    return createSuccessResponse({
      message: '資格情報が正常に登録されました',
      pdu: {
        id: pdu.id,
        pdu_id: pdu.pdu_id,
        employee_id: pdu.employee_id,
        certification_id: pdu.certification_id,
        activity_name: pdu.activity_name,
        activity_date: pdu.activity_date,
        pdu_points: pdu.pdu_points,
        approval_status: pdu.approval_status,
        created_at: pdu.created_at
      }
    }, 201);
  } catch (error) {
    console.error('資格情報登録エラー:', error);
    return createErrorResponse(
      'SYSTEM_ERROR',
      'システムエラーが発生しました',
      error instanceof Error ? error.message : '不明なエラー',
      500
    );
  }
}
