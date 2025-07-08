// WPM.1-BULK.1: 作業実績一括登録API
import { NextRequest, NextResponse } from 'next/server';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

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

interface BulkUploadRequest {
  employee_id: string;
  records: BulkWorkRecord[];
}

export async function POST(request: NextRequest) {
  try {
    const body: BulkUploadRequest = await request.json();
    
    // 入力値検証
    if (!body.employee_id || !body.records || !Array.isArray(body.records)) {
      return NextResponse.json({
        success: false,
        error: '必須項目が不足しています'
      }, { status: 400 });
    }

    if (body.records.length === 0) {
      return NextResponse.json({
        success: false,
        error: '登録するレコードがありません'
      }, { status: 400 });
    }

    if (body.records.length > 100) {
      return NextResponse.json({
        success: false,
        error: '一度に登録できるレコード数は100件までです'
      }, { status: 400 });
    }

    // バリデーション結果
    const validationErrors: Array<{ row: number; field: string; message: string }> = [];

    body.records.forEach((record, index) => {
      const row = index + 1;
      
      // 必須項目チェック
      if (!record.project_name?.trim()) {
        validationErrors.push({ row, field: 'project_name', message: 'プロジェクト名は必須です' });
      }
      if (!record.project_code?.trim()) {
        validationErrors.push({ row, field: 'project_code', message: 'プロジェクトコードは必須です' });
      }
      if (!record.role_title?.trim()) {
        validationErrors.push({ row, field: 'role_title', message: '役割は必須です' });
      }
      if (!record.start_date) {
        validationErrors.push({ row, field: 'start_date', message: '開始日は必須です' });
      }
      if (!record.project_status?.trim()) {
        validationErrors.push({ row, field: 'project_status', message: 'プロジェクトステータスは必須です' });
      }

      // 日付形式チェック
      if (record.start_date && !isValidDate(record.start_date)) {
        validationErrors.push({ row, field: 'start_date', message: '開始日の形式が正しくありません (YYYY-MM-DD)' });
      }
      if (record.end_date && !isValidDate(record.end_date)) {
        validationErrors.push({ row, field: 'end_date', message: '終了日の形式が正しくありません (YYYY-MM-DD)' });
      }

      // 数値範囲チェック
      if (record.participation_rate !== undefined && (record.participation_rate < 0 || record.participation_rate > 100)) {
        validationErrors.push({ row, field: 'participation_rate', message: '参加率は0-100の範囲で入力してください' });
      }
      if (record.team_size !== undefined && record.team_size < 1) {
        validationErrors.push({ row, field: 'team_size', message: 'チーム規模は1以上で入力してください' });
      }
      if (record.evaluation_score !== undefined && (record.evaluation_score < 1 || record.evaluation_score > 5)) {
        validationErrors.push({ row, field: 'evaluation_score', message: '評価スコアは1-5の範囲で入力してください' });
      }

      // ステータス値チェック
      const validStatuses = ['planning', 'active', 'completed', 'on_hold', 'cancelled'];
      if (record.project_status && !validStatuses.includes(record.project_status)) {
        validationErrors.push({ 
          row, 
          field: 'project_status', 
          message: `プロジェクトステータスは次のいずれかを指定してください: ${validStatuses.join(', ')}` 
        });
      }
    });

    // バリデーションエラーがある場合は返す
    if (validationErrors.length > 0) {
      return NextResponse.json({
        success: false,
        error: 'バリデーションエラーがあります',
        validation_errors: validationErrors
      }, { status: 400 });
    }

    // トランザクションで一括登録
    const results = await prisma.$transaction(async (tx) => {
      const createdRecords = [];
      const errors = [];

      for (let i = 0; i < body.records.length; i++) {
        const record = body.records[i];
        const row = i + 1;

        // recordの存在チェック
        if (!record) {
          errors.push({
            row,
            field: 'general',
            message: 'レコードデータが不正です'
          });
          continue;
        }

        try {
          // プロジェクトコードの重複チェック
          const existingRecord = await tx.projectRecord.findFirst({
            where: {
              employee_id: body.employee_id,
              project_code: record.project_code,
              is_deleted: false
            }
          });

          if (existingRecord) {
            errors.push({
              row,
              field: 'project_code',
              message: `プロジェクトコード "${record.project_code}" は既に登録されています`
            });
            continue;
          }

          // レコード作成
          const projectRecord = await tx.projectRecord.create({
            data: {
              id: `proj_${Date.now()}_${i}`,
              employee_id: body.employee_id,
              project_name: record.project_name,
              project_code: record.project_code,
              client_name: record.client_name || null,
              project_type: record.project_type || null,
              project_scale: record.project_scale || null,
              start_date: new Date(record.start_date),
              end_date: record.end_date ? new Date(record.end_date) : null,
              participation_rate: record.participation_rate ? record.participation_rate / 100 : null,
              role_title: record.role_title,
              responsibilities: record.responsibilities || null,
              technologies_used: record.technologies_used || null,
              skills_applied: record.skills_applied || null,
              achievements: record.achievements || null,
              challenges_faced: record.challenges_faced || null,
              lessons_learned: record.lessons_learned || null,
              team_size: record.team_size || null,
              budget_range: record.budget_range || null,
              project_status: record.project_status,
              evaluation_score: record.evaluation_score || null,
              evaluation_comment: record.evaluation_comment || null,
              is_confidential: record.is_confidential || false,
              is_public_reference: record.is_public_reference || false,
              is_deleted: false,
              tenant_id: 'default', // シングルテナント対応
              created_at: new Date(),
              updated_at: new Date(),
              created_by: body.employee_id,
              updated_by: body.employee_id
            }
          });

          createdRecords.push({
            row,
            id: projectRecord.id,
            project_name: projectRecord.project_name,
            project_code: projectRecord.project_code
          });

        } catch (error) {
          console.error(`Row ${row} processing error:`, error);
          errors.push({
            row,
            field: 'general',
            message: `データベースエラーが発生しました: ${error instanceof Error ? error.message : '不明なエラー'}`
          });
        }
      }

      return { createdRecords, errors };
    });

    // 結果の集計
    const summary = {
      total_records: body.records.length,
      success_count: results.createdRecords.length,
      error_count: results.errors.length,
      success_rate: Math.round((results.createdRecords.length / body.records.length) * 100)
    };

    // レスポンス
    if (results.errors.length === 0) {
      // 全件成功
      return NextResponse.json({
        success: true,
        message: `${results.createdRecords.length}件の作業実績を正常に登録しました`,
        summary,
        created_records: results.createdRecords
      }, { status: 201 });
    } else if (results.createdRecords.length > 0) {
      // 部分成功
      return NextResponse.json({
        success: true,
        message: `${results.createdRecords.length}件の作業実績を登録しました（${results.errors.length}件のエラーがありました）`,
        summary,
        created_records: results.createdRecords,
        errors: results.errors
      }, { status: 207 }); // Multi-Status
    } else {
      // 全件失敗
      return NextResponse.json({
        success: false,
        message: '作業実績の登録に失敗しました',
        summary,
        errors: results.errors
      }, { status: 400 });
    }

  } catch (error) {
    console.error('Bulk upload error:', error);
    return NextResponse.json({
      success: false,
      error: 'サーバーエラーが発生しました',
      details: error instanceof Error ? error.message : '不明なエラー'
    }, { status: 500 });
  } finally {
    await prisma.$disconnect();
  }
}

// 日付形式チェック関数
function isValidDate(dateString: string): boolean {
  const regex = /^\d{4}-\d{2}-\d{2}$/;
  if (!regex.test(dateString)) return false;
  
  const date = new Date(dateString);
  return date instanceof Date && !isNaN(date.getTime());
}

// CSVテンプレートダウンロード用エンドポイント
export async function GET() {
  try {
    const csvTemplate = `project_name,project_code,client_name,project_type,project_scale,start_date,end_date,participation_rate,role_title,responsibilities,technologies_used,skills_applied,achievements,challenges_faced,lessons_learned,team_size,budget_range,project_status,evaluation_score,evaluation_comment,is_confidential,is_public_reference
年間スキル報告書WEB化プロジェクト,SKILL-WEB-2025,社内,新規開発,中規模,2025-05-01,2025-12-31,100,プロジェクトリーダー,プロジェクト全体の進行管理・技術的な意思決定,Next.js・TypeScript・React・Tailwind CSS・PostgreSQL,プロジェクト管理・フロントエンド開発・データベース設計,プロジェクト計画の策定と承認取得・技術スタックの選定と環境構築,スケジュール調整の難しさ・新技術習得の時間確保,チーム連携の重要性・段階的な実装アプローチの有効性,6,500万円-1000万円,active,4,順調に進行中,false,true
顧客管理システム改修,CRM-UPG-2024,ABC商事,改修,中規模,2024-10-01,2025-03-31,80,フロントエンドエンジニア,UI/UX改善・パフォーマンス最適化,React・Redux・Material-UI・Node.js・MySQL,フロントエンド開発・UI/UXデザイン,ページ読み込み速度50%改善・ユーザビリティテスト満足度90%達成,既存コードの複雑さ・レガシーブラウザ対応,ユーザー中心設計の重要性・段階的リファクタリングの効果,4,300万円-500万円,completed,5,期待を上回る成果,false,true`;

    return new NextResponse(csvTemplate, {
      status: 200,
      headers: {
        'Content-Type': 'text/csv; charset=utf-8',
        'Content-Disposition': 'attachment; filename="work_records_template.csv"'
      }
    });

  } catch (error) {
    console.error('Template download error:', error);
    return NextResponse.json({
      success: false,
      error: 'テンプレートファイルの生成に失敗しました'
    }, { status: 500 });
  }
}
