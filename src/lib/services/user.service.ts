/**
 * ユーザーサービス（テストサンプル用）
 *
 * このファイルは、Prismaモックを使用したテストの実例を示すためのサンプルです。
 * 実際のプロジェクトでは、より複雑なビジネスロジックが含まれます。
 */

import { prisma } from '@/lib/prisma'
import type { MST_User } from '@prisma/client'

/**
 * ユーザーをIDで取得
 */
export async function getUserById(userId: number): Promise<MST_User | null> {
  return await prisma.mST_User.findUnique({
    where: { user_id: userId },
  })
}

/**
 * すべてのユーザーを取得
 */
export async function getAllUsers(): Promise<MST_User[]> {
  return await prisma.mST_User.findMany({
    orderBy: { user_id: 'asc' },
  })
}

/**
 * 新しいユーザーを作成
 */
export async function createUser(data: {
  employee_id: string
  name: string
  email: string
  role: string
}): Promise<MST_User> {
  return await prisma.mST_User.create({
    data: {
      employee_id: data.employee_id,
      name: data.name,
      email: data.email,
      role: data.role,
    },
  })
}

/**
 * ユーザー数をカウント
 */
export async function countUsers(): Promise<number> {
  return await prisma.mST_User.count()
}

/**
 * ユーザーを削除
 */
export async function deleteUser(userId: number): Promise<MST_User> {
  return await prisma.mST_User.delete({
    where: { user_id: userId },
  })
}
