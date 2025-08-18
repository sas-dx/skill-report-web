const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function checkUser() {
  try {
    // Employeeテーブルから確認
    const employees = await prisma.employee.findMany({
      select: {
        id: true,
        employee_code: true,
        full_name: true,
        email: true
      }
    });
    
    console.log('=== Employee一覧 ===');
    employees.forEach(emp => {
      console.log(`Employee ID (PK): ${emp.id}`);
      console.log(`Employee Code: ${emp.employee_code}`);
      console.log(`Name: ${emp.full_name}`);
      console.log(`Email: ${emp.email}`);
      console.log('---');
    });
    
    // ダッシュボードAPIで使用されているIDを確認
    console.log('\n=== ダッシュボードで期待されるID ===');
    console.log('00000000-0000-0000-0000-000000000001');
    
  } catch (error) {
    console.error('エラー:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkUser();
