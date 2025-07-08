/**
 * 要求仕様ID: PRO.1-BASE.1
 * 対応設計書: docs/design/api/specs/API定義書_API-011_プロフィール取得API.md
 * 実装内容: プロフィール取得API
 */

import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth } from '@/lib/auth';
import { prisma } from '@/lib/prisma';

// プロフィール取得API
export async function GET(
  request: NextRequest,
  { params }: { params: { userId: string } }
) {
  try {
    // 認証チェック
    const authResult = await verifyAuth(request);
    if (!authResult.success) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'UNAUTHORIZED',
            message: '認証が必要です'
          }
        },
        { status: 401 }
      );
    }

    if (!params || !params.userId) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'INVALID_PARAMETER',
            message: 'ユーザーIDが指定されていません'
          }
        },
        { status: 400 }
      );
    }

    const { userId } = params;
    if (!authResult.userId) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'INVALID_TOKEN',
            message: '無効な認証トークンです'
          }
        },
        { status: 401 }
      );
    }

    const currentUserId = authResult.userId;

    // userIdが'me'の場合は認証されたユーザーのIDを使用
    const targetUserId = userId === 'me' ? (authResult.employeeId || currentUserId) : userId;

    // クエリパラメータの取得
    const { searchParams } = new URL(request.url);
    const includeHistory = searchParams.get('includeHistory') === 'true';
    const includeSkillSummary = searchParams.get('includeSkillSummary') === 'true';
    const includeGoalSummary = searchParams.get('includeGoalSummary') === 'true';

    // 権限チェック（自分以外のプロフィールを見る場合）
    const currentEmployeeId = authResult.employeeId || currentUserId;
    if (targetUserId !== currentEmployeeId) {
      // TODO: 管理者権限チェックを実装
      // 現在は暫定的に403を返す
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'FORBIDDEN',
            message: 'アクセス権限がありません'
          }
        },
        { status: 403 }
      );
    }

    // ユーザー情報の取得
    if (!targetUserId) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'INVALID_PARAMETER',
            message: 'ユーザーIDが無効です'
          }
        },
        { status: 400 }
      );
    }

    const user = await prisma.employee.findUnique({
      where: { employee_code: targetUserId }
    });

    if (!user) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'USER_NOT_FOUND',
            message: '指定されたユーザーが見つかりません',
            details: `ユーザーID: ${targetUserId}`
          }
        },
        { status: 404 }
      );
    }

    // 部署情報の取得
    let department = null;
    if (user?.department_id) {
      department = await prisma.department.findUnique({
        where: { department_code: user.department_id }
      });
    }

    // 役職情報の取得
    let position = null;
    if (user?.position_id) {
      position = await prisma.position.findUnique({
        where: { position_code: user.position_id }
      });
    }

    // 上長情報の取得
    let managerName = '';
    if (user.manager_id) {
      const manager = await prisma.employee.findUnique({
        where: { employee_code: user.manager_id },
        select: { full_name: true }
      });
      managerName = manager?.full_name || '';
    }

    // フルネームを分割（仮実装）
    const fullName = user?.full_name || '';
    const nameParts = fullName.split(' ');
    const lastName = nameParts[0] || '';
    const firstName = nameParts[1] || '';
    
    const fullNameKana = user?.full_name_kana || '';
    const kanaNameParts = fullNameKana.split(' ');
    const lastNameKana = kanaNameParts[0] || '';
    const firstNameKana = kanaNameParts[1] || '';

    // レスポンスデータの構築
    const profile = {
      id: user.employee_code,
      email: user.email || '',
      employeeId: user.employee_code,
      personalInfo: {
        lastName: lastName,
        firstName: firstName,
        lastNameKana: lastNameKana,
        firstNameKana: firstNameKana,
        displayName: fullName,
        phoneNumber: user.phone || '',
        emergencyContact: {
          name: '',
          relationship: '',
          phoneNumber: ''
        }
      },
      organizationInfo: {
        tenantId: 'tenant_001', // 現在はシングルテナント
        tenantName: '株式会社A',
        departmentId: user.department_id || '',
        departmentName: department?.department_name || '',
        divisionId: '',
        divisionName: '',
        positionId: user.position_id || '',
        positionName: position?.position_name || '',
        employmentType: user.employment_status || '正社員',
        hireDate: user.hire_date ? user.hire_date.toISOString().split('T')[0] : '',
        managerUserId: user.manager_id || '',
        managerName: managerName
      },
      workInfo: {
        workLocation: '東京本社',
        workStyle: 'hybrid',
        contractHours: 8.0,
        overtimeAllowed: true,
        remoteWorkAllowed: true,
        flexTimeAllowed: true
      },
      systemInfo: {
        status: user.is_deleted ? 'inactive' : 'active',
        role: 'user',
        permissions: [
          'profile:read',
          'profile:write',
          'skills:read',
          'skills:write',
          'goals:read',
          'goals:write'
        ],
        lastLoginAt: new Date().toISOString(),
        createdAt: user.created_at.toISOString(),
        updatedAt: user.updated_at.toISOString()
      },
      preferences: {
        language: 'ja',
        timezone: 'Asia/Tokyo',
        dateFormat: 'YYYY-MM-DD',
        notifications: {
          email: true,
          inApp: true,
          skillExpiry: true,
          goalReminder: true
        },
        privacy: {
          profileVisibility: 'team',
          skillVisibility: 'department',
          goalVisibility: 'manager'
        }
      }
    };

    // スキルサマリーの取得（オプション）
    let skillSummary = null;
    if (includeSkillSummary) {
      const skills = await prisma.skillRecord.findMany({
        where: { 
          employee_id: targetUserId,
          is_deleted: false
        }
      });

      const skillsByLevel = skills.reduce((acc: Record<string, number>, skill) => {
        const level = (skill.skill_level || 0).toString();
        acc[level] = (acc[level] || 0) + 1;
        return acc;
      }, {} as Record<string, number>);

      // スキルカテゴリ情報を取得
      const skillCategories = await Promise.all(
        skills.map(async (skill) => {
          if (skill.skill_category_id) {
            const category = await prisma.skillCategory.findUnique({
              where: { category_code: skill.skill_category_id }
            });
            return { skill, category };
          }
          return { skill, category: null };
        })
      );

      skillSummary = {
        totalSkills: skills.length,
        skillsByCategory: {
          technical: skillCategories.filter(s => s.category?.category_name?.includes('技術')).length,
          business: skillCategories.filter(s => s.category?.category_name?.includes('ビジネス')).length,
          management: skillCategories.filter(s => s.category?.category_name?.includes('マネジメント')).length
        },
        skillsByLevel: {
          '×': skillsByLevel['1'] || 0,
          '△': skillsByLevel['2'] || 0,
          '○': skillsByLevel['3'] || 0,
          '◎': skillsByLevel['4'] || 0
        },
        topSkills: skillCategories
          .sort((a, b) => (b.skill.skill_level || 0) - (a.skill.skill_level || 0))
          .slice(0, 3)
          .map(({ skill, category }) => ({
            skillId: skill.skill_item_id || '',
            skillName: category?.category_name || '',
            level: skill.skill_level === 4 ? '◎' : skill.skill_level === 3 ? '○' : skill.skill_level === 2 ? '△' : '×',
            categoryName: category?.category_name || ''
          })),
        certifications: {
          total: 0,
          active: 0,
          expiringSoon: 0
        },
        lastUpdated: skills.length > 0 
          ? Math.max(...skills.map(s => s.updated_at.getTime()))
          : new Date().toISOString()
      };
    }

    // 目標サマリーの取得（オプション）
    let goalSummary = null;
    if (includeGoalSummary) {
      // TODO: 目標管理テーブルが実装されたら追加
      goalSummary = {
        currentGoals: 3,
        completedGoals: 8,
        overallProgress: 75.5,
        goalsByStatus: {
          not_started: 0,
          in_progress: 2,
          completed: 1,
          on_hold: 0
        },
        upcomingDeadlines: [
          {
            goalId: 'goal_001',
            goalTitle: 'AWS Professional資格取得',
            deadline: '2025-08-31',
            progress: 60,
            daysRemaining: 93
          }
        ],
        lastUpdated: new Date().toISOString()
      };
    }

    // 更新履歴の取得（オプション）
    let updateHistory = null;
    if (includeHistory) {
      // TODO: 更新履歴テーブルが実装されたら追加
      updateHistory = [
        {
          id: 'hist_001',
          fieldName: 'organizationInfo.positionName',
          previousValue: 'エンジニア',
          newValue: 'シニアエンジニア',
          changeReason: '昇進',
          updatedBy: 'user_manager_001',
          updatedByName: '佐藤部長',
          updatedAt: new Date().toISOString(),
          approvedBy: 'user_hr_001',
          approvedByName: '人事部',
          approvedAt: new Date().toISOString()
        }
      ];
    }

    // レスポンスの返却
    return NextResponse.json({
      success: true,
      data: {
        profile,
        ...(skillSummary && { skillSummary }),
        ...(goalSummary && { goalSummary }),
        ...(updateHistory && { updateHistory })
      }
    });

  } catch (error) {
    console.error('Profile fetch error:', error);
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'INTERNAL_SERVER_ERROR',
          message: 'サーバー内部エラーが発生しました'
        }
      },
      { status: 500 }
    );
  }
}

/**
 * 要求仕様ID: PRO.1-BASE.1
 * 対応設計書: docs/design/api/specs/API定義書_API-012_プロフィール更新API.md
 * 実装内容: プロフィール更新API
 */
export async function PUT(
  request: NextRequest,
  { params }: { params: { userId: string } }
) {
  try {
    // 認証チェック
    const authResult = await verifyAuth(request);
    if (!authResult.success) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'UNAUTHORIZED',
            message: '認証が必要です'
          }
        },
        { status: 401 }
      );
    }

    if (!params || !params.userId) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'INVALID_PARAMETER',
            message: 'ユーザーIDが指定されていません'
          }
        },
        { status: 400 }
      );
    }

    const { userId } = params;

    if (!authResult.userId) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'INVALID_TOKEN',
            message: '無効な認証トークンです'
          }
        },
        { status: 401 }
      );
    }

    const currentUserId = authResult.userId;

    // "me"の場合は現在のユーザーIDに置き換え
    const targetUserId = userId === 'me' ? currentUserId : userId;

    // 権限チェック（自分以外のプロフィールを更新する場合）
    if (targetUserId !== currentUserId) {
      // TODO: 管理者権限チェックを実装
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'PERMISSION_DENIED',
            message: '権限がありません'
          }
        },
        { status: 403 }
      );
    }

    // リクエストボディの取得
    const body = await request.json();

    // 入力値検証
    const errors: Array<{ field: string; reason: string }> = [];

    // 氏名の検証
    if (body.first_name && (body.first_name.length < 1 || body.first_name.length > 30)) {
      errors.push({ field: 'first_name', reason: '名は1-30文字で入力してください' });
    }
    if (body.last_name && (body.last_name.length < 1 || body.last_name.length > 30)) {
      errors.push({ field: 'last_name', reason: '姓は1-30文字で入力してください' });
    }

    // カナの検証
    const katakanaRegex = /^[ァ-ヶー]+$/;
    if (body.first_name_kana && !katakanaRegex.test(body.first_name_kana)) {
      errors.push({ field: 'first_name_kana', reason: '全角カタカナで入力してください' });
    }
    if (body.last_name_kana && !katakanaRegex.test(body.last_name_kana)) {
      errors.push({ field: 'last_name_kana', reason: '全角カタカナで入力してください' });
    }

    // 表示名の検証
    if (body.display_name && (body.display_name.length < 1 || body.display_name.length > 50)) {
      errors.push({ field: 'display_name', reason: '表示名は1-50文字で入力してください' });
    }

    // メールアドレスの検証
    if (body.email !== undefined) {
      if (!body.email || body.email.trim() === '') {
        errors.push({ field: 'email', reason: 'メールアドレスは必須です' });
      } else {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(body.email)) {
          errors.push({ field: 'email', reason: '有効なメールアドレスを入力してください' });
        } else if (body.email.length > 255) {
          errors.push({ field: 'email', reason: 'メールアドレスは255文字以内で入力してください' });
        }
      }
    }

    // エラーがある場合は400を返す
    if (errors.length > 0) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'INVALID_PARAMETER',
            message: 'パラメータが不正です',
            details: errors[0]?.reason || '',
            invalid_fields: errors
          }
        },
        { status: 400 }
      );
    }

    // ユーザー情報の更新
    const updateData: any = {};
    const updatedFields: string[] = [];

    // 現在のユーザー情報を取得して、既存の姓名を取得
    const currentUser = await prisma.employee.findUnique({
      where: { employee_code: targetUserId }
    });

    if (!currentUser) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'USER_NOT_FOUND',
            message: 'ユーザーが見つかりません'
          }
        },
        { status: 404 }
      );
    }

    // 既存の姓名を分割
    const existingFullName = currentUser.full_name || '';
    const existingNameParts = existingFullName.split(' ');
    const existingLastName = existingNameParts[0] || '';
    const existingFirstName = existingNameParts[1] || '';

    const existingFullNameKana = currentUser.full_name_kana || '';
    const existingKanaNameParts = existingFullNameKana.split(' ');
    const existingLastNameKana = existingKanaNameParts[0] || '';
    const existingFirstNameKana = existingKanaNameParts[1] || '';

    // フルネームの構築（既存の値を保持しつつ更新）
    if (body.first_name !== undefined || body.last_name !== undefined) {
      const lastName = body.last_name !== undefined ? body.last_name : existingLastName;
      const firstName = body.first_name !== undefined ? body.first_name : existingFirstName;
      const fullName = `${lastName} ${firstName}`.trim();
      updateData.full_name = fullName;
      updatedFields.push('full_name');
      console.log('姓名更新:', { lastName, firstName, fullName });
    }
    
    if (body.first_name_kana !== undefined || body.last_name_kana !== undefined) {
      const lastNameKana = body.last_name_kana !== undefined ? body.last_name_kana : existingLastNameKana;
      const firstNameKana = body.first_name_kana !== undefined ? body.first_name_kana : existingFirstNameKana;
      const fullNameKana = `${lastNameKana} ${firstNameKana}`.trim();
      updateData.full_name_kana = fullNameKana;
      updatedFields.push('full_name_kana');
      console.log('カナ更新:', { lastNameKana, firstNameKana, fullNameKana });
    }
    
    if (body.contact_info?.phone !== undefined) {
      updateData.phone = body.contact_info.phone;
      updatedFields.push('contact_info.phone');
    }

    // 組織情報の更新
    if (body.organization_info?.department_id !== undefined) {
      // 部署IDが空文字列の場合はnullに変換
      updateData.department_id = body.organization_info.department_id === '' ? null : body.organization_info.department_id;
      updatedFields.push('organization_info.department_id');
      console.log('部署ID更新:', body.organization_info.department_id, '→', updateData.department_id);
    }
    
    if (body.organization_info?.position_id !== undefined) {
      // 役職IDが空文字列の場合はnullに変換
      updateData.position_id = body.organization_info.position_id === '' ? null : body.organization_info.position_id;
      updatedFields.push('organization_info.position_id');
      console.log('役職ID更新:', body.organization_info.position_id, '→', updateData.position_id);
    }

    // メールアドレスの更新（重複チェック付き）
    if (body.email !== undefined) {
      const trimmedEmail = body.email.trim();
      
      // 現在のユーザーのメールアドレスと異なる場合のみ重複チェック
      if (currentUser && currentUser.email !== trimmedEmail) {
        // 他のユーザーが同じメールアドレスを使用していないかチェック
        const existingUser = await prisma.employee.findFirst({
          where: {
            email: trimmedEmail,
            employee_code: { not: targetUserId },
            is_deleted: false
          }
        });
        
        if (existingUser) {
          return NextResponse.json(
            {
              success: false,
              error: {
                code: 'EMAIL_ALREADY_EXISTS',
                message: 'このメールアドレスは既に他のユーザーによって使用されています',
                details: 'メールアドレスを変更してください',
                invalid_fields: [{ field: 'email', reason: 'このメールアドレスは既に使用されています' }]
              }
            },
            { status: 409 }
          );
        }
      }
      
      updateData.email = trimmedEmail;
      updatedFields.push('email');
    }

    // 更新日時を追加
    updateData.updated_at = new Date();

    // データベース更新
    if (!targetUserId) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'INVALID_PARAMETER',
            message: 'ユーザーIDが無効です'
          }
        },
        { status: 400 }
      );
    }

    // デバッグログを追加
    console.log('=== プロフィール更新デバッグ ===');
    console.log('Target user ID:', targetUserId);
    console.log('Request body:', JSON.stringify(body, null, 2));
    console.log('Update data:', JSON.stringify(updateData, null, 2));
    console.log('Updated fields:', updatedFields);

    const updatedUser = await prisma.employee.update({
      where: { employee_code: targetUserId },
      data: updateData
    });

    console.log('Updated user result:', {
      employee_code: updatedUser.employee_code,
      department_id: updatedUser.department_id,
      position_id: updatedUser.position_id,
      email: updatedUser.email,
      full_name: updatedUser.full_name,
      updated_at: updatedUser.updated_at
    });

    // 部署情報の取得
    let department = null;
    if (updatedUser.department_id) {
      department = await prisma.department.findUnique({
        where: { department_code: updatedUser.department_id }
      });
    }

    // 役職情報の取得
    let position = null;
    if (updatedUser.position_id) {
      position = await prisma.position.findUnique({
        where: { position_code: updatedUser.position_id }
      });
    }

    // フルネームを分割（仮実装）
    const updatedFullName = updatedUser.full_name || '';
    const updatedNameParts = updatedFullName.split(' ');
    const updatedLastName = updatedNameParts[0] || '';
    const updatedFirstName = updatedNameParts[1] || '';
    
    const updatedFullNameKana = updatedUser.full_name_kana || '';
    const updatedKanaNameParts = updatedFullNameKana.split(' ');
    const updatedLastNameKana = updatedKanaNameParts[0] || '';
    const updatedFirstNameKana = updatedKanaNameParts[1] || '';

    // レスポンスデータの構築
    const response = {
      user_id: updatedUser.employee_code,
      username: updatedUser.employee_code,
      email: updatedUser.email || '',
      display_name: body.display_name || updatedFullName,
      first_name: updatedFirstName,
      last_name: updatedLastName,
      first_name_kana: updatedFirstNameKana,
      last_name_kana: updatedLastNameKana,
      employee_id: updatedUser.employee_code,
      department: {
        department_id: updatedUser.department_id || '',
        name: department?.department_name || '',
        code: updatedUser.department_id || '',
        parent_id: ''
      },
      position: {
        position_id: updatedUser.position_id || '',
        name: position?.position_name || '',
        level: 3,
        is_manager: false
      },
      join_date: updatedUser.hire_date ? updatedUser.hire_date.toISOString().split('T')[0] : '',
      profile_image: '',
      contact_info: {
        phone: updatedUser.phone || '',
        extension: '',
        mobile: '',
        emergency_contact: '',
        address: {
          postal_code: '',
          prefecture: '',
          city: '',
          street_address: ''
        }
      },
      updated_by: currentUserId || '',
      updated_at: updatedUser.updated_at.toISOString(),
      change_summary: {
        updated_fields: updatedFields,
        profile_image_changed: false,
        skills_changed: false
      }
    };

    return NextResponse.json({
      success: true,
      data: response
    });

  } catch (error) {
    console.error('Profile update error:', error);
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'INTERNAL_SERVER_ERROR',
          message: 'サーバー内部エラーが発生しました'
        }
      },
      { status: 500 }
    );
  }
}
