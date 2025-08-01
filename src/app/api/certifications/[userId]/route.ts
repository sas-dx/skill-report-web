/**
 * 要求仕様ID: TRN.1-ATT.1
 * 対応設計書: docs/design/api/specs/API定義書_API-053_資格情報取得API.md
 * 実装内容: ユーザーIDに基づいて資格情報を取得するAPI
 */
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { createErrorResponse, createSuccessResponse } from '@/lib/api-utils';

/**
 * 資格情報取得API
 * 
 * @param request - リクエスト
 * @param params - URLパラメータ（ユーザーID）
 * @returns 資格情報一覧
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
    const certificationId = searchParams.get('certification_id');
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
      
      whereCondition.activity_date = {
        gte: startDate,
        lt: endDate
      };
    }
    
    // 資格IDフィルター
    if (certificationId) {
      whereCondition.certification_id = certificationId;
    }
    
    // ステータスフィルター
    if (status) {
      whereCondition.approval_status = status;
    }
    
    // 資格情報の取得
    const certifications = await prisma.pDU.findMany({
      where: whereCondition,
      orderBy: {
        activity_date: 'desc'
      },
      skip: offset,
      take: limit
    });
    
    // 資格マスタ情報の取得
    const certificationIds = [...new Set(certifications.map(cert => cert.certification_id).filter(Boolean) as string[])];
    const certificationMasters = await prisma.certification.findMany({
      where: {
        certification_code: {
          in: certificationIds.length > 0 ? certificationIds : ['dummy']
        }
      }
    });
    
    // 資格マスタ情報のマッピング
    const certificationMap = new Map();
    certificationMasters.forEach(cert => {
      certificationMap.set(cert.certification_code, cert);
    });
    
    // 総件数の取得
    const totalCount = await prisma.pDU.count({
      where: whereCondition
    });
    
    // 資格情報が見つからない場合でも空配列を返す
    if (certifications.length === 0) {
      console.log(`資格情報が見つかりません: Employee ID: ${userId}, Filters: ${JSON.stringify({ year, certificationId, status })}`);
      // 404ではなく空の配列を返す
      return createSuccessResponse({
        certifications: [],
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
      certifications: certifications.map(cert => ({
        id: cert.id,
        pdu_id: cert.pdu_id,
        employee_id: cert.employee_id,
        certification_id: cert.certification_id,
        certification_name: certificationMap.get(cert.certification_id)?.certification_name,
        certification_provider: certificationMap.get(cert.certification_id)?.certification_provider,
        certification_level: certificationMap.get(cert.certification_id)?.certification_level,
        activity_type: cert.activity_type,
        activity_name: cert.activity_name,
        activity_date: cert.activity_date,
        pdu_points: cert.pdu_points,
        pdu_category: cert.pdu_category,
        approval_status: cert.approval_status,
        certificate_number: cert.certificate_number,
        created_at: cert.created_at
      })),
      pagination: {
        total: totalCount,
        offset: offset,
        limit: limit,
        has_more: offset + certifications.length < totalCount
      }
    });
  } catch (error) {
    console.error('資格情報取得エラー:', error);
    return createErrorResponse(
      'SYSTEM_ERROR',
      'システムエラーが発生しました',
      error instanceof Error ? error.message : '不明なエラー',
      500
    );
  }
}
