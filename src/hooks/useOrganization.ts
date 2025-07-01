/**
 * 要求仕様ID: API-013
 * 設計書: docs/design/api/specs/API定義書_API-013_組織情報取得API.md
 * 実装内容: 組織情報取得カスタムフック
 */

import { useState, useEffect } from 'react'

export interface Department {
  id: string
  code: string
  name: string
  shortName: string
  level: number
}

export interface Position {
  id: string
  code: string
  name: string
  shortName: string
  level: number
  category: string
}

export interface JobType {
  id: string
  code: string
  name: string
  category: string
  level: string
}

export interface OrganizationData {
  departments: Department[]
  positions: Position[]
  jobTypes: JobType[]
}

export interface UseOrganizationReturn {
  data: OrganizationData | null
  loading: boolean
  error: string | null
  refetch: () => Promise<void>
}

export function useOrganization(): UseOrganizationReturn {
  const [data, setData] = useState<OrganizationData | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  const fetchOrganization = async () => {
    try {
      setLoading(true)
      setError(null)

      console.log('🏢 組織情報を取得中...')
      
      const response = await fetch('/api/organization', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result = await response.json()

      if (!result.success) {
        throw new Error(result.error?.message || '組織情報の取得に失敗しました')
      }

      console.log('✅ 組織情報取得成功:', result.data)
      setData(result.data)

    } catch (err) {
      console.error('❌ 組織情報取得エラー:', err)
      setError(err instanceof Error ? err.message : '組織情報の取得に失敗しました')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchOrganization()
  }, [])

  return {
    data,
    loading,
    error,
    refetch: fetchOrganization
  }
}
