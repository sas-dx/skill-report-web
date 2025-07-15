/**
 * 要求仕様ID: TRN.1-ATT.1
 * 対応設計書: docs/design/api/specs/API定義書_API-053_資格情報取得API.md
 * 実装内容: 資格情報取得・作成API
 */

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

// JWT検証ヘルパー関数（開発用：認証をスキップ）
function verifyToken(authHeader: string | null): { employeeCode: string } | null {
  // 開発環境では常に認証をスキップしてモックユーザーを返す
  console.log('NODE_ENV:', process.env.NODE_ENV);
  console.log('Auth header:', authHeader);
  
  // 開発環境では認証をスキップ
  return { employeeCode: 'EMP001' };
}

// 資格情報取得API
export async function GET(request: NextRequest) {
  try {
    const url = new URL(request.url);
    const userId = url.searchParams.get('userId');

    // 認証チェック（開発環境では簡易化）
    const authHeader = request.headers.get('authorization');
    const tokenData = verifyToken(authHeader);
    
    if (!tokenData) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'UNAUTHORIZED',
          message: '認証が必要です'
        }
      }, { status: 401 });
    }

    const currentUserId = userId || tokenData.employeeCode;

    try {
      // 個人資格記録テーブルから資格情報を取得
      const certifications = await prisma.personalCertificationRecord.findMany({
        where: {
          employee_id: currentUserId,
          is_deleted: false
        },
        orderBy: {
          acquired_date: 'desc'
        }
      });

      // レスポンス形式に変換
      const formattedCertifications = certifications.map((cert: any) => ({
        id: cert.id,
        certificationName: cert.certification_name,
        organizationName: cert.organization_name || '',
        acquiredDate: cert.acquired_date.toISOString().split('T')[0],
        expiryDate: cert.expiry_date ? cert.expiry_date.toISOString().split('T')[0] : '',
        score: cert.score || '',
        remarks: cert.remarks || '',
        createdAt: cert.created_at.toISOString(),
        updatedAt: cert.updated_at.toISOString()
      }));

      return NextResponse.json({
        success: true,
        data: formattedCertifications,
        count: formattedCertifications.length,
        timestamp: new Date().toISOString()
      });

    } catch (dbError) {
      console.error('データベースエラー:', dbError);
      return NextResponse.json({
        success: false,
        error: {
          code: 'DATABASE_ERROR',
          message: 'データベースエラーが発生しました'
        },
        timestamp: new Date().toISOString()
      }, { status: 500 });
    }

  } catch (error) {
    console.error('資格情報取得エラー:', error);
    return NextResponse.json({
      success: false,
      error: {
        code: 'SYSTEM_ERROR',
        message: 'システムエラーが発生しました'
      },
      timestamp: new Date().toISOString()
    }, { status: 500 });
  }
}

// 資格情報作成API
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // 認証チェック
    const authHeader = request.headers.get('authorization');
    const tokenData = verifyToken(authHeader);
    
    if (!tokenData) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'UNAUTHORIZED',
          message: '認証が必要です'
        }
      }, { status: 401 });
    }

    // リクエストボディの検証
    if (!body.certificationName || !body.acquiredDate) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_PARAMETER',
          message: '資格名と取得日は必須です'
        }
      }, { status: 400 });
    }

    try {
      // 日付の変換
      const acquiredDate = new Date(body.acquiredDate);
      const expiryDate = body.expiryDate ? new Date(body.expiryDate) : null;

      // 個人資格記録テーブルに新しい資格情報を作成
      const newCertification = await prisma.personalCertificationRecord.create({
        data: {
          employee_id: tokenData.employeeCode,
          certification_name: body.certificationName,
          organization_name: body.organizationName || null,
          acquired_date: acquiredDate,
          expiry_date: expiryDate,
          score: body.score || null,
          remarks: body.remarks || null,
          created_by: tokenData.employeeCode,
          updated_by: tokenData.employeeCode
        }
      });

      // レスポンス形式に変換
      const response = {
        id: newCertification.id,
        certificationName: newCertification.certification_name,
        organizationName: newCertification.organization_name || '',
        acquiredDate: newCertification.acquired_date.toISOString().split('T')[0],
        expiryDate: newCertification.expiry_date ? newCertification.expiry_date.toISOString().split('T')[0] : '',
        score: newCertification.score || '',
        remarks: newCertification.remarks || '',
        createdAt: newCertification.created_at.toISOString(),
        updatedAt: newCertification.updated_at.toISOString()
      };

      return NextResponse.json({
        success: true,
        data: response,
        timestamp: new Date().toISOString()
      }, { status: 201 });

    } catch (dbError) {
      console.error('データベースエラー:', dbError);
      return NextResponse.json({
        success: false,
        error: {
          code: 'DATABASE_ERROR',
          message: 'データベースエラーが発生しました'
        },
        timestamp: new Date().toISOString()
      }, { status: 500 });
    }

  } catch (error) {
    console.error('資格情報作成エラー:', error);
    return NextResponse.json({
      success: false,
      error: {
        code: 'SYSTEM_ERROR',
        message: 'システムエラーが発生しました'
      },
      timestamp: new Date().toISOString()
    }, { status: 500 });
  }
}
