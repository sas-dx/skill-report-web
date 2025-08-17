/**
 * 要求仕様ID: SKL.1-CAT.1
 * 対応設計書: docs/design/api/specs/API定義書_API-021_スキルカテゴリマスタ取得API.md
 * 実装内容: スキルカテゴリのマスタデータ取得API
 */

import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import { createSuccessResponse, createAuthErrorResponse, createSystemErrorResponse } from '@/lib/api-utils';

/**
 * スキルカテゴリマスタデータ取得API
 * @param request NextRequest
 * @returns NextResponse
 */
export async function GET(request: NextRequest) {
  try {
    // 認証チェック
    const authResult = await verifyAuth(request);
    if (!authResult.success) {
      return createAuthErrorResponse('認証が必要です');
    }

    if (!authResult.userId) {
      return createAuthErrorResponse('無効な認証トークンです');
    }

    // クエリパラメータの取得
    const { searchParams } = new URL(request.url);
    const includeHierarchy = searchParams.get('includeHierarchy') === 'true';
    const includeStats = searchParams.get('includeStats') === 'true';
    const activeOnly = searchParams.get('activeOnly') !== 'false'; // デフォルトでアクティブのみ

    console.log('Skill Categories API - Parameters:', {
      includeHierarchy,
      includeStats,
      activeOnly
    });

    // スキルカテゴリの取得条件を構築
    const whereCondition: any = {
      is_deleted: false
    };

    if (activeOnly) {
      // category_statusがnullまたは'active'のものを取得
      whereCondition.OR = [
        { category_status: 'active' },
        { category_status: null }
      ];
    }

    // スキルカテゴリの取得
    const categories = await prisma.skillCategory.findMany({
      where: whereCondition,
      orderBy: [
        { display_order: 'asc' },
        { category_name: 'asc' }
      ]
    });

    // 階層構造の取得（オプション）
    let hierarchyMap = new Map();
    if (includeHierarchy) {
      const hierarchies = await prisma.skillHierarchy.findMany({
        where: {
          is_deleted: false,
          is_active: true
        },
        orderBy: [
          { hierarchy_level: 'asc' },
          { sort_order: 'asc' }
        ]
      });

      hierarchies.forEach(hierarchy => {
        if (!hierarchyMap.has(hierarchy.skill_id)) {
          hierarchyMap.set(hierarchy.skill_id, hierarchy);
        }
      });
    }

    // スキル数の統計情報の取得（オプション）
    let skillCountMap = new Map();
    if (includeStats) {
      // カテゴリ別のスキル数を取得
      const skillCounts = await prisma.skillItem.groupBy({
        by: ['skill_category_id'],
        where: {
          is_deleted: false
        },
        _count: {
          skill_code: true
        }
      });

      skillCounts.forEach(count => {
        if (count.skill_category_id) {
          skillCountMap.set(count.skill_category_id, count._count.skill_code);
        }
      });

      // カテゴリ別のユーザースキル保有数を取得
      const userSkillCounts = await prisma.skillRecord.groupBy({
        by: ['skill_category_id'],
        where: {
          is_deleted: false
        },
        _count: {
          id: true
        }
      });

      userSkillCounts.forEach(count => {
        if (count.skill_category_id) {
          const existing = skillCountMap.get(count.skill_category_id) || 0;
          skillCountMap.set(count.skill_category_id, {
            totalSkills: existing,
            userAssignments: count._count.id
          });
        }
      });
    }

    // 親子関係を構築するためのマップ
    const categoryMap = new Map();
    const rootCategories: any[] = [];
    
    // 全カテゴリをマップに追加
    categories.forEach(category => {
      const categoryData = {
        categoryId: category.category_code,
        categoryName: category.category_name,
        categoryNameShort: category.category_name_short,
        categoryNameEn: category.category_name_en,
        categoryType: category.category_type,
        categoryLevel: category.category_level,
        categoryPath: category.category_path,
        isSystemCategory: category.is_system_category,
        isLeafCategory: category.is_leaf_category,
        evaluationMethod: category.evaluation_method,
        maxLevel: category.max_level,
        iconUrl: category.icon_url,
        colorCode: category.color_code,
        displayOrder: category.display_order,
        isPopular: category.is_popular,
        categoryStatus: category.category_status,
        description: category.description,
        parentCategoryId: category.parent_category_id,
        children: [] as any[],
        ...(includeHierarchy && {
          hierarchy: hierarchyMap.get(category.category_code) ? {
            hierarchyLevel: hierarchyMap.get(category.category_code).hierarchy_level,
            skillPath: hierarchyMap.get(category.category_code).skill_path,
            sortOrder: hierarchyMap.get(category.category_code).sort_order,
            isLeaf: hierarchyMap.get(category.category_code).is_leaf
          } : null
        }),
        ...(includeStats && {
          statistics: {
            skillCount: typeof skillCountMap.get(category.category_code) === 'object' 
              ? skillCountMap.get(category.category_code).totalSkills || 0
              : skillCountMap.get(category.category_code) || 0,
            userAssignmentCount: typeof skillCountMap.get(category.category_code) === 'object'
              ? skillCountMap.get(category.category_code).userAssignments || 0
              : 0
          }
        }),
        createdAt: category.created_at.toISOString(),
        updatedAt: category.updated_at.toISOString()
      };

      categoryMap.set(category.category_code, categoryData);
    });

    // 親子関係を構築
    categoryMap.forEach((category, categoryId) => {
      if (category.parentCategoryId) {
        const parentCategory = categoryMap.get(category.parentCategoryId);
        if (parentCategory) {
          parentCategory.children.push(category);
        } else {
          // 親が見つからない場合はルートレベルに追加
          rootCategories.push(category);
        }
      } else {
        // 親がない場合はルートレベル
        rootCategories.push(category);
      }
    });

    // 子要素を表示順でソート
    const sortChildren = (categories: any[]) => {
      categories.forEach(category => {
        if (category.children.length > 0) {
          category.children.sort((a: any, b: any) => {
            return (a.displayOrder || 999) - (b.displayOrder || 999);
          });
          sortChildren(category.children);
        }
      });
    };

    sortChildren(rootCategories);

    // ルートカテゴリも表示順でソート
    rootCategories.sort((a, b) => {
      return (a.displayOrder || 999) - (b.displayOrder || 999);
    });

    // フラット形式のカテゴリリストも提供
    const flatCategories = Array.from(categoryMap.values()).sort((a, b) => {
      return (a.displayOrder || 999) - (b.displayOrder || 999);
    });

    // サマリー情報の計算
    const totalCategories = categories.length;
    const activeCategories = categories.filter(cat => cat.category_status === 'active').length;
    const leafCategories = categories.filter(cat => cat.is_leaf_category).length;
    const systemCategories = categories.filter(cat => cat.is_system_category).length;

    const responseData = {
      summary: {
        totalCategories,
        activeCategories,
        leafCategories,
        systemCategories,
        lastUpdated: categories.length > 0 
          ? Math.max(...categories.map(cat => cat.updated_at.getTime()))
          : Date.now()
      },
      hierarchicalCategories: rootCategories,
      flatCategories: flatCategories,
      filters: {
        includeHierarchy,
        includeStats,
        activeOnly
      }
    };

    return createSuccessResponse(responseData);

  } catch (error) {
    console.error('Skill categories fetch error:', error);
    return createSystemErrorResponse(error as Error);
  }
}