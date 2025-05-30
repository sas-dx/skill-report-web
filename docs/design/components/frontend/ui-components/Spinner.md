# Spinner コンポーネント定義書

## 1. 基本情報

- **部品名**: Spinner
- **カテゴリ**: フロントエンド - UIコンポーネント
- **責務**: ローディング状態の視覚的表示
- **依存関係**: なし（基盤UIコンポーネント）
- **作成日**: 2025/05/30
- **最終更新**: 2025/05/30

---

## 2. 概要

### 2.1 目的

Spinnerコンポーネントは、データの読み込み中やAPIリクエスト処理中などの待機状態をユーザーに視覚的に伝えるためのローディングインジケーターです。

### 2.2 特徴

- Material Design準拠のスピナーアニメーション
- 複数のサイズバリエーション
- カスタマイズ可能な色とスタイル
- アクセシビリティ対応
- 軽量で高パフォーマンス

---

## 3. インターフェース定義

### 3.1 Props

```typescript
interface SpinnerProps {
  /** スピナーのサイズ */
  size?: 'small' | 'medium' | 'large' | number;
  
  /** スピナーの色 */
  color?: 'primary' | 'secondary' | 'success' | 'warning' | 'error' | string;
  
  /** 表示状態 */
  visible?: boolean;
  
  /** ラベルテキスト */
  label?: string;
  
  /** ラベルの位置 */
  labelPosition?: 'top' | 'bottom' | 'left' | 'right';
  
  /** アニメーション速度（秒） */
  duration?: number;
  
  /** 背景オーバーレイを表示するか */
  overlay?: boolean;
  
  /** オーバーレイの透明度 */
  overlayOpacity?: number;
  
  /** カスタムクラス名 */
  className?: string;
  
  /** カスタムスタイル */
  style?: React.CSSProperties;
  
  /** テストID */
  testId?: string;
  
  /** アクセシビリティラベル */
  ariaLabel?: string;
}
```

### 3.2 デフォルト値

```typescript
const defaultProps: Partial<SpinnerProps> = {
  size: 'medium',
  color: 'primary',
  visible: true,
  labelPosition: 'bottom',
  duration: 1.4,
  overlay: false,
  overlayOpacity: 0.5,
  ariaLabel: '読み込み中'
};
```

---

## 4. 実装仕様

### 4.1 コンポーネント構造

```typescript
import React from 'react';
import { MDCCircularProgress } from '@material/circular-progress';
import './Spinner.scss';

export const Spinner: React.FC<SpinnerProps> = ({
  size = 'medium',
  color = 'primary',
  visible = true,
  label,
  labelPosition = 'bottom',
  duration = 1.4,
  overlay = false,
  overlayOpacity = 0.5,
  className,
  style,
  testId,
  ariaLabel = '読み込み中',
  ...props
}) => {
  const spinnerRef = useRef<HTMLDivElement>(null);
  const [circularProgress, setCircularProgress] = useState<MDCCircularProgress | null>(null);

  // MDC初期化
  useEffect(() => {
    if (spinnerRef.current && visible) {
      const progress = new MDCCircularProgress(spinnerRef.current);
      setCircularProgress(progress);
      
      return () => {
        progress.destroy();
      };
    }
  }, [visible]);

  // サイズの計算
  const getSize = (): number => {
    if (typeof size === 'number') return size;
    
    const sizeMap = {
      small: 24,
      medium: 48,
      large: 72
    };
    
    return sizeMap[size];
  };

  // 色の取得
  const getColor = (): string => {
    const colorMap = {
      primary: 'var(--mdc-theme-primary)',
      secondary: 'var(--mdc-theme-secondary)',
      success: 'var(--color-success)',
      warning: 'var(--color-warning)',
      error: 'var(--color-error)'
    };
    
    return colorMap[color as keyof typeof colorMap] || color;
  };

  if (!visible) return null;

  const spinnerSize = getSize();
  const spinnerColor = getColor();
  
  const spinnerClasses = [
    'spinner',
    `spinner--${size}`,
    `spinner--${color}`,
    overlay && 'spinner--overlay',
    className
  ].filter(Boolean).join(' ');

  const spinnerStyle: React.CSSProperties = {
    '--spinner-size': `${spinnerSize}px`,
    '--spinner-color': spinnerColor,
    '--spinner-duration': `${duration}s`,
    '--overlay-opacity': overlayOpacity,
    ...style
  };

  const renderSpinner = () => (
    <div className="spinner__container">
      <div
        ref={spinnerRef}
        className="mdc-circular-progress"
        style={{
          width: spinnerSize,
          height: spinnerSize
        }}
        role="progressbar"
        aria-label={ariaLabel}
        aria-valuemin={0}
        aria-valuemax={1}
        data-testid={testId}
      >
        <div className="mdc-circular-progress__determinate-container">
          <svg
            className="mdc-circular-progress__determinate-circle-graphic"
            viewBox="0 0 48 48"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle
              className="mdc-circular-progress__determinate-track"
              cx="24"
              cy="24"
              r="18"
              stroke="transparent"
            />
            <circle
              className="mdc-circular-progress__determinate-circle"
              cx="24"
              cy="24"
              r="18"
              strokeDasharray="113.097"
              strokeDashoffset="113.097"
              stroke={spinnerColor}
            />
          </svg>
        </div>
        <div className="mdc-circular-progress__indeterminate-container">
          <div className="mdc-circular-progress__spinner-layer">
            <div className="mdc-circular-progress__circle-clipper mdc-circular-progress__circle-left">
              <svg
                className="mdc-circular-progress__indeterminate-circle-graphic"
                viewBox="0 0 48 48"
                xmlns="http://www.w3.org/2000/svg"
              >
                <circle
                  cx="24"
                  cy="24"
                  r="18"
                  strokeDasharray="113.097"
                  strokeDashoffset="56.549"
                  stroke={spinnerColor}
                />
              </svg>
            </div>
            <div className="mdc-circular-progress__gap-patch">
              <svg
                className="mdc-circular-progress__indeterminate-circle-graphic"
                viewBox="0 0 48 48"
                xmlns="http://www.w3.org/2000/svg"
              >
                <circle
                  cx="24"
                  cy="24"
                  r="18"
                  strokeDasharray="113.097"
                  strokeDashoffset="56.549"
                  stroke={spinnerColor}
                />
              </svg>
            </div>
            <div className="mdc-circular-progress__circle-clipper mdc-circular-progress__circle-right">
              <svg
                className="mdc-circular-progress__indeterminate-circle-graphic"
                viewBox="0 0 48 48"
                xmlns="http://www.w3.org/2000/svg"
              >
                <circle
                  cx="24"
                  cy="24"
                  r="18"
                  strokeDasharray="113.097"
                  strokeDashoffset="56.549"
                  stroke={spinnerColor}
                />
              </svg>
            </div>
          </div>
        </div>
      </div>
      
      {label && (
        <div className={`spinner__label spinner__label--${labelPosition}`}>
          {label}
        </div>
      )}
    </div>
  );

  if (overlay) {
    return (
      <div className={spinnerClasses} style={spinnerStyle}>
        <div className="spinner__overlay" />
        {renderSpinner()}
      </div>
    );
  }

  return (
    <div className={spinnerClasses} style={spinnerStyle}>
      {renderSpinner()}
    </div>
  );
};

export default Spinner;
```

### 4.2 スタイル定義

```scss
@use '@material/circular-progress/mdc-circular-progress';

.spinner {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  position: relative;

  &--overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, var(--overlay-opacity));
    backdrop-filter: blur(2px);
  }

  &__container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    position: relative;
    z-index: 1;
  }

  &__label {
    font-size: 14px;
    color: var(--mdc-theme-text-secondary-on-background);
    text-align: center;
    white-space: nowrap;

    &--top {
      order: -1;
    }

    &--bottom {
      order: 1;
    }

    &--left {
      writing-mode: vertical-rl;
      text-orientation: mixed;
    }

    &--right {
      writing-mode: vertical-lr;
      text-orientation: mixed;
    }
  }

  // サイズバリエーション
  &--small {
    .spinner__label {
      font-size: 12px;
    }
  }

  &--large {
    .spinner__label {
      font-size: 16px;
    }
  }

  // 色バリエーション
  &--primary {
    .mdc-circular-progress__determinate-circle,
    .mdc-circular-progress__indeterminate-circle-graphic circle {
      stroke: var(--mdc-theme-primary);
    }
  }

  &--secondary {
    .mdc-circular-progress__determinate-circle,
    .mdc-circular-progress__indeterminate-circle-graphic circle {
      stroke: var(--mdc-theme-secondary);
    }
  }

  &--success {
    .mdc-circular-progress__determinate-circle,
    .mdc-circular-progress__indeterminate-circle-graphic circle {
      stroke: var(--color-success);
    }
  }

  &--warning {
    .mdc-circular-progress__determinate-circle,
    .mdc-circular-progress__indeterminate-circle-graphic circle {
      stroke: var(--color-warning);
    }
  }

  &--error {
    .mdc-circular-progress__determinate-circle,
    .mdc-circular-progress__indeterminate-circle-graphic circle {
      stroke: var(--color-error);
    }
  }
}

// アニメーション調整
.mdc-circular-progress {
  .mdc-circular-progress__indeterminate-container {
    animation-duration: var(--spinner-duration);
  }

  .mdc-circular-progress__spinner-layer {
    animation-duration: calc(var(--spinner-duration) * 4);
  }

  .mdc-circular-progress__circle-left .mdc-circular-progress__indeterminate-circle-graphic {
    animation-duration: calc(var(--spinner-duration) * 2);
  }

  .mdc-circular-progress__circle-right .mdc-circular-progress__indeterminate-circle-graphic {
    animation-duration: calc(var(--spinner-duration) * 2);
  }
}

// レスポンシブ対応
@media (max-width: 768px) {
  .spinner {
    &--large {
      .mdc-circular-progress {
        width: 56px !important;
        height: 56px !important;
      }
    }
  }
}

// ダークモード対応
@media (prefers-color-scheme: dark) {
  .spinner {
    &__label {
      color: var(--mdc-theme-text-primary-on-dark);
    }

    &__overlay {
      background-color: rgba(255, 255, 255, calc(var(--overlay-opacity) * 0.1));
    }
  }
}

// アクセシビリティ
@media (prefers-reduced-motion: reduce) {
  .mdc-circular-progress {
    .mdc-circular-progress__indeterminate-container,
    .mdc-circular-progress__spinner-layer,
    .mdc-circular-progress__circle-left .mdc-circular-progress__indeterminate-circle-graphic,
    .mdc-circular-progress__circle-right .mdc-circular-progress__indeterminate-circle-graphic {
      animation-duration: 0s;
    }
  }
}
```

---

## 5. 使用例

### 5.1 基本的な使用例

```typescript
import React from 'react';
import { Spinner } from '@/components/ui/Spinner';

// 基本的なスピナー
export const BasicSpinner = () => (
  <Spinner />
);

// サイズ指定
export const SizedSpinner = () => (
  <div>
    <Spinner size="small" />
    <Spinner size="medium" />
    <Spinner size="large" />
    <Spinner size={96} />
  </div>
);

// 色指定
export const ColoredSpinner = () => (
  <div>
    <Spinner color="primary" />
    <Spinner color="secondary" />
    <Spinner color="success" />
    <Spinner color="#ff6b6b" />
  </div>
);

// ラベル付き
export const LabeledSpinner = () => (
  <div>
    <Spinner label="読み込み中..." />
    <Spinner label="保存中..." labelPosition="top" />
    <Spinner label="処理中..." labelPosition="right" />
  </div>
);
```

### 5.2 実用的な使用例

```typescript
import React, { useState } from 'react';
import { Spinner } from '@/components/ui/Spinner';

// ローディング状態の管理
export const DataLoader = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  const loadData = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/data');
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error('データの読み込みに失敗しました:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button onClick={loadData} disabled={loading}>
        データを読み込む
      </button>
      
      {loading && (
        <Spinner 
          label="データを読み込み中..."
          overlay
          overlayOpacity={0.3}
        />
      )}
      
      {data && (
        <div>
          {/* データの表示 */}
        </div>
      )}
    </div>
  );
};

// フォーム送信時のスピナー
export const FormWithSpinner = () => {
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setSubmitting(true);
    
    try {
      // フォーム送信処理
      await submitForm();
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* フォームフィールド */}
      
      <button type="submit" disabled={submitting}>
        {submitting ? (
          <>
            <Spinner size="small" color="white" />
            送信中...
          </>
        ) : (
          '送信'
        )}
      </button>
    </form>
  );
};

// 条件付きスピナー表示
export const ConditionalSpinner = () => {
  const { data, loading, error } = useApiData();

  if (loading) {
    return (
      <div className="loading-container">
        <Spinner 
          size="large"
          label="データを読み込んでいます..."
          labelPosition="bottom"
        />
      </div>
    );
  }

  if (error) {
    return <div className="error">エラーが発生しました</div>;
  }

  return (
    <div>
      {/* データの表示 */}
    </div>
  );
};
```

### 5.3 カスタムフック連携

```typescript
import { useState, useEffect } from 'react';
import { Spinner } from '@/components/ui/Spinner';

// ローディング状態管理フック
export const useLoading = (initialState = false) => {
  const [loading, setLoading] = useState(initialState);

  const withLoading = async <T>(asyncFn: () => Promise<T>): Promise<T> => {
    setLoading(true);
    try {
      return await asyncFn();
    } finally {
      setLoading(false);
    }
  };

  return { loading, setLoading, withLoading };
};

// スピナー付きコンポーネント
export const SpinnerWrapper: React.FC<{
  loading: boolean;
  children: React.ReactNode;
  spinnerProps?: Partial<SpinnerProps>;
}> = ({ loading, children, spinnerProps = {} }) => {
  if (loading) {
    return (
      <Spinner 
        overlay
        label="処理中..."
        {...spinnerProps}
      />
    );
  }

  return <>{children}</>;
};
```

---

## 6. テスト仕様

### 6.1 単体テスト

```typescript
import React from 'react';
import { render, screen } from '@testing-library/react';
import { Spinner } from './Spinner';

describe('Spinner', () => {
  test('基本的なレンダリング', () => {
    render(<Spinner testId="spinner" />);
    expect(screen.getByTestId('spinner')).toBeInTheDocument();
  });

  test('ラベルの表示', () => {
    render(<Spinner label="読み込み中..." />);
    expect(screen.getByText('読み込み中...')).toBeInTheDocument();
  });

  test('非表示状態', () => {
    render(<Spinner visible={false} testId="spinner" />);
    expect(screen.queryByTestId('spinner')).not.toBeInTheDocument();
  });

  test('オーバーレイ表示', () => {
    render(<Spinner overlay testId="spinner" />);
    const spinner = screen.getByTestId('spinner');
    expect(spinner).toHaveClass('spinner--overlay');
  });

  test('アクセシビリティ属性', () => {
    render(<Spinner ariaLabel="カスタムラベル" testId="spinner" />);
    const progressbar = screen.getByRole('progressbar');
    expect(progressbar).toHaveAttribute('aria-label', 'カスタムラベル');
  });
});
```

### 6.2 統合テスト

```typescript
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { DataLoader } from './examples';

describe('Spinner Integration', () => {
  test('ローディング状態の切り替え', async () => {
    render(<DataLoader />);
    
    const button = screen.getByText('データを読み込む');
    fireEvent.click(button);
    
    expect(screen.getByText('データを読み込み中...')).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.queryByText('データを読み込み中...')).not.toBeInTheDocument();
    });
  });
});
```

---

## 7. パフォーマンス考慮事項

### 7.1 最適化ポイント

- **遅延レンダリング**: 短時間のローディングでは表示しない
- **アニメーション最適化**: CSS transformを使用
- **メモ化**: 不要な再レンダリングを防止

### 7.2 実装例

```typescript
import React, { memo, useMemo } from 'react';

export const OptimizedSpinner = memo<SpinnerProps>(({
  size,
  color,
  visible,
  delay = 200,
  ...props
}) => {
  const [shouldShow, setShouldShow] = useState(false);

  useEffect(() => {
    if (visible) {
      const timer = setTimeout(() => setShouldShow(true), delay);
      return () => clearTimeout(timer);
    } else {
      setShouldShow(false);
    }
  }, [visible, delay]);

  const spinnerStyle = useMemo(() => ({
    '--spinner-size': typeof size === 'number' ? `${size}px` : undefined,
    '--spinner-color': typeof color === 'string' ? color : undefined,
  }), [size, color]);

  if (!shouldShow) return null;

  return <Spinner style={spinnerStyle} {...props} />;
});
```

---

## 8. アクセシビリティ

### 8.1 対応項目

- **ARIA属性**: role="progressbar", aria-label
- **キーボードナビゲーション**: フォーカス管理
- **スクリーンリーダー**: 適切な読み上げ
- **モーション配慮**: prefers-reduced-motion対応

### 8.2 実装ガイドライン

```typescript
// アクセシビリティ強化版
export const AccessibleSpinner: React.FC<SpinnerProps> = ({
  ariaLabel = '読み込み中',
  announceChanges = true,
  ...props
}) => {
  const [announced, setAnnounced] = useState(false);

  useEffect(() => {
    if (props.visible && announceChanges && !announced) {
      // スクリーンリーダーへの通知
      const announcement = document.createElement('div');
      announcement.setAttribute('aria-live', 'polite');
      announcement.setAttribute('aria-atomic', 'true');
      announcement.className = 'sr-only';
      announcement.textContent = ariaLabel;
      
      document.body.appendChild(announcement);
      setAnnounced(true);
      
      return () => {
        document.body.removeChild(announcement);
      };
    }
  }, [props.visible, announceChanges, ariaLabel, announced]);

  return <Spinner ariaLabel={ariaLabel} {...props} />;
};
```

---

## 9. 変更履歴

| 日付 | バージョン | 変更内容 | 担当者 |
|------|-----------|----------|--------|
| 2025/05/30 | 1.0.0 | 初版作成 | 開発チーム |

---

## 10. 関連ドキュメント

- [共通部品定義書](../../共通部品定義書.md)
- [Button コンポーネント](./Button.md)
- [Form コンポーネント](../Form.md)
- [UI/UX共通仕様書](../../../requirements/UI_UX共通仕様書.md)

---

このSpinnerコンポーネントにより、統一されたローディング表示とユーザーエクスペリエンスの向上を実現します。
