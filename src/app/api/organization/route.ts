/**
 * 要求仕様ID: API-013
 * 設計書: docs/design/api/specs/API定義書_API-013_組織情報取得API.md
 * 実装内容: 組織情報（部署・役職・職種）取得API
 */

import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET(request: NextRequest) {
  try {
    console.log('🏢 組織情報取得API開始')

    // 部署情報を取得
    const departments = await prisma.department.findMany({
      where: {
        department_status: 'ACTIVE'
      },
      select: {
        department_code: true,
        department_name: true,
        department_name_short: true,
        department_level: true,
        sort_order: true
      },
      orderBy: {
        sort_order: 'asc'
      }
    })

    // 役職情報を取得
    const positions = await prisma.position.findMany({
      where: {
        position_status: 'ACTIVE'
      },
      select: {
        position_code: true,
        position_name: true,
        position_name_short: true,
        position_level: true,
        position_category: true,
        sort_order: true
      },
      orderBy: {
        sort_order: 'asc'
      }
    })

    // 職種情報を取得
    const jobTypes = await prisma.jobType.findMany({
      where: {
        is_active: true
      },
      select: {
        job_type_code: true,
        job_type_name: true,
        job_category: true,
        job_level: true,
        sort_order: true
      },
      orderBy: {
        sort_order: 'asc'
      }
    })

    console.log('📊 取得結果:', {
      departments: departments.length,
      positions: positions.length,
      jobTypes: jobTypes.length
    })

    return NextResponse.json({
      success: true,
      data: {
        departments: departments.map(dept => ({
          id: dept.department_code,
          code: dept.department_code,
          name: dept.department_name,
          shortName: dept.department_name_short,
          level: dept.department_level
        })),
        positions: positions.map(pos => ({
          id: pos.position_code,
          code: pos.position_code,
          name: pos.position_name,
          shortName: pos.position_name_short,
          level: pos.position_level,
          category: pos.position_category
        })),
        jobTypes: jobTypes.map(job => ({
          id: job.job_type_code,
          code: job.job_type_code,
          name: job.job_type_name,
          category: job.job_category,
          level: job.job_level
        }))
      },
      timestamp: new Date().toISOString()
    })

  } catch (error) {
    console.error('❌ 組織情報取得エラー:', error)
    
    return NextResponse.json({
      success: false,
      error: {
        code: 'ORGANIZATION_FETCH_ERROR',
        message: '組織情報の取得に失敗しました',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      timestamp: new Date().toISOString()
    }, { status: 500 })
  }
}
