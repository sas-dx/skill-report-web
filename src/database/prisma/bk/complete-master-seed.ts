// @ts-nocheck
import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()

export async function runCompleteMasterSeed() {
  console.log('🌱 完全版マスタデータ投入を開始します...')

  try {
    // パスワードハッシュ生成
    const passwordHash = await bcrypt.hash('password', 12);
    console.log('🔐 パスワードハッシュを生成しました');

    // ========================================
    // Priority 1: 基本マスタ（依存関係なし）
    // ========================================

    // 1. MST_Tenant
    console.log('📊 [1/30] MST_Tenantデータを投入中...')
    await prisma.tenant.upsert({
      where: { tenant_id: 'default-tenant' },
      update: {},
      create: {
        tenant_id: 'default-tenant',
        tenant_code: 'DEFAULT',
        tenant_name: 'デフォルトテナント',
      },
    });

    // 2. MST_Department（部署）
    console.log('📊 [2/30] MST_Departmentデータを投入中...')
    const departments = [
      { code: 'DEPT001', name: '経営企画部' },
      { code: 'DEPT002', name: 'システム開発部' },
      { code: 'DEPT003', name: '営業部' },
    ];
    for (const dept of departments) {
      await prisma.department.upsert({
        where: { department_code: dept.code },
        update: {},
        create: {
          department_code: dept.code,
          department_name: dept.name,
        },
      });
    }

    // 3. MST_Position（役職）
    console.log('📊 [3/30] MST_Positionデータを投入中...')
    const positions = [
      { code: 'POS001', name: '社長' },
      { code: 'POS002', name: '取締役' },
      { code: 'POS003', name: '部長' },
      { code: 'POS004', name: '課長' },
      { code: 'POS005', name: '一般社員' },
    ];
    for (const pos of positions) {
      await prisma.position.upsert({
        where: { position_code: pos.code },
        update: {},
        create: {
          position_code: pos.code,
          position_name: pos.name,
        },
      });
    }

    // 4. MST_JobType（職種）
    console.log('📊 [4/30] MST_JobTypeデータを投入中...')
    const jobTypes = [
      { code: 'SE', name: 'システムエンジニア', description: 'システムの設計・開発' },
      { code: 'PM', name: 'プロジェクトマネージャー', description: 'プロジェクト管理' },
      { code: 'PG', name: 'プログラマー', description: 'プログラミング' },
    ];
    for (const job of jobTypes) {
      await prisma.jobType.upsert({
        where: { job_type_code: job.code },
        update: {},
        create: {
          job_type_code: job.code,
          job_type_name: job.name,
          description: job.description,
        },
      });
    }

    // 5. MST_Role（ロール）
    console.log('📊 [5/30] MST_Roleデータを投入中...')
    const roles = [
      { code: 'ADMIN', name: '管理者', description: 'システム管理者' },
      { code: 'USER', name: '一般ユーザー', description: '一般利用者' },
      { code: 'MANAGER', name: 'マネージャー', description: '承認権限者' },
    ];
    for (const role of roles) {
      await prisma.role.upsert({
        where: { role_code: role.code },
        update: {},
        create: {
          role_code: role.code,
          role_name: role.name,
          role_description: role.description,
        },
      });
    }

    // 6. MST_Permission（権限）
    console.log('📊 [6/30] MST_Permissionデータを投入中...')
    const permissions = [
      { code: 'VIEW_ALL', name: '全データ閲覧', description: 'すべてのデータを閲覧' },
      { code: 'EDIT_ALL', name: '全データ編集', description: 'すべてのデータを編集' },
      { code: 'APPROVE', name: '承認', description: 'データを承認' },
      { code: 'VIEW_OWN', name: '自データ閲覧', description: '自分のデータを閲覧' },
      { code: 'EDIT_OWN', name: '自データ編集', description: '自分のデータを編集' },
    ];
    for (const perm of permissions) {
      await prisma.permission.upsert({
        where: { permission_code: perm.code },
        update: {},
        create: {
          permission_code: perm.code,
          permission_name: perm.name,
          permission_description: perm.description,
        },
      });
    }

    // 7. MST_SkillCategory（スキルカテゴリ）
    console.log('📊 [7/30] MST_SkillCategoryデータを投入中...')
    const skillCategories = [
      { code: 'CAT001', name: 'プログラミング言語' },
      { code: 'CAT002', name: 'フレームワーク' },
      { code: 'CAT003', name: 'データベース' },
      { code: 'CAT004', name: 'クラウドサービス' },
      { code: 'CAT005', name: 'プロジェクト管理' },
    ];
    for (const cat of skillCategories) {
      await prisma.skillCategory.upsert({
        where: { category_code: cat.code },
        update: {},
        create: {
          category_code: cat.code,
          category_name: cat.name,
        },
      });
    }

    // 8. MST_SkillGrade（スキルグレード）
    console.log('📊 [8/30] MST_SkillGradeデータを投入中...')
    const skillGrades = [
      { code: 'GRADE1', name: '初級', points: 1, description: '基礎知識がある' },
      { code: 'GRADE2', name: '中級', points: 2, description: '実務経験がある' },
      { code: 'GRADE3', name: '上級', points: 3, description: '独力で実装できる' },
      { code: 'GRADE4', name: 'エキスパート', points: 4, description: '指導できる' },
      { code: 'GRADE5', name: 'マスター', points: 5, description: '専門家レベル' },
    ];
    for (const grade of skillGrades) {
      await prisma.skillGrade.upsert({
        where: { grade_code: grade.code },
        update: {},
        create: {
          grade_code: grade.code,
          grade_name: grade.name,
          grade_points: grade.points,
          grade_description: grade.description,
        },
      });
    }

    // 9. MST_TrainingType（研修タイプ）
    console.log('📊 [9/30] MST_TrainingTypeデータを投入中...')
    const trainingTypes = [
      { code: 'TYPE001', name: '社内研修' },
      { code: 'TYPE002', name: '外部研修' },
      { code: 'TYPE003', name: 'オンライン研修' },
    ];
    for (const type of trainingTypes) {
      await prisma.trainingType.upsert({
        where: { type_code: type.code },
        update: {},
        create: {
          type_code: type.code,
          type_name: type.name,
        },
      });
    }

    // 10. MST_TrainingStatus（研修ステータス）
    console.log('📊 [10/30] MST_TrainingStatusデータを投入中...')
    const trainingStatuses = [
      { code: 'PLAN', name: '計画中' },
      { code: 'APPLY', name: '申請中' },
      { code: 'APPROVE', name: '承認済' },
      { code: 'COMPLETE', name: '完了' },
      { code: 'CANCEL', name: 'キャンセル' },
    ];
    for (const status of trainingStatuses) {
      await prisma.trainingStatus.upsert({
        where: { status_code: status.code },
        update: {},
        create: {
          status_code: status.code,
          status_name: status.name,
        },
      });
    }

    // 11. MST_EvaluationGrade（評価グレード）
    console.log('📊 [11/30] MST_EvaluationGradeデータを投入中...')
    const evaluationGrades = [
      { code: 'S', name: '優秀', points: 5.0, description: '期待を大きく上回る' },
      { code: 'A', name: '良好', points: 4.0, description: '期待を上回る' },
      { code: 'B', name: '標準', points: 3.0, description: '期待通り' },
      { code: 'C', name: '要改善', points: 2.0, description: '期待を下回る' },
      { code: 'D', name: '不可', points: 1.0, description: '大幅に改善が必要' },
    ];
    for (const grade of evaluationGrades) {
      await prisma.evaluationGrade.upsert({
        where: { grade_code: grade.code },
        update: {},
        create: {
          grade_code: grade.code,
          grade_name: grade.name,
          grade_points: grade.points,
          grade_description: grade.description,
        },
      });
    }

    // 12. MST_ProjectStatus（プロジェクトステータス）
    console.log('📊 [12/30] MST_ProjectStatusデータを投入中...')
    const projectStatuses = [
      { code: 'PLAN', name: '計画中' },
      { code: 'PROGRESS', name: '進行中' },
      { code: 'REVIEW', name: 'レビュー中' },
      { code: 'COMPLETE', name: '完了' },
      { code: 'HOLD', name: '保留' },
    ];
    for (const status of projectStatuses) {
      await prisma.projectStatus.upsert({
        where: { status_code: status.code },
        update: {},
        create: {
          status_code: status.code,
          status_name: status.name,
        },
      });
    }

    // 13. MST_CertificationCategory（資格カテゴリ）
    console.log('📊 [13/30] MST_CertificationCategoryデータを投入中...')
    const certCategories = [
      { code: 'CERT_CAT001', name: '国家資格' },
      { code: 'CERT_CAT002', name: 'ベンダー資格' },
      { code: 'CERT_CAT003', name: '語学資格' },
    ];
    for (const cat of certCategories) {
      await prisma.certificationCategory.upsert({
        where: { category_code: cat.code },
        update: {},
        create: {
          category_code: cat.code,
          category_name: cat.name,
        },
      });
    }

    // 14. MST_CertificationLevel（資格レベル）
    console.log('📊 [14/30] MST_CertificationLevelデータを投入中...')
    const certLevels = [
      { code: 'LEVEL1', name: '初級', points: 1 },
      { code: 'LEVEL2', name: '中級', points: 2 },
      { code: 'LEVEL3', name: '上級', points: 3 },
      { code: 'LEVEL4', name: '専門', points: 4 },
    ];
    for (const level of certLevels) {
      await prisma.certificationLevel.upsert({
        where: { level_code: level.code },
        update: {},
        create: {
          level_code: level.code,
          level_name: level.name,
          level_points: level.points,
        },
      });
    }

    // 15. MST_GoalCategory（目標カテゴリ）
    console.log('📊 [15/30] MST_GoalCategoryデータを投入中...')
    const goalCategories = [
      { code: 'GOAL_CAT001', name: 'スキル向上' },
      { code: 'GOAL_CAT002', name: '資格取得' },
      { code: 'GOAL_CAT003', name: 'プロジェクト達成' },
      { code: 'GOAL_CAT004', name: 'キャリア開発' },
    ];
    for (const cat of goalCategories) {
      await prisma.goalCategory.upsert({
        where: { category_code: cat.code },
        update: {},
        create: {
          category_code: cat.code,
          category_name: cat.name,
        },
      });
    }

    // 16. MST_GoalStatus（目標ステータス）
    console.log('📊 [16/30] MST_GoalStatusデータを投入中...')
    const goalStatuses = [
      { code: 'NOT_START', name: '未着手' },
      { code: 'IN_PROGRESS', name: '進行中' },
      { code: 'ACHIEVED', name: '達成' },
      { code: 'NOT_ACHIEVED', name: '未達成' },
      { code: 'CANCELLED', name: '中止' },
    ];
    for (const status of goalStatuses) {
      await prisma.goalStatus.upsert({
        where: { status_code: status.code },
        update: {},
        create: {
          status_code: status.code,
          status_name: status.name,
        },
      });
    }

    // 17. MST_FiscalYear（会計年度）
    console.log('📊 [17/30] MST_FiscalYearデータを投入中...')
    const fiscalYears = [
      {
        year_code: 'FY2024',
        year_name: '2024年度',
        start_date: new Date('2024-04-01'),
        end_date: new Date('2025-03-31'),
        is_current: false,
      },
      {
        year_code: 'FY2025',
        year_name: '2025年度',
        start_date: new Date('2025-04-01'),
        end_date: new Date('2026-03-31'),
        is_current: true,
      },
    ];
    for (const fy of fiscalYears) {
      await prisma.fiscalYear.upsert({
        where: { year_code: fy.year_code },
        update: {},
        create: fy,
      });
    }

    // 18. MST_ReportTemplate（レポートテンプレート）
    console.log('📊 [18/30] MST_ReportTemplateデータを投入中...')
    const reportTemplates = [
      {
        template_code: 'TMPL001',
        template_name: '月次報告書',
        template_description: '月次の進捗報告書',
      },
      {
        template_code: 'TMPL002',
        template_name: '年次スキル報告書',
        template_description: '年度末のスキル評価報告書',
      },
    ];
    for (const tmpl of reportTemplates) {
      await prisma.reportTemplate.upsert({
        where: { template_code: tmpl.template_code },
        update: {},
        create: tmpl,
      });
    }

    // 19. MST_NotificationType（通知タイプ）
    console.log('📊 [19/30] MST_NotificationTypeデータを投入中...')
    const notificationTypes = [
      { code: 'INFO', name: 'お知らせ' },
      { code: 'APPROVE', name: '承認依頼' },
      { code: 'ALERT', name: 'アラート' },
      { code: 'REMINDER', name: 'リマインダー' },
    ];
    for (const type of notificationTypes) {
      await prisma.notificationType.upsert({
        where: { type_code: type.code },
        update: {},
        create: {
          type_code: type.code,
          type_name: type.name,
        },
      });
    }

    // 20. MST_NotificationPriority（通知優先度）
    console.log('📊 [20/30] MST_NotificationPriorityデータを投入中...')
    const notificationPriorities = [
      { code: 'HIGH', name: '高', level: 1 },
      { code: 'MEDIUM', name: '中', level: 2 },
      { code: 'LOW', name: '低', level: 3 },
    ];
    for (const priority of notificationPriorities) {
      await prisma.notificationPriority.upsert({
        where: { priority_code: priority.code },
        update: {},
        create: {
          priority_code: priority.code,
          priority_name: priority.name,
          priority_level: priority.level,
        },
      });
    }

    // 21. MST_EvaluationPeriod（評価期間）
    console.log('📊 [21/30] MST_EvaluationPeriodデータを投入中...')
    const evaluationPeriods = [
      {
        period_code: 'EVAL2024H1',
        period_name: '2024年度上期',
        start_date: new Date('2024-04-01'),
        end_date: new Date('2024-09-30'),
        is_active: false,
      },
      {
        period_code: 'EVAL2024H2',
        period_name: '2024年度下期',
        start_date: new Date('2024-10-01'),
        end_date: new Date('2025-03-31'),
        is_active: true,
      },
    ];
    for (const period of evaluationPeriods) {
      await prisma.evaluationPeriod.upsert({
        where: { period_code: period.period_code },
        update: {},
        create: period,
      });
    }

    // 22. MST_SystemConfig（システム設定）
    console.log('📊 [22/30] MST_SystemConfigデータを投入中...')
    const systemConfigs = [
      {
        config_code: 'SESSION_TIMEOUT',
        config_value: '480',
        config_description: 'セッションタイムアウト（分）',
      },
      {
        config_code: 'MAX_LOGIN_ATTEMPTS',
        config_value: '5',
        config_description: '最大ログイン試行回数',
      },
      {
        config_code: 'PASSWORD_EXPIRE_DAYS',
        config_value: '90',
        config_description: 'パスワード有効期限（日）',
      },
    ];
    for (const config of systemConfigs) {
      await prisma.systemConfig.upsert({
        where: { config_code: config.config_code },
        update: {},
        create: config,
      });
    }

    // ========================================
    // Priority 2: 依存関係のあるマスタ
    // ========================================

    // 23. MST_Employee（従業員）
    console.log('📊 [23/30] MST_Employeeデータを投入中...')
    const employees = [
      {
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
      {
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
        position_id: 'POS004',
        job_type_id: 'PM',
        employment_status: 'FULL_TIME',
        employee_status: 'ACTIVE',
        manager_id: 'emp_001',
      },
      {
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
        position_id: 'POS005',
        job_type_id: 'PG',
        employment_status: 'FULL_TIME',
        employee_status: 'ACTIVE',
      },
    ];
    for (const emp of employees) {
      await prisma.employee.upsert({
        where: { id: emp.id },
        update: {},
        create: emp,
      });
    }

    // 24. MST_UserAuth（ユーザー認証）
    console.log('📊 [24/30] MST_UserAuthデータを投入中...')
    const userAuths = [
      {
        user_id: 'USER000001',
        login_id: '000001',
        password_hash: passwordHash,
        password_salt: 'randomsalt123',
        employee_id: '000001',
        account_status: 'ACTIVE',
        failed_login_count: 0,
        session_timeout: 480,
      },
      {
        user_id: 'USER000002',
        login_id: '000002',
        password_hash: passwordHash,
        password_salt: 'randomsalt456',
        employee_id: '000002',
        account_status: 'ACTIVE',
        failed_login_count: 0,
        session_timeout: 480,
      },
      {
        user_id: 'USER_TEST_EMPLOYEE',
        login_id: 'test-employee',
        password_hash: passwordHash,
        password_salt: 'testsalt123',
        employee_id: 'test-employee',
        account_status: 'ACTIVE',
        failed_login_count: 0,
        session_timeout: 480,
      },
    ];
    for (const auth of userAuths) {
      await prisma.userAuth.upsert({
        where: { user_id: auth.user_id },
        update: {},
        create: auth,
      });
    }

    // 25. MST_UserRole（ユーザーロール）
    console.log('📊 [25/30] MST_UserRoleデータを投入中...')
    const userRoles = [
      { user_id: 'USER000001', role_code: 'USER', assigned_date: new Date() },
      { user_id: 'USER000002', role_code: 'MANAGER', assigned_date: new Date() },
      { user_id: 'USER_TEST_EMPLOYEE', role_code: 'ADMIN', assigned_date: new Date() },
    ];
    for (const ur of userRoles) {
      await prisma.userRole.upsert({
        where: {
          user_id_role_code: {
            user_id: ur.user_id,
            role_code: ur.role_code,
          },
        },
        update: {},
        create: ur,
      });
    }

    // 26. MST_RolePermission（ロール権限）
    console.log('📊 [26/30] MST_RolePermissionデータを投入中...')
    const rolePermissions = [
      // ADMIN: すべての権限
      { role_code: 'ADMIN', permission_code: 'VIEW_ALL' },
      { role_code: 'ADMIN', permission_code: 'EDIT_ALL' },
      { role_code: 'ADMIN', permission_code: 'APPROVE' },
      // MANAGER: 閲覧と承認
      { role_code: 'MANAGER', permission_code: 'VIEW_ALL' },
      { role_code: 'MANAGER', permission_code: 'APPROVE' },
      // USER: 自分のデータのみ
      { role_code: 'USER', permission_code: 'VIEW_OWN' },
      { role_code: 'USER', permission_code: 'EDIT_OWN' },
    ];
    for (const rp of rolePermissions) {
      await prisma.rolePermission.upsert({
        where: {
          role_code_permission_code: {
            role_code: rp.role_code,
            permission_code: rp.permission_code,
          },
        },
        update: {},
        create: rp,
      });
    }

    // 27. MST_SkillItem（スキル項目）
    console.log('📊 [27/30] MST_SkillItemデータを投入中...')
    const skillItems = [
      // プログラミング言語
      { code: 'SKILL001', name: 'Java', category: 'CAT001' },
      { code: 'SKILL002', name: 'Python', category: 'CAT001' },
      { code: 'SKILL003', name: 'JavaScript', category: 'CAT001' },
      { code: 'SKILL004', name: 'TypeScript', category: 'CAT001' },
      { code: 'SKILL005', name: 'C#', category: 'CAT001' },
      // フレームワーク
      { code: 'SKILL006', name: 'Spring Boot', category: 'CAT002' },
      { code: 'SKILL007', name: 'React', category: 'CAT002' },
      { code: 'SKILL008', name: 'Next.js', category: 'CAT002' },
      { code: 'SKILL009', name: 'Vue.js', category: 'CAT002' },
      { code: 'SKILL010', name: 'Angular', category: 'CAT002' },
      // データベース
      { code: 'SKILL011', name: 'PostgreSQL', category: 'CAT003' },
      { code: 'SKILL012', name: 'MySQL', category: 'CAT003' },
      { code: 'SKILL013', name: 'Oracle', category: 'CAT003' },
      { code: 'SKILL014', name: 'MongoDB', category: 'CAT003' },
      { code: 'SKILL015', name: 'Redis', category: 'CAT003' },
      // クラウドサービス
      { code: 'SKILL016', name: 'AWS', category: 'CAT004' },
      { code: 'SKILL017', name: 'Azure', category: 'CAT004' },
      { code: 'SKILL018', name: 'GCP', category: 'CAT004' },
      // プロジェクト管理
      { code: 'SKILL019', name: 'スクラム', category: 'CAT005' },
      { code: 'SKILL020', name: 'ウォーターフォール', category: 'CAT005' },
    ];
    for (const skill of skillItems) {
      await prisma.skillItem.upsert({
        where: { skill_code: skill.code },
        update: {},
        create: {
          skill_code: skill.code,
          skill_name: skill.name,
          skill_category_id: skill.category,
        },
      });
    }

    // 28. MST_TrainingProgram（研修プログラム）
    console.log('📊 [28/30] MST_TrainingProgramデータを投入中...')
    const trainingPrograms = [
      {
        program_code: 'PROG001',
        program_name: '新人研修',
        program_description: '新入社員向け基礎研修',
        training_type_id: 'TYPE001',
        duration_days: 30,
        max_participants: 20,
        is_mandatory: true,
      },
      {
        program_code: 'PROG002',
        program_name: 'Java開発研修',
        program_description: 'Java開発スキル向上研修',
        training_type_id: 'TYPE002',
        duration_days: 5,
        max_participants: 15,
        is_mandatory: false,
      },
      {
        program_code: 'PROG003',
        program_name: 'AWS認定研修',
        program_description: 'AWS認定資格取得研修',
        training_type_id: 'TYPE003',
        duration_days: 3,
        max_participants: 10,
        is_mandatory: false,
      },
    ];
    for (const prog of trainingPrograms) {
      await prisma.trainingProgram.upsert({
        where: { program_code: prog.program_code },
        update: {},
        create: prog,
      });
    }

    // 29. MST_Certification（資格）
    console.log('📊 [29/30] MST_Certificationデータを投入中...')
    const certifications = [
      {
        certification_code: 'CERT001',
        certification_name: '基本情報技術者',
        certification_description: 'ITエンジニアの基礎資格',
        category_id: 'CERT_CAT001',
        level_id: 'LEVEL1',
        validity_years: null,
      },
      {
        certification_code: 'CERT002',
        certification_name: '応用情報技術者',
        certification_description: 'ITエンジニアの応用資格',
        category_id: 'CERT_CAT001',
        level_id: 'LEVEL2',
        validity_years: null,
      },
      {
        certification_code: 'CERT003',
        certification_name: 'AWS Certified Solutions Architect',
        certification_description: 'AWS認定ソリューションアーキテクト',
        category_id: 'CERT_CAT002',
        level_id: 'LEVEL3',
        validity_years: 3,
      },
      {
        certification_code: 'CERT004',
        certification_name: 'TOEIC 700点以上',
        certification_description: '英語能力試験',
        category_id: 'CERT_CAT003',
        level_id: 'LEVEL2',
        validity_years: 2,
      },
    ];
    for (const cert of certifications) {
      await prisma.certification.upsert({
        where: { certification_code: cert.certification_code },
        update: {},
        create: cert,
      });
    }

    // 30. MST_CareerPath（キャリアパス）- 最後に追加
    console.log('📊 [30/30] MST_CareerPathデータを投入中...')
    const careerPaths = [
      {
        path_code: 'PATH001',
        path_name: 'テクニカルスペシャリスト',
        path_description: '技術専門家を目指すキャリアパス',
        required_years: 5,
        required_skills: 'プログラミング上級、設計スキル',
      },
      {
        path_code: 'PATH002',
        path_name: 'プロジェクトマネージャー',
        path_description: 'PM職を目指すキャリアパス',
        required_years: 7,
        required_skills: 'マネジメント、コミュニケーション',
      },
      {
        path_code: 'PATH003',
        path_name: 'ITアーキテクト',
        path_description: 'システムアーキテクトを目指すキャリアパス',
        required_years: 10,
        required_skills: '設計、クラウド、セキュリティ',
      },
    ];
    for (const path of careerPaths) {
      await prisma.careerPath.upsert({
        where: { path_code: path.path_code },
        update: {},
        create: path,
      });
    }

    // ========================================
    // 完了メッセージ
    // ========================================
    console.log('\n✅ 完全版マスタデータ投入が完了しました！\n')
    console.log('📋 投入されたマスタデータ:')
    console.log('   基本マスタ:')
    console.log('     - テナント: 1件')
    console.log('     - 部署: 3件')
    console.log('     - 役職: 5件')
    console.log('     - 職種: 3件')
    console.log('     - ロール: 3件')
    console.log('     - 権限: 5件')
    console.log('   スキル関連:')
    console.log('     - スキルカテゴリ: 5件')
    console.log('     - スキル項目: 20件')
    console.log('     - スキルグレード: 5件')
    console.log('   研修・資格:')
    console.log('     - 研修タイプ: 3件')
    console.log('     - 研修ステータス: 5件')
    console.log('     - 研修プログラム: 3件')
    console.log('     - 資格カテゴリ: 3件')
    console.log('     - 資格レベル: 4件')
    console.log('     - 資格: 4件')
    console.log('   評価・目標:')
    console.log('     - 評価グレード: 5件')
    console.log('     - 評価期間: 2件')
    console.log('     - 目標カテゴリ: 4件')
    console.log('     - 目標ステータス: 5件')
    console.log('   その他:')
    console.log('     - プロジェクトステータス: 5件')
    console.log('     - 会計年度: 2件')
    console.log('     - レポートテンプレート: 2件')
    console.log('     - 通知タイプ: 4件')
    console.log('     - 通知優先度: 3件')
    console.log('     - キャリアパス: 3件')
    console.log('     - システム設定: 3件')
    console.log('   ユーザー関連:')
    console.log('     - 従業員: 3件')
    console.log('     - ユーザー認証: 3件')
    console.log('     - ユーザーロール: 3件')
    console.log('     - ロール権限: 7件')
    console.log('\n🔐 ログイン情報:')
    console.log('   管理者ユーザー:')
    console.log('     ユーザーID: test-employee')
    console.log('     パスワード: password')
    console.log('     権限: ADMIN（全権限）')
    console.log('   マネージャーユーザー:')
    console.log('     ユーザーID: 000002')
    console.log('     パスワード: password')
    console.log('     権限: MANAGER（閲覧・承認）')
    console.log('   一般ユーザー:')
    console.log('     ユーザーID: 000001')
    console.log('     パスワード: password')
    console.log('     権限: USER（自データのみ）')

  } catch (error) {
    console.error('❌ マスタデータ投入中にエラーが発生しました:', error)
    throw error
  } finally {
    await prisma.$disconnect()
  }
}

// 直接実行時
if (require.main === module) {
  runCompleteMasterSeed()
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
export default runCompleteMasterSeed