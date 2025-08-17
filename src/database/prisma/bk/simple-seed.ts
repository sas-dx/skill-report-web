// @ts-nocheck
import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()

export async function runSimpleSeed() {
  console.log('🌱 シンプル版マスタデータ投入を開始します...')

  try {
    // パスワードハッシュ生成
    const passwordHash = await bcrypt.hash('password', 12);
    console.log('🔐 パスワードハッシュを生成しました');

    // 1. MST_Department（部署）
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
    await prisma.department.upsert({
      where: { department_code: 'DEPT003' },
      update: {},
      create: {
        department_code: 'DEPT003',
        department_name: '営業部',
      },
    });

    // 2. MST_Position（役職）
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

    // 3. MST_JobType（職種）
    console.log('📊 MST_JobTypeデータを投入中...')
    await prisma.jobType.upsert({
      where: { job_type_code: 'SE' },
      update: {},
      create: {
        job_type_code: 'SE',
        job_type_name: 'システムエンジニア',
      },
    });
    await prisma.jobType.upsert({
      where: { job_type_code: 'PM' },
      update: {},
      create: {
        job_type_code: 'PM',
        job_type_name: 'プロジェクトマネージャー',
      },
    });
    await prisma.jobType.upsert({
      where: { job_type_code: 'PG' },
      update: {},
      create: {
        job_type_code: 'PG',
        job_type_name: 'プログラマー',
      },
    });

    // 4. MST_Employee（従業員）
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
        position_id: 'POS003',
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
        department_id: 'DEPT002',
        position_id: 'POS003',
        job_type_id: 'PG',
        employment_status: 'FULL_TIME',
        employee_status: 'ACTIVE',
      },
    });

    // 5. MST_UserAuth（ユーザー認証）
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

    // 6. MST_SkillCategory（スキルカテゴリ）
    console.log('📊 MST_SkillCategoryデータを投入中...')
    await prisma.skillCategory.upsert({
      where: { category_code: 'CAT001' },
      update: {},
      create: {
        category_code: 'CAT001',
        category_name: 'プログラミング言語',
      },
    });
    await prisma.skillCategory.upsert({
      where: { category_code: 'CAT002' },
      update: {},
      create: {
        category_code: 'CAT002',
        category_name: 'フレームワーク',
      },
    });
    await prisma.skillCategory.upsert({
      where: { category_code: 'CAT003' },
      update: {},
      create: {
        category_code: 'CAT003',
        category_name: 'データベース',
      },
    });

    // 7. MST_SkillItem（スキル項目）
    console.log('📊 MST_SkillItemデータを投入中...')
    // プログラミング言語
    await prisma.skillItem.upsert({
      where: { skill_code: 'SKILL001' },
      update: {},
      create: {
        skill_code: 'SKILL001',
        skill_name: 'Java',
        skill_category_id: 'CAT001',
      },
    });
    await prisma.skillItem.upsert({
      where: { skill_code: 'SKILL002' },
      update: {},
      create: {
        skill_code: 'SKILL002',
        skill_name: 'Python',
        skill_category_id: 'CAT001',
      },
    });
    await prisma.skillItem.upsert({
      where: { skill_code: 'SKILL003' },
      update: {},
      create: {
        skill_code: 'SKILL003',
        skill_name: 'TypeScript',
        skill_category_id: 'CAT001',
      },
    });
    // フレームワーク
    await prisma.skillItem.upsert({
      where: { skill_code: 'SKILL004' },
      update: {},
      create: {
        skill_code: 'SKILL004',
        skill_name: 'React',
        skill_category_id: 'CAT002',
      },
    });
    await prisma.skillItem.upsert({
      where: { skill_code: 'SKILL005' },
      update: {},
      create: {
        skill_code: 'SKILL005',
        skill_name: 'Next.js',
        skill_category_id: 'CAT002',
      },
    });
    // データベース
    await prisma.skillItem.upsert({
      where: { skill_code: 'SKILL006' },
      update: {},
      create: {
        skill_code: 'SKILL006',
        skill_name: 'PostgreSQL',
        skill_category_id: 'CAT003',
      },
    });
    await prisma.skillItem.upsert({
      where: { skill_code: 'SKILL007' },
      update: {},
      create: {
        skill_code: 'SKILL007',
        skill_name: 'MySQL',
        skill_category_id: 'CAT003',
      },
    });

    // 8. MST_SkillGrade（スキルグレード）
    console.log('📊 MST_SkillGradeデータを投入中...')
    await prisma.skillGrade.upsert({
      where: { grade_code: 'GRADE1' },
      update: {},
      create: {
        grade_code: 'GRADE1',
        grade_name: '初級',
        grade_level: 1,
      },
    });
    await prisma.skillGrade.upsert({
      where: { grade_code: 'GRADE2' },
      update: {},
      create: {
        grade_code: 'GRADE2',
        grade_name: '中級',
        grade_level: 2,
      },
    });
    await prisma.skillGrade.upsert({
      where: { grade_code: 'GRADE3' },
      update: {},
      create: {
        grade_code: 'GRADE3',
        grade_name: '上級',
        grade_level: 3,
      },
    });
    await prisma.skillGrade.upsert({
      where: { grade_code: 'GRADE4' },
      update: {},
      create: {
        grade_code: 'GRADE4',
        grade_name: 'エキスパート',
        grade_level: 4,
      },
    });
    await prisma.skillGrade.upsert({
      where: { grade_code: 'GRADE5' },
      update: {},
      create: {
        grade_code: 'GRADE5',
        grade_name: 'マスター',
        grade_level: 5,
      },
    });

    console.log('\n✅ シンプル版マスタデータ投入が完了しました！\n')
    console.log('📋 投入されたマスタデータ:')
    console.log('   - 部署: 3件')
    console.log('   - 役職: 3件')
    console.log('   - 職種: 3件')
    console.log('   - 従業員: 3件')
    console.log('   - ユーザー認証: 3件')
    console.log('   - スキルカテゴリ: 3件')
    console.log('   - スキル項目: 7件')
    console.log('   - スキルグレード: 5件')
    console.log('\n🔐 ログイン情報:')
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
    console.error('❌ マスタデータ投入中にエラーが発生しました:', error)
    throw error
  } finally {
    await prisma.$disconnect()
  }
}

// 直接実行時
if (require.main === module) {
  runSimpleSeed()
    .then(() => {
      console.log('🎉 処理が正常に完了しました')
      process.exit(0)
    })
    .catch((e) => {
      console.error('❌ エラーが発生しました:', e)
      process.exit(1)
    })
}

// エクスポート
export default runSimpleSeed