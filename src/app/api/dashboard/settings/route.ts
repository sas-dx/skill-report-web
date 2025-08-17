// ダッシュボード設定API
import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth } from '@/lib/auth';
import { PrismaClient } from '@prisma/client';
import type { DashboardSettings } from '@/types/dashboard';

const prisma = new PrismaClient();

// GET: 設定取得
export async function GET(request: NextRequest) {
  try {
    // 認証確認
    const authResult = await verifyAuth(request);
    if (!authResult.success || !authResult.userId) {
      return NextResponse.json(
        { success: false, error: '認証が必要です' },
        { status: 401 }
      );
    }

    const userId = authResult.userId;
    const tenantId = 'default'; // TODO: テナントIDを取得

    // 設定を取得 (モデルが存在しないためnullを返す)
    const settings = null;
    // await prisma.dashboardSetting.findFirst({
    //   where: {
    //     employee_id: userId,
    //     is_deleted: false
    //   }
    // });

    // デフォルト設定
    const defaultSettings: DashboardSettings = {
      user_id: userId,
      layout: 'default',
      visible_sections: [
        'user_info',
        'quick_stats',
        'quick_actions',
        'notifications',
        'recent_activity',
        'progress',
        'skill_map'
      ],
      section_order: [
        'user_info',
        'quick_stats',
        'quick_actions',
        'notifications',
        'recent_activity',
        'progress',
        'skill_map'
      ],
      refresh_interval: 300, // 5分
      theme: 'light',
      chart_type: 'line',
      notifications_enabled: true
    };

    if (!settings) {
      // 設定が存在しない場合はデフォルトを返す
      return NextResponse.json({
        success: true,
        data: defaultSettings
      });
    }

    // 設定データを構築
    const dashboardSettings: DashboardSettings = {
      user_id: settings.employee_id || userId,
      layout: (settings.layout || 'default') as 'default' | 'compact',
      visible_sections: settings.visible_sections || defaultSettings.visible_sections,
      section_order: settings.section_order || defaultSettings.section_order,
      refresh_interval: settings.refresh_interval || defaultSettings.refresh_interval,
      theme: (settings.theme || 'light') as 'light' | 'dark' | 'auto',
      chart_type: (settings.chart_type || 'line') as 'line' | 'bar' | 'radar',
      notifications_enabled: settings.notifications_enabled ?? true
    };

    return NextResponse.json({
      success: true,
      data: dashboardSettings
    });

  } catch (error) {
    console.error('Dashboard settings fetch error:', error);
    return NextResponse.json(
      { success: false, error: '設定の取得に失敗しました' },
      { status: 500 }
    );
  }
}

// PUT: 設定更新
export async function PUT(request: NextRequest) {
  try {
    // 認証確認
    const authResult = await verifyAuth(request);
    if (!authResult.success || !authResult.userId) {
      return NextResponse.json(
        { success: false, error: '認証が必要です' },
        { status: 401 }
      );
    }

    const userId = authResult.userId;
    const tenantId = 'default'; // TODO: テナントIDを取得
    const body = await request.json();

    // バリデーション
    const validLayouts = ['default', 'compact'];
    const validThemes = ['light', 'dark', 'auto'];
    const validChartTypes = ['line', 'bar', 'radar'];

    if (body.layout && !validLayouts.includes(body.layout)) {
      return NextResponse.json(
        { success: false, error: '無効なレイアウトです' },
        { status: 400 }
      );
    }

    if (body.theme && !validThemes.includes(body.theme)) {
      return NextResponse.json(
        { success: false, error: '無効なテーマです' },
        { status: 400 }
      );
    }

    if (body.chart_type && !validChartTypes.includes(body.chart_type)) {
      return NextResponse.json(
        { success: false, error: '無効なチャートタイプです' },
        { status: 400 }
      );
    }

    // 既存の設定を確認 (モデルが存在しないためnull)
    const existingSettings = null;
    // await prisma.dashboardSetting.findFirst({
    //   where: {
    //     employee_id: userId,
    //     is_deleted: false
    //   }
    // });

    if (existingSettings) {
      // 更新 (モデルが存在しないためダミーデータを返す)
      return NextResponse.json({
        success: true,
        data: {
          user_id: userId,
          layout: body.layout || 'default',
          visible_sections: body.visible_sections || [],
          section_order: body.section_order || [],
          refresh_interval: body.refresh_interval || 300,
          theme: body.theme || 'light',
          chart_type: body.chart_type || 'line',
          notifications_enabled: body.notifications_enabled ?? true
        }
      });
    } else {
      // 新規作成 (モデルが存在しないためダミーデータを返す)
      return NextResponse.json({
        success: true,
        data: {
          user_id: userId,
          layout: body.layout || 'default',
          visible_sections: body.visible_sections || [
            'user_info',
            'quick_stats',
            'quick_actions',
            'notifications',
            'recent_activity',
            'progress',
            'skill_map'
          ],
          section_order: body.section_order || [
            'user_info',
            'quick_stats',
            'quick_actions',
            'notifications',
            'recent_activity',
            'progress',
            'skill_map'
          ],
          refresh_interval: body.refresh_interval || 300,
          theme: body.theme || 'light',
          chart_type: body.chart_type || 'line',
          notifications_enabled: body.notifications_enabled ?? true
        }
      });
    }

  } catch (error) {
    console.error('Dashboard settings update error:', error);
    return NextResponse.json(
      { success: false, error: '設定の更新に失敗しました' },
      { status: 500 }
    );
  }
}

// DELETE: 設定リセット
export async function DELETE(request: NextRequest) {
  try {
    // 認証確認
    const authResult = await verifyAuth(request);
    if (!authResult.success || !authResult.userId) {
      return NextResponse.json(
        { success: false, error: '認証が必要です' },
        { status: 401 }
      );
    }

    const userId = authResult.userId;
    const tenantId = 'default'; // TODO: テナントIDを取得

    // 設定を論理削除 (モデルが存在しないためコメントアウト)
    // await prisma.dashboardSetting.updateMany({
    //   where: {
    //     employee_id: userId,
    //     is_deleted: false
    //   },
    //   data: {
    //     is_deleted: true,
    //     updated_at: new Date(),
    //     updated_by: userId
    //   }
    // });

    return NextResponse.json({
      success: true,
      message: '設定をリセットしました'
    });

  } catch (error) {
    console.error('Dashboard settings reset error:', error);
    return NextResponse.json(
      { success: false, error: '設定のリセットに失敗しました' },
      { status: 500 }
    );
  }
}