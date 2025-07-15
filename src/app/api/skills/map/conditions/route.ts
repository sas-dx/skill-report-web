/**
 * 要求仕様ID: SKL.3-MAP.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_SKL_Map_スキルマップ画面.md
 * API仕様書: docs/design/api/specs/API定義書_API-026_スキルマップ生成API.md
 * 実装内容: マップ条件取得API（API-600）
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
interface OrganizationOption {
  id: string;
  name: string;
  type: 'company' | 'department' | 'team';
  parentId?: string;
}

interface SkillCategoryOption {
  id: string;
  name: string;
  description?: string;
  skillCount: number;
}

interface DisplayTypeOption {
  id: string;
  name: string;
  description: string;
  icon: string;
}

interface ConditionsResponse {
  success: boolean;
  data: {
    organizations: OrganizationOption[];
    skillCategories: SkillCategoryOption[];
    displayTypes: DisplayTypeOption[];
  };
}

interface ErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
  };
}

type ApiResponse = ConditionsResponse | ErrorResponse;

/**
 * マップ条件取得API
 * エンドポイント: GET /api/skills/map/conditions
 * 目的: スキルマップ表示に必要な選択肢（組織、スキルカテゴリ、表示形式）を取得
 */
export async function GET(request: NextRequest): Promise<NextResponse<ApiResponse>> {
  try {
    // 認証チェック（開発環境では簡易化）
    const authHeader = request.headers.get('authorization');
    if (!authHeader && !request.cookies.get('auth-token')) {
      console.log('認証情報なし - 開発環境のためスキップ');
    }

    // 組織一覧（階層構造）
    const organizations: OrganizationOption[] = [
      {
        id: 'company_001',
        name: '全社',
        type: 'company'
      },
      {
        id: 'dept_001',
        name: '開発部',
        type: 'department',
        parentId: 'company_001'
      },
      {
        id: 'dept_002',
        name: '営業部',
        type: 'department',
        parentId: 'company_001'
      },
      {
        id: 'team_001',
        name: 'フロントエンドチーム',
        type: 'team',
        parentId: 'dept_001'
      },
      {
        id: 'team_002',
        name: 'バックエンドチーム',
        type: 'team',
        parentId: 'dept_001'
      },
      {
        id: 'team_003',
        name: 'インフラチーム',
        type: 'team',
        parentId: 'dept_001'
      }
    ];

    // スキルカテゴリ一覧
    const skillCategories: SkillCategoryOption[] = [
      {
        id: 'technical',
        name: '技術スキル',
        description: 'プログラミング、データベース、インフラ等の技術的スキル',
        skillCount: 45
      },
      {
        id: 'business',
        name: 'ビジネススキル',
        description: 'コミュニケーション、マネジメント、企画等のビジネススキル',
        skillCount: 25
      },
      {
        id: 'domain',
        name: 'ドメイン知識',
        description: '業界知識、業務知識等の専門領域スキル',
        skillCount: 18
      },
      {
        id: 'certification',
        name: '資格・認定',
        description: '各種資格、認定試験等',
        skillCount: 32
      }
    ];

    // 表示形式一覧
    const displayTypes: DisplayTypeOption[] = [
      {
        id: 'heatmap',
        name: 'ヒートマップ',
        description: 'スキル項目×社員のマトリクス表示',
        icon: '🔥'
      },
      {
        id: 'radar',
        name: 'レーダーチャート',
        description: 'スキル項目を軸とした多角形チャート',
        icon: '📊'
      },
      {
        id: 'bubble',
        name: 'バブルチャート',
        description: 'スキル分布を円の大きさで表現',
        icon: '🫧'
      },
      {
        id: 'treemap',
        name: 'ツリーマップ',
        description: '階層構造を矩形で表現',
        icon: '🌳'
      },
      {
        id: 'bar',
        name: '棒グラフ',
        description: 'スキルレベル別の人数分布',
        icon: '📈'
      }
    ];

    // TODO: 実際のデータベースからの取得
    // const organizations = await getOrganizationsForUser(auth.userId);
    // const skillCategories = await getSkillCategoriesWithCount();

    const response: ConditionsResponse = {
      success: true,
      data: {
        organizations,
        skillCategories,
        displayTypes
      }
    };

    return NextResponse.json(response, { status: 200 });

  } catch (error) {
    console.error('マップ条件取得API エラー:', error);
    
    const errorResponse: ErrorResponse = {
      success: false,
      error: {
        code: 'INTERNAL_SERVER_ERROR',
        message: 'サーバー内部エラーが発生しました'
      }
    };

    return NextResponse.json(errorResponse, { status: 500 });
  }
}

// TODO: 将来的な実装
// async function getOrganizationsForUser(userId: string): Promise<OrganizationOption[]> {
//   // ユーザーの権限に基づいて閲覧可能な組織一覧を取得
//   // 組織階層に基づくアクセス制御
// }

// async function getSkillCategoriesWithCount(): Promise<SkillCategoryOption[]> {
//   // スキルカテゴリ一覧とそれぞれのスキル数を取得
// }
