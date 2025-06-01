// PRO.1-BASE.1: プロフィール管理画面
'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { mockProfileData, mockUpdateHistory, type ProfileData, type UpdateHistory } from '@/lib/mockData';

const ProfilePage: React.FC = () => {
  const [profileData, setProfileData] = useState<ProfileData>(mockProfileData);
  const [updateHistory] = useState<UpdateHistory[]>(mockUpdateHistory);
  const [isEditing, setIsEditing] = useState(false);
  const [editedData, setEditedData] = useState<ProfileData>(mockProfileData);

  const handleEdit = () => {
    setIsEditing(true);
    setEditedData(profileData);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditedData(profileData);
  };

  const handleSave = () => {
    // 実際のAPIコールはここで実行
    setProfileData(editedData);
    setIsEditing(false);
    // 成功メッセージ表示（実装時）
    alert('プロフィール情報を保存しました');
  };

  const handleInputChange = (field: keyof ProfileData, value: string) => {
    setEditedData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ja-JP');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ヘッダー */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="py-6">
            <h1 className="text-2xl font-bold text-gray-900">プロフィール管理</h1>
            <p className="mt-1 text-sm text-gray-600">
              個人情報・所属情報の確認・編集を行います
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* メインコンテンツ */}
          <div className="lg:col-span-2 space-y-6">
            {/* 基本情報セクション */}
            <div className="bg-white shadow rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-medium text-gray-900">基本情報</h2>
                  {!isEditing && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handleEdit}
                      className="flex items-center"
                    >
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                      編集
                    </Button>
                  )}
                </div>
              </div>
              <div className="px-6 py-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      社員番号
                    </label>
                    <Input
                      value={isEditing ? editedData.emp_no : profileData.emp_no}
                      onChange={(e) => handleInputChange('emp_no', e.target.value)}
                      disabled={!isEditing}
                      className="w-full"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      氏名（漢字） <span className="text-red-500">*</span>
                    </label>
                    <Input
                      value={isEditing ? editedData.name_kanji : profileData.name_kanji}
                      onChange={(e) => handleInputChange('name_kanji', e.target.value)}
                      disabled={!isEditing}
                      className="w-full"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      氏名（カナ） <span className="text-red-500">*</span>
                    </label>
                    <Input
                      value={isEditing ? editedData.name_kana : profileData.name_kana}
                      onChange={(e) => handleInputChange('name_kana', e.target.value)}
                      disabled={!isEditing}
                      className="w-full"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      氏名（英字）
                    </label>
                    <Input
                      value={isEditing ? editedData.name_english : profileData.name_english}
                      onChange={(e) => handleInputChange('name_english', e.target.value)}
                      disabled={!isEditing}
                      className="w-full"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      メールアドレス <span className="text-red-500">*</span>
                    </label>
                    <Input
                      type="email"
                      value={isEditing ? editedData.email : profileData.email}
                      onChange={(e) => handleInputChange('email', e.target.value)}
                      disabled={!isEditing}
                      className="w-full"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      生年月日
                    </label>
                    <Input
                      type="date"
                      value={isEditing ? editedData.birth_date : profileData.birth_date}
                      onChange={(e) => handleInputChange('birth_date', e.target.value)}
                      disabled={!isEditing}
                      className="w-full"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      入社日
                    </label>
                    <Input
                      type="date"
                      value={isEditing ? editedData.join_date : profileData.join_date}
                      onChange={(e) => handleInputChange('join_date', e.target.value)}
                      disabled={!isEditing}
                      className="w-full"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      電話番号
                    </label>
                    <Input
                      type="tel"
                      value={isEditing ? editedData.phone : profileData.phone}
                      onChange={(e) => handleInputChange('phone', e.target.value)}
                      disabled={!isEditing}
                      className="w-full"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* 所属情報セクション */}
            <div className="bg-white shadow rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-medium text-gray-900">所属情報</h2>
              </div>
              <div className="px-6 py-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      部署名
                    </label>
                    <Input
                      value={isEditing ? editedData.dept_name : profileData.dept_name}
                      onChange={(e) => handleInputChange('dept_name', e.target.value)}
                      disabled={!isEditing}
                      className="w-full"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      役職
                    </label>
                    <Input
                      value={isEditing ? editedData.position_name : profileData.position_name}
                      onChange={(e) => handleInputChange('position_name', e.target.value)}
                      disabled={!isEditing}
                      className="w-full"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      上司名
                    </label>
                    <Input
                      value={isEditing ? editedData.manager_name : profileData.manager_name}
                      onChange={(e) => handleInputChange('manager_name', e.target.value)}
                      disabled={!isEditing}
                      className="w-full"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* 連絡先情報セクション */}
            <div className="bg-white shadow rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-medium text-gray-900">連絡先情報</h2>
              </div>
              <div className="px-6 py-4">
                <div className="grid grid-cols-1 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      緊急連絡先
                    </label>
                    <Input
                      type="tel"
                      value={isEditing ? editedData.emergency_contact : profileData.emergency_contact}
                      onChange={(e) => handleInputChange('emergency_contact', e.target.value)}
                      disabled={!isEditing}
                      className="w-full"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      住所
                    </label>
                    <Input
                      value={isEditing ? editedData.address : profileData.address}
                      onChange={(e) => handleInputChange('address', e.target.value)}
                      disabled={!isEditing}
                      className="w-full"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* 操作ボタン */}
            {isEditing && (
              <div className="bg-white shadow rounded-lg">
                <div className="px-6 py-4">
                  <div className="flex justify-end space-x-3">
                    <Button
                      variant="outline"
                      onClick={handleCancel}
                    >
                      キャンセル
                    </Button>
                    <Button
                      onClick={handleSave}
                    >
                      保存
                    </Button>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* サイドバー */}
          <div className="space-y-6">
            {/* 更新履歴 */}
            <div className="bg-white shadow rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-medium text-gray-900">更新履歴</h2>
              </div>
              <div className="px-6 py-4">
                <div className="space-y-4">
                  {updateHistory.map((history) => (
                    <div key={history.id} className="border-l-4 border-blue-400 pl-4">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium text-gray-900">
                          {history.section}
                        </p>
                        <p className="text-xs text-gray-500">
                          {formatDate(history.updated_at)}
                        </p>
                      </div>
                      <p className="text-sm text-gray-600 mt-1">
                        {history.changes}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        更新者: {history.updated_by}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* 最終更新情報 */}
            <div className="bg-white shadow rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-medium text-gray-900">最終更新情報</h2>
              </div>
              <div className="px-6 py-4">
                <dl className="space-y-2">
                  <div>
                    <dt className="text-sm font-medium text-gray-500">更新日時</dt>
                    <dd className="text-sm text-gray-900">
                      {formatDate(profileData.updated_at)}
                    </dd>
                  </div>
                  <div>
                    <dt className="text-sm font-medium text-gray-500">更新者</dt>
                    <dd className="text-sm text-gray-900">
                      {profileData.updated_by}
                    </dd>
                  </div>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
