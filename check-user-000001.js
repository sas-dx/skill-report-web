const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function checkUser000001() {
  try {
    // 000001の目標進捗データを確認
    const goals = await prisma.goalProgress.findMany({
      where: {
        employee_id: '000001',
        is_deleted: false
      }
    });
    
    console.log('=== 000001の目標データ ===');
    console.log('全目標数: ' + goals.length);
    
    // ステータス別にカウント
    const statusCount = {};
    goals.forEach(g => {
      statusCount[g.achievement_status] = (statusCount[g.achievement_status] || 0) + 1;
    });
    
    console.log('\nステータス別内訳:');
    Object.entries(statusCount).forEach(([status, count]) => {
      console.log('  ' + status + ': ' + count + '個');
    });
    
    // アクティブな目標のみ（キャンセル・延期を除外）
    const activeGoals = goals.filter(g => 
      g.achievement_status !== 'cancelled' && 
      g.achievement_status !== 'postponed'
    );
    
    console.log('\nアクティブな目標: ' + activeGoals.length + '個');
    
    // 各目標の詳細
    console.log('\n目標の詳細:');
    activeGoals.forEach(g => {
      console.log('  - ' + (g.goal_title || '(タイトルなし)'));
      console.log('    ステータス: ' + g.achievement_status);
      console.log('    進捗率: ' + (g.progress_rate || 0) + '%');
    });
    
    // ダッシュボードの計算方式
    let totalProgress = 0;
    activeGoals.forEach(goal => {
      if (goal.achievement_status === 'completed' || goal.achievement_status === 'achieved') {
        totalProgress += 100;
      } else {
        totalProgress += (goal.progress_rate || goal.achievement_rate || 0);
      }
    });
    
    const dashboardProgress = activeGoals.length > 0 
      ? Math.round(totalProgress / activeGoals.length)
      : 0;
    
    console.log('\n計算結果:');
    console.log('目標達成率: ' + dashboardProgress + '%');
    
  } catch (error) {
    console.error('エラー:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkUser000001();
