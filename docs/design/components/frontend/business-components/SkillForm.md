# SkillForm コンポーネント定義書

## 1. 基本情報

- **部品名**: SkillForm
- **カテゴリ**: ビジネス部品
- **責務**: スキル情報の入力・編集フォーム
- **依存関係**: Form, Input, Select, DatePicker, CheckboxGroup, Button
- **作成日**: 2025/05/30
- **最終更新**: 2025/05/30

---

## 2. インターフェース仕様

### 2.1 Props定義

| 名前 | 型 | 必須 | デフォルト | 説明 |
|------|----|----|----------|------|
| initialData | `SkillItem \| null` | No | `null` | 初期データ（編集時） |
| mode | `'create'` \| `'edit'` | No | `'create'` | フォームモード |
| onSubmit | `(data: SkillFormData) => Promise<void>` | Yes | - | 送信時コールバック |
| onCancel | `() => void` | No | - | キャンセル時コールバック |
| loading | `boolean` | No | `false` | 送信中状態 |
| disabled | `boolean` | No | `false` | フォーム無効状態 |
| showDraftSave | `boolean` | No | `true` | 下書き保存ボタン表示 |
| onDraftSave | `(data: Partial<SkillFormData>) => Promise<void>` | No | - | 下書き保存コールバック |
| validationErrors | `Record<string, string>` | No | `{}` | サーバーサイドバリデーションエラー |
| className | `string` | No | - | 追加CSSクラス |

### 2.2 型定義

```typescript
export interface SkillFormData {
  skillName: string;
  category: SkillCategory;
  level: SkillLevel;
  experience: number;
  lastUsed: Date;
  target: boolean;
  comments?: string;
  certifications?: string[];
  projects?: string[];
}

export interface SkillItem extends SkillFormData {
  id: string;
  userId: string;
  createdAt: Date;
  updatedAt: Date;
}

export type SkillCategory = 
  | 'プログラミング言語'
  | 'フレームワーク・ライブラリ'
  | 'データベース'
  | 'クラウド・インフラ'
  | 'ツール・その他';

export type SkillLevel = '初級' | '中級' | '上級' | 'エキスパート';

export interface SkillFormProps {
  initialData?: SkillItem | null;
  mode?: 'create' | 'edit';
  onSubmit: (data: SkillFormData) => Promise<void>;
  onCancel?: () => void;
  loading?: boolean;
  disabled?: boolean;
  showDraftSave?: boolean;
  onDraftSave?: (data: Partial<SkillFormData>) => Promise<void>;
  validationErrors?: Record<string, string>;
  className?: string;
}
```

### 2.3 戻り値
- `JSX.Element`

---

## 3. 実装仕様

### 3.1 技術スタック
- **React**: 18.x
- **TypeScript**: 5.x
- **React Hook Form**: 7.x
- **Zod**: 3.x（バリデーション）
- **Tailwind CSS**: 3.x
- **date-fns**: 2.x（日付処理）

### 3.2 バリデーションスキーマ

```typescript
import { z } from 'zod';

export const skillFormSchema = z.object({
  skillName: z
    .string()
    .min(1, 'スキル名は必須です')
    .max(100, 'スキル名は100文字以内で入力してください'),
  
  category: z.enum([
    'プログラミング言語',
    'フレームワーク・ライブラリ',
    'データベース',
    'クラウド・インフラ',
    'ツール・その他'
  ], {
    errorMap: () => ({ message: 'カテゴリを選択してください' })
  }),
  
  level: z.enum(['初級', '中級', '上級', 'エキスパート'], {
    errorMap: () => ({ message: 'レベルを選択してください' })
  }),
  
  experience: z
    .number()
    .min(0, '経験年数は0以上で入力してください')
    .max(50, '経験年数は50年以内で入力してください'),
  
  lastUsed: z
    .date()
    .max(new Date(), '最終使用日は今日以前の日付を選択してください'),
  
  target: z.boolean(),
  
  comments: z
    .string()
    .max(500, 'コメントは500文字以内で入力してください')
    .optional(),
  
  certifications: z
    .array(z.string())
    .optional(),
  
  projects: z
    .array(z.string())
    .optional()
});

export type SkillFormData = z.infer<typeof skillFormSchema>;
```

### 3.3 内部構造

```typescript
import React, { useEffect, useMemo } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { format } from 'date-fns';
import { ja } from 'date-fns/locale';

import { Form } from '@/components/ui/Form';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { DatePicker } from '@/components/ui/DatePicker';
import { CheckboxGroup } from '@/components/ui/CheckboxGroup';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { skillFormSchema, SkillFormData, SkillFormProps } from './SkillForm.types';
import { SKILL_CATEGORIES, SKILL_LEVELS, COMMON_CERTIFICATIONS } from '@/constants/skillConstants';

export const SkillForm: React.FC<SkillFormProps> = ({
  initialData = null,
  mode = 'create',
  onSubmit,
  onCancel,
  loading = false,
  disabled = false,
  showDraftSave = true,
  onDraftSave,
  validationErrors = {},
  className
}) => {
  const {
    control,
    handleSubmit,
    watch,
    setValue,
    getValues,
    formState: { errors, isDirty, isValid },
    reset
  } = useForm<SkillFormData>({
    resolver: zodResolver(skillFormSchema),
    defaultValues: {
      skillName: initialData?.skillName || '',
      category: initialData?.category || 'プログラミング言語',
      level: initialData?.level || '初級',
      experience: initialData?.experience || 0,
      lastUsed: initialData?.lastUsed || new Date(),
      target: initialData?.target || false,
      comments: initialData?.comments || '',
      certifications: initialData?.certifications || [],
      projects: initialData?.projects || []
    },
    mode: 'onChange'
  });

  // フォームデータの監視
  const watchedData = watch();

  // 自動保存（下書き保存）
  useEffect(() => {
    if (!isDirty || !onDraftSave) return;

    const timer = setTimeout(() => {
      onDraftSave(getValues());
    }, 2000); // 2秒後に自動保存

    return () => clearTimeout(timer);
  }, [watchedData, isDirty, onDraftSave, getValues]);

  // 初期データ変更時のリセット
  useEffect(() => {
    if (initialData) {
      reset({
        skillName: initialData.skillName,
        category: initialData.category,
        level: initialData.level,
        experience: initialData.experience,
        lastUsed: initialData.lastUsed,
        target: initialData.target,
        comments: initialData.comments || '',
        certifications: initialData.certifications || [],
        projects: initialData.projects || []
      });
    }
  }, [initialData, reset]);

  // カテゴリ選択肢
  const categoryOptions = useMemo(() => 
    SKILL_CATEGORIES.map(category => ({
      value: category,
      label: category
    })), []
  );

  // レベル選択肢
  const levelOptions = useMemo(() => 
    SKILL_LEVELS.map(level => ({
      value: level,
      label: level
    })), []
  );

  // 資格選択肢
  const certificationOptions = useMemo(() => 
    COMMON_CERTIFICATIONS.map(cert => ({
      id: cert.id,
      label: cert.name,
      value: cert.id
    })), []
  );

  // フォーム送信
  const handleFormSubmit = async (data: SkillFormData) => {
    try {
      await onSubmit(data);
    } catch (error) {
      console.error('Form submission error:', error);
    }
  };

  // 下書き保存
  const handleDraftSave = async () => {
    if (!onDraftSave) return;
    
    try {
      await onDraftSave(getValues());
    } catch (error) {
      console.error('Draft save error:', error);
    }
  };

  return (
    <Form className={className}>
      <div className="space-y-6">
        {/* 基本情報セクション */}
        <section className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900">基本情報</h3>
          
          {/* スキル名 */}
          <Controller
            name="skillName"
            control={control}
            render={({ field }) => (
              <div>
                <label className="form-label required">スキル名</label>
                <Input
                  {...field}
                  placeholder="例: JavaScript, React, AWS"
                  error={!!errors.skillName || !!validationErrors.skillName}
                  disabled={disabled || loading}
                />
                {errors.skillName && (
                  <p className="text-sm text-error-600 mt-1">{errors.skillName.message}</p>
                )}
                {validationErrors.skillName && (
                  <p className="text-sm text-error-600 mt-1">{validationErrors.skillName}</p>
                )}
              </div>
            )}
          />

          {/* カテゴリ */}
          <Controller
            name="category"
            control={control}
            render={({ field }) => (
              <div>
                <label className="form-label required">カテゴリ</label>
                <Select
                  {...field}
                  options={categoryOptions}
                  placeholder="カテゴリを選択"
                  error={!!errors.category || !!validationErrors.category}
                  disabled={disabled || loading}
                />
                {errors.category && (
                  <p className="text-sm text-error-600 mt-1">{errors.category.message}</p>
                )}
              </div>
            )}
          />

          {/* レベル */}
          <Controller
            name="level"
            control={control}
            render={({ field }) => (
              <div>
                <label className="form-label required">レベル</label>
                <Select
                  {...field}
                  options={levelOptions}
                  placeholder="レベルを選択"
                  error={!!errors.level || !!validationErrors.level}
                  disabled={disabled || loading}
                />
                {errors.level && (
                  <p className="text-sm text-error-600 mt-1">{errors.level.message}</p>
                )}
                <div className="mt-2 text-sm text-gray-500">
                  <p><strong>初級:</strong> 基本的な操作・概念を理解</p>
                  <p><strong>中級:</strong> 実務で活用可能</p>
                  <p><strong>上級:</strong> 高度な機能・最適化が可能</p>
                  <p><strong>エキスパート:</strong> 他者への指導・アーキテクチャ設計が可能</p>
                </div>
              </div>
            )}
          />
        </section>

        {/* 経験情報セクション */}
        <section className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900">経験情報</h3>
          
          {/* 経験年数 */}
          <Controller
            name="experience"
            control={control}
            render={({ field: { value, onChange, ...field } }) => (
              <div>
                <label className="form-label required">経験年数</label>
                <div className="flex items-center gap-2">
                  <Input
                    {...field}
                    type="number"
                    min="0"
                    max="50"
                    step="0.5"
                    value={value}
                    onChange={(e) => onChange(parseFloat(e.target.value) || 0)}
                    placeholder="0"
                    error={!!errors.experience || !!validationErrors.experience}
                    disabled={disabled || loading}
                    className="w-24"
                  />
                  <span className="text-sm text-gray-500">年</span>
                </div>
                {errors.experience && (
                  <p className="text-sm text-error-600 mt-1">{errors.experience.message}</p>
                )}
              </div>
            )}
          />

          {/* 最終使用日 */}
          <Controller
            name="lastUsed"
            control={control}
            render={({ field }) => (
              <div>
                <label className="form-label required">最終使用日</label>
                <DatePicker
                  {...field}
                  placeholder="日付を選択"
                  error={!!errors.lastUsed || !!validationErrors.lastUsed}
                  disabled={disabled || loading}
                  maxDate={new Date()}
                />
                {errors.lastUsed && (
                  <p className="text-sm text-error-600 mt-1">{errors.lastUsed.message}</p>
                )}
              </div>
            )}
          />

          {/* 目標スキル */}
          <Controller
            name="target"
            control={control}
            render={({ field: { value, onChange, ...field } }) => (
              <div>
                <label className="flex items-center gap-2">
                  <input
                    {...field}
                    type="checkbox"
                    checked={value}
                    onChange={(e) => onChange(e.target.checked)}
                    disabled={disabled || loading}
                    className="form-checkbox"
                  />
                  <span className="text-sm font-medium text-gray-700">
                    目標スキル（今後伸ばしたいスキル）
                  </span>
                </label>
              </div>
            )}
          />
        </section>

        {/* 詳細情報セクション */}
        <section className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900">詳細情報</h3>
          
          {/* 関連資格 */}
          <Controller
            name="certifications"
            control={control}
            render={({ field: { value, onChange } }) => (
              <div>
                <label className="form-label">関連資格</label>
                <CheckboxGroup
                  options={certificationOptions}
                  value={value || []}
                  onChange={onChange}
                  skillStyle
                />
              </div>
            )}
          />

          {/* コメント */}
          <Controller
            name="comments"
            control={control}
            render={({ field }) => (
              <div>
                <label className="form-label">コメント・備考</label>
                <textarea
                  {...field}
                  rows={4}
                  placeholder="具体的な経験内容、プロジェクトでの活用例、学習状況など"
                  className="form-input resize-none"
                  disabled={disabled || loading}
                />
                {errors.comments && (
                  <p className="text-sm text-error-600 mt-1">{errors.comments.message}</p>
                )}
                <p className="text-sm text-gray-500 mt-1">
                  {(field.value?.length || 0)}/500文字
                </p>
              </div>
            )}
          />
        </section>

        {/* アクションボタン */}
        <div className="flex flex-col sm:flex-row gap-3 pt-6 border-t border-gray-200">
          <div className="flex gap-2 sm:ml-auto">
            {onCancel && (
              <Button
                type="button"
                variant="secondary"
                onClick={onCancel}
                disabled={loading}
              >
                キャンセル
              </Button>
            )}
            
            {showDraftSave && onDraftSave && (
              <Button
                type="button"
                variant="ghost"
                onClick={handleDraftSave}
                disabled={!isDirty || loading}
                size="sm"
              >
                下書き保存
              </Button>
            )}
            
            <Button
              type="submit"
              onClick={handleSubmit(handleFormSubmit)}
              loading={loading}
              disabled={!isValid || loading}
            >
              {mode === 'create' ? 'スキル登録' : 'スキル更新'}
            </Button>
          </div>
        </div>

        {/* フォーム状態表示（開発時のみ） */}
        {process.env.NODE_ENV === 'development' && (
          <div className="mt-4 p-4 bg-gray-100 rounded-md text-xs">
            <p>isDirty: {isDirty.toString()}</p>
            <p>isValid: {isValid.toString()}</p>
            <p>errors: {Object.keys(errors).length}</p>
          </div>
        )}
      </div>
    </Form>
  );
};

SkillForm.displayName = 'SkillForm';
```

### 3.4 状態管理
- **フォーム状態**: React Hook Form
- **バリデーション**: Zod + React Hook Form
- **自動保存**: useEffect + setTimeout
- **外部状態**: Props経由で制御

---

## 4. 使用例・サンプルコード

### 4.1 新規作成モード

```tsx
import { SkillForm } from '@/components/business/SkillForm';
import { useSkillData } from '@/hooks/useSkillData';
import { useRouter } from 'next/router';

export const CreateSkillPage = () => {
  const { createSkill } = useSkillData();
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (data: SkillFormData) => {
    setLoading(true);
    try {
      await createSkill(data);
      router.push('/skills');
    } catch (error) {
      console.error('Failed to create skill:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    router.back();
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">新しいスキルを登録</h1>
      <SkillForm
        mode="create"
        onSubmit={handleSubmit}
        onCancel={handleCancel}
        loading={loading}
      />
    </div>
  );
};
```

### 4.2 編集モード

```tsx
import { SkillForm } from '@/components/business/SkillForm';
import { useSkillData } from '@/hooks/useSkillData';

export const EditSkillPage = ({ skillId }: { skillId: string }) => {
  const { getSkill, updateSkill } = useSkillData();
  const [skill, setSkill] = useState<SkillItem | null>(null);
  const [loading, setLoading] = useState(false);
  const [validationErrors, setValidationErrors] = useState({});

  useEffect(() => {
    const loadSkill = async () => {
      try {
        const skillData = await getSkill(skillId);
        setSkill(skillData);
      } catch (error) {
        console.error('Failed to load skill:', error);
      }
    };
    loadSkill();
  }, [skillId, getSkill]);

  const handleSubmit = async (data: SkillFormData) => {
    setLoading(true);
    setValidationErrors({});
    
    try {
      await updateSkill(skillId, data);
      // 成功処理
    } catch (error) {
      if (error.response?.data?.errors) {
        setValidationErrors(error.response.data.errors);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDraftSave = async (data: Partial<SkillFormData>) => {
    try {
      await updateSkill(skillId, { ...data, isDraft: true });
    } catch (error) {
      console.error('Failed to save draft:', error);
    }
  };

  if (!skill) {
    return <div>Loading...</div>;
  }

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">スキル編集</h1>
      <SkillForm
        mode="edit"
        initialData={skill}
        onSubmit={handleSubmit}
        onDraftSave={handleDraftSave}
        loading={loading}
        validationErrors={validationErrors}
      />
    </div>
  );
};
```

### 4.3 モーダル内での使用

```tsx
import { Modal } from '@/components/ui/Modal';
import { SkillForm } from '@/components/business/SkillForm';

export const SkillFormModal = ({ 
  isOpen, 
  onClose, 
  skill 
}: {
  isOpen: boolean;
  onClose: () => void;
  skill?: SkillItem;
}) => {
  const handleSubmit = async (data: SkillFormData) => {
    // スキル保存処理
    onClose();
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="lg">
      <Modal.Header>
        <h2 className="text-xl font-semibold">
          {skill ? 'スキル編集' : '新しいスキル'}
        </h2>
      </Modal.Header>
      <Modal.Body>
        <SkillForm
          mode={skill ? 'edit' : 'create'}
          initialData={skill}
          onSubmit={handleSubmit}
          onCancel={onClose}
          showDraftSave={false}
        />
      </Modal.Body>
    </Modal>
  );
};
```

---

## 5. テスト仕様

### 5.1 単体テスト

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SkillForm } from './SkillForm';
import { TestDataFactory } from '@/test/utils/TestDataFactory';

describe('SkillForm', () => {
  const mockOnSubmit = jest.fn();
  const mockOnCancel = jest.fn();
  const mockOnDraftSave = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('新規作成モードでの基本レンダリング', () => {
    render(
      <SkillForm
        mode="create"
        onSubmit={mockOnSubmit}
      />
    );

    expect(screen.getByLabelText('スキル名')).toBeInTheDocument();
    expect(screen.getByLabelText('カテゴリ')).toBeInTheDocument();
    expect(screen.getByLabelText('レベル')).toBeInTheDocument();
    expect(screen.getByText('スキル登録')).toBeInTheDocument();
  });

  test('編集モードでの初期データ表示', () => {
    const skillData = TestDataFactory.createSkillItem({
      skillName: 'React',
      category: 'フレームワーク・ライブラリ',
      level: '上級'
    });

    render(
      <SkillForm
        mode="edit"
        initialData={skillData}
        onSubmit={mockOnSubmit}
      />
    );

    expect(screen.getByDisplayValue('React')).toBeInTheDocument();
    expect(screen.getByText('スキル更新')).toBeInTheDocument();
  });

  test('フォームバリデーション', async () => {
    const user = userEvent.setup();
    
    render(
      <SkillForm
        mode="create"
        onSubmit={mockOnSubmit}
      />
    );

    // 空のフォームで送信
    await user.click(screen.getByText('スキル登録'));

    await waitFor(() => {
      expect(screen.getByText('スキル名は必須です')).toBeInTheDocument();
    });

    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  test('正常なフォーム送信', async () => {
    const user = userEvent.setup();
    
    render(
      <SkillForm
        mode="create"
        onSubmit={mockOnSubmit}
      />
    );

    // フォーム入力
    await user.type(screen.getByLabelText('スキル名'), 'JavaScript');
    await user.selectOptions(screen.getByLabelText('カテゴリ'), 'プログラミング言語');
    await user.selectOptions(screen.getByLabelText('レベル'), '中級');
    await user.type(screen.getByLabelText('経験年数'), '3');

    // 送信
    await user.click(screen.getByText('スキル登録'));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          skillName: 'JavaScript',
          category: 'プログラミング言語',
          level: '中級',
          experience: 3
        })
      );
    });
  });

  test('下書き保存機能', async () => {
    const user = userEvent.setup();
    
    render(
      <SkillForm
        mode="create"
        onSubmit={mockOnSubmit}
        onDraftSave={mockOnDraftSave}
      />
    );

    // フォーム入力
    await user.type(screen.getByLabelText('スキル名'), 'Vue.js');

    // 下書き保存ボタンクリック
    await user.click(screen.getByText('下書き保存'));

    await waitFor(() => {
      expect(mockOnDraftSave).toHaveBeenCalledWith(
        expect.objectContaining({
          skillName: 'Vue.js'
        })
      );
    });
  });

  test('自動保存機能', async () => {
    const user = userEvent.setup();
    jest.useFakeTimers();
    
    render(
      <SkillForm
        mode="create"
        onSubmit={mockOnSubmit}
        onDraftSave={mockOnDraftSave}
      />
    );

    // フォーム入力
    await user.type(screen.getByLabelText('スキル名'), 'Angular');

    // 2秒経過
    jest.advanceTimersByTime(2000);

    await waitFor(() => {
      expect(mockOnDraftSave).toHaveBeenCalled();
    });

    jest.useRealTimers();
  });

  test('バリデーションエラー表示', () => {
    const validationErrors = {
      skillName: 'このスキル名は既に登録されています'
    };

    render(
      <SkillForm
        mode="create"
        onSubmit={mockOnSubmit}
        validationErrors={validationErrors}
      />
    );

    expect(screen.getByText('このスキル名は既に登録されています')).toBeInTheDocument();
  });

  test('ローディング状態', () => {
    render(
      <SkillForm
        mode="create"
        onSubmit={mockOnSubmit}
        loading={true}
      />
    );

    expect(screen.getByText('スキル登録')).toBeDisabled();
    expect(screen.getByLabelText('スキル名')).toBeDisabled();
  });
});
```

### 5.2 統合テスト

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SkillForm } from './SkillForm';
import { ApiTestHelper } from '@/test/utils/ApiTestHelper';

describe('SkillForm 統合テスト', () => {
  test('スキル作成フロー', async () => {
    const user = userEvent.setup();
    const mockCreateSkill = jest.fn().mockResolvedValue({ id: '1' });

    render(
      <SkillForm
        mode="create"
        onSubmit={mockCreateSkill}
      />
    );

    // 完全なフォーム入力
    await user.type(screen.getByLabelText('スキル名'), 'TypeScript');
    await user.selectOptions(screen.getByLabelText('カテゴリ'), 'プログラミング言語');
    await user.selectOptions(screen.getByLabelText('レベル'), '上級');
    await user.type(screen.getByLabelText('経験年数'), '5');
    await user.type(screen.getByL
