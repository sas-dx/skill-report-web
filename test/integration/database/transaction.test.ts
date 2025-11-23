/**
 * Prismaトランザクション統合テスト
 *
 * テスト計画書 5.1節に基づく実装
 * - 複数レコード一括作成のトランザクション
 * - エラー時の自動ロールバック
 * - Prismaエラーハンドリング
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
  createTestSkillItem
} from '@/test/helpers'

describe('DB-001: Prismaトランザクション統合テスト', () => {
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

    // テストデータ準備
    testTenant = await createTestTenant(prisma, {
      tenant_code: 'TENANT_TXN_001',
      tenant_name: 'トランザクションテスト用テナント'
    })

    testEmployee1 = await createTestEmployee(prisma, {
      tenant_id: testTenant.id,
      employee_code: 'TXN_EMP_001',
      full_name: 'トランザクションテストユーザー1'
    })

    testEmployee2 = await createTestEmployee(prisma, {
      tenant_id: testTenant.id,
      employee_code: 'TXN_EMP_002',
      full_name: 'トランザクションテストユーザー2'
    })
  })

  describe('複数レコード一括作成', () => {
    it('正常系: トランザクション内で複数の作業実績レコード作成成功', async () => {
      const timestamp = Date.now()

      // トランザクション実行
      const result = await prisma.$transaction(async (tx) => {
        const project1 = await tx.tRN_ProjectRecord.create({
          data: {
            id: `txn_proj_1_${timestamp}`,
            project_record_id: `PRJ_TXN_001_${timestamp}`,
            tenant_id: testTenant.id,
            employee_id: testEmployee1.id,
            project_name: 'トランザクションテストプロジェクト1',
            project_code: `PRJ_TXN_001_${timestamp}`,
            project_type: 'DEVELOPMENT',
            start_date: new Date('2025-01-01'),
            end_date: new Date('2025-12-31'),
            role_title: 'エンジニア',
            project_status: 'ACTIVE',
            created_by: testEmployee1.id,
            updated_by: testEmployee1.id,
            is_deleted: false
          }
        })

        const project2 = await tx.tRN_ProjectRecord.create({
          data: {
            id: `txn_proj_2_${timestamp}`,
            project_record_id: `PRJ_TXN_002_${timestamp}`,
            tenant_id: testTenant.id,
            employee_id: testEmployee1.id,
            project_name: 'トランザクションテストプロジェクト2',
            project_code: `PRJ_TXN_002_${timestamp}`,
            project_type: 'CONSULTING',
            start_date: new Date('2025-02-01'),
            end_date: new Date('2025-11-30'),
            role_title: 'コンサルタント',
            project_status: 'ACTIVE',
            created_by: testEmployee1.id,
            updated_by: testEmployee1.id,
            is_deleted: false
          }
        })

        const project3 = await tx.tRN_ProjectRecord.create({
          data: {
            id: `txn_proj_3_${timestamp}`,
            project_record_id: `PRJ_TXN_003_${timestamp}`,
            tenant_id: testTenant.id,
            employee_id: testEmployee2.id,
            project_name: 'トランザクションテストプロジェクト3',
            project_code: `PRJ_TXN_003_${timestamp}`,
            project_type: 'MAINTENANCE',
            start_date: new Date('2025-03-01'),
            end_date: new Date('2025-10-31'),
            role_title: 'プロジェクトマネージャー',
            project_status: 'ACTIVE',
            created_by: testEmployee2.id,
            updated_by: testEmployee2.id,
            is_deleted: false
          }
        })

        return { project1, project2, project3 }
      })

      // トランザクション成功確認
      expect(result.project1).toBeTruthy()
      expect(result.project1.project_name).toBe('トランザクションテストプロジェクト1')
      expect(result.project2).toBeTruthy()
      expect(result.project2.project_name).toBe('トランザクションテストプロジェクト2')
      expect(result.project3).toBeTruthy()
      expect(result.project3.project_name).toBe('トランザクションテストプロジェクト3')

      // データが実際に保存されていることを確認
      const projects = await prisma.tRN_ProjectRecord.findMany({
        where: {
          employee_id: { in: [testEmployee1.id, testEmployee2.id] },
          is_deleted: false
        },
        orderBy: { created_at: 'asc' }
      })

      expect(projects).toHaveLength(3)
      expect(projects[0].project_name).toBe('トランザクションテストプロジェクト1')
      expect(projects[1].project_name).toBe('トランザクションテストプロジェクト2')
      expect(projects[2].project_name).toBe('トランザクションテストプロジェクト3')
    })

    it('正常系: 複数テーブルにまたがるトランザクション成功', async () => {
      const timestamp = Date.now()

      // スキルカテゴリとスキルアイテム作成
      const category = await createTestSkillCategory(prisma, testTenant.id, 'system', {
        category_code: `CAT_TXN_${timestamp}`,
        category_name: 'トランザクションテスト用カテゴリ'
      })

      // 複数テーブルにまたがるトランザクション
      const result = await prisma.$transaction(async (tx) => {
        // スキルアイテム作成
        const skillItem = await tx.mST_SkillItem.create({
          data: {
            id: `skill_item_txn_${timestamp}`,
            skill_item_id: `SKILL_TXN_${timestamp}`,
            tenant_id: testTenant.id,
            category_id: category.id,
            skill_name: 'トランザクションテストスキル',
            skill_name_en: 'Transaction Test Skill',
            skill_type: 'TECHNICAL',
            difficulty_level: 3,
            is_core_skill: true,
            is_active: true,
            created_by: 'system',
            updated_by: 'system',
            is_deleted: false
          }
        })

        // スキルレコード作成
        const skillRecord = await tx.tRN_SkillRecord.create({
          data: {
            id: `skill_record_txn_${timestamp}`,
            skill_record_id: `SKILL_REC_TXN_${timestamp}`,
            tenant_id: testTenant.id,
            employee_id: testEmployee1.id,
            skill_item_id: skillItem.id,
            skill_level: 3,
            self_assessment: 3,
            manager_assessment: 3,
            acquisition_date: new Date(),
            last_used_date: new Date(),
            skill_status: 'ACTIVE',
            created_by: testEmployee1.id,
            updated_by: testEmployee1.id,
            is_deleted: false
          }
        })

        return { skillItem, skillRecord }
      })

      // 両方のレコードが作成されていることを確認
      expect(result.skillItem).toBeTruthy()
      expect(result.skillRecord).toBeTruthy()
      expect(result.skillRecord.skill_item_id).toBe(result.skillItem.id)

      // データベースに保存されていることを確認
      const savedSkillItem = await prisma.mST_SkillItem.findUnique({
        where: { id: result.skillItem.id }
      })
      const savedSkillRecord = await prisma.tRN_SkillRecord.findUnique({
        where: { id: result.skillRecord.id }
      })

      expect(savedSkillItem).toBeTruthy()
      expect(savedSkillRecord).toBeTruthy()
    })
  })

  describe('トランザクションロールバック', () => {
    it('異常系: トランザクション内でエラー発生時は全てロールバック', async () => {
      const timestamp = Date.now()

      // トランザクション実行（エラー発生を期待）
      await expect(
        prisma.$transaction(async (tx) => {
          // 1つ目は成功
          await tx.tRN_ProjectRecord.create({
            data: {
              id: `txn_rollback_1_${timestamp}`,
              project_record_id: `PRJ_ROLLBACK_001_${timestamp}`,
              tenant_id: testTenant.id,
              employee_id: testEmployee1.id,
              project_name: 'ロールバックテスト1',
              project_code: `PRJ_ROLLBACK_001_${timestamp}`,
              project_type: 'DEVELOPMENT',
              start_date: new Date(),
              role_title: 'エンジニア',
              project_status: 'ACTIVE',
              created_by: testEmployee1.id,
              updated_by: testEmployee1.id,
              is_deleted: false
            }
          })

          // 2つ目も成功
          await tx.tRN_ProjectRecord.create({
            data: {
              id: `txn_rollback_2_${timestamp}`,
              project_record_id: `PRJ_ROLLBACK_002_${timestamp}`,
              tenant_id: testTenant.id,
              employee_id: testEmployee1.id,
              project_name: 'ロールバックテスト2',
              project_code: `PRJ_ROLLBACK_002_${timestamp}`,
              project_type: 'CONSULTING',
              start_date: new Date(),
              role_title: 'コンサルタント',
              project_status: 'ACTIVE',
              created_by: testEmployee1.id,
              updated_by: testEmployee1.id,
              is_deleted: false
            }
          })

          // 3つ目で意図的にエラー発生（重複ID）
          await tx.tRN_ProjectRecord.create({
            data: {
              id: `txn_rollback_1_${timestamp}`, // 重複ID
              project_record_id: `PRJ_ROLLBACK_003_${timestamp}`,
              tenant_id: testTenant.id,
              employee_id: testEmployee1.id,
              project_name: 'ロールバックテスト3',
              project_code: `PRJ_ROLLBACK_003_${timestamp}`,
              project_type: 'MAINTENANCE',
              start_date: new Date(),
              role_title: 'PM',
              project_status: 'ACTIVE',
              created_by: testEmployee1.id,
              updated_by: testEmployee1.id,
              is_deleted: false
            }
          })
        })
      ).rejects.toThrow()

      // ロールバックされていることを確認（どのレコードも保存されていない）
      const projects = await prisma.tRN_ProjectRecord.findMany({
        where: {
          employee_id: testEmployee1.id,
          project_name: { contains: 'ロールバックテスト' },
          is_deleted: false
        }
      })

      expect(projects).toHaveLength(0)
    })

    it('異常系: 外部キー制約違反でロールバック', async () => {
      const timestamp = Date.now()

      await expect(
        prisma.$transaction(async (tx) => {
          // 存在しない社員IDでレコード作成を試みる
          await tx.tRN_ProjectRecord.create({
            data: {
              id: `txn_fk_error_${timestamp}`,
              project_record_id: `PRJ_FK_ERROR_${timestamp}`,
              tenant_id: testTenant.id,
              employee_id: 'NONEXISTENT_EMPLOYEE_ID',
              project_name: '外部キーエラーテスト',
              project_code: `PRJ_FK_ERROR_${timestamp}`,
              project_type: 'DEVELOPMENT',
              start_date: new Date(),
              role_title: 'エンジニア',
              project_status: 'ACTIVE',
              created_by: 'NONEXISTENT_EMPLOYEE_ID',
              updated_by: 'NONEXISTENT_EMPLOYEE_ID',
              is_deleted: false
            }
          })
        })
      ).rejects.toThrow()

      // レコードが保存されていないことを確認
      const projects = await prisma.tRN_ProjectRecord.findMany({
        where: {
          project_name: '外部キーエラーテスト',
          is_deleted: false
        }
      })

      expect(projects).toHaveLength(0)
    })
  })

  describe('Prismaエラーハンドリング', () => {
    it('正常系: P2002 (一意制約違反) を適切にハンドリング', async () => {
      const timestamp = Date.now()
      const uniqueCode = `UNIQUE_${timestamp}`

      // 1つ目のスキルカテゴリ作成
      await createTestSkillCategory(prisma, testTenant.id, 'system', {
        category_code: uniqueCode,
        category_name: '一意制約テスト'
      })

      // 同じcategory_codeで2つ目を作成しようとする
      try {
        await prisma.mST_SkillCategory.create({
          data: {
            id: `duplicate_cat_${timestamp}`,
            category_id: `CAT_DUPLICATE_${timestamp}`,
            tenant_id: testTenant.id,
            category_code: uniqueCode, // 重複
            category_name: '一意制約テスト2',
            category_name_en: 'Unique Constraint Test 2',
            display_order: 1,
            is_active: true,
            created_by: 'system',
            updated_by: 'system',
            is_deleted: false
          }
        })
        // エラーが発生しなければテスト失敗
        fail('一意制約違反のエラーが発生すべきです')
      } catch (error) {
        // Prismaの一意制約違反エラーを確認
        if (error instanceof Prisma.PrismaClientKnownRequestError) {
          expect(error.code).toBe('P2002')
          expect(error.meta).toBeTruthy()
        } else {
          throw error
        }
      }
    })

    it('正常系: P2025 (レコードが見つからない) を適切にハンドリング', async () => {
      const nonexistentId = 'NONEXISTENT_ID_12345'

      try {
        await prisma.tRN_ProjectRecord.update({
          where: { id: nonexistentId },
          data: { project_name: '更新テスト' }
        })
        fail('レコードが見つからないエラーが発生すべきです')
      } catch (error) {
        if (error instanceof Prisma.PrismaClientKnownRequestError) {
          expect(error.code).toBe('P2025')
        } else {
          throw error
        }
      }
    })

    it('正常系: トランザクション内でのエラーハンドリングとリトライ', async () => {
      const timestamp = Date.now()
      let attemptCount = 0
      const maxAttempts = 3

      const executeWithRetry = async (): Promise<any> => {
        attemptCount++

        try {
          return await prisma.$transaction(async (tx) => {
            // 1回目は意図的に失敗させる
            if (attemptCount === 1) {
              throw new Error('Simulated transaction error')
            }

            // 2回目以降は成功
            const project = await tx.tRN_ProjectRecord.create({
              data: {
                id: `txn_retry_${timestamp}`,
                project_record_id: `PRJ_RETRY_${timestamp}`,
                tenant_id: testTenant.id,
                employee_id: testEmployee1.id,
                project_name: 'リトライテスト',
                project_code: `PRJ_RETRY_${timestamp}`,
                project_type: 'DEVELOPMENT',
                start_date: new Date(),
                role_title: 'エンジニア',
                project_status: 'ACTIVE',
                created_by: testEmployee1.id,
                updated_by: testEmployee1.id,
                is_deleted: false
              }
            })

            return project
          })
        } catch (error) {
          if (attemptCount < maxAttempts) {
            // リトライ
            return await executeWithRetry()
          }
          throw error
        }
      }

      const result = await executeWithRetry()

      // 2回試行されたことを確認
      expect(attemptCount).toBe(2)
      expect(result).toBeTruthy()
      expect(result.project_name).toBe('リトライテスト')

      // データベースに保存されていることを確認
      const savedProject = await prisma.tRN_ProjectRecord.findUnique({
        where: { id: result.id }
      })
      expect(savedProject).toBeTruthy()
    })
  })

  describe('インタラクティブトランザクション（Interactive Transaction）', () => {
    it('正常系: 条件付きロジックを含むトランザクション', async () => {
      const timestamp = Date.now()

      const result = await prisma.$transaction(async (tx) => {
        // 社員1の作業実績を作成
        const project1 = await tx.tRN_ProjectRecord.create({
          data: {
            id: `interactive_1_${timestamp}`,
            project_record_id: `PRJ_INTERACTIVE_1_${timestamp}`,
            tenant_id: testTenant.id,
            employee_id: testEmployee1.id,
            project_name: '条件付きトランザクション1',
            project_code: `PRJ_INTERACTIVE_1_${timestamp}`,
            project_type: 'DEVELOPMENT',
            start_date: new Date(),
            role_title: 'エンジニア',
            project_status: 'ACTIVE',
            created_by: testEmployee1.id,
            updated_by: testEmployee1.id,
            is_deleted: false
          }
        })

        // 社員1の作業実績数を確認
        const employee1ProjectCount = await tx.tRN_ProjectRecord.count({
          where: {
            employee_id: testEmployee1.id,
            is_deleted: false
          }
        })

        // 社員1の作業実績が1件以上ある場合のみ、社員2の作業実績を作成
        let project2 = null
        if (employee1ProjectCount > 0) {
          project2 = await tx.tRN_ProjectRecord.create({
            data: {
              id: `interactive_2_${timestamp}`,
              project_record_id: `PRJ_INTERACTIVE_2_${timestamp}`,
              tenant_id: testTenant.id,
              employee_id: testEmployee2.id,
              project_name: '条件付きトランザクション2',
              project_code: `PRJ_INTERACTIVE_2_${timestamp}`,
              project_type: 'CONSULTING',
              start_date: new Date(),
              role_title: 'コンサルタント',
              project_status: 'ACTIVE',
              created_by: testEmployee2.id,
              updated_by: testEmployee2.id,
              is_deleted: false
            }
          })
        }

        return { project1, project2, employee1ProjectCount }
      })

      // 条件が満たされたため、両方のプロジェクトが作成されている
      expect(result.project1).toBeTruthy()
      expect(result.project2).toBeTruthy()
      expect(result.employee1ProjectCount).toBeGreaterThan(0)

      // データベースに保存されていることを確認
      const projects = await prisma.tRN_ProjectRecord.findMany({
        where: {
          employee_id: { in: [testEmployee1.id, testEmployee2.id] },
          is_deleted: false
        }
      })
      expect(projects).toHaveLength(2)
    })

    it('正常系: 集計とデータ作成を組み合わせたトランザクション', async () => {
      const timestamp = Date.now()

      // 事前にテストデータ作成
      const category = await createTestSkillCategory(prisma, testTenant.id, 'system', {
        category_code: `CAT_AGG_${timestamp}`,
        category_name: '集計テスト用カテゴリ'
      })

      const skillItem = await createTestSkillItem(
        prisma,
        category.id,
        testTenant.id,
        'system',
        {
          skill_item_id: `SKILL_AGG_${timestamp}`,
          skill_name: '集計テストスキル'
        }
      )

      // トランザクション内で集計とデータ作成
      const result = await prisma.$transaction(async (tx) => {
        // 既存のスキルレコード数を集計
        const existingCount = await tx.tRN_SkillRecord.count({
          where: {
            employee_id: testEmployee1.id,
            is_deleted: false
          }
        })

        // 新しいスキルレコードを作成
        const newRecord = await tx.tRN_SkillRecord.create({
          data: {
            id: `skill_agg_${timestamp}`,
            skill_record_id: `SKILL_REC_AGG_${timestamp}`,
            tenant_id: testTenant.id,
            employee_id: testEmployee1.id,
            skill_item_id: skillItem.id,
            skill_level: 3,
            self_assessment: 3,
            manager_assessment: 3,
            acquisition_date: new Date(),
            last_used_date: new Date(),
            skill_status: 'ACTIVE',
            created_by: testEmployee1.id,
            updated_by: testEmployee1.id,
            is_deleted: false
          }
        })

        // 作成後の件数を確認
        const newCount = await tx.tRN_SkillRecord.count({
          where: {
            employee_id: testEmployee1.id,
            is_deleted: false
          }
        })

        return { existingCount, newRecord, newCount }
      })

      // 件数が1件増えていることを確認
      expect(result.newCount).toBe(result.existingCount + 1)
      expect(result.newRecord).toBeTruthy()
    })
  })
})
