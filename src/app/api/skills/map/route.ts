/**
 * 要求仕様ID: SKL.3-MAP.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_SKL_Map_スキルマップ画面.md
 * API仕様書: docs/design/api/specs/API定義書_API-026_スキルマップ生成API.md
 * 実装内容: スキルマップ取得API（API-601）
 */

import { NextRequest, NextResponse } from 'next/server';

// 型定義
interface MapRequest {
  organizationIds: string[];
  skillCategoryIds: string[];
  displayType: 'heatmap' | 'radar' | 'bubble' | 'treemap' | 'bar';
  filters?: {
    skillLevelMin?: number;
    skillLevelMax?: number;
    employeeIds?: string[];
    positionIds?: string[];
  };
  pagination?: {
    page: number;
    limit: number;
  };
}

interface EmployeeSkillData {
  employeeId: string;
  employeeName: string;
  department: string;
  position: string;
  skills: {
    skillId: string;
    skillName: string;
    category: string;
    level: number;
    lastUpdated: string;
  }[];
}

interface SkillStatistics {
  skillId: string;
  skillName: string;
  category: string;
  averageLevel: number;
  employeeCount: number;
  levelDistribution: {
    level1: number;
    level2: number;
    level3: number;
    level4: number;
  };
}

interface HeatmapData {
  employees: string[];
  skills: string[];
  matrix: number[][];
}

interface RadarData {
  employeeId: string;
  employeeName: string;
  skillCategories: {
    category: string;
    averageLevel: number;
    maxLevel: number;
  }[];
}

interface BubbleData {
  skillId: string;
  skillName: string;
  x: number; // 平均レベル
  y: number; // 習得者数
  size: number; // 重要度
}

interface MapResponse {
  success: boolean;
  data: {
    displayType: string;
    totalEmployees: number;
    totalSkills: number;
    employees: EmployeeSkillData[];
    statistics: SkillStatistics[];
    visualization: {
      heatmap?: HeatmapData;
      radar?: RadarData[];
      bubble?: BubbleData[];
      treemap?: any;
      bar?: any;
    };
    pagination?: {
      page: number;
      limit: number;
      total: number;
      totalPages: number;
    };
  };
}

interface ErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: any;
  };
}

type ApiResponse = MapResponse | ErrorResponse;

/**
 * スキルマップ取得API
 * エンドポイント: POST /api/skills/map
 * 目的: 指定された条件に基づいてスキルマップデータを生成・取得
 */
export async function POST(request: NextRequest): Promise<NextResponse<ApiResponse>> {
  try {
    // TODO: 認証・認可チェック
    // const auth = await verifyAuth(request);
    // if (!auth.success) {
    //   const errorResponse: ErrorResponse = {
    //     success: false,
    //     error: { code: 'UNAUTHORIZED', message: '認証が必要です' }
    //   };
    //   return NextResponse.json(errorResponse, { status: 401 });
    // }

    // リクエストボディの解析
    const requestData: MapRequest = await request.json();

    // バリデーション
    if (!requestData.organizationIds || requestData.organizationIds.length === 0) {
      const errorResponse: ErrorResponse = {
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: '組織IDは必須です',
          details: { field: 'organizationIds' }
        }
      };
      return NextResponse.json(errorResponse, { status: 400 });
    }

    if (!requestData.displayType) {
      const errorResponse: ErrorResponse = {
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: '表示形式は必須です',
          details: { field: 'displayType' }
        }
      };
      return NextResponse.json(errorResponse, { status: 400 });
    }

    // モックデータ生成
    const employees: EmployeeSkillData[] = generateMockEmployeeData(requestData);
    const statistics: SkillStatistics[] = generateMockStatistics(requestData);
    const visualization = generateVisualizationData(requestData, employees);

    // ページネーション設定
    const page = requestData.pagination?.page || 1;
    const limit = requestData.pagination?.limit || 50;
    const total = employees.length;
    const totalPages = Math.ceil(total / limit);
    const startIndex = (page - 1) * limit;
    const endIndex = startIndex + limit;
    const paginatedEmployees = employees.slice(startIndex, endIndex);

    const response: MapResponse = {
      success: true,
      data: {
        displayType: requestData.displayType,
        totalEmployees: employees.length,
        totalSkills: statistics.length,
        employees: paginatedEmployees,
        statistics,
        visualization,
        pagination: {
          page,
          limit,
          total,
          totalPages
        }
      }
    };

    return NextResponse.json(response, { status: 200 });

  } catch (error) {
    console.error('スキルマップ取得API エラー:', error);
    
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

// モックデータ生成関数
function generateMockEmployeeData(request: MapRequest): EmployeeSkillData[] {
  const employees: EmployeeSkillData[] = [];
  
  for (let i = 1; i <= 20; i++) {
    const employee: EmployeeSkillData = {
      employeeId: `emp_${i.toString().padStart(3, '0')}`,
      employeeName: `社員${i}`,
      department: i <= 10 ? '開発部' : '営業部',
      position: i <= 5 ? 'シニア' : i <= 15 ? 'ミドル' : 'ジュニア',
      skills: generateMockSkills(request.skillCategoryIds)
    };
    employees.push(employee);
  }
  
  return employees;
}

function generateMockSkills(categoryIds: string[]) {
  const skillsMap: Record<string, string[]> = {
    technical: ['JavaScript', 'TypeScript', 'React', 'Node.js', 'PostgreSQL'],
    business: ['コミュニケーション', 'プレゼンテーション', 'プロジェクト管理', 'チームリーダーシップ'],
    domain: ['金融業界知識', 'システム設計', 'セキュリティ', 'クラウド技術'],
    certification: ['AWS認定', 'PMP', '情報処理技術者', 'TOEIC']
  };

  const skills = [];
  let skillIndex = 1;

  for (const categoryId of categoryIds) {
    const categorySkills = skillsMap[categoryId] || ['汎用スキル'];
    for (const skillName of categorySkills) {
      skills.push({
        skillId: `skill_${skillIndex.toString().padStart(3, '0')}`,
        skillName,
        category: categoryId,
        level: Math.floor(Math.random() * 4) + 1,
        lastUpdated: new Date().toISOString()
      });
      skillIndex++;
    }
  }

  return skills;
}

function generateMockStatistics(request: MapRequest): SkillStatistics[] {
  const statistics: SkillStatistics[] = [];
  let skillIndex = 1;

  const skillsMap: Record<string, string[]> = {
    technical: ['JavaScript', 'TypeScript', 'React', 'Node.js', 'PostgreSQL'],
    business: ['コミュニケーション', 'プレゼンテーション', 'プロジェクト管理', 'チームリーダーシップ'],
    domain: ['金融業界知識', 'システム設計', 'セキュリティ', 'クラウド技術'],
    certification: ['AWS認定', 'PMP', '情報処理技術者', 'TOEIC']
  };

  for (const categoryId of request.skillCategoryIds) {
    const categorySkills = skillsMap[categoryId] || ['汎用スキル'];
    for (const skillName of categorySkills) {
      const level1 = Math.floor(Math.random() * 5) + 1;
      const level2 = Math.floor(Math.random() * 8) + 2;
      const level3 = Math.floor(Math.random() * 6) + 1;
      const level4 = Math.floor(Math.random() * 3) + 1;
      const total = level1 + level2 + level3 + level4;

      statistics.push({
        skillId: `skill_${skillIndex.toString().padStart(3, '0')}`,
        skillName,
        category: categoryId,
        averageLevel: ((level1 * 1 + level2 * 2 + level3 * 3 + level4 * 4) / total),
        employeeCount: total,
        levelDistribution: { level1, level2, level3, level4 }
      });
      skillIndex++;
    }
  }

  return statistics;
}

function generateVisualizationData(request: MapRequest, employees: EmployeeSkillData[]) {
  const visualization: any = {};

  switch (request.displayType) {
    case 'heatmap':
      visualization.heatmap = generateHeatmapData(employees);
      break;
    case 'radar':
      visualization.radar = generateRadarData(employees);
      break;
    case 'bubble':
      visualization.bubble = generateBubbleData(employees);
      break;
    default:
      break;
  }

  return visualization;
}

function generateHeatmapData(employees: EmployeeSkillData[]): HeatmapData {
  const employeeNames = employees.map(emp => emp.employeeName);
  const allSkills = [...new Set(employees.flatMap(emp => emp.skills.map(skill => skill.skillName)))];
  
  const matrix = employees.map(employee => 
    allSkills.map(skillName => {
      const skill = employee.skills.find(s => s.skillName === skillName);
      return skill ? skill.level : 0;
    })
  );

  return {
    employees: employeeNames,
    skills: allSkills,
    matrix
  };
}

function generateRadarData(employees: EmployeeSkillData[]): RadarData[] {
  return employees.map(employee => {
    const categoryMap = new Map<string, { total: number, count: number }>();
    
    employee.skills.forEach(skill => {
      const current = categoryMap.get(skill.category) || { total: 0, count: 0 };
      categoryMap.set(skill.category, {
        total: current.total + skill.level,
        count: current.count + 1
      });
    });

    const skillCategories = Array.from(categoryMap.entries()).map(([category, data]) => ({
      category,
      averageLevel: data.total / data.count,
      maxLevel: 4
    }));

    return {
      employeeId: employee.employeeId,
      employeeName: employee.employeeName,
      skillCategories
    };
  });
}

function generateBubbleData(employees: EmployeeSkillData[]): BubbleData[] {
  const skillMap = new Map<string, { levels: number[], category: string }>();
  
  employees.forEach(employee => {
    employee.skills.forEach(skill => {
      const current = skillMap.get(skill.skillName) || { levels: [], category: skill.category };
      current.levels.push(skill.level);
      skillMap.set(skill.skillName, current);
    });
  });

  return Array.from(skillMap.entries()).map(([skillName, data], index) => {
    const averageLevel = data.levels.reduce((sum, level) => sum + level, 0) / data.levels.length;
    const employeeCount = data.levels.length;
    
    return {
      skillId: `skill_${(index + 1).toString().padStart(3, '0')}`,
      skillName,
      x: averageLevel,
      y: employeeCount,
      size: employeeCount * 2
    };
  });
}
