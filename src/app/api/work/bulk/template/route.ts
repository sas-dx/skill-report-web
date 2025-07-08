// API-103: テンプレート取得API
// WRK.2-BULK.3: 作業実績一括登録テンプレート取得

import { NextRequest, NextResponse } from 'next/server';
import * as XLSX from 'xlsx';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const format = searchParams.get('format') || 'xlsx';

    if (!['csv', 'xlsx'].includes(format)) {
      return NextResponse.json(
        { 
          success: false, 
          error: 'Invalid format. Supported formats: csv, xlsx' 
        },
        { status: 400 }
      );
    }

    // テンプレートヘッダー定義
    const headers = [
      'project_name',
      'project_code', 
      'client_name',
      'project_type',
      'project_scale',
      'start_date',
      'end_date',
      'participation_rate',
      'role_title',
      'responsibilities',
      'technologies_used',
      'skills_applied',
      'achievements',
      'challenges_faced',
      'lessons_learned',
      'team_size',
      'budget_range',
      'project_status',
      'evaluation_score',
      'evaluation_comment',
      'is_confidential',
      'is_public_reference'
    ];

    // 日本語ヘッダー
    const japaneseHeaders = [
      'プロジェクト名',
      'プロジェクトコード',
      'クライアント名',
      'プロジェクト種別',
      'プロジェクト規模',
      '開始日',
      '終了日',
      '参画率(%)',
      '役割・職位',
      '担当業務',
      '使用技術',
      '適用スキル',
      '成果・実績',
      '課題・困難',
      '学習・気づき',
      'チーム規模',
      '予算規模',
      'プロジェクト状況',
      '評価点数',
      '評価コメント',
      '機密情報フラグ',
      '公開参照可能フラグ'
    ];

    // サンプルデータ
    const sampleData = [
      'ECサイト構築プロジェクト',
      'PROJ-2024-001',
      '株式会社サンプル',
      'Webアプリケーション開発',
      '中規模',
      '2024-01-15',
      '2024-06-30',
      '80',
      'フロントエンドエンジニア',
      'UI/UX設計、React開発、テスト実装',
      'React, TypeScript, Next.js, Tailwind CSS',
      'フロントエンド開発、UI/UX設計',
      'レスポンシブ対応完了、パフォーマンス20%向上',
      '複雑な状態管理、API連携の最適化',
      'React Hooks活用、TypeScript型安全性',
      '5',
      '1000万円以上',
      '完了',
      '4',
      '期待以上の成果を達成',
      'false',
      'true'
    ];

    if (format === 'csv') {
      // CSV形式でテンプレート生成
      const csvContent = [
        japaneseHeaders.join(','),
        headers.join(','),
        sampleData.join(',')
      ].join('\n');

      return new NextResponse(csvContent, {
        status: 200,
        headers: {
          'Content-Type': 'text/csv; charset=utf-8',
          'Content-Disposition': 'attachment; filename="work_records_template.csv"',
        },
      });
    } else {
      // Excel形式でテンプレート生成
      const workbook = XLSX.utils.book_new();
      
      // ワークシートデータを作成（配列の配列形式）
      const worksheetData = [
        japaneseHeaders,  // 1行目: 日本語ヘッダー
        headers,          // 2行目: 英語ヘッダー（システム用）
        sampleData        // 3行目: サンプルデータ
      ];
      
      // ワークシートを作成
      const worksheet = XLSX.utils.aoa_to_sheet(worksheetData);
      
      // 列幅を設定（見やすくするため）
      const colWidths = japaneseHeaders.map(() => ({ wch: 20 }));
      worksheet['!cols'] = colWidths;
      
      // ワークシートをワークブックに追加
      XLSX.utils.book_append_sheet(workbook, worksheet, '作業実績テンプレート');
      
      // Excelファイルをバッファとして生成
      const excelBuffer = XLSX.write(workbook, { 
        type: 'buffer', 
        bookType: 'xlsx' 
      });

      return new NextResponse(excelBuffer, {
        status: 200,
        headers: {
          'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
          'Content-Disposition': 'attachment; filename="work_records_template.xlsx"',
        },
      });
    }

  } catch (error) {
    console.error('Template generation error:', error);
    return NextResponse.json(
      { 
        success: false, 
        error: 'テンプレートファイルの生成に失敗しました' 
      },
      { status: 500 }
    );
  }
}
