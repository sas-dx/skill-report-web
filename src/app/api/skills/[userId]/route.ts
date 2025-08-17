/**
 * 要求仕様ID: SKL.1-GET.1
 * 対応設計書: docs/design/api/specs/API定義書_API-020_スキル情報取得API.md
 * 実装内容: ユーザーのスキル情報取得API
 */

import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import { createSuccessResponse, createAuthErrorResponse, createNotFoundErrorResponse, createSystemErrorResponse } from '@/lib/api-utils';

/**
 * ユーザーのスキル情報取得API
 * @param request NextRequest
 * @param params パラメータ { userId: string }
 * @returns NextResponse
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { userId: string } }
) {
  try {
    // 認証チェック
    const authResult = await verifyAuth(request);
    if (!authResult.success) {
      return createAuthErrorResponse('認証が必要です');
    }

    if (!authResult.userId) {
      return createAuthErrorResponse('無効な認証トークンです');
    }

    const { userId } = params;
    const currentEmployeeId = authResult.employeeId || authResult.userId;
    
    // userIdが'me'の場合は認証されたユーザーのIDを使用
    const targetUserId = userId === 'me' ? currentEmployeeId : userId;

    // 権限チェック（自分のデータのみアクセス可能）
    if (targetUserId !== currentEmployeeId) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'AUTHORIZATION_ERROR',
            message: '自分以外のスキル情報にはアクセスできません'
          }
        },
        { status: 403 }
      );
    }

    // クエリパラメータの取得
    const { searchParams } = new URL(request.url);
    const categoryId = searchParams.get('categoryId');
    const includeExpired = searchParams.get('includeExpired') === 'true';
    const includeEvidence = searchParams.get('includeEvidence') === 'true';

    console.log('Skills API - Parameters:', {
      userId: targetUserId,
      categoryId,
      includeExpired,
      includeEvidence
    });

    // ユーザーの存在確認
    const user = await prisma.employee.findUnique({
      where: { employee_code: targetUserId }
    });

    if (!user) {
      return createNotFoundErrorResponse('ユーザー', targetUserId);
    }

    // スキルレコードの取得条件を構築
    const whereCondition: any = {
      employee_id: targetUserId,
      is_deleted: false
    };

    // カテゴリでフィルタリング
    if (categoryId) {
      whereCondition.skill_category_id = categoryId;
    }

    // 期限切れスキルの除外（オプション）
    if (!includeExpired) {
      whereCondition.OR = [
        { expiry_date: null },
        { expiry_date: { gt: new Date() } }
      ];
    }

    // スキルレコードの取得
    const skillRecords = await prisma.skillRecord.findMany({
      where: whereCondition,
      orderBy: [
        { skill_category_id: 'asc' },
        { updated_at: 'desc' }
      ]
    });

    // スキルアイテムの詳細情報を取得
    const skillItems = await Promise.all(
      skillRecords.map(async (record) => {
        const skillItem = await prisma.skillItem.findUnique({
          where: { skill_code: record.skill_item_id || '' }
        });
        return { record, skillItem };
      })
    );

    // スキルカテゴリの詳細情報を取得
    const categoryMap = new Map();
    for (const { record } of skillItems) {
      if (record.skill_category_id && !categoryMap.has(record.skill_category_id)) {
        const category = await prisma.skillCategory.findUnique({
          where: { category_code: record.skill_category_id }
        });
        if (category) {
          categoryMap.set(record.skill_category_id, category);
        }
      }
    }

    // エビデンス情報の取得（オプション）
    let evidenceMap = new Map();
    if (includeEvidence) {
      const evidences = await prisma.skillEvidence.findMany({
        where: {
          employee_id: targetUserId,
          is_deleted: false
        }
      });
      
      evidences.forEach(evidence => {
        if (evidence.skill_id) {
          if (!evidenceMap.has(evidence.skill_id)) {
            evidenceMap.set(evidence.skill_id, []);
          }
          evidenceMap.get(evidence.skill_id).push({
            evidenceId: evidence.evidence_id,
            evidenceType: evidence.evidence_type,
            evidenceTitle: evidence.evidence_title,
            evidenceDescription: evidence.evidence_description,
            evidenceDate: evidence.evidence_date?.toISOString(),
            verificationStatus: evidence.verification_status,
            filePath: evidence.file_path,
            externalUrl: evidence.external_url
          });
        }
      });
    }

    // レスポンスデータの構築
    const skillsByCategory = new Map();

    skillItems.forEach(({ record, skillItem }) => {
      const categoryId = record.skill_category_id || 'uncategorized';
      const category = categoryMap.get(categoryId);

      if (!skillsByCategory.has(categoryId)) {
        skillsByCategory.set(categoryId, {
          categoryId,
          categoryName: category?.category_name || '未分類',
          categoryDescription: category?.description || '',
          skills: []
        });
      }

      // スキルレベルの日本語表記への変換
      const getSkillLevelDisplay = (level: number | null) => {
        switch (level) {
          case 1: return '×';
          case 2: return '△';
          case 3: return '○';
          case 4: return '◎';
          default: return '未評価';
        }
      };

      const skillData = {
        skillRecordId: record.id,
        skillItemId: record.skill_item_id,
        skillId: record.skill_item_id,
        skillName: skillItem?.skill_name || '',
        skillLevel: record.skill_level || 0,
        skillLevelDisplay: getSkillLevelDisplay(record.skill_level),
        selfAssessment: record.self_assessment || 0,
        selfAssessmentDisplay: getSkillLevelDisplay(record.self_assessment),
        managerAssessment: record.manager_assessment || 0,
        managerAssessmentDisplay: getSkillLevelDisplay(record.manager_assessment),
        evidenceDescription: record.evidence_description || '',
        acquisitionDate: record.acquisition_date?.toISOString().split('T')[0] || '',
        lastUsedDate: record.last_used_date?.toISOString().split('T')[0] || '',
        expiryDate: record.expiry_date?.toISOString().split('T')[0] || '',
        certificationId: record.certification_id || '',
        skillStatus: record.skill_status || 'active',
        learningHours: record.learning_hours || 0,
        projectExperienceCount: record.project_experience_count || 0,
        assessmentDate: record.assessment_date?.toISOString().split('T')[0] || '',
        assessorId: record.assessor_id || '',
        lastUpdated: record.updated_at.toISOString(),
        ...(includeEvidence && {
          evidences: evidenceMap.get(record.skill_item_id) || []
        })
      };

      skillsByCategory.get(categoryId).skills.push(skillData);
    });

    // Map から配列に変換
    const categorizedSkills = Array.from(skillsByCategory.values());

    // サマリー情報の計算
    const totalSkills = skillRecords.length;
    const skillsByLevel = skillRecords.reduce((acc, record) => {
      const level = record.skill_level || 0;
      const levelKey = getSkillLevelDisplay(level);
      acc[levelKey] = (acc[levelKey] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    // 最新更新日の取得
    const lastUpdated = skillRecords.length > 0 
      ? Math.max(...skillRecords.map(record => record.updated_at.getTime()))
      : Date.now();

    const responseData = {
      userId,
      summary: {
        totalSkills,
        skillsByLevel,
        lastUpdated: new Date(lastUpdated).toISOString()
      },
      skills: categorizedSkills,
      filters: {
        categoryId: categoryId || null,
        includeExpired,
        includeEvidence
      }
    };

    return createSuccessResponse(responseData);

  } catch (error) {
    console.error('Skills fetch error:', error);
    return createSystemErrorResponse(error as Error);
  }
}

// スキルレベルの日本語表記への変換ヘルパー関数
function getSkillLevelDisplay(level: number | null): string {
  switch (level) {
    case 1: return '×';
    case 2: return '△';
    case 3: return '○';
    case 4: return '◎';
    default: return '未評価';
  }
}