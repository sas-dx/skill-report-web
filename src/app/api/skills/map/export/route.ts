/**
 * 要求仕様ID: SKL.3-MAP.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_SKL_Map_スキルマップ画面.md
 * API仕様書: docs/design/api/specs/API定義書_API-026_スキルマップ生成API.md
 * 実装内容: マップデータエクスポートAPI（API-602）
 */

import { NextRequest, NextResponse } from 'next/server';

// 型定義
interface ExportRequest {
  organizationIds: string[];
  skillCategoryIds: string[];
  format: 'csv' | 'excel' | 'json';
  exportType: 'summary' | 'detailed' | 'statistics';
  filters?: {
    skillLevelMin?: number;
    skillLevelMax?: number;
    employeeIds?: string[];
    positionIds?: string[];
  };
  options?: {
    includeHeaders: boolean;
    includeStatistics: boolean;
    includeChartData: boolean;
  };
}

interface ExportResponse {
  success: boolean;
  data: {
    downloadUrl: string;
    fileName: string;
    fileSize: number;
    recordCount: number;
    expiresAt: string;
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

type ApiResponse = ExportResponse | ErrorResponse;

/**
 * マップデータエクスポートAPI
 * エンドポイント: POST /api/skills/map/export
 * 目的: スキルマップデータをCSV/Excel形式でエクスポート
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
    const requestData: ExportRequest = await request.json();

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

    if (!requestData.format) {
      const errorResponse: ErrorResponse = {
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'エクスポート形式は必須です',
          details: { field: 'format' }
        }
      };
      return NextResponse.json(errorResponse, { status: 400 });
    }

    if (!requestData.exportType) {
      const errorResponse: ErrorResponse = {
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'エクスポートタイプは必須です',
          details: { field: 'exportType' }
        }
      };
      return NextResponse.json(errorResponse, { status: 400 });
    }

    // エクスポートデータ生成
    const exportData = await generateExportData(requestData);
    
    // ファイル生成
    const fileInfo = await createExportFile(exportData, requestData);

    // レスポンス生成
    const response: ExportResponse = {
      success: true,
      data: {
        downloadUrl: fileInfo.downloadUrl,
        fileName: fileInfo.fileName,
        fileSize: fileInfo.fileSize,
        recordCount: fileInfo.recordCount,
        expiresAt: fileInfo.expiresAt
      }
    };

    return NextResponse.json(response, { status: 200 });

  } catch (error) {
    console.error('マップデータエクスポートAPI エラー:', error);
    
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

// エクスポートデータ生成
async function generateExportData(request: ExportRequest) {
  const { exportType, skillCategoryIds, organizationIds, filters } = request;

  switch (exportType) {
    case 'summary':
      return generateSummaryData(skillCategoryIds, organizationIds, filters);
    case 'detailed':
      return generateDetailedData(skillCategoryIds, organizationIds, filters);
    case 'statistics':
      return generateStatisticsData(skillCategoryIds, organizationIds, filters);
    default:
      throw new Error(`未対応のエクスポートタイプ: ${exportType}`);
  }
}

// サマリーデータ生成
function generateSummaryData(skillCategoryIds: string[], organizationIds: string[], filters?: any) {
  const headers = [
    '社員ID',
    '社員名',
    '部署',
    'ポジション',
    'スキルカテゴリ',
    '平均スキルレベル',
    '最高スキルレベル',
    '保有スキル数',
    '最終更新日'
  ];

  const rows: (string | number)[][] = [];
  
  // モックデータ生成
  for (let i = 1; i <= 50; i++) {
    for (const categoryId of skillCategoryIds) {
      const categoryName = getCategoryName(categoryId);
      const avgLevel = (Math.random() * 3 + 1).toFixed(1);
      const maxLevel = Math.floor(Math.random() * 4) + 1;
      const skillCount = Math.floor(Math.random() * 10) + 1;
      
      rows.push([
        `emp_${i.toString().padStart(3, '0')}`,
        `社員${i}`,
        i <= 25 ? '開発部' : '営業部',
        i <= 10 ? 'シニア' : i <= 30 ? 'ミドル' : 'ジュニア',
        categoryName,
        parseFloat(avgLevel),
        maxLevel,
        skillCount,
        new Date().toISOString().split('T')[0] || ''
      ]);
    }
  }

  return { headers, rows };
}

// 詳細データ生成
function generateDetailedData(skillCategoryIds: string[], organizationIds: string[], filters?: any) {
  const headers = [
    '社員ID',
    '社員名',
    '部署',
    'ポジション',
    'スキルID',
    'スキル名',
    'スキルカテゴリ',
    'スキルレベル',
    '習得日',
    '最終更新日',
    '認定状況',
    '備考'
  ];

  const rows: (string | number)[][] = [];
  const skillsMap: Record<string, string[]> = {
    technical: ['JavaScript', 'TypeScript', 'React', 'Node.js', 'PostgreSQL', 'Docker', 'AWS', 'Git'],
    business: ['コミュニケーション', 'プレゼンテーション', 'プロジェクト管理', 'チームリーダーシップ', '営業', '企画'],
    domain: ['金融業界知識', 'システム設計', 'セキュリティ', 'クラウド技術', 'AI/ML', 'データ分析'],
    certification: ['AWS認定', 'PMP', '情報処理技術者', 'TOEIC', 'Java認定', 'Microsoft認定']
  };

  // モックデータ生成
  for (let empId = 1; empId <= 30; empId++) {
    for (const categoryId of skillCategoryIds) {
      const categorySkills = skillsMap[categoryId] || ['汎用スキル'];
      const categoryName = getCategoryName(categoryId);
      
      // 各社員がカテゴリ内の一部スキルを持つ
      const skillCount = Math.floor(Math.random() * categorySkills.length) + 1;
      const selectedSkills = categorySkills.slice(0, skillCount);
      
      selectedSkills.forEach((skillName, skillIndex) => {
        const level = Math.floor(Math.random() * 4) + 1;
        const acquiredDate = new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000);
        const updatedDate = new Date(acquiredDate.getTime() + Math.random() * 30 * 24 * 60 * 60 * 1000);
        
        rows.push([
          `emp_${empId.toString().padStart(3, '0')}`,
          `社員${empId}`,
          empId <= 15 ? '開発部' : '営業部',
          empId <= 5 ? 'シニア' : empId <= 20 ? 'ミドル' : 'ジュニア',
          `skill_${categoryId}_${skillIndex + 1}`,
          skillName,
          categoryName,
          level,
          acquiredDate.toISOString().split('T')[0] || '',
          updatedDate.toISOString().split('T')[0] || '',
          level >= 3 ? '認定済み' : '未認定',
          level === 4 ? 'エキスパート' : level === 3 ? '上級' : level === 2 ? '中級' : '初級'
        ]);
      });
    }
  }

  return { headers, rows };
}

// 統計データ生成
function generateStatisticsData(skillCategoryIds: string[], organizationIds: string[], filters?: any) {
  const headers = [
    'スキルカテゴリ',
    'スキル名',
    '保有者数',
    '平均レベル',
    'レベル1人数',
    'レベル2人数',
    'レベル3人数',
    'レベル4人数',
    '習得率(%)',
    '組織内順位'
  ];

  const rows: (string | number)[][] = [];
  const skillsMap: Record<string, string[]> = {
    technical: ['JavaScript', 'TypeScript', 'React', 'Node.js', 'PostgreSQL'],
    business: ['コミュニケーション', 'プレゼンテーション', 'プロジェクト管理', 'チームリーダーシップ'],
    domain: ['金融業界知識', 'システム設計', 'セキュリティ', 'クラウド技術'],
    certification: ['AWS認定', 'PMP', '情報処理技術者', 'TOEIC']
  };

  let rank = 1;
  for (const categoryId of skillCategoryIds) {
    const categorySkills = skillsMap[categoryId] || ['汎用スキル'];
    const categoryName = getCategoryName(categoryId);
    
    categorySkills.forEach(skillName => {
      const level1 = Math.floor(Math.random() * 8) + 2;
      const level2 = Math.floor(Math.random() * 12) + 5;
      const level3 = Math.floor(Math.random() * 8) + 3;
      const level4 = Math.floor(Math.random() * 4) + 1;
      const total = level1 + level2 + level3 + level4;
      const avgLevel = ((level1 * 1 + level2 * 2 + level3 * 3 + level4 * 4) / total).toFixed(1);
      const acquisitionRate = ((total / 50) * 100).toFixed(1);
      
      rows.push([
        categoryName,
        skillName,
        total,
        parseFloat(avgLevel),
        level1,
        level2,
        level3,
        level4,
        parseFloat(acquisitionRate),
        rank
      ]);
      rank++;
    });
  }

  return { headers, rows };
}

// ファイル生成
async function createExportFile(exportData: any, request: ExportRequest) {
  const { format, exportType } = request;
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('T')[0];
  const fileName = `skillmap_${exportType}_${timestamp}.${format}`;
  
  let fileContent: string;
  let mimeType: string;

  switch (format) {
    case 'csv':
      fileContent = generateCSV(exportData);
      mimeType = 'text/csv';
      break;
    case 'json':
      fileContent = JSON.stringify({
        exportType,
        timestamp: new Date().toISOString(),
        data: exportData
      }, null, 2);
      mimeType = 'application/json';
      break;
    default:
      throw new Error(`未対応のフォーマット: ${format}`);
  }

  // TODO: 実際のファイル保存処理
  // const filePath = await saveToStorage(fileName, fileContent, mimeType);
  
  // モック用のダウンロードURL生成
  const downloadUrl = `/api/files/download/${fileName}`;
  const fileSize = Buffer.byteLength(fileContent, 'utf8');
  const expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(); // 24時間後

  return {
    downloadUrl,
    fileName,
    fileSize,
    recordCount: exportData.rows.length,
    expiresAt
  };
}

// CSV生成
function generateCSV(exportData: any): string {
  const { headers, rows } = exportData;
  
  const csvHeaders = headers.join(',');
  const csvRows = rows.map((row: any[]) => 
    row.map(cell => {
      // セル内容をCSV形式でエスケープ
      const cellStr = String(cell);
      if (cellStr.includes(',') || cellStr.includes('"') || cellStr.includes('\n')) {
        return `"${cellStr.replace(/"/g, '""')}"`;
      }
      return cellStr;
    }).join(',')
  );

  return [csvHeaders, ...csvRows].join('\n');
}

// カテゴリ名取得
function getCategoryName(categoryId: string): string {
  const categoryMap: Record<string, string> = {
    technical: '技術スキル',
    business: 'ビジネススキル',
    domain: 'ドメイン知識',
    certification: '資格・認定'
  };
  
  return categoryMap[categoryId] || categoryId;
}
