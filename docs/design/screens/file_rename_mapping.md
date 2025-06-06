# 画面定義書ファイル名統一化マッピング

## 統一化方針
- 標準フォーマット: `画面定義書_SCR_[カテゴリ]_[機能]_[画面名].md`
- 画面一覧.mdのリンクと一致させる
- ルールに従い `SCR-` から `SCR_` に統一

## ファイル名変更マッピング

### 現在存在するファイル → 統一後のファイル名

| 現在のファイル名 | 統一後のファイル名 | 画面一覧.mdでの期待ファイル名 | 状態 |
|-----------------|------------------|---------------------------|------|
| 画面定義書_SCR_AUT_Login_ログイン画面.md | 画面定義書_SCR_AUT_Login_ログイン画面.md | specs/画面定義書_SCR_AUT_Login_ログイン画面.md | ✅ 一致 |
| 画面定義書_SCR_AUT_Login_ログイン画面_Mermaid.md | 画面定義書_SCR_AUT_Login_ログイン画面_Mermaid.md | - | 📝 補助ファイル |
| 画面定義書_SCR_CMN_Home_ホームダッシュボード画面.md | 画面定義書_SCR_CMN_Home_ホーム画面.md | specs/画面定義書_SCR_CMN_Home_ホーム画面.md | 🔄 要変更 |
| 画面定義書_SCR_TEN_Admin_テナント管理画面.md | 画面定義書_SCR_TNT_Admin_テナント管理画面.md | specs/画面定義書_SCR_TNT_Admin_テナント管理画面.md | 🔄 要変更 |
| 画面定義書_SCR_TEN_Select_テナント選択画面.md | 画面定義書_SCR_TNT_Select_テナント選択画面.md | specs/画面定義書_SCR_TNT_Select_テナント選択画面.md | 🔄 要変更 |
| 画面定義書_SCR-ACCESS_アクセス画面.md | 画面定義書_SCR_ACC_Access_権限管理画面.md | specs/画面定義書_SCR_ACC_Access_権限管理画面.md | 🔄 要変更 |
| 画面定義書_SCR-ADMIN_管理画面.md | 画面定義書_SCR_ADM_System_システム管理画面.md | specs/画面定義書_SCR_ADM_System_システム管理画面.md | 🔄 要変更 |
| 画面定義書_SCR-CAREER_キャリア画面.md | 画面定義書_SCR_CAR_Plan_キャリアプラン画面.md | specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md | 🔄 要変更 |
| 画面定義書_SCR-HOME_ホーム画面.md | 画面定義書_SCR_CMN_Home_ホーム画面.md | specs/画面定義書_SCR_CMN_Home_ホーム画面.md | 🔄 要変更（重複） |
| 画面定義書_SCR-LOGIN_ログイン画面.md | 画面定義書_SCR_AUT_Login_ログイン画面.md | specs/画面定義書_SCR_AUT_Login_ログイン画面.md | 🔄 要変更（重複） |
| 画面定義書_SCR-NOTIFY_通知画面.md | 画面定義書_SCR_NTF_Admin_通知管理画面.md | specs/画面定義書_SCR_NTF_Admin_通知管理画面.md | 🔄 要変更 |
| 画面定義書_SCR-NOTIFY-ADMIN_通知設定管理画面.md | 画面定義書_SCR_NTF_Admin_通知管理画面.md | specs/画面定義書_SCR_NTF_Admin_通知管理画面.md | 🔄 要変更（重複） |
| 画面定義書_SCR-PROFILE_プロフィール画面.md | 画面定義書_SCR_PRO_Profile_プロフィール画面.md | specs/画面定義書_SCR_PRO_Profile_プロフィール画面.md | 🔄 要変更 |
| 画面定義書_SCR-REPORT_レポート画面.md | 画面定義書_SCR_RPT_Report_レポート出力画面.md | specs/画面定義書_SCR_RPT_Report_レポート出力画面.md | 🔄 要変更 |
| 画面定義書_SCR-SKILL_スキル画面.md | 画面定義書_SCR_SKL_Skill_スキル管理画面.md | specs/画面定義書_SCR_SKL_Skill_スキル管理画面.md | 🔄 要変更 |
| 画面定義書_SCR-SKILL-M_スキル管理画面.md | 画面定義書_SCR_SKL_Master_スキルマスタ管理画面.md | specs/画面定義書_SCR_SKL_Master_スキルマスタ管理画面.md | 🔄 要変更 |
| 画面定義書_SCR-SKILL-MAP_スキルマップ画面.md | 画面定義書_SCR_SKL_Map_スキルマップ画面.md | specs/画面定義書_SCR_SKL_Map_スキルマップ画面.md | 🔄 要変更 |
| 画面定義書_SCR-SKILL-SEARCH_スキル検索画面.md | 画面定義書_SCR_SKL_Search_スキル検索画面.md | specs/画面定義書_SCR_SKL_Search_スキル検索画面.md | 🔄 要変更 |
| 画面定義書_SCR-TENANT-ADMIN_テナント管理画面.md | 画面定義書_SCR_TNT_Admin_テナント管理画面.md | specs/画面定義書_SCR_TNT_Admin_テナント管理画面.md | 🔄 要変更（重複） |
| 画面定義書_SCR-TENANT-SELECT_テナント選択画面.md | 画面定義書_SCR_TNT_Select_テナント選択画面.md | specs/画面定義書_SCR_TNT_Select_テナント選択画面.md | 🔄 要変更（重複） |
| 画面定義書_SCR-TRAINING_研修画面.md | 画面定義書_SCR_TRN_Train_研修管理画面.md | specs/画面定義書_SCR_TRN_Train_研修管理画面.md | 🔄 要変更 |
| 画面定義書_SCR-WORK_作業画面.md | 画面定義書_SCR_WPM_Work_作業実績画面.md | specs/画面定義書_SCR_WPM_Work_作業実績画面.md | 🔄 要変更 |
| 画面定義書_SCR-WORK-BULK_作業一括画面.md | 画面定義書_SCR_WPM_Bulk_一括登録画面.md | specs/画面定義書_SCR_WPM_Bulk_一括登録画面.md | 🔄 要変更 |

## 画面一覧.mdに記載されているが存在しないファイル

| 画面一覧.mdでの期待ファイル名 | 状態 |
|---------------------------|------|
| specs/画面定義書_SCR_CAR_Eval_目標評価画面.md | ❌ 未作成 |
| specs/画面定義書_SCR_TRN_Master_研修マスタ画面.md | ❌ 未作成 |
| specs/画面定義書_SCR_ADM_Master_マスタ管理画面.md | ❌ 未作成 |

## 重複ファイルの処理方針

### 1. ログイン画面（2ファイル存在）
- `画面定義書_SCR_AUT_Login_ログイン画面.md` ← メイン（保持）
- `画面定義書_SCR-LOGIN_ログイン画面.md` ← 削除対象

### 2. ホーム画面（2ファイル存在）
- `画面定義書_SCR_CMN_Home_ホームダッシュボード画面.md` ← リネーム
- `画面定義書_SCR-HOME_ホーム画面.md` ← 削除対象

### 3. テナント管理画面（2ファイル存在）
- `画面定義書_SCR_TEN_Admin_テナント管理画面.md` ← リネーム
- `画面定義書_SCR-TENANT-ADMIN_テナント管理画面.md` ← 削除対象

### 4. テナント選択画面（2ファイル存在）
- `画面定義書_SCR_TEN_Select_テナント選択画面.md` ← リネーム
- `画面定義書_SCR-TENANT-SELECT_テナント選択画面.md` ← 削除対象

### 5. 通知管理画面（2ファイル存在）
- `画面定義書_SCR-NOTIFY_通知画面.md` ← リネーム
- `画面定義書_SCR-NOTIFY-ADMIN_通知設定管理画面.md` ← 削除対象

## 実行手順

1. 重複ファイルの内容確認・統合
2. ファイル名変更実行
3. 不要ファイル削除
4. 画面一覧.mdのリンク確認・修正
5. 未作成ファイルの作成（必要に応じて）
