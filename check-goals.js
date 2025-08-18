const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function checkGoals() {
  try {
    // emp_001のGoalProgressを確認
    const goals = await prisma.goalProgress.findMany({
      where: {
        employee_id: 'emp_001',
        is_deleted: false
      }
    });
    
    console.log('emp_001の目標数: ' + goals.length);
    
    const currentGoals = goals.filter(g => g.achievement_status === 'in_progress' || g.achievement_status === 'pending');
    const completedGoals = goals.filter(g => g.achievement_status === 'completed' || g.achievement_status === 'achieved');
    
    console.log('進行中の目標: ' + currentGoals.length + '個');
    console.log('完了済みの目標: ' + completedGoals.length + '個');
    
    // 計算ロジック再現
    let totalProgress = 0;
    let totalGoalCount = goals.length;
    
    totalProgress += completedGoals.length * 100;
    totalProgress += currentGoals.reduce((sum, goal) => {
      const progress = goal.progress_rate || goal.achievement_rate || 0;
      console.log('目標: ' + goal.goal_name + ', 進捗率: ' + progress + '%');
      return sum + Number(progress);
    }, 0);
    
    const overallProgress = totalGoalCount > 0 
      ? totalProgress / totalGoalCount 
      : 0;
    
    console.log('\n計算結果:');
    console.log('totalProgress: ' + totalProgress);
    console.log('totalGoalCount: ' + totalGoalCount);
    console.log('目標達成率: ' + Math.round(overallProgress) + '%');
    
  } catch (error) {
    console.error('エラー:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkGoals();
