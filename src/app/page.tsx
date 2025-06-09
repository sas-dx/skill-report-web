// 要求仕様ID: PLT.1-WEB.1, ACC.1-AUTH.1 - ログイン画面（ルート）
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { AcademicCapIcon, EyeIcon, EyeSlashIcon } from '@/components/ui/Icons';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Spinner } from '@/components/ui/Spinner';

export default function LoginPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    loginId: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // エラーをクリア
    if (error) setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        // トークンを保存
        if (data.data?.token) {
          localStorage.setItem('token', data.data.token);
          localStorage.setItem('user', JSON.stringify(data.data.user));
        }
        // ログイン成功時はダッシュボードにリダイレクト
        router.push('/dashboard');
      } else {
        setError(data.error?.message || 'ログインに失敗しました');
      }
    } catch (error) {
      console.error('Login error:', error);
      setError('ネットワークエラーが発生しました');
    } finally {
      setIsLoading(false);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* ヘッダー */}
        <div className="text-center">
          <div className="flex justify-center">
            <div className="flex items-center justify-center w-16 h-16 bg-blue-600 rounded-full">
              <AcademicCapIcon className="text-white" size={40} />
            </div>
          </div>
          <h1 className="mt-6 text-3xl font-bold text-gray-900">
            年間スキル報告書システム
          </h1>
          <p className="mt-2 text-sm text-gray-600">
            アカウントにログインしてください
          </p>
        </div>

        {/* ログインフォーム */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <form className="space-y-6" onSubmit={handleSubmit}>
            {/* エラーメッセージ */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-md p-4">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <p className="text-sm text-red-800">{error}</p>
                  </div>
                </div>
              </div>
            )}

            {/* ログインID */}
            <div>
              <label htmlFor="loginId" className="block text-sm font-medium text-gray-700 mb-2">
                ログインID
              </label>
              <Input
                id="loginId"
                name="loginId"
                type="text"
                required
                value={formData.loginId}
                onChange={handleInputChange}
                placeholder="ログインIDを入力してください"
                disabled={isLoading}
                className="w-full"
              />
            </div>

            {/* パスワード */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                パスワード
              </label>
              <div className="relative">
                <Input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={formData.password}
                  onChange={handleInputChange}
                  placeholder="パスワードを入力してください"
                  disabled={isLoading}
                  className="w-full pr-10"
                />
                <button
                  type="button"
                  onClick={togglePasswordVisibility}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  disabled={isLoading}
                >
                  {showPassword ? (
                    <EyeSlashIcon className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                  ) : (
                    <EyeIcon className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                  )}
                </button>
              </div>
            </div>

            {/* ログインボタン */}
            <div>
              <Button
                type="submit"
                variant="primary"
                size="lg"
                disabled={isLoading || !formData.loginId || !formData.password}
                className="w-full"
              >
                {isLoading ? (
                  <div className="flex items-center justify-center">
                    <Spinner size="sm" className="mr-2" />
                    ログイン中...
                  </div>
                ) : (
                  'ログイン'
                )}
              </Button>
            </div>

            {/* パスワードリセットリンク */}
            <div className="text-center">
              <button
                type="button"
                className="text-sm text-blue-600 hover:text-blue-500 hover:underline"
                disabled={isLoading}
              >
                パスワードを忘れた方はこちら
              </button>
            </div>
          </form>

          {/* デモ用ログイン情報 */}
          <div className="mt-6 p-4 bg-gray-50 rounded-md">
            <h3 className="text-sm font-medium text-gray-700 mb-2">デモ用ログイン情報</h3>
            <div className="text-xs text-gray-600 space-y-1">
              <div>テストユーザー: 000001 / password</div>
            </div>
          </div>
        </div>

        {/* フッター */}
        <div className="text-center">
          <p className="text-xs text-gray-500">
            © 2025 年間スキル報告書システム. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  );
}
