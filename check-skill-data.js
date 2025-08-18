const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function checkSkillData() {
  try {
    console.log('=== SkillRecordテーブルのスキルデータ ===');
    
    // emp_001のデータ
    const skillsEmp001 = await prisma.skillRecord.findMany({
      where: {
        employee_id: 'emp_001',
        skill_level: { gt: 0 },
        is_deleted: false
      }
    });
    console.log('emp_001のスキル数: ' + skillsEmp001.length);
    
    // 000001のデータ
    const skills000001 = await prisma.skillRecord.findMany({
      where: {
        employee_id: '000001',
        skill_level: { gt: 0 },
        is_deleted: false
      }
    });
    console.log('000001のスキル数: ' + skills000001.length);
    
    // すべてのスキルデータを確認
    const allSkills = await prisma.skillRecord.findMany({
      where: {
        skill_level: { gt: 0 },
        is_deleted: false
      },
      select: {
        employee_id: true,
        skill_name: true,
        skill_level: true
      }
    });
    
    console.log('\n全スキルデータ:');
    const byEmployee = {};
    allSkills.forEach(s => {
      if (!byEmployee[s.employee_id]) {
        byEmployee[s.employee_id] = [];
      }
      byEmployee[s.employee_id].push(s.skill_name);
    });
    
    Object.entries(byEmployee).forEach(([empId, skills]) => {
      console.log('  employee_id: ' + empId + ' - ' + skills.length + '個のスキル');
    });
    
  } catch (error) {
    console.error('エラー:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkSkillData();
