// 要求仕様ID: ACC.1-AUTH.1 - ユーザー認証API
import { NextRequest, NextResponse } from 'next/server';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export async function POST(request: NextRequest) {
  try {
    const { loginId, password } = await request.json();

    console.log('Login attempt:', { 
      loginId, 
      passwordReceived: !!password,
      passwordLength: password?.length || 0 
    }); // パスワードの内容ではなく、受信状況のみログ出力

    // 入力値検証
    if (!loginId || !password) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message: 'ログインIDとパスワードは必須です',
          },
        },
        { status: 400 }
      );
    }

    // UserAuthテーブルのみを使用してシンプルに認証
    const userAuth = await prisma.userAuth.findFirst({
      where: {
        login_id: loginId,
        account_status: 'ACTIVE',
      },
    });

    console.log('User lookup result:', {
      loginId,
      userFound: !!userAuth,
      userId: userAuth?.user_id,
      hasPasswordHash: !!userAuth?.password_hash,
      accountStatus: userAuth?.account_status
    });

    if (!userAuth) {
      console.log('User not found or inactive for loginId:', loginId);
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'AUTHENTICATION_ERROR',
            message: 'ログインIDまたはパスワードが正しくありません',
          },
        },
        { status: 401 }
      );
    }

    // パスワード検証（bcryptハッシュ比較）
    const isValidPassword = await bcrypt.compare(password, userAuth.password_hash || '');
    
    console.log('Password validation:', {
      loginId,
      passwordProvided: !!password,
      hashExists: !!userAuth.password_hash,
      isValidPassword
    });
    
    if (!isValidPassword) {
      console.log('Password validation failed for loginId:', loginId);
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'AUTHENTICATION_ERROR',
            message: 'ログインIDまたはパスワードが正しくありません',
          },
        },
        { status: 401 }
      );
    }

    // ログイン成功時の処理
    await prisma.userAuth.update({
      where: { user_id: userAuth.user_id },
      data: {
        last_login_at: new Date(),
        failed_login_count: 0,
      },
    });

    // 実際のユーザー情報を取得（Employeeテーブルから）
    let employeeInfo = null;
    let departmentInfo = null;
    let positionInfo = null;
    
    if (userAuth.employee_id) {
      try {
        employeeInfo = await prisma.employee.findUnique({
          where: { employee_code: userAuth.employee_id }
        });
        
        // 部署情報を取得
        if (employeeInfo?.department_id) {
          departmentInfo = await prisma.department.findUnique({
            where: { department_code: employeeInfo.department_id }
          });
        }
        
        // 役職情報を取得
        if (employeeInfo?.position_id) {
          positionInfo = await prisma.position.findUnique({
            where: { position_code: employeeInfo.position_id }
          });
        }
      } catch (error) {
        console.log('Employee info fetch failed:', error);
      }
    }

    // JWTトークン生成（ダッシュボードAPIと整合性を保つ）
    const token = jwt.sign(
      {
        userId: userAuth.user_id,
        employeeId: userAuth.employee_id,
        employeeCode: userAuth.employee_id, // employee_idをemployeeCodeとしても使用
        email: employeeInfo?.email || '',
      },
      process.env.JWT_SECRET || 'fallback-secret',
      { expiresIn: '8h' }
    );

    console.log('Login successful for:', userAuth.login_id);

    // レスポンス（実際のユーザー情報を含める）
    const response = NextResponse.json(
      {
        success: true,
        data: {
          token,
          user: {
            id: userAuth.user_id,
            loginId: userAuth.login_id,
            employeeId: userAuth.employee_id,
            name: employeeInfo?.full_name || userAuth.login_id,
            nameKana: employeeInfo?.full_name_kana || '',
            email: employeeInfo?.email || '',
            department: departmentInfo?.department_name || '',
            position: positionInfo?.position_name || '',
            lastLoginAt: userAuth.last_login_at,
          },
        },
        timestamp: new Date().toISOString(),
      },
      { status: 200 }
    );

    // 認証トークンをhttpOnlyクッキーに設定
    response.cookies.set('auth-token', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 8 * 60 * 60, // 8時間
      path: '/'
    });

    return response;
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
  } finally {
    await prisma.$disconnect();
  }
}
