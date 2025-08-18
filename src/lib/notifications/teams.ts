/**
 * Microsoft Teams通知サービス
 * 要求仕様ID: NTF.1-TEAMS.1
 */

import axios from 'axios';
import { prisma } from '@/lib/prisma';

interface TeamsMessage {
  title: string;
  text: string;
  color?: string;
  sections?: Array<{
    activityTitle?: string;
    activitySubtitle?: string;
    activityImage?: string;
    facts?: Array<{
      name: string;
      value: string;
    }>;
    text?: string;
    markdown?: boolean;
  }>;
  potentialAction?: Array<{
    '@type': string;
    name: string;
    target?: string[];
    inputs?: Array<{
      '@type': string;
      id: string;
      title: string;
      isMultiline?: boolean;
    }>;
    actions?: Array<{
      '@type': string;
      name: string;
      target: string;
    }>;
  }>;
}

interface TeamsResult {
  success: boolean;
  error?: string;
}

class TeamsService {
  /**
   * Teams Webhookにメッセージを送信
   */
  async sendWebhookMessage(
    webhookUrl: string,
    message: TeamsMessage
  ): Promise<TeamsResult> {
    try {
      // 開発環境でWebhook URLが設定されていない場合はスキップ
      if (process.env.NODE_ENV === 'development' && !webhookUrl) {
        console.log('💬 [開発環境] Teams通知をシミュレート:');
        console.log('  Title:', message.title);
        console.log('  Text:', message.text);
        return { success: true };
      }

      // メッセージカードの構築
      const card = {
        '@type': 'MessageCard',
        '@context': 'https://schema.org/extensions',
        themeColor: message.color || '0076D7',
        summary: message.title,
        title: message.title,
        text: message.text,
        sections: message.sections,
        potentialAction: message.potentialAction,
      };

      // Webhookに送信
      const response = await axios.post(webhookUrl, card, {
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 10000,
      });

      if (response.status === 200) {
        console.log('✅ Teams通知送信成功');
        return { success: true };
      } else {
        console.error('❌ Teams通知送信失敗:', response.status, response.data);
        return {
          success: false,
          error: `HTTPステータス: ${response.status}`,
        };
      }
    } catch (error) {
      console.error('❌ Teams通知エラー:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : '不明なエラー',
      };
    }
  }

  /**
   * テンプレートベースのTeams通知
   */
  async sendTemplateNotification(
    templateId: string,
    variables: Record<string, any>,
    tenantId: string
  ): Promise<TeamsResult> {
    try {
      // テナント設定からWebhook URLを取得
      const tenantSettings = await prisma.tenantSettings.findFirst({
        where: {
          tenant_id: tenantId,
          setting_category: 'NOTIFICATION',
          setting_key: 'TEAMS_WEBHOOK_URL',
          is_deleted: false,
        },
      });

      if (!tenantSettings || !tenantSettings.setting_value) {
        console.log('Teams Webhook URLが設定されていません');
        return { success: false, error: 'Webhook URLが未設定' };
      }

      const webhookUrl = tenantSettings.setting_value;

      // テンプレートを取得
      const template = await prisma.notificationTemplate.findFirst({
        where: {
          template_key: templateId,
          tenant_id: tenantId,
          is_deleted: false,
        },
      });

      if (!template) {
        throw new Error(`Teamsテンプレートが見つかりません: ${templateId}`);
      }

      // 変数を置換
      let title = (template as any).subject || template.template_name || '';
      let body = template.body_template || '';

      Object.entries(variables).forEach(([key, value]) => {
        const placeholder = `{{${key}}}`;
        title = title.replace(new RegExp(placeholder, 'g'), String(value));
        body = body.replace(new RegExp(placeholder, 'g'), String(value));
      });

      // メッセージを構築
      const message: TeamsMessage = {
        title,
        text: body,
        color: (template as any).priority === 'HIGH' ? 'FF0000' : 
               (template as any).priority === 'MEDIUM' ? 'FFA500' : '0076D7',
      };

      // 送信
      const result = await this.sendWebhookMessage(webhookUrl, message);

      // ログを記録
      await prisma.notificationLog.create({
        data: {
          id: `notif_log_${Date.now()}`,
          tenant_id: tenantId,
          template_id: templateId,
          notification_type: 'TEAMS',
          recipient_type: 'CHANNEL',
          recipient_address: 'Teams Channel',
          subject: title,
          message_body: body,
          message_format: 'TEXT',
          send_status: result.success ? 'SENT' : 'FAILED',
          send_attempts: 1,
          sent_at: result.success ? new Date() : null,
          response_code: result.success ? '200' : '500',
          response_message: result.error || null,
          error_details: result.error || null,
          created_at: new Date(),
          updated_at: new Date(),
        },
      });

      return result;
    } catch (error) {
      console.error('テンプレートTeams通知エラー:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : '不明なエラー',
      };
    }
  }

  /**
   * スキル更新通知
   */
  async notifySkillUpdate(
    employeeName: string,
    skillName: string,
    oldLevel: string,
    newLevel: string,
    tenantId: string
  ): Promise<TeamsResult> {
    const message: TeamsMessage = {
      title: 'スキル更新通知',
      text: `${employeeName}さんのスキルが更新されました`,
      color: '00FF00',
      sections: [{
        activityTitle: employeeName,
        activitySubtitle: new Date().toLocaleString('ja-JP'),
        facts: [
          { name: 'スキル', value: skillName },
          { name: '変更前', value: oldLevel },
          { name: '変更後', value: newLevel },
        ],
      }],
    };

    // Webhook URLを取得
    const settings = await prisma.tenantSettings.findFirst({
      where: {
        tenant_id: tenantId,
        setting_category: 'NOTIFICATION',
        setting_key: 'TEAMS_WEBHOOK_URL',
      },
    });

    if (settings?.setting_value) {
      return await this.sendWebhookMessage(settings.setting_value, message);
    }

    return { success: false, error: 'Webhook URL未設定' };
  }

  /**
   * 研修完了通知
   */
  async notifyTrainingCompletion(
    employeeName: string,
    trainingName: string,
    completionDate: Date,
    score: number | null,
    tenantId: string
  ): Promise<TeamsResult> {
    const message: TeamsMessage = {
      title: '研修完了通知',
      text: `${employeeName}さんが研修を完了しました`,
      color: '0076D7',
      sections: [{
        activityTitle: trainingName,
        activitySubtitle: completionDate.toLocaleDateString('ja-JP'),
        facts: [
          { name: '受講者', value: employeeName },
          { name: '完了日', value: completionDate.toLocaleDateString('ja-JP') },
          ...(score !== null ? [{ name: 'スコア', value: `${score}点` }] : []),
        ],
      }],
      potentialAction: [{
        '@type': 'OpenUri',
        name: '詳細を確認',
        target: [`${process.env.NEXTAUTH_URL}/trainings`],
      }],
    };

    const settings = await prisma.tenantSettings.findFirst({
      where: {
        tenant_id: tenantId,
        setting_category: 'NOTIFICATION',
        setting_key: 'TEAMS_WEBHOOK_URL',
      },
    });

    if (settings?.setting_value) {
      return await this.sendWebhookMessage(settings.setting_value, message);
    }

    return { success: false, error: 'Webhook URL未設定' };
  }

  /**
   * 目標達成通知
   */
  async notifyGoalAchievement(
    employeeName: string,
    goalName: string,
    achievementDate: Date,
    tenantId: string
  ): Promise<TeamsResult> {
    const message: TeamsMessage = {
      title: '🎉 目標達成通知',
      text: `${employeeName}さんが目標を達成しました！`,
      color: 'FFD700',
      sections: [{
        activityTitle: goalName,
        activitySubtitle: '目標達成',
        facts: [
          { name: '達成者', value: employeeName },
          { name: '達成日', value: achievementDate.toLocaleDateString('ja-JP') },
        ],
        text: 'おめでとうございます！素晴らしい成果です。',
      }],
    };

    const settings = await prisma.tenantSettings.findFirst({
      where: {
        tenant_id: tenantId,
        setting_category: 'NOTIFICATION',
        setting_key: 'TEAMS_WEBHOOK_URL',
      },
    });

    if (settings?.setting_value) {
      return await this.sendWebhookMessage(settings.setting_value, message);
    }

    return { success: false, error: 'Webhook URL未設定' };
  }
}

// シングルトンインスタンスをエクスポート
export const teamsService = new TeamsService();

/**
 * 汎用Teams通知関数
 */
export async function sendTeamsNotification(
  notificationType: string,
  data: Record<string, any>,
  tenantId: string
): Promise<TeamsResult> {
  try {
    // 通知設定を確認
    const settings = await prisma.notificationSettings.findFirst({
      where: {
        tenant_id: tenantId,
        notification_type: notificationType,
        is_enabled: true,
        is_deleted: false,
      },
    });

    if (!settings) {
      console.log(`通知タイプ ${notificationType} のTeams送信は無効です`);
      return { success: false, error: '通知が無効化されています' };
    }

    // テンプレートIDを取得
    const templateId = settings.template_id || `default_${notificationType.toLowerCase()}`;

    // Teams通知送信
    return await teamsService.sendTemplateNotification(
      templateId,
      data,
      tenantId
    );
  } catch (error) {
    console.error('Teams通知エラー:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : '不明なエラー',
    };
  }
}