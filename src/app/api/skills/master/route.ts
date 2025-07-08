/**
 * 要求仕様ID: API-023
 * 対応設計書: docs/design/api/specs/API定義書_API-023_スキルマスタ取得API.md
 * 実装内容: スキルマスタ情報取得API
 */

import { NextRequest, NextResponse } from 'next/server';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// スキルマスタ取得API (API-023)
export async function GET(request: NextRequest) {
  try {
    const url = new URL(request.url);
    const category = url.searchParams.get('category');
    const level = url.searchParams.get('level');
    const search = url.searchParams.get('search');

    // 認証チェック（簡易実装）
    const authHeader = request.headers.get('authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json({
        error: {
          code: 'UNAUTHORIZED',
          message: '認証が必要です'
        }
      }, { status: 401 });
    }

    // スキルカテゴリマスタを取得
    const skillCategories = await prisma.skillCategory.findMany({
      where: {
        ...(category && { category_code: category })
      },
      orderBy: {
        display_order: 'asc'
      }
    });

    // スキルアイテムマスタを取得
    const whereConditions: any = {};

    if (category) {
      whereConditions.skill_category_id = category;
    }

    if (level) {
      whereConditions.difficulty_level = parseInt(level);
    }

    if (search) {
      whereConditions.OR = [
        { skill_name: { contains: search, mode: 'insensitive' } },
        { description: { contains: search, mode: 'insensitive' } }
      ];
    }

    const skillItems = await prisma.skillItem.findMany({
      where: whereConditions,
      orderBy: [
        { skill_category_id: 'asc' },
        { skill_code: 'asc' }
      ]
    });

    // レスポンス形式に変換
    const categories = skillCategories.map(category => ({
      category_id: category.category_code,
      category_code: category.category_code,
      category_name: category.category_name,
      description: category.description || '',
      display_order: category.display_order || 0,
      skills: skillItems
        .filter(item => item.skill_category_id === category.category_code)
        .map(item => ({
          skill_id: item.skill_code,
          skill_code: item.skill_code,
          skill_name: item.skill_name,
          description: item.description || '',
          required_level: item.difficulty_level || 1,
          max_level: 5, // 固定値
          display_order: 0, // 固定値
          is_active: true // 固定値
        }))
    }));

    // 統計情報を計算
    const totalCategories = skillCategories.length;
    const totalSkills = skillItems.length;
    const skillsByLevel = await prisma.skillItem.groupBy({
      by: ['difficulty_level'],
      where: {
        ...(category && { skill_category_id: category })
      },
      _count: {
        skill_code: true
      }
    });

    const levelDistribution = skillsByLevel.reduce((acc, item) => {
      acc[`level_${item.difficulty_level || 1}`] = item._count.skill_code;
      return acc;
    }, {} as Record<string, number>);

    return NextResponse.json({
      categories: categories,
      statistics: {
        total_categories: totalCategories,
        total_skills: totalSkills,
        level_distribution: levelDistribution
      },
      filters: {
        category: category,
        level: level ? parseInt(level) : null,
        search: search
      },
      last_updated: new Date().toISOString()
    });

  } catch (error) {
    console.error('スキルマスタ取得エラー:', error);
    return NextResponse.json({
      error: {
        code: 'SYSTEM_ERROR',
        message: 'システムエラーが発生しました'
      }
    }, { status: 500 });
  }
}

// スキルマスタ更新API (管理者用)
export async function PUT(request: NextRequest) {
  try {
    const body = await request.json();

    // 認証チェック（簡易実装）
    const authHeader = request.headers.get('authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json({
        error: {
          code: 'UNAUTHORIZED',
          message: '認証が必要です'
        }
      }, { status: 401 });
    }

    // 管理者権限チェック（簡易実装）
    // 実際の実装では、JWTトークンから権限を確認

    // リクエストボディの検証
    if (!body.type || !body.data) {
      return NextResponse.json({
        error: {
          code: 'INVALID_PARAMETER',
          message: 'パラメータが不正です'
        }
      }, { status: 400 });
    }

    let result;

    if (body.type === 'category') {
      // スキルカテゴリの更新
      if (body.data.category_id) {
        // 既存カテゴリの更新
        result = await prisma.skillCategory.update({
          where: { category_code: body.data.category_id },
          data: {
            category_name: body.data.category_name,
            description: body.data.description,
            display_order: body.data.display_order
          }
        });
      } else {
        // 新規カテゴリの作成
        result = await prisma.skillCategory.create({
          data: {
            category_code: body.data.category_code,
            category_name: body.data.category_name,
            description: body.data.description,
            display_order: body.data.display_order || 0,
            code: body.data.category_code,
            name: body.data.category_name
          }
        });
      }
    } else if (body.type === 'skill') {
      // スキルアイテムの更新
      if (body.data.skill_id) {
        // 既存スキルの更新
        result = await prisma.skillItem.update({
          where: { skill_code: body.data.skill_id },
          data: {
            skill_name: body.data.skill_name,
            description: body.data.description,
            difficulty_level: body.data.required_level
          }
        });
      } else {
        // 新規スキルの作成
        result = await prisma.skillItem.create({
          data: {
            skill_code: body.data.skill_code,
            skill_name: body.data.skill_name,
            description: body.data.description,
            skill_category_id: body.data.skill_category_id,
            difficulty_level: body.data.required_level || 1,
            code: body.data.skill_code,
            name: body.data.skill_name
          }
        });
      }
    } else {
      return NextResponse.json({
        error: {
          code: 'INVALID_TYPE',
          message: '更新タイプが不正です'
        }
      }, { status: 400 });
    }

    return NextResponse.json({
      success: true,
      type: body.type,
      data: result,
      updated_at: new Date().toISOString()
    });

  } catch (error) {
    console.error('スキルマスタ更新エラー:', error);
    
    if (error && typeof error === 'object' && 'code' in error && error.code === 'P2025') {
      return NextResponse.json({
        error: {
          code: 'RECORD_NOT_FOUND',
          message: '更新対象が見つかりません'
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

// スキルマスタ削除API (管理者用)
export async function DELETE(request: NextRequest) {
  try {
    const url = new URL(request.url);
    const type = url.searchParams.get('type');
    const id = url.searchParams.get('id');

    // 認証チェック（簡易実装）
    const authHeader = request.headers.get('authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json({
        error: {
          code: 'UNAUTHORIZED',
          message: '認証が必要です'
        }
      }, { status: 401 });
    }

    // パラメータ検証
    if (!type || !id) {
      return NextResponse.json({
        error: {
          code: 'INVALID_PARAMETER',
          message: 'パラメータが不正です'
        }
      }, { status: 400 });
    }

    let result;

    if (type === 'category') {
      // スキルカテゴリの削除
      result = await prisma.skillCategory.delete({
        where: { category_code: id }
      });
    } else if (type === 'skill') {
      // スキルアイテムの削除
      result = await prisma.skillItem.delete({
        where: { skill_code: id }
      });
    } else {
      return NextResponse.json({
        error: {
          code: 'INVALID_TYPE',
          message: '削除タイプが不正です'
        }
      }, { status: 400 });
    }

    return NextResponse.json({
      success: true,
      type: type,
      id: id,
      deleted_at: new Date().toISOString()
    });

  } catch (error) {
    console.error('スキルマスタ削除エラー:', error);
    
    if (error && typeof error === 'object' && 'code' in error && error.code === 'P2025') {
      return NextResponse.json({
        error: {
          code: 'RECORD_NOT_FOUND',
          message: '削除対象が見つかりません'
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
