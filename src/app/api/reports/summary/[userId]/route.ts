/**
 * レポートサマリーAPI
 * 要求仕様ID: RPT.1-SUM.1
 */

import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import {
  createSuccessResponse,
  createErrorResponse,
  createAuthErrorResponse,
  createNotFoundErrorResponse
} from '@/lib/api-utils';

// レポートサマリー取得API
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
    const year = searchParams.get('year') || new Date().getFullYear().toString();

    // 権限チェック（自分以外のレポートを見る場合）
    const currentEmployeeId = authResult.employeeId || currentUserId;
    if (targetUserId !== currentEmployeeId) {
      // TODO: 管理者権限チェックを実装
      // 現在は暫定的に403を返す
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'AUTHORIZATION_ERROR',
            message: '権限がありません'
          }
        },
        { status: 403 }
      );
    }

    // 年始と年末の日付を設定
    const startOfYear = new Date(`${year}-01-01`);
    const endOfYear = new Date(`${year}-12-31`);

    // 各種データの集計
    const [
      skillRecords,
      projectRecords,
      totalGoals,
      completedGoals,
      totalTrainingHours
    ] = await Promise.all([
      // スキル記録の取得
      prisma.skillRecord.findMany({
        where: {
          employee_id: targetUserId,
          is_deleted: false,
          created_at: {
            gte: startOfYear,
            lte: endOfYear
          }
        }
      }),
      
      // プロジェクト記録の取得
      prisma.projectRecord.findMany({
        where: {
          employee_id: targetUserId,
          is_deleted: false,
          start_date: {
            gte: startOfYear,
            lte: endOfYear
          }
        }
      }),
      
      // キャリア目標の総数
      prisma.goalProgress.count({
        where: {
          employee_id: targetUserId,
          is_deleted: false,
          created_at: {
            gte: startOfYear,
            lte: endOfYear
          }
        }
      }),
      
      // 完了したキャリア目標
      prisma.goalProgress.count({
        where: {
          employee_id: targetUserId,
          is_deleted: false,
          progress_rate: 100,
          created_at: {
            gte: startOfYear,
            lte: endOfYear
          }
        }
      }),
      
      // 研修時間の合計（仮想的な計算）
      Promise.resolve(40) // TODO: 実際の研修記録から計算
    ]);

    // スキル分析
    const skillsByCategory = skillRecords.reduce((acc, record) => {
      const category = record.skill_category || 'その他';
      if (!acc[category]) {
        acc[category] = [];
      }
      acc[category].push({
        name: record.skill_name || '不明',
        level: record.skill_level || 1,
        score: record.self_assessment_score || 0
      });
      return acc;
    }, {} as Record<string, Array<{ name: string; level: number; score: number }>>);

    // プロジェクト分析
    const projectsByStatus = projectRecords.reduce((acc, record) => {
      const status = record.status || 'active';
      acc[status] = (acc[status] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    // 技術スタック分析
    const technologies = projectRecords
      .map(record => record.technologies_used || '')
      .filter(tech => tech)
      .flatMap(tech => tech.split(',').map(t => t.trim()))
      .reduce((acc, tech) => {
        acc[tech] = (acc[tech] || 0) + 1;
        return acc;
      }, {} as Record<string, number>);

    // 成長トレンド分析（月別スキル記録数）
    const monthlyProgress = Array.from({ length: 12 }, (_, i) => {
      const month = i + 1;
      const monthStart = new Date(parseInt(year), i, 1);
      const monthEnd = new Date(parseInt(year), i + 1, 0);
      
      const skillCount = skillRecords.filter(record => {
        const recordDate = new Date(record.created_at || '');
        return recordDate >= monthStart && recordDate <= monthEnd;
      }).length;

      return {
        month,
        skillRecords: skillCount,
        projectMilestones: Math.floor(Math.random() * 3) // TODO: 実際のマイルストーン数
      };
    });

    // レスポンスデータの構築
    const summaryData = {
      overview: {
        year: parseInt(year),
        totalSkills: skillRecords.length,
        totalProjects: projectRecords.length,
        careerGoals: {
          total: totalGoals,
          completed: completedGoals,
          completionRate: totalGoals > 0 ? Math.round((completedGoals / totalGoals) * 100) : 0
        },
        trainingHours: totalTrainingHours,
        averageSkillLevel: skillRecords.length > 0 
          ? Math.round(skillRecords.reduce((sum, record) => sum + (record.skill_level || 1), 0) / skillRecords.length * 10) / 10
          : 0
      },
      skillAnalysis: {
        byCategory: skillsByCategory,
        topSkills: Object.entries(skillsByCategory)
          .flatMap(([category, skills]) => skills.map(skill => ({ ...skill, category })))
          .sort((a, b) => b.score - a.score)
          .slice(0, 10),
        skillGrowth: skillRecords.length // TODO: より詳細な成長分析
      },
      projectAnalysis: {
        byStatus: projectsByStatus,
        technologies: Object.entries(technologies)
          .sort(([, a], [, b]) => b - a)
          .slice(0, 10)
          .map(([name, count]) => ({ name, count })),
        totalDuration: projectRecords.reduce((sum, record) => {
          if (record.start_date && record.end_date) {
            const duration = new Date(record.end_date).getTime() - new Date(record.start_date).getTime();
            return sum + Math.floor(duration / (1000 * 60 * 60 * 24)); // 日数
          }
          return sum;
        }, 0)
      },
      growthTrend: {
        monthly: monthlyProgress,
        yearOverYear: {
          previousYear: parseInt(year) - 1,
          skillGrowth: Math.floor(Math.random() * 20) + 10, // TODO: 実際の成長率計算
          projectGrowth: Math.floor(Math.random() * 15) + 5
        }
      },
      recommendations: [
        {
          type: 'skill',
          priority: 'high',
          title: 'フロントエンド技術の強化',
          description: 'React, TypeScriptのスキルレベル向上が推奨されます',
          actionItems: ['React Hooks の深い理解', 'TypeScript の高度な型システム学習']
        },
        {
          type: 'career',
          priority: 'medium',
          title: 'リーダーシップ経験の蓄積',
          description: '小規模プロジェクトでのリーダー経験を積むことを推奨します',
          actionItems: ['チームリーダー研修受講', 'メンター活動への参加']
        }
      ]
    };

    return createSuccessResponse(summaryData);

  } catch (error) {
    console.error('Report Summary API Error:', error);
    return createErrorResponse(
      'INTERNAL_SERVER_ERROR',
      'サーバーエラーが発生しました',
      undefined,
      500
    );
  } finally {
    await prisma.$disconnect();
  }
}