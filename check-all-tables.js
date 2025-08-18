const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function checkAllTables() {
  try {
    console.log('=== データベース全体のチェック ===\n');
    
    // 1. TrainingHistoryテーブル
    const trainingCount = await prisma.trainingHistory.count();
    console.log(`TrainingHistoryテーブル: ${trainingCount}件`);
    if (trainingCount > 0) {
      const trainings = await prisma.trainingHistory.findMany({
        select: {
          id: true,
          employee_id: true,
          training_name: true,
          certificate_obtained: true,
          attendance_status: true
        }
      });
      console.log('TrainingHistoryレコード:', trainings);
    }
    
    // 2. PDUテーブル
    const pduCount = await prisma.pDU.count();
    console.log(`\nPDUテーブル: ${pduCount}件`);
    if (pduCount > 0) {
      const pdus = await prisma.pDU.findMany({
        select: {
          id: true,
          employee_id: true,
          activity_name: true,
          activity_type: true,
          approval_status: true
        }
      });
      console.log('PDUレコード:', pdus);
    }
    
    // 3. Certificationテーブル（資格マスタ）
    const certCount = await prisma.certification.count();
    console.log(`\nCertificationテーブル（マスタ）: ${certCount}件`);
    
    // 4. TrainingProgramテーブル
    const programCount = await prisma.trainingProgram.count();
    console.log(`TrainingProgramテーブル: ${programCount}件`);
    
  } catch (error) {
    console.error('エラー:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkAllTables();
