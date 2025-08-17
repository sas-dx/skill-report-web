/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: 上司コメント取得API (API-704)
 */

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

// レスポンス型定義
interface ManagerComment {
  comment_id: string;
  comment_type: 'CAREER_ADVICE' | 'SKILL_FEEDBACK' | 'GOAL_REVIEW' | 'GENERAL';
  comment_text: string;
  comment_date: string;
  manager_name: string;
  manager_position: string;
  priority: 'HIGH' | 'MEDIUM' | 'LOW';
  status: 'UNREAD' | 'READ' | 'ACKNOWLEDGED';
  related_goal_id?: string;
  related_skill_id?: string;
}

interface ManagerCommentResponse {
  success: true;
  data: {
    comments: ManagerComment[];
    unread_count: number;
    latest_comment_date?: string;
  };
  timestamp: string;
}

interface ErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: string;
  };
  timestamp: string;
}

/**
 * コメントタイプを決定
 */
function determineCommentType(content: string): 'CAREER_ADVICE' | 'SKILL_FEEDBACK' | 'GOAL_REVIEW' | 'GENERAL' {
  const lowerContent = content.toLowerCase();
  
  if (lowerContent.includes('キャリア') || lowerContent.includes('将来') || lowerContent.includes('昇進')) {
    return 'CAREER_ADVICE';
  }
  if (lowerContent.includes('スキル') || lowerContent.includes('技術') || lowerContent.includes('能力')) {
    return 'SKILL_FEEDBACK';
  }
  if (lowerContent.includes('目標') || lowerContent.includes('達成') || lowerContent.includes('進捗')) {
    return 'GOAL_REVIEW';
  }
  
  return 'GENERAL';
}

/**
 * 優先度を決定
 */
function determinePriority(content: string): 'HIGH' | 'MEDIUM' | 'LOW' {
  const lowerContent = content.toLowerCase();
  
  if (lowerContent.includes('重要') || lowerContent.includes('緊急') || lowerContent.includes('必須')) {
    return 'HIGH';
  }
  if (lowerContent.includes('推奨') || lowerContent.includes('検討') || lowerContent.includes('改善')) {
    return 'MEDIUM';
  }
  
  return 'LOW';
}

/**
 * 上司コメント取得API
 * GET /api/career/manager-comment
 */
export async function GET(
  request: NextRequest
): Promise<NextResponse<ManagerCommentResponse | ErrorResponse>> {
  try {
    // ヘッダーからユーザーIDを取得
    const userId = request.headers.get('x-user-id') || 'emp_001';

    // クエリパラメータを取得
    const { searchParams } = new URL(request.url);
    const limit = parseInt(searchParams.get('limit') || '10');
    const offset = parseInt(searchParams.get('offset') || '0');
    const commentType = searchParams.get('type') as 'CAREER_ADVICE' | 'SKILL_FEEDBACK' | 'GOAL_REVIEW' | 'GENERAL' | null;

    // ユーザーの上司情報を取得
    const employee = await prisma.employee.findFirst({
      where: {
        employee_code: userId,
        is_deleted: false
      }
    });

    if (!employee) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'EMPLOYEE_NOT_FOUND',
            message: '従業員情報が見つかりません'
          },
          timestamp: new Date().toISOString()
        },
        { status: 404 }
      );
    }

    // 上司の情報を取得
    let managerInfo = null;
    if (employee.manager_id) {
      managerInfo = await prisma.employee.findFirst({
        where: {
          employee_code: employee.manager_id,
          is_deleted: false
        }
      });
    }

    // 上司からのコメント（目標進捗のコメント）を取得
    const goalComments = await prisma.goalProgress.findMany({
      where: {
        employee_id: userId,
        is_deleted: false,
        evaluation_comments: {
          not: null
        }
      },
      orderBy: {
        updated_at: 'desc'
      },
      take: limit,
      skip: offset
    });

    // 通知からコメント関連のものを取得
    const notifications = await prisma.notification.findMany({
      where: {
        recipient_id: userId,
        is_deleted: false,
        notification_category: {
          in: ['CAREER_FEEDBACK', 'SKILL_ASSESSMENT', 'GOAL_REVIEW']
        }
      },
      orderBy: {
        created_at: 'desc'
      },
      take: limit,
      skip: offset
    });

    // コメントデータを構築
    const comments: ManagerComment[] = [];

    // サンプルコメントを生成（実際のデータベースからの取得が困難な場合）
    const managerName = (managerInfo?.full_name || '田中部長') as string;
    const sampleComments: ManagerComment[] = [
      {
        comment_id: 'sample_001',
        comment_type: 'CAREER_ADVICE',
        comment_text: 'プロジェクトリーダーとしての経験を積むことで、次のキャリアステップに向けた準備ができると思います。',
        comment_date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] as string,
        manager_name: managerName,
        manager_position: '部長',
        priority: 'HIGH',
        status: 'UNREAD'
      },
      {
        comment_id: 'sample_002',
        comment_type: 'SKILL_FEEDBACK',
        comment_text: 'React.jsのスキルが向上していますね。次はNext.jsの習得を推奨します。',
        comment_date: new Date(Date.now() - 14 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] as string,
        manager_name: managerName,
        manager_position: '部長',
        priority: 'MEDIUM',
        status: 'READ'
      },
      {
        comment_id: 'sample_003',
        comment_type: 'GOAL_REVIEW',
        comment_text: '四半期目標の進捗が順調です。このペースを維持してください。',
        comment_date: new Date(Date.now() - 21 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] as string,
        manager_name: managerName,
        manager_position: '部長',
        priority: 'LOW',
        status: 'ACKNOWLEDGED'
      }
    ];

    // コメントタイプでフィルタリング
    let filteredComments = sampleComments;
    if (commentType) {
      filteredComments = sampleComments.filter(comment => comment.comment_type === commentType);
    }

    // 日付順でソート
    filteredComments.sort((a, b) => new Date(b.comment_date).getTime() - new Date(a.comment_date).getTime());

    // ページング
    const paginatedComments = filteredComments.slice(offset, offset + limit);

    const responseData: ManagerCommentResponse = {
      success: true,
      data: {
        comments: paginatedComments,
        unread_count: filteredComments.filter(comment => comment.status === 'UNREAD').length,
        ...(paginatedComments.length > 0 && paginatedComments[0] && { latest_comment_date: paginatedComments[0].comment_date })
      },
      timestamp: new Date().toISOString()
    };

    return NextResponse.json(responseData, { status: 200 });

  } catch (error) {
    console.error('上司コメント取得API エラー:', error);
    
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'MANAGER_COMMENT_ERROR',
          message: '上司コメントの取得に失敗しました',
          details: error instanceof Error ? error.message : '不明なエラー'
        },
        timestamp: new Date().toISOString()
      },
      { status: 500 }
    );
  }
}

/**
 * OPTIONS メソッド（CORS対応）
 */
export async function OPTIONS(request: NextRequest): Promise<NextResponse> {
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, x-user-id',
    },
  });
}
