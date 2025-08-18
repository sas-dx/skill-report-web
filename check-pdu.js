const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function checkPDU() {
  try {
    const pdus = await prisma.pDU.findMany({
      where: {
        employee_id: '00000000-0000-0000-0000-000000000001'
      }
    });
    
    console.log('PDUレコード:', pdus);
    
    const count = await prisma.pDU.count({
      where: {
        employee_id: '00000000-0000-0000-0000-000000000001',
        activity_type: 'certification',
        approval_status: 'approved',
        is_deleted: false
      }
    });
    
    console.log('資格カウント:', count);
  } catch (error) {
    console.error('エラー:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkPDU();
