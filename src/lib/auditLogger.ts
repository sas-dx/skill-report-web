/**
 * 要求仕様ID: PRO.1-BASE.1
 * 実装内容: AuditLogテーブルへの履歴記録用ユーティリティ
 */

import { prisma } from '@/lib/prisma';

export interface AuditLogData {
  userId: string;
  actionType: string;
  targetTable: string;
  targetId: string;
  oldValues?: Record<string, any>;
  newValues?: Record<string, any>;
  changeReason?: string;
  ipAddress?: string;
  userAgent?: string;
}

/**
 * 監査ログを記録する
 */
export async function createAuditLog(data: AuditLogData): Promise<void> {
  try {
    await prisma.auditLog.create({
      data: {
        id: `audit_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        user_id: data.userId,
        action_type: data.actionType,
        target_table: data.targetTable,
        target_id: data.targetId,
        old_values: data.oldValues ? JSON.stringify(data.oldValues) : null,
        new_values: data.newValues ? JSON.stringify(data.newValues) : null,
        ip_address: data.ipAddress || null,
        user_agent: data.userAgent || null,
        created_at: new Date(),
        updated_at: new Date()
      }
    });
  } catch (error) {
    console.error('Audit log creation failed:', error);
    // 監査ログの失敗はメイン処理を止めない
  }
}

/**
 * ユーザーの更新履歴を取得する
 */
export async function getUserUpdateHistory(userId: string, limit: number = 50): Promise<any[]> {
  try {
    const auditLogs = await prisma.auditLog.findMany({
      where: {
        target_table: 'Employee',
        target_id: userId
      },
      orderBy: {
        created_at: 'desc'
      },
      take: limit
    });

    // フロントエンドが期待する形式に変換
    const historyItems: any[] = [];
    
    auditLogs.forEach((log: any) => {
      let oldValues: Record<string, any> = {};
      let newValues: Record<string, any> = {};

      try {
        if (log.old_values) {
          oldValues = JSON.parse(log.old_values);
        }
        if (log.new_values) {
          newValues = JSON.parse(log.new_values);
        }
      } catch (parseError) {
        console.error('Failed to parse audit log values:', parseError);
      }

      // 変更されたフィールドを特定
      const changedFields = Object.keys(newValues).filter(key => 
        oldValues[key] !== newValues[key]
      );

      const createdAt = log.created_at || new Date();
      const dateStr = createdAt.toISOString().split('T')[0];
      const timeStr = createdAt.toTimeString().split(' ')[0];

      // 各変更フィールドを個別の履歴項目として追加
      changedFields.forEach(field => {
        historyItems.push({
          date: `${dateStr} ${timeStr}`,
          field: getFieldDisplayName(field),
          oldValue: formatFieldValue(field, oldValues[field]),
          newValue: formatFieldValue(field, newValues[field]),
          updatedBy: log.user_id || 'system'
        });
      });
    });

    return historyItems;
  } catch (error) {
    console.error('Failed to get user update history:', error);
    return [];
  }
}

/**
 * フィールド名を表示用に変換
 */
function getFieldDisplayName(fieldName: string): string {
  const fieldMap: Record<string, string> = {
    'full_name': '氏名',
    'full_name_kana': '氏名（カナ）',
    'email': 'メールアドレス',
    'phone': '電話番号',
    'department_id': '部署',
    'position_id': '役職',
    'employment_status': '雇用形態',
    'hire_date': '入社日',
    'manager_id': '上長'
  };

  return fieldMap[fieldName] || fieldName;
}

/**
 * フィールド値を表示用にフォーマット
 */
function formatFieldValue(fieldName: string, value: any): string {
  if (value === null || value === undefined) {
    return '－';
  }

  // 日付フィールドの場合
  if (fieldName.includes('date') || fieldName.includes('_at')) {
    try {
      const date = new Date(value);
      return date.toISOString().split('T')[0] || '－';
    } catch {
      return String(value);
    }
  }

  return String(value);
}

/**
 * オブジェクトの差分を取得
 */
export function getObjectDiff(oldObj: Record<string, any> = {}, newObj: Record<string, any> = {}): {
  oldValues: Record<string, any>;
  newValues: Record<string, any>;
} {
  const oldValues: Record<string, any> = {};
  const newValues: Record<string, any> = {};

  // 新しいオブジェクトのキーをチェック
  Object.keys(newObj).forEach(key => {
    if (oldObj[key] !== newObj[key]) {
      oldValues[key] = oldObj[key];
      newValues[key] = newObj[key];
    }
  });

  return { oldValues, newValues };
}
