// API-082: ユーザーサマリー取得API
import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth } from '@/lib/auth';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export async function GET(request: NextRequest) {
  try {
    // 認証確認
    const authResult = await verifyAuth(request);
    if (!authResult.success || !authResult.userId) {
      return NextResponse.json(
        { success: false, error: '認証が必要です' },
        { status: 401 }
      );
    }

    const userId = authResult.userId;
    const employeeId = authResult.employeeId || userId;
    const tenantId = 'default'; // TODO: テナントIDを取得

    // ユーザー情報を取得
    const user = await prisma.employee.findFirst({
      where: {
        employee_code: employeeId,
        is_deleted: false
      }
    });

    if (!user) {
      return NextResponse.json(
        { success: false, error: 'ユーザーが見つかりません' },
        { status: 404 }
      );
    }

    // 部門とポジション情報を取得
    let department = null;
    let position = null;
    
    if (user.department_id) {
      department = await prisma.department.findFirst({
        where: { department_code: user.department_id }
      });
    }
    
    if (user.position_id) {
      position = await prisma.position.findFirst({
        where: { position_code: user.position_id }
      });
    }

    // 統計情報を取得
    const [skillCount, goalCount, certificationCount, trainingCount] = await Promise.all([
      // スキル数
      prisma.skillRecord.count({
        where: {
          employee_id: employeeId,
          skill_level: { gt: 0 },
          is_deleted: false
        }
      }),
      // 目標数
      prisma.goalProgress.count({
        where: {
          employee_id: employeeId,
          OR: [
            { achievement_status: 'in_progress' },
            { achievement_status: 'pending' }
          ],
          is_deleted: false
        }
      }),
      // 資格数 - PDUテーブルから資格取得済み(activity_type='certification', approval_status='approved')をカウント
      prisma.pDU.count({
        where: {
          employee_id: employeeId,
          activity_type: 'certification',
          approval_status: 'approved',
          is_deleted: false
        }
      }),
      // 研修数 - TrainingHistoryテーブルから完了済み研修をカウント
      prisma.trainingHistory.count({
        where: {
          employee_id: employeeId,
          attendance_status: 'completed',
          is_deleted: false
        }
      })
    ]);

    // 目標達成率を計算
    const completedGoals = await prisma.goalProgress.count({
      where: {
        employee_id: employeeId,
        OR: [
          { achievement_status: 'completed' },
          { achievement_status: 'achieved' }
        ],
        is_deleted: false
      }
    });
    
    const totalGoals = completedGoals + goalCount;
    const achievementRate = totalGoals > 0 ? Math.round((completedGoals / totalGoals) * 100) : 0;

    // 今月の成長率（仮データ）
    const growthRate = 5; // 実際は過去データと比較して計算

    // ユーザーサマリーデータを構築
    const userSummary = {
      user_info: {
        user_id: user.id,
        employee_id: user.employee_code || '',
        name: user.full_name || '',
        email: user.email || '',
        department_name: department?.department_name || '',
        position_name: position?.position_name || '',
        avatar_url: null,
        last_login: null
      },
      statistics: {
        skill_count: skillCount,
        goal_count: goalCount,
        certification_count: certificationCount,
        training_count: trainingCount,
        achievement_rate: achievementRate,
        growth_rate: growthRate
      },
      quick_stats: {
        skills: {
          total: skillCount,
          this_month: 3, // 仮データ
          trend: 'up' as const
        },
        goals: {
          active: goalCount,
          completed: completedGoals,
          achievement_rate: achievementRate
        },
        trainings: {
          completed: trainingCount,
          in_progress: 2, // 仮データ
          upcoming: 1 // 仮データ
        },
        certifications: {
          active: certificationCount,
          expiring_soon: 1 // 仮データ
        }
      }
    };

    return NextResponse.json({
      success: true,
      data: userSummary
    });

  } catch (error) {
    console.error('User summary fetch error:', error);
    return NextResponse.json(
      { success: false, error: 'データの取得に失敗しました' },
      { status: 500 }
    );
  }
}