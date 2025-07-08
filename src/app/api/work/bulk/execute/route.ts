// API-102: 一括登録実行API
// WRK.2-BULK.2: 作業実績一括登録実行

import { NextRequest, NextResponse } from 'next/server';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// バリデーションAPIと同じデータストレージを参照
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

// 外部からvalidationDataStoreにアクセスするための関数
// 実際の実装では共有ストレージ（Redis等）を使用
declare global {
  var validationDataStore: Map<string, {
    data: BulkWorkRecord[];
    timestamp: number;
    expiresAt: number;
  }> | undefined;
}

// グローバル変数として初期化（開発環境用）
if (!global.validationDataStore) {
  global.validationDataStore = new Map();
}

interface ExecutionResult {
  success: boolean;
  message: string;
  success_count: number;
  error_count: number;
  result_details?: Array<{
    row: number;
    status: 'success' | 'error';
    message: string;
    record_id?: string;
  }>;
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { validation_id } = body;

    if (!validation_id) {
      return NextResponse.json({
        success: false,
        message: 'バリデーションIDが必要です'
      }, { status: 400 });
    }

    // validation_idに基づいて検証済みデータを取得
    const validationData = global.validationDataStore?.get(validation_id);
    
    if (!validationData) {
      return NextResponse.json({
        success: false,
        message: 'バリデーションデータが見つかりません。再度ファイルをアップロードしてください。'
      }, { status: 404 });
    }

    // データの有効期限チェック
    if (Date.now() > validationData.expiresAt) {
      global.validationDataStore?.delete(validation_id);
      return NextResponse.json({
        success: false,
        message: 'バリデーションデータの有効期限が切れています。再度ファイルをアップロードしてください。'
      }, { status: 410 });
    }

    console.log(`Processing validation ID: ${validation_id}, Records: ${validationData.data.length}`);

    // 検証済みデータを処理用形式に変換
    const validatedData = validationData.data.map((record, index) => ({
      row: index + 1,
      data: record
    }));

    const results: Array<{
      row: number;
      status: 'success' | 'error';
      message: string;
      record_id?: string;
    }> = [];

    let successCount = 0;
    let errorCount = 0;

    // トランザクション処理
    await prisma.$transaction(async (tx) => {
      for (const item of validatedData) {
        try {
          // 作業実績レコード作成
          const workRecord = await tx.projectRecord.create({
            data: {
              id: `work_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
              employee_id: 'emp_001', // TODO: 実際のログインユーザーIDを使用
              project_name: item.data.project_name,
              project_code: item.data.project_code,
              client_name: item.data.client_name || null,
              project_type: item.data.project_type || null,
              project_scale: item.data.project_scale || null,
              start_date: new Date(item.data.start_date),
              end_date: item.data.end_date ? new Date(item.data.end_date) : null,
              participation_rate: item.data.participation_rate || null,
              role_title: item.data.role_title,
              responsibilities: item.data.responsibilities || null,
              technologies_used: item.data.technologies_used || null,
              skills_applied: item.data.skills_applied || null,
              achievements: item.data.achievements || null,
              challenges_faced: item.data.challenges_faced || null,
              lessons_learned: item.data.lessons_learned || null,
              team_size: item.data.team_size || null,
              budget_range: item.data.budget_range || null,
              project_status: item.data.project_status,
              evaluation_score: item.data.evaluation_score || null,
              evaluation_comment: item.data.evaluation_comment || null,
              is_confidential: item.data.is_confidential || false,
              is_public_reference: item.data.is_public_reference || false,
              is_deleted: false,
              tenant_id: 'tenant_001', // TODO: 実際のテナントIDを使用
              created_at: new Date(),
              updated_at: new Date(),
              created_by: 'emp_001', // TODO: 実際のログインユーザーIDを使用
              updated_by: 'emp_001'  // TODO: 実際のログインユーザーIDを使用
            }
          });

          results.push({
            row: item.row,
            status: 'success',
            message: `プロジェクト「${item.data.project_name}」を登録しました`,
            record_id: workRecord.id
          });

          successCount++;

        } catch (error) {
          console.error(`Row ${item.row} registration error:`, error);
          
          results.push({
            row: item.row,
            status: 'error',
            message: error instanceof Error ? error.message : '登録に失敗しました'
          });

          errorCount++;
        }
      }
    });

    // 監査ログ記録
    try {
      await prisma.auditLog.create({
        data: {
          id: `audit_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          user_id: 'emp_001', // TODO: 実際のログインユーザーIDを使用
          action_type: 'BULK_WORK_RECORD_CREATE',
          target_table: 'TRN_ProjectRecord',
          target_id: validation_id,
          old_values: null,
          new_values: JSON.stringify({
            validation_id,
            success_count: successCount,
            error_count: errorCount
          }),
          ip_address: request.headers.get('x-forwarded-for') || 'unknown',
          user_agent: request.headers.get('user-agent') || 'unknown',
          tenant_id: 'tenant_001', // TODO: 実際のテナントIDを使用
          created_at: new Date()
        }
      });
    } catch (auditError) {
      console.error('Audit log creation failed:', auditError);
      // 監査ログの失敗は処理を停止しない
    }

    const response: ExecutionResult = {
      success: errorCount === 0,
      message: errorCount === 0 
        ? `${successCount}件の作業実績を正常に登録しました`
        : `${successCount}件が成功、${errorCount}件が失敗しました`,
      success_count: successCount,
      error_count: errorCount,
      result_details: results
    };

    return NextResponse.json(response, { status: 200 });

  } catch (error) {
    console.error('Bulk execution error:', error);
    
    // エラー監査ログ
    try {
      await prisma.auditLog.create({
        data: {
          id: `audit_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          user_id: 'emp_001',
          action_type: 'BULK_WORK_RECORD_CREATE_ERROR',
          target_table: 'TRN_ProjectRecord',
          target_id: 'bulk_execution',
          old_values: null,
          new_values: JSON.stringify({
            error: error instanceof Error ? error.message : '不明なエラー'
          }),
          ip_address: request.headers.get('x-forwarded-for') || 'unknown',
          user_agent: request.headers.get('user-agent') || 'unknown',
          tenant_id: 'tenant_001', // TODO: 実際のテナントIDを使用
          created_at: new Date()
        }
      });
    } catch (auditError) {
      console.error('Error audit log creation failed:', auditError);
    }

    return NextResponse.json({
      success: false,
      message: 'システム障害が発生しました。管理者にお問い合わせください',
      success_count: 0,
      error_count: 0,
      details: error instanceof Error ? error.message : '不明なエラー'
    }, { status: 500 });
  } finally {
    await prisma.$disconnect();
  }
}
