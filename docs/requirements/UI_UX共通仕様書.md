# UI/UX共通仕様書: 年間スキル報告書WEB化PJT

## 1. 文書基本情報

- **文書名**: UI/UX共通仕様書
- **プロジェクト名**: 年間スキル報告書WEB化PJT
- **対象システム**: 年間スキル報告書Webアプリケーション
- **技術スタック**: Next.js 14 + TypeScript + React 18 + Tailwind CSS
- **作成日**: 2025/05/30
- **作成者**: システム設計担当
- **改訂履歴**: 2025/05/30 初版作成

---

## 2. 基本設計方針

### 2.1 デザインコンセプト
- **シンプル・直感的**: 業務効率を重視したミニマルデザイン
- **アクセシブル**: WCAG 2.1 AA準拠、全ユーザーが利用可能
- **レスポンシブ**: PC・タブレット・スマートフォン対応
- **一貫性**: 全画面で統一されたUI/UX

### 2.2 ユーザビリティ原則
- **3ステップ以内**: 目的の画面・機能へ3ステップ以内でアクセス
- **1秒以内**: API〜UI まで1秒以内のレスポンス
- **直感的操作**: 説明不要で操作可能なインターフェース
- **エラー防止**: 入力ミス・操作ミスを事前に防ぐ設計

---

## 3. カラーパレット

### 3.1 プライマリカラー
```css
/* メインブランドカラー */
--primary-50: #eff6ff;    /* 背景・薄い強調 */
--primary-100: #dbeafe;   /* ホバー背景 */
--primary-200: #bfdbfe;   /* 無効状態 */
--primary-300: #93c5fd;   /* ボーダー */
--primary-400: #60a5fa;   /* アイコン */
--primary-500: #3b82f6;   /* メインボタン */
--primary-600: #2563eb;   /* ホバー状態 */
--primary-700: #1d4ed8;   /* アクティブ状態 */
--primary-800: #1e40af;   /* 濃い強調 */
--primary-900: #1e3a8a;   /* 最濃色 */
```

### 3.2 セカンダリカラー
```css
/* サブカラー（グレー系） */
--gray-50: #f9fafb;       /* 背景 */
--gray-100: #f3f4f6;      /* カード背景 */
--gray-200: #e5e7eb;      /* ボーダー */
--gray-300: #d1d5db;      /* 無効テキスト */
--gray-400: #9ca3af;      /* プレースホルダー */
--gray-500: #6b7280;      /* 補助テキスト */
--gray-600: #4b5563;      /* 通常テキスト */
--gray-700: #374151;      /* 見出し */
--gray-800: #1f2937;      /* 強調テキスト */
--gray-900: #111827;      /* 最濃テキスト */
```

### 3.3 ステータスカラー
```css
/* 成功・エラー・警告・情報 */
--success-50: #f0fdf4;    /* 成功背景 */
--success-500: #22c55e;   /* 成功メイン */
--success-600: #16a34a;   /* 成功ホバー */

--error-50: #fef2f2;      /* エラー背景 */
--error-500: #ef4444;     /* エラーメイン */
--error-600: #dc2626;     /* エラーホバー */

--warning-50: #fffbeb;    /* 警告背景 */
--warning-500: #f59e0b;   /* 警告メイン */
--warning-600: #d97706;   /* 警告ホバー */

--info-50: #eff6ff;       /* 情報背景 */
--info-500: #3b82f6;      /* 情報メイン */
--info-600: #2563eb;      /* 情報ホバー */
```

---

## 4. タイポグラフィ

### 4.1 フォントファミリー
```css
/* 日本語・英語混在対応 */
--font-family-base: 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', 'Yu Gothic Medium', 'Meiryo', 'MS PGothic', sans-serif;
--font-family-mono: 'SFMono-Regular', 'Consolas', 'Liberation Mono', 'Menlo', monospace;
```

### 4.2 フォントサイズ・行間
```css
/* テキストサイズ階層 */
--text-xs: 0.75rem;       /* 12px - 注釈・補助情報 */
--text-sm: 0.875rem;      /* 14px - 小さなラベル */
--text-base: 1rem;        /* 16px - 基本テキスト */
--text-lg: 1.125rem;      /* 18px - 強調テキスト */
--text-xl: 1.25rem;       /* 20px - 小見出し */
--text-2xl: 1.5rem;       /* 24px - 中見出し */
--text-3xl: 1.875rem;     /* 30px - 大見出し */
--text-4xl: 2.25rem;      /* 36px - ページタイトル */

/* 行間 */
--leading-tight: 1.25;    /* 見出し用 */
--leading-normal: 1.5;    /* 本文用 */
--leading-relaxed: 1.625; /* 長文用 */
```

### 4.3 フォントウェイト
```css
--font-light: 300;        /* 軽い強調 */
--font-normal: 400;       /* 通常テキスト */
--font-medium: 500;       /* 中程度強調 */
--font-semibold: 600;     /* 強調 */
--font-bold: 700;         /* 見出し */
```

---

## 5. スペーシング・レイアウト

### 5.1 スペーシングシステム
```css
/* 8px基準のスペーシング */
--space-1: 0.25rem;       /* 4px */
--space-2: 0.5rem;        /* 8px */
--space-3: 0.75rem;       /* 12px */
--space-4: 1rem;          /* 16px */
--space-5: 1.25rem;       /* 20px */
--space-6: 1.5rem;        /* 24px */
--space-8: 2rem;          /* 32px */
--space-10: 2.5rem;       /* 40px */
--space-12: 3rem;         /* 48px */
--space-16: 4rem;         /* 64px */
--space-20: 5rem;         /* 80px */
--space-24: 6rem;         /* 96px */
```

### 5.2 レイアウトグリッド
```css
/* コンテナ幅 */
--container-sm: 640px;    /* スマートフォン */
--container-md: 768px;    /* タブレット */
--container-lg: 1024px;   /* デスクトップ */
--container-xl: 1280px;   /* 大画面 */
--container-2xl: 1536px;  /* 超大画面 */

/* グリッド間隔 */
--gap-4: 1rem;            /* 基本間隔 */
--gap-6: 1.5rem;          /* 中間隔 */
--gap-8: 2rem;            /* 大間隔 */
```

---

## 6. コンポーネント仕様

### 6.1 ボタン

#### プライマリボタン
```css
/* 基本スタイル */
.btn-primary {
  background-color: var(--primary-500);
  color: white;
  padding: var(--space-3) var(--space-6);
  border-radius: 0.375rem; /* 6px */
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  border: none;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

/* ホバー状態 */
.btn-primary:hover {
  background-color: var(--primary-600);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

/* アクティブ状態 */
.btn-primary:active {
  background-color: var(--primary-700);
  transform: translateY(0);
}

/* 無効状態 */
.btn-primary:disabled {
  background-color: var(--gray-300);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}
```

#### セカンダリボタン
```css
.btn-secondary {
  background-color: white;
  color: var(--primary-500);
  border: 1px solid var(--primary-500);
  padding: var(--space-3) var(--space-6);
  border-radius: 0.375rem;
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.btn-secondary:hover {
  background-color: var(--primary-50);
  border-color: var(--primary-600);
}
```

#### ボタンサイズバリエーション
```css
/* 小サイズ */
.btn-sm {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
}

/* 大サイズ */
.btn-lg {
  padding: var(--space-4) var(--space-8);
  font-size: var(--text-lg);
}

/* 全幅 */
.btn-full {
  width: 100%;
}
```

### 6.2 フォーム要素

#### 入力フィールド
```css
.form-input {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--gray-300);
  border-radius: 0.375rem;
  font-size: var(--text-base);
  background-color: white;
  transition: all 0.2s ease-in-out;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-500);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input:invalid {
  border-color: var(--error-500);
}

.form-input:disabled {
  background-color: var(--gray-100);
  color: var(--gray-500);
  cursor: not-allowed;
}
```

#### ラベル
```css
.form-label {
  display: block;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--gray-700);
  margin-bottom: var(--space-2);
}

.form-label.required::after {
  content: ' *';
  color: var(--error-500);
}
```

#### セレクトボックス
```css
.form-select {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--gray-300);
  border-radius: 0.375rem;
  font-size: var(--text-base);
  background-color: white;
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3E%3Cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3E%3C/svg%3E");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}
```

#### チェックボックス・ラジオボタン
```css
.form-checkbox,
.form-radio {
  width: 1rem;
  height: 1rem;
  border: 1px solid var(--gray-300);
  background-color: white;
  cursor: pointer;
}

.form-checkbox {
  border-radius: 0.25rem;
}

.form-radio {
  border-radius: 50%;
}

.form-checkbox:checked,
.form-radio:checked {
  background-color: var(--primary-500);
  border-color: var(--primary-500);
}
```

### 6.3 カード・パネル

#### 基本カード
```css
.card {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--gray-200);
  overflow: hidden;
}

.card-header {
  padding: var(--space-6);
  border-bottom: 1px solid var(--gray-200);
  background-color: var(--gray-50);
}

.card-body {
  padding: var(--space-6);
}

.card-footer {
  padding: var(--space-6);
  border-top: 1px solid var(--gray-200);
  background-color: var(--gray-50);
}
```

### 6.4 テーブル

#### 基本テーブル
```css
.table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--gray-200);
}

.table th {
  background-color: var(--gray-50);
  padding: var(--space-3) var(--space-4);
  text-align: left;
  font-weight: var(--font-semibold);
  color: var(--gray-700);
  border-bottom: 1px solid var(--gray-200);
  font-size: var(--text-sm);
  white-space: nowrap;
}

.table td {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--gray-200);
  font-size: var(--text-sm);
  color: var(--gray-600);
  vertical-align: middle;
}

.table tbody tr:hover {
  background-color: var(--gray-50);
  transition: background-color 0.2s ease-in-out;
}

.table tbody tr:nth-child(even) {
  background-color: var(--gray-25);
}

.table tbody tr:nth-child(even):hover {
  background-color: var(--gray-75);
}

/* テーブル内のアクションボタン */
.table-action-btn {
  padding: var(--space-1) var(--space-3);
  font-size: var(--text-xs);
  border-radius: 0.25rem;
  border: 1px solid var(--primary-300);
  background-color: white;
  color: var(--primary-600);
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.table-action-btn:hover {
  background-color: var(--primary-50);
  border-color: var(--primary-400);
}

/* レスポンシブテーブル */
.table-responsive {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

@media (max-width: 767px) {
  .table-responsive .table {
    min-width: 600px;
  }
  
  .table th,
  .table td {
    padding: var(--space-2) var(--space-3);
    font-size: var(--text-xs);
  }
}
```

#### データテーブル（一覧表示）
```css
.data-table {
  background-color: white;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--gray-200);
}

.data-table-header {
  background-color: var(--gray-50);
  padding: var(--space-4) var(--space-6);
  border-bottom: 1px solid var(--gray-200);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.data-table-title {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--gray-900);
}

.data-table-actions {
  display: flex;
  gap: var(--space-2);
}

.data-table-body {
  padding: var(--space-4);
}

.data-table-filters {
  display: flex;
  gap: var(--space-4);
  margin-bottom: var(--space-4);
  align-items: center;
  flex-wrap: wrap;
}

.data-table-filter-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.data-table-filter-label {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--gray-700);
  white-space: nowrap;
}

/* 空状態 */
.data-table-empty {
  text-align: center;
  padding: var(--space-12) var(--space-6);
  color: var(--gray-500);
}

.data-table-empty-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto var(--space-4);
  color: var(--gray-300);
}

.data-table-empty-title {
  font-size: var(--text-lg);
  font-weight: var(--font-medium);
  color: var(--gray-900);
  margin-bottom: var(--space-2);
}

.data-table-empty-description {
  font-size: var(--text-sm);
  color: var(--gray-500);
}
```

### 6.5 ナビゲーション

#### ヘッダーナビゲーション
```css
.header-nav {
  background-color: white;
  border-bottom: 1px solid var(--gray-200);
  padding: var(--space-4) 0;
}

.nav-item {
  padding: var(--space-2) var(--space-4);
  color: var(--gray-600);
  text-decoration: none;
  border-radius: 0.375rem;
  transition: all 0.2s ease-in-out;
}

.nav-item:hover {
  background-color: var(--gray-100);
  color: var(--gray-900);
}

.nav-item.active {
  background-color: var(--primary-100);
  color: var(--primary-700);
}
```

#### サイドバーナビゲーション
```css
.sidebar {
  width: 256px;
  background-color: var(--gray-50);
  border-right: 1px solid var(--gray-200);
  height: 100vh;
  overflow-y: auto;
}

.sidebar-item {
  display: block;
  padding: var(--space-3) var(--space-4);
  color: var(--gray-700);
  text-decoration: none;
  border-left: 3px solid transparent;
  transition: all 0.2s ease-in-out;
}

.sidebar-item:hover {
  background-color: var(--gray-100);
  border-left-color: var(--primary-300);
}

.sidebar-item.active {
  background-color: var(--primary-50);
  color: var(--primary-700);
  border-left-color: var(--primary-500);
}
```

#### ハンバーガーメニュー

##### 基本仕様
- **表示条件**: 画面幅768px未満（タブレット・スマートフォン）
- **配置**: ヘッダー左上、ロゴの左側
- **サイズ**: 44px × 44px（タッチフレンドリー）
- **アニメーション**: 開閉時のスムーズなトランジション

##### ハンバーガーアイコン
```css
.hamburger-menu {
  display: none;
  width: 44px;
  height: 44px;
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--space-2);
  border-radius: 0.375rem;
  transition: background-color 0.2s ease-in-out;
}

.hamburger-menu:hover {
  background-color: var(--gray-100);
}

.hamburger-menu:focus {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* ハンバーガーアイコンの線 */
.hamburger-lines {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 24px;
  height: 18px;
}

.hamburger-line {
  width: 100%;
  height: 2px;
  background-color: var(--gray-700);
  border-radius: 1px;
  transition: all 0.3s ease-in-out;
  transform-origin: center;
}

/* アクティブ状態（×マーク） */
.hamburger-menu.active .hamburger-line:nth-child(1) {
  transform: rotate(45deg) translate(6px, 6px);
}

.hamburger-menu.active .hamburger-line:nth-child(2) {
  opacity: 0;
}

.hamburger-menu.active .hamburger-line:nth-child(3) {
  transform: rotate(-45deg) translate(6px, -6px);
}

/* レスポンシブ表示 */
@media (max-width: 767px) {
  .hamburger-menu {
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
```

##### モバイルメニューオーバーレイ
```css
.mobile-menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 998;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease-in-out;
}

.mobile-menu-overlay.active {
  opacity: 1;
  visibility: visible;
}

.mobile-menu {
  position: fixed;
  top: 0;
  left: -100%;
  width: 280px;
  height: 100%;
  background-color: white;
  z-index: 999;
  overflow-y: auto;
  transition: left 0.3s ease-in-out;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
}

.mobile-menu.active {
  left: 0;
}

.mobile-menu-header {
  padding: var(--space-4);
  border-bottom: 1px solid var(--gray-200);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mobile-menu-close {
  width: 32px;
  height: 32px;
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--space-1);
  border-radius: 0.25rem;
  color: var(--gray-500);
}

.mobile-menu-close:hover {
  background-color: var(--gray-100);
  color: var(--gray-700);
}

.mobile-menu-nav {
  padding: var(--space-4) 0;
}

.mobile-menu-item {
  display: block;
  padding: var(--space-3) var(--space-4);
  color: var(--gray-700);
  text-decoration: none;
  border-bottom: 1px solid var(--gray-100);
  transition: background-color 0.2s ease-in-out;
}

.mobile-menu-item:hover {
  background-color: var(--gray-50);
}

.mobile-menu-item.active {
  background-color: var(--primary-50);
  color: var(--primary-700);
  border-left: 3px solid var(--primary-500);
}

/* サブメニュー */
.mobile-submenu {
  background-color: var(--gray-50);
  border-top: 1px solid var(--gray-200);
}

.mobile-submenu-item {
  padding: var(--space-2) var(--space-6);
  font-size: var(--text-sm);
  color: var(--gray-600);
}
```

##### JavaScript実装例
```typescript
// MobileMenu.tsx
interface MobileMenuProps {
  isOpen: boolean;
  onClose: () => void;
  menuItems: MenuItem[];
}

export const MobileMenu: React.FC<MobileMenuProps> = ({
  isOpen,
  onClose,
  menuItems
}) => {
  // ESCキーでメニューを閉じる
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  // メニューが開いている間はボディのスクロールを無効化
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  return (
    <>
      {/* オーバーレイ */}
      <div
        className={`mobile-menu-overlay ${isOpen ? 'active' : ''}`}
        onClick={onClose}
        aria-hidden="true"
      />
      
      {/* メニュー本体 */}
      <nav
        className={`mobile-menu ${isOpen ? 'active' : ''}`}
        role="navigation"
        aria-label="モバイルメニュー"
      >
        <div className="mobile-menu-header">
          <h2 className="text-lg font-semibold">メニュー</h2>
          <button
            className="mobile-menu-close"
            onClick={onClose}
            aria-label="メニューを閉じる"
          >
            <XMarkIcon className="w-5 h-5" />
          </button>
        </div>
        
        <div className="mobile-menu-nav">
          {menuItems.map((item) => (
            <a
              key={item.id}
              href={item.href}
              className={`mobile-menu-item ${item.active ? 'active' : ''}`}
              onClick={onClose}
            >
              {item.label}
            </a>
          ))}
        </div>
      </nav>
    </>
  );
};

// ハンバーガーボタンコンポーネント
export const HamburgerButton: React.FC<{
  isOpen: boolean;
  onClick: () => void;
}> = ({ isOpen, onClick }) => {
  return (
    <button
      className={`hamburger-menu ${isOpen ? 'active' : ''}`}
      onClick={onClick}
      aria-label={isOpen ? 'メニューを閉じる' : 'メニューを開く'}
      aria-expanded={isOpen}
    >
      <div className="hamburger-lines">
        <span className="hamburger-line" />
        <span className="hamburger-line" />
        <span className="hamburger-line" />
      </div>
    </button>
  );
};
```

##### アクセシビリティ要件
- **ARIA属性**: `aria-label`, `aria-expanded`, `role="navigation"`
- **キーボード操作**: Escキーでメニューを閉じる
- **フォーカス管理**: メニュー開閉時の適切なフォーカス移動
- **スクリーンリーダー**: メニューの状態を音声で通知

##### UX設計指針
- **タッチターゲット**: 最小44px×44pxのタッチ領域確保
- **アニメーション**: 300ms以内のスムーズなトランジション
- **直感的操作**: オーバーレイタップ・Escキーでメニューを閉じる
- **視覚的フィードバック**: ホバー・アクティブ状態の明確な表示

---

## 7. アラート・メッセージ

### 7.1 アラートコンポーネント
```css
.alert {
  padding: var(--space-4);
  border-radius: 0.375rem;
  border: 1px solid;
  margin-bottom: var(--space-4);
}

.alert-success {
  background-color: var(--success-50);
  border-color: var(--success-200);
  color: var(--success-800);
}

.alert-error {
  background-color: var(--error-50);
  border-color: var(--error-200);
  color: var(--error-800);
}

.alert-warning {
  background-color: var(--warning-50);
  border-color: var(--warning-200);
  color: var(--warning-800);
}

.alert-info {
  background-color: var(--info-50);
  border-color: var(--info-200);
  color: var(--info-800);
}
```

### 7.2 トースト通知
```css
.toast {
  position: fixed;
  top: var(--space-4);
  right: var(--space-4);
  min-width: 300px;
  padding: var(--space-4);
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border-left: 4px solid;
  z-index: 1000;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
```

---

## 8. レスポンシブデザイン

### 8.1 ブレークポイント
```css
/* モバイルファースト */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
@media (min-width: 1536px) { /* 2xl */ }
```

### 8.2 レスポンシブ対応指針
- **モバイル**: 単一カラム、タッチフレンドリー（44px以上のタップ領域）
- **タブレット**: 2カラム、スワイプ操作対応
- **デスクトップ**: 3カラム、マウス操作最適化

---

## 9. アクセシビリティ

### 9.1 WCAG 2.1 AA準拠要件
- **コントラスト比**: 4.5:1以上（通常テキスト）、3:1以上（大きなテキスト）
- **キーボード操作**: 全機能がキーボードのみで操作可能
- **フォーカス表示**: 明確なフォーカスインジケーター
- **スクリーンリーダー**: 適切なARIAラベル・ロール

### 9.2 実装要件
```css
/* フォーカス表示 */
*:focus {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* スキップリンク */
.skip-link {
  position: absolute;
  top: -40px;
  left: 6px;
  background: var(--primary-500);
  color: white;
  padding: 8px;
  text-decoration: none;
  z-index: 1000;
}

.skip-link:focus {
  top: 6px;
}
```

---

## 10. アニメーション・トランジション

### 10.1 基本トランジション
```css
/* 標準的なトランジション */
.transition-base {
  transition: all 0.2s ease-in-out;
}

.transition-fast {
  transition: all 0.1s ease-in-out;
}

.transition-slow {
  transition: all 0.3s ease-in-out;
}
```

### 10.2 ローディング・スピナー
```css
.spinner {
  width: 2rem;
  height: 2rem;
  border: 2px solid var(--gray-200);
  border-top: 2px solid var(--primary-500);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```

---

## 11. アイコン・画像

### 11.1 アイコンシステム
- **アイコンライブラリ**: Heroicons（Tailwind CSS公式）
- **サイズ**: 16px, 20px, 24px, 32px
- **スタイル**: Outline（通常）、Solid（強調）

### 11.2 画像最適化
- **フォーマット**: WebP優先、PNG/JPEGフォールバック
- **レスポンシブ**: srcset属性による解像度対応
- **遅延読み込み**: loading="lazy"属性

---

## 12. パフォーマンス・最適化

### 12.1 CSS最適化
- **Critical CSS**: Above-the-fold CSSの優先読み込み
- **CSS分割**: ページ別CSS分割
- **未使用CSS除去**: PurgeCSS使用

### 12.2 フォント最適化
- **フォント表示**: font-display: swap
- **サブセット**: 日本語フォントサブセット化
- **プリロード**: 重要フォントのpreload

---

## 13. 実装ガイドライン

### 13.1 Tailwind CSS設定
```javascript
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          // ... 他の色定義
        }
      },
      fontFamily: {
        sans: ['Hiragino Kaku Gothic ProN', 'Hiragino Sans', 'Yu Gothic Medium', 'Meiryo', 'MS PGothic', 'sans-serif']
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography')
  ]
}
```

### 13.2 コンポーネント実装例
```typescript
// Button.tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'base' | 'lg';
  fullWidth?: boolean;
  disabled?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'base',
  fullWidth = false,
  disabled = false,
  children,
  onClick
}) => {
  const baseClasses = 'font-medium rounded-md transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2';
  
  const variantClasses = {
    primary: 'bg-primary-500 text-white hover:bg-primary-600 focus:ring-primary-500',
    secondary: 'bg-white text-primary-500 border border-primary-500 hover:bg-primary-50 focus:ring-primary-500'
  };
  
  const sizeClasses = {
    sm: 'px-4 py-2 text-sm',
    base: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg'
  };
  
  const classes = [
    baseClasses,
    variantClasses[variant],
    sizeClasses[size],
    fullWidth ? 'w-full' : '',
    disabled ? 'opacity-50 cursor-not-allowed' : ''
  ].join(' ');
  
  return (
    <button
      className={classes}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

---

## 14. 品質保証・テスト

### 14.1 ビジュアルリグレッションテスト
- **ツール**: Chromatic、Percy
- **対象**: 全コンポーネント、主要画面
- **頻度**: PR作成時、リリース前

### 14.2 アクセシビリティテスト
- **自動テスト**: axe-core、Lighthouse
- **手動テスト**: スクリーンリーダー、キーボード操作
- **基準**: WCAG 2.1 AA準拠

---

## 15. 運用・メンテナンス

### 15.1 デザインシステム管理
- **Storybook**: コンポーネントカタログ
- **ドキュメント**: 使用方法・実装例
- **バージョン管理**: セマンティックバージョニング

### 15.2 継続的改善
- **ユーザーフィードバック**: 定期的なユーザビリティテスト
- **パフォーマンス監視**: Core Web Vitals監視
- **アクセシビリティ監査**: 四半期ごとの監査

---

## 16. 付録

### 16.1 参考リソース
- [Tailwind CSS公式ドキュメント](https://tailwindcss.com/)
- [WCAG 2.1ガイドライン](https://www.w3.org/WAI/WCAG21/quickref/)
- [Material Design](https://material.io/design)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)

### 16.2 ツール・ライブラリ
- **CSS**: Tailwind CSS
- **アイコン**: Heroicons
- **フォーム**: React Hook Form
- **アニメーション**: Framer Motion
- **テスト**: Jest, Testing Library, axe-core

---

この共通仕様書に従って、一貫性のある高品質なUI/UXを実現し、ユーザビリティとアクセシビリティを両立したWebアプリケーションを構築します。
