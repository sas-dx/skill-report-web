// @ts-nocheck
// 要求仕様ID: PLT.1-DB.1 - データベース初期データ投入
// 設計書: docs/design/database/data/ 配下のサンプルデータSQLファイル群
// 自動生成日時: 2025-06-09 11:20:00
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

export async function runSampleSeed() {
  console.log('🌱 データベースの初期データ投入を開始します...')

  try {
    // MST_Tenantデータ
    console.log('📊 MST_Tenantデータを投入中...')
    const tenantData = await Promise.all([
      prisma.tenant.upsert({
        where: { tenant_id: 'TENANT_001' },
        update: {},
        create: {
          tenant_id: 'TENANT_001',
          tenant_code: 'acme-corp',
          tenant_name: '株式会社ACME',
          tenant_name_en: 'ACME Corporation',
          tenant_short_name: 'ACME',
          tenant_type: 'ENTERPRISE',
          tenant_level: 1,
          domain_name: 'acme-corp.com',
          subdomain: 'acme',
          logo_url: 'https://cdn.example.com/logos/acme-corp.png',
          primary_color: '#0066CC',
          secondary_color: '#FF6600',
          timezone: 'Asia/Tokyo',
          locale: 'ja_JP',
          currency_code: 'JPY',
          date_format: 'YYYY-MM-DD',
          time_format: 'HH:mm:ss',
          admin_email: 'admin@acme-corp.com',
          contact_email: 'contact@acme-corp.com',
          phone_number: '03-1234-5678',
          address: '東京都千代田区丸の内1-1-1',
          postal_code: '100-0005',
          country_code: 'JP',
          subscription_plan: 'ENTERPRISE',
          max_users: 1000,
          max_storage_gb: 1000,
          features_enabled: '["advanced_analytics", "custom_reports", "api_access", "sso", "audit_logs"]',
          custom_settings: '{"theme": "corporate", "dashboard_layout": "advanced", "notification_preferences": {"email": true, "slack": true}}',
          security_policy: '{"password_policy": {"min_length": 8, "require_special_chars": true}, "session_timeout": 480, "ip_whitelist": ["192.168.1.0/24"]}',
          data_retention_days: 2555,
          backup_enabled: true,
          backup_frequency: 'DAILY',
          contract_start_date: new Date('2024-01-01'),
          contract_end_date: new Date('2024-12-31'),
          billing_cycle: 'ANNUAL',
          monthly_fee: 50000.0,
          setup_fee: 100000.0,
          status: 'ACTIVE',
          activation_date: new Date('2024-01-01'),
          last_login_date: new Date('2024-06-01'),
          current_users_count: 250,
          storage_used_gb: 125.5,
          api_rate_limit: 10000,
          sso_enabled: true,
          sso_provider: 'SAML',
          sso_config: '{"entity_id": "acme-corp", "sso_url": "https://sso.acme-corp.com/saml", "certificate": "..."}',
          webhook_url: 'https://api.acme-corp.com/webhooks/skill-system',
          webhook_secret: 'webhook_secret_key_123',
          created_by: 'SYSTEM',
          notes: '大手企業向けエンタープライズプラン',
          code: 'TENANT_001',
          name: '株式会社ACME',
          description: '大手企業向けエンタープライズプラン',
        },
      }),
    ])

    // MST_Departmentデータ
    console.log('📊 MST_Departmentデータを投入中...')
    const departmentData = await Promise.all([
      prisma.department.upsert({
        where: { department_code: 'DEPT001' },
        update: {},
        create: {
          department_code: 'DEPT001',
          department_name: '経営企画本部',
          department_name_short: '経営企画',
          department_level: 1,
          department_type: 'HEADQUARTERS',
          manager_id: '000001',
          cost_center_code: 'CC001',
          budget_amount: 50000000.0,
          location: '本社ビル 10F',
          phone_number: '03-1234-5678',
          email_address: 'planning@company.com',
          establishment_date: new Date('2020-04-01'),
          department_status: 'ACTIVE',
          sort_order: 1,
          description: '会社全体の経営戦略立案・推進を担当',
          code: 'DEPT001',
          name: '経営企画本部',
        },
      }),
    ])

    // MST_Positionデータ
    console.log('📊 MST_Positionデータを投入中...')
    const positionData = await Promise.all([
      prisma.position.upsert({
        where: { position_code: 'POS001' },
        update: {},
        create: {
          position_code: 'POS001',
          position_name: '代表取締役社長',
          position_name_short: '社長',
          position_level: 1,
          position_rank: 1,
          position_category: 'EXECUTIVE',
          authority_level: 10,
          approval_limit: 999999999.99,
          salary_grade: 'E1',
          allowance_amount: 500000.0,
          is_management: true,
          is_executive: true,
          requires_approval: true,
          can_hire: true,
          can_evaluate: true,
          position_status: 'ACTIVE',
          sort_order: 1,
          description: '会社の最高責任者として経営全般を統括',
          code: 'POS001',
          name: '代表取締役社長',
        },
      }),
    ])

    // MST_JobTypeデータ
    console.log('📊 MST_JobTypeデータを投入中...')
    const jobTypeData = await Promise.all([
      prisma.jobType.upsert({
        where: { job_type_code: 'SE' },
        update: {},
        create: {
          job_type_code: 'SE',
          job_type_name: 'システムエンジニア',
          job_type_name_en: 'Systems Engineer',
          job_category: 'ENGINEERING',
          job_level: 'SENIOR',
          description: 'システムの設計・開発・テストを担当するエンジニア',
          required_experience_years: 3,
          salary_grade_min: 3,
          salary_grade_max: 6,
          career_path: 'SE → シニアSE → テックリード → エンジニアリングマネージャー',
          required_certifications: '["基本情報技術者", "応用情報技術者"]',
          required_skills: '["Java", "SQL", "システム設計", "要件定義"]',
          department_affinity: '["開発部", "システム部"]',
          remote_work_eligible: true,
          travel_frequency: 'LOW',
          sort_order: 1,
          is_active: true,
          code: 'SE',
          name: 'システムエンジニア',
        },
      }),
    ])

    // MST_Roleデータ
    console.log('📊 MST_Roleデータを投入中...')
    const roleData = await Promise.all([
      prisma.role.upsert({
        where: { role_code: 'ROLE001' },
        update: {},
        create: {
          role_code: 'ROLE001',
          role_name: 'システム管理者',
          role_name_short: 'システム管理者',
          role_category: 'SYSTEM',
          role_level: 1,
          is_system_role: true,
          is_tenant_specific: false,
          max_users: 5,
          role_priority: 1,
          role_status: 'ACTIVE',
          effective_from: new Date('2025-01-01'),
          sort_order: 1,
          description: 'システム全体の管理権限を持つ最上位ロール',
          code: 'ROLE001',
          name: 'システム管理者',
        },
      }),
    ])

    // MST_Permissionデータ
    console.log('📊 MST_Permissionデータを投入中...')
    const permissionData = await Promise.all([
      prisma.permission.upsert({
        where: { permission_code: 'PERM_USER_READ' },
        update: {},
        create: {
          permission_code: 'PERM_USER_READ',
          permission_name: 'ユーザー情報参照',
          permission_name_short: 'ユーザー参照',
          permission_category: 'DATA',
          resource_type: 'USER',
          action_type: 'READ',
          scope_level: 'TENANT',
          is_system_permission: true,
          requires_conditions: false,
          risk_level: 1,
          requires_approval: false,
          audit_required: true,
          permission_status: 'ACTIVE',
          effective_from: new Date('2025-01-01'),
          sort_order: 1,
          description: 'ユーザー情報の参照権限',
          code: 'PERM_USER_READ',
          name: 'ユーザー情報参照',
        },
      }),
    ])

    // MST_SkillCategoryデータ
    console.log('📊 MST_SkillCategoryデータを投入中...')
    const skillCategoryData = await Promise.all([
      prisma.skillCategory.upsert({
        where: { category_code: 'CAT001' },
        update: {},
        create: {
          category_code: 'CAT001',
          category_name: 'プログラミング言語',
          category_name_short: 'プログラミング',
          category_name_en: 'Programming Languages',
          category_type: 'TECHNICAL',
          category_level: 1,
          category_path: '/プログラミング言語',
          is_system_category: true,
          is_leaf_category: false,
          skill_count: 25,
          evaluation_method: 'LEVEL',
          max_level: 5,
          icon_url: '/icons/programming.svg',
          color_code: '#007ACC',
          display_order: 1,
          is_popular: true,
          category_status: 'ACTIVE',
          effective_from: new Date('2025-01-01'),
          description: '各種プログラミング言語のスキル',
          code: 'CAT001',
          name: 'プログラミング言語',
        },
      }),
    ])

    // MST_SkillItemデータ
    console.log('📊 MST_SkillItemデータを投入中...')
    const skillItemData = await Promise.all([
      prisma.skillItem.upsert({
        where: { skill_code: 'SKILL001' },
        update: {},
        create: {
          skill_code: 'SKILL001',
          skill_name: 'Java',
          skill_category_id: 'CAT001',
          skill_type: 'TECHNICAL',
          difficulty_level: 3,
          importance_level: 4,
          code: 'SKILL001',
          name: 'Java',
          description: 'Java言語のプログラミングスキル',
        },
      }),
    ])

    // MST_Employeeデータ
    console.log('📊 MST_Employeeデータを投入中...')
    const employeeData = await Promise.all([
      prisma.employee.upsert({
        where: { employee_code: '000001' },
        update: {},
        create: {
          employee_code: '000001',
          full_name: '山田太郎',
          full_name_kana: 'ヤマダタロウ',
          email: 'yamada.taro@company.com',
          phone: '090-1234-5678',
          hire_date: new Date('2020-04-01'),
          birth_date: new Date('1990-01-15'),
          gender: 'M',
          department_id: 'DEPT001',
          position_id: 'POS001',
          job_type_id: 'SE',
          employment_status: 'FULL_TIME',
          employee_status: 'ACTIVE',
          code: '000001',
          name: '山田太郎',
          description: '経営企画本部所属の社員',
        },
      }),
    ])

    // MST_EmployeeDepartmentデータ
    console.log('📊 MST_EmployeeDepartmentデータを投入中...')
    const employeeDepartmentData = await Promise.all([
      prisma.employeeDepartment.upsert({
        where: { employee_id: '000001' },
        update: {},
        create: {
          employee_id: '000001',
          department_id: 'DEPT001',
          assignment_type: 'PRIMARY',
          start_date: new Date('2020-04-01'),
          assignment_ratio: 100.0,
          role_in_department: '部長',
          reporting_manager_id: '000001',
          assignment_reason: '新規採用時の配属',
          assignment_status: 'ACTIVE',
          approval_status: 'APPROVED',
          approved_by: 'SYSTEM',
          approved_at: new Date('2020-04-01'),
          code: 'EMP_DEPT_000001',
          name: '山田太郎の経営企画本部配属',
          description: '経営企画本部への主担当配属',
        },
      }),
    ])

    // MST_EmployeeJobTypeデータ
    console.log('📊 MST_EmployeeJobTypeデータを投入中...')
    const employeeJobTypeData = await Promise.all([
      prisma.employeeJobType.upsert({
        where: { employee_job_type_id: 'EMP_JOB_000001_SE' },
        update: {},
        create: {
          employee_job_type_id: 'EMP_JOB_000001_SE',
          employee_id: '000001',
          job_type_id: 'SE',
          assignment_type: 'PRIMARY',
          assignment_ratio: 100.0,
          effective_start_date: new Date('2020-04-01'),
          assignment_reason: '新規採用時の職種配属',
          assignment_status: 'ACTIVE',
          proficiency_level: 'SENIOR',
          target_proficiency_level: 'EXPERT',
          target_achievement_date: new Date('2025-12-31'),
          certification_requirements: '["基本情報技術者", "応用情報技術者"]',
          skill_requirements: '["Java", "SQL", "システム設計", "要件定義"]',
          experience_requirements: '3年以上のシステム開発経験',
          development_plan: 'シニアSEからテックリードへのキャリアパス',
          training_plan: '年間40時間の技術研修受講',
          mentor_id: '000001',
          supervisor_id: '000001',
          performance_rating: 'EXCELLENT',
          last_evaluation_date: new Date('2025-04-01'),
          next_evaluation_date: new Date('2025-10-01'),
          evaluation_frequency: 'SEMI_ANNUAL',
          career_path: 'SE → シニアSE → テックリード → エンジニアリングマネージャー',
          strengths: 'Java開発、システム設計、チームリーダーシップ',
          improvement_areas: 'クラウド技術、AI/ML技術',
          achievements: 'プロジェクト成功率95%、チーム生産性20%向上',
          goals: '新技術習得、後進育成、プロジェクト品質向上',
          workload_percentage: 100.0,
          billable_flag: true,
          cost_center: 'CC001',
          budget_allocation: 8000000.0,
          hourly_rate: 5000.0,
          overtime_eligible: true,
          remote_work_eligible: true,
          travel_required: false,
          security_clearance_required: false,
          created_by: 'SYSTEM',
          approved_by: 'SYSTEM',
          approval_date: new Date('2020-04-01'),
          notes: 'システムエンジニアとしての主担当職種',
          code: 'EMP_JOB_000001_SE',
          name: '山田太郎のSE職種配属',
          description: 'システムエンジニア職種への配属情報',
        },
      }),
    ])

    // MST_EmployeePositionデータ
    console.log('📊 MST_EmployeePositionデータを投入中...')
    const employeePositionData = await Promise.all([
      prisma.employeePosition.upsert({
        where: { employee_id: '000001' },
        update: {},
        create: {
          employee_id: '000001',
          position_id: 'POS001',
          appointment_type: 'PERMANENT',
          start_date: new Date('2020-04-01'),
          appointment_reason: '新規採用時の役職任命',
          responsibility_scope: '会社全体の経営戦略立案・推進・統括',
          authority_level: 10,
          salary_grade: 'E1',
          appointment_status: 'ACTIVE',
          approval_status: 'APPROVED',
          approved_by: 'BOARD_OF_DIRECTORS',
          approved_at: new Date('2020-04-01'),
          performance_target: '売上前年比110%、利益率15%以上',
          delegation_authority: '取締役会決議事項以外の全権限',
          code: 'EMP_POS_000001',
          name: '山田太郎の代表取締役社長任命',
          description: '代表取締役社長としての任命情報',
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
          password_hash: '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uIoS',
          password_salt: 'randomsalt123',
          employee_id: '000001',
          account_status: 'ACTIVE',
          last_login_at: new Date('2025-06-01 09:00:00'),
          last_login_ip: '192.168.1.100',
          failed_login_count: 0,
          password_changed_at: new Date('2025-01-01 00:00:00'),
          password_expires_at: new Date('2025-12-31 23:59:59'),
          mfa_enabled: true,
          mfa_secret: 'JBSWY3DPEHPK3PXP',
          session_timeout: 480,
          code: 'USER000001',
          name: '山田太郎アカウント',
          description: '山田太郎のユーザーアカウント',
        },
      }),
    ])

    // MST_UserRoleデータ
    console.log('📊 MST_UserRoleデータを投入中...')
    const userRoleData = await Promise.all([
      prisma.userRole.upsert({
        where: { user_id_role_id: { user_id: 'USER000001', role_id: 'ROLE001' } },
        update: {},
        create: {
          user_id: 'USER000001',
          role_id: 'ROLE001',
          assignment_type: 'DIRECT',
          assigned_by: 'SYSTEM',
          assignment_reason: '新規ユーザー登録時の標準ロール割り当て',
          effective_from: new Date('2025-01-01 00:00:00'),
          is_primary_role: true,
          priority_order: 1,
          auto_assigned: true,
          requires_approval: false,
          assignment_status: 'ACTIVE',
          last_used_at: new Date('2025-06-01 09:00:00'),
          usage_count: 150,
          code: 'USER000001_ROLE001',
          name: 'USER000001の管理者ロール',
          description: 'システム管理者ロールの割り当て',
        },
      }),
    ])

    // TRN_SkillRecordデータ
    console.log('📊 TRN_SkillRecordデータを投入中...')
    const skillRecordData = await Promise.all([
      prisma.skillRecord.upsert({
        where: { employee_id_skill_item_id: { employee_id: '000001', skill_item_id: 'SKILL001' } },
        update: {},
        create: {
          employee_id: '000001',
          skill_item_id: 'SKILL001',
          skill_level: 4,
          self_assessment: 4,
          manager_assessment: 3,
          evidence_description: 'Javaを使用したWebアプリケーション開発プロジェクトを3件担当',
          acquisition_date: new Date('2020-06-01'),
          last_used_date: new Date('2025-05-30'),
          skill_category_id: 'CAT001',
          assessment_date: new Date('2025-04-01'),
          assessor_id: '000001',
          skill_status: 'ACTIVE',
          learning_hours: 120,
          project_experience_count: 3,
          id: 'SR_EMP000001_SKILL001',
          is_deleted: false,
          tenant_id: 'TENANT_001',
          created_at: new Date('2025-06-01'),
          updated_at: new Date('2025-06-01'),
          created_by: 'USER000001',
          updated_by: 'USER000001',
        },
      }),
    ])

    console.log('✅ データベースの初期データ投入が完了しました！')
    console.log('📋 投入されたデータの詳細:')
    console.log('   - テナント: 1件')
    console.log('   - 部署: 1件')
    console.log('   - 役職: 1件')
    console.log('   - 職種: 1件')
    console.log('   - ロール: 1件')
    console.log('   - 権限: 1件')
    console.log('   - スキルカテゴリ: 1件')
    console.log('   - スキル項目: 1件')
    console.log('   - 社員: 1件')
    console.log('   - 社員部署配属: 1件')
    console.log('   - 社員職種配属: 1件')
    console.log('   - スキル記録: 1件')
    console.log('')
    console.log('🔐 ログイン情報:')
    console.log('   テストユーザー:')
    console.log('     ユーザーID: 000001')
    console.log('     パスワード: password')

  } catch (error) {
    console.error('❌ 初期データ投入中にエラーが発生しました:', error)
    throw error
  }
}

if (require.main === module) {
  runSampleSeed()
    .then(async () => {
      await prisma.$disconnect()
    })
    .catch(async (e) => {
      console.error('❌ 初期データ投入中にエラーが発生しました:', e)
      await prisma.$disconnect()
      throw e
    })
}
