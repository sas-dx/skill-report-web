/**
 * 要求仕様ID: PRO.1-BASE.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR-PROFILE_プロフィール画面.md
 * 実装内容: プロフィール画面（新しい組織情報API対応版）
 */
'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { Sidebar } from '@/components/dashboard/Sidebar';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Spinner } from '@/components/ui/Spinner';
import { getProfile, updateProfile, ProfileData, ProfileUpdateRequest } from '@/lib/api/profile';
import { useOrganization, Department, Position } from '@/hooks/useOrganization';

interface EditableProfile {
  firstName: string;
  lastName: string;
  firstNameKana: string;
  lastNameKana: string;
  displayName: string;
  email: string;
  phoneNumber: string;
  departmentId: string;
  positionId: string;
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

  // 組織情報取得フック
  const { data: organizationData, loading: orgLoading, error: orgError } = useOrganization();

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
        
        const profileResponse = await getProfile('me', {
          includeSkillSummary: true,
          includeGoalSummary: false,
          includeHistory: false
        });
        
        if (profileResponse.success && profileResponse.data) {
          setProfile(profileResponse.data.profile);
          setEditedProfile({
            firstName: profileResponse.data.profile.personalInfo.firstName,
            lastName: profileResponse.data.profile.personalInfo.lastName,
            firstNameKana: profileResponse.data.profile.personalInfo.firstNameKana,
            lastNameKana: profileResponse.data.profile.personalInfo.lastNameKana,
            displayName: profileResponse.data.profile.personalInfo.displayName,
            email: profileResponse.data.profile.email,
            phoneNumber: profileResponse.data.profile.personalInfo.phoneNumber,
            departmentId: profileResponse.data.profile.organizationInfo.departmentId,
            positionId: profileResponse.data.profile.organizationInfo.positionId,
          });
        } else {
          setError(profileResponse.error?.message || 'プロフィール情報の取得に失敗しました');
        }
      } catch (error) {
        console.error('プロフィール読み込みエラー:', error);
        setError('プロフィールの読み込み中にエラーが発生しました');
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
        email: profile.email,
        phoneNumber: profile.personalInfo.phoneNumber,
        departmentId: profile.organizationInfo.departmentId,
        positionId: profile.organizationInfo.positionId,
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
    
    // メールアドレスのバリデーション
    if (!editedProfile?.email?.trim()) {
      errors.email = 'メールアドレスは必須です';
    } else {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(editedProfile.email)) {
        errors.email = '有効なメールアドレスを入力してください';
      } else if (editedProfile.email.length > 255) {
        errors.email = 'メールアドレスは255文字以内で入力してください';
      }
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
        email: editedProfile.email,
        contact_info: {
          phone: editedProfile.phoneNumber
        },
        organization_info: {
          department_id: editedProfile.departmentId,
          position_id: editedProfile.positionId
        }
      };

      const response = await updateProfile('me', updateData);
      
      if (response.success) {
        // プロフィール状態を編集内容で更新（再読み込みではなく）
        if (profile && organizationData) {
          // 部署名と役職名を取得
          const selectedDepartment = organizationData.departments.find(d => d.id === editedProfile.departmentId);
          const selectedPosition = organizationData.positions.find(p => p.id === editedProfile.positionId);

          const updatedProfile = {
            ...profile,
            email: editedProfile.email,
            personalInfo: {
              ...profile.personalInfo,
              firstName: editedProfile.firstName,
              lastName: editedProfile.lastName,
              firstNameKana: editedProfile.firstNameKana,
              lastNameKana: editedProfile.lastNameKana,
              displayName: editedProfile.displayName,
              phoneNumber: editedProfile.phoneNumber
            },
            organizationInfo: {
              ...profile.organizationInfo,
              departmentId: editedProfile.departmentId,
              departmentName: selectedDepartment?.name || '',
              positionId: editedProfile.positionId,
              positionName: selectedPosition?.name || ''
            }
          };
          setProfile(updatedProfile);
        }
        setIsEditing(false);
        setError(null);
        setValidationErrors({});
      } else {
        // APIエラーの詳細処理
        if (response.error?.code === 'EMAIL_ALREADY_EXISTS') {
          // メールアドレス重複エラーの場合、フィールド固有のエラーとして表示
          setValidationErrors({
            email: 'このメールアドレスは既に他のユーザーによって使用されています'
          });
          setError(null);
        } else if (response.error?.invalid_fields) {
          // バリデーションエラーの場合、フィールド固有のエラーを設定
          const fieldErrors: Record<string, string> = {};
          response.error.invalid_fields.forEach((fieldError: any) => {
            fieldErrors[fieldError.field] = fieldError.reason;
          });
          setValidationErrors(fieldErrors);
          setError(null);
        } else {
          // その他のエラーの場合、一般的なエラーメッセージを表示
          setError(response.error?.message || 'プロフィール更新に失敗しました');
          setValidationErrors({});
        }
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

  // 部署選択肢を生成
  const getDepartmentOptions = () => {
    if (!organizationData?.departments) return [];
    return organizationData.departments.map(dept => ({
      value: dept.id,
      label: dept.name
    }));
  };

  // 役職選択肢を生成
  const getPositionOptions = () => {
    if (!organizationData?.positions) return [];
    return organizationData.positions.map(pos => ({
      value: pos.id,
      label: pos.name
    }));
  };

  if (isLoading || orgLoading) {
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

  if ((error && !profile) || orgError) {
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
              <h2 className="text-xl font-semibold text-gray-900 mb-2">データの読み込みに失敗しました</h2>
              <p className="text-gray-600 mb-4">{error || orgError}</p>
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
                        メールアドレス <span className="text-red-500">*</span>
                      </label>
                      <Input
                        type="email"
                        value={isEditing ? editedProfile?.email || '' : profile.email}
                        onChange={(e) => handleInputChange('email', e.target.value)}
                        disabled={!isEditing}
                        className={!isEditing ? 'bg-gray-50' : ''}
                        placeholder="example@company.com"
                      />
                      {validationErrors.email && (
                        <p className="mt-1 text-sm text-red-600">{validationErrors.email}</p>
                      )}
                    </div>

                    {/* 部署 */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        部署
                      </label>
                      {isEditing ? (
                        <Select
                          value={editedProfile?.departmentId || profile.organizationInfo.departmentId}
                          onChange={(value) => handleInputChange('departmentId', value)}
                          options={getDepartmentOptions()}
                          placeholder="部署を選択してください"
                        />
                      ) : (
                        <Input
                          value={profile.organizationInfo.departmentName}
                          disabled={true}
                          className="bg-gray-50"
                        />
                      )}
                    </div>

                    {/* 役職 */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        役職
                      </label>
                      {isEditing ? (
                        <Select
                          value={editedProfile?.positionId || profile.organizationInfo.positionId}
                          onChange={(value) => handleInputChange('positionId', value)}
                          options={getPositionOptions()}
                          placeholder="役職を選択してください"
                        />
                      ) : (
                        <Input
                          value={profile.organizationInfo.positionName}
                          disabled={true}
                          className="bg-gray-50"
                        />
                      )}
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
