# API仕様書：API-032 キャリア目標更新API

## 1. 基本情報

- **API ID**: API-032
- **API名称**: キャリア目標更新API
- **概要**: ユーザーのキャリア目標情報を更新する
- **エンドポイント**: `/api/career-goals/{user_id}`
- **HTTPメソッド**: PUT
- **リクエスト形式**: JSON
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-CAREER](画面設計書_SCR-CAREER.md)
- **作成日**: 2025/05/28
- **作成者**: API設計担当
- **改訂履歴**: 2025/05/28 初版作成

---

## 2. リクエスト仕様

### 2.1 リクエストヘッダ

| ヘッダ名 | 必須 | 説明 | 備考 |
|---------|------|------|------|
| Authorization | ○ | 認証トークン | Bearer {JWT} 形式 |
| Content-Type | ○ | リクエスト形式 | application/json |
| Accept | - | レスポンス形式 | application/json |

### 2.2 パスパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| user_id | string | ○ | ユーザーID | 自身のIDまたは部下のIDを指定可能 |

### 2.3 リクエストボディ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| year | number | ○ | 年度 | 例: 2025 |
| career_goals | array | ○ | キャリア目標情報の配列 | |
| operation_type | string | ○ | 操作タイプ | "add", "update", "delete" |

#### career_goals 配列要素

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| goal_id | string | △ | 目標ID | 更新・削除時は必須<br>新規追加時は不要（自動採番） |
| goal_type | string | △ | 目標タイプ | "short_term", "mid_term", "long_term"<br>新規追加・更新時は必須 |
| title | string | △ | 目標タイトル | 新規追加・更新時は必須<br>最大100文字 |
| description | string | - | 目標詳細 | 最大1000文字 |
| target_date | string | △ | 目標達成予定日 | ISO 8601形式（YYYY-MM-DD）<br>新規追加・更新時は必須 |
| status | string | △ | 目標ステータス | "not_started", "in_progress", "completed", "postponed", "cancelled"<br>新規追加・更新時は必須 |
| priority | number | △ | 優先度 | 1-5（5が最高）<br>新規追加・更新時は必須 |
| related_skills | array | - | 関連スキル | |
| action_plans | array | - | 行動計画 | |
| feedback | array | - | フィードバック | |

#### related_skills 配列要素

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| skill_id | string | ○ | スキルID | |
| target_level | number | ○ | 目標レベル | 1-5（5が最高） |

#### action_plans 配列要素

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| action_id | string | △ | 行動計画ID | 更新・削除時は必須<br>新規追加時は不要（自動採番） |
| title | string | △ | タイトル | 新規追加・更新時は必須<br>最大100文字 |
| description | string | - | 詳細 | 最大500文字 |
| due_date | string | △ | 期限 | ISO 8601形式（YYYY-MM-DD）<br>新規追加・更新時は必須 |
| status | string | △ | ステータス | "not_started", "in_progress", "completed"<br>新規追加・更新時は必須 |
| completed_date | string | - | 完了日 | ISO 8601形式（YYYY-MM-DD）<br>status="completed"の場合のみ有効 |

#### feedback 配列要素

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| feedback_id | string | △ | フィードバックID | 更新・削除時は必須<br>新規追加時は不要（自動採番） |
| comment | string | △ | コメント内容 | 新規追加・更新時は必須<br>最大500文字 |

### 2.4 リクエスト例（目標追加）

```json
{
  "year": 2025,
  "operation_type": "add",
  "career_goals": [
    {
      "goal_type": "short_term",
      "title": "クラウドアーキテクチャの習得",
      "description": "AWSのソリューションアーキテクト資格を取得し、クラウドアーキテクチャの設計スキルを向上させる",
      "target_date": "2025-12-31",
      "status": "not_started",
      "priority": 4,
      "related_skills": [
        {
          "skill_id": "S040",
          "target_level": 4
        },
        {
          "skill_id": "S041",
          "target_level": 3
        }
      ],
      "action_plans": [
        {
          "title": "AWS公式ドキュメントの学習",
          "description": "AWS公式ドキュメントを読み、基本的な概念を理解する",
          "due_date": "2025-06-30",
          "status": "not_started"
        },
        {
          "title": "ハンズオンラボの実施",
          "description": "AWS提供のハンズオンラボを実施し、実践的なスキルを身につける",
          "due_date": "2025-09-30",
          "status": "not_started"
        }
      ]
    }
  ]
}
```

### 2.5 リクエスト例（目標更新）

```json
{
  "year": 2025,
  "operation_type": "update",
  "career_goals": [
    {
      "goal_id": "G001",
      "goal_type": "short_term",
      "title": "Reactの実践的スキル習得",
      "description": "実務でReactを使用したプロジェクトに参加し、実践的なスキルを身につける",
      "target_date": "2025-12-31",
      "status": "in_progress",
      "priority": 5,
      "related_skills": [
        {
          "skill_id": "S007",
          "target_level": 4
        },
        {
          "skill_id": "S008",
          "target_level": 3
        }
      ],
      "action_plans": [
        {
          "action_id": "A001",
          "title": "Reactの公式チュートリアルを完了する",
          "description": "Reactの公式ドキュメントに沿ってチュートリアルを実施",
          "due_date": "2025-06-30",
          "status": "completed",
          "completed_date": "2025-06-15"
        },
        {
          "action_id": "A002",
          "title": "社内のReactプロジェクトに参加する",
          "description": "プロジェクトマネージャーに相談し、Reactを使用するプロジェクトにアサインしてもらう",
          "due_date": "2025-08-31",
          "status": "in_progress"
        }
      ],
      "feedback": [
        {
          "comment": "進捗が順調で良いですね。次はTypeScriptとの組み合わせも検討してみてはどうでしょうか。"
        }
      ]
    }
  ]
}
```

### 2.6 リクエスト例（目標削除）

```json
{
  "year": 2025,
  "operation_type": "delete",
  "career_goals": [
    {
      "goal_id": "G002"
    }
  ]
}
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | ユーザーID | |
| year | number | 年度 | |
| updated_goals | array | 更新されたキャリア目標情報 | |
| operation_type | string | 実行された操作タイプ | "add", "update", "delete" |
| operation_result | string | 操作結果 | "success" |
| last_updated | string | 最終更新日時 | ISO 8601形式 |
| last_updated_by | string | 最終更新者 | |

#### updated_goals 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| goal_id | string | 目標ID | |
| goal_type | string | 目標タイプ | "short_term", "mid_term", "long_term" |
| title | string | 目標タイトル | |
| status | string | 目標ステータス | "not_started", "in_progress", "completed", "postponed", "cancelled" |
| updated_at | string | 更新日時 | ISO 8601形式 |

### 3.2 正常時レスポンス例（目標追加）

```json
{
  "user_id": "U12345",
  "year": 2025,
  "updated_goals": [
    {
      "goal_id": "G004",
      "goal_type": "short_term",
      "title": "クラウドアーキテクチャの習得",
      "status": "not_started",
      "updated_at": "2025-05-28T14:30:00+09:00"
    }
  ],
  "operation_type": "add",
  "operation_result": "success",
  "last_updated": "2025-05-28T14:30:00+09:00",
  "last_updated_by": "U12345"
}
```

### 3.3 正常時レスポンス例（目標更新）

```json
{
  "user_id": "U12345",
  "year": 2025,
  "updated_goals": [
    {
      "goal_id": "G001",
      "goal_type": "short_term",
      "title": "Reactの実践的スキル習得",
      "status": "in_progress",
      "updated_at": "2025-05-28T14:35:00+09:00"
    }
  ],
  "operation_type": "update",
  "operation_result": "success",
  "last_updated": "2025-05-28T14:35:00+09:00",
  "last_updated_by": "U12345"
}
```

### 3.4 正常時レスポンス例（目標削除）

```json
{
  "user_id": "U12345",
  "year": 2025,
  "updated_goals": [
    {
      "goal_id": "G002",
      "goal_type": "mid_term",
      "title": "フロントエンドアーキテクト資格取得",
      "status": "cancelled",
      "updated_at": "2025-05-28T14:40:00+09:00"
    }
  ],
  "operation_type": "delete",
  "operation_result": "success",
  "last_updated": "2025-05-28T14:40:00+09:00",
  "last_updated_by": "U12345"
}
```

### 3.5 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 400 Bad Request | INVALID_YEAR | 年度が不正です | 存在しない年度指定 |
| 400 Bad Request | INVALID_OPERATION | 操作タイプが不正です | 存在しない操作タイプ |
| 400 Bad Request | INVALID_GOAL_TYPE | 目標タイプが不正です | 存在しない目標タイプ |
| 400 Bad Request | INVALID_STATUS | ステータスが不正です | 存在しないステータス |
| 400 Bad Request | INVALID_PRIORITY | 優先度が不正です | 範囲外の優先度 |
| 400 Bad Request | INVALID_SKILL_ID | スキルIDが不正です | 存在しないスキルID |
| 400 Bad Request | GOAL_NOT_FOUND | 目標が見つかりません | 更新・削除対象の目標が存在しない |
| 400 Bad Request | PAST_YEAR_MODIFICATION | 過去の年度は変更できません | 過去の年度のデータ変更試行 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他ユーザーの情報更新権限なし |
| 404 Not Found | USER_NOT_FOUND | ユーザーが見つかりません | 指定されたユーザーIDが存在しない |
| 409 Conflict | DUPLICATE_GOAL | 重複する目標があります | 同一タイトルの目標が既に存在 |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.6 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "パラメータが不正です",
    "details": "目標タイトルは必須項目です。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - ユーザーIDの権限チェック（自身または部下のIDかどうか）
2. リクエストパラメータの検証
   - ユーザーIDの存在チェック
   - 年度の妥当性チェック
   - 操作タイプの検証
   - 必須パラメータの検証
3. 操作タイプに応じた処理
   - add: 新規キャリア目標の追加
   - update: 既存キャリア目標の更新
   - delete: キャリア目標の削除（論理削除）
4. データベース更新
   - トランザクション内で関連テーブルを一括更新
5. レスポンスの生成
   - 更新結果を整形
6. レスポンス返却

### 4.2 権限チェック

- 自身のキャリア目標は常に更新可能
- 他ユーザーのキャリア目標更新には以下のいずれかの条件を満たす必要がある
  - 対象ユーザーの直属の上長である
  - キャリア目標更新権限（PERM_UPDATE_CAREER_GOALS）を持っている
  - 管理者権限（ROLE_ADMIN）を持っている

### 4.3 年度の扱い

- 年度は4月1日から翌年3月31日までの期間
- 過去の年度のキャリア目標は更新不可（読み取り専用）
- 現在および未来の年度のキャリア目標のみ更新可能

### 4.4 操作タイプ別処理

#### add（追加）

1. 新規キャリア目標IDの採番
2. 関連スキル情報の検証
   - スキルIDの存在チェック
   - 目標レベルの範囲チェック（1-5）
3. 行動計画の処理
   - 行動計画IDの採番
   - 期限の妥当性チェック
4. キャリア目標情報の登録
   - career_goals テーブルに登録
   - career_goal_skills テーブルに関連スキル情報を登録
   - career_goal_actions テーブルに行動計画を登録

#### update（更新）

1. 更新対象キャリア目標の存在チェック
2. 関連スキル情報の処理
   - 既存の関連スキル情報を削除
   - 新しい関連スキル情報を登録
3. 行動計画の処理
   - 既存の行動計画を更新
   - 新規行動計画を追加
   - 削除された行動計画を削除
4. フィードバックの処理
   - 新規フィードバックを追加
5. キャリア目標情報の更新
   - career_goals テーブルを更新

#### delete（削除）

1. 削除対象キャリア目標の存在チェック
2. 論理削除処理
   - career_goals テーブルの is_deleted フラグを true に設定
   - 物理削除は行わない（履歴保持のため）

### 4.5 データ整合性

- トランザクション処理により、関連テーブル間の整合性を確保
- 楽観的ロック制御を実装し、同時更新による不整合を防止
- 更新履歴を career_goals_history テーブルに保存

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-021](API仕様書_API-021.md) | スキル情報取得API | ユーザースキル情報取得 |
| [API-023](API仕様書_API-023.md) | スキルマスタ取得API | スキルマスタ情報取得 |
| [API-031](API仕様書_API-031.md) | キャリア目標取得API | キャリア目標情報取得 |
| [API-033](API仕様書_API-033.md) | 目標進捗取得API | 目標進捗情報取得 |
| [API-034](API仕様書_API-034.md) | 目標進捗更新API | 目標進捗情報更新 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| career_goals | キャリア目標情報 | 作成・更新・削除（CUD） |
| career_goal_skills | キャリア目標関連スキル | 作成・更新・削除（CUD） |
| career_goal_actions | キャリア目標行動計画 | 作成・更新・削除（CUD） |
| career_goal_feedback | キャリア目標フィードバック | 作成（C） |
| career_goals_history | キャリア目標更新履歴 | 作成（C） |
| skill_masters | スキルマスタ | 参照（R） |

### 5.3 注意事項・補足

- キャリア目標の削除は論理削除とし、履歴として保持
- フィードバックは追加のみ可能で、更新・削除は不可
- 関連スキルの更新は全置換方式（既存の関連スキルを削除し、新しい関連スキルを登録）
- 行動計画は個別に追加・更新・削除が可能
- 目標タイプ（短期・中期・長期）によって、目標達成予定日の妥当性をチェック
  - 短期：1年以内
  - 中期：1-3年
  - 長期：3-5年
- 上長からのフィードバックは通知機能と連携

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import { useForm, Controller, useFieldArray } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { 
  Button, 
  TextField, 
  Select, 
  MenuItem, 
  FormControl, 
  InputLabel, 
  FormHelperText,
  Grid,
  Typography,
  Paper,
  Divider,
  IconButton,
  Box,
  Snackbar,
  Alert
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';

// バリデーションスキーマ
const schema = yup.object().shape({
  year: yup.number().required('年度は必須です').min(2020).max(2030),
  operation_type: yup.string().required('操作タイプは必須です').oneOf(['add', 'update', 'delete']),
  career_goals: yup.array().of(
    yup.object().shape({
      goal_id: yup.string().when('$operation_type', {
        is: (val: string) => val === 'update' || val === 'delete',
        then: yup.string().required('目標IDは必須です'),
        otherwise: yup.string().nullable()
      }),
      goal_type: yup.string().when('$operation_type', {
        is: (val: string) => val === 'add' || val === 'update',
        then: yup.string().required('目標タイプは必須です').oneOf(['short_term', 'mid_term', 'long_term']),
        otherwise: yup.string().nullable()
      }),
      title: yup.string().when('$operation_type', {
        is: (val: string) => val === 'add' || val === 'update',
        then: yup.string().required('タイトルは必須です').max(100, 'タイトルは100文字以内で入力してください'),
        otherwise: yup.string().nullable()
      }),
      description: yup.string().max(1000, '詳細は1000文字以内で入力してください'),
      target_date: yup.date().when('$operation_type', {
        is: (val: string) => val === 'add' || val === 'update',
        then: yup.date().required('目標達成予定日は必須です'),
        otherwise: yup.date().nullable()
      }),
      status: yup.string().when('$operation_type', {
        is: (val: string) => val === 'add' || val === 'update',
        then: yup.string().required('ステータスは必須です').oneOf(['not_started', 'in_progress', 'completed', 'postponed', 'cancelled']),
        otherwise: yup.string().nullable()
      }),
      priority: yup.number().when('$operation_type', {
        is: (val: string) => val === 'add' || val === 'update',
        then: yup.number().required('優先度は必須です').min(1).max(5),
        otherwise: yup.number().nullable()
      }),
      related_skills: yup.array().of(
        yup.object().shape({
          skill_id: yup.string().required('スキルIDは必須です'),
          target_level: yup.number().required('目標レベルは必須です').min(1).max(5)
        })
      ),
      action_plans: yup.array().of(
        yup.object().shape({
          action_id: yup.string(),
          title: yup.string().required('タイトルは必須です').max(100, 'タイトルは100文字以内で入力してください'),
          description: yup.string().max(500, '詳細は500文字以内で入力してください'),
          due_date: yup.date().required('期限は必須です'),
          status: yup.string().required('ステータスは必須です').oneOf(['not_started', 'in_progress', 'completed']),
          completed_date: yup.date().when('status', {
            is: 'completed',
            then: yup.date().required('完了日は必須です'),
            otherwise: yup.date().nullable()
          })
        })
      ),
      feedback: yup.array().of(
        yup.object().shape({
          feedback_id: yup.string(),
          comment: yup.string().required('コメントは必須です').max(500, 'コメントは500文字以内で入力してください')
        })
      )
    })
  )
});

// フォームの型定義
interface CareerGoalFormData {
  year: number;
  operation_type: 'add' | 'update' | 'delete';
  career_goals: Array<{
    goal_id?: string;
    goal_type?: 'short_term' | 'mid_term' | 'long_term';
    title?: string;
    description?: string;
    target_date?: Date;
    status?: 'not_started' | 'in_progress' | 'completed' | 'postponed' | 'cancelled';
    priority?: number;
    related_skills?: Array<{
      skill_id: string;
      target_level: number;
    }>;
    action_plans?: Array<{
      action_id?: string;
      title: string;
      description?: string;
      due_date: Date;
      status: 'not_started' | 'in_progress' | 'completed';
      completed_date?: Date | null;
    }>;
    feedback?: Array<{
      feedback_id?: string;
      comment: string;
    }>;
  }>;
}

// スキルマスタの型定義
interface SkillMaster {
  skill_id: string;
  name: string;
  category: string;
}

const CareerGoalUpdateForm: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<boolean>(false);
  const [skillMasters, setSkillMasters] = useState<SkillMaster[]>([]);
  
  // React Hook Formの設定
  const { control, handleSubmit, watch, setValue, formState: { errors } } = useForm<CareerGoalFormData>({
    resolver: yupResolver(schema),
    defaultValues: {
      year: new Date().getFullYear(),
      operation_type: 'add',
      career_goals: [
        {
          goal_type: 'short_term',
          status: 'not_started',
          priority: 3,
          related_skills: [],
          action_plans: [],
          feedback: []
        }
      ]
    },
    context: {
      operation_type: watch('operation_type')
    }
  });
  
  // フィールド配列の設定
  const { fields: goalFields, append: appendGoal, remove: removeGoal } = useFieldArray({
    control,
    name: 'career_goals'
  });
  
  // スキルマスタの取得
  React.useEffect(() => {
    const fetchSkillMasters = async () => {
      try {
        const response = await axios.get<{ skills: SkillMaster[] }>('/api/skill-masters', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        setSkillMasters(response.data.skills);
      } catch (err) {
