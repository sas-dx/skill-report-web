const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function checkCurrentUser() {
  try {
    // 実際にログインしているユーザーの確認（emp_001）
    console.log('=== emp_001の目標データ ===');
    const empGoals = await prisma.goalProgress.findMany({
      where: {
        employee_id: 'emp_001',
        is_deleted: false
      }
    });
    
    console.log('emp_001の目標数: ' + empGoals.length);
    let empTotal = 0;
    empGoals.forEach(g => {
      let value = 0;
      if (g.progress_rate) {
        value = typeof g.progress_rate === 'object' 
          ? parseFloat(g.progress_rate.toString())
          : Number(g.progress_rate);
      }
      console.log('- ' + (g.goal_title || 'タイトルなし') + ': ' + value + '%');
      empTotal += value;
    });
    const empAvg = empGoals.length > 0 ? Math.round(empTotal / empGoals.length) : 0;
    console.log('平均進捗率: ' + empAvg + '%\n');
    
    // 000001のデータも確認
    console.log('=== 000001の目標データ ===');
    const goals000001 = await prisma.goalProgress.findMany({
      where: {
        employee_id: '000001',
        is_deleted: false
      }
    });
    
    console.log('000001の目標数: ' + goals000001.length);
    let total000001 = 0;
    goals000001.forEach(g => {
      let value = 0;
      if (g.progress_rate) {
        value = typeof g.progress_rate === 'object' 
          ? parseFloat(g.progress_rate.toString())
          : Number(g.progress_rate);
      }
      console.log('- ' + (g.goal_title || 'タイトルなし') + ': ' + value + '%');
      total000001 += value;
    });
    const avg000001 = goals000001.length > 0 ? Math.round(total000001 / goals000001.length) : 0;
    console.log('平均進捗率: ' + avg000001 + '%');
    
  } catch (error) {
    console.error('エラー:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkCurrentUser();
