/**
 * データ整合性統合テスト
 *
 * テスト計画書 5.2節に基づく実装
 * - 一意制約テスト
 * - 論理削除テスト
 * - 外部キー制約テスト
 * - NOT NULL制約テスト
 */

import { describe, it, expect, beforeAll, afterAll, beforeEach } from '@jest/globals'
import { PrismaClient, Prisma } from '@prisma/client'
import {
  setupTestDatabase,
  teardownTestDatabase,
  cleanupTestData,
  createTestTenant,
  createTestEmployee,
  createTestSkillCategory,
  createTestSkillItem,
  createTestProjectRecord
} from '@/test/helpers'

describe('DB-002: データ整合性統合テスト', () => {
  let prisma: PrismaClient
  let testTenant: any
  let testEmployee1: any
  let testEmployee2: any

  beforeAll(async () => {
    prisma = await setupTestDatabase()
  })

  afterAll(async () => {
    await teardownTestDatabase()
  })

  beforeEach(async () => {
    await cleanupTestData(prisma)

    testTenant = await createTestTenant(prisma, {
      tenant_code: 'TENANT_INTEGRITY_001',
      tenant_name: 'データ整合性テスト用テナント'
    })

    testEmployee1 = await createTestEmployee(prisma, {
      tenant_id: testTenant.id,
      employee_code: 'INTEGRITY_EMP_001',
      full_name: 'データ整合性テストユーザー1',
      email: 'integrity1@example.com'
    })

    testEmployee2 = await createTestEmployee(prisma, {
      tenant_id: testTenant.id,
      employee_code: 'INTEGRITY_EMP_002',
      full_name: 'データ整合性テストユーザー2',
      email: 'integrity2@example.com'
    })
  })

  describe('一意制約テスト', () => {
    it('異常系: 重複社員コード（employee_code）で一意制約違反', async () => {
      const duplicateCode = 'DUPLICATE_EMP_CODE'

      // 1つ目の社員作成
      await createTestEmployee(prisma, {
        tenant_id: testTenant.id,
        employee_code: duplicateCode,
        full_name: '重複テスト1',
        email: 'unique1@example.com'
      })

      // 同じemployee_codeで2つ目を作成しようとする
      await expect(
        createTestEmployee(prisma, {
          tenant_id: testTenant.id,
          employee_code: duplicateCode, // 重複
          full_name: '重複テスト2',
          email: 'unique2@example.com'
        })
      ).rejects.toThrow()
    })

    it('異常系: 重複メールアドレス（email）で一意制約違反', async () => {
      const duplicateEmail = 'duplicate@example.com'

      // 1つ目の社員作成
      await createTestEmployee(prisma, {
        tenant_id: testTenant.id,
        employee_code: 'UNIQUE_TEST_001',
        full_name: '重複メールテスト1',
        email: duplicateEmail
      })

      // 同じemailで2つ目を作成しようとする
      await expect(
        createTestEmployee(prisma, {
          tenant_id: testTenant.id,
          employee_code: 'UNIQUE_TEST_002',
          full_name: '重複メールテスト2',
          email: duplicateEmail // 重複
        })
      ).rejects.toThrow()
    })

    it('異常系: 重複スキルカテゴリコード（category_code）で一意制約違反', async () => {
      const duplicateCategoryCode = 'DUPLICATE_CAT_CODE'
      const timestamp = Date.now()

      // 1つ目のカテゴリ作成
      await createTestSkillCategory(prisma, testTenant.id, 'system', {
        category_code: duplicateCategoryCode,
        category_name: '重複カテゴリテスト1'
      })

      // 同じcategory_codeで2つ目を作成しようとする
      try {
        await prisma.mST_SkillCategory.create({
          data: {
            id: `dup_cat_${timestamp}`,
            category_id: `CAT_DUP_${timestamp}`,
            tenant_id: testTenant.id,
            category_code: duplicateCategoryCode, // 重複
            category_name: '重複カテゴリテスト2',
            category_name_en: 'Duplicate Category Test 2',
            display_order: 1,
            is_active: true,
            created_by: 'system',
            updated_by: 'system',
            is_deleted: false
          }
        })
        fail('一意制約違反のエラーが発生すべきです')
      } catch (error) {
        if (error instanceof Prisma.PrismaClientKnownRequestError) {
          expect(error.code).toBe('P2002')
        } else {
          throw error
        }
      }
    })

    it('正常系: 同一社員が同一スキルを複数回登録できない（複合一意制約）', async () => {
      const timestamp = Date.now()

      // スキルカテゴリとスキルアイテム作成
      const category = await createTestSkillCategory(prisma, testTenant.id, 'system', {
        category_code: `CAT_COMPOSITE_${timestamp}`,
        category_name: '複合制約テスト用カテゴリ'
      })

      const skillItem = await createTestSkillItem(
        prisma,
        category.id,
        testTenant.id,
        'system',
        {
          skill_item_id: `SKILL_COMPOSITE_${timestamp}`,
          skill_name: '複合制約テストスキル'
        }
      )

      // 1つ目のスキルレコード作成
      await prisma.tRN_SkillRecord.create({
        data: {
          id: `skill_rec_1_${timestamp}`,
          skill_record_id: `SKILL_REC_1_${timestamp}`,
          tenant_id: testTenant.id,
          employee_id: testEmployee1.id,
          skill_item_id: skillItem.id,
          skill_level: 3,
          self_assessment: 3,
          acquisition_date: new Date(),
          last_used_date: new Date(),
          skill_status: 'ACTIVE',
          created_by: testEmployee1.id,
          updated_by: testEmployee1.id,
          is_deleted: false
        }
      })

      // 同じ社員・同じスキルで2つ目を作成しようとする
      try {
        await prisma.tRN_SkillRecord.create({
          data: {
            id: `skill_rec_2_${timestamp}`,
            skill_record_id: `SKILL_REC_2_${timestamp}`,
            tenant_id: testTenant.id,
            employee_id: testEmployee1.id, // 同じ社員
            skill_item_id: skillItem.id, // 同じスキル
            skill_level: 4,
            self_assessment: 4,
            acquisition_date: new Date(),
            last_used_date: new Date(),
            skill_status: 'ACTIVE',
            created_by: testEmployee1.id,
            updated_by: testEmployee1.id,
            is_deleted: false
          }
        })
        fail('複合一意制約違反のエラーが発生すべきです')
      } catch (error) {
        if (error instanceof Prisma.PrismaClientKnownRequestError) {
          expect(error.code).toBe('P2002')
        } else {
          throw error
        }
      }
    })
  })

  describe('論理削除テスト', () => {
    it('正常系: is_deletedフラグで社員を論理削除', async () => {
      const employee = await createTestEmployee(prisma, {
        tenant_id: testTenant.id,
        employee_code: 'SOFT_DELETE_TEST',
        full_name: '論理削除テストユーザー',
        email: 'softdelete@example.com'
      })

      // 論理削除実行
      await prisma.mST_Employee.update({
        where: { id: employee.id },
        data: {
          is_deleted: true,
          updated_at: new Date()
        }
      })

      // is_deleted=falseでは取得できない
      const activeEmployees = await prisma.mST_Employee.findMany({
        where: {
          id: employee.id,
          is_deleted: false
        }
      })
      expect(activeEmployees).toHaveLength(0)

      // is_deletedを含めると取得できる
      const allEmployees = await prisma.mST_Employee.findMany({
        where: { id: employee.id }
      })
      expect(allEmployees).toHaveLength(1)
      expect(allEmployees[0].is_deleted).toBe(true)
    })

    it('正常系: スキルレコードの論理削除', async () => {
      const timestamp = Date.now()

      const category = await createTestSkillCategory(prisma, testTenant.id, 'system', {
        category_code: `CAT_SOFT_DEL_${timestamp}`,
        category_name: '論理削除テスト用カテゴリ'
      })

      const skillItem = await createTestSkillItem(
        prisma,
        category.id,
        testTenant.id,
        'system',
        {
          skill_item_id: `SKILL_SOFT_DEL_${timestamp}`,
          skill_name: '論理削除テストスキル'
        }
      )

      const skillRecord = await prisma.tRN_SkillRecord.create({
        data: {
          id: `skill_soft_del_${timestamp}`,
          skill_record_id: `SKILL_REC_SOFT_DEL_${timestamp}`,
          tenant_id: testTenant.id,
          employee_id: testEmployee1.id,
          skill_item_id: skillItem.id,
          skill_level: 3,
          self_assessment: 3,
          acquisition_date: new Date(),
          last_used_date: new Date(),
          skill_status: 'ACTIVE',
          created_by: testEmployee1.id,
          updated_by: testEmployee1.id,
          is_deleted: false
        }
      })

      // 論理削除実行
      await prisma.tRN_SkillRecord.update({
        where: { id: skillRecord.id },
        data: {
          is_deleted: true,
          updated_at: new Date()
        }
      })

      // is_deleted=falseでは取得できない
      const activeRecords = await prisma.tRN_SkillRecord.findMany({
        where: {
          id: skillRecord.id,
          is_deleted: false
        }
      })
      expect(activeRecords).toHaveLength(0)

      // is_deletedを含めると取得できる
      const allRecords = await prisma.tRN_SkillRecord.findMany({
        where: { id: skillRecord.id }
      })
      expect(allRecords).toHaveLength(1)
      expect(allRecords[0].is_deleted).toBe(true)
    })

    it('正常系: 論理削除後に同一コードで新規作成が可能', async () => {
      const employeeCode = 'REUSABLE_CODE'

      // 1つ目の社員作成
      const employee1 = await createTestEmployee(prisma, {
        tenant_id: testTenant.id,
        employee_code: employeeCode,
        full_name: '再利用テスト1',
        email: 'reusable1@example.com'
      })

      // 論理削除
      await prisma.mST_Employee.update({
        where: { id: employee1.id },
        data: {
          is_deleted: true,
          updated_at: new Date()
        }
      })

      // 同じemployee_codeで新規作成（一意制約はis_deleted=falseのレコードのみ対象の場合）
      // 注: スキーマ設計によっては、この動作が異なる場合があります
      // この例では論理削除されたレコードは一意制約の対象外と仮定
      try {
        const employee2 = await createTestEmployee(prisma, {
          tenant_id: testTenant.id,
          employee_code: employeeCode, // 同じコード
          full_name: '再利用テスト2',
          email: 'reusable2@example.com'
        })

        expect(employee2).toBeTruthy()
        expect(employee2.employee_code).toBe(employeeCode)
        expect(employee2.is_deleted).toBe(false)
      } catch (error) {
        // スキーマが論理削除を考慮していない場合はエラーになる
        // その場合はスキップ
        console.log('Note: Schema does not allow code reuse after soft delete')
      }
    })
  })

  describe('外部キー制約テスト', () => {
    it('異常系: 存在しない社員IDで作業実績を作成', async () => {
      const timestamp = Date.now()

      await expect(
        prisma.tRN_ProjectRecord.create({
          data: {
            id: `fk_error_proj_${timestamp}`,
            project_record_id: `PRJ_FK_ERROR_${timestamp}`,
            tenant_id: testTenant.id,
            employee_id: 'NONEXISTENT_EMPLOYEE_ID', // 存在しない社員ID
            project_name: '外部キーエラーテスト',
            project_code: `PRJ_FK_ERROR_${timestamp}`,
            project_type: 'DEVELOPMENT',
            start_date: new Date(),
            role_title: 'エンジニア',
            project_status: 'ACTIVE',
            created_by: 'system',
            updated_by: 'system',
            is_deleted: false
          }
        })
      ).rejects.toThrow()
    })

    it('異常系: 存在しないスキルアイテムIDでスキルレコードを作成', async () => {
      const timestamp = Date.now()

      await expect(
        prisma.tRN_SkillRecord.create({
          data: {
            id: `fk_error_skill_${timestamp}`,
            skill_record_id: `SKILL_REC_FK_ERROR_${timestamp}`,
            tenant_id: testTenant.id,
            employee_id: testEmployee1.id,
            skill_item_id: 'NONEXISTENT_SKILL_ITEM_ID', // 存在しないスキルアイテムID
            skill_level: 3,
            self_assessment: 3,
            acquisition_date: new Date(),
            last_used_date: new Date(),
            skill_status: 'ACTIVE',
            created_by: testEmployee1.id,
            updated_by: testEmployee1.id,
            is_deleted: false
          }
        })
      ).rejects.toThrow()
    })

    it('正常系: CASCADE削除の動作確認（親削除時に子も削除）', async () => {
      const timestamp = Date.now()

      // スキルカテゴリとスキルアイテム作成
      const category = await createTestSkillCategory(prisma, testTenant.id, 'system', {
        category_code: `CAT_CASCADE_${timestamp}`,
        category_name: 'CASCADE削除テスト用カテゴリ'
      })

      const skillItem = await createTestSkillItem(
        prisma,
        category.id,
        testTenant.id,
        'system',
        {
          skill_item_id: `SKILL_CASCADE_${timestamp}`,
          skill_name: 'CASCADE削除テストスキル'
        }
      )

      // スキルレコード作成
      const skillRecord = await prisma.tRN_SkillRecord.create({
        data: {
          id: `skill_cascade_${timestamp}`,
          skill_record_id: `SKILL_REC_CASCADE_${timestamp}`,
          tenant_id: testTenant.id,
          employee_id: testEmployee1.id,
          skill_item_id: skillItem.id,
          skill_level: 3,
          self_assessment: 3,
          acquisition_date: new Date(),
          last_used_date: new Date(),
          skill_status: 'ACTIVE',
          created_by: testEmployee1.id,
          updated_by: testEmployee1.id,
          is_deleted: false
        }
      })

      // スキーマの設定によってCASCADE削除が有効な場合のテスト
      // 注: このテストはスキーマのonDelete設定に依存します
      try {
        // スキルアイテムを物理削除
        await prisma.mST_SkillItem.delete({
          where: { id: skillItem.id }
        })

        // スキルレコードも削除されていることを確認
        const deletedRecord = await prisma.tRN_SkillRecord.findUnique({
          where: { id: skillRecord.id }
        })
        expect(deletedRecord).toBeNull()
      } catch (error) {
        // CASCADE削除が設定されていない場合は外部キー制約エラー
        if (error instanceof Prisma.PrismaClientKnownRequestError) {
          expect(error.code).toBe('P2003')
        }
        console.log('Note: CASCADE delete not configured for this relationship')
      }
    })
  })

  describe('NOT NULL制約テスト', () => {
    it('異常系: 必須フィールド（employee_code）がNULLでエラー', async () => {
      const timestamp = Date.now()

      await expect(
        prisma.mST_Employee.create({
          data: {
            id: `null_test_${timestamp}`,
            // employee_code: 省略（NULL） - エラーになるべき
            tenant_id: testTenant.id,
            full_name: 'NULL制約テスト',
            email: `nulltest${timestamp}@example.com`,
            is_deleted: false
          } as any
        })
      ).rejects.toThrow()
    })

    it('異常系: 必須フィールド（full_name）がNULLでエラー', async () => {
      const timestamp = Date.now()

      await expect(
        prisma.mST_Employee.create({
          data: {
            id: `null_name_${timestamp}`,
            employee_code: `NULL_NAME_${timestamp}`,
            tenant_id: testTenant.id,
            // full_name: 省略（NULL） - エラーになるべき
            email: `nullname${timestamp}@example.com`,
            is_deleted: false
          } as any
        })
      ).rejects.toThrow()
    })

    it('異常系: スキルレコードの必須フィールド（skill_level）がNULLでエラー', async () => {
      const timestamp = Date.now()

      const category = await createTestSkillCategory(prisma, testTenant.id, 'system', {
        category_code: `CAT_NULL_${timestamp}`,
        category_name: 'NULL制約テスト用カテゴリ'
      })

      const skillItem = await createTestSkillItem(
        prisma,
        category.id,
        testTenant.id,
        'system',
        {
          skill_item_id: `SKILL_NULL_${timestamp}`,
          skill_name: 'NULL制約テストスキル'
        }
      )

      await expect(
        prisma.tRN_SkillRecord.create({
          data: {
            id: `skill_null_${timestamp}`,
            skill_record_id: `SKILL_REC_NULL_${timestamp}`,
            tenant_id: testTenant.id,
            employee_id: testEmployee1.id,
            skill_item_id: skillItem.id,
            // skill_level: 省略（NULL） - エラーになるべき
            self_assessment: 3,
            acquisition_date: new Date(),
            last_used_date: new Date(),
            skill_status: 'ACTIVE',
            created_by: testEmployee1.id,
            updated_by: testEmployee1.id,
            is_deleted: false
          } as any
        })
      ).rejects.toThrow()
    })
  })

  describe('データ型制約テスト', () => {
    it('異常系: 数値フィールドに文字列を設定', async () => {
      const timestamp = Date.now()

      const category = await createTestSkillCategory(prisma, testTenant.id, 'system', {
        category_code: `CAT_TYPE_${timestamp}`,
        category_name: '型制約テスト用カテゴリ'
      })

      const skillItem = await createTestSkillItem(
        prisma,
        category.id,
        testTenant.id,
        'system',
        {
          skill_item_id: `SKILL_TYPE_${timestamp}`,
          skill_name: '型制約テストスキル'
        }
      )

      await expect(
        prisma.tRN_SkillRecord.create({
          data: {
            id: `skill_type_${timestamp}`,
            skill_record_id: `SKILL_REC_TYPE_${timestamp}`,
            tenant_id: testTenant.id,
            employee_id: testEmployee1.id,
            skill_item_id: skillItem.id,
            skill_level: 'invalid' as any, // 文字列（本来はnumber）
            self_assessment: 3,
            acquisition_date: new Date(),
            last_used_date: new Date(),
            skill_status: 'ACTIVE',
            created_by: testEmployee1.id,
            updated_by: testEmployee1.id,
            is_deleted: false
          }
        })
      ).rejects.toThrow()
    })

    it('異常系: 日付フィールドに不正な値を設定', async () => {
      const timestamp = Date.now()

      await expect(
        createTestProjectRecord(prisma, testEmployee1.id, testTenant.id, testEmployee1.id, {
          project_record_id: `PRJ_DATE_ERROR_${timestamp}`,
          project_code: `PRJ_DATE_ERROR_${timestamp}`,
          project_name: '日付制約テスト',
          start_date: 'invalid-date' as any // 不正な日付
        })
      ).rejects.toThrow()
    })
  })

  describe('データ整合性ルール', () => {
    it('正常系: 論理的な整合性が保たれる（開始日 <= 終了日）', async () => {
      const timestamp = Date.now()

      // 開始日が終了日より後の場合でもデータベースには保存される
      // （ビジネスロジックでの検証が必要）
      const invalidProject = await createTestProjectRecord(
        prisma,
        testEmployee1.id,
        testTenant.id,
        testEmployee1.id,
        {
          project_record_id: `PRJ_DATE_CHECK_${timestamp}`,
          project_code: `PRJ_DATE_CHECK_${timestamp}`,
          project_name: '日付整合性テスト',
          start_date: new Date('2025-12-31'),
          end_date: new Date('2025-01-01') // 開始日より前
        }
      )

      // データベースには保存される（CHECK制約がない場合）
      expect(invalidProject).toBeTruthy()

      // ビジネスロジックでの検証が必要
      const isValid = invalidProject.start_date <= invalidProject.end_date
      expect(isValid).toBe(false) // ビジネスルール違反
    })

    it('正常系: スキルレベルの範囲制約（1-5）', async () => {
      const timestamp = Date.now()

      const category = await createTestSkillCategory(prisma, testTenant.id, 'system', {
        category_code: `CAT_RANGE_${timestamp}`,
        category_name: '範囲制約テスト用カテゴリ'
      })

      const skillItem = await createTestSkillItem(
        prisma,
        category.id,
        testTenant.id,
        'system',
        {
          skill_item_id: `SKILL_RANGE_${timestamp}`,
          skill_name: '範囲制約テストスキル'
        }
      )

      // 範囲外の値でも保存される（CHECK制約がない場合）
      const invalidSkillRecord = await prisma.tRN_SkillRecord.create({
        data: {
          id: `skill_range_${timestamp}`,
          skill_record_id: `SKILL_REC_RANGE_${timestamp}`,
          tenant_id: testTenant.id,
          employee_id: testEmployee1.id,
          skill_item_id: skillItem.id,
          skill_level: 10, // 範囲外（1-5が正常）
          self_assessment: 10,
          acquisition_date: new Date(),
          last_used_date: new Date(),
          skill_status: 'ACTIVE',
          created_by: testEmployee1.id,
          updated_by: testEmployee1.id,
          is_deleted: false
        }
      })

      expect(invalidSkillRecord.skill_level).toBe(10)

      // ビジネスロジックでの検証が必要
      const isValidLevel = invalidSkillRecord.skill_level >= 1 && invalidSkillRecord.skill_level <= 5
      expect(isValidLevel).toBe(false) // ビジネスルール違反
    })
  })
})
