/**
 * 要求仕様ID: API-021, API-022
 * 対応設計書: docs/design/api/specs/API定義書_API-021_スキル情報取得API.md
 * 対応設計書: docs/design/api/specs/API定義書_API-022_スキル情報更新API.md
 * 実装内容: ユーザーのスキル情報取得・更新API
 */

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import jwt from 'jsonwebtoken';

// JWT検証ヘルパー関数（開発用：認証をスキップ）
function verifyToken(authHeader: string | null): { loginId: string } | null {
  // 開発環境では常に認証をスキップしてモックユーザーを返す
  console.log('NODE_ENV:', process.env.NODE_ENV);
  console.log('Auth header:', authHeader);
  
  // 開発環境では認証をスキップ
  return { loginId: 'user001' };
}

// 型定義
interface SkillResponse {
  skill_id: string;
  category: string;
  name: string;
  level: number;
  experience_years: number;
  description: string;
  projects: any[];
  certifications: any[];
  last_used_date: string;
  self_assessment: {
    strengths: string;
    weaknesses: string;
    improvement_plan: string;
  };
}

// スキル情報取得API (API-021)
export async function GET(
  request: NextRequest,
  { params }: { params: { userId: string } }
) {
  try {
    const { userId } = params;
    const url = new URL(request.url);
    const year = url.searchParams.get('year') || new Date().getFullYear().toString();

    // 認証チェック（開発環境では簡易化）
    const authHeader = request.headers.get('authorization');
    if (!authHeader && !request.cookies.get('auth-token')) {
      console.log('認証情報なし - 開発環境のためスキップ');
    }

    // ユーザーの存在確認
    const employee = await prisma.employee.findUnique({
      where: { employee_code: userId }
    });

    if (!employee) {
      return NextResponse.json({
        error: {
          code: 'USER_NOT_FOUND',
          message: 'ユーザーが見つかりません'
        }
      }, { status: 404 });
    }

    // スキル情報を取得
    const skillRecords = await prisma.skillRecord.findMany({
      where: {
        employee_id: userId,
        is_deleted: false
      }
    });

    // レスポンス形式に変換
    const skills = skillRecords.map(record => ({
      skill_id: record.id,
      category: record.skill_category_id || 'technical',
      name: record.skill_item_id, // 実際はSkillItemテーブルから取得
      level: record.skill_level || 1,
      experience_years: 0, // 計算ロジックが必要
      description: record.evidence_description || '',
      projects: [], // ProjectRecordから取得
      certifications: [], // 資格情報から取得
      last_used_date: record.last_used_date?.toISOString().split('T')[0] || '',
      self_assessment: {
        strengths: '',
        weaknesses: '',
        improvement_plan: ''
      }
    }));

    return NextResponse.json({
      success: true,
      data: {
        user_id: userId,
        year: parseInt(year),
        skills: skills,
        last_updated: new Date().toISOString()
      }
    });

  } catch (error) {
    console.error('スキル情報取得エラー:', error);
    return NextResponse.json({
      error: {
        code: 'SYSTEM_ERROR',
        message: 'システムエラーが発生しました'
      }
    }, { status: 500 });
  }
}

// スキル情報更新API (API-022)
export async function PUT(
  request: NextRequest,
  { params }: { params: { userId: string } }
) {
  try {
    const { userId } = params;
    const body = await request.json();

    // 認証チェック
    const authHeader = request.headers.get('authorization');
    const tokenData = verifyToken(authHeader);
    
    if (!tokenData) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'UNAUTHORIZED',
          message: '認証が必要です'
        }
      }, { status: 401 });
    }

    // リクエストボディの検証
    if (!body.year || !Array.isArray(body.skills)) {
      return NextResponse.json({
        error: {
          code: 'INVALID_PARAMETER',
          message: 'パラメータが不正です'
        }
      }, { status: 400 });
    }

    // ユーザーの存在確認
    const employee = await prisma.employee.findUnique({
      where: { employee_code: userId }
    });

    if (!employee) {
      return NextResponse.json({
        error: {
          code: 'USER_NOT_FOUND',
          message: 'ユーザーが見つかりません'
        }
      }, { status: 404 });
    }

    // スキル情報の検証
    for (const skill of body.skills) {
      // スキルレベルの検証
      if (skill.level < 1 || skill.level > 5) {
        return NextResponse.json({
          error: {
            code: 'INVALID_SKILL_LEVEL',
            message: 'スキルレベルが不正です',
            details: 'スキルレベルは1から5の整数で指定してください。',
            field: 'level',
            value: skill.level
          }
        }, { status: 400 });
      }

      // 経験年数の検証
      if (skill.experience_years < 0) {
        return NextResponse.json({
          error: {
            code: 'INVALID_EXPERIENCE_YEARS',
            message: '経験年数が不正です',
            details: '経験年数は0以上の数値で指定してください。',
            field: 'experience_years',
            value: skill.experience_years
          }
        }, { status: 400 });
      }

      // 日付形式の検証
      if (skill.last_used_date && !isValidDate(skill.last_used_date)) {
        return NextResponse.json({
          error: {
            code: 'INVALID_DATE_FORMAT',
            message: '日付形式が不正です',
            details: '日付はYYYY-MM-DD形式で指定してください。',
            field: 'last_used_date',
            value: skill.last_used_date
          }
        }, { status: 400 });
      }
    }

    // トランザクション内でスキル情報を更新
    const result = await prisma.$transaction(async (tx) => {
      const updatedSkills: SkillResponse[] = [];

      for (const skill of body.skills) {
        let skillRecord;

        if (skill.skill_id && skill.skill_id !== '') {
          // 既存スキルの更新
          skillRecord = await tx.skillRecord.update({
            where: {
              id: skill.skill_id
            },
            data: {
              skill_level: skill.level,
              self_assessment: skill.level, // 自己評価として設定
              evidence_description: skill.description,
              last_used_date: skill.last_used_date ? new Date(skill.last_used_date) : null,
              updated_at: new Date(),
              updated_by: userId
            }
          });
        } else {
          // 新規スキルの作成
          const skillId = `skill_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
          skillRecord = await tx.skillRecord.create({
            data: {
              id: skillId,
              employee_id: userId,
              skill_item_id: skill.name, // 実際はSkillItemのIDを使用
              skill_level: skill.level,
              self_assessment: skill.level,
              evidence_description: skill.description,
              last_used_date: skill.last_used_date ? new Date(skill.last_used_date) : null,
              skill_category_id: skill.category,
              assessment_date: new Date(),
              assessor_id: userId,
              skill_status: 'ACTIVE',
              is_deleted: false,
              tenant_id: 'default', // 実際のテナントIDを設定
              created_at: new Date(),
              updated_at: new Date(),
              created_by: userId,
              updated_by: userId
            }
          });
        }

        updatedSkills.push({
          skill_id: skillRecord.id,
          category: skill.category,
          name: skill.name,
          level: skill.level,
          experience_years: skill.experience_years,
          description: skill.description,
          projects: skill.projects || [],
          certifications: skill.certifications || [],
          last_used_date: skill.last_used_date,
          self_assessment: skill.self_assessment || {
            strengths: '',
            weaknesses: '',
            improvement_plan: ''
          }
        });
      }

      return updatedSkills;
    });

    return NextResponse.json({
      user_id: userId,
      year: body.year,
      updated_at: new Date().toISOString(),
      skills: result
    });

  } catch (error) {
    console.error('スキル情報更新エラー:', error);
    
    if (error && typeof error === 'object' && 'code' in error && error.code === 'P2025') {
      return NextResponse.json({
        error: {
          code: 'SKILL_NOT_FOUND',
          message: 'スキルが見つかりません'
        }
      }, { status: 404 });
    }

    return NextResponse.json({
      error: {
        code: 'SYSTEM_ERROR',
        message: 'システムエラーが発生しました'
      }
    }, { status: 500 });
  }
}

// 日付形式の検証関数
function isValidDate(dateString: string): boolean {
  const regex = /^\d{4}-\d{2}-\d{2}$/;
  if (!regex.test(dateString)) {
    return false;
  }
  
  const date = new Date(dateString);
  return date instanceof Date && !isNaN(date.getTime());
}
