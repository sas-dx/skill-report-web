/**
 * 要求仕様ID: NTF.1-LIST.1
 * 対応設計書: docs/design/api/specs/API定義書_API-091_通知取得API.md
 * 実装内容: 通知取得API
 */

import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import {
  createSuccessResponse,
  createErrorResponse,
  createAuthErrorResponse,
  createAuthorizationErrorResponse
} from '@/lib/api-utils';

// 通知取得API
export async function GET(
  request: NextRequest,
  { params }: { params: { userId: string } }
) {
  try {
    // 認証チェック
    const authResult = await verifyAuth(request);
    if (!authResult.success) {
      return createAuthErrorResponse();
    }

    if (!params || !params.userId) {
      return createErrorResponse(
        'INVALID_PARAMETER',
        'ユーザーIDが指定されていません',
        undefined,
        400
      );
    }

    const { userId } = params;
    const currentUserId = authResult.userId;

    // userIdが'me'の場合は認証されたユーザーのIDを使用
    const targetUserId = userId === 'me' ? (authResult.employeeId || currentUserId) : userId;

    // クエリパラメータの取得
    const { searchParams } = new URL(request.url);
    const status = searchParams.get('status'); // unread, read, all
    const type = searchParams.get('type'); // info, warning, error, success
    const limit = parseInt(searchParams.get('limit') || '20');
    const offset = parseInt(searchParams.get('offset') || '0');

    // 権限チェック（自分以外の通知を見る場合）
    const currentEmployeeId = authResult.employeeId || currentUserId;
    if (targetUserId !== currentEmployeeId) {
      // TODO: 管理者権限チェックを実装
      // 現在は暫定的に403を返す
      return createAuthorizationErrorResponse();
    }

    // 通知の取得条件を構築
    const whereCondition: any = {
      recipient_id: targetUserId,
      is_deleted: false
    };

    // ステータスフィルタ
    if (status && status !== 'all') {
      if (status === 'unread') {
        whereCondition.read_status = 'unread';
      } else if (status === 'read') {
        whereCondition.read_status = 'read';
      }
    }

    // タイプフィルタ
    if (type) {
      whereCondition.notification_type = type;
    }

    // 通知データの取得
    const [notifications, totalCount, unreadCount] = await Promise.all([
      prisma.notification.findMany({
        where: whereCondition,
        orderBy: [
          { priority_level: 'desc' },
          { created_at: 'desc' }
        ],
        take: limit,
        skip: offset
      }),
      prisma.notification.count({
        where: whereCondition
      }),
      prisma.notification.count({
        where: {
          ...whereCondition,
          read_status: 'unread'
        }
      })
    ]);

    // レスポンスデータの整形
    const formattedNotifications = notifications.map(notification => ({
      id: notification.notification_id || notification.id,
      type: notification.notification_type || 'info',
      title: notification.title,
      message: notification.message,
      is_read: notification.read_status === 'read',
      priority: notification.priority_level || 'normal',
      action_url: notification.action_url || null,
      metadata: notification.personalization_data ? JSON.parse(notification.personalization_data) : {},
      created_at: notification.created_at?.toISOString() || '',
      read_at: notification.read_at?.toISOString() || null,
      expires_at: notification.expiry_date?.toISOString() || null
    }));

    // サマリー情報
    const summary = {
      total: totalCount,
      unread: unreadCount,
      read: totalCount - unreadCount
    };

    // ページネーション情報
    const pagination = {
      limit,
      offset,
      hasMore: offset + limit < totalCount
    };

    return createSuccessResponse({
      notifications: formattedNotifications,
      summary,
      pagination
    });

  } catch (error) {
    console.error('通知取得エラー:', error);
    return createErrorResponse(
      'INTERNAL_SERVER_ERROR',
      'サーバーエラーが発生しました',
      error instanceof Error ? error.message : '不明なエラー',
      500
    );
  }
}

// 通知既読API
export async function PUT(
  request: NextRequest,
  { params }: { params: { userId: string } }
) {
  try {
    // 認証チェック
    const authResult = await verifyAuth(request);
    if (!authResult.success) {
      return createAuthErrorResponse();
    }

    const body = await request.json();
    const { userId } = params;
    const currentUserId = authResult.userId;

    // userIdが'me'の場合は認証されたユーザーのIDを使用
    const targetUserId = userId === 'me' ? (authResult.employeeId || currentUserId) : userId;

    // 権限チェック
    const currentEmployeeId = authResult.employeeId || currentUserId;
    if (targetUserId !== currentEmployeeId) {
      return createAuthorizationErrorResponse();
    }

    // 通知IDの検証
    if (!body.notificationIds || !Array.isArray(body.notificationIds)) {
      return createErrorResponse(
        'INVALID_PARAMETER',
        '通知IDが指定されていません',
        undefined,
        400
      );
    }

    // 既読処理
    const updateResult = await prisma.notification.updateMany({
      where: {
        notification_id: {
          in: body.notificationIds
        },
        ...(targetUserId && { recipient_id: targetUserId }),
        read_status: 'unread'
      },
      data: {
        read_status: 'read',
        read_at: new Date(),
        updated_at: new Date(),
        updated_by: targetUserId || 'system'
      }
    });

    return createSuccessResponse({
      updated: updateResult.count,
      message: `${updateResult.count}件の通知を既読にしました`
    });

  } catch (error) {
    console.error('通知既読エラー:', error);
    return createErrorResponse(
      'INTERNAL_SERVER_ERROR',
      'サーバーエラーが発生しました',
      error instanceof Error ? error.message : '不明なエラー',
      500
    );
  }
}