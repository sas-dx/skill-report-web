const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function checkWorkData() {
  try {
    console.log('=== ProjectRecordテーブルの作業実績データ ===');
    
    // emp_001のデータ
    const workEmp001 = await prisma.projectRecord.count({
      where: {
        employee_id: 'emp_001',
        is_deleted: false
      }
    });
    console.log('emp_001の作業実績数: ' + workEmp001);
    
    // 000001のデータ
    const work000001 = await prisma.projectRecord.count({
      where: {
        employee_id: '000001',
        is_deleted: false
      }
    });
    console.log('000001の作業実績数: ' + work000001);
    
  } catch (error) {
    console.error('エラー:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkWorkData();
