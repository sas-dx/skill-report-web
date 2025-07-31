/**
 * 要求仕様ID: TNT.1-MGMT
 * 対応設計書: docs/design/screens/specs/画面設計書_SCR-TENANT_テナント管理画面.md
 * 実装内容: テナント管理コンポーネント
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Icons } from '@/components/ui/Icons';

interface Tenant {
  tenant_id: string;
  tenant_code: string;
  tenant_name: string;
  tenant_type: string;
  status: string;
  max_users: number;
  created_at: string;
  updated_at: string;
}

interface TenantFormData {
  tenant_code: string;
  tenant_name: string;
  tenant_short_name: string;
  tenant_type: string;
  domain_name: string;
  admin_email: string;
  max_users: number;
  subscription_plan: string;
}

export function TenantManagement() {
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingTenant, setEditingTenant] = useState<Tenant | null>(null);
  const [formData, setFormData] = useState<TenantFormData>({
    tenant_code: '',
    tenant_name: '',
    tenant_short_name: '',
    tenant_type: 'corporate',
    domain_name: '',
    admin_email: '',
    max_users: 100,
    subscription_plan: 'standard'
  });

  useEffect(() => {
    fetchTenants();
  }, []);

  const fetchTenants = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/tenants');
      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          setTenants(data.tenants || []);
        } else {
          console.error('テナント取得エラー:', data.error);
        }
      }
    } catch (error) {
      console.error('テナント一覧の取得に失敗しました:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const url = editingTenant 
        ? `/api/tenants/${editingTenant.tenant_id}`
        : '/api/tenants';
      
      const method = editingTenant ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        await fetchTenants();
        setShowForm(false);
        setEditingTenant(null);
        resetForm();
      } else {
        const error = await response.json();
        alert(`エラー: ${error.message}`);
      }
    } catch (error) {
      console.error('テナント保存に失敗しました:', error);
      alert('テナント保存に失敗しました');
    }
  };

  const handleEdit = async (tenant: Tenant) => {
    try {
      // 個別テナント情報を取得
      const response = await fetch(`/api/tenants/${tenant.tenant_id}`);
      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          const fullTenant = data.tenant;
          setEditingTenant(tenant);
          setFormData({
            tenant_code: fullTenant.tenant_code || '',
            tenant_name: fullTenant.tenant_name || '',
            tenant_short_name: fullTenant.tenant_short_name || '',
            tenant_type: fullTenant.tenant_type || 'corporate',
            domain_name: fullTenant.domain_name || '',
            admin_email: fullTenant.admin_email || '',
            max_users: fullTenant.max_users || 100,
            subscription_plan: fullTenant.subscription_plan || 'standard'
          });
          setShowForm(true);
        } else {
          console.error('テナント詳細取得エラー:', data.error);
          alert('テナント情報の取得に失敗しました');
        }
      } else {
        console.error('テナント詳細取得失敗:', response.status);
        alert('テナント情報の取得に失敗しました');
      }
    } catch (error) {
      console.error('テナント詳細取得エラー:', error);
      alert('テナント情報の取得に失敗しました');
    }
  };

  const handleDelete = async (tenantId: string) => {
    if (!confirm('このテナントを削除してもよろしいですか？')) {
      return;
    }

    try {
      const response = await fetch(`/api/tenants/${tenantId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        await fetchTenants();
      } else {
        const error = await response.json();
        alert(`エラー: ${error.message}`);
      }
    } catch (error) {
      console.error('テナント削除に失敗しました:', error);
      alert('テナント削除に失敗しました');
    }
  };

  const resetForm = () => {
    setFormData({
      tenant_code: '',
      tenant_name: '',
      tenant_short_name: '',
      tenant_type: 'corporate',
      domain_name: '',
      admin_email: '',
      max_users: 100,
      subscription_plan: 'standard'
    });
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingTenant(null);
    resetForm();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* ヘッダー */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">テナント管理</h1>
        <Button
          onClick={() => setShowForm(true)}
          className="bg-blue-600 hover:bg-blue-700"
        >
          <Icons.Plus className="w-4 h-4 mr-2" />
          新規テナント作成
        </Button>
      </div>

      {/* テナント作成・編集フォーム */}
      {showForm && (
        <div className="bg-white p-6 rounded-lg shadow-md border">
          <h2 className="text-lg font-semibold mb-4">
            {editingTenant ? 'テナント編集' : '新規テナント作成'}
          </h2>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  テナントコード *
                </label>
                <Input
                  type="text"
                  value={formData.tenant_code}
                  onChange={(e) => setFormData({ ...formData, tenant_code: e.target.value })}
                  required
                  placeholder="例: company-001"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  テナント名 *
                </label>
                <Input
                  type="text"
                  value={formData.tenant_name}
                  onChange={(e) => setFormData({ ...formData, tenant_name: e.target.value })}
                  required
                  placeholder="例: 株式会社サンプル"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  テナント短縮名
                </label>
                <Input
                  type="text"
                  value={formData.tenant_short_name}
                  onChange={(e) => setFormData({ ...formData, tenant_short_name: e.target.value })}
                  placeholder="例: Sample Corp"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  タイプ *
                </label>
                <Select
                  value={formData.tenant_type}
                  onChange={(value) => setFormData({ ...formData, tenant_type: value })}
                >
                  <option value="corporate">企業</option>
                  <option value="government">官公庁</option>
                  <option value="nonprofit">非営利団体</option>
                  <option value="educational">教育機関</option>
                  <option value="healthcare">医療機関</option>
                  <option value="other">その他</option>
                </Select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  ドメイン名 *
                </label>
                <Input
                  type="text"
                  value={formData.domain_name}
                  onChange={(e) => setFormData({ ...formData, domain_name: e.target.value })}
                  required
                  placeholder="例: sample.com"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  管理者メールアドレス *
                </label>
                <Input
                  type="email"
                  value={formData.admin_email}
                  onChange={(e) => setFormData({ ...formData, admin_email: e.target.value })}
                  required
                  placeholder="例: admin@sample.com"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  最大ユーザー数
                </label>
                <Input
                  type="number"
                  value={formData.max_users}
                  onChange={(e) => setFormData({ ...formData, max_users: parseInt(e.target.value) || 0 })}
                  min="1"
                  placeholder="100"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  サブスクリプションプラン
                </label>
                <Select
                  value={formData.subscription_plan}
                  onChange={(value) => setFormData({ ...formData, subscription_plan: value })}
                >
                  <option value="basic">ベーシック</option>
                  <option value="standard">スタンダード</option>
                  <option value="premium">プレミアム</option>
                  <option value="enterprise">エンタープライズ</option>
                </Select>
              </div>
            </div>
            
            <div className="flex justify-end space-x-3 pt-4">
              <Button
                type="button"
                variant="secondary"
                onClick={handleCancel}
              >
                キャンセル
              </Button>
              <Button
                type="submit"
                className="bg-blue-600 hover:bg-blue-700"
              >
                {editingTenant ? '更新' : '作成'}
              </Button>
            </div>
          </form>
        </div>
      )}

      {/* テナント一覧 */}
      <div className="bg-white rounded-lg shadow-md border">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold">テナント一覧</h2>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  テナントコード
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  テナント名
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  タイプ
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  ステータス
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  最大ユーザー数
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  作成日
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  操作
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {tenants.map((tenant) => (
                <tr key={tenant.tenant_id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {tenant.tenant_code}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {tenant.tenant_name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                      {tenant.tenant_type}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      tenant.status === 'active' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {tenant.status === 'active' ? 'アクティブ' : '無効'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {tenant.max_users}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {new Date(tenant.created_at).toLocaleDateString('ja-JP')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div className="flex justify-end space-x-2">
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => handleEdit(tenant)}
                      >
                        <Icons.Edit className="w-4 h-4" />
                      </Button>
                      <Button
                        variant="danger"
                        size="sm"
                        onClick={() => handleDelete(tenant.tenant_id)}
                      >
                        <Icons.Trash className="w-4 h-4" />
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          
          {tenants.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              テナントが登録されていません
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
