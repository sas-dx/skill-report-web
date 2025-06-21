# コーディング規約（技術スタック非依存）

## エグゼクティブサマリー

この文書は技術スタックに依存しない汎用的なコーディング規約を定義します。可読性・保守性を重視した命名規則、SOLID原則の適用、セキュリティコーディング、パフォーマンス考慮事項、テスト可能な設計パターンを提供し、高品質で一貫性のあるコードベースの構築を支援します。プロジェクト固有の技術スタック詳細は01-project-specific-rules.mdを参照し、このファイルでは言語・フレームワークに依存しない普遍的な品質基準に焦点を当てています。

## 基本原則

### 1. 可読性とメンテナンス性
- **自己文書化コード**: コード自体が何をしているかを明確に表現する
- **一貫性**: プロジェクト全体で統一されたスタイルを維持
- **シンプルさ**: 複雑さを避け、理解しやすいコードを書く
- **DRY原則**: Don't Repeat Yourself - 重複を避ける

### 2. SOLID原則の適用
- **S**: Single Responsibility Principle（単一責任原則）
- **O**: Open/Closed Principle（開放閉鎖原則）
- **L**: Liskov Substitution Principle（リスコフの置換原則）
- **I**: Interface Segregation Principle（インターフェース分離原則）
- **D**: Dependency Inversion Principle（依存性逆転原則）

## 命名規則

### 1. 変数・関数名
- **意味のある名前**: 目的や内容が分かる名前を使用
- **動詞+名詞**: 関数名は動作を表す動詞から始める
- **ブール値**: `is`, `has`, `can`, `should`などの接頭辞を使用
- **定数**: 大文字とアンダースコアで表現（言語に依存）

```typescript
// 良い例
const userAge: number = 25;
const isAuthenticated: boolean = true;
const getUserProfile = (): Promise<UserProfile> => { /* ... */ };
const MAX_RETRY_COUNT: number = 3;

// 悪い例
const a = 25;
const flag = true;
const getData = () => { /* ... */ };
const max = 3;
```

### 2. クラス・コンポーネント名
- **PascalCase**: 各単語の最初を大文字
- **名詞**: クラス名は名詞で表現
- **具体的**: 抽象的すぎない具体的な名前

```typescript
// 良い例
class UserProfileManager { }
class SkillReportValidator { }

// 悪い例
class Manager { }
class Helper { }
```

### 3. ファイル・ディレクトリ名
- **kebab-case**: ハイフン区切り（推奨）
- **camelCase**: キャメルケース（言語・フレームワークに依存）
- **機能・目的を表現**: ファイルの内容が分かる名前

```
// 良い例
user-profile-service.js
skill-report-validator.js
components/
  skill-input-form/
  career-plan-chart/

// 悪い例
service.js
validator.js
comp/
```

## コメント・ドキュメント規約

### 1. コメントの原則
- **なぜ（Why）を説明**: 何をしているかではなく、なぜそうしているかを説明
- **複雑なロジック**: アルゴリズムやビジネスルールの説明
- **TODO/FIXME**: 将来の改善点や既知の問題を明記

```typescript
// 良い例
// ユーザーの権限レベルに応じてアクセス可能な機能を制限
// セキュリティ要件: 管理者のみがユーザー削除可能
if (user.role === 'admin') {
  // ...
}

// TODO: パフォーマンス改善 - キャッシュ機能の実装を検討
// FIXME: 特定条件下でメモリリークが発生する可能性

// 悪い例
// ユーザーロールをチェック
if (user.role === 'admin') {
  // ...
}
```

### 2. 関数・メソッドドキュメント
- **目的**: 関数の目的と責任を明記
- **パラメータ**: 各パラメータの型と説明
- **戻り値**: 戻り値の型と説明
- **例外**: 発生する可能性のある例外

```typescript
interface SkillData {
  category: string;
  level: number;
}

/**
 * ユーザーのスキル情報を検証し、不正な値をサニタイズする
 * 
 * @param skillData - 検証対象のスキルデータ
 * @param skillData.category - スキルカテゴリ
 * @param skillData.level - スキルレベル（1-4）
 * @returns 検証済みのスキルデータ
 * @throws ValidationError 必須項目が不足している場合
 */
function validateSkillData(skillData: SkillData): SkillData {
  // ...
}
```

## エラーハンドリング原則

### 1. 例外処理の基本方針
- **早期発見**: エラーは可能な限り早期に検出
- **適切なレベル**: エラーは適切なレベルで処理
- **ログ記録**: エラー情報は必ずログに記録
- **ユーザーフレンドリー**: ユーザーには分かりやすいメッセージを表示

### 2. エラーメッセージ
- **具体的**: 何が問題かを具体的に説明
- **解決策**: 可能であれば解決方法を提示
- **セキュリティ**: 機密情報を含まない

```typescript
// 良い例
throw new ValidationError(
  `スキルレベルは1から4の範囲で入力してください。入力値: ${level}`
);

// 悪い例
throw new Error('Invalid input');
```

### 3. エラーカテゴリ
- **ValidationError**: 入力値検証エラー
- **AuthenticationError**: 認証エラー
- **AuthorizationError**: 認可エラー
- **BusinessLogicError**: ビジネスロジックエラー
- **SystemError**: システムエラー

## ログ出力規約

### 1. ログレベル
- **ERROR**: システムエラー、例外
- **WARN**: 警告、非推奨機能の使用
- **INFO**: 重要な処理の開始・終了
- **DEBUG**: デバッグ情報（開発時のみ）

### 2. ログフォーマット
- **タイムスタンプ**: ISO 8601形式
- **ログレベル**: 明確に表示
- **コンテキスト**: ユーザーID、セッションID等
- **メッセージ**: 構造化された情報

```typescript
// 良い例
logger.info('User login successful', {
  userId: 'user123',
  sessionId: 'session456',
  timestamp: '2025-05-26T10:58:21.000Z',
  ipAddress: '192.168.1.1'
});

// 悪い例
console.log('User logged in');
```

## セキュリティコーディング原則

### 1. 入力値検証
- **すべての入力を検証**: ユーザー入力、API入力、ファイル入力
- **ホワイトリスト方式**: 許可する値を明示的に定義
- **サニタイゼーション**: 危険な文字列の無害化

### 2. 認証・認可
- **最小権限の原則**: 必要最小限の権限のみ付与
- **セッション管理**: 適切なセッションタイムアウト
- **トークン管理**: JWTの適切な検証と更新

### 3. データ保護
- **機密データの暗号化**: パスワード、個人情報の暗号化
- **ログ出力時の注意**: 機密情報をログに出力しない
- **HTTPS通信**: すべての通信でHTTPS使用

```typescript
// 良い例
const hashedPassword = await bcrypt.hash(password, 10);
logger.info('Password updated', { userId: user.id }); // パスワードはログに出力しない

// 悪い例
const password = req.body.password; // 平文保存
logger.info('Password updated', { userId: user.id, password: password });
```

## パフォーマンス考慮事項

### 1. 効率的なアルゴリズム
- **時間計算量**: O(n²)を避け、可能な限りO(n)やO(log n)を目指す
- **空間計算量**: メモリ使用量を最適化
- **キャッシュ活用**: 計算結果の再利用

### 2. データベースアクセス
- **N+1問題の回避**: 適切なJOINやバッチ処理
- **インデックス活用**: 検索性能の最適化
- **ページネーション**: 大量データの分割取得

### 3. フロントエンド最適化
- **遅延読み込み**: 必要な時にリソースを読み込み
- **バンドルサイズ**: 不要なライブラリの除去
- **レンダリング最適化**: 不要な再レンダリングの回避

## テスト可能なコード

### 1. 依存性注入
- **外部依存の分離**: データベース、API、ファイルシステム
- **モック可能**: テスト時に依存関係を置き換え可能
- **純粋関数**: 副作用のない関数の推奨

### 2. テストしやすい構造
- **単一責任**: 1つの関数は1つの責任
- **小さな関数**: テストしやすいサイズに分割
- **明確な入出力**: 予測可能な動作

```typescript
interface Skill {
  level: number;
}

// 良い例（テスト可能）
function calculateSkillScore(skills: Skill[], weights: number[]): number {
  return skills.reduce((total, skill, index) => {
    return total + (skill.level * weights[index]);
  }, 0);
}

// 悪い例（テスト困難）
function updateUserSkillAndSendEmail(userId: string, skillData: any): void {
  // データベース更新、メール送信、ログ出力が混在
  database.updateSkill(userId, skillData);
  emailService.sendNotification(userId);
  logger.info('Skill updated');
}
```

## コードレビューチェックリスト

### 1. 機能性
- [ ] 要件を満たしているか
- [ ] エッジケースが考慮されているか
- [ ] エラーハンドリングが適切か

### 2. 品質
- [ ] 命名規則に従っているか
- [ ] コメントが適切か
- [ ] 重複コードがないか
- [ ] SOLID原則に従っているか

### 3. セキュリティ
- [ ] 入力値検証が実装されているか
- [ ] 機密情報が適切に保護されているか
- [ ] 認証・認可が正しく実装されているか

### 4. パフォーマンス
- [ ] 効率的なアルゴリズムが使用されているか
- [ ] 不要な処理がないか
- [ ] リソース使用量が適切か

### 5. テスト
- [ ] テストが書かれているか
- [ ] テストカバレッジが十分か
- [ ] テストが意味のあるケースをカバーしているか
