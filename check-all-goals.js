const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function checkAllGoals() {
  try {
    // 全員のGoalProgressを確認
    const allGoals = await prisma.goalProgress.findMany({
      where: {
        is_deleted: false
      }
    });
    
    // employee_idごとにグループ化
    const goalsByEmployee = {};
    allGoals.forEach(goal => {
      if (!goalsByEmployee[goal.employee_id]) {
        goalsByEmployee[goal.employee_id] = [];
      }
      goalsByEmployee[goal.employee_id].push(goal);
    });
    
    console.log('=== 各従業員の目標データ ===\n');
    
    for (const [empId, goals] of Object.entries(goalsByEmployee)) {
      console.log('Employee ID: ' + empId);
      console.log('目標数: ' + goals.length);
      
      const currentGoals = goals.filter(g => g.achievement_status === 'in_progress' || g.achievement_status === 'pending');
      const completedGoals = goals.filter(g => g.achievement_status === 'completed' || g.achievement_status === 'achieved');
      
      let totalProgress = 0;
      totalProgress += completedGoals.length * 100;
      totalProgress += currentGoals.reduce((sum, goal) => {
        const progress = goal.progress_rate || goal.achievement_rate || 0;
        return sum + Number(progress);
      }, 0);
      
      const overallProgress = goals.length > 0 ? totalProgress / goals.length : 0;
      
      console.log('進行中: ' + currentGoals.length + '個');
      console.log('完了済み: ' + completedGoals.length + '個');
      console.log('目標達成率: ' + Math.round(overallProgress) + '%');
      
      // 各目標の詳細
      goals.forEach(g => {
        console.log('  - ' + g.goal_name + ' (' + g.achievement_status + '): ' + (g.progress_rate || g.achievement_rate || 0) + '%');
      });
      
      console.log('---\n');
    }
    
  } catch (error) {
    console.error('エラー:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkAllGoals();
