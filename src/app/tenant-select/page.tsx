/**
 * 要求仕様ID: TNT.1-SELECT
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_TNT_Select_テナント選択画面.md
 * 実装内容: テナント選択画面
 */

'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Spinner } from '@/components/ui/Spinner';
import { SearchIcon, BuildingOfficeIcon, GlobeIcon, ArrowRightIcon } from '@/components/ui/Icons';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { Sidebar } from '@/components/dashboard/Sidebar';

interface Tenant {
  tenant_id: string;
  tenant_code: string;
  tenant_name: string;
  tenant_short_name: string;
  domain_name: string;
  status: string;
  subscription_plan: string;
}

export default function TenantSelectPage() {
  const router = useRouter();
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredTenants, setFilteredTenants] = useState<Tenant[]>([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // テナント一覧取得
  const fetchTenants = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/tenants?status=active&limit=100');
      const data = await response.json();

      if (data.success) {
        setTenants(data.tenants || []);
        setFilteredTenants(data.tenants || []);
      } else {
        console.error('テナント取得エラー:', data.error);
      }
    } catch (error) {
      console.error('テナント取得エラー:', error);
    } finally {
      setLoading(false);
    }
  };

  // 初期データ読み込み
  useEffect(() => {
    fetchTenants();
  }, []);

  // 検索フィルタリング
  useEffect(() => {
    if (!searchTerm) {
      setFilteredTenants(tenants);
    } else {
      const filtered = tenants.filter(
        (tenant) =>
          tenant.tenant_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          tenant.tenant_code.toLowerCase().includes(searchTerm.toLowerCase()) ||
          tenant.domain_name.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredTenants(filtered);
    }
  }, [searchTerm, tenants]);

  // テナント選択
  const handleTenantSelect = (tenant: Tenant) => {
    // テナント情報をローカルストレージに保存
    localStorage.setItem('selectedTenant', JSON.stringify(tenant));
    
    // ダッシュボードにリダイレクト
    router.push('/dashboard');
  };

  // プラン表示用のバッジ
  const getPlanBadge = (plan: string) => {
    const planConfig = {
      basic: { label: 'Basic', className: 'bg-gray-100 text-gray-800' },
      standard: { label: 'Standard', className: 'bg-blue-100 text-blue-800' },
      premium: { label: 'Premium', className: 'bg-purple-100 text-purple-800' },
      enterprise: { label: 'Enterprise', className: 'bg-green-100 text-green-800' },
    };

    const config = planConfig[plan as keyof typeof planConfig] || planConfig.basic;

    return (
      <span className={`px-2 py-1 text-xs font-medium rounded-full ${config.className}`}>
        {config.label}
      </span>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ダッシュボードヘッダー */}
      <DashboardHeader 
        onMenuClick={() => setSidebarOpen(true)}
        title="テナント選択"
      />

      {/* サイドバー */}
      <Sidebar 
        isOpen={sidebarOpen} 
        onClose={() => setSidebarOpen(false)} 
      />

      {/* メインコンテンツ */}
      <div className="pt-16 lg:pl-64">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* ページタイトル */}
          <div className="mb-8">
            <div className="text-center">
              <h1 className="text-3xl font-bold text-gray-900">テナント選択</h1>
              <p className="mt-2 text-lg text-gray-600">
                アクセスするテナント（組織）を選択してください
              </p>
            </div>
          </div>

          {/* 検索バー */}
          <div className="mb-8">
            <div className="relative max-w-md mx-auto">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <SearchIcon className="h-5 w-5 text-gray-400" />
              </div>
              <Input
                type="text"
                placeholder="テナント名、コード、ドメインで検索..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 w-full"
              />
            </div>
          </div>

          {/* テナント一覧 */}
          {loading ? (
            <div className="flex justify-center items-center py-12">
              <Spinner size="lg" />
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredTenants.length === 0 ? (
                <div className="col-span-full text-center py-12">
                  <BuildingOfficeIcon className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">
                    テナントが見つかりません
                  </h3>
                  <p className="mt-1 text-sm text-gray-500">
                    検索条件を変更してお試しください。
                  </p>
                </div>
              ) : (
                filteredTenants.map((tenant) => (
                  <div
                    key={tenant.tenant_id}
                    className="bg-white rounded-lg shadow hover:shadow-md transition-shadow duration-200 cursor-pointer"
                    onClick={() => handleTenantSelect(tenant)}
                  >
                    <div className="p-6">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center">
                          <div className="flex-shrink-0">
                            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                              <BuildingOfficeIcon className="w-6 h-6 text-blue-600" />
                            </div>
                          </div>
                          <div className="ml-3">
                            <h3 className="text-lg font-medium text-gray-900">
                              {tenant.tenant_name}
                            </h3>
                            <p className="text-sm text-gray-500">
                              {tenant.tenant_code}
                            </p>
                          </div>
                        </div>
                        {getPlanBadge(tenant.subscription_plan)}
                      </div>

                      <div className="space-y-2">
                        <div className="flex items-center text-sm text-gray-600">
                          <GlobeIcon className="w-4 h-4 mr-2" />
                          {tenant.domain_name}
                        </div>
                      </div>

                      <div className="mt-6">
                        <Button
                          variant="primary"
                          className="w-full"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleTenantSelect(tenant);
                          }}
                        >
                          <ArrowRightIcon className="w-4 h-4 mr-2" />
                          このテナントでログイン
                        </Button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}

          {/* フッター */}
          <div className="mt-12 text-center">
            <p className="text-sm text-gray-500">
              アクセス権限のないテナントは表示されません。
            </p>
            <p className="text-sm text-gray-500 mt-1">
              新しいテナントへのアクセスが必要な場合は、システム管理者にお問い合わせください。
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
