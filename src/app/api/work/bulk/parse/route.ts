// WPM.1-BULK.2: CSVパース用API
import { NextRequest, NextResponse } from 'next/server';
import * as XLSX from 'xlsx';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;
    
    if (!file) {
      return NextResponse.json({
        success: false,
        error: 'ファイルが選択されていません'
      }, { status: 400 });
    }

    // ファイル形式チェック
    const fileName = file.name.toLowerCase();
    const isCSV = fileName.endsWith('.csv');
    const isExcel = fileName.endsWith('.xlsx') || fileName.endsWith('.xls');
    
    if (!isCSV && !isExcel) {
      return NextResponse.json({
        success: false,
        error: 'サポートされていないファイル形式です。CSV、XLSXファイルのみ対応しています。'
      }, { status: 400 });
    }

    // ファイルを読み込み
    const buffer = await file.arrayBuffer();
    const data = Buffer.from(buffer);
    
    // xlsxライブラリでパース
    const workbook = XLSX.read(data, { type: 'buffer' });
    const sheetName = workbook.SheetNames[0];
    if (!sheetName) {
      return NextResponse.json({
        success: false,
        error: 'ファイルにシートがありません。'
      }, { status: 400 });
    }
    const worksheet = workbook.Sheets[sheetName];
    if (!worksheet) {
      return NextResponse.json({
        success: false,
        error: 'ワークシートが見つかりません。'
      }, { status: 400 });
    }
    
    // JSONに変換（ヘッダー行を使用）
    const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 }) as any[][];
    
    if (jsonData.length < 3) {
      return NextResponse.json({
        success: false,
        error: 'ファイルにデータがありません。最低でもヘッダー行とデータ行が必要です。'
      }, { status: 400 });
    }

    // ヘッダー行の取得（2行目が英語ヘッダー）
    const headers = jsonData[1] as string[];
    
    // 期待されるヘッダーのチェック
    const expectedHeaders = [
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

    // ヘッダーの検証
    const missingHeaders = expectedHeaders.filter(h => !headers.includes(h));
    if (missingHeaders.length > 0) {
      return NextResponse.json({
        success: false,
        error: `必須のヘッダーが不足しています: ${missingHeaders.join(', ')}`,
        hint: 'テンプレートをダウンロードして正しい形式を確認してください。'
      }, { status: 400 });
    }

    // データ行を処理（3行目以降）
    const records = [];
    for (let i = 2; i < jsonData.length; i++) {
      const row = jsonData[i];
      
      // 空行をスキップ
      if (!row || row.length === 0 || row.every(cell => !cell)) {
        continue;
      }

      // 行データをオブジェクトに変換
      const record: any = {};
      headers.forEach((header, index) => {
        const value = row[index];
        
        // 値の型変換
        if (header === 'participation_rate' || header === 'team_size' || header === 'evaluation_score') {
          record[header] = value ? Number(value) : undefined;
        } else if (header === 'is_confidential' || header === 'is_public_reference') {
          record[header] = value === 'true' || value === true;
        } else if (header === 'start_date' || header === 'end_date') {
          // Excelの日付形式を処理
          if (value && typeof value === 'number') {
            // Excelのシリアル値を日付に変換
            const date = XLSX.SSF.parse_date_code(value);
            record[header] = `${date.y}-${String(date.m).padStart(2, '0')}-${String(date.d).padStart(2, '0')}`;
          } else {
            record[header] = value || '';
          }
        } else {
          record[header] = value ? String(value).trim() : '';
        }
      });

      // 必須フィールドが存在する行のみ追加
      if (record.project_name && record.project_code) {
        records.push(record);
      }
    }

    if (records.length === 0) {
      return NextResponse.json({
        success: false,
        error: 'インポート可能なデータが見つかりませんでした。',
        hint: 'プロジェクト名とプロジェクトコードは必須です。'
      }, { status: 400 });
    }

    // パース結果を返す
    return NextResponse.json({
      success: true,
      message: `${records.length}件のレコードをパースしました`,
      records: records,
      summary: {
        total_rows: jsonData.length - 2,
        valid_records: records.length,
        skipped_rows: jsonData.length - 2 - records.length
      }
    });

  } catch (error) {
    console.error('CSV parse error:', error);
    return NextResponse.json({
      success: false,
      error: 'ファイルの解析に失敗しました',
      details: error instanceof Error ? error.message : '不明なエラー'
    }, { status: 500 });
  }
}