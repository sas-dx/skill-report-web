/**
 * 要求仕様ID: PRO.1-BASE.1
 * 対応設計書: docs/design/api/specs/API定義書_API-011_プロフィール取得API.md
 * 実装内容: 現在のユーザーのプロフィール取得専用エンドポイント
 */

import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import { createAuditLog, getObjectDiff } from '@/lib/auditLogger';

// 現在のユーザーのプロフィール取得API
export async function GET(request: NextRequest) {
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

    // JWTからemployeeIdを取得（ログインAPIと整合性を保つ）
    const currentEmployeeId = authResult.employeeId || authResult.userId;

    // クエリパラメータの取得
    const { searchParams } = new URL(request.url);
    const includeHistory = searchParams.get('includeHistory') === 'true';
    const includeSkillSummary = searchParams.get('includeSkillSummary') === 'true';
    const includeGoalSummary = searchParams.get('includeGoalSummary') === 'true';

    console.log('Profile API - Auth result:', {
      userId: authResult.userId,
      employeeId: authResult.employeeId,
      loginId: authResult.loginId,
      currentEmployeeId
    });

    // ユーザー情報の取得（employee_codeで検索）
    const user = await prisma.employee.findUnique({
      where: { 
        employee_code: currentEmployeeId
      }
    });

    if (!user) {
      console.log('User not found for employee_code:', currentEmployeeId);
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'USER_NOT_FOUND',
            message: '指定されたユーザーが見つかりません',
            details: `EmployeeID: ${currentEmployeeId}`
          }
        },
        { status: 404 }
      );
    }

    console.log('User found:', {
      employee_code: user.employee_code,
      full_name: user.full_name,
      department_id: user.department_id,
      position_id: user.position_id
    });

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

    // フルネームを分割（仮実装）
    const fullName = user?.full_name || '';
    const nameParts = fullName.split(' ');
    const lastName = nameParts[0] || '';
    const firstName = nameParts[1] || '';
    
    const fullNameKana = user?.full_name_kana || '';
    const kanaNameParts = fullNameKana.split(' ');
    const lastNameKana = kanaNameParts[0] || '';
    const firstNameKana = kanaNameParts[1] || '';

    // 表示名の生成（アイコン表示用）
    const generateDisplayName = (fullName: string, employeeCode: string) => {
      if (!fullName || fullName.trim() === '') {
        // フルネームがない場合は社員コードから表示名を生成
        return `社員${employeeCode}`;
      }
      
      const parts = fullName.trim().split(/\s+/);
      if (parts.length >= 2) {
        // 姓名がある場合は「姓 名」形式
        return `${parts[0]} ${parts[1]}`;
      } else if (parts.length === 1) {
        // 姓のみの場合はそのまま
        return parts[0];
      }
      
      return `社員${employeeCode}`; // フォールバック
    };

    const displayName = generateDisplayName(fullName, user.employee_code);

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
        displayName: displayName,
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
        managerName: ''
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

    // 部下情報の取得
    let subordinates = null;
    const isManager = position?.position_level && position.position_level >= 3; // レベル3以上を管理職とする
    
    if (isManager) {
      const subordinateList = await prisma.employee.findMany({
        where: {
          manager_id: currentEmployeeId,
          is_deleted: false
        },
        select: {
          employee_code: true,
          full_name: true,
          email: true,
          position_id: true,
          department_id: true
        }
      });

      // 部下の役職・部署情報を取得
      subordinates = await Promise.all(
        subordinateList.map(async (sub) => {
          const subPosition = sub.position_id ? 
            await prisma.position.findUnique({ 
              where: { position_code: sub.position_id } 
            }) : null;
          
          const subDepartment = sub.department_id ?
            await prisma.department.findUnique({
              where: { department_code: sub.department_id }
            }) : null;

          return {
            employee_id: sub.employee_code,
            name: sub.full_name,
            email: sub.email,
            position: subPosition?.position_name || '未設定',
            department: subDepartment?.department_name || '未設定'
          };
        })
      );
    }

    // スキルサマリーの取得（オプション）
    let skillSummary = null;
    if (includeSkillSummary) {
      const skills = await prisma.skillRecord.findMany({
        where: { 
          employee_id: currentEmployeeId,
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
    const jsonResponse = NextResponse.json({
      success: true,
      data: {
        profile,
        ...(skillSummary && { skillSummary }),
        ...(goalSummary && { goalSummary }),
        ...(updateHistory && { updateHistory }),
        ...(subordinates && { subordinates })
      }
    });
    jsonResponse.headers.set('Content-Type', 'application/json; charset=utf-8');
    return jsonResponse;

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
 * 実装内容: 現在のユーザーのプロフィール更新専用エンドポイント
 */
export async function PUT(request: NextRequest) {
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

    // JWTからemployeeIdを取得（ログインAPIと整合性を保つ）
    const currentEmployeeId = authResult.employeeId || authResult.userId;

    // リクエストボディの取得
    let body;
    try {
      body = await request.json();
    } catch (error) {
      console.error('JSON parse error:', error);
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'INVALID_JSON',
            message: 'リクエストボディのJSONが不正です'
          }
        },
        { status: 400 }
      );
    }

    console.log('=== プロフィール更新API デバッグ情報 ===');
    console.log('Request method:', request.method);
    console.log('Request URL:', request.url);
    console.log('Request headers:', Object.fromEntries(request.headers.entries()));
    console.log('Received update data:', JSON.stringify(body, null, 2));
    console.log('Body keys:', Object.keys(body));
    console.log('Body type:', typeof body);
    console.log('Body first_name:', body.first_name, typeof body.first_name);
    console.log('Body last_name:', body.last_name, typeof body.last_name);
    console.log('Body display_name:', body.display_name, typeof body.display_name);
    console.log('Body email:', body.email, typeof body.email);
    console.log('Body contact_info:', body.contact_info);
    console.log('Body organization_info:', body.organization_info);

    // 入力値検証
    const errors: Array<{ field: string; reason: string }> = [];

    // 必須項目の検証
    if (!body.first_name || typeof body.first_name !== 'string' || body.first_name.trim() === '') {
      errors.push({ field: 'first_name', reason: '名前（名）は必須です' });
    } else if (body.first_name.length > 30) {
      errors.push({ field: 'first_name', reason: '名は30文字以内で入力してください' });
    }
    
    if (!body.last_name || typeof body.last_name !== 'string' || body.last_name.trim() === '') {
      errors.push({ field: 'last_name', reason: '名前（姓）は必須です' });
    } else if (body.last_name.length > 30) {
      errors.push({ field: 'last_name', reason: '姓は30文字以内で入力してください' });
    }

    if (!body.display_name || typeof body.display_name !== 'string' || body.display_name.trim() === '') {
      errors.push({ field: 'display_name', reason: '表示名は必須です' });
    } else if (body.display_name.length > 50) {
      errors.push({ field: 'display_name', reason: '表示名は50文字以内で入力してください' });
    }

    if (!body.email || typeof body.email !== 'string' || body.email.trim() === '') {
      errors.push({ field: 'email', reason: 'メールアドレスは必須です' });
    } else {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(body.email)) {
        errors.push({ field: 'email', reason: '有効なメールアドレスを入力してください' });
      } else if (body.email.length > 255) {
        errors.push({ field: 'email', reason: 'メールアドレスは255文字以内で入力してください' });
      } else {
        // メールアドレス重複チェック
        const existingUser = await prisma.employee.findFirst({
          where: {
            email: body.email,
            employee_code: { not: currentEmployeeId }
          }
        });
        
        if (existingUser) {
          errors.push({ field: 'email', reason: 'このメールアドレスは既に他のユーザーによって使用されています' });
        }
      }
    }

    // カナの検証（オプション） - 一時的に無効化
    // const katakanaRegex = /^[ァ-ヿー\s]*$/;
    // if (body.first_name_kana && typeof body.first_name_kana === 'string' && body.first_name_kana.trim() !== '' && !katakanaRegex.test(body.first_name_kana)) {
    //   errors.push({ field: 'first_name_kana', reason: '全角カタカナで入力してください' });
    // }
    // if (body.last_name_kana && typeof body.last_name_kana === 'string' && body.last_name_kana.trim() !== '' && !katakanaRegex.test(body.last_name_kana)) {
    //   errors.push({ field: 'last_name_kana', reason: '全角カタカナで入力してください' });
    // }

    // 電話番号の検証（オプション）
    const phoneNumber = body.contact_info?.phone;
    if (phoneNumber && typeof phoneNumber === 'string' && phoneNumber.trim() !== '' && !/^[\d\-+()]*$/.test(phoneNumber)) {
      errors.push({ field: 'phone', reason: '電話番号の形式が正しくありません' });
    }

    // 部署の検証（オプション）
    const departmentId = body.organization_info?.department_id;
    if (departmentId && typeof departmentId === 'string' && departmentId.trim() !== '') {
      const department = await prisma.department.findUnique({
        where: { department_code: departmentId }
      });
      if (!department) {
        errors.push({ field: 'department_id', reason: '指定された部署が存在しません' });
      }
    }

    // 役職の検証（オプション）
    const positionId = body.organization_info?.position_id;
    if (positionId && typeof positionId === 'string' && positionId.trim() !== '') {
      const position = await prisma.position.findUnique({
        where: { position_code: positionId }
      });
      if (!position) {
        errors.push({ field: 'position_id', reason: '指定された役職が存在しません' });
      }
    }

    // エラーがある場合は400を返す
    if (errors.length > 0) {
      console.error('プロフィール更新バリデーションエラー:', JSON.stringify(errors, null, 2));
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message: '入力値に誤りがあります',
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

    // フルネームの構築
    const lastName = body.last_name || '';
    const firstName = body.first_name || '';
    const fullName = `${lastName} ${firstName}`.trim();
    updateData.full_name = fullName;
    updatedFields.push('full_name');
    
    // フルネームカナの構築
    if (body.first_name_kana || body.last_name_kana) {
      const lastNameKana = body.last_name_kana || '';
      const firstNameKana = body.first_name_kana || '';
      const fullNameKana = `${lastNameKana} ${firstNameKana}`.trim();
      updateData.full_name_kana = fullNameKana;
      updatedFields.push('full_name_kana');
    }
    
    // 電話番号の更新
    if (body.contact_info && typeof body.contact_info.phone === 'string') {
      updateData.phone = body.contact_info.phone.trim() || null;
      updatedFields.push('phone');
    }

    // メールアドレスの更新
    updateData.email = body.email;
    updatedFields.push('email');

    // 部署の更新
    if (body.organization_info && typeof body.organization_info.department_id === 'string') {
      updateData.department_id = body.organization_info.department_id.trim() || null;
      updatedFields.push('department_id');
    }

    // 役職の更新
    if (body.organization_info && typeof body.organization_info.position_id === 'string') {
      updateData.position_id = body.organization_info.position_id.trim() || null;
      updatedFields.push('position_id');
    }

    // 更新日時を追加
    updateData.updated_at = new Date();

    console.log('Update data to be saved:', JSON.stringify(updateData, null, 2));

    // 更新前のデータを取得（AuditLog用）
    const currentUser = await prisma.employee.findUnique({
      where: { 
        employee_code: currentEmployeeId
      }
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

    // データベース更新
    const updatedUser = await prisma.employee.update({
      where: { 
        employee_code: currentEmployeeId
      },
      data: updateData
    });

    // AuditLog記録（更新後に実行）
    try {
      const { oldValues, newValues } = getObjectDiff(
        {
          full_name: currentUser.full_name,
          full_name_kana: currentUser.full_name_kana,
          email: currentUser.email,
          phone: currentUser.phone,
          department_id: currentUser.department_id,
          position_id: currentUser.position_id
        },
        {
          full_name: updatedUser.full_name,
          full_name_kana: updatedUser.full_name_kana,
          email: updatedUser.email,
          phone: updatedUser.phone,
          department_id: updatedUser.department_id,
          position_id: updatedUser.position_id
        }
      );

      // 変更があった場合のみAuditLogを記録
      if (Object.keys(newValues).length > 0) {
        await createAuditLog({
          userId: currentEmployeeId,
          actionType: 'UPDATE',
          targetTable: 'Employee',
          targetId: currentEmployeeId,
          oldValues,
          newValues,
          changeReason: 'プロフィール更新',
          ipAddress: request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown',
          userAgent: request.headers.get('user-agent') || 'unknown'
        });
        console.log('AuditLog記録完了:', { oldValues, newValues });
      }
    } catch (auditError) {
      console.error('AuditLog記録エラー:', auditError);
      // AuditLogの失敗はメイン処理を止めない
    }

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
      updated_by: currentEmployeeId || '',
      updated_at: updatedUser.updated_at.toISOString(),
      change_summary: {
        updated_fields: updatedFields,
        profile_image_changed: false,
        skills_changed: false
      }
    };

    const jsonResponse = NextResponse.json({
      success: true,
      data: response
    });
    jsonResponse.headers.set('Content-Type', 'application/json; charset=utf-8');
    return jsonResponse;

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
