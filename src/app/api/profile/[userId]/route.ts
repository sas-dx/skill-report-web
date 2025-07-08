/**
 * 要求仕様ID: PRO.1-BASE.1
 * 対応設計書: docs/design/api/specs/API定義書_API-011_プロフィール取得API.md
 * 実装内容: プロフィール管理API（取得・更新）
 */

import { NextRequest, NextResponse } from 'next/server';

// モックデータ（実際の実装では Prisma を使用）
const mockProfile = {
  employeeId: 'EMP001',
  email: 'yamada.taro@company.com',
  personalInfo: {
    firstName: '太郎',
    lastName: '山田',
    firstNameKana: 'タロウ',
    lastNameKana: 'ヤマダ',
    displayName: '山田 太郎',
    phoneNumber: '090-1234-5678'
  },
  organizationInfo: {
    departmentId: 'DEPT001',
    departmentName: '開発部',
    positionId: 'POS001',
    positionName: 'エンジニア',
    hireDate: '2020-04-01'
  },
  skillSummary: {
    totalSkills: 15,
    averageLevel: 2.8,
    topCategories: [
      { category: 'プログラミング', level: 3 },
      { category: 'データベース', level: 2 },
      { category: 'インフラ', level: 2 }
    ]
  },
  lastUpdated: '2025-07-08T15:30:00Z'
};

/**
 * プロフィール情報取得API
 * GET /api/profile/[userId]
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { userId: string } }
) {
  try {
    const { userId } = params;
    const { searchParams } = new URL(request.url);
    
    // クエリパラメータの取得
    const includeSkillSummary = searchParams.get('include_skill_summary') === 'true';
    const includeGoalSummary = searchParams.get('include_goal_summary') === 'true';
    const includeHistory = searchParams.get('include_history') === 'true';

    // ユーザーIDの検証
    if (!userId || userId === '') {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_USER_ID',
          message: 'ユーザーIDが指定されていません'
        }
      }, { status: 400 });
    }

    // 実際の実装では、ここでデータベースからプロフィール情報を取得
    // const profile = await prisma.user.findUnique({
    //   where: { id: userId === 'me' ? currentUserId : userId },
    //   include: {
    //     department: true,
    //     position: true,
    //     skills: includeSkillSummary,
    //     // その他の関連データ
    //   }
    // });

    // モックデータを使用
    let responseProfile: any = { ...mockProfile };

    // オプションに応じてデータを調整
    if (!includeSkillSummary) {
      delete responseProfile.skillSummary;
    }

    return NextResponse.json({
      success: true,
      data: {
        profile: responseProfile
      }
    });

  } catch (error) {
    console.error('プロフィール取得エラー:', error);
    return NextResponse.json({
      success: false,
      error: {
        code: 'INTERNAL_SERVER_ERROR',
        message: 'プロフィール情報の取得中にエラーが発生しました'
      }
    }, { status: 500 });
  }
}

/**
 * プロフィール情報更新API
 * PUT /api/profile/[userId]
 */
export async function PUT(
  request: NextRequest,
  { params }: { params: { userId: string } }
) {
  try {
    const { userId } = params;
    const updateData = await request.json();

    // ユーザーIDの検証
    if (!userId || userId === '') {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_USER_ID',
          message: 'ユーザーIDが指定されていません'
        }
      }, { status: 400 });
    }

    // 入力値検証
    const validationErrors = [];

    if (!updateData.first_name?.trim()) {
      validationErrors.push({
        field: 'first_name',
        reason: '名前（名）は必須です'
      });
    }

    if (!updateData.last_name?.trim()) {
      validationErrors.push({
        field: 'last_name',
        reason: '名前（姓）は必須です'
      });
    }

    if (!updateData.display_name?.trim()) {
      validationErrors.push({
        field: 'display_name',
        reason: '表示名は必須です'
      });
    }

    if (!updateData.email?.trim()) {
      validationErrors.push({
        field: 'email',
        reason: 'メールアドレスは必須です'
      });
    } else {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(updateData.email)) {
        validationErrors.push({
          field: 'email',
          reason: '有効なメールアドレスを入力してください'
        });
      } else if (updateData.email.length > 255) {
        validationErrors.push({
          field: 'email',
          reason: 'メールアドレスは255文字以内で入力してください'
        });
      }
    }

    if (updateData.contact_info?.phone && !/^[\d-+()]+$/.test(updateData.contact_info.phone)) {
      validationErrors.push({
        field: 'phone',
        reason: '電話番号の形式が正しくありません'
      });
    }

    if (validationErrors.length > 0) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: '入力値に誤りがあります',
          invalid_fields: validationErrors
        }
      }, { status: 400 });
    }

    // 実際の実装では、ここでデータベースを更新
    // const updatedProfile = await prisma.user.update({
    //   where: { id: userId === 'me' ? currentUserId : userId },
    //   data: {
    //     firstName: updateData.first_name,
    //     lastName: updateData.last_name,
    //     firstNameKana: updateData.first_name_kana,
    //     lastNameKana: updateData.last_name_kana,
    //     displayName: updateData.display_name,
    //     email: updateData.email,
    //     phoneNumber: updateData.contact_info?.phone,
    //     departmentId: updateData.organization_info?.department_id,
    //     positionId: updateData.organization_info?.position_id,
    //     updatedAt: new Date()
    //   },
    //   include: {
    //     department: true,
    //     position: true
    //   }
    // });

    // モックデータで更新をシミュレート
    const updatedProfile = {
      ...mockProfile,
      email: updateData.email,
      personalInfo: {
        ...mockProfile.personalInfo,
        firstName: updateData.first_name,
        lastName: updateData.last_name,
        firstNameKana: updateData.first_name_kana || mockProfile.personalInfo.firstNameKana,
        lastNameKana: updateData.last_name_kana || mockProfile.personalInfo.lastNameKana,
        displayName: updateData.display_name,
        phoneNumber: updateData.contact_info?.phone || mockProfile.personalInfo.phoneNumber
      },
      organizationInfo: {
        ...mockProfile.organizationInfo,
        departmentId: updateData.organization_info?.department_id || mockProfile.organizationInfo.departmentId,
        positionId: updateData.organization_info?.position_id || mockProfile.organizationInfo.positionId
      },
      lastUpdated: new Date().toISOString()
    };

    return NextResponse.json({
      success: true,
      data: {
        profile: updatedProfile
      }
    });

  } catch (error) {
    console.error('プロフィール更新エラー:', error);
    return NextResponse.json({
      success: false,
      error: {
        code: 'INTERNAL_SERVER_ERROR',
        message: 'プロフィール情報の更新中にエラーが発生しました'
      }
    }, { status: 500 });
  }
}
