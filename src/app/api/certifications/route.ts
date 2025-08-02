/**
 * 要求仕様ID: TRN.1-ATT.1
 * 対応設計書: docs/design/api/specs/API定義書_API-053_資格情報取得API.md
 * 実装内容: 資格情報管理API（TRN_PDUテーブル使用）
 */

import { NextRequest, NextResponse } from 'next/server';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// 資格情報の型定義（TRN_PDUテーブルベース）
interface CertificationRecord {
  id: string;
  employee_id: string;
  certification_name: string;
  issuing_organization: string;
  category: string;
  level: string;
  status: 'acquired' | 'expired' | 'planned';
  acquisition_date?: string | undefined;
  expiry_date?: string | undefined;
  planned_date?: string | undefined;
  certification_number?: string | undefined;
  score?: number | undefined;
  description: string;
  tenant_id: string;
  created_at: string;
  updated_at: string;
}

// GET: 資格情報取得
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const employeeId = searchParams.get('employee_id') || 'emp_001';
    const category = searchParams.get('category');
    const status = searchParams.get('status');
    const year = searchParams.get('year');

    console.log('資格情報取得API呼び出し:', { employeeId, category, status, year });

    // TRN_PDUテーブルから資格情報を取得
    const whereConditions: any = {
      employee_id: employeeId,
      is_deleted: false,
      // 資格関連のPDUのみを取得（activity_typeで判定）
      activity_type: {
        in: ['certification', 'exam', 'license']
      }
    };

    if (category) {
      whereConditions.pdu_category = category;
    }

    if (year) {
      const startDate = new Date(`${year}-01-01`);
      const endDate = new Date(`${year}-12-31`);
      whereConditions.activity_date = {
        gte: startDate,
        lte: endDate
      };
    }

    const pduRecords = await prisma.pDU.findMany({
      where: whereConditions,
      orderBy: {
        activity_date: 'desc'
      }
    });

    // TRN_PDUのデータをCertificationRecord形式に変換
    const certifications: CertificationRecord[] = pduRecords.map(pdu => ({
      id: pdu.id,
      employee_id: pdu.employee_id || '',
      certification_name: pdu.activity_name || '',
      issuing_organization: pdu.provider_name || '',
      category: pdu.pdu_category || 'other',
      level: 'basic', // PDUテーブルにはレベル情報がないため固定値
      status: pdu.approval_status === 'approved' ? 'acquired' : 'planned',
      acquisition_date: pdu.activity_date?.toISOString().split('T')[0] || undefined,
      expiry_date: pdu.expiry_date?.toISOString().split('T')[0] || undefined,
      certification_number: pdu.certificate_number || undefined,
      score: undefined, // PDUテーブルにはスコア情報がない
      description: pdu.activity_description || '',
      tenant_id: pdu.tenant_id,
      created_at: pdu.created_at.toISOString(),
      updated_at: pdu.updated_at.toISOString()
    }));

    // ステータスでフィルタリング（変換後に実行）
    const filteredCertifications = status 
      ? certifications.filter(cert => cert.status === status)
      : certifications;

    return NextResponse.json({
      success: true,
      data: {
        total: filteredCertifications.length,
        page: 1,
        per_page: 20,
        total_pages: 1,
        certifications: filteredCertifications
      }
    });

  } catch (error) {
    console.error('資格情報取得エラー:', error);
    return NextResponse.json({
      success: false,
      error: {
        code: 'SYSTEM_ERROR',
        message: 'システムエラーが発生しました',
        details: error instanceof Error ? error.message : '不明なエラー'
      }
    }, { status: 500 });
  } finally {
    await prisma.$disconnect();
  }
}

// POST: 資格情報登録・更新
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    console.log('資格情報登録API呼び出し:', body);

    // バリデーション
    if (!body.certification_name || !body.issuing_organization) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: '必須項目が不足しています',
          details: '資格名と発行機関は必須です'
        }
      }, { status: 400 });
    }

    // TRN_PDUテーブルに資格情報を保存
    const pduData = {
      id: `pdu-cert-${Date.now()}`,
      pdu_id: `PDU-CERT-${Date.now()}`,
      employee_id: body.employee_id || 'emp_001',
      certification_id: body.certification_id || null,
      activity_type: 'certification',
      activity_name: body.certification_name,
      activity_description: body.description || '',
      provider_name: body.issuing_organization,
      activity_date: body.acquisition_date ? new Date(body.acquisition_date) : new Date(),
      duration_hours: 0, // 資格取得の場合は0
      pdu_points: 0, // 必要に応じて設定
      pdu_category: body.category || 'technical',
      pdu_subcategory: body.level || 'basic',
      certificate_number: body.certification_number || null,
      approval_status: body.status === 'acquired' ? 'approved' : 'pending',
      expiry_date: body.expiry_date ? new Date(body.expiry_date) : null,
      tenant_id: body.tenant_id || 'default',
      created_by: body.employee_id || 'emp_001',
      updated_by: body.employee_id || 'emp_001'
    };

    const newPDU = await prisma.pDU.create({
      data: pduData
    });

    console.log('資格情報登録成功:', newPDU);

    // レスポンス用にCertificationRecord形式に変換
    const certificationResponse: CertificationRecord = {
      id: newPDU.id,
      employee_id: newPDU.employee_id || '',
      certification_name: newPDU.activity_name || '',
      issuing_organization: newPDU.provider_name || '',
      category: newPDU.pdu_category || 'other',
      level: newPDU.pdu_subcategory || 'basic',
      status: newPDU.approval_status === 'approved' ? 'acquired' : 'planned',
      acquisition_date: newPDU.activity_date?.toISOString().split('T')[0] || undefined,
      expiry_date: newPDU.expiry_date?.toISOString().split('T')[0] || undefined,
      certification_number: newPDU.certificate_number || undefined,
      description: newPDU.activity_description || '',
      tenant_id: newPDU.tenant_id,
      created_at: newPDU.created_at.toISOString(),
      updated_at: newPDU.updated_at.toISOString()
    };

    return NextResponse.json({
      success: true,
      data: {
        certification: certificationResponse
      }
    }, { status: 201 });

  } catch (error) {
    console.error('資格情報登録エラー:', error);
    return NextResponse.json({
      success: false,
      error: {
        code: 'SYSTEM_ERROR',
        message: 'システムエラーが発生しました',
        details: error instanceof Error ? error.message : '不明なエラー'
      }
    }, { status: 500 });
  } finally {
    await prisma.$disconnect();
  }
}

// PUT: 資格情報更新
export async function PUT(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const certificationId = searchParams.get('id');
    const body = await request.json();

    if (!certificationId) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: '資格IDが必要です'
        }
      }, { status: 400 });
    }

    console.log('資格情報更新API呼び出し:', { certificationId, body });

    // バリデーション
    if (!body.certification_name || !body.issuing_organization) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: '必須項目が不足しています',
          details: '資格名と発行機関は必須です'
        }
      }, { status: 400 });
    }

    // 既存の資格情報を確認
    const existingPDU = await prisma.pDU.findUnique({
      where: { id: certificationId }
    });

    if (!existingPDU) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'NOT_FOUND',
          message: '指定された資格情報が見つかりません'
        }
      }, { status: 404 });
    }

    // TRN_PDUテーブルの資格情報を更新
    const updatedPDU = await prisma.pDU.update({
      where: { id: certificationId },
      data: {
        activity_name: body.certification_name,
        activity_description: body.description || '',
        provider_name: body.issuing_organization,
        activity_date: body.acquisition_date ? new Date(body.acquisition_date) : existingPDU.activity_date,
        pdu_category: body.category || existingPDU.pdu_category,
        pdu_subcategory: body.level || existingPDU.pdu_subcategory,
        certificate_number: body.certification_number || existingPDU.certificate_number,
        approval_status: body.status === 'acquired' ? 'approved' : 'pending',
        expiry_date: body.expiry_date ? new Date(body.expiry_date) : existingPDU.expiry_date,
        updated_by: body.employee_id || 'emp_001',
        updated_at: new Date()
      }
    });

    console.log('資格情報更新成功:', updatedPDU);

    // レスポンス用にCertificationRecord形式に変換
    const certificationResponse: CertificationRecord = {
      id: updatedPDU.id,
      employee_id: updatedPDU.employee_id || '',
      certification_name: updatedPDU.activity_name || '',
      issuing_organization: updatedPDU.provider_name || '',
      category: updatedPDU.pdu_category || 'other',
      level: updatedPDU.pdu_subcategory || 'basic',
      status: updatedPDU.approval_status === 'approved' ? 'acquired' : 'planned',
      acquisition_date: updatedPDU.activity_date?.toISOString().split('T')[0] || undefined,
      expiry_date: updatedPDU.expiry_date?.toISOString().split('T')[0] || undefined,
      certification_number: updatedPDU.certificate_number || undefined,
      description: updatedPDU.activity_description || '',
      tenant_id: updatedPDU.tenant_id,
      created_at: updatedPDU.created_at.toISOString(),
      updated_at: updatedPDU.updated_at.toISOString()
    };

    return NextResponse.json({
      success: true,
      data: {
        certification: certificationResponse
      }
    });

  } catch (error) {
    console.error('資格情報更新エラー:', error);
    return NextResponse.json({
      success: false,
      error: {
        code: 'SYSTEM_ERROR',
        message: 'システムエラーが発生しました',
        details: error instanceof Error ? error.message : '不明なエラー'
      }
    }, { status: 500 });
  } finally {
    await prisma.$disconnect();
  }
}

// DELETE: 資格情報削除
export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const certificationId = searchParams.get('id');

    if (!certificationId) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: '資格IDが必要です'
        }
      }, { status: 400 });
    }

    // TRN_PDUテーブルから資格情報を論理削除
    const existingPDU = await prisma.pDU.findUnique({
      where: { id: certificationId }
    });

    if (!existingPDU) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'NOT_FOUND',
          message: '指定された資格情報が見つかりません'
        }
      }, { status: 404 });
    }

    await prisma.pDU.update({
      where: { id: certificationId },
      data: {
        is_deleted: true,
        updated_at: new Date()
      }
    });

    return NextResponse.json({
      success: true,
      data: {
        message: '資格情報を削除しました'
      }
    });

  } catch (error) {
    console.error('資格情報削除エラー:', error);
    return NextResponse.json({
      success: false,
      error: {
        code: 'SYSTEM_ERROR',
        message: 'システムエラーが発生しました',
        details: error instanceof Error ? error.message : '不明なエラー'
      }
    }, { status: 500 });
  } finally {
    await prisma.$disconnect();
  }
}
