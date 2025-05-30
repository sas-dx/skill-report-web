# API定義書：API-034 目標進捗更新API

## 1. 基本情報

- **API ID**: API-034
- **API名称**: 目標進捗更新API
- **概要**: ユーザーの目標進捗情報を更新する
- **エンドポイント**: `/api/goal-progress/{user_id}`
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
| goal_id | string | ○ | 目標ID | |
| update_type | string | ○ | 更新タイプ | "status", "action_plan", "milestone", "skill_level", "feedback" |
| update_data | object | ○ | 更新データ | 更新タイプに応じたデータ構造 |
| comment | string | - | 更新コメント | 最大500文字 |

#### update_data オブジェクト（更新タイプ別）

##### status 更新の場合

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| status | string | ○ | 新しい目標ステータス | "not_started", "in_progress", "completed", "postponed", "cancelled" |
| completion_date | string | △ | 完了日 | ISO 8601形式（YYYY-MM-DD）<br>status="completed"の場合のみ必須 |
| reason | string | △ | 理由 | status="postponed"または"cancelled"の場合のみ必須<br>最大500文字 |

##### action_plan 更新の場合

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| action_id | string | ○ | 行動計画ID | |
| status | string | ○ | 新しい行動計画ステータス | "not_started", "in_progress", "completed" |
| completion_date | string | △ | 完了日 | ISO 8601形式（YYYY-MM-DD）<br>status="completed"の場合のみ必須 |
| progress_note | string | - | 進捗メモ | 最大500文字 |

##### milestone 更新の場合

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| milestone_id | string | ○ | マイルストーンID | |
| status | string | ○ | 新しいマイルストーンステータス | "not_started", "in_progress", "completed" |
| completion_date | string | △ | 完了日 | ISO 8601形式（YYYY-MM-DD）<br>status="completed"の場合のみ必須 |
| achievement_note | string | - | 達成メモ | 最大500文字 |

##### skill_level 更新の場合

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| skill_id | string | ○ | スキルID | |
| current_level | number | ○ | 現在のレベル | 1-5（5が最高） |
| evidence | string | - | 根拠・エビデンス | 最大500文字 |

##### feedback 更新の場合

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| feedback_text | string | ○ | フィードバック内容 | 最大1000文字 |
| feedback_type | string | - | フィードバックタイプ | "praise", "suggestion", "concern"<br>デフォルト: "suggestion" |

### 2.4 リクエスト例（目標ステータス更新）

```json
{
  "goal_id": "G001",
  "update_type": "status",
  "update_data": {
    "status": "in_progress"
  },
  "comment": "プロジェクトへの参加が決まり、実践的なスキル習得を開始しました。"
}
```

### 2.5 リクエスト例（行動計画更新）

```json
{
  "goal_id": "G001",
  "update_type": "action_plan",
  "update_data": {
    "action_id": "A001",
    "status": "completed",
    "completion_date": "2025-06-15",
    "progress_note": "Reactの公式チュートリアルを全て完了し、基本的な概念を理解しました。"
  },
  "comment": "予定より早く完了することができました。"
}
```

### 2.6 リクエスト例（スキルレベル更新）

```json
{
  "goal_id": "G001",
  "update_type": "skill_level",
  "update_data": {
    "skill_id": "S007",
    "current_level": 3,
    "evidence": "社内プロジェクトでReactコンポーネントを5つ実装し、コードレビューで高評価を得ました。"
  },
  "comment": "実践的な経験を積み、レベルが向上しました。"
}
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | ユーザーID | |
| goal_id | string | 目標ID | |
| update_type | string | 更新タイプ | "status", "action_plan", "milestone", "skill_level", "feedback" |
| update_result | string | 更新結果 | "success" |
| updated_data | object | 更新後のデータ | 更新タイプに応じたデータ構造 |
| progress_rate | number | 更新後の進捗率 | 0-100（%） |
| update_id | string | 更新ID | |
| updated_at | string | 更新日時 | ISO 8601形式 |
| updated_by | string | 更新者 | |

#### updated_data オブジェクト（更新タイプ別）

##### status 更新の場合

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| status | string | 更新後の目標ステータス | "not_started", "in_progress", "completed", "postponed", "cancelled" |
| completion_date | string | 完了日 | ISO 8601形式（YYYY-MM-DD）、完了時のみ |
| reason | string | 理由 | 延期または中止時のみ |

##### action_plan 更新の場合

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| action_id | string | 行動計画ID | |
| title | string | 行動計画タイトル | |
| status | string | 更新後の行動計画ステータス | "not_started", "in_progress", "completed" |
| completion_date | string | 完了日 | ISO 8601形式（YYYY-MM-DD）、完了時のみ |
| action_plan_progress | object | 行動計画の進捗状況 | |

##### milestone 更新の場合

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| milestone_id | string | マイルストーンID | |
| title | string | マイルストーンタイトル | |
| status | string | 更新後のマイルストーンステータス | "not_started", "in_progress", "completed" |
| completion_date | string | 完了日 | ISO 8601形式（YYYY-MM-DD）、完了時のみ |
| milestone_progress | object | マイルストーンの進捗状況 | |

##### skill_level 更新の場合

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| skill_id | string | スキルID | |
| name | string | スキル名 | |
| category | string | スキルカテゴリ | |
| current_level | number | 更新後の現在のレベル | 1-5（5が最高） |
| target_level | number | 目標レベル | 1-5（5が最高） |
| progress_rate | number | 進捗率 | 0-100（%） |

##### feedback 更新の場合

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| feedback_id | string | フィードバックID | |
| feedback_text | string | フィードバック内容 | |
| feedback_type | string | フィードバックタイプ | "praise", "suggestion", "concern" |
| commenter_id | string | コメント者ID | |
| commenter_name | string | コメント者名 | |

### 3.2 正常時レスポンス例（目標ステータス更新）

```json
{
  "user_id": "U12345",
  "goal_id": "G001",
  "update_type": "status",
  "update_result": "success",
  "updated_data": {
    "status": "in_progress",
    "completion_date": null,
    "reason": null
  },
  "progress_rate": 30,
  "update_id": "UP001",
  "updated_at": "2025-05-28T15:30:00+09:00",
  "updated_by": "U12345"
}
```

### 3.3 正常時レスポンス例（行動計画更新）

```json
{
  "user_id": "U12345",
  "goal_id": "G001",
  "update_type": "action_plan",
  "update_result": "success",
  "updated_data": {
    "action_id": "A001",
    "title": "Reactの公式チュートリアルを完了する",
    "status": "completed",
    "completion_date": "2025-06-15",
    "action_plan_progress": {
      "total": 3,
      "completed": 1,
      "in_progress": 1,
      "not_started": 1,
      "completion_rate": 33.3
    }
  },
  "progress_rate": 45,
  "update_id": "UP002",
  "updated_at": "2025-06-15T15:45:00+09:00",
  "updated_by": "U12345"
}
```

### 3.4 正常時レスポンス例（スキルレベル更新）

```json
{
  "user_id": "U12345",
  "goal_id": "G001",
  "update_type": "skill_level",
  "update_result": "success",
  "updated_data": {
    "skill_id": "S007",
    "name": "React",
    "category": "technical",
    "current_level": 3,
    "target_level": 4,
    "progress_rate": 75
  },
  "progress_rate": 55,
  "update_id": "UP003",
  "updated_at": "2025-07-15T10:30:00+09:00",
  "updated_by": "U12345"
}
```

### 3.5 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 400 Bad Request | INVALID_GOAL_ID | 目標IDが不正です | 存在しない目標ID |
| 400 Bad Request | INVALID_UPDATE_TYPE | 更新タイプが不正です | 存在しない更新タイプ |
| 400 Bad Request | INVALID_STATUS | ステータスが不正です | 存在しないステータス |
| 400 Bad Request | INVALID_ACTION_ID | 行動計画IDが不正です | 存在しない行動計画ID |
| 400 Bad Request | INVALID_MILESTONE_ID | マイルストーンIDが不正です | 存在しないマイルストーンID |
| 400 Bad Request | INVALID_SKILL_ID | スキルIDが不正です | 存在しないスキルID |
| 400 Bad Request | INVALID_SKILL_LEVEL | スキルレベルが不正です | 範囲外のスキルレベル |
| 400 Bad Request | MISSING_REQUIRED_FIELD | 必須フィールドがありません | 必須フィールドの欠落 |
| 400 Bad Request | PAST_GOAL_MODIFICATION | 過去の目標は変更できません | 完了済み目標の変更試行 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他ユーザーの情報更新権限なし |
| 404 Not Found | USER_NOT_FOUND | ユーザーが見つかりません | 指定されたユーザーIDが存在しない |
| 404 Not Found | GOAL_NOT_FOUND | 目標が見つかりません | 指定された目標IDが存在しない |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.6 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_STATUS",
    "message": "ステータスが不正です",
    "details": "指定されたステータス 'finished' は存在しません。有効なステータス: not_started, in_progress, completed, postponed, cancelled"
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
   - 目標IDの存在チェック
   - 更新タイプの検証
   - 更新データの検証
3. 更新タイプに応じた処理
   - status: 目標ステータスの更新
   - action_plan: 行動計画の更新
   - milestone: マイルストーンの更新
   - skill_level: スキルレベルの更新
   - feedback: フィードバックの追加
4. 進捗率の再計算
   - 更新内容に基づいて目標の進捗率を再計算
5. 更新履歴の記録
   - 更新内容を履歴として記録
6. レスポンスの生成
   - 更新結果を整形
7. レスポンス返却

### 4.2 権限チェック

- 自身の目標進捗は常に更新可能
- 他ユーザーの目標進捗更新には以下のいずれかの条件を満たす必要がある
  - 対象ユーザーの直属の上長である
  - 目標進捗更新権限（PERM_UPDATE_GOAL_PROGRESS）を持っている
  - 管理者権限（ROLE_ADMIN）を持っている
- フィードバック追加は、対象ユーザーの上長または同じチームのメンバーであれば可能

### 4.3 更新タイプ別処理

#### status（目標ステータス更新）

1. 目標ステータスの妥当性チェック
2. 完了日の検証（ステータスが"completed"の場合）
3. 理由の検証（ステータスが"postponed"または"cancelled"の場合）
4. 目標ステータスの更新
5. 関連する通知の生成（ステータス変更通知）

#### action_plan（行動計画更新）

1. 行動計画IDの存在チェック
2. 行動計画ステータスの妥当性チェック
3. 完了日の検証（ステータスが"completed"の場合）
4. 行動計画の更新
5. 行動計画の進捗状況の再計算
6. 関連する通知の生成（行動計画完了通知など）

#### milestone（マイルストーン更新）

1. マイルストーンIDの存在チェック
2. マイルストーンステータスの妥当性チェック
3. 完了日の検証（ステータスが"completed"の場合）
4. マイルストーンの更新
5. マイルストーンの進捗状況の再計算
6. 関連する通知の生成（マイルストーン達成通知など）

#### skill_level（スキルレベル更新）

1. スキルIDの存在チェック
2. スキルレベルの範囲チェック（1-5）
3. スキルレベルの更新
4. スキルの進捗率の再計算
5. 関連する通知の生成（スキルレベル向上通知など）

#### feedback（フィードバック追加）

1. フィードバック内容の検証
2. フィードバックタイプの妥当性チェック
3. フィードバックの追加
4. 関連する通知の生成（フィードバック受信通知）

### 4.4 進捗率の再計算

- 更新内容に基づいて目標の進捗率を再計算
- 計算方法はAPI-033（目標進捗取得API）と同様
- 更新された進捗率はレスポンスに含める

### 4.5 更新履歴の記録

- 更新内容を career_goal_updates テーブルに記録
- 更新履歴には以下の情報を含める
  - 更新ID
  - 目標ID
  - 更新タイプ
  - 更新内容
  - 更新コメント
  - 更新日時
  - 更新者ID

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-021](API仕様書_API-021.md) | スキル情報取得API | ユーザースキル情報取得 |
| [API-031](API仕様書_API-031.md) | キャリア目標取得API | キャリア目標情報取得 |
| [API-032](API仕様書_API-032.md) | キャリア目標更新API | キャリア目標情報更新 |
| [API-033](API仕様書_API-033.md) | 目標進捗取得API | 目標進捗情報取得 |
| [API-201](API仕様書_API-201.md) | 通知一覧取得API | 通知一覧取得 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| career_goals | キャリア目標情報 | 更新（U） |
| career_goal_skills | キャリア目標関連スキル | 参照（R） |
| career_goal_actions | キャリア目標行動計画 | 更新（U） |
| career_goal_milestones | キャリア目標マイルストーン | 更新（U） |
| career_goal_feedback | キャリア目標フィードバック | 作成（C） |
| career_goal_updates | キャリア目標更新履歴 | 作成（C） |
| user_skills | ユーザースキル情報 | 更新（U） |
| notifications | 通知情報 | 作成（C） |

### 5.3 注意事項・補足

- 目標ステータスが"completed"に変更された場合、関連する全ての行動計画とマイルストーンも自動的に完了状態に更新される
- 目標ステータスが"postponed"または"cancelled"に変更された場合、理由の入力が必須
- スキルレベルの更新は、user_skills テーブルにも反映される
- フィードバックは追加のみ可能で、更新・削除は不可
- 更新履歴は時系列で保持され、目標の進捗状況の変遷を追跡可能
- 更新操作によって通知が生成され、関係者に通知される
- 完了した目標は更新不可（読み取り専用）

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import { useForm, Controller } from 'react-hook-form';
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
  Box,
  Snackbar,
  Alert,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormLabel,
  Rating
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';

// バリデーションスキーマ（目標ステータス更新用）
const statusUpdateSchema = yup.object().shape({
  goal_id: yup.string().required('目標IDは必須です'),
  update_type: yup.string().required('更新タイプは必須です').oneOf(['status']),
  update_data: yup.object().shape({
    status: yup.string()
      .required('ステータスは必須です')
      .oneOf(['not_started', 'in_progress', 'completed', 'postponed', 'cancelled'], '無効なステータスです'),
    completion_date: yup.date().when('status', {
      is: 'completed',
      then: yup.date().required('完了日は必須です').max(new Date(), '未来の日付は指定できません'),
      otherwise: yup.date().nullable()
    }),
    reason: yup.string().when('status', {
      is: (val: string) => val === 'postponed' || val === 'cancelled',
      then: yup.string().required('理由は必須です').max(500, '500文字以内で入力してください'),
      otherwise: yup.string().nullable()
    })
  }),
  comment: yup.string().max(500, '500文字以内で入力してください')
});

// バリデーションスキーマ（行動計画更新用）
const actionPlanUpdateSchema = yup.object().shape({
  goal_id: yup.string().required('目標IDは必須です'),
  update_type: yup.string().required('更新タイプは必須です').oneOf(['action_plan']),
  update_data: yup.object().shape({
    action_id: yup.string().required('行動計画IDは必須です'),
    status: yup.string()
      .required('ステータスは必須です')
      .oneOf(['not_started', 'in_progress', 'completed'], '無効なステータスです'),
    completion_date: yup.date().when('status', {
      is: 'completed',
      then: yup.date().required('完了日は必須です').max(new Date(), '未来の日付は指定できません'),
      otherwise: yup.date().nullable()
    }),
    progress_note: yup.string().max(500, '500文字以内で入力してください')
  }),
  comment: yup.string().max(500, '500文字以内で入力してください')
});

// バリデーションスキーマ（スキルレベル更新用）
const skillLevelUpdateSchema = yup.object().shape({
  goal_id: yup.string().required('目標IDは必須です'),
  update_type: yup.string().required('更新タイプは必須です').oneOf(['skill_level']),
  update_data: yup.object().shape({
    skill_id: yup.string().required('スキルIDは必須です'),
    current_level: yup.number()
      .required('現在のレベルは必須です')
      .min(1, 'レベルは1以上である必要があります')
      .max(5, 'レベルは5以下である必要があります')
      .integer('レベルは整数である必要があります'),
    evidence: yup.string().max(500, '500文字以内で入力してください')
  }),
  comment: yup.string().max(500, '500文字以内で入力してください')
});

// 型定義
interface StatusUpdateFormData {
  goal_id: string;
  update_type: 'status';
  update_data: {
    status: 'not_started' | 'in_progress' | 'completed' | 'postponed' | 'cancelled';
    completion_date?: Date | null;
    reason?: string | null;
  };
  comment?: string;
}

interface ActionPlanUpdateFormData {
  goal_id: string;
  update_type: 'action_plan';
  update_data: {
    action_id: string;
    status: 'not_started' | 'in_progress' | 'completed';
    completion_date?: Date | null;
    progress_note?: string;
  };
  comment?: string;
}

interface SkillLevelUpdateFormData {
  goal_id: string;
  update_type: 'skill_level';
  update_data: {
    skill_id: string;
    current_level: number;
    evidence?: string;
  };
  comment?: string;
}

interface ActionPlan {
  action_id: string;
  title: string;
  status: 'not_started' | 'in_progress' | 'completed';
  due_date: string;
  completion_date?: string | null;
}

interface RelatedSkill {
  skill_id: string;
  name: string;
  category: string;
  target_level: number;
  current_level: number;
}

interface GoalDetails {
  goal_id: string;
  title: string;
  status: 'not_started' | 'in_progress' | 'completed' | 'postponed' | 'cancelled';
  action_plans: ActionPlan[];
  related_skills: RelatedSkill[];
}

// 目標ステータス更新フォームコンポーネント
const GoalStatusUpdateForm: React.FC<{ goalDetails: GoalDetails }> = ({ goalDetails }) => {
  const { userId } = useParams<{ userId: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<boolean>(false);
  
  const {
