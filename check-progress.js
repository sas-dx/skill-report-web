const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function checkProgress() {
  console.log('=== 目標の進捗率を確認 ===\n');
  
  const goals = await prisma.goalProgress.findMany({
    where: {
      employee_id: '000001',
      is_deleted: false
    },
    orderBy: {
      created_at: 'desc'
    }
  });
  
  goals.forEach((goal, index) => {
    console.log(`目標 ${index + 1}:`);
    console.log(`  タイトル: ${goal.goal_title}`);
    console.log(`  ステータス: ${goal.achievement_status}`);
    console.log(`  進捗率: ${goal.progress_rate}%`);
    console.log(`  達成率: ${goal.achievement_rate}%`);
    console.log(`  目標日: ${goal.target_date?.toLocaleDateString('ja-JP')}`);
    console.log('---');
  });
  
  // 進捗率を50%に更新してテスト
  if (goals.length > 0) {
    console.log('\n=== 最初の目標の進捗率を50%に更新 ===');
    const updated = await prisma.goalProgress.update({
      where: { id: goals[0].id },
      data: {
        progress_rate: 50,
        updated_at: new Date()
      }
    });
    console.log(`更新後の進捗率: ${updated.progress_rate}%`);
  }
}

checkProgress()
  .then(() => prisma.$disconnect())
  .catch(err => {
    console.error(err);
    prisma.$disconnect();
  });