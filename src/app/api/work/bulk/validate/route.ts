/**
 * 要求仕様ID: WRK.2-BULK.1
 * 設計書: docs/design/screens/specs/画面定義書_SCR_WPM_Bulk_一括登録画面.md
 * API-101: 一括登録検証API
 * 実装内容: ファイル内容の検証のみ実施、DB登録は行わない
 */
import { NextRequest, NextResponse } from 'next/server';
import * as XLSX from 'xlsx';

interface BulkWorkRecord {
  project_name: string;
  project_code: string;
  client_name?: string;
  project_type?: string;
  project_scale?: string;
  start_date: string;
  end_date?: string;
  participation_rate?: number;
  role_title: string;
  responsibilities?: string;
  technologies_used?: string;
  skills_applied?: string;
  achievements?: string;
  challenges_faced?: string;
  lessons_learned?: string;
  team_size?: number;
  budget_range?: string;
  project_status: string;
  evaluation_score?: number;
  evaluation_comment?: string;
  is_confidential?: boolean;
  is_public_reference?: boolean;
}

interface ValidationResult {
  row: number;
  status: 'OK' | 'ERROR' | 'WARNING';
  errors: Array<{ field: string; message: string }>;
  data: BulkWorkRecord;
}

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json({
        success: false,
        error: 'ファイルを選択してください'
      }, { status: 400 });
    }

    // ファイル形式チェック
    const allowedTypes = [
      'text/csv',
      'application/vnd.ms-excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ];
    
    if (!allowedTypes.includes(file.type)) {
      return NextResponse.json({
        success: false,
        error: '対応していないファイル形式です。CSV または Excel ファイルを選択してください。'
      }, { status: 400 });
    }

    // ファイルサイズチェック (10MB制限)
    if (file.size > 10 * 1024 * 1024) {
      return NextResponse.json({
        success: false,
        error: 'ファイルサイズが10MBを超えています'
      }, { status: 400 });
    }

    // ファイル読み込み
    const buffer = await file.arrayBuffer();
    let records: BulkWorkRecord[] = [];

    try {
      if (file.type === 'text/csv') {
        // CSV読み込み
        const text = new TextDecoder('utf-8').decode(buffer);
        records = parseCSV(text);
      } else {
        // Excel読み込み
        const workbook = XLSX.read(buffer, { type: 'buffer' });
        if (workbook.SheetNames.length === 0) {
          throw new Error('Excelファイルにシートが見つかりません');
        }
        const sheetName = workbook.SheetNames[0];
        if (!sheetName) {
          throw new Error('Excelシートが見つかりません');
        }
        const worksheet = workbook.Sheets[sheetName];
        if (!worksheet) {
          throw new Error('Excelシートの読み込みに失敗しました');
        }
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
        records = parseExcelData(jsonData);
      }
    } catch (parseError) {
      return NextResponse.json({
        success: false,
        error: 'ファイルの読み込みに失敗しました。ファイル形式を確認してください。'
      }, { status: 400 });
    }

    // レコード数チェック
    if (records.length === 0) {
      return NextResponse.json({
        success: false,
        error: '登録するデータがありません'
      }, { status: 400 });
    }

    if (records.length > 1000) {
      return NextResponse.json({
        success: false,
        error: '一度に登録できるレコード数は1,000件までです'
      }, { status: 400 });
    }

    // バリデーション実行
    const validationResults: ValidationResult[] = [];
    
    records.forEach((record, index) => {
      const row = index + 1;
      const errors: Array<{ field: string; message: string }> = [];

      // 必須項目チェック
      if (!record.project_name?.trim()) {
        errors.push({ field: 'project_name', message: 'プロジェクト名は必須です' });
      }
      if (!record.project_code?.trim()) {
        errors.push({ field: 'project_code', message: 'プロジェクトコードは必須です' });
      }
      if (!record.role_title?.trim()) {
        errors.push({ field: 'role_title', message: '役割は必須です' });
      }
      if (!record.start_date) {
        errors.push({ field: 'start_date', message: '開始日は必須です' });
      }
      if (!record.project_status?.trim()) {
        errors.push({ field: 'project_status', message: 'プロジェクトステータスは必須です' });
      }

      // 日付形式チェック
      if (record.start_date && !isValidDate(record.start_date)) {
        errors.push({ field: 'start_date', message: '開始日の形式が正しくありません (YYYY-MM-DD)' });
      }
      if (record.end_date && !isValidDate(record.end_date)) {
        errors.push({ field: 'end_date', message: '終了日の形式が正しくありません (YYYY-MM-DD)' });
      }

      // 数値範囲チェック
      if (record.participation_rate !== undefined && (record.participation_rate < 0 || record.participation_rate > 100)) {
        errors.push({ field: 'participation_rate', message: '参加率は0-100の範囲で入力してください' });
      }
      if (record.team_size !== undefined && record.team_size < 1) {
        errors.push({ field: 'team_size', message: 'チーム規模は1以上で入力してください' });
      }
      if (record.evaluation_score !== undefined && (record.evaluation_score < 1 || record.evaluation_score > 5)) {
        errors.push({ field: 'evaluation_score', message: '評価スコアは1-5の範囲で入力してください' });
      }

      // ステータス値チェック
      const validStatuses = ['planning', 'active', 'completed', 'on_hold', 'cancelled'];
      if (record.project_status && !validStatuses.includes(record.project_status)) {
        errors.push({ 
          field: 'project_status', 
          message: `プロジェクトステータスは次のいずれかを指定してください: ${validStatuses.join(', ')}` 
        });
      }

      // 文字数制限チェック
      if (record.project_name && record.project_name.length > 200) {
        errors.push({ field: 'project_name', message: 'プロジェクト名は200文字以内で入力してください' });
      }
      if (record.project_code && record.project_code.length > 50) {
        errors.push({ field: 'project_code', message: 'プロジェクトコードは50文字以内で入力してください' });
      }

      // 結果追加
      validationResults.push({
        row,
        status: errors.length === 0 ? 'OK' : 'ERROR',
        errors,
        data: record
      });
    });

    // 統計情報
    const totalCount = validationResults.length;
    const errorCount = validationResults.filter(r => r.status === 'ERROR').length;
    const successCount = totalCount - errorCount;

    // 検証IDを生成（実行時に使用）
    const validationId = `validation_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

    // 検証結果をセッションストレージ用に返す（実際の実装では Redis等を使用）
    const response = {
      success: true,
      validation_id: validationId,
      summary: {
        total_count: totalCount,
        success_count: successCount,
        error_count: errorCount,
        success_rate: Math.round((successCount / totalCount) * 100)
      },
      validation_result: validationResults,
      message: errorCount === 0 
        ? `${totalCount}件のデータを検証しました。すべて正常です。`
        : `${totalCount}件のデータを検証しました。${errorCount}件のエラーがあります。`
    };

    return NextResponse.json(response, { status: 200 });

  } catch (error) {
    console.error('Validation error:', error);
    return NextResponse.json({
      success: false,
      error: 'システム障害が発生しました。再度お試しください',
      details: error instanceof Error ? error.message : '不明なエラー'
    }, { status: 500 });
  }
}

// CSV解析関数
function parseCSV(text: string): BulkWorkRecord[] {
  const lines = text.split('\n').filter(line => line.trim());
  if (lines.length < 2) return [];

  const headers = (lines[0] ?? '').split(',').map(h => h.trim().replace(/"/g, ''));
  const records: BulkWorkRecord[] = [];

  for (let i = 1; i < lines.length; i++) {
    const values = (lines[i] ?? '').split(',').map(v => v.trim().replace(/"/g, ''));
    const record: any = {};

    headers.forEach((header, index) => {
      if (header && typeof header === 'string' && index < values.length) {
        const value = values[index] || '';
        record[header] = value;
      }
    });

    // 数値変換
    if (record.participation_rate && typeof record.participation_rate === 'string') {
      record.participation_rate = parseFloat(record.participation_rate);
    }
    if (record.team_size && typeof record.team_size === 'string') {
      record.team_size = parseInt(record.team_size);
    }
    if (record.evaluation_score && typeof record.evaluation_score === 'string') {
      record.evaluation_score = parseFloat(record.evaluation_score);
    }
    // Boolean変換（型安全性を確保）
    if (record && typeof record === 'object' && record !== null) {
      const typedRecord = record as Record<string, any>;
      try {
        if ('is_confidential' in typedRecord) {
          const isConfidentialValue = typedRecord['is_confidential'];
          if (isConfidentialValue !== undefined && typeof isConfidentialValue === 'string') {
            typedRecord['is_confidential'] = isConfidentialValue.toLowerCase() === 'true';
          }
        }
        
        if ('is_public_reference' in typedRecord) {
          const isPublicReferenceValue = typedRecord['is_public_reference'];
          if (isPublicReferenceValue !== undefined && typeof isPublicReferenceValue === 'string') {
            typedRecord['is_public_reference'] = isPublicReferenceValue.toLowerCase() === 'true';
          }
        }
      } catch (e) {
        // 型変換エラーを無視
      }
    }

    records.push(record as BulkWorkRecord);
  }

  return records;
}

// Excel解析関数
function parseExcelData(jsonData: any[]): BulkWorkRecord[] {
  if (jsonData.length < 2) return [];

  const headers = jsonData[0];
  if (!headers || !Array.isArray(headers)) return [];

  const records: BulkWorkRecord[] = [];

  for (let i = 1; i < jsonData.length; i++) {
    const row = jsonData[i];
    if (!row || !Array.isArray(row)) continue;

    const record: any = {};

    headers.forEach((header: string, index: number) => {
      if (header && typeof header === 'string' && index < row.length) {
        const value = row[index] || '';
        record[header] = value;
      }
    });

    // 数値変換
    if (record.participation_rate) record.participation_rate = parseFloat(record.participation_rate);
    if (record.team_size) record.team_size = parseInt(record.team_size);
    if (record.evaluation_score) record.evaluation_score = parseFloat(record.evaluation_score);
    if (record.is_confidential) record.is_confidential = record.is_confidential === true || record.is_confidential === 'true';
    if (record.is_public_reference) record.is_public_reference = record.is_public_reference === true || record.is_public_reference === 'true';

    records.push(record as BulkWorkRecord);
  }

  return records;
}

// 日付形式チェック関数
function isValidDate(dateString: string): boolean {
  const regex = /^\d{4}-\d{2}-\d{2}$/;
  if (!regex.test(dateString)) return false;
  
  const date = new Date(dateString);
  return date instanceof Date && !isNaN(date.getTime());
}
