const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function testAPI() {
  try {
    // emp_001でデータを確認
    console.log('=== emp_001でTrainingHistoryを確認 ===');
    const trainings = await prisma.trainingHistory.findMany({
      where: {
        employee_id: 'emp_001',
        certificate_obtained: true
      }
    });
    console.log(`certificate_obtained=trueの件数: ${trainings.length}`);
    
    // PDUテーブルも確認
    console.log('\n=== emp_001でPDUを確認 ===');
    const pdus = await prisma.pDU.findMany({
      where: {
        employee_id: 'emp_001',
        activity_type: 'certification',
        approval_status: 'approved'
      }
    });
    console.log(`PDU資格の件数: ${pdus.length}`);
    pdus.forEach(pdu => {
      console.log(`- ${pdu.activity_name}`);
    });
    
  } catch (error) {
    console.error('エラー:', error);
  } finally {
    await prisma.$disconnect();
  }
}

testAPI();
