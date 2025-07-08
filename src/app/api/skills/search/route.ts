/**
 * 要求仕様ID: API-030
 * 対応設計書: docs/design/api/specs/API定義書_API-030_スキル検索API.md
 * 実装内容: スキル検索API
 */

import { NextRequest, NextResponse } from 'next/server';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// スキル検索API (API-030)
export async function GET(request: NextRequest) {
  try {
    const url = new URL(request.url);
    const keyword = url.searchParams.get('keyword');
    const category = url.searchParams.get('category');
    const level = url.searchParams.get('level');
    const page = parseInt(url.searchParams.get('page') || '1');
    const limit = parseInt(url.searchParams.get('limit') || '20');
    const sort = url.searchParams.get('sort') || 'relevance';

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

    // 検索条件の構築
    const whereConditions: any = {};

    if (keyword) {
      whereConditions.OR = [
        { skill_name: { contains: keyword, mode: 'insensitive' } },
        { description: { contains: keyword, mode: 'insensitive' } },
        { skill_code: { contains: keyword, mode: 'insensitive' } }
      ];
    }

    if (category) {
      whereConditions.skill_category_id = category;
    }

    if (level) {
      whereConditions.difficulty_level = parseInt(level);
    }

    // ソート条件の構築
    let orderBy: any = {};
    switch (sort) {
      case 'name':
        orderBy = { skill_name: 'asc' };
        break;
      case 'level':
        orderBy = { difficulty_level: 'asc' };
        break;
      case 'category':
        orderBy = [
          { skill_category_id: 'asc' },
          { skill_name: 'asc' }
        ];
        break;
      default: // relevance
        orderBy = { skill_name: 'asc' };
        break;
    }

    // ページネーション計算
    const offset = (page - 1) * limit;

    // 総件数取得
    const totalCount = await prisma.skillItem.count({
      where: whereConditions
    });

    // スキル検索実行
    const skills = await prisma.skillItem.findMany({
      where: whereConditions,
      orderBy: orderBy,
      skip: offset,
      take: limit
    });

    // カテゴリ情報を別途取得
    const categoryIds = [...new Set(skills.map(skill => skill.skill_category_id).filter(id => id !== null))];
    const categories = await prisma.skillCategory.findMany({
      where: {
        category_code: {
          in: categoryIds
        }
      }
    });

    const categoryMap = categories.reduce((map, cat) => {
      map[cat.category_code] = cat;
      return map;
    }, {} as Record<string, any>);

    // レスポンス形式に変換
    const searchResults = skills.map(skill => {
      const category = skill.skill_category_id ? categoryMap[skill.skill_category_id] : null;
      return {
        skill_id: skill.skill_code,
        skill_code: skill.skill_code,
        skill_name: skill.skill_name,
        description: skill.description || '',
        category: {
          category_id: category?.category_code || '',
          category_name: category?.category_name || '',
          category_code: category?.category_code || ''
        },
        difficulty_level: skill.difficulty_level || 1,
        max_level: 5, // 固定値
        is_active: true, // 固定値
        relevance_score: keyword ? calculateRelevanceScore(skill, keyword) : 1.0
      };
    });

    // ページネーション情報
    const totalPages = Math.ceil(totalCount / limit);
    const hasNext = page < totalPages;
    const hasPrev = page > 1;

    // 検索統計情報
    const categoryStats = await prisma.skillItem.groupBy({
      by: ['skill_category_id'],
      where: whereConditions,
      _count: {
        skill_code: true
      }
    });

    const levelStats = await prisma.skillItem.groupBy({
      by: ['difficulty_level'],
      where: whereConditions,
      _count: {
        skill_code: true
      }
    });

    return NextResponse.json({
      results: searchResults,
      pagination: {
        current_page: page,
        total_pages: totalPages,
        total_count: totalCount,
        limit: limit,
        has_next: hasNext,
        has_prev: hasPrev
      },
      search_info: {
        keyword: keyword,
        category: category,
        level: level ? parseInt(level) : null,
        sort: sort,
        execution_time: Date.now() // 簡易実装
      },
      statistics: {
        total_results: totalCount,
        categories: categoryStats.map(stat => ({
          category_id: stat.skill_category_id,
          count: stat._count.skill_code
        })),
        levels: levelStats.map(stat => ({
          level: stat.difficulty_level || 1,
          count: stat._count.skill_code
        }))
      }
    });

  } catch (error) {
    console.error('スキル検索エラー:', error);
    return NextResponse.json({
      error: {
        code: 'SYSTEM_ERROR',
        message: 'システムエラーが発生しました'
      }
    }, { status: 500 });
  }
}

// 関連度スコア計算（簡易実装）
function calculateRelevanceScore(skill: any, keyword: string): number {
  let score = 0;
  const lowerKeyword = keyword.toLowerCase();
  const skillName = (skill.skill_name || '').toLowerCase();
  const description = (skill.description || '').toLowerCase();
  const skillCode = (skill.skill_code || '').toLowerCase();

  // スキル名での完全一致
  if (skillName === lowerKeyword) {
    score += 10;
  }
  // スキル名での部分一致
  else if (skillName.includes(lowerKeyword)) {
    score += 5;
  }

  // スキルコードでの一致
  if (skillCode.includes(lowerKeyword)) {
    score += 3;
  }

  // 説明での一致
  if (description.includes(lowerKeyword)) {
    score += 1;
  }

  // 最低スコアは0.1
  return Math.max(score / 10, 0.1);
}

// 検索候補取得API（オートコンプリート用）
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { query, limit = 10 } = body;

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

    if (!query || query.length < 2) {
      return NextResponse.json({
        suggestions: []
      });
    }

    // スキル名での候補検索
    const skillSuggestions = await prisma.skillItem.findMany({
      where: {
        OR: [
          { skill_name: { contains: query, mode: 'insensitive' } },
          { skill_code: { contains: query, mode: 'insensitive' } }
        ]
      },
      select: {
        skill_code: true,
        skill_name: true,
        skill_category_id: true
      },
      take: limit,
      orderBy: {
        skill_name: 'asc'
      }
    });

    // カテゴリ名での候補検索
    const categorySuggestions = await prisma.skillCategory.findMany({
      where: {
        OR: [
          { category_name: { contains: query, mode: 'insensitive' } },
          { category_code: { contains: query, mode: 'insensitive' } }
        ]
      },
      select: {
        category_code: true,
        category_name: true
      },
      take: Math.floor(limit / 2),
      orderBy: {
        category_name: 'asc'
      }
    });

    const suggestions = [
      ...skillSuggestions.map(skill => ({
        type: 'skill',
        id: skill.skill_code,
        text: skill.skill_name,
        category: skill.skill_category_id
      })),
      ...categorySuggestions.map(category => ({
        type: 'category',
        id: category.category_code,
        text: category.category_name,
        category: null
      }))
    ];

    return NextResponse.json({
      suggestions: suggestions.slice(0, limit),
      query: query
    });

  } catch (error) {
    console.error('検索候補取得エラー:', error);
    return NextResponse.json({
      error: {
        code: 'SYSTEM_ERROR',
        message: 'システムエラーが発生しました'
      }
    }, { status: 500 });
  }
}
