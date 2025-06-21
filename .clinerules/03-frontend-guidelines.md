# フロントエンド設計ガイドライン（汎用的）

## エグゼクティブサマリー

この文書はフロントエンド設計における汎用的なガイドラインを定義します。コンポーネント設計原則、状態管理パターン、レスポンシブデザイン、アクセシビリティ要件、パフォーマンス最適化手法を提供し、モダンで保守性の高いフロントエンドアプリケーションの構築を支援します。技術スタック非依存の基本原則を中心に記載し、特定フレームワーク固有の実装詳細は01-project-specific-rules.mdを参照してください。

## 基本設計原則

### 1. コンポーネント設計原則
- **単一責任の原則**: 1つのコンポーネントは1つの責任を持つ
- **再利用性**: 汎用的で再利用可能なコンポーネントを作成
- **疎結合**: コンポーネント間の依存関係を最小限に
- **高凝集**: 関連する機能は同じコンポーネント内にまとめる

### 2. 状態管理パターン
- **状態の局所化**: 状態は可能な限りローカルに保持
- **単一方向データフロー**: データの流れを予測可能に
- **状態の最小化**: 必要最小限の状態のみを管理
- **派生状態の活用**: 計算可能な値は状態として保持しない

### 3. パフォーマンス最適化
- **遅延読み込み**: 必要な時にリソースを読み込み
- **メモ化**: 計算コストの高い処理の結果をキャッシュ
- **仮想化**: 大量のデータを効率的に表示
- **バンドル最適化**: 不要なコードの除去

## コンポーネント設計規約

### 1. コンポーネント分類
- **プレゼンテーションコンポーネント**: UIの表示のみを担当
- **コンテナコンポーネント**: ビジネスロジックと状態管理を担当
- **共通コンポーネント**: プロジェクト全体で再利用される基本コンポーネント
- **ページコンポーネント**: 特定のページやルートに対応するコンポーネント

### 2. コンポーネント命名規則
- **PascalCase**: コンポーネント名は大文字で開始
- **機能を表現**: コンポーネントの役割が分かる名前
- **接頭辞の活用**: 共通コンポーネントには統一された接頭辞

```typescript
// 良い例
const UserProfileCard = () => { /* ... */ };
const SkillInputForm = () => { /* ... */ };
const CommonButton = () => { /* ... */ };
const CommonModal = () => { /* ... */ };

// 悪い例
const Card = () => { /* ... */ };
const Form = () => { /* ... */ };
const Component1 = () => { /* ... */ };
```

### 3. プロパティ設計
- **型安全性**: プロパティの型を明確に定義
- **デフォルト値**: 適切なデフォルト値を設定
- **必須プロパティの最小化**: 必須プロパティは最小限に抑える
- **コールバック命名**: イベントハンドラーは`on`で開始

```typescript
// 良い例
interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  onClick?: (event: MouseEvent) => void;
  onFocus?: (event: FocusEvent) => void;
}

// 悪い例
interface ButtonProps {
  text: string;
  type: string;
  click: Function;
}
```

## 状態管理設計

### 1. 状態の分類
- **ローカル状態**: コンポーネント内でのみ使用される状態
- **共有状態**: 複数のコンポーネント間で共有される状態
- **グローバル状態**: アプリケーション全体で使用される状態
- **サーバー状態**: APIから取得されるデータの状態

### 2. 状態管理の原則
- **状態の正規化**: 重複を避け、単一の情報源を維持
- **状態の分離**: 関連のない状態は分離して管理
- **状態の派生**: 計算可能な値は状態として保持しない
- **状態の同期**: サーバー状態とクライアント状態の同期を適切に管理

```typescript
interface User {
  id: string;
  name: string;
  departmentId: string;
}

interface Department {
  id: string;
  name: string;
}

interface NormalizedState {
  users: {
    byId: Record<string, User>;
    allIds: string[];
  };
  departments: {
    byId: Record<string, Department>;
  };
}

// 良い例（正規化された状態）
const state: NormalizedState = {
  users: {
    byId: {
      '1': { id: '1', name: '山田太郎', departmentId: 'dept1' },
      '2': { id: '2', name: '佐藤花子', departmentId: 'dept2' }
    },
    allIds: ['1', '2']
  },
  departments: {
    byId: {
      'dept1': { id: 'dept1', name: '開発部' },
      'dept2': { id: 'dept2', name: '営業部' }
    }
  }
};

// 悪い例（非正規化された状態）
const badState = {
  users: [
    { id: '1', name: '山田太郎', department: { id: 'dept1', name: '開発部' } },
    { id: '2', name: '佐藤花子', department: { id: 'dept2', name: '営業部' } }
  ]
};
```

## API通信パターン

### 1. API通信の基本原則
- **非同期処理**: すべてのAPI通信は非同期で実行
- **エラーハンドリング**: 適切なエラー処理とユーザーへの通知
- **ローディング状態**: API通信中のローディング状態を管理
- **キャッシュ戦略**: 適切なキャッシュ戦略でパフォーマンスを向上

### 2. API通信パターン
- **データフェッチング**: コンポーネントマウント時のデータ取得
- **楽観的更新**: ユーザー操作に対する即座のUI更新
- **リアルタイム更新**: WebSocketやServer-Sent Eventsによるリアルタイム通信
- **バックグラウンド同期**: 定期的なデータ同期

```typescript
interface UserData {
  id: string;
  name: string;
  email: string;
}

interface UseUserDataReturn {
  data: UserData | null;
  loading: boolean;
  error: string | null;
}

// 良い例（エラーハンドリングとローディング状態を含む）
const useUserData = (userId: string): UseUserDataReturn => {
  const [data, setData] = useState<UserData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        setLoading(true);
        const response = await api.getUser(userId);
        setData(response.data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
        setData(null);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, [userId]);

  return { data, loading, error };
};

// 悪い例（エラーハンドリングなし）
const useUserDataBad = (userId: string) => {
  const [data, setData] = useState<UserData | null>(null);

  useEffect(() => {
    api.getUser(userId).then(response => {
      setData(response.data);
    });
  }, [userId]);

  return data;
};
```

## フォームバリデーション規約

### 1. バリデーション戦略
- **クライアントサイドバリデーション**: ユーザビリティ向上のための即座の検証
- **サーバーサイドバリデーション**: セキュリティのための必須検証
- **リアルタイムバリデーション**: 入力中の即座のフィードバック
- **送信時バリデーション**: フォーム送信前の最終検証

### 2. バリデーションルール
- **必須項目**: 明確な必須項目の表示
- **形式チェック**: メールアドレス、電話番号等の形式検証
- **文字数制限**: 最小・最大文字数の制限
- **カスタムルール**: ビジネスロジックに基づく独自の検証

```typescript
interface SkillFormData {
  skillName?: string;
  level: number;
  description?: string;
}

interface ValidationResult {
  isValid: boolean;
  errors: Record<string, string>;
}

// 良い例（包括的なバリデーション）
const validateSkillForm = (formData: SkillFormData): ValidationResult => {
  const errors: Record<string, string> = {};

  // 必須項目チェック
  if (!formData.skillName?.trim()) {
    errors.skillName = 'スキル名は必須です';
  }

  // 範囲チェック
  if (formData.level < 1 || formData.level > 4) {
    errors.level = 'スキルレベルは1から4の範囲で入力してください';
  }

  // 文字数制限
  if (formData.description?.length && formData.description.length > 500) {
    errors.description = '説明は500文字以内で入力してください';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};

// 悪い例（不十分なバリデーション）
const validateSkillFormBad = (formData: SkillFormData): boolean => {
  return formData.skillName ? true : false;
};
```

## レスポンシブデザイン原則

### 1. ブレークポイント設計
- **モバイルファースト**: 小さい画面から設計を開始
- **標準ブレークポイント**: 一般的なデバイスサイズに対応
- **コンテンツ駆動**: コンテンツに基づいたブレークポイントの設定
- **柔軟性**: 様々なデバイスサイズに対応

```css
/* 良い例（モバイルファーストのブレークポイント） */
.container {
  width: 100%;
  padding: 1rem;
}

@media (min-width: 768px) {
  .container {
    max-width: 750px;
    margin: 0 auto;
  }
}

@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    padding: 2rem;
  }
}
```

### 2. レイアウト設計
- **フレキシブルグリッド**: 相対的な単位を使用したグリッドシステム
- **フルードイメージ**: 画像の適切なスケーリング
- **タッチフレンドリー**: タッチデバイスでの操作性を考慮
- **読みやすさ**: 様々な画面サイズでの可読性を確保

## アクセシビリティ要件

### 1. WCAG 2.1 AA準拠
- **知覚可能**: すべてのユーザーが情報を知覚できる
- **操作可能**: すべてのユーザーがインターフェースを操作できる
- **理解可能**: 情報とUIの操作が理解できる
- **堅牢**: 様々な支援技術で確実に解釈できる

### 2. 実装要件
- **セマンティックHTML**: 適切なHTML要素の使用
- **キーボードナビゲーション**: キーボードのみでの操作が可能
- **スクリーンリーダー対応**: 適切なARIAラベルとロール
- **色彩コントラスト**: 十分なコントラスト比の確保

```html
<!-- 良い例（アクセシブルなフォーム） -->
<form>
  <label for="skill-name">
    スキル名 <span aria-label="必須">*</span>
  </label>
  <input
    id="skill-name"
    type="text"
    required
    aria-describedby="skill-name-error"
    aria-invalid="false"
  />
  <div id="skill-name-error" role="alert" aria-live="polite">
    <!-- エラーメッセージ -->
  </div>
</form>

<!-- 悪い例（アクセシビリティに配慮されていない） -->
<div>
  <div>スキル名*</div>
  <input type="text" />
  <div style="color: red;">エラー</div>
</div>
```

## パフォーマンス最適化

### 1. レンダリング最適化
- **仮想化**: 大量のリストアイテムの効率的な表示
- **メモ化**: 計算コストの高いコンポーネントのキャッシュ
- **コード分割**: 必要な時にコンポーネントを読み込み
- **プリロード**: 重要なリソースの事前読み込み

### 2. バンドル最適化
- **Tree Shaking**: 使用されていないコードの除去
- **動的インポート**: 必要な時にモジュールを読み込み
- **圧縮**: JavaScriptとCSSの圧縮
- **キャッシュ戦略**: 適切なキャッシュヘッダーの設定

```javascript
// 良い例（遅延読み込みとメモ化）
import { lazy, memo, useMemo } from 'react';

const LazySkillChart = lazy(() => import('./SkillChart'));

const SkillList = memo(({ skills, filters }) => {
  const filteredSkills = useMemo(() => {
    return skills.filter(skill => 
      filters.category ? skill.category === filters.category : true
    );
  }, [skills, filters]);

  return (
    <div>
      {filteredSkills.map(skill => (
        <SkillItem key={skill.id} skill={skill} />
      ))}
    </div>
  );
});

// 悪い例（最適化されていない）
const SkillList = ({ skills, filters }) => {
  const filteredSkills = skills.filter(skill => 
    filters.category ? skill.category === filters.category : true
  );

  return (
    <div>
      {filteredSkills.map(skill => (
        <SkillItem key={skill.id} skill={skill} />
      ))}
    </div>
  );
};
```

## テスト戦略

### 1. テストの種類
- **ユニットテスト**: 個別のコンポーネントや関数のテスト
- **統合テスト**: コンポーネント間の連携テスト
- **E2Eテスト**: ユーザーシナリオに基づくテスト
- **ビジュアルリグレッションテスト**: UIの視覚的な変更の検出

### 2. テスト実装原則
- **テスト可能な設計**: テストしやすいコンポーネント設計
- **モックの活用**: 外部依存関係のモック化
- **ユーザー中心**: ユーザーの行動に基づいたテスト
- **継続的テスト**: CI/CDパイプラインでの自動テスト実行

```javascript
// 良い例（包括的なコンポーネントテスト）
describe('SkillInputForm', () => {
  it('should render all form fields', () => {
    render(<SkillInputForm />);
    
    expect(screen.getByLabelText('スキル名')).toBeInTheDocument();
    expect(screen.getByLabelText('スキルレベル')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: '保存' })).toBeInTheDocument();
  });

  it('should show validation error for empty skill name', async () => {
    render(<SkillInputForm />);
    
    const submitButton = screen.getByRole('button', { name: '保存' });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('スキル名は必須です')).toBeInTheDocument();
    });
  });

  it('should call onSubmit with form data when valid', async () => {
    const mockOnSubmit = jest.fn();
    render(<SkillInputForm onSubmit={mockOnSubmit} />);
    
    fireEvent.change(screen.getByLabelText('スキル名'), {
      target: { value: 'JavaScript' }
    });
    fireEvent.change(screen.getByLabelText('スキルレベル'), {
      target: { value: '3' }
    });
    fireEvent.click(screen.getByRole('button', { name: '保存' }));
    
    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        skillName: 'JavaScript',
        level: 3
      });
    });
  });
});
```

## セキュリティ考慮事項

### 1. XSS対策
- **入力値のサニタイゼーション**: ユーザー入力の適切な処理
- **出力時のエスケープ**: HTMLへの出力時の適切なエスケープ
- **CSP（Content Security Policy）**: 適切なCSPヘッダーの設定
- **信頼できないコンテンツの分離**: 外部コンテンツの安全な表示

### 2. 認証・認可
- **トークンの安全な保存**: 認証トークンの適切な管理
- **セッション管理**: セッションの適切な管理と無効化
- **権限チェック**: UI レベルでの適切な権限制御
- **機密情報の保護**: 機密情報のクライアントサイドでの適切な取り扱い

```javascript
// 良い例（安全な認証状態管理）
const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = secureStorage.getToken();
    if (token && !isTokenExpired(token)) {
      validateToken(token)
        .then(userData => setUser(userData))
        .catch(() => secureStorage.removeToken())
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (credentials) => {
    const { token, user } = await authAPI.login(credentials);
    secureStorage.setToken(token);
    setUser(user);
  };

  const logout = () => {
    secureStorage.removeToken();
    setUser(null);
  };

  return { user, loading, login, logout };
};

// 悪い例（安全でない認証管理）
const useAuth = () => {
  const [user, setUser] = useState(
    JSON.parse(localStorage.getItem('user'))
  );

  const login = (credentials) => {
    const user = authAPI.login(credentials);
    localStorage.setItem('user', JSON.stringify(user));
    setUser(user);
  };

  return { user, login };
};
