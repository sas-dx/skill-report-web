const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function checkTrainingData() {
  try {
    console.log('=== TrainingHistoryテーブルの研修データ ===');
    
    // emp_001のデータ
    const trainingEmp001 = await prisma.trainingHistory.findMany({
      where: {
        employee_id: 'emp_001',
        attendance_status: 'completed',
        is_deleted: false
      }
    });
    console.log('emp_001の完了研修数: ' + trainingEmp001.length);
    
    // 000001のデータ
    const training000001 = await prisma.trainingHistory.findMany({
      where: {
        employee_id: '000001',
        attendance_status: 'completed',
        is_deleted: false
      }
    });
    console.log('000001の完了研修数: ' + training000001.length);
    
    // すべての研修データ
    const allTraining = await prisma.trainingHistory.findMany({
      where: {
        is_deleted: false
      },
      select: {
        employee_id: true,
        attendance_status: true,
        training_name: true
      }
    });
    
    console.log('\n全研修データ:');
    allTraining.forEach(t => {
      console.log('  employee_id: ' + t.employee_id + ', status: ' + t.attendance_status + ', name: ' + t.training_name);
    });
    
  } catch (error) {
    console.error('エラー:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkTrainingData();
