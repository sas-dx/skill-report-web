/**
 * メール通知サービス
 * 要求仕様ID: NTF.1-EMAIL.1
 */

import nodemailer from 'nodemailer';
import { prisma } from '@/lib/prisma';

interface EmailOptions {
  to: string | string[];
  subject: string;
  text?: string;
  html?: string;
  from?: string;
  cc?: string | string[];
  bcc?: string | string[];
  attachments?: Array<{
    filename: string;
    content?: string | Buffer;
    path?: string;
  }>;
}

interface EmailResult {
  success: boolean;
  messageId?: string;
  error?: string;
}

class EmailService {
  private transporter: nodemailer.Transporter | null = null;
  private initialized = false;

  /**
   * メールサービスの初期化
   */
  private async initialize(): Promise<void> {
    if (this.initialized) return;

    try {
      // 環境変数から設定を取得
      const config = {
        host: process.env.SMTP_HOST || 'localhost',
        port: parseInt(process.env.SMTP_PORT || '1025'),
        secure: process.env.SMTP_PORT === '465',
        auth: process.env.SMTP_USER && process.env.SMTP_PASS ? {
          user: process.env.SMTP_USER,
          pass: process.env.SMTP_PASS,
        } : undefined,
      };

      // 開発環境では実際のメール送信をスキップ
      if (process.env.NODE_ENV === 'development' && !process.env.SMTP_HOST) {
        console.log('📧 メールサービス: 開発環境モード（メール送信をスキップ）');
        this.initialized = true;
        return;
      }

      this.transporter = nodemailer.createTransport(config);

      // 接続テスト
      await this.transporter.verify();
      console.log('✅ メールサービスが正常に初期化されました');
      this.initialized = true;
    } catch (error) {
      console.error('❌ メールサービスの初期化に失敗:', error);
      this.initialized = false;
      throw error;
    }
  }

  /**
   * メール送信
   */
  async sendEmail(options: EmailOptions): Promise<EmailResult> {
    try {
      await this.initialize();

      // 開発環境では実際の送信をスキップ
      if (process.env.NODE_ENV === 'development' && !this.transporter) {
        console.log('📧 [開発環境] メール送信をシミュレート:');
        console.log('  To:', options.to);
        console.log('  Subject:', options.subject);
        console.log('  Body:', options.text || options.html?.substring(0, 100));
        
        return {
          success: true,
          messageId: `dev-${Date.now()}@localhost`,
        };
      }

      if (!this.transporter) {
        throw new Error('メールトランスポーターが初期化されていません');
      }

      // メール送信
      const info = await this.transporter.sendMail({
        from: options.from || process.env.SMTP_FROM || 'noreply@skillreport.local',
        to: Array.isArray(options.to) ? options.to.join(', ') : options.to,
        cc: options.cc ? (Array.isArray(options.cc) ? options.cc.join(', ') : options.cc) : undefined,
        bcc: options.bcc ? (Array.isArray(options.bcc) ? options.bcc.join(', ') : options.bcc) : undefined,
        subject: options.subject,
        text: options.text,
        html: options.html,
        attachments: options.attachments,
      });

      console.log('✅ メール送信成功:', info.messageId);

      return {
        success: true,
        messageId: info.messageId,
      };
    } catch (error) {
      console.error('❌ メール送信エラー:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : '不明なエラー',
      };
    }
  }

  /**
   * テンプレートベースのメール送信
   */
  async sendTemplateEmail(
    templateId: string,
    to: string | string[],
    variables: Record<string, any>,
    tenantId: string
  ): Promise<EmailResult> {
    try {
      // テンプレートを取得
      const template = await prisma.notificationTemplate.findFirst({
        where: {
          template_type: 'EMAIL',
          is_active: true,
          is_deleted: false,
        } as any,
      });

      if (!template) {
        throw new Error(`メールテンプレートが見つかりません: ${templateId}`);
      }

      // 変数を置換
      let subject = (template as any).subject || '';
      let body = (template as any).body_template || '';

      Object.entries(variables).forEach(([key, value]) => {
        const placeholder = `{{${key}}}`;
        subject = subject.replace(new RegExp(placeholder, 'g'), String(value));
        body = body.replace(new RegExp(placeholder, 'g'), String(value));
      });

      // メール送信
      const result = await this.sendEmail({
        to,
        subject,
        html: body,
        text: body.replace(/<[^>]*>/g, ''), // HTMLタグを除去
      });

      // 送信ログを記録
      await prisma.notificationLog.create({
        data: {
          id: `notif_log_${Date.now()}`,
          tenant_id: tenantId,
          template_id: templateId,
          notification_type: 'EMAIL',
          recipient_type: 'USER',
          recipient_address: Array.isArray(to) ? to.join(', ') : to,
          subject,
          message_body: body,
          message_format: 'HTML',
          send_status: result.success ? 'SENT' : 'FAILED',
          send_attempts: 1,
          sent_at: result.success ? new Date() : null,
          response_code: result.success ? '200' : '500',
          response_message: result.messageId || result.error || null,
          error_details: result.error || null,
          created_at: new Date(),
          updated_at: new Date(),
        },
      });

      return result;
    } catch (error) {
      console.error('テンプレートメール送信エラー:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : '不明なエラー',
      };
    }
  }

  /**
   * バッチメール送信
   */
  async sendBatchEmails(
    recipients: Array<{ email: string; variables: Record<string, any> }>,
    templateId: string,
    tenantId: string
  ): Promise<Array<{ email: string; result: EmailResult }>> {
    const results: Array<{ email: string; result: EmailResult }> = [];

    for (const recipient of recipients) {
      const result = await this.sendTemplateEmail(
        templateId,
        recipient.email,
        recipient.variables,
        tenantId
      );

      results.push({
        email: recipient.email,
        result,
      });

      // レート制限（1秒に5通まで）
      await new Promise(resolve => setTimeout(resolve, 200));
    }

    return results;
  }
}

// シングルトンインスタンスをエクスポート
export const emailService = new EmailService();

/**
 * 通知イベントに基づくメール送信
 */
export async function sendNotificationEmail(
  notificationType: string,
  recipientEmail: string,
  data: Record<string, any>,
  tenantId: string
): Promise<EmailResult> {
  try {
    // 通知設定を確認
    const settings = await prisma.notificationSettings.findFirst({
      where: {
        tenant_id: tenantId,
        notification_type: notificationType,
        is_enabled: true,
        is_deleted: false,
      } as any,
    });

    if (!settings) {
      console.log(`通知タイプ ${notificationType} のメール送信は無効です`);
      return { success: false, error: '通知が無効化されています' };
    }

    // テンプレートIDを取得
    const templateId = settings.template_id || `default_${notificationType.toLowerCase()}`;

    // メール送信
    return await emailService.sendTemplateEmail(
      templateId,
      recipientEmail,
      data,
      tenantId
    );
  } catch (error) {
    console.error('通知メール送信エラー:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : '不明なエラー',
    };
  }
}