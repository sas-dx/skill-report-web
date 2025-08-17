/**
 * 要求仕様ID: API-013
 * 設計書: docs/design/api/specs/API定義書_API-013_組織情報取得API.md
 * 実装内容: 組織情報取得API（部署・役職・職種マスタ）
 */

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET(request: NextRequest) {
  try {
    console.log('📊 組織情報取得APIが呼び出されました');

    // 部署データ取得
    const departments = await prisma.department.findMany({
      select: {
        department_code: true,
        department_name: true,
        department_name_short: true,
        department_level: true,
      },
      orderBy: {
        department_code: 'asc',
      },
    });

    // 役職データ取得
    const positions = await prisma.position.findMany({
      select: {
        position_code: true,
        position_name: true,
        position_name_short: true,
        position_level: true,
        position_category: true,
      },
      orderBy: {
        position_code: 'asc',
      },
    });

    // 職種データ取得
    const jobTypes = await prisma.jobType.findMany({
      select: {
        job_type_code: true,
        job_type_name: true,
        job_category: true,
        job_level: true,
      },
      orderBy: {
        job_type_code: 'asc',
      },
    });

    console.log(`✅ 組織情報取得成功: 部署${departments.length}件、役職${positions.length}件、職種${jobTypes.length}件`);

    // レスポンスデータの整形
    const responseData = {
      departments: departments.map(dept => ({
        id: dept.department_code,
        code: dept.department_code,
        name: dept.department_name || '',
        shortName: dept.department_name_short || dept.department_name || '',
        level: dept.department_level || 1,
      })),
      positions: positions.map(pos => ({
        id: pos.position_code,
        code: pos.position_code,
        name: pos.position_name || '',
        shortName: pos.position_name_short || pos.position_name || '',
        level: pos.position_level || 1,
        category: pos.position_category || 'GENERAL',
      })),
      jobTypes: jobTypes.map(job => ({
        id: job.job_type_code,
        code: job.job_type_code,
        name: job.job_type_name || '',
        category: job.job_category || 'GENERAL',
        level: job.job_level || 'JUNIOR',
      })),
    };

    return NextResponse.json({
      success: true,
      data: responseData,
      timestamp: new Date().toISOString(),
    });

  } catch (error) {
    console.error('❌ 組織情報取得エラー:', error);
    
    return NextResponse.json({
      success: false,
      error: {
        code: 'ORGANIZATION_FETCH_ERROR',
        message: '組織情報の取得に失敗しました',
        details: error instanceof Error ? error.message : '不明なエラー',
      },
      timestamp: new Date().toISOString(),
    }, { status: 500 });
  }
}
