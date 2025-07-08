/**
 * 要求仕様ID: PRO.1-BASE.1
 * 対応設計書: docs/design/api/specs/API定義書_API-013_組織情報取得API.md
 * 実装内容: 組織情報取得API（部署・役職一覧）
 */

import { NextRequest, NextResponse } from 'next/server';

// モックデータ（実際の実装では Prisma を使用）
const mockOrganizationData = {
  departments: [
    { id: 'DEPT001', name: '開発部', description: 'システム開発を担当' },
    { id: 'DEPT002', name: '営業部', description: '営業活動を担当' },
    { id: 'DEPT003', name: '人事部', description: '人事管理を担当' },
    { id: 'DEPT004', name: '総務部', description: '総務業務を担当' },
    { id: 'DEPT005', name: '経理部', description: '経理業務を担当' },
    { id: 'DEPT006', name: 'マーケティング部', description: 'マーケティング活動を担当' }
  ],
  positions: [
    { id: 'POS001', name: 'エンジニア', level: 1, description: '開発業務を担当' },
    { id: 'POS002', name: 'シニアエンジニア', level: 2, description: '上級開発業務を担当' },
    { id: 'POS003', name: 'リードエンジニア', level: 3, description: 'チームリーダー業務を担当' },
    { id: 'POS004', name: 'マネージャー', level: 4, description: '管理業務を担当' },
    { id: 'POS005', name: '営業担当', level: 1, description: '営業活動を担当' },
    { id: 'POS006', name: '営業主任', level: 2, description: '営業チームの主任' },
    { id: 'POS007', name: '営業課長', level: 3, description: '営業課の管理' },
    { id: 'POS008', name: '人事担当', level: 1, description: '人事業務を担当' },
    { id: 'POS009', name: '人事主任', level: 2, description: '人事業務の主任' },
    { id: 'POS010', name: '総務担当', level: 1, description: '総務業務を担当' }
  ]
};

/**
 * 組織情報取得API
 * GET /api/organization
 */
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    
    // クエリパラメータの取得
    const includeDepartments = searchParams.get('include_departments') !== 'false';
    const includePositions = searchParams.get('include_positions') !== 'false';
    const departmentId = searchParams.get('department_id');
    const positionLevel = searchParams.get('position_level');

    // 実際の実装では、ここでデータベースから組織情報を取得
    // const departments = await prisma.department.findMany({
    //   where: departmentId ? { id: departmentId } : undefined,
    //   orderBy: { name: 'asc' }
    // });
    // 
    // const positions = await prisma.position.findMany({
    //   where: positionLevel ? { level: parseInt(positionLevel) } : undefined,
    //   orderBy: [{ level: 'asc' }, { name: 'asc' }]
    // });

    let responseData: any = {};

    // 部署情報の取得
    if (includeDepartments) {
      let departments = [...mockOrganizationData.departments];
      
      // 特定の部署IDでフィルタリング
      if (departmentId) {
        departments = departments.filter(dept => dept.id === departmentId);
      }
      
      responseData.departments = departments;
    }

    // 役職情報の取得
    if (includePositions) {
      let positions = [...mockOrganizationData.positions];
      
      // 特定の役職レベルでフィルタリング
      if (positionLevel) {
        const level = parseInt(positionLevel);
        if (!isNaN(level)) {
          positions = positions.filter(pos => pos.level === level);
        }
      }
      
      responseData.positions = positions;
    }

    return NextResponse.json({
      success: true,
      data: responseData
    });

  } catch (error) {
    console.error('組織情報取得エラー:', error);
    return NextResponse.json({
      success: false,
      error: {
        code: 'INTERNAL_SERVER_ERROR',
        message: '組織情報の取得中にエラーが発生しました'
      }
    }, { status: 500 });
  }
}
