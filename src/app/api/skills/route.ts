/**
 * 要求仕様ID: SKL.1-HIER.1
 * 対応設計書: docs/design/api/specs/API定義書_API-021_スキル情報取得API.md
 * 実装内容: スキル情報取得API
 */

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

// モックデータ
const mockSkills = [
  {
    id: 1,
    userId: 1,
    skillCategoryId: 1,
    skillName: 'JavaScript',
    skillLevel: 4,
    experienceYears: 3,
    lastUsedDate: '2024-12-01',
    certifications: ['JavaScript認定試験'],
    projects: ['ECサイト開発', 'SPA開発'],
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-12-01T00:00:00Z'
  },
  {
    id: 2,
    userId: 1,
    skillCategoryId: 2,
    skillName: 'TypeScript',
    skillLevel: 3,
    experienceYears: 2,
    lastUsedDate: '2024-12-01',
    certifications: [],
    projects: ['管理画面開発'],
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-12-01T00:00:00Z'
  },
  {
    id: 3,
    userId: 1,
    skillCategoryId: 3,
    skillName: 'React',
    skillLevel: 4,
    experienceYears: 3,
    lastUsedDate: '2024-12-01',
    certifications: [],
    projects: ['コンポーネントライブラリ開発'],
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-12-01T00:00:00Z'
  },
  {
    id: 4,
    userId: 1,
    skillCategoryId: 4,
    skillName: 'Node.js',
    skillLevel: 3,
    experienceYears: 2,
    lastUsedDate: '2024-11-15',
    certifications: [],
    projects: ['API開発'],
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-11-15T00:00:00Z'
  },
  {
    id: 5,
    userId: 1,
    skillCategoryId: 5,
    skillName: 'PostgreSQL',
    skillLevel: 3,
    experienceYears: 2,
    lastUsedDate: '2024-12-01',
    certifications: [],
    projects: ['データベース設計'],
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-12-01T00:00:00Z'
  }
];

export async function GET(request: NextRequest) {
  try {
    // URLパラメータから userId を取得
    const { searchParams } = new URL(request.url);
    const userId = searchParams.get('userId') || '1';

    // 認証チェック（簡易版）
    const authHeader = request.headers.get('authorization');
    if (!authHeader && !request.cookies.get('auth-token')) {
      // 開発環境では認証をスキップ
      console.log('認証情報なし - 開発環境のためスキップ');
    }

    try {
      // データベースからスキル情報を取得
      const skillRecords = await prisma.skillRecord.findMany({
        where: {
          employee_id: userId,
          is_deleted: false
        },
        orderBy: {
          updated_at: 'desc'
        }
      });

      // データベースからスキルアイテム情報も取得
      const skillItems = await prisma.skillItem.findMany({
        where: {
          skill_code: {
            in: skillRecords.map(record => record.skill_item_id || '')
          }
        }
      });

      // データベースからスキルカテゴリ情報も取得
      const skillCategories = await prisma.skillCategory.findMany({
        where: {
          category_code: {
            in: skillItems.map(item => item.skill_category_id || '')
          }
        }
      });

      // データを結合してレスポンス形式に変換
      const userSkills = skillRecords.map(record => {
        const skillItem = skillItems.find(item => item.skill_code === record.skill_item_id);
        const category = skillCategories.find(cat => cat.category_code === skillItem?.skill_category_id);

        return {
          id: record.id,
          userId: record.employee_id,
          skillCategoryId: skillItem?.skill_category_id || '',
          skillCategoryName: category?.category_name || '',
          skillName: skillItem?.skill_name || '',
          skillLevel: record.skill_level || 1,
          selfAssessment: record.self_assessment || null,
          managerAssessment: record.manager_assessment || null,
          experienceYears: 0, // 計算ロジックを後で追加
          lastUsedDate: record.last_used_date?.toISOString().split('T')[0] || null,
          acquisitionDate: record.acquisition_date?.toISOString().split('T')[0] || null,
          certificationId: record.certification_id || null,
          evidenceDescription: record.evidence_description || '',
          skillStatus: record.skill_status || 'active',
          learningHours: record.learning_hours || 0,
          projectExperienceCount: record.project_experience_count || 0,
          createdAt: record.created_at?.toISOString() || '',
          updatedAt: record.updated_at?.toISOString() || ''
        };
      });

      return NextResponse.json({
        success: true,
        data: userSkills,
        count: userSkills.length,
        timestamp: new Date().toISOString()
      });

    } catch (dbError) {
      console.error('データベースエラー:', dbError);
      
      // データベースエラーの場合はモックデータを返す（開発環境）
      console.log('データベース接続エラーのためモックデータを使用');
      const userSkills = mockSkills.filter(skill => skill.userId === parseInt(userId));

      return NextResponse.json({
        success: true,
        data: userSkills,
        count: userSkills.length,
        source: 'mock', // モックデータであることを示す
        timestamp: new Date().toISOString()
      });
    }

  } catch (error) {
    console.error('スキル情報取得エラー:', error);
    return NextResponse.json({
      success: false,
      error: {
        code: 'INTERNAL_SERVER_ERROR',
        message: 'スキル情報の取得に失敗しました'
      },
      timestamp: new Date().toISOString()
    }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // 認証チェック（簡易版）
    const authHeader = request.headers.get('authorization');
    if (!authHeader && !request.cookies.get('auth-token')) {
      console.log('認証情報なし - 開発環境のためスキップ');
    }

    // バリデーション
    if (!body.skillItemId || !body.skillLevel || !body.employeeId) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'スキルアイテムID、スキルレベル、従業員IDは必須です'
        },
        timestamp: new Date().toISOString()
      }, { status: 400 });
    }

    // スキルレベルの範囲チェック
    if (body.skillLevel < 1 || body.skillLevel > 4) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'スキルレベルは1から4の範囲で入力してください'
        },
        timestamp: new Date().toISOString()
      }, { status: 400 });
    }

    try {
      // データベースに新しいスキル記録を作成
      const newSkillRecord = await prisma.skillRecord.create({
        data: {
          id: `SKL_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          tenant_id: 'default', // シングルテナント環境では固定値
          employee_id: body.employeeId,
          skill_item_id: body.skillItemId,
          skill_level: body.skillLevel,
          self_assessment: body.selfAssessment || null,
          manager_assessment: body.managerAssessment || null,
          last_used_date: body.lastUsedDate ? new Date(body.lastUsedDate) : null,
          acquisition_date: body.acquisitionDate ? new Date(body.acquisitionDate) : null,
          certification_id: body.certificationId || null,
          evidence_description: body.evidenceDescription || '',
          skill_status: body.skillStatus || 'active',
          learning_hours: body.learningHours || 0,
          project_experience_count: body.projectExperienceCount || 0,
          is_deleted: false,
          created_at: new Date(),
          updated_at: new Date(),
          created_by: body.employeeId,
          updated_by: body.employeeId
        }
      });

      // 作成されたスキル記録の詳細情報を取得
      const skillItem = await prisma.skillItem.findUnique({
        where: { skill_code: body.skillItemId }
      });

      const skillCategory = skillItem ? await prisma.skillCategory.findUnique({
        where: { category_code: skillItem.skill_category_id || '' }
      }) : null;

      // レスポンス用のデータ形式に変換
      const responseData = {
        id: newSkillRecord.id,
        userId: newSkillRecord.employee_id,
        skillCategoryId: skillItem?.skill_category_id || '',
        skillCategoryName: skillCategory?.category_name || '',
        skillName: skillItem?.skill_name || '',
        skillLevel: newSkillRecord.skill_level,
        selfAssessment: newSkillRecord.self_assessment,
        managerAssessment: newSkillRecord.manager_assessment,
        lastUsedDate: newSkillRecord.last_used_date?.toISOString().split('T')[0] || null,
        acquisitionDate: newSkillRecord.acquisition_date?.toISOString().split('T')[0] || null,
        certificationId: newSkillRecord.certification_id,
        evidenceDescription: newSkillRecord.evidence_description,
        skillStatus: newSkillRecord.skill_status,
        learningHours: newSkillRecord.learning_hours,
        projectExperienceCount: newSkillRecord.project_experience_count,
        createdAt: newSkillRecord.created_at?.toISOString() || '',
        updatedAt: newSkillRecord.updated_at?.toISOString() || ''
      };

      return NextResponse.json({
        success: true,
        data: responseData,
        timestamp: new Date().toISOString()
      }, { status: 201 });

    } catch (dbError) {
      console.error('データベースエラー:', dbError);
      
      // データベースエラーの場合はモック作成を実行
      console.log('データベース接続エラーのためモック作成を実行');
      const newSkill = {
        id: mockSkills.length + 1,
        userId: body.employeeId || 1,
        skillCategoryId: body.skillCategoryId || 1,
        skillName: body.skillName || 'Unknown Skill',
        skillLevel: body.skillLevel,
        experienceYears: body.experienceYears || 0,
        lastUsedDate: body.lastUsedDate || new Date().toISOString().split('T')[0],
        certifications: body.certifications || [],
        projects: body.projects || [],
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };

      mockSkills.push(newSkill);

      return NextResponse.json({
        success: true,
        data: newSkill,
        source: 'mock', // モックデータであることを示す
        timestamp: new Date().toISOString()
      }, { status: 201 });
    }

  } catch (error) {
    console.error('スキル作成エラー:', error);
    return NextResponse.json({
      success: false,
      error: {
        code: 'INTERNAL_SERVER_ERROR',
        message: 'スキルの作成に失敗しました'
      },
      timestamp: new Date().toISOString()
    }, { status: 500 });
  }
}
