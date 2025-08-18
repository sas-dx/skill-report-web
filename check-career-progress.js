const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function checkCareerProgress() {
  try {
    // emp_001の目標進捗データを確認
    const empGoals = await prisma.goalProgress.findMany({
      where: {
        employee_id: 'emp_001',
        is_deleted: false
      }
    });
    
    console.log('=== emp_001のキャリアプラン進捗 ===');
    console.log('目標数: ' + empGoals.length);
    
    if (empGoals.length > 0) {
      empGoals.forEach(g => {
        console.log('\n目標: ' + (g.goal_title || '(タイトルなし)'));
        console.log('  ステータス: ' + g.achievement_status);
        console.log('  進捗率: ' + (g.progress_rate || 0) + '%');
        console.log('  達成率: ' + (g.achievement_rate || 0) + '%');
      });
      
      // キャリアプランAPIと同じ計算
      const avgProgress = empGoals.length > 0 
        ? Math.round(empGoals.reduce((sum, p) => sum + (p.progress_rate || 0), 0) / empGoals.length)
        : 0;
      
      console.log('\n平均進捗率（キャリアプラン方式）: ' + avgProgress + '%');
      
      // ダッシュボードの新しい計算方式
      const activeGoals = empGoals.filter(g => 
        g.achievement_status !== 'cancelled' && 
        g.achievement_status !== 'postponed'
      );
      
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
      
      console.log('目標達成率（ダッシュボード方式）: ' + dashboardProgress + '%');
    }
    
  } catch (error) {
    console.error('エラー:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkCareerProgress();
