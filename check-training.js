const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function checkTraining() {
  try {
    const trainings = await prisma.trainingHistory.findMany({
      where: {
        employee_id: '00000000-0000-0000-0000-000000000001'
      }
    });
    
    console.log('TrainingHistoryレコード:', trainings);
    
    const certCount = await prisma.trainingHistory.count({
      where: {
        employee_id: '00000000-0000-0000-0000-000000000001',
        certificate_obtained: true,
        is_deleted: false
      }
    });
    
    console.log('certificate_obtained=trueの数:', certCount);
  } catch (error) {
    console.error('エラー:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkTraining();
