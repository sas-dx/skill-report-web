// 要求仕様ID: ACC.1-AUTH.1 - ユーザー認証API
import { NextRequest, NextResponse } from 'next/server';
import jwt from 'jsonwebtoken';

// モックユーザーデータ（デモ用）
const mockUsers = [
  {
    id: '1',
    empNo: 'EMP001',
    email: 'test.user@example.com',
    name: '山田太郎',
    nameKana: 'ヤマダタロウ',
    password: 'password123',
    isActive: true,
    department: { name: '開発部' },
    position: { name: 'エンジニア' },
    deptId: 'DEPT001',
    positionId: 'POS001',
  },
  {
    id: '2',
    empNo: 'admin',
    email: 'admin@example.com',
    name: '管理者',
    nameKana: 'カンリシャ',
    password: 'admin123',
    isActive: true,
    department: { name: '管理部' },
    position: { name: '管理者' },
    deptId: 'DEPT002',
    positionId: 'POS002',
  },
];

export async function POST(request: NextRequest) {
  try {
    const { empNo, password } = await request.json();

    console.log('Login attempt:', { empNo, password }); // デバッグ用

    // 入力値検証
    if (!empNo || !password) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message: '社員番号とパスワードは必須です',
          },
        },
        { status: 400 }
      );
    }

    // モックユーザー検索
    const user = mockUsers.find(u => u.empNo === empNo && u.isActive);

    if (!user) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'AUTHENTICATION_ERROR',
            message: '社員番号またはパスワードが正しくありません',
          },
        },
        { status: 401 }
      );
    }

    // パスワード検証
    const isValidPassword = password === user.password;
    
    if (!isValidPassword) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'AUTHENTICATION_ERROR',
            message: '社員番号またはパスワードが正しくありません',
          },
        },
        { status: 401 }
      );
    }

    // JWTトークン生成
    const token = jwt.sign(
      {
        userId: user.id,
        empNo: user.empNo,
        email: user.email,
        name: user.name,
        deptId: user.deptId,
        positionId: user.positionId,
      },
      process.env.JWT_SECRET || 'fallback-secret',
      { expiresIn: '8h' }
    );

    console.log('Login successful for:', user.empNo); // デバッグ用

    // レスポンス
    return NextResponse.json(
      {
        success: true,
        data: {
          token,
          user: {
            id: user.id,
            empNo: user.empNo,
            email: user.email,
            name: user.name,
            nameKana: user.nameKana,
            department: user.department?.name || null,
            position: user.position?.name || null,
          },
        },
        timestamp: new Date().toISOString(),
      },
      { status: 200 }
    );
  } catch (error) {
    console.error('Login API Error:', error);
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'INTERNAL_SERVER_ERROR',
          message: 'システムエラーが発生しました',
        },
      },
      { status: 500 }
    );
  }
}
