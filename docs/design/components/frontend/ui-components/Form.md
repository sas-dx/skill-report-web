# Form コンポーネント定義書

## 1. 基本情報

- **部品名**: Form
- **カテゴリ**: フロントエンド - UIコンポーネント
- **責務**: フォーム入力・バリデーション・送信の統合管理
- **依存関係**: Button, Spinner, Material Design Components
- **作成日**: 2025/05/30
- **最終更新**: 2025/05/30

---

## 2. 概要

### 2.1 目的

Formコンポーネントは、Material Design準拠のフォーム要素を統合し、バリデーション、エラーハンドリング、送信処理を一元管理する包括的なフォームソリューションです。

### 2.2 特徴

- Material Design Components準拠
- リアルタイムバリデーション
- 多様な入力フィールドサポート
- アクセシビリティ完全対応
- TypeScript型安全性
- カスタマイズ可能なレイアウト

---

## 3. インターフェース定義

### 3.1 基本Props

```typescript
interface FormProps<T = Record<string, any>> {
  /** フォームの初期値 */
  initialValues?: Partial<T>;
  
  /** バリデーションスキーマ */
  validationSchema?: ValidationSchema<T>;
  
  /** 送信時のコールバック */
  onSubmit: (values: T) => Promise<void> | void;
  
  /** 値変更時のコールバック */
  onChange?: (values: Partial<T>) => void;
  
  /** バリデーションエラー時のコールバック */
  onValidationError?: (errors: FormErrors<T>) => void;
  
  /** フォームレイアウト */
  layout?: 'vertical' | 'horizontal' | 'inline';
  
  /** 送信ボタンのテキスト */
  submitText?: string;
  
  /** リセットボタンを表示するか */
  showResetButton?: boolean;
  
  /** リセットボタンのテキスト */
  resetText?: string;
  
  /** ローディング状態 */
  loading?: boolean;
  
  /** 無効状態 */
  disabled?: boolean;
  
  /** 自動フォーカス */
  autoFocus?: boolean;
  
  /** カスタムクラス名 */
  className?: string;
  
  /** カスタムスタイル */
  style?: React.CSSProperties;
  
  /** テストID */
  testId?: string;
  
  /** 子要素 */
  children: React.ReactNode;
}
```

### 3.2 フィールド関連型

```typescript
/**
 * フォームフィールドの基本Props
 */
interface BaseFieldProps {
  /** フィールド名 */
  name: string;
  
  /** ラベル */
  label?: string;
  
  /** プレースホルダー */
  placeholder?: string;
  
  /** ヘルプテキスト */
  helperText?: string;
  
  /** 必須フィールドか */
  required?: boolean;
  
  /** 無効状態 */
  disabled?: boolean;
  
  /** 読み取り専用 */
  readOnly?: boolean;
  
  /** 自動フォーカス */
  autoFocus?: boolean;
  
  /** カスタムクラス名 */
  className?: string;
  
  /** テストID */
  testId?: string;
}

/**
 * テキストフィールドProps
 */
interface TextFieldProps extends BaseFieldProps {
  /** 入力タイプ */
  type?: 'text' | 'email' | 'password' | 'tel' | 'url' | 'search';
  
  /** 最大文字数 */
  maxLength?: number;
  
  /** 最小文字数 */
  minLength?: number;
  
  /** パターン（正規表現） */
  pattern?: string;
  
  /** 複数行入力 */
  multiline?: boolean;
  
  /** 行数（multiline時） */
  rows?: number;
  
  /** 最大行数（multiline時） */
  maxRows?: number;
}

/**
 * セレクトフィールドProps
 */
interface SelectFieldProps extends BaseFieldProps {
  /** 選択肢 */
  options: SelectOption[];
  
  /** 複数選択可能か */
  multiple?: boolean;
  
  /** 検索可能か */
  searchable?: boolean;
  
  /** クリア可能か */
  clearable?: boolean;
  
  /** プレースホルダー（選択なし時） */
  emptyText?: string;
}

/**
 * チェックボックスProps
 */
interface CheckboxFieldProps extends BaseFieldProps {
  /** チェックボックスのラベル */
  checkboxLabel?: string;
  
  /** 中間状態 */
  indeterminate?: boolean;
}

/**
 * ラジオボタンProps
 */
interface RadioFieldProps extends BaseFieldProps {
  /** 選択肢 */
  options: RadioOption[];
  
  /** レイアウト方向 */
  direction?: 'row' | 'column';
}
```

---

## 4. 実装仕様

### 4.1 メインコンポーネント

```typescript
import React, { useState, useCallback, useRef } from 'react';
import { MDCTextField } from '@material/textfield';
import { MDCSelect } from '@material/select';
import { MDCCheckbox } from '@material/checkbox';
import { MDCRadio } from '@material/radio';
import { Button } from './Button';
import { Spinner } from './Spinner';
import './Form.scss';

export const Form = <T extends Record<string, any>>({
  initialValues = {} as Partial<T>,
  validationSchema,
  onSubmit,
  onChange,
  onValidationError,
  layout = 'vertical',
  submitText = '送信',
  showResetButton = false,
  resetText = 'リセット',
  loading = false,
  disabled = false,
  autoFocus = false,
  className,
  style,
  testId,
  children,
  ...props
}: FormProps<T>) => {
  const formRef = useRef<HTMLFormElement>(null);
  const [values, setValues] = useState<Partial<T>>(initialValues);
  const [errors, setErrors] = useState<FormErrors<T>>({});
  const [touched, setTouched] = useState<Record<keyof T, boolean>>({} as Record<keyof T, boolean>);
  const [submitting, setSubmitting] = useState(false);

  // バリデーション実行
  const validateField = useCallback((name: keyof T, value: any): string | undefined => {
    if (!validationSchema) return undefined;
    
    const fieldSchema = validationSchema[name];
    if (!fieldSchema) return undefined;
    
    return fieldSchema.validate(value);
  }, [validationSchema]);

  // 全フィールドバリデーション
  const validateForm = useCallback((): FormErrors<T> => {
    const newErrors: FormErrors<T> = {};
    
    if (validationSchema) {
      Object.keys(validationSchema).forEach((key) => {
        const error = validateField(key as keyof T, values[key as keyof T]);
        if (error) {
          newErrors[key as keyof T] = error;
        }
      });
    }
    
    return newErrors;
  }, [values, validateField, validationSchema]);

  // 値の更新
  const updateValue = useCallback((name: keyof T, value: any) => {
    const newValues = { ...values, [name]: value };
    setValues(newValues);
    
    // リアルタイムバリデーション
    if (touched[name]) {
      const error = validateField(name, value);
      setErrors(prev => ({
        ...prev,
        [name]: error
      }));
    }
    
    onChange?.(newValues);
  }, [values, touched, validateField, onChange]);

  // フィールドのフォーカス離脱
  const handleBlur = useCallback((name: keyof T) => {
    setTouched(prev => ({ ...prev, [name]: true }));
    
    const error = validateField(name, values[name]);
    setErrors(prev => ({
      ...prev,
      [name]: error
    }));
  }, [values, validateField]);

  // フォーム送信
  const handleSubmit = useCallback(async (event: React.FormEvent) => {
    event.preventDefault();
    
    const formErrors = validateForm();
    setErrors(formErrors);
    
    if (Object.keys(formErrors).length > 0) {
      onValidationError?.(formErrors);
      return;
    }
    
    setSubmitting(true);
    try {
      await onSubmit(values as T);
    } catch (error) {
      console.error('フォーム送信エラー:', error);
    } finally {
      setSubmitting(false);
    }
  }, [values, validateForm, onSubmit, onValidationError]);

  // フォームリセット
  const handleReset = useCallback(() => {
    setValues(initialValues);
    setErrors({});
    setTouched({} as Record<keyof T, boolean>);
  }, [initialValues]);

  const formClasses = [
    'form',
    `form--${layout}`,
    disabled && 'form--disabled',
    className
  ].filter(Boolean).join(' ');

  const formContext = {
    values,
    errors,
    touched,
    updateValue,
    handleBlur,
    disabled: disabled || submitting
  };

  return (
    <FormProvider value={formContext}>
      <form
        ref={formRef}
        className={formClasses}
        style={style}
        onSubmit={handleSubmit}
        onReset={handleReset}
        noValidate
        data-testid={testId}
        {...props}
      >
        <div className="form__fields">
          {children}
        </div>
        
        <div className="form__actions">
          {showResetButton && (
            <Button
              type="reset"
              variant="outlined"
              disabled={disabled || submitting}
              className="form__reset-button"
            >
              {resetText}
            </Button>
          )}
          
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={disabled || submitting}
            loading={submitting}
            className="form__submit-button"
          >
            {submitting ? <Spinner size="small" color="white" /> : submitText}
          </Button>
        </div>
        
        {loading && (
          <div className="form__loading-overlay">
            <Spinner overlay label="処理中..." />
          </div>
        )}
      </form>
    </FormProvider>
  );
};
```

### 4.2 フィールドコンポーネント

```typescript
// テキストフィールド
export const TextField: React.FC<TextFieldProps> = ({
  name,
  label,
  placeholder,
  helperText,
  required = false,
  disabled = false,
  readOnly = false,
  autoFocus = false,
  type = 'text',
  maxLength,
  minLength,
  pattern,
  multiline = false,
  rows = 3,
  maxRows,
  className,
  testId,
  ...props
}) => {
  const { values, errors, touched, updateValue, handleBlur, disabled: formDisabled } = useFormContext();
  const fieldRef = useRef<HTMLDivElement>(null);
  const [mdcTextField, setMdcTextField] = useState<MDCTextField | null>(null);

  const value = values[name] || '';
  const error = touched[name] ? errors[name] : undefined;
  const isDisabled = disabled || formDisabled;

  useEffect(() => {
    if (fieldRef.current) {
      const textField = new MDCTextField(fieldRef.current);
      setMdcTextField(textField);
      
      return () => {
        textField.destroy();
      };
    }
  }, []);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    updateValue(name, event.target.value);
  };

  const handleFieldBlur = () => {
    handleBlur(name);
  };

  const fieldClasses = [
    'mdc-text-field',
    multiline && 'mdc-text-field--textarea',
    error && 'mdc-text-field--invalid',
    isDisabled && 'mdc-text-field--disabled',
    className
  ].filter(Boolean).join(' ');

  const inputProps = {
    className: multiline ? 'mdc-text-field__input' : 'mdc-text-field__input',
    value,
    onChange: handleChange,
    onBlur: handleFieldBlur,
    disabled: isDisabled,
    readOnly,
    autoFocus,
    maxLength,
    minLength,
    pattern,
    required,
    placeholder,
    'data-testid': testId,
    ...props
  };

  return (
    <div className="form__field">
      <div ref={fieldRef} className={fieldClasses}>
        {multiline ? (
          <>
            <span className="mdc-text-field__resizer">
              <textarea
                {...inputProps}
                rows={rows}
                style={{ maxHeight: maxRows ? `${maxRows * 1.5}em` : undefined }}
              />
            </span>
            <span className="mdc-notched-outline">
              <span className="mdc-notched-outline__leading"></span>
              <span className="mdc-notched-outline__notch">
                {label && (
                  <span className="mdc-floating-label">
                    {label}
                    {required && <span className="form__required">*</span>}
                  </span>
                )}
              </span>
              <span className="mdc-notched-outline__trailing"></span>
            </span>
          </>
        ) : (
          <>
            <span className="mdc-text-field__ripple"></span>
            <span className="mdc-floating-label">
              {label}
              {required && <span className="form__required">*</span>}
            </span>
            <input type={type} {...inputProps} />
            <span className="mdc-line-ripple"></span>
          </>
        )}
      </div>
      
      {(error || helperText) && (
        <div className={`mdc-text-field-helper-line ${error ? 'mdc-text-field-helper-line--validation-msg' : ''}`}>
          <div className="mdc-text-field-helper-text mdc-text-field-helper-text--persistent">
            {error || helperText}
          </div>
        </div>
      )}
    </div>
  );
};

// セレクトフィールド
export const SelectField: React.FC<SelectFieldProps> = ({
  name,
  label,
  options,
  multiple = false,
  searchable = false,
  clearable = false,
  emptyText = '選択してください',
  required = false,
  disabled = false,
  className,
  testId,
  ...props
}) => {
  const { values, errors, touched, updateValue, handleBlur, disabled: formDisabled } = useFormContext();
  const selectRef = useRef<HTMLDivElement>(null);
  const [mdcSelect, setMdcSelect] = useState<MDCSelect | null>(null);

  const value = values[name];
  const error = touched[name] ? errors[name] : undefined;
  const isDisabled = disabled || formDisabled;

  useEffect(() => {
    if (selectRef.current) {
      const select = new MDCSelect(selectRef.current);
      setMdcSelect(select);
      
      select.listen('MDCSelect:change', () => {
        updateValue(name, select.value);
      });
      
      return () => {
        select.destroy();
      };
    }
  }, [name, updateValue]);

  const selectClasses = [
    'mdc-select',
    error && 'mdc-select--invalid',
    isDisabled && 'mdc-select--disabled',
    className
  ].filter(Boolean).join(' ');

  return (
    <div className="form__field">
      <div ref={selectRef} className={selectClasses} data-testid={testId}>
        <div className="mdc-select__anchor">
          <span className="mdc-select__ripple"></span>
          <span className="mdc-floating-label">
            {label}
            {required && <span className="form__required">*</span>}
          </span>
          <span className="mdc-select__selected-text-container">
            <span className="mdc-select__selected-text"></span>
          </span>
          <span className="mdc-select__dropdown-icon">
            <svg className="mdc-select__dropdown-icon-graphic" viewBox="7 10 10 5">
              <polygon className="mdc-select__dropdown-icon-inactive" stroke="none" fillRule="evenodd" points="7 10 12 15 17 10"></polygon>
              <polygon className="mdc-select__dropdown-icon-active" stroke="none" fillRule="evenodd" points="7 15 12 10 17 15"></polygon>
            </svg>
          </span>
          <span className="mdc-notched-outline">
            <span className="mdc-notched-outline__leading"></span>
            <span className="mdc-notched-outline__notch"></span>
            <span className="mdc-notched-outline__trailing"></span>
          </span>
        </div>

        <div className="mdc-select__menu mdc-menu mdc-menu-surface">
          <ul className="mdc-list">
            {!required && (
              <li className="mdc-list-item" data-value="">
                <span className="mdc-list-item__ripple"></span>
                <span className="mdc-list-item__text">{emptyText}</span>
              </li>
            )}
            {options.map((option) => (
              <li
                key={option.value}
                className="mdc-list-item"
                data-value={option.value}
                aria-selected={value === option.value}
              >
                <span className="mdc-list-item__ripple"></span>
                <span className="mdc-list-item__text">{option.label}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
      
      {(error || props.helperText) && (
        <div className={`mdc-text-field-helper-line ${error ? 'mdc-text-field-helper-line--validation-msg' : ''}`}>
          <div className="mdc-text-field-helper-text mdc-text-field-helper-text--persistent">
            {error || props.helperText}
          </div>
        </div>
      )}
    </div>
  );
};
```

---

## 5. 使用例

### 5.1 基本的な使用例

```typescript
import React from 'react';
import { Form, TextField, SelectField, CheckboxField } from '@/components/ui/Form';

interface UserFormData {
  name: string;
  email: string;
  age: number;
  department: string;
  newsletter: boolean;
}

export const UserForm = () => {
  const handleSubmit = async (values: UserFormData) => {
    console.log('送信データ:', values);
    // API送信処理
  };

  return (
    <Form<UserFormData>
      initialValues={{
        name: '',
        email: '',
        age: 0,
        department: '',
        newsletter: false
      }}
      onSubmit={handleSubmit}
      submitText="ユーザー登録"
      showResetButton
    >
      <TextField
        name="name"
        label="氏名"
        required
        placeholder="山田太郎"
      />
      
      <TextField
        name="email"
        label="メールアドレス"
        type="email"
        required
        placeholder="example@company.com"
      />
      
      <TextField
        name="age"
        label="年齢"
        type="number"
        required
      />
      
      <SelectField
        name="department"
        label="部署"
        required
        options={[
          { value: 'engineering', label: 'エンジニアリング' },
          { value: 'design', label: 'デザイン' },
          { value: 'marketing', label: 'マーケティング' },
          { value: 'sales', label: '営業' }
        ]}
      />
      
      <CheckboxField
        name="newsletter"
        label="ニュースレターを受信する"
      />
    </Form>
  );
};
```

---

## 6. 変更履歴

| 日付 | バージョン | 変更内容 | 担当者 |
|------|-----------|----------|--------|
| 2025/05/30 | 1.0.0 | 初版作成 | 開発チーム |

---

## 7. 関連ドキュメント

- [共通部品定義書](../../共通部品定義書.md)
- [Button コンポーネント](./Button.md)
- [Spinner コンポーネント](./Spinner.md)
- [SkillForm コンポーネント](../business-components/SkillForm.md)

---

このFormコンポーネントにより、統一されたフォーム体験と開発効率の向上を実現します。
