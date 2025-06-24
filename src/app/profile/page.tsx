/**
 * 要求仕様ID: PRO.1-BASE.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR-PROFILE_プロフィール画面.md
 * 実装内容: プロフィール画面（実際のAPI連携版）
 */
'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { Sidebar } from '@/components/dashboard/Sidebar';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Spinner } from '@/components/ui/Spinner';
import { getProfile, updateProfile, ProfileData, ProfileUpdateRequest } from '@/lib/api/profile';

interface EditableProfile {
  firstName: string;
  lastName: string;
  firstNameKana: string;
  lastNameKana: string;
  displayName: string;
  phoneNumber: string;
  emergencyContactName: string;
  emergencyContactPhone: string;
}

export default function ProfilePage() {
  const router = useRouter();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [editedProfile, setEditedProfile] = useState<EditableProfile | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});

  const handleMenuClick = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleSidebarClose = () => {
    setIsSidebarOpen(false);
  };

  // プロフィール情報の読み込み
  useEffect(() => {
    const loadProfile = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const response = await getProfile('me', {
          includeSkillSummary: true,
          includeGoalSummary: false,
          includeHistory: false
        });
        
        if (response.success && response.data) {
          setProfile(response.data.profile);
          setEditedProfile({
            firstName: response.data.profile.personalInfo.firstName,
            lastName: response.data.profile.personalInfo.lastName,
            firstNameKana: response.data.profile.personalInfo.firstNameKana,
            lastNameKana: response.data.profile.personalInfo.lastNameKana,
            displayName: response.data.profile.personalInfo.displayName,
            phoneNumber: response.data.profile.personalInfo.phoneNumber,
            emergencyContactName: response.data.profile.personalInfo.emergencyContact.name,
            emergencyContactPhone: response.data.profile.personalInfo.emergencyContact.phoneNumber,
          });
        } else {
          setError(response.error?.message || 'プロフィール情報の取得に失敗しました');
        }
      } catch (error) {
        console.error('プロフィール読み込みエラー:', error);
        setError('プロフィール情報の読み込み中にエラーが発生しました');
      } finally {
        setIsLoading(false);
      }
    };

    loadProfile();
  }, []);

  const handleEdit = () => {
    setIsEditing(true);
    setValidationErrors({});
  };

  const handleCancel = () => {
    if (profile) {
      setEditedProfile({
        firstName: profile.personalInfo.firstName,
        lastName: profile.personalInfo.lastName,
        firstNameKana: profile.personalInfo.firstNameKana,
        lastNameKana: profile.personalInfo.lastNameKana,
        displayName: profile.personalInfo.displayName,
        phoneNumber: profile.personalInfo.phoneNumber,
        emergencyContactName: profile.personalInfo.emergencyContact.name,
        emergencyContactPhone: profile.personalInfo.emergencyContact.phoneNumber,
      });
    }
    setIsEditing(false);
    setValidationErrors({});
  };

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};
    
    if (!editedProfile?.firstName?.trim()) {
      errors.firstName = '名前（名）は必須です';
    }
    
    if (!editedProfile?.lastName?.trim()) {
      errors.lastName = '名前（姓）は必須です';
    }
    
    if (!editedProfile?.displayName?.trim()) {
      errors.displayName = '表示名は必須です';
    }
    
    if (editedProfile?.phoneNumber && !/^[\d-+()]+$/.test(editedProfile.phoneNumber)) {
      errors.phoneNumber = '電話番号の形式が正しくありません';
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSave = async () => {
    if (!editedProfile || !validateForm()) return;
    
    setIsSaving(true);
    try {
      const updateData: ProfileUpdateRequest = {
        first_name: editedProfile.firstName,
        last_name: editedProfile.lastName,
        first_name_kana: editedProfile.firstNameKana,
        last_name_kana: editedProfile.lastNameKana,
        display_name: editedProfile.displayName,
        contact_info: {
          phone: editedProfile.phoneNumber
        }
      };

      const response = await updateProfile('me', updateData);
      
      if (response.success) {
        // プロフィール情報を再読み込み
        const updatedProfile = await getProfile('me');
        if (updatedProfile.success && updatedProfile.data) {
          setProfile(updatedProfile.data.profile);
        }
        setIsEditing(false);
        setError(null);
      } else {
        setError(response.error?.message || 'プロフィール更新に失敗しました');
      }
    } catch (error) {
      console.error('プロフィール保存エラー:', error);
      setError('プロフィール保存中にエラーが発生しました');
    } finally {
      setIsSaving(false);
    }
  };

  const handleInputChange = (field: keyof EditableProfile, value: string) => {
    if (!editedProfile) return;
    
    setEditedProfile({
      ...editedProfile,
      [field]: value
    });
    
    // バリデーションエラーをクリア
    if (validationErrors[field]) {
      setValidationErrors({
        ...validationErrors,
        [field]: ''
      });
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <DashboardHeader 
          onMenuClick={handleMenuClick}
          title="プロフィール"
        />
        <div className="flex pt-16">
          <Sidebar 
            isOpen={isSidebarOpen}
            onClose={handleSidebarClose}
          />
          <div className="flex-1 lg:ml-64 flex items-center justify-center">
            <Spinner size="lg" />
          </div>
        </div>
      </div>
    );
  }

  if (error && !profile) {
    return (
      <div className="min-h-screen bg-gray-50">
        <DashboardHeader 
          onMenuClick={handleMenuClick}
          title="プロフィール"
        />
        <div className="flex pt-16">
          <Sidebar 
            isOpen={isSidebarOpen}
            onClose={handleSidebarClose}
          />
          <div className="flex-1 lg:ml-64 flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-xl font-semibold text-gray-900 mb-2">プロフィールが見つかりません</h2>
              <p className="text-gray-600 mb-4">{error}</p>
              <Button onClick={() => window.location.reload()} variant="primary">
                再読み込み
              </Button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ヘッダー - 最上部に固定 */}
      <DashboardHeader 
        onMenuClick={handleMenuClick}
        title="プロフィール"
      />

      {/* メインレイアウト - ヘッダーの下 */}
      <div className="flex pt-16">
        {/* サイドバー */}
        <Sidebar 
          isOpen={isSidebarOpen}
          onClose={handleSidebarClose}
        />

        {/* メインコンテンツエリア */}
        <div className="flex-1 lg:ml-64">
          <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
            {/* エラー表示 */}
            {error && (
              <div className="mb-6 bg-red-50 border border-red-200 rounded-md p-4">
                <div className="flex">
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">エラー</h3>
                    <div className="mt-2 text-sm text-red-700">
                      <p>{error}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* ページヘッダー */}
            <div className="mb-8">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">プロフィール</h1>
                  <p className="text-gray-600 mt-1">個人情報とスキル概要を管理します</p>
                </div>
                <div className="flex space-x-3">
                  {!isEditing ? (
                    <Button onClick={handleEdit} variant="primary">
                      編集
                    </Button>
                  ) : (
                    <>
                      <Button onClick={handleCancel} variant="secondary">
                        キャンセル
                      </Button>
                      <Button 
                        onClick={handleSave} 
                        variant="primary"
                        disabled={isSaving}
                      >
                        {isSaving ? '保存中...' : '保存'}
                      </Button>
                    </>
                  )}
                </div>
              </div>
            </div>

            {/* プロフィール情報 */}
            {profile && (
              <div className="bg-white shadow rounded-lg">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h2 className="text-lg font-medium text-gray-900">基本情報</h2>
                </div>
                
                <div className="px-6 py-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* 社員番号 */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        社員番号
                      </label>
                      <Input
                        value={profile.employeeId}
                        disabled={true}
                        className="bg-gray-50"
                      />
                    </div>

                    {/* 姓 */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        姓 <span className="text-red-500">*</span>
                      </label>
                      <Input
                        value={isEditing ? editedProfile?.lastName || '' : profile.personalInfo.lastName}
                        onChange={(e) => handleInputChange('lastName', e.target.value)}
                        disabled={!isEditing}
                        className={!isEditing ? 'bg-gray-50' : ''}
                      />
                      {validationErrors.lastName && (
                        <p className="mt-1 text-sm text-red-600">{validationErrors.lastName}</p>
                      )}
                    </div>

                    {/* 名 */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        名 <span className="text-red-500">*</span>
                      </label>
                      <Input
                        value={isEditing ? editedProfile?.firstName || '' : profile.personalInfo.firstName}
                        onChange={(e) => handleInputChange('firstName', e.target.value)}
                        disabled={!isEditing}
                        className={!isEditing ? 'bg-gray-50' : ''}
                      />
                      {validationErrors.firstName && (
                        <p className="mt-1 text-sm text-red-600">{validationErrors.firstName}</p>
                      )}
                    </div>

                    {/* 表示名 */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        表示名 <span className="text-red-500">*</span>
                      </label>
                      <Input
                        value={isEditing ? editedProfile?.displayName || '' : profile.personalInfo.displayName}
                        onChange={(e) => handleInputChange('displayName', e.target.value)}
                        disabled={!isEditing}
                        className={!isEditing ? 'bg-gray-50' : ''}
                      />
                      {validationErrors.displayName && (
                        <p className="mt-1 text-sm text-red-600">{validationErrors.displayName}</p>
                      )}
                    </div>

                    {/* メールアドレス */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        メールアドレス
                      </label>
                      <Input
                        type="email"
                        value={profile.email}
                        disabled={true}
                        className="bg-gray-50"
                      />
                    </div>

                    {/* 部署 */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        部署
                      </label>
                      <Input
                        value={profile.organizationInfo.departmentName}
                        disabled={true}
                        className="bg-gray-50"
                      />
                    </div>

                    {/* 役職 */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        役職
                      </label>
                      <Input
                        value={profile.organizationInfo.positionName}
                        disabled={true}
                        className="bg-gray-50"
                      />
                    </div>

                    {/* 入社日 */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        入社日
                      </label>
                      <Input
                        value={profile.organizationInfo.hireDate}
                        disabled={true}
                        className="bg-gray-50"
                      />
                    </div>

                    {/* 電話番号 */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        電話番号
                      </label>
                      <Input
                        value={isEditing ? editedProfile?.phoneNumber || '' : profile.personalInfo.phoneNumber}
                        onChange={(e) => handleInputChange('phoneNumber', e.target.value)}
                        disabled={!isEditing}
                        className={!isEditing ? 'bg-gray-50' : ''}
                      />
                      {validationErrors.phoneNumber && (
                        <p className="mt-1 text-sm text-red-600">{validationErrors.phoneNumber}</p>
                      )}
                    </div>

                    {/* 緊急連絡先 */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        緊急連絡先
                      </label>
                      <Input
                        value={isEditing ? editedProfile?.emergencyContactPhone || '' : profile.personalInfo.emergencyContact.phoneNumber}
                        onChange={(e) => handleInputChange('emergencyContactPhone', e.target.value)}
                        disabled={!isEditing}
                        className={!isEditing ? 'bg-gray-50' : ''}
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
