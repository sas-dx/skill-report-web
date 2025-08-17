/**
 * 部下情報表示セクション
 */

'use client';

import React from 'react';
import { Input } from '@/components/ui/Input';

interface Subordinate {
  employee_id: string;
  name: string;
  email: string;
  position: string;
  department: string;
}

interface SubordinatesSectionProps {
  subordinates: Subordinate[];
  isManager: boolean;
  onAddSubordinate?: () => void;
  onEditSubordinate?: (subordinate: Subordinate) => void;
  onRemoveSubordinate?: (employeeId: string) => void;
}

export function SubordinatesSection({
  subordinates,
  isManager,
  onAddSubordinate,
  onEditSubordinate,
  onRemoveSubordinate
}: SubordinatesSectionProps) {
  if (!isManager) {
    return null;
  }

  return (
    <div className="bg-white shadow rounded-lg">
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-lg font-medium text-gray-900">部下情報</h2>
      </div>
      
      <div className="px-6 py-4">
        {subordinates.length === 0 ? (
          <div className="text-gray-500 text-sm">部下情報が設定されていません</div>
        ) : (
          <div className="space-y-6">
            {subordinates.map((subordinate, index) => (
              <div key={subordinate.employee_id} className={index > 0 ? 'pt-6 border-t border-gray-200' : ''}>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      部下名
                    </label>
                    <Input
                      value={subordinate.name}
                      disabled={true}
                      className="bg-gray-50"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      社員番号
                    </label>
                    <Input
                      value={subordinate.employee_id}
                      disabled={true}
                      className="bg-gray-50"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      部署
                    </label>
                    <Input
                      value={subordinate.department}
                      disabled={true}
                      className="bg-gray-50"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      役職
                    </label>
                    <Input
                      value={subordinate.position}
                      disabled={true}
                      className="bg-gray-50"
                    />
                  </div>
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      メールアドレス
                    </label>
                    <Input
                      value={subordinate.email}
                      disabled={true}
                      className="bg-gray-50"
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default SubordinatesSection;