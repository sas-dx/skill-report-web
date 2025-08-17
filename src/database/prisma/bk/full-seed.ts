// @ts-nocheck
import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()

export async function runFullSeed() {
  console.log('🌱 完全なデータベース初期データ投入を開始します...')

  try {
    // パスワードを正しくハッシュ化
    const passwordHash = await bcrypt.hash('password', 12);
    console.log('🔐 Generated password hash');

    // 1. MST_Tenantデータ（最小限）
    console.log('📊 MST_Tenantデータを投入中...')
    await prisma.tenant.upsert({
      where: { tenant_id: 'default-tenant' },
      update: {},
      create: {
        tenant_id: 'default-tenant',
        tenant_code: 'DEFAULT',
        tenant_name: 'デフォルトテナント',
      },
    });

    // 2. MST_Departmentデータ
    console.log('📊 MST_Departmentデータを投入中...')
    await prisma.department.upsert({
      where: { department_code: 'DEPT001' },
      update: {},
      create: {
        department_code: 'DEPT001',
        department_name: '経営企画部',
      },
    });
    
    await prisma.department.upsert({
      where: { department_code: 'DEPT002' },
      update: {},
      create: {
        department_code: 'DEPT002',
        department_name: 'システム開発部',
      },
    });

    // 3. MST_Positionデータ
    console.log('📊 MST_Positionデータを投入中...')
    await prisma.position.upsert({
      where: { position_code: 'POS001' },
      update: {},
      create: {
        position_code: 'POS001',
        position_name: '社長',
      },
    });
    
    await prisma.position.upsert({
      where: { position_code: 'POS002' },
      update: {},
      create: {
        position_code: 'POS002',
        position_name: '取締役',
      },
    });
    
    await prisma.position.upsert({
      where: { position_code: 'POS003' },
      update: {},
      create: {
        position_code: 'POS003',
        position_name: '部長',
      },
    });

    // 4. MST_Employeeデータ
    console.log('📊 MST_Employeeデータを投入中...')
    await prisma.employee.upsert({
      where: { id: 'emp_001' },
      update: {},
      create: {
        id: 'emp_001',
        employee_code: '000001',
        full_name: '笹尾 豊樹',
        full_name_kana: 'ササオ トヨキ',
        email: 'sasao.toyoki@example.com',
        phone: '090-1234-5678',
        hire_date: new Date('2020-04-01'),
        birth_date: new Date('1990-01-15'),
        gender: 'M',
        department_id: 'DEPT002',
        position_id: 'POS002',
        job_type_id: 'SE',
        employment_status: 'FULL_TIME',
        employee_status: 'ACTIVE',
      },
    });
    
    await prisma.employee.upsert({
      where: { id: 'emp_002' },
      update: {},
      create: {
        id: 'emp_002',
        employee_code: '000002',
        full_name: '佐藤 花子',
        full_name_kana: 'サトウ ハナコ',
        email: 'sato.hanako@example.com',
        phone: '090-2345-6789',
        hire_date: new Date('2018-04-01'),
        birth_date: new Date('1985-03-20'),
        gender: 'F',
        department_id: 'DEPT001',
        position_id: 'POS003',
        job_type_id: 'PM',
        employment_status: 'FULL_TIME',
        employee_status: 'ACTIVE',
      },
    });
    
    await prisma.employee.upsert({
      where: { id: 'emp_test' },
      update: {},
      create: {
        id: 'emp_test',
        employee_code: 'test-employee',
        full_name: 'テスト ユーザー',
        full_name_kana: 'テスト ユーザー',
        email: 'test@example.com',
        phone: '090-0000-0000',
        hire_date: new Date('2025-01-01'),
        birth_date: new Date('1995-01-01'),
        gender: 'M',
        department_id: 'DEPT001',
        position_id: 'POS003',
        job_type_id: 'SE',
        employment_status: 'FULL_TIME',
        employee_status: 'ACTIVE',
      },
    });

    // 5. MST_UserAuthデータ
    console.log('📊 MST_UserAuthデータを投入中...')
    await prisma.userAuth.upsert({
      where: { user_id: 'USER000001' },
      update: {},
      create: {
        user_id: 'USER000001',
        login_id: '000001',
        password_hash: passwordHash,
        password_salt: 'randomsalt123',
        employee_id: '000001',
        account_status: 'ACTIVE',
        failed_login_count: 0,
        session_timeout: 480,
      },
    });
    
    await prisma.userAuth.upsert({
      where: { user_id: 'USER000002' },
      update: {},
      create: {
        user_id: 'USER000002',
        login_id: '000002',
        password_hash: passwordHash,
        password_salt: 'randomsalt456',
        employee_id: '000002',
        account_status: 'ACTIVE',
        failed_login_count: 0,
        session_timeout: 480,
      },
    });
    
    await prisma.userAuth.upsert({
      where: { user_id: 'USER_TEST_EMPLOYEE' },
      update: {},
      create: {
        user_id: 'USER_TEST_EMPLOYEE',
        login_id: 'test-employee',
        password_hash: passwordHash,
        password_salt: 'testsalt123',
        employee_id: 'test-employee',
        account_status: 'ACTIVE',
        failed_login_count: 0,
        session_timeout: 480,
      },
    });

    // 6. 基本的なスキルカテゴリ
    console.log('📊 MST_SkillCategoryデータを投入中...')
    await prisma.skillCategory.upsert({
      where: { category_code: 'CAT001' },
      update: {},
      create: {
        category_code: 'CAT001',
        category_name: 'プログラミング言語',
      },
    });

    // 7. 基本的なスキル項目
    console.log('📊 MST_SkillItemデータを投入中...')
    await prisma.skillItem.upsert({
      where: { skill_code: 'SKILL001' },
      update: {},
      create: {
        skill_code: 'SKILL001',
        skill_name: 'Java',
        skill_category_id: 'CAT001',
      },
    });

    // 8. スキル記録はスキップ（必須フィールドが多すぎるため）
    console.log('📊 TRN_SkillRecordデータはスキップ...')

    // 9. プロジェクト記録もスキップ（必須フィールドが多すぎるため）
    console.log('📊 TRN_ProjectRecordデータはスキップ...')

    console.log('✅ 完全なデータベース初期データ投入が完了しました！')
    console.log('')
    console.log('📋 投入されたデータの詳細:')
    console.log('   - テナント: 1件')
    console.log('   - 部署: 2件')
    console.log('   - 役職: 3件')
    console.log('   - 社員: 3件')
    console.log('   - ユーザー認証: 3件')
    console.log('   - スキルカテゴリ: 1件')
    console.log('   - スキル項目: 1件')
    console.log('')
    console.log('🔐 ログイン情報:')
    console.log('   テストユーザー（推奨）:')
    console.log('     ユーザーID: test-employee')
    console.log('     パスワード: password')
    console.log('   ユーザー1:')
    console.log('     ユーザーID: 000001')
    console.log('     パスワード: password')
    console.log('   ユーザー2:')
    console.log('     ユーザーID: 000002')
    console.log('     パスワード: password')

  } catch (error) {
    console.error('❌ 初期データ投入中にエラーが発生しました:', error)
    throw error
  }
}

if (require.main === module) {
  runFullSeed()
    .then(async () => {
      await prisma.$disconnect()
    })
    .catch(async (e) => {
      console.error('❌ 初期データ投入中にエラーが発生しました:', e)
      await prisma.$disconnect()
      throw e
    })
}