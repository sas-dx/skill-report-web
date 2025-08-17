const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function checkGoals() {
  console.log('=== TRN_GoalProgress テーブル確認 ===');
  
  const goals = await prisma.goalProgress.findMany({
    where: {
      employee_id: '000001',
      is_deleted: false
    },
    orderBy: {
      created_at: 'desc'
    }
  });
  
  console.log(`\n総目標数: ${goals.length}`);
  
  goals.forEach((goal, index) => {
    console.log(`\n--- 目標 ${index + 1} ---`);
    console.log(`ID: ${goal.id}`);
    console.log(`Goal ID: ${goal.goal_id}`);
    console.log(`タイトル: ${goal.goal_title}`);
    console.log(`タイプ: ${goal.goal_type}`);
    console.log(`ステータス: ${goal.achievement_status}`);
    console.log(`目標日: ${goal.target_date}`);
    console.log(`作成日: ${goal.created_at}`);
    console.log(`優先度: ${goal.priority_level}`);
  });

  console.log('\n=== TRN_CareerPlan テーブル確認 ===');
  
  const careerPlans = await prisma.careerPlan.findMany({
    where: {
      employee_id: '000001',
      is_deleted: false
    },
    orderBy: {
      created_at: 'desc'
    }
  });
  
  console.log(`\n総キャリアプラン数: ${careerPlans.length}`);
  
  careerPlans.forEach((plan, index) => {
    console.log(`\n--- プラン ${index + 1} ---`);
    console.log(`ID: ${plan.career_plan_id}`);
    console.log(`名前: ${plan.plan_name}`);
    console.log(`説明: ${plan.plan_description}`);
    console.log(`ステータス: ${plan.plan_status}`);
    console.log(`開始日: ${plan.plan_start_date}`);
    console.log(`終了日: ${plan.plan_end_date}`);
  });
}

checkGoals()
  .then(() => prisma.$disconnect())
  .catch(err => {
    console.error(err);
    prisma.$disconnect();
  });