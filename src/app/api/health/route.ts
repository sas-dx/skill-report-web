/**
 * ヘルスチェックAPI
 * 要求仕様ID: PLT.1-DOCKER.1 - コンテナヘルスチェック
 */

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

/**
 * GET /api/health
 * アプリケーションとデータベースの健全性をチェック
 */
export async function GET(request: NextRequest) {
  try {
    const startTime = Date.now();

    // データベース接続チェック
    let dbStatus = 'unknown';
    let dbResponseTime = 0;

    try {
      const dbStartTime = Date.now();
      await prisma.$queryRaw`SELECT 1`;
      dbResponseTime = Date.now() - dbStartTime;
      dbStatus = 'healthy';
    } catch (dbError) {
      console.error('Database health check failed:', dbError);
      dbStatus = 'unhealthy';

      // データベースが接続できない場合はサービス利用不可
      return NextResponse.json(
        {
          status: 'unhealthy',
          timestamp: new Date().toISOString(),
          checks: {
            application: 'healthy',
            database: 'unhealthy',
          },
          error: 'Database connection failed',
        },
        { status: 503 }
      );
    }

    const totalResponseTime = Date.now() - startTime;

    // すべてのチェックが成功
    return NextResponse.json(
      {
        status: 'healthy',
        timestamp: new Date().toISOString(),
        checks: {
          application: 'healthy',
          database: dbStatus,
        },
        performance: {
          database: `${dbResponseTime}ms`,
          total: `${totalResponseTime}ms`,
        },
        version: process.env.npm_package_version || 'unknown',
        environment: process.env.NODE_ENV || 'development',
      },
      { status: 200 }
    );
  } catch (error) {
    console.error('Health check failed:', error);

    return NextResponse.json(
      {
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        error: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 503 }
    );
  }
}

/**
 * HEAD /api/health
 * 軽量なヘルスチェック（レスポンスボディなし）
 */
export async function HEAD(request: NextRequest) {
  try {
    // 簡易的なチェック（DBクエリなし）
    return new NextResponse(null, { status: 200 });
  } catch (error) {
    return new NextResponse(null, { status: 503 });
  }
}
