/**
 * ログインAPI
 * 要求仕様ID: TNT.3-AUTH.1, ACC.1-AUTH.1
 * マルチテナント対応版
 */

import { NextRequest, NextResponse } from 'next/server';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import { prisma } from '@/lib/prisma';
import { getTenantFromRequest } from '@/lib/tenant-context';

export async function POST(request: NextRequest) {
  try {
    const { loginId, password, tenantCode } = await request.json();

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

    // テナント情報を取得
    let tenantId: string | null = null;
    
    if (tenantCode) {
      const tenant = await prisma.tenant.findFirst({
        where: {
          tenant_code: tenantCode,
          is_deleted: false
        }
      });
      
      if (tenant) {
        tenantId = tenant.tenant_id;
      }
    } else {
      // リクエストからテナント情報を取得
      const tenantContext = await getTenantFromRequest(request);
      if (tenantContext) {
        tenantId = tenantContext.tenantId;
      }
    }
    
    if (!tenantId) {
      // デフォルトテナントを使用（開発用）
      const defaultTenant = await prisma.tenant.findFirst({
        where: {
          tenant_code: 'DEFAULT'
        }
      });
      
      if (defaultTenant) {
        tenantId = defaultTenant.tenant_id;
      } else {
        return NextResponse.json(
          {
            success: false,
            error: {
              code: 'TENANT_NOT_FOUND',
              message: 'テナントが特定できません',
            },
          },
          { status: 400 }
        );
      }
    }
    
    // UserAuthテーブルを使用して認証
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

    // テナント情報を取得
    const tenant = await prisma.tenant.findUnique({
      where: { tenant_id: tenantId }
    });
    
    // ユーザーロールを取得
    const userRole = await prisma.userRole.findFirst({
      where: {
        user_id: userAuth.user_id,
        is_deleted: false
      }
    });
    
    let roleName = 'user';
    let permissions: string[] = [];
    
    if (userRole) {
      const role = await prisma.role.findFirst({
        where: { role_code: userRole.role_id }
      });
      
      if (role) {
        roleName = role.role_code || 'user';
        
        // 権限情報を取得
        const rolePermissions = await prisma.rolePermission.findMany({
          where: {
            role_id: role.role_code,
            is_deleted: false
          }
        });
        
        for (const rp of rolePermissions) {
          if (rp.permission_id) {
            permissions.push(rp.permission_id);
          }
        }
      }
    }
    
    // JWTトークン生成（テナント情報を含む）
    const token = jwt.sign(
      {
        loginId: userAuth.login_id,
        employeeId: userAuth.employee_id,
        userId: userAuth.user_id,
        tenantId: tenantId,
        tenantCode: tenant?.tenant_code || '',
        role: roleName,
        permissions
      },
      process.env.JWT_SECRET || 'fallback-secret',
      { expiresIn: '24h' }
    );
    
    // リフレッシュトークンも生成
    const refreshToken = jwt.sign(
      {
        userId: userAuth.user_id,
        tenantId: tenantId,
        type: 'refresh'
      },
      process.env.JWT_SECRET || 'fallback-secret',
      { expiresIn: '7d' }
    );
    
    // トークンを保存（TokenStoreテーブルが存在しない場合はスキップ）
    // const now = new Date();
    // const accessExpiry = new Date(now.getTime() + 24 * 60 * 60 * 1000);
    // const refreshExpiry = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
    
    // await prisma.tokenStore.createMany({
    //   data: [
    //     {
    //       id: `token_${Date.now()}_access`,
    //       token_type: 'ACCESS',
    //       token_value: token,
    //       user_id: userAuth.user_id,
    //       tenant_id: tenantId,
    //       expires_at: accessExpiry,
    //       is_revoked: false,
    //       is_deleted: false
    //     },
    //     {
    //       id: `token_${Date.now()}_refresh`,
    //       token_type: 'REFRESH',
    //       token_value: refreshToken,
    //       user_id: userAuth.user_id,
    //       tenant_id: tenantId,
    //       expires_at: refreshExpiry,
    //       is_revoked: false,
    //       is_deleted: false
    //     }
    //   ]
    // });

    console.log('Login successful for:', userAuth.login_id);

    // レスポンス（テナント情報を含める）
    return NextResponse.json(
      {
        success: true,
        data: {
          accessToken: token,
          refreshToken: refreshToken,
          expiresIn: 24 * 60 * 60 * 1000,
          user: {
            id: userAuth.user_id,
            loginId: userAuth.login_id,
            employeeId: userAuth.employee_id,
            name: employeeInfo?.full_name || userAuth.login_id,
            nameKana: employeeInfo?.full_name_kana || '',
            email: employeeInfo?.email || '',
            department: departmentInfo?.department_name || '',
            position: positionInfo?.position_name || '',
            role: roleName,
            permissions,
            lastLoginAt: userAuth.last_login_at,
          },
          tenant: {
            id: tenantId,
            code: tenant?.tenant_code || '',
            name: tenant?.tenant_name || ''
          }
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
  } finally {
    await prisma.$disconnect();
  }
}
