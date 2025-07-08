/**
 * 要求仕様ID: PRO.1-BASE.1
 * 対応設計書: docs/design/api/specs/API定義書_API-011_プロフィール取得API.md
 * 実装内容: ユーザーの上長情報取得API
 */

import { NextRequest, NextResponse } from 'next/server'
import { verifyAuth } from '@/lib/auth'
import { prisma } from '@/lib/prisma'

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

    const { userId } = params

    // userIdが'me'の場合は認証されたユーザーのIDを使用
    const targetUserId = userId === 'me' ? (authResult.employeeId || authResult.userId) : userId;

    // 権限チェック：自分の上長情報のみ閲覧可能
    const currentEmployeeId = authResult.employeeId || authResult.userId;
    if (targetUserId !== currentEmployeeId) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'FORBIDDEN',
            message: '他のユーザーの上長情報は閲覧できません'
          }
        },
        { status: 403 }
      );
    }

    console.log('Manager API - Target User ID:', targetUserId);

    // ユーザーの基本情報と上長情報を取得
    const employee = await prisma.employee.findUnique({
      where: { employee_code: targetUserId },
      select: {
        id: true,
        employee_code: true,
        full_name: true,
        manager_id: true,
        department_id: true,
        position_id: true,
      }
    })

    console.log('Manager API - Found employee:', employee);

    if (!employee) {
      return NextResponse.json(
        { success: false, error: 'ユーザーが見つかりません' },
        { status: 404 }
      )
    }

    // 上長の詳細情報を取得
    let managerInfo = null
    if (employee.manager_id) {
      console.log('Manager API - Looking for manager with ID:', employee.manager_id);
      
      // manager_idがemployee_codeかidかを確認して適切に検索
      const manager = await prisma.employee.findFirst({
        where: {
          OR: [
            { employee_code: employee.manager_id },
            { id: employee.manager_id }
          ]
        },
        select: {
          id: true,
          employee_code: true,
          full_name: true,
          email: true,
          phone: true,
          department_id: true,
          position_id: true,
        }
      })

      console.log('Manager API - Found manager:', manager);

      if (manager) {
        // 上長の部署名と役職名を取得
        const [department, position] = await Promise.all([
          manager.department_id ? prisma.department.findUnique({
            where: { department_code: manager.department_id },
            select: { department_name: true }
          }) : Promise.resolve(null),
          manager.position_id ? prisma.position.findUnique({
            where: { position_code: manager.position_id },
            select: { position_name: true }
          }) : Promise.resolve(null)
        ])

        console.log('Manager API - Department:', department);
        console.log('Manager API - Position:', position);

        managerInfo = {
          id: manager.id,
          employee_code: manager.employee_code,
          full_name: manager.full_name,
          email: manager.email,
          phone: manager.phone,
          department_name: department?.department_name || '',
          position_name: position?.position_name || '',
        }
      } else {
        console.log('Manager API - No manager found for manager_id:', employee.manager_id);
      }
    } else {
      console.log('Manager API - No manager_id set for employee');
    }

    return NextResponse.json({
      success: true,
      data: {
        employee: {
          id: employee.id,
          employee_code: employee.employee_code,
          full_name: employee.full_name,
        },
        manager: managerInfo
      }
    })

  } catch (error) {
    console.error('上長情報取得エラー:', error)
    return NextResponse.json(
      { success: false, error: 'サーバーエラーが発生しました' },
      { status: 500 }
    )
  }
}
