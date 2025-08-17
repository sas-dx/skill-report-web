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

    // サンプルデータ（実際にインポート可能な値）
    const sampleData1 = [
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
      'completed',  // ステータス: planning, active, completed, on_hold, cancelled
      '4',
      '期待以上の成果を達成',
      'false',
      'true'
    ];

    const sampleData2 = [
      '在庫管理システム改修',
      'PROJ-2024-002',
      'テクノ商事株式会社',
      'システム改修',
      '小規模',
      '2024-07-01',
      '',  // 終了日は空でもOK
      '50',
      'バックエンドエンジニア',
      'API開発、データベース最適化',
      'Node.js, Express, PostgreSQL, Docker',
      'バックエンド開発、データベース設計',
      'クエリ最適化により処理速度3倍向上',
      'レガシーコードのリファクタリング',
      'マイクロサービス化の重要性',
      '3',
      '300万円未満',
      'active',  // 現在進行中
      '3',
      '順調に進行中',
      'false',
      'false'
    ];

    if (format === 'csv') {
      // CSV形式でテンプレート生成
      const csvContent = [
        japaneseHeaders.join(','),
        headers.join(','),
        sampleData1.join(','),
        sampleData2.join(',')
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
        sampleData1,      // 3行目: サンプルデータ1
        sampleData2       // 4行目: サンプルデータ2
      ];
      
      // ワークシートを作成
      const worksheet = XLSX.utils.aoa_to_sheet(worksheetData);
      
      // 列幅を設定（見やすくするため）
      const colWidths = japaneseHeaders.map(() => ({ wch: 20 }));
      worksheet['!cols'] = colWidths;
      
      // ワークシートをワークブックに追加
      XLSX.utils.book_append_sheet(workbook, worksheet, '作業実績テンプレート');
      
      // 説明シートを追加
      const instructionData = [
        ['作業実績一括登録テンプレート 使用方法'],
        [''],
        ['【入力ルール】'],
        ['1. 2行目の英語ヘッダーは削除しないでください（システムで使用します）'],
        ['2. 3行目以降にデータを入力してください（サンプルデータは削除して構いません）'],
        ['3. 必須項目：プロジェクト名、プロジェクトコード、役割、開始日、プロジェクトステータス'],
        [''],
        ['【プロジェクトステータスの値】'],
        ['planning: 計画中'],
        ['active: 進行中'],
        ['completed: 完了'],
        ['on_hold: 保留中'],
        ['cancelled: キャンセル'],
        [''],
        ['【日付形式】'],
        ['YYYY-MM-DD形式で入力（例：2024-01-15）'],
        [''],
        ['【数値項目】'],
        ['参画率: 0-100の数値（%記号は不要）'],
        ['チーム規模: 1以上の整数'],
        ['評価点数: 1-5の整数'],
        [''],
        ['【真偽値項目】'],
        ['機密情報フラグ、公開参照可能フラグ: true または false'],
        [''],
        ['【注意事項】'],
        ['・プロジェクトコードは重複できません'],
        ['・1度に登録できるのは100件までです'],
        ['・CSVで保存する場合はUTF-8エンコーディングを使用してください']
      ];
      
      const instructionSheet = XLSX.utils.aoa_to_sheet(instructionData);
      instructionSheet['!cols'] = [{ wch: 80 }];
      XLSX.utils.book_append_sheet(workbook, instructionSheet, '使用方法');
      
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
