const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function checkDetail() {
  try {
    const goals = await prisma.goalProgress.findMany({
      where: {
        employee_id: '000001',
        is_deleted: false,
        achievement_status: { notIn: ['cancelled', 'postponed'] }
      }
    });
    
    console.log('=== 各目標の詳細データ ===');
    goals.forEach(g => {
      console.log('\n目標: ' + (g.goal_title || '(タイトルなし)'));
      console.log('  progress_rate: ' + g.progress_rate);
      console.log('  progress_rate型: ' + typeof g.progress_rate);
      console.log('  achievement_rate: ' + g.achievement_rate);
      console.log('  achievement_rate型: ' + typeof g.achievement_rate);
      console.log('  ステータス: ' + g.achievement_status);
      
      const progressValue = Number(g.progress_rate) || Number(g.achievement_rate) || 0;
      console.log('  計算に使用する値: ' + progressValue);
    });
    
  } catch (error) {
    console.error('エラー:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkDetail();
