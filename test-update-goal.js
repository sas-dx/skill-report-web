const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function testUpdateGoal() {
  console.log('=== 更新前の目標を確認 ===');
  
  // 最新の目標を取得
  const goal = await prisma.goalProgress.findFirst({
    where: {
      employee_id: '000001',
      is_deleted: false
    },
    orderBy: {
      created_at: 'desc'
    }
  });
  
  if (!goal) {
    console.log('目標が見つかりません');
    return;
  }
  
  console.log('現在の目標:');
  console.log(`  ID: ${goal.id}`);
  console.log(`  Goal ID: ${goal.goal_id}`);
  console.log(`  タイトル: ${goal.goal_title}`);
  console.log(`  ステータス: ${goal.achievement_status}`);
  console.log(`  更新日: ${goal.updated_at}`);
  
  console.log('\n=== ステータスをcancelledに更新 ===');
  
  try {
    const updated = await prisma.goalProgress.update({
      where: {
        id: goal.id
      },
      data: {
        achievement_status: 'cancelled',
        updated_at: new Date(),
        updated_by: '000001'
      }
    });
    
    console.log('更新後:');
    console.log(`  ステータス: ${updated.achievement_status}`);
    console.log(`  更新日: ${updated.updated_at}`);
    
    // 再度確認
    const confirmed = await prisma.goalProgress.findUnique({
      where: { id: goal.id }
    });
    
    console.log('\n=== 更新確認 ===');
    console.log(`  ステータス: ${confirmed.achievement_status}`);
    
  } catch (error) {
    console.error('更新エラー:', error);
  }
}

testUpdateGoal()
  .then(() => prisma.$disconnect())
  .catch(err => {
    console.error(err);
    prisma.$disconnect();
  });