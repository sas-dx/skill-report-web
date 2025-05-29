# API一覧

以下は年間スキル報告書WEB化PJTのAPI一覧です。各API IDをクリックすると、詳細なAPI仕様書を参照できます。

## 認証・認可系API

| API ID | API名称 | エンドポイント | HTTPメソッド | 概要 | 利用画面 | API仕様書リンク |
|--------|--------|---------------|------------|------|---------|---------------|
| [API-001](specs/API仕様書_API-001.md) | ユーザー認証API | /api/auth/login | POST | ユーザーID・パスワードによる認証 | SCR-LOGIN | [詳細仕様書](specs/API仕様書_API-001.md) |
| [API-002](specs/API仕様書_API-002.md) | SSO認証API | /api/auth/sso | GET | シングルサインオン認証 | SCR-LOGIN | [詳細仕様書](specs/API仕様書_API-002.md) |
| [API-003](specs/API仕様書_API-003.md) | 権限情報取得API | /api/auth/permissions | GET | ユーザー権限情報取得 | SCR-ACCESS | [詳細仕様書](specs/API仕様書_API-003.md) |
| [API-004](specs/API仕様書_API-004.md) | 権限設定API | /api/auth/permissions | PUT | ユーザー権限情報更新 | SCR-ACCESS | [詳細仕様書](specs/API仕様書_API-004.md) |

## プロフィール系API

| API ID | API名称 | エンドポイント | HTTPメソッド | 概要 | 利用画面 | API仕様書リンク |
|--------|--------|---------------|------------|------|---------|---------------|
| [API-011](specs/API仕様書_API-011.md) | プロフィール取得API | /api/profiles/{user_id} | GET | ユーザープロフィール情報取得 | SCR-PROFILE | [詳細仕様書](specs/API仕様書_API-011.md) |
| [API-012](specs/API仕様書_API-012.md) | プロフィール更新API | /api/profiles/{user_id} | PUT | ユーザープロフィール情報更新 | SCR-PROFILE | [詳細仕様書](specs/API仕様書_API-012.md) |
| [API-013](specs/API仕様書_API-013.md) | 組織情報取得API | /api/organizations | GET | 組織情報一覧取得 | SCR-PROFILE, SCR-ADMIN | [詳細仕様書](specs/API仕様書_API-013.md) |

## スキル管理系API

| API ID | API名称 | エンドポイント | HTTPメソッド | 概要 | 利用画面 | API仕様書リンク |
|--------|--------|---------------|------------|------|---------|---------------|
| [API-021](specs/API仕様書_API-021.md) | スキル情報取得API | /api/skills/{user_id} | GET | ユーザースキル情報取得 | SCR-SKILL | [詳細仕様書](specs/API仕様書_API-021.md) |
| [API-022](specs/API仕様書_API-022.md) | スキル情報更新API | /api/skills/{user_id} | PUT | ユーザースキル情報更新 | SCR-SKILL | [詳細仕様書](specs/API仕様書_API-022.md) |
| [API-023](specs/API仕様書_API-023.md) | スキルマスタ取得API | /api/skill-masters | GET | スキルマスタ情報取得 | SCR-SKILL-M | [詳細仕様書](specs/API仕様書_API-023.md) |
| [API-024](specs/API仕様書_API-024.md) | スキルマスタ更新API | /api/skill-masters | PUT | スキルマスタ情報更新 | SCR-SKILL-M | [詳細仕様書](specs/API仕様書_API-024.md) |
| [API-025](specs/API仕様書_API-025.md) | スキル検索API | /api/skills/search | POST | 条件指定によるスキル検索 | SCR-SKILL-SEARCH | [詳細仕様書](specs/API仕様書_API-025.md) |
| [API-026](specs/API仕様書_API-026.md) | スキルマップ生成API | /api/skills/map | POST | スキルマップデータ生成 | SCR-SKILL-MAP | [詳細仕様書](specs/API仕様書_API-026.md) |

## キャリア・目標管理系API

| API ID | API名称 | エンドポイント | HTTPメソッド | 概要 | 利用画面 | API仕様書リンク |
|--------|--------|---------------|------------|------|---------|---------------|
| [API-031](specs/API仕様書_API-031.md) | キャリア目標取得API | /api/career-goals/{user_id} | GET | キャリア目標情報取得 | SCR-CAREER | [詳細仕様書](specs/API仕様書_API-031.md) |
| [API-032](specs/API仕様書_API-032.md) | キャリア目標更新API | /api/career-goals/{user_id} | PUT | キャリア目標情報更新 | SCR-CAREER | [詳細仕様書](specs/API仕様書_API-032.md) |
| [API-033](specs/API仕様書_API-033.md) | 目標進捗取得API | /api/goal-progress/{user_id} | GET | 目標進捗情報取得 | SCR-CAREER | [詳細仕様書](specs/API仕様書_API-033.md) |
| [API-034](specs/API仕様書_API-034.md) | 目標進捗更新API | /api/goal-progress/{user_id} | PUT | 目標進捗情報更新 | SCR-CAREER | [詳細仕様書](specs/API仕様書_API-034.md) |

## 作業実績管理系API

| API ID | API名称 | エンドポイント | HTTPメソッド | 概要 | 利用画面 | API仕様書リンク |
|--------|--------|---------------|------------|------|---------|---------------|
| [API-041](specs/API仕様書_API-041.md) | 作業実績取得API | /api/work-records/{user_id} | GET | 作業実績情報取得 | SCR-WORK | [詳細仕様書](specs/API仕様書_API-041.md) |
| [API-042](specs/API仕様書_API-042.md) | 作業実績登録API | /api/work-records/{user_id} | POST | 作業実績情報登録 | SCR-WORK | [詳細仕様書](specs/API仕様書_API-042.md) |
| [API-043](specs/API仕様書_API-043.md) | 作業実績更新API | /api/work-records/{user_id}/{record_id} | PUT | 作業実績情報更新 | SCR-WORK | [詳細仕様書](specs/API仕様書_API-043.md) |
| [API-101](specs/API仕様書_API-101.md) | 一括登録検証API | /api/work/bulk/validate | POST | 一括登録データ検証 | SCR-WORK-BULK | [詳細仕様書](specs/API仕様書_API-101.md) |
| [API-102](specs/API仕様書_API-102.md) | 一括登録実行API | /api/work/bulk | POST | 一括登録実行 | SCR-WORK-BULK | [詳細仕様書](specs/API仕様書_API-102.md) |
| [API-103](specs/API仕様書_API-103.md) | テンプレート取得API | /api/work/bulk/template | GET | 一括登録テンプレート取得 | SCR-WORK-BULK | [詳細仕様書](specs/API仕様書_API-103.md) |

## 研修・資格管理系API

| API ID | API名称 | エンドポイント | HTTPメソッド | 概要 | 利用画面 | API仕様書リンク |
|--------|--------|---------------|------------|------|---------|---------------|
| [API-051](specs/API仕様書_API-051.md) | 研修記録取得API | /api/trainings/{user_id} | GET | 研修記録情報取得 | SCR-TRAINING | [詳細仕様書](specs/API仕様書_API-051.md) |
| [API-052](specs/API仕様書_API-052.md) | 研修記録登録API | /api/trainings/{user_id} | POST | 研修記録情報登録 | SCR-TRAINING | [詳細仕様書](specs/API仕様書_API-052.md) |
| [API-053](specs/API仕様書_API-053.md) | 資格情報取得API | /api/certifications/{user_id} | GET | 資格情報取得 | SCR-TRAINING | [詳細仕様書](specs/API仕様書_API-053.md) |
| [API-054](specs/API仕様書_API-054.md) | 資格情報更新API | /api/certifications/{user_id} | PUT | 資格情報更新 | SCR-TRAINING | [詳細仕様書](specs/API仕様書_API-054.md) |

## レポート・分析系API

| API ID | API名称 | エンドポイント | HTTPメソッド | 概要 | 利用画面 | API仕様書リンク |
|--------|--------|---------------|------------|------|---------|---------------|
| [API-061](specs/API仕様書_API-061.md) | レポート生成API | /api/reports | POST | レポート生成 | SCR-REPORT | [詳細仕様書](specs/API仕様書_API-061.md) |
| [API-062](specs/API仕様書_API-062.md) | レポート取得API | /api/reports/{report_id} | GET | 生成済みレポート取得 | SCR-REPORT | [詳細仕様書](specs/API仕様書_API-062.md) |

## 通知・アラート系API

| API ID | API名称 | エンドポイント | HTTPメソッド | 概要 | 利用画面 | API仕様書リンク |
|--------|--------|---------------|------------|------|---------|---------------|
| [API-201](specs/API仕様書_API-201.md) | 通知一覧取得API | /api/notifications | GET | 通知一覧取得 | SCR-NOTIFY | [詳細仕様書](specs/API仕様書_API-201.md) |
| [API-202](specs/API仕様書_API-202.md) | 通知詳細取得API | /api/notifications/{id} | GET | 通知詳細取得 | SCR-NOTIFY | [詳細仕様書](specs/API仕様書_API-202.md) |
| [API-203](specs/API仕様書_API-203.md) | 通知状態更新API | /api/notifications/{id}/read | PUT | 通知既読状態更新 | SCR-NOTIFY | [詳細仕様書](specs/API仕様書_API-203.md) |
| [API-204](specs/API仕様書_API-204.md) | 全通知既読API | /api/notifications/read-all | PUT | 全通知既読化 | SCR-NOTIFY | [詳細仕様書](specs/API仕様書_API-204.md) |

## システム管理系API

| API ID | API名称 | エンドポイント | HTTPメソッド | 概要 | 利用画面 | API仕様書リンク |
|--------|--------|---------------|------------|------|---------|---------------|
| [API-071](specs/API仕様書_API-071.md) | システム設定取得API | /api/system/settings | GET | システム設定情報取得 | SCR-ADMIN | [詳細仕様書](specs/API仕様書_API-071.md) |
| [API-072](specs/API仕様書_API-072.md) | システム設定更新API | /api/system/settings | PUT | システム設定情報更新 | SCR-ADMIN | [詳細仕様書](specs/API仕様書_API-072.md) |
| [API-073](specs/API仕様書_API-073.md) | マスタデータ取得API | /api/system/masters/{master_type} | GET | マスタデータ取得 | SCR-ADMIN | [詳細仕様書](specs/API仕様書_API-073.md) |
| [API-074](specs/API仕様書_API-074.md) | マスタデータ更新API | /api/system/masters/{master_type} | PUT | マスタデータ更新 | SCR-ADMIN | [詳細仕様書](specs/API仕様書_API-074.md) |

## ホーム・ダッシュボード系API

| API ID | API名称 | エンドポイント | HTTPメソッド | 概要 | 利用画面 | API仕様書リンク |
|--------|--------|---------------|------------|------|---------|---------------|
| [API-081](specs/API仕様書_API-081.md) | ダッシュボードデータ取得API | /api/dashboard | GET | ダッシュボード表示データ取得 | SCR-HOME | [詳細仕様書](specs/API仕様書_API-081.md) |
| [API-082](specs/API仕様書_API-082.md) | ユーザーサマリー取得API | /api/dashboard/user-summary | GET | ユーザー情報サマリー取得 | SCR-HOME | [詳細仕様書](specs/API仕様書_API-082.md) |
