/**
 * 要求仕様ID: API-023
 * 対応設計書: docs/design/api/specs/API定義書_API-023_スキルマスタ取得API.md
 * 実装内容: スキルマスタ情報取得API（Prisma実装）
 */

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

// JWT検証ヘルパー関数（開発用：認証をスキップ）
function verifyToken(authHeader: string | null): { employeeCode: string } | null {
  // 開発環境では常に認証をスキップしてモックユーザーを返す
  console.log('NODE_ENV:', process.env.NODE_ENV);
  console.log('Auth header:', authHeader);
  
  // 開発環境では認証をスキップ
  return { employeeCode: 'EMP001' };
}

// スキルマスタ取得API (API-023)
export async function GET(request: NextRequest) {
  try {
    const url = new URL(request.url);
    const category = url.searchParams.get('category');
    const type = url.searchParams.get('type');
    const level = url.searchParams.get('level');
    const search = url.searchParams.get('search');

    // 認証チェック（開発環境では簡易化）
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

    console.log('🔍 データベースからスキル階層データを取得中...');
    
    // カテゴリフィルタリングの条件を構築
    const categoryFilter: any = {
      category_status: 'active'
    };
    
    // カテゴリが指定されている場合のフィルタリング
    if (category) {
      // 指定されたカテゴリまたはその子カテゴリを取得
      categoryFilter.OR = [
        { category_code: category },
        { parent_category_id: category }
      ];
    }

    // データベースからスキルカテゴリとスキル項目を取得
    const [skillCategories, skillItems] = await Promise.all([
      prisma.skillCategory.findMany({
        where: categoryFilter,
        orderBy: [
          { category_level: 'asc' },
          { display_order: 'asc' }
        ]
      }),
      prisma.skillItem.findMany({
        where: category ? { 
          skill_category_id: {
            in: await prisma.skillCategory.findMany({
              where: categoryFilter,
              select: { category_code: true }
            }).then(cats => cats.map(c => c.category_code))
          }
        } : {},
        orderBy: [
          { skill_category_id: 'asc' },
          { difficulty_level: 'asc' },
          { skill_name: 'asc' }
        ]
      })
    ]);

    console.log(`📊 取得データ: カテゴリ ${skillCategories.length}件, スキル項目 ${skillItems.length}件`);

    // 階層構造を構築
    const hierarchyMap = new Map();
    
    // 1階層目：メインカテゴリ
    const mainCategories = skillCategories.filter(cat => cat.category_level === 1);
    console.log('📋 メインカテゴリ:', mainCategories.map(c => `${c.category_code}: ${c.category_name}`));
    
    mainCategories.forEach(category => {
      hierarchyMap.set(category.category_code, {
        id: category.category_code,
        name: category.category_name || category.name,
        category: category.category_name || category.name,
        level: 1,
        description: category.description || '',
        children: new Map()
      });
    });

    // 2階層目：サブカテゴリ
    const subCategories = skillCategories.filter(cat => cat.category_level === 2);
    console.log('📋 サブカテゴリ:', subCategories.map(c => `${c.category_code}: ${c.category_name} (親: ${c.parent_category_id})`));
    
    subCategories.forEach(category => {
      if (category.parent_category_id) {
        const parentCategory = hierarchyMap.get(category.parent_category_id);
        if (parentCategory) {
          parentCategory.children.set(category.category_code, {
            id: category.category_code,
            name: category.category_name || category.name,
            category: parentCategory.name,
            subcategory: category.category_name || category.name,
            parentId: category.parent_category_id,
            level: 2,
            description: category.description || '',
            children: []
          });
        }
      }
    });

    // 3階層目：スキル項目
    console.log('📋 スキル項目:', skillItems.map(s => `${s.skill_code}: ${s.skill_name} (カテゴリ: ${s.skill_category_id})`));
    
    skillItems.forEach(skill => {
      const categoryId = skill.skill_category_id;
      if (categoryId) {
        // サブカテゴリに属する場合を探す
        let found = false;
        for (const [parentId, parentCategory] of hierarchyMap) {
          const subcategory = parentCategory.children.get(categoryId);
          if (subcategory) {
            subcategory.children.push({
              id: skill.skill_code,
              name: skill.skill_name || skill.name,
              category: parentCategory.name,
              subcategory: subcategory.name,
              parentId: categoryId,
              level: 3,
              description: skill.description || '',
              difficulty_level: skill.difficulty_level,
              importance_level: skill.importance_level
            });
            found = true;
            break;
          }
        }
        
        // サブカテゴリが見つからない場合、メインカテゴリ直下に配置
        if (!found) {
          const directCategory = hierarchyMap.get(categoryId);
          if (directCategory && directCategory.level === 1) {
            if (!directCategory.children.has('default')) {
              directCategory.children.set('default', {
                id: `${categoryId}_default`,
                name: 'その他',
                category: directCategory.name,
                subcategory: 'その他',
                parentId: categoryId,
                level: 2,
                description: '',
                children: []
              });
            }
            directCategory.children.get('default').children.push({
              id: skill.skill_code,
              name: skill.skill_name || skill.name,
              category: directCategory.name,
              subcategory: 'その他',
              parentId: `${categoryId}_default`,
              level: 3,
              description: skill.description || '',
              difficulty_level: skill.difficulty_level,
              importance_level: skill.importance_level
            });
          }
        }
      }
    });

    // Map構造を配列に変換
    const hierarchyData = Array.from(hierarchyMap.values()).map(category => ({
      ...category,
      children: Array.from(category.children.values())
    }));

    console.log('✅ 階層データ構築完了:', hierarchyData.length, '個のメインカテゴリ');
    hierarchyData.forEach((cat: any) => {
      console.log(`  📁 ${cat.name}: ${cat.children.length}個のサブカテゴリ`);
      cat.children.forEach((sub: any) => {
        console.log(`    📂 ${sub.name}: ${sub.children.length}個のスキル`);
      });
    });

    return NextResponse.json({
      success: true,
      data: hierarchyData,
      count: hierarchyData.length,
      source: 'database',
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('スキルマスタ取得エラー:', error);
    return NextResponse.json({
      success: false,
      error: {
        code: 'SYSTEM_ERROR',
        message: 'システムエラーが発生しました'
      },
      timestamp: new Date().toISOString()
    }, { status: 500 });
  }
}

// スキルカテゴリ取得API
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action } = body;

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

    if (action === 'getCategories') {
      try {
        // データベースからスキルカテゴリを取得
        const categories = await prisma.skillCategory.findMany({
          where: {
            category_status: 'active'
          },
          orderBy: {
            display_order: 'asc'
          }
        });

        const categoriesData = categories.map(category => ({
          category_id: category.category_code,
          name: category.category_name || category.name,
          description: category.description || '',
          type: category.category_type || 'technical',
          level: category.category_level || 1,
          parent_id: category.parent_category_id || null,
          is_leaf: category.is_leaf_category || false,
          skill_count: category.skill_count || 0,
          display_order: category.display_order || 0,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }));

        return NextResponse.json({
          success: true,
          data: categoriesData,
          count: categoriesData.length,
          timestamp: new Date().toISOString()
        });

      } catch (dbError) {
        console.error('データベースエラー:', dbError);
        
        return NextResponse.json({
          success: false,
          error: {
            code: 'DATABASE_ERROR',
            message: 'データベースエラーが発生しました'
          },
          timestamp: new Date().toISOString()
        }, { status: 500 });
      }
    }

    return NextResponse.json({
      success: false,
      error: {
        code: 'INVALID_ACTION',
        message: '無効なアクションです'
      }
    }, { status: 400 });

  } catch (error) {
    console.error('スキルカテゴリ取得エラー:', error);
    return NextResponse.json({
      success: false,
      error: {
        code: 'SYSTEM_ERROR',
        message: 'システムエラーが発生しました'
      },
      timestamp: new Date().toISOString()
    }, { status: 500 });
  }
}
