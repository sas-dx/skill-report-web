// @ts-nocheck
import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()

export async function runMinimalSeed() {
  console.log('🌱 最小限のデータベース初期データ投入を開始します...')

  try {
    // パスワードを正しくハッシュ化
    const passwordHash = await bcrypt.hash('password', 12);
    console.log('🔐 Generated password hash for "password":', passwordHash);

    // MST_Employeeデータ
    console.log('📊 MST_Employeeデータを投入中...')
    const employeeData = await Promise.all([
      prisma.employee.upsert({
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
          manager_id: 'emp_002',
          employee_status: 'ACTIVE',
        },
      }),
      prisma.employee.upsert({
        where: { id: 'emp_002' },
        update: {},
        create: {
          id: 'emp_002',
          employee_code: '000002',
          full_name: '佐藤花子',
          full_name_kana: 'サトウハナコ',
          email: 'sato.hanako@example.com',
          phone: '090-2345-6789',
          hire_date: new Date('2018-04-01'),
          birth_date: new Date('1985-03-20'),
          gender: 'F',
          department_id: 'DEPT001',
          position_id: 'POS002',
          job_type_id: 'PM',
          employment_status: 'FULL_TIME',
          employee_status: 'ACTIVE',
        },
      }),
      // テスト用Employee
      prisma.employee.upsert({
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
      }),
    ])

    // MST_UserAuthデータ
    console.log('📊 MST_UserAuthデータを投入中...')
    const userAuthData = await Promise.all([
      prisma.userAuth.upsert({
        where: { user_id: 'USER000001' },
        update: {},
        create: {
          user_id: 'USER000001',
          login_id: '000001',
          password_hash: passwordHash,
          password_salt: 'randomsalt123',
          employee_id: '000001',
          account_status: 'ACTIVE',
          last_login_at: new Date('2025-06-01T09:00:00Z'),
          last_login_ip: '192.168.1.100',
          failed_login_count: 0,
          password_changed_at: new Date('2025-01-01T00:00:00Z'),
          password_expires_at: new Date('2025-12-31T23:59:59Z'),
          mfa_enabled: true,
          mfa_secret: 'JBSWY3DPEHPK3PXP',
          session_timeout: 480,
        },
      }),
      // テスト用ユーザー追加
      prisma.userAuth.upsert({
        where: { user_id: 'USER_TEST_EMPLOYEE' },
        update: {},
        create: {
          user_id: 'USER_TEST_EMPLOYEE',
          login_id: 'test-employee',
          password_hash: passwordHash,
          password_salt: 'testsalt123',
          employee_id: 'test-employee',
          account_status: 'ACTIVE',
          last_login_at: new Date('2025-06-01T09:00:00Z'),
          last_login_ip: '192.168.1.100',
          failed_login_count: 0,
          password_changed_at: new Date('2025-01-01T00:00:00Z'),
          password_expires_at: new Date('2025-12-31T23:59:59Z'),
          mfa_enabled: false,
          session_timeout: 480,
        },
      }),
      prisma.userAuth.upsert({
        where: { user_id: 'USER000002' },
        update: {},
        create: {
          user_id: 'USER000002',
          login_id: '000002',
          password_hash: passwordHash,
          password_salt: 'randomsalt456',
          employee_id: '000002',
          account_status: 'ACTIVE',
          last_login_at: new Date('2025-06-01T10:30:00Z'),
          last_login_ip: '192.168.1.101',
          failed_login_count: 0,
          password_changed_at: new Date('2025-01-01T00:00:00Z'),
          password_expires_at: new Date('2025-12-31T23:59:59Z'),
          mfa_enabled: false,
          session_timeout: 480,
        },
      }),
    ])

    console.log('✅ 最小限のデータベース初期データ投入が完了しました！')
    console.log('📋 投入されたデータの詳細:')
    console.log('   - 社員: 2件')
    console.log('   - ユーザー認証: 3件')
    console.log('')
    console.log('🔐 ログイン情報:')
    console.log('   テストユーザー（推奨）:')
    console.log('     ユーザーID: test-employee')
    console.log('     パスワード: password')
    console.log('   テストユーザー1:')
    console.log('     ユーザーID: 000001')
    console.log('     パスワード: password')
    console.log('   テストユーザー2:')
    console.log('     ユーザーID: 000002')
    console.log('     パスワード: password')

  } catch (error) {
    console.error('❌ 最小限初期データ投入中にエラーが発生しました:', error)
    throw error
  }
}

if (require.main === module) {
  runMinimalSeed()
    .then(async () => {
      await prisma.$disconnect()
    })
    .catch(async (e) => {
      console.error('❌ 最小限初期データ投入中にエラーが発生しました:', e)
      await prisma.$disconnect()
      throw e
    })
}