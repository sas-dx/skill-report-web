# Button コンポーネント定義書

## 1. 基本情報

- **部品名**: Button
- **カテゴリ**: UI基本部品
- **責務**: ユーザーアクション実行のトリガー
- **依存関係**: なし（基本部品）
- **作成日**: 2025/05/30
- **最終更新**: 2025/05/30

---

## 2. インターフェース仕様

### 2.1 Props定義

| 名前 | 型 | 必須 | デフォルト | 説明 |
|------|----|----|----------|------|
| variant | `'primary'` \| `'secondary'` \| `'danger'` \| `'ghost'` | No | `'primary'` | ボタンの種類 |
| size | `'sm'` \| `'base'` \| `'lg'` | No | `'base'` | ボタンのサイズ |
| disabled | `boolean` | No | `false` | 無効状態 |
| loading | `boolean` | No | `false` | ローディング状態 |
| fullWidth | `boolean` | No | `false` | 全幅表示 |
| icon | `ReactNode` | No | - | アイコン（左側） |
| iconRight | `ReactNode` | No | - | アイコン（右側） |
| children | `ReactNode` | Yes | - | ボタンテキスト |
| onClick | `() => void` | No | - | クリックイベント |
| type | `'button'` \| `'submit'` \| `'reset'` | No | `'button'` | ボタンタイプ |
| className | `string` | No | - | 追加CSSクラス |

### 2.2 戻り値
- `JSX.Element`

### 2.3 イベント
- **onClick**: ボタンクリック時に発火
- **onFocus**: フォーカス取得時に発火
- **onBlur**: フォーカス失去時に発火

---

## 3. 実装仕様

### 3.1 技術スタック
- **React**: 18.x
- **TypeScript**: 5.x
- **Tailwind CSS**: 3.x
- **Heroicons**: 2.x（アイコン）
- **clsx**: クラス名結合

### 3.2 型定義

```typescript
import { ReactNode, ButtonHTMLAttributes } from 'react';

export interface ButtonProps extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'type'> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'base' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
  icon?: ReactNode;
  iconRight?: ReactNode;
  children: ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  className?: string;
}
```

### 3.3 内部構造

```typescript
import React from 'react';
import clsx from 'clsx';
import { ButtonProps } from './Button.types';
import { Spinner } from '../Spinner';

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'base',
  disabled = false,
  loading = false,
  fullWidth = false,
  icon,
  iconRight,
  children,
  onClick,
  type = 'button',
  className,
  ...props
}) => {
  const baseClasses = [
    'inline-flex',
    'items-center',
    'justify-center',
    'font-medium',
    'rounded-md',
    'transition-all',
    'duration-200',
    'focus:outline-none',
    'focus:ring-2',
    'focus:ring-offset-2',
    'disabled:opacity-50',
    'disabled:cursor-not-allowed',
    'disabled:transform-none'
  ];

  const variantClasses = {
    primary: [
      'bg-primary-500',
      'text-white',
      'hover:bg-primary-600',
      'focus:ring-primary-500',
      'active:bg-primary-700'
    ],
    secondary: [
      'bg-white',
      'text-primary-500',
      'border',
      'border-primary-500',
      'hover:bg-primary-50',
      'focus:ring-primary-500',
      'active:bg-primary-100'
    ],
    danger: [
      'bg-error-500',
      'text-white',
      'hover:bg-error-600',
      'focus:ring-error-500',
      'active:bg-error-700'
    ],
    ghost: [
      'bg-transparent',
      'text-gray-700',
      'hover:bg-gray-100',
      'focus:ring-gray-500',
      'active:bg-gray-200'
    ]
  };

  const sizeClasses = {
    sm: ['px-3', 'py-2', 'text-sm', 'gap-1'],
    base: ['px-4', 'py-2', 'text-base', 'gap-2'],
    lg: ['px-6', 'py-3', 'text-lg', 'gap-2']
  };

  const classes = clsx(
    baseClasses,
    variantClasses[variant],
    sizeClasses[size],
    {
      'w-full': fullWidth,
      'hover:transform hover:-translate-y-0.5 hover:shadow-lg': !disabled && !loading,
    },
    className
  );

  const handleClick = () => {
    if (!disabled && !loading && onClick) {
      onClick();
    }
  };

  return (
    <button
      type={type}
      className={classes}
      disabled={disabled || loading}
      onClick={handleClick}
      {...props}
    >
      {loading && <Spinner size={size === 'sm' ? 'sm' : 'base'} />}
      {!loading && icon && <span className="flex-shrink-0">{icon}</span>}
      <span>{children}</span>
      {!loading && iconRight && <span className="flex-shrink-0">{iconRight}</span>}
    </button>
  );
};

Button.displayName = 'Button';
```

### 3.4 状態管理
- **内部状態**: なし（ステートレス）
- **外部制御**: プロパティによる完全制御
- **副作用**: なし

---

## 4. 使用例・サンプルコード

### 4.1 基本的な使用例

```tsx
import { Button } from '@/components/ui/Button';
import { PlusIcon, TrashIcon } from '@heroicons/react/24/outline';

// プライマリボタン
<Button onClick={handleSave}>
  保存
</Button>

// セカンダリボタン
<Button variant="secondary" onClick={handleCancel}>
  キャンセル
</Button>

// 危険なアクション
<Button variant="danger" onClick={handleDelete}>
  削除
</Button>

// アイコン付きボタン
<Button icon={<PlusIcon className="w-4 h-4" />}>
  新規作成
</Button>

// ローディング状態
<Button loading disabled>
  保存中...
</Button>

// 全幅ボタン
<Button fullWidth>
  送信
</Button>
```

### 4.2 スキル報告書での使用例

```tsx
// スキル保存ボタン
<Button 
  variant="primary" 
  onClick={handleSkillSave}
  disabled={!isFormValid}
  loading={isSaving}
>
  スキル保存
</Button>

// 下書き保存ボタン
<Button 
  variant="secondary" 
  size="sm"
  onClick={handleDraftSave}
  icon={<DocumentIcon className="w-4 h-4" />}
>
  下書き保存
</Button>

// スキル削除ボタン
<Button 
  variant="danger"
  size="sm"
  onClick={() => handleSkillDelete(skill.id)}
  icon={<TrashIcon className="w-4 h-4" />}
>
  削除
</Button>

// エクスポートボタン
<Button 
  variant="ghost"
  onClick={handleExport}
  iconRight={<ArrowDownTrayIcon className="w-4 h-4" />}
>
  エクスポート
</Button>
```

### 4.3 フォームでの使用例

```tsx
// フォーム送信
<form onSubmit={handleSubmit}>
  <div className="flex gap-2 justify-end">
    <Button 
      type="button" 
      variant="secondary" 
      onClick={handleReset}
    >
      リセット
    </Button>
    <Button 
      type="submit" 
      loading={isSubmitting}
      disabled={!isValid}
    >
      送信
    </Button>
  </div>
</form>
```

---

## 5. テスト仕様

### 5.1 単体テスト

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  test('基本的なレンダリング', () => {
    render(<Button>テストボタン</Button>);
    expect(screen.getByRole('button')).toHaveTextContent('テストボタン');
  });

  test('クリックイベントの発火', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>クリック</Button>);
    
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  test('無効状態の動作', () => {
    const handleClick = jest.fn();
    render(<Button disabled onClick={handleClick}>無効ボタン</Button>);
    
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).not.toHaveBeenCalled();
    expect(screen.getByRole('button')).toBeDisabled();
  });

  test('ローディング状態の表示', () => {
    render(<Button loading>ローディング</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
    expect(screen.getByTestId('spinner')).toBeInTheDocument();
  });

  test('バリアント別スタイル適用', () => {
    const { rerender } = render(<Button variant="primary">プライマリ</Button>);
    expect(screen.getByRole('button')).toHaveClass('bg-primary-500');

    rerender(<Button variant="secondary">セカンダリ</Button>);
    expect(screen.getByRole('button')).toHaveClass('border-primary-500');

    rerender(<Button variant="danger">危険</Button>);
    expect(screen.getByRole('button')).toHaveClass('bg-error-500');
  });

  test('サイズ別スタイル適用', () => {
    const { rerender } = render(<Button size="sm">小</Button>);
    expect(screen.getByRole('button')).toHaveClass('px-3', 'py-2', 'text-sm');

    rerender(<Button size="lg">大</Button>);
    expect(screen.getByRole('button')).toHaveClass('px-6', 'py-3', 'text-lg');
  });

  test('アイコン表示', () => {
    render(
      <Button icon={<span data-testid="icon">📝</span>}>
        アイコン付き
      </Button>
    );
    expect(screen.getByTestId('icon')).toBeInTheDocument();
  });

  test('全幅表示', () => {
    render(<Button fullWidth>全幅</Button>);
    expect(screen.getByRole('button')).toHaveClass('w-full');
  });
});
```

### 5.2 アクセシビリティテスト

```typescript
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('Button アクセシビリティ', () => {
  test('WCAG準拠', async () => {
    const { container } = render(<Button>アクセシブルボタン</Button>);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  test('キーボード操作', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>キーボードテスト</Button>);
    
    const button = screen.getByRole('button');
    button.focus();
    
    fireEvent.keyDown(button, { key: 'Enter' });
    expect(handleClick).toHaveBeenCalledTimes(1);
    
    fireEvent.keyDown(button, { key: ' ' });
    expect(handleClick).toHaveBeenCalledTimes(2);
  });

  test('フォーカス表示', () => {
    render(<Button>フォーカステスト</Button>);
    const button = screen.getByRole('button');
    
    button.focus();
    expect(button).toHaveFocus();
    expect(button).toHaveClass('focus:ring-2');
  });
});
```

### 5.3 E2Eテスト

```typescript
// tests/e2e/button.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Button E2E', () => {
  test('スキル保存ボタンの動作', async ({ page }) => {
    await page.goto('/skills/new');
    
    // フォーム入力
    await page.fill('[data-testid="skill-name"]', 'JavaScript');
    await page.selectOption('[data-testid="skill-level"]', '中級');
    
    // 保存ボタンクリック
    await page.click('[data-testid="save-button"]');
    
    // ローディング状態確認
    await expect(page.locator('[data-testid="save-button"]')).toBeDisabled();
    await expect(page.locator('[data-testid="spinner"]')).toBeVisible();
    
    // 成功メッセージ確認
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
  });

  test('削除確認ダイアログ', async ({ page }) => {
    await page.goto('/skills');
    
    // 削除ボタンクリック
    await page.click('[data-testid="delete-button-1"]');
    
    // 確認ダイアログ表示
    await expect(page.locator('[data-testid="confirm-dialog"]')).toBeVisible();
    
    // 確認ボタンクリック
    await page.click('[data-testid="confirm-delete"]');
    
    // 削除完了確認
    await expect(page.locator('[data-testid="skill-item-1"]')).not.toBeVisible();
  });
});
```

---

## 6. パフォーマンス要件

### 6.1 レンダリング性能
- **初回レンダリング**: 16ms以内
- **再レンダリング**: 8ms以内
- **メモリ使用量**: 1MB以下

### 6.2 バンドルサイズ
- **コンポーネント本体**: 2KB以下（gzip圧縮後）
- **依存関係込み**: 5KB以下（gzip圧縮後）

### 6.3 最適化手法
- **React.memo**: 不要な再レンダリング防止
- **useMemo**: 重い計算のメモ化
- **Tree Shaking**: 未使用コードの除去

```typescript
import React, { memo, useMemo } from 'react';

export const Button = memo<ButtonProps>(({
  variant = 'primary',
  size = 'base',
  // ... other props
}) => {
  const classes = useMemo(() => {
    return clsx(
      baseClasses,
      variantClasses[variant],
      sizeClasses[size],
      // ... other classes
    );
  }, [variant, size, fullWidth, disabled, loading]);

  // ... component implementation
});
```

---

## 7. アクセシビリティ要件

### 7.1 WCAG 2.1 AA準拠

#### コントラスト比
- **通常状態**: 4.5:1以上
- **フォーカス状態**: 3:1以上
- **無効状態**: 3:1以上

#### キーボード操作
- **Tab**: フォーカス移動
- **Enter/Space**: ボタン実行
- **Escape**: フォーカス解除（モーダル内）

#### スクリーンリーダー対応
```typescript
<button
  type={type}
  className={classes}
  disabled={disabled || loading}
  onClick={handleClick}
  aria-label={loading ? `${children} 実行中` : undefined}
  aria-disabled={disabled || loading}
  {...props}
>
  {/* content */}
</button>
```

### 7.2 フォーカス管理
- **フォーカス表示**: 明確な視覚的インジケーター
- **フォーカス順序**: 論理的なタブ順序
- **フォーカストラップ**: モーダル内での適切な制御

### 7.3 状態通知
- **ローディング状態**: `aria-label`で状態通知
- **エラー状態**: `aria-describedby`でエラー関連付け
- **成功状態**: `role="status"`で完了通知

---

## 8. セキュリティ要件

### 8.1 XSS対策
- **入力値サニタイズ**: `children`の適切なエスケープ
- **innerHTML禁止**: `dangerouslySetInnerHTML`使用禁止

### 8.2 CSRF対策
- **フォーム送信**: CSRFトークン必須
- **重要操作**: 二重送信防止

### 8.3 クリックジャッキング対策
- **重要ボタン**: 適切な配置・サイズ
- **視覚的確認**: 操作前の確認ダイアログ

---

## 9. 変更履歴

| 日付 | バージョン | 変更内容 | 担当者 |
|------|-----------|----------|--------|
| 2025/05/30 | 1.0.0 | 初版作成 | 開発チーム |

---

## 10. 関連ドキュメント

- [UI/UX共通仕様書](../../../requirements/UI_UX共通仕様書.md)
- [共通部品定義書](../../共通部品定義書.md)
- [Spinner コンポーネント](./Spinner.md)
- [Form コンポーネント](../Form.md)

---

## 11. 実装チェックリスト

### 開発時
- [ ] TypeScript型定義完了
- [ ] Tailwind CSSクラス適用
- [ ] Props検証実装
- [ ] デフォルト値設定
- [ ] イベントハンドラー実装

### テスト時
- [ ] 単体テスト実装（80%以上カバレッジ）
- [ ] アクセシビリティテスト実行
- [ ] ビジュアルリグレッションテスト
- [ ] パフォーマンステスト実行

### リリース前
- [ ] Storybook登録
- [ ] ドキュメント更新
- [ ] 使用例追加
- [ ] レビュー完了

---

このButton定義書に基づいて、一貫性があり、アクセシブルで、高性能なボタンコンポーネントを実装します。
