// 要求仕様ID: PLT.1-DB.1 - データベース初期データ投入
import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()

async function main() {
  console.log('🌱 データベースの初期データ投入を開始します...')

  // 1. 部署マスターデータ
  console.log('📁 部署マスターデータを投入中...')
  const departments = await Promise.all([
    prisma.department.upsert({
      where: { code: 'DEPT001' },
      update: {},
      create: {
        code: 'DEPT001',
        name: '開発部',
        parentId: null,
        level: 1,
        sortOrder: 1,
        isActive: true,
      },
    }),
    prisma.department.upsert({
      where: { code: 'DEPT002' },
      update: {},
      create: {
        code: 'DEPT002',
        name: '営業部',
        parentId: null,
        level: 1,
        sortOrder: 2,
        isActive: true,
      },
    }),
    prisma.department.upsert({
      where: { code: 'DEPT003' },
      update: {},
      create: {
        code: 'DEPT003',
        name: '管理部',
        parentId: null,
        level: 1,
        sortOrder: 3,
        isActive: true,
      },
    }),
  ])

  // 2. 役職マスターデータ
  console.log('👔 役職マスターデータを投入中...')
  const positions = await Promise.all([
    prisma.position.upsert({
      where: { code: 'POS001' },
      update: {},
      create: {
        code: 'POS001',
        name: '部長',
        level: 4,
        sortOrder: 1,
        isActive: true,
      },
    }),
    prisma.position.upsert({
      where: { code: 'POS002' },
      update: {},
      create: {
        code: 'POS002',
        name: '課長',
        level: 3,
        sortOrder: 2,
        isActive: true,
      },
    }),
    prisma.position.upsert({
      where: { code: 'POS003' },
      update: {},
      create: {
        code: 'POS003',
        name: '主任',
        level: 2,
        sortOrder: 3,
        isActive: true,
      },
    }),
    prisma.position.upsert({
      where: { code: 'POS004' },
      update: {},
      create: {
        code: 'POS004',
        name: '一般',
        level: 1,
        sortOrder: 4,
        isActive: true,
      },
    }),
  ])

  // 3. 権限マスターデータ
  console.log('🔐 権限マスターデータを投入中...')
  const roles = await Promise.all([
    prisma.role.upsert({
      where: { name: 'システム管理者' },
      update: {},
      create: {
        name: 'システム管理者',
        description: 'システム全体の管理権限',
        isActive: true,
      },
    }),
    prisma.role.upsert({
      where: { name: '部門管理者' },
      update: {},
      create: {
        name: '部門管理者',
        description: '部門内のデータ管理権限',
        isActive: true,
      },
    }),
    prisma.role.upsert({
      where: { name: '一般ユーザー' },
      update: {},
      create: {
        name: '一般ユーザー',
        description: '自分のデータのみ編集可能',
        isActive: true,
      },
    }),
  ])

  // 4. 権限設定データ
  console.log('🔑 権限設定データを投入中...')
  const permissions = await Promise.all([
    prisma.permission.upsert({
      where: { name: 'user:read' },
      update: {},
      create: {
        name: 'user:read',
        description: 'ユーザー情報の閲覧',
        resource: 'user',
        action: 'read',
      },
    }),
    prisma.permission.upsert({
      where: { name: 'user:write' },
      update: {},
      create: {
        name: 'user:write',
        description: 'ユーザー情報の編集',
        resource: 'user',
        action: 'write',
      },
    }),
    prisma.permission.upsert({
      where: { name: 'skill:read' },
      update: {},
      create: {
        name: 'skill:read',
        description: 'スキル情報の閲覧',
        resource: 'skill',
        action: 'read',
      },
    }),
    prisma.permission.upsert({
      where: { name: 'skill:write' },
      update: {},
      create: {
        name: 'skill:write',
        description: 'スキル情報の編集',
        resource: 'skill',
        action: 'write',
      },
    }),
    prisma.permission.upsert({
      where: { name: 'admin:all' },
      update: {},
      create: {
        name: 'admin:all',
        description: '管理者権限（全操作）',
        resource: 'admin',
        action: 'all',
      },
    }),
  ])

  // 5. スキルカテゴリマスターデータ
  console.log('🎯 スキルカテゴリマスターデータを投入中...')
  const skillCategories = await Promise.all([
    prisma.skillCategory.upsert({
      where: { code: 'CAT001' },
      update: {},
      create: {
        code: 'CAT001',
        name: 'フロントエンド',
        parentId: null,
        level: 1,
        sortOrder: 1,
        isActive: true,
      },
    }),
    prisma.skillCategory.upsert({
      where: { code: 'CAT002' },
      update: {},
      create: {
        code: 'CAT002',
        name: 'バックエンド',
        parentId: null,
        level: 1,
        sortOrder: 2,
        isActive: true,
      },
    }),
    prisma.skillCategory.upsert({
      where: { code: 'CAT003' },
      update: {},
      create: {
        code: 'CAT003',
        name: 'インフラ',
        parentId: null,
        level: 1,
        sortOrder: 3,
        isActive: true,
      },
    }),
    prisma.skillCategory.upsert({
      where: { code: 'CAT004' },
      update: {},
      create: {
        code: 'CAT004',
        name: 'マネジメント',
        parentId: null,
        level: 1,
        sortOrder: 4,
        isActive: true,
      },
    }),
  ])

  // 6. スキルマスターデータ
  console.log('⚡ スキルマスターデータを投入中...')
  const skills = await Promise.all([
    // フロントエンドスキル
    prisma.skillMaster.upsert({
      where: { code: 'SKL001' },
      update: {},
      create: {
        code: 'SKL001',
        name: 'React.js',
        categoryId: skillCategories[0].id,
        description: 'Reactライブラリを使用したフロントエンド開発',
        level: 1,
        sortOrder: 1,
        isActive: true,
      },
    }),
    prisma.skillMaster.upsert({
      where: { code: 'SKL002' },
      update: {},
      create: {
        code: 'SKL002',
        name: 'Next.js',
        categoryId: skillCategories[0].id,
        description: 'Next.jsフレームワークを使用したフルスタック開発',
        level: 1,
        sortOrder: 2,
        isActive: true,
      },
    }),
    prisma.skillMaster.upsert({
      where: { code: 'SKL003' },
      update: {},
      create: {
        code: 'SKL003',
        name: 'TypeScript',
        categoryId: skillCategories[0].id,
        description: 'TypeScriptを使用した型安全な開発',
        level: 1,
        sortOrder: 3,
        isActive: true,
      },
    }),
    // バックエンドスキル
    prisma.skillMaster.upsert({
      where: { code: 'SKL004' },
      update: {},
      create: {
        code: 'SKL004',
        name: 'Node.js',
        categoryId: skillCategories[1].id,
        description: 'Node.jsを使用したサーバーサイド開発',
        level: 1,
        sortOrder: 1,
        isActive: true,
      },
    }),
    prisma.skillMaster.upsert({
      where: { code: 'SKL005' },
      update: {},
      create: {
        code: 'SKL005',
        name: 'PostgreSQL',
        categoryId: skillCategories[1].id,
        description: 'PostgreSQLデータベースの設計・運用',
        level: 1,
        sortOrder: 2,
        isActive: true,
      },
    }),
    // インフラスキル
    prisma.skillMaster.upsert({
      where: { code: 'SKL006' },
      update: {},
      create: {
        code: 'SKL006',
        name: 'Docker',
        categoryId: skillCategories[2].id,
        description: 'Dockerを使用したコンテナ化技術',
        level: 1,
        sortOrder: 1,
        isActive: true,
      },
    }),
    prisma.skillMaster.upsert({
      where: { code: 'SKL007' },
      update: {},
      create: {
        code: 'SKL007',
        name: 'Vercel',
        categoryId: skillCategories[2].id,
        description: 'Vercelを使用したデプロイメント',
        level: 1,
        sortOrder: 2,
        isActive: true,
      },
    }),
  ])

  // 7. 管理者ユーザーの作成
  console.log('👤 管理者ユーザーを作成中...')
  
  const adminUser = await prisma.user.upsert({
    where: { empNo: 'ADMIN001' },
    update: {},
    create: {
      empNo: 'ADMIN001',
      email: 'admin@skill-report.local',
      name: 'システム管理者',
      nameKana: 'システムカンリシャ',
      deptId: departments[0].id,
      positionId: positions[0].id,
      joinDate: new Date('2025-01-01'),
      isActive: true,
    },
  })

  // 管理者の認証情報を作成
  const adminPasswordHash = await bcrypt.hash('admin123', 10)
  await prisma.userAuth.upsert({
    where: { userId: adminUser.id },
    update: {},
    create: {
      userId: adminUser.id,
      passwordHash: adminPasswordHash,
      lastLoginAt: null,
      loginFailureCount: 0,
      isLocked: false,
    },
  })

  // 8. 管理者の権限設定
  console.log('🔑 管理者権限を設定中...')
  await prisma.userRole.upsert({
    where: {
      userId_roleId: {
        userId: adminUser.id,
        roleId: roles[0].id,
      },
    },
    update: {},
    create: {
      userId: adminUser.id,
      roleId: roles[0].id,
    },
  })

  // 9. テストユーザーの作成
  console.log('🧪 テストユーザーを作成中...')
  
  const testUser = await prisma.user.upsert({
    where: { empNo: 'TEST001' },
    update: {},
    create: {
      empNo: 'TEST001',
      email: 'test@skill-report.local',
      name: 'テスト太郎',
      nameKana: 'テストタロウ',
      deptId: departments[0].id,
      positionId: positions[3].id,
      joinDate: new Date('2025-04-01'),
      isActive: true,
    },
  })

  // テストユーザーの認証情報を作成
  const testPasswordHash = await bcrypt.hash('test123', 10)
  await prisma.userAuth.upsert({
    where: { userId: testUser.id },
    update: {},
    create: {
      userId: testUser.id,
      passwordHash: testPasswordHash,
      lastLoginAt: null,
      loginFailureCount: 0,
      isLocked: false,
    },
  })

  // 10. テストユーザーの権限設定
  await prisma.userRole.upsert({
    where: {
      userId_roleId: {
        userId: testUser.id,
        roleId: roles[2].id,
      },
    },
    update: {},
    create: {
      userId: testUser.id,
      roleId: roles[2].id,
    },
  })

  // 11. ロール権限の設定
  await Promise.all([
    // システム管理者権限
    prisma.rolePermission.upsert({
      where: {
        roleId_permissionId: {
          roleId: roles[0].id,
          permissionId: permissions[4].id, // admin:all
        },
      },
      update: {},
      create: {
        roleId: roles[0].id,
        permissionId: permissions[4].id,
      },
    }),
    // 一般ユーザー権限
    prisma.rolePermission.upsert({
      where: {
        roleId_permissionId: {
          roleId: roles[2].id,
          permissionId: permissions[0].id, // user:read
        },
      },
      update: {},
      create: {
        roleId: roles[2].id,
        permissionId: permissions[0].id,
      },
    }),
    prisma.rolePermission.upsert({
      where: {
        roleId_permissionId: {
          roleId: roles[2].id,
          permissionId: permissions[2].id, // skill:read
        },
      },
      update: {},
      create: {
        roleId: roles[2].id,
        permissionId: permissions[2].id,
      },
    }),
  ])

  // 12. テストユーザーのサンプルスキルデータ
  console.log('📊 サンプルスキルデータを投入中...')
  await Promise.all([
    prisma.userSkill.upsert({
      where: {
        userId_skillId: {
          userId: testUser.id,
          skillId: skills[0].id, // React.js
        },
      },
      update: {},
      create: {
        userId: testUser.id,
        skillId: skills[0].id,
        level: 3,
        acquiredDate: new Date('2024-01-01'),
        note: 'プロジェクトで実際に使用',
      },
    }),
    prisma.userSkill.upsert({
      where: {
        userId_skillId: {
          userId: testUser.id,
          skillId: skills[2].id, // TypeScript
        },
      },
      update: {},
      create: {
        userId: testUser.id,
        skillId: skills[2].id,
        level: 2,
        acquiredDate: new Date('2024-06-01'),
        note: '基本的な型定義ができる',
      },
    }),
  ])

  console.log('✅ データベースの初期データ投入が完了しました！')
  console.log('📋 投入されたデータ:')
  console.log(`   - 部署: ${departments.length}件`)
  console.log(`   - 役職: ${positions.length}件`)
  console.log(`   - 権限: ${roles.length}件`)
  console.log(`   - 権限設定: ${permissions.length}件`)
  console.log(`   - スキルカテゴリ: ${skillCategories.length}件`)
  console.log(`   - スキル: ${skills.length}件`)
  console.log(`   - ユーザー: 2件（管理者・テストユーザー）`)
  console.log('')
  console.log('🔐 ログイン情報:')
  console.log('   管理者:')
  console.log('     ユーザーID: admin@skill-report.local')
  console.log('     パスワード: admin123')
  console.log('   テストユーザー:')
  console.log('     ユーザーID: test@skill-report.local')
  console.log('     パスワード: test123')
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
