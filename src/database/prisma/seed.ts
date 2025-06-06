// 要求仕様ID: PLT.1-DB.1 - データベース初期データ投入
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function main() {
  console.log('🌱 データベースの初期データ投入を開始します...')

  // 1. テナントマスターデータ
  console.log('🏢 テナントマスターデータを投入中...')
  const tenant = await prisma.tenant.upsert({
    where: { tenant_id: 'TENANT001' },
    update: {},
    create: {
      tenant_id: 'TENANT001',
      tenant_code: 'DEFAULT',
      tenant_name: 'デフォルトテナント',
      tenant_short_name: 'DEFAULT',
      tenant_type: 'ENTERPRISE',
      domain_name: 'skill-report.local',
      subdomain: 'default',
      timezone: 'Asia/Tokyo',
      locale: 'ja-JP',
      currency_code: 'JPY',
      status: 'ACTIVE',
      max_users: 1000,
      code: 'TENANT001',
      name: 'デフォルトテナント',
    },
  })

  // 2. 部署マスターデータ
  console.log('📁 部署マスターデータを投入中...')
  const departments = await Promise.all([
    prisma.department.upsert({
      where: { department_code: 'DEPT001' },
      update: {},
      create: {
        department_code: 'DEPT001',
        department_name: '開発部',
        parent_department_id: null,
        department_level: 1,
        sort_order: 1,
        code: 'DEPT001',
        name: '開発部',
      },
    }),
    prisma.department.upsert({
      where: { department_code: 'DEPT002' },
      update: {},
      create: {
        department_code: 'DEPT002',
        department_name: '営業部',
        parent_department_id: null,
        department_level: 1,
        sort_order: 2,
        code: 'DEPT002',
        name: '営業部',
      },
    }),
    prisma.department.upsert({
      where: { department_code: 'DEPT003' },
      update: {},
      create: {
        department_code: 'DEPT003',
        department_name: '管理部',
        parent_department_id: null,
        department_level: 1,
        sort_order: 3,
        code: 'DEPT003',
        name: '管理部',
      },
    }),
  ])

  // 3. 役職マスターデータ
  console.log('👔 役職マスターデータを投入中...')
  const positions = await Promise.all([
    prisma.position.upsert({
      where: { position_code: 'POS001' },
      update: {},
      create: {
        position_code: 'POS001',
        position_name: '部長',
        position_level: 4,
        sort_order: 1,
        code: 'POS001',
        name: '部長',
      },
    }),
    prisma.position.upsert({
      where: { position_code: 'POS002' },
      update: {},
      create: {
        position_code: 'POS002',
        position_name: '課長',
        position_level: 3,
        sort_order: 2,
        code: 'POS002',
        name: '課長',
      },
    }),
    prisma.position.upsert({
      where: { position_code: 'POS003' },
      update: {},
      create: {
        position_code: 'POS003',
        position_name: '主任',
        position_level: 2,
        sort_order: 3,
        code: 'POS003',
        name: '主任',
      },
    }),
    prisma.position.upsert({
      where: { position_code: 'POS004' },
      update: {},
      create: {
        position_code: 'POS004',
        position_name: '一般',
        position_level: 1,
        sort_order: 4,
        code: 'POS004',
        name: '一般',
      },
    }),
  ])

  // 4. 権限マスターデータ
  console.log('🔐 権限マスターデータを投入中...')
  const roles = await Promise.all([
    prisma.role.upsert({
      where: { role_code: 'ROLE001' },
      update: {},
      create: {
        role_code: 'ROLE001',
        role_name: 'システム管理者',
        role_category: 'ADMIN',
        role_level: 5,
        is_system_role: true,
        role_status: 'ACTIVE',
        code: 'ROLE001',
        name: 'システム管理者',
        description: 'システム全体の管理権限',
      },
    }),
    prisma.role.upsert({
      where: { role_code: 'ROLE002' },
      update: {},
      create: {
        role_code: 'ROLE002',
        role_name: '部門管理者',
        role_category: 'MANAGER',
        role_level: 3,
        is_system_role: false,
        role_status: 'ACTIVE',
        code: 'ROLE002',
        name: '部門管理者',
        description: '部門内のデータ管理権限',
      },
    }),
    prisma.role.upsert({
      where: { role_code: 'ROLE003' },
      update: {},
      create: {
        role_code: 'ROLE003',
        role_name: '一般ユーザー',
        role_category: 'USER',
        role_level: 1,
        is_system_role: false,
        role_status: 'ACTIVE',
        code: 'ROLE003',
        name: '一般ユーザー',
        description: '自分のデータのみ編集可能',
      },
    }),
  ])

  // 5. 権限設定データ
  console.log('🔑 権限設定データを投入中...')
  const permissions = await Promise.all([
    prisma.permission.upsert({
      where: { permission_code: 'PERM001' },
      update: {},
      create: {
        permission_code: 'PERM001',
        permission_name: 'ユーザー情報閲覧',
        permission_category: 'USER',
        resource_type: 'USER',
        action_type: 'READ',
        scope_level: 'ALL',
        permission_status: 'ACTIVE',
        code: 'PERM001',
        name: 'ユーザー情報閲覧',
        description: 'ユーザー情報の閲覧権限',
      },
    }),
    prisma.permission.upsert({
      where: { permission_code: 'PERM002' },
      update: {},
      create: {
        permission_code: 'PERM002',
        permission_name: 'ユーザー情報編集',
        permission_category: 'USER',
        resource_type: 'USER',
        action_type: 'WRITE',
        scope_level: 'SELF',
        permission_status: 'ACTIVE',
        code: 'PERM002',
        name: 'ユーザー情報編集',
        description: 'ユーザー情報の編集権限',
      },
    }),
    prisma.permission.upsert({
      where: { permission_code: 'PERM003' },
      update: {},
      create: {
        permission_code: 'PERM003',
        permission_name: 'スキル情報閲覧',
        permission_category: 'SKILL',
        resource_type: 'SKILL',
        action_type: 'READ',
        scope_level: 'ALL',
        permission_status: 'ACTIVE',
        code: 'PERM003',
        name: 'スキル情報閲覧',
        description: 'スキル情報の閲覧権限',
      },
    }),
    prisma.permission.upsert({
      where: { permission_code: 'PERM004' },
      update: {},
      create: {
        permission_code: 'PERM004',
        permission_name: 'スキル情報編集',
        permission_category: 'SKILL',
        resource_type: 'SKILL',
        action_type: 'WRITE',
        scope_level: 'SELF',
        permission_status: 'ACTIVE',
        code: 'PERM004',
        name: 'スキル情報編集',
        description: 'スキル情報の編集権限',
      },
    }),
    prisma.permission.upsert({
      where: { permission_code: 'PERM005' },
      update: {},
      create: {
        permission_code: 'PERM005',
        permission_name: '管理者権限',
        permission_category: 'ADMIN',
        resource_type: 'SYSTEM',
        action_type: 'ALL',
        scope_level: 'ALL',
        permission_status: 'ACTIVE',
        code: 'PERM005',
        name: '管理者権限',
        description: '管理者権限（全操作）',
      },
    }),
  ])

  // 6. スキルカテゴリマスターデータ
  console.log('🎯 スキルカテゴリマスターデータを投入中...')
  const skillCategories = await Promise.all([
    prisma.skillCategory.upsert({
      where: { category_code: 'CAT001' },
      update: {},
      create: {
        category_code: 'CAT001',
        category_name: 'フロントエンド',
        category_type: 'TECHNICAL',
        parent_category_id: null,
        category_level: 1,
        display_order: 1,
        category_status: 'ACTIVE',
        code: 'CAT001',
        name: 'フロントエンド',
      },
    }),
    prisma.skillCategory.upsert({
      where: { category_code: 'CAT002' },
      update: {},
      create: {
        category_code: 'CAT002',
        category_name: 'バックエンド',
        category_type: 'TECHNICAL',
        parent_category_id: null,
        category_level: 1,
        display_order: 2,
        category_status: 'ACTIVE',
        code: 'CAT002',
        name: 'バックエンド',
      },
    }),
    prisma.skillCategory.upsert({
      where: { category_code: 'CAT003' },
      update: {},
      create: {
        category_code: 'CAT003',
        category_name: 'インフラ',
        category_type: 'TECHNICAL',
        parent_category_id: null,
        category_level: 1,
        display_order: 3,
        category_status: 'ACTIVE',
        code: 'CAT003',
        name: 'インフラ',
      },
    }),
    prisma.skillCategory.upsert({
      where: { category_code: 'CAT004' },
      update: {},
      create: {
        category_code: 'CAT004',
        category_name: 'マネジメント',
        category_type: 'BUSINESS',
        parent_category_id: null,
        category_level: 1,
        display_order: 4,
        category_status: 'ACTIVE',
        code: 'CAT004',
        name: 'マネジメント',
      },
    }),
  ])

  // 7. スキルマスターデータ
  console.log('⚡ スキルマスターデータを投入中...')
  const skills = await Promise.all([
    // フロントエンドスキル
    prisma.skillItem.upsert({
      where: { skill_code: 'SKL001' },
      update: {},
      create: {
        skill_code: 'SKL001',
        skill_name: 'React.js',
        skill_category_id: skillCategories[0].category_code,
        skill_type: 'FRAMEWORK',
        difficulty_level: 3,
        importance_level: 5,
        code: 'SKL001',
        name: 'React.js',
        description: 'Reactライブラリを使用したフロントエンド開発',
      },
    }),
    prisma.skillItem.upsert({
      where: { skill_code: 'SKL002' },
      update: {},
      create: {
        skill_code: 'SKL002',
        skill_name: 'Next.js',
        skill_category_id: skillCategories[0].category_code,
        skill_type: 'FRAMEWORK',
        difficulty_level: 4,
        importance_level: 5,
        code: 'SKL002',
        name: 'Next.js',
        description: 'Next.jsフレームワークを使用したフルスタック開発',
      },
    }),
    prisma.skillItem.upsert({
      where: { skill_code: 'SKL003' },
      update: {},
      create: {
        skill_code: 'SKL003',
        skill_name: 'TypeScript',
        skill_category_id: skillCategories[0].category_code,
        skill_type: 'LANGUAGE',
        difficulty_level: 3,
        importance_level: 4,
        code: 'SKL003',
        name: 'TypeScript',
        description: 'TypeScriptを使用した型安全な開発',
      },
    }),
    // バックエンドスキル
    prisma.skillItem.upsert({
      where: { skill_code: 'SKL004' },
      update: {},
      create: {
        skill_code: 'SKL004',
        skill_name: 'Node.js',
        skill_category_id: skillCategories[1].category_code,
        skill_type: 'RUNTIME',
        difficulty_level: 3,
        importance_level: 4,
        code: 'SKL004',
        name: 'Node.js',
        description: 'Node.jsを使用したサーバーサイド開発',
      },
    }),
    prisma.skillItem.upsert({
      where: { skill_code: 'SKL005' },
      update: {},
      create: {
        skill_code: 'SKL005',
        skill_name: 'PostgreSQL',
        skill_category_id: skillCategories[1].category_code,
        skill_type: 'DATABASE',
        difficulty_level: 3,
        importance_level: 4,
        code: 'SKL005',
        name: 'PostgreSQL',
        description: 'PostgreSQLデータベースの設計・運用',
      },
    }),
    // インフラスキル
    prisma.skillItem.upsert({
      where: { skill_code: 'SKL006' },
      update: {},
      create: {
        skill_code: 'SKL006',
        skill_name: 'Docker',
        skill_category_id: skillCategories[2].category_code,
        skill_type: 'TOOL',
        difficulty_level: 3,
        importance_level: 3,
        code: 'SKL006',
        name: 'Docker',
        description: 'Dockerを使用したコンテナ化技術',
      },
    }),
    prisma.skillItem.upsert({
      where: { skill_code: 'SKL007' },
      update: {},
      create: {
        skill_code: 'SKL007',
        skill_name: 'Vercel',
        skill_category_id: skillCategories[2].category_code,
        skill_type: 'PLATFORM',
        difficulty_level: 2,
        importance_level: 3,
        code: 'SKL007',
        name: 'Vercel',
        description: 'Vercelを使用したデプロイメント',
      },
    }),
  ])

  // 8. 従業員マスターデータ
  console.log('👤 従業員マスターデータを投入中...')
  const employees = await Promise.all([
    // 管理者ユーザー
    prisma.employee.upsert({
      where: { employee_code: 'ADMIN001' },
      update: {},
      create: {
        employee_code: 'ADMIN001',
        full_name: 'システム管理者',
        full_name_kana: 'システムカンリシャ',
        email: 'admin@skill-report.local',
        hire_date: new Date('2025-01-01'),
        department_id: departments[0].department_code,
        position_id: positions[0].position_code,
        employment_status: 'ACTIVE',
        employee_status: 'ACTIVE',
        code: 'ADMIN001',
        name: 'システム管理者',
      },
    }),
    // テストユーザー
    prisma.employee.upsert({
      where: { employee_code: 'TEST001' },
      update: {},
      create: {
        employee_code: 'TEST001',
        full_name: 'テスト太郎',
        full_name_kana: 'テストタロウ',
        email: 'test@skill-report.local',
        hire_date: new Date('2025-04-01'),
        department_id: departments[0].department_code,
        position_id: positions[3].position_code,
        employment_status: 'ACTIVE',
        employee_status: 'ACTIVE',
        code: 'TEST001',
        name: 'テスト太郎',
      },
    }),
  ])

  // 9. 認証情報の作成
  console.log('🔐 認証情報を作成中...')
  const userAuths = await Promise.all([
    // 管理者の認証情報
    prisma.userAuth.upsert({
      where: { user_id: employees[0].employee_code },
      update: {},
      create: {
        user_id: employees[0].employee_code,
        login_id: 'admin@skill-report.local',
        password_hash: '$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
        employee_id: employees[0].employee_code,
        account_status: 'ACTIVE',
        failed_login_count: 0,
        mfa_enabled: false,
        code: 'AUTH001',
        name: 'システム管理者認証',
      },
    }),
    // テストユーザーの認証情報
    prisma.userAuth.upsert({
      where: { user_id: employees[1].employee_code },
      update: {},
      create: {
        user_id: employees[1].employee_code,
        login_id: 'test@skill-report.local',
        password_hash: '$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
        employee_id: employees[1].employee_code,
        account_status: 'ACTIVE',
        failed_login_count: 0,
        mfa_enabled: false,
        code: 'AUTH002',
        name: 'テストユーザー認証',
      },
    }),
  ])

  console.log('✅ データベースの初期データ投入が完了しました！')
  console.log('📋 投入されたデータ:')
  console.log(`   - テナント: 1件`)
  console.log(`   - 部署: ${departments.length}件`)
  console.log(`   - 役職: ${positions.length}件`)
  console.log(`   - 権限: ${roles.length}件`)
  console.log(`   - 権限設定: ${permissions.length}件`)
  console.log(`   - スキルカテゴリ: ${skillCategories.length}件`)
  console.log(`   - スキル: ${skills.length}件`)
  console.log(`   - 従業員: ${employees.length}件`)
  console.log(`   - 認証情報: ${userAuths.length}件`)
  console.log('')
  console.log('🔐 ログイン情報:')
  console.log('   管理者:')
  console.log('     ユーザーID: admin@skill-report.local')
  console.log('     パスワード: password')
  console.log('   テストユーザー:')
  console.log('     ユーザーID: test@skill-report.local')
  console.log('     パスワード: password')
}

main()
  .then(async () => {
    await prisma.$disconnect()
  })
  .catch(async (e) => {
    console.error('❌ 初期データ投入中にエラーが発生しました:', e)
    await prisma.$disconnect()
    throw e
  })
