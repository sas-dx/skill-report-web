const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function checkCertData() {
  try {
    console.log('=== PDUテーブルの資格データ ===');
    
    // emp_001のデータ
    const pduEmp001 = await prisma.pDU.findMany({
      where: {
        employee_id: 'emp_001',
        activity_type: 'certification',
        approval_status: 'approved',
        is_deleted: false
      }
    });
    console.log('emp_001の資格数: ' + pduEmp001.length);
    
    // 000001のデータ
    const pdu000001 = await prisma.pDU.findMany({
      where: {
        employee_id: '000001',
        activity_type: 'certification',
        approval_status: 'approved',
        is_deleted: false
      }
    });
    console.log('000001の資格数: ' + pdu000001.length);
    
    // すべてのPDUデータを確認
    const allPdu = await prisma.pDU.findMany({
      where: {
        activity_type: 'certification',
        approval_status: 'approved',
        is_deleted: false
      }
    });
    console.log('\n全PDU資格データ:');
    allPdu.forEach(p => {
      console.log('  employee_id: ' + p.employee_id + ', activity_name: ' + p.activity_name);
    });
    
  } catch (error) {
    console.error('エラー:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkCertData();
