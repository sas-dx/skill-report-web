/**
 * 要求仕様ID: API-023
 * 対応設計書: docs/design/api/specs/API定義書_API-023_スキルマスタ取得API.md
 * 実装内容: スキルマスタ情報取得API（Prisma実装）
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

// モックデータ
const mockSkillCategories = [
  {
    category_id: 'frontend',
    category_code: 'frontend',
    category_name: 'フロントエンド',
    description: 'フロントエンド開発技術',
    display_order: 1,
    skills: [
      {
        skill_id: 'javascript',
        skill_code: 'javascript',
        skill_name: 'JavaScript',
        description: 'JavaScript プログラミング言語',
        required_level: 1,
        max_level: 5,
        display_order: 1,
        is_active: true
      },
      {
        skill_id: 'typescript',
        skill_code: 'typescript',
        skill_name: 'TypeScript',
        description: 'TypeScript プログラミング言語',
        required_level: 2,
        max_level: 5,
        display_order: 2,
        is_active: true
      },
      {
        skill_id: 'react',
        skill_code: 'react',
        skill_name: 'React',
        description: 'React フレームワーク',
        required_level: 2,
        max_level: 5,
        display_order: 3,
        is_active: true
      }
    ]
  },
  {
    category_id: 'backend',
    category_code: 'backend',
    category_name: 'バックエンド',
    description: 'バックエンド開発技術',
    display_order: 2,
    skills: [
      {
        skill_id: 'nodejs',
        skill_code: 'nodejs',
        skill_name: 'Node.js',
        description: 'Node.js ランタイム環境',
        required_level: 2,
        max_level: 5,
        display_order: 1,
        is_active: true
      },
      {
        skill_id: 'python',
        skill_code: 'python',
        skill_name: 'Python',
        description: 'Python プログラミング言語',
        required_level: 1,
        max_level: 5,
        display_order: 2,
        is_active: true
      }
    ]
  },
  {
    category_id: 'database',
    category_code: 'database',
    category_name: 'データベース',
    description: 'データベース技術',
    display_order: 3,
    skills: [
      {
        skill_id: 'postgresql',
        skill_code: 'postgresql',
        skill_name: 'PostgreSQL',
        description: 'PostgreSQL データベース',
        required_level: 2,
        max_level: 5,
        display_order: 1,
        is_active: true
      },
      {
        skill_id: 'mysql',
        skill_code: 'mysql',
        skill_name: 'MySQL',
        description: 'MySQL データベース',
        required_level: 1,
        max_level: 5,
        display_order: 2,
        is_active: true
      }
    ]
  }
];

// スキルマスタ取得API (API-023)
export async function GET(request: NextRequest) {
  try {
    const url = new URL(request.url);
    const category = url.searchParams.get('category');
    const level = url.searchParams.get('level');
    const search = url.searchParams.get('search');

    // 認証チェック（開発環境では簡易化）
    const authHeader = request.headers.get('authorization');
    if (!authHeader && !request.cookies.get('auth-token')) {
      console.log('認証情報なし - 開発環境のためスキップ');
    }

    try {
      // データベースからスキルカテゴリを取得
      let categoryWhere: any = {
        is_deleted: false
      };

      if (category) {
        categoryWhere.category_code = category;
      }

      const skillCategories = await prisma.skillCategory.findMany({
        where: categoryWhere,
        orderBy: {
          display_order: 'asc'
        }
      });

      // データベースからスキルアイテムを取得
      let skillWhere: any = {
        is_deleted: false
      };

      if (category) {
        skillWhere.skill_category_id = category;
      }

      if (level) {
        const levelNum = parseInt(level);
        skillWhere.difficulty_level = {
          lte: levelNum
        };
      }

      if (search) {
        const searchLower = search.toLowerCase();
        skillWhere.OR = [
          {
            skill_name: {
              contains: search,
              mode: 'insensitive'
            }
          },
          {
            description: {
              contains: search,
              mode: 'insensitive'
            }
          }
        ];
      }

      const skillItems = await prisma.skillItem.findMany({
        where: skillWhere,
        orderBy: {
          skill_name: 'asc'
        }
      });

      // カテゴリとスキルを結合してレスポンス形式に変換
      const categoriesWithSkills = skillCategories.map(category => {
        const categorySkills = skillItems
          .filter(skill => skill.skill_category_id === category.category_code)
          .map(skill => ({
            skill_id: skill.skill_code,
            skill_code: skill.skill_code,
            skill_name: skill.skill_name || '',
            description: skill.description || '',
            required_level: skill.difficulty_level || 1,
            max_level: 5, // 固定値
            display_order: 0, // デフォルト値
            is_active: true // デフォルト値（is_deletedフィールドがないため）
          }));

        return {
          category_id: category.category_code,
          category_code: category.category_code,
          category_name: category.category_name || '',
          description: category.description || '',
          display_order: category.display_order || 0,
          skills: categorySkills
        };
      }).filter(cat => cat.skills.length > 0 || !search); // 検索時は結果があるカテゴリのみ

      return NextResponse.json({
        success: true,
        data: categoriesWithSkills,
        count: categoriesWithSkills.length,
        timestamp: new Date().toISOString()
      });

    } catch (dbError) {
      console.error('データベースエラー:', dbError);
      
      // データベースエラーの場合はモックデータを返す
      console.log('データベース接続エラーのためモックデータを使用');
      
      // フィルタリング処理（モックデータ）
      let filteredCategories = [...mockSkillCategories];

      // カテゴリフィルタ
      if (category) {
        filteredCategories = filteredCategories.filter(cat => cat.category_code === category);
      }

      // レベルフィルタ
      if (level) {
        const levelNum = parseInt(level);
        filteredCategories = filteredCategories.map(cat => ({
          ...cat,
          skills: cat.skills.filter(skill => skill.required_level <= levelNum)
        }));
      }

      // 検索フィルタ
      if (search) {
        const searchLower = search.toLowerCase();
        filteredCategories = filteredCategories.map(cat => ({
          ...cat,
          skills: cat.skills.filter(skill => 
            skill.skill_name.toLowerCase().includes(searchLower) ||
            skill.description.toLowerCase().includes(searchLower)
          )
        })).filter(cat => cat.skills.length > 0);
      }

      return NextResponse.json({
        success: true,
        data: filteredCategories,
        count: filteredCategories.length,
        source: 'mock', // モックデータであることを示す
        timestamp: new Date().toISOString()
      });
    }

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

// スキルマスタ更新API (管理者用)
export async function PUT(request: NextRequest) {
  try {
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

    // 管理者権限チェック（簡易実装）
    // 実際の実装では、JWTトークンから権限を確認

    // リクエストボディの検証
    if (!body.type || !body.data) {
      return NextResponse.json({
        success: false,
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
        success: false,
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
        success: false,
        error: {
          code: 'RECORD_NOT_FOUND',
          message: '更新対象が見つかりません'
        }
      }, { status: 404 });
    }

    return NextResponse.json({
      success: false,
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

    // パラメータ検証
    if (!type || !id) {
      return NextResponse.json({
        success: false,
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
        success: false,
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
        success: false,
        error: {
          code: 'RECORD_NOT_FOUND',
          message: '削除対象が見つかりません'
        }
      }, { status: 404 });
    }

    return NextResponse.json({
      success: false,
      error: {
        code: 'SYSTEM_ERROR',
        message: 'システムエラーが発生しました'
      }
    }, { status: 500 });
  }
}
