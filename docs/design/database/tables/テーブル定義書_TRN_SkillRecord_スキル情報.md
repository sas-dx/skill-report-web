# テーブル定義書: TRN_SkillRecord

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_SkillRecord |
| 論理名 | スキル情報 |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-21 22:02:17 |

## 概要

TRN_SkillRecord（スキル情報）は、組織内の全社員が保有するスキル・技術・資格等の詳細情報を管理するトランザクションテーブルです。
主な目的：
- 社員個人のスキルポートフォリオ管理（技術スキル、ビジネススキル、資格等）
- スキルレベルの客観的評価・管理（5段階評価システム）
- 自己評価と上司評価による多面的スキル評価
- プロジェクトアサインメントのためのスキルマッチング
- 人材育成計画・キャリア開発支援
- 組織全体のスキル可視化・分析
- 資格取得状況・有効期限管理
このテーブルは、人材配置の最適化、教育研修計画の策定、組織のスキルギャップ分析など、
戦略的人材マネジメントの基盤となる重要なデータを提供します。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| skillrecord_id | TRN_SkillRecordの主キー | SERIAL |  | × |  | TRN_SkillRecordの主キー |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_by | レコード作成者のユーザーID | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | レコード更新者のユーザーID | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_trn_skillrecord_tenant_id | tenant_id | × | テナントID検索用インデックス |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_skill_employee | None | None | None | CASCADE | CASCADE | 外部キー制約 |
| fk_skill_item | None | None | None | CASCADE | CASCADE | 外部キー制約 |
| fk_skill_certification | None | None | None | CASCADE | SET NULL | 外部キー制約 |
| fk_skill_category | None | None | None | CASCADE | SET NULL | 外部キー制約 |
| fk_skill_assessor | None | None | None | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_trn_skillrecord | PRIMARY KEY | skillrecord_id, id | 主キー制約 |

## サンプルデータ

| employee_id | skill_item_id | skill_level | self_assessment | manager_assessment | evidence_description | acquisition_date | last_used_date | expiry_date | certification_id | skill_category_id | assessment_date | assessor_id | skill_status | learning_hours | project_experience_count |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| EMP000001 | SKILL001 | 4 | 4 | 3 | Javaを使用したWebアプリケーション開発プロジェクトを3件担当 | 2020-06-01 | 2025-05-30 | None | CERT001 | CAT001 | 2025-04-01 | EMP000010 | ACTIVE | 120 | 3 |
| EMP000001 | SKILL002 | 3 | 3 | 3 | AWS環境でのインフラ構築・運用経験 | 2021-03-15 | 2025-05-25 | 2026-03-15 | CERT002 | CAT002 | 2025-04-01 | EMP000010 | ACTIVE | 80 | 2 |

## 特記事項

- 社員とスキル項目の組み合わせは一意（1人の社員が同じスキルを複数持つことはない）
- スキルレベルは1-5の5段階評価（1:初級、5:マスター）
- 自己評価と上司評価は任意項目（評価制度に応じて入力）
- 有効期限は資格系スキルの場合に設定
- 学習時間とプロジェクト経験回数は統計・分析用
- スキル状況により論理削除を実現

## 業務ルール

- スキルレベルは客観的な基準に基づいて設定
- 自己評価と上司評価の乖離が大きい場合は再評価を実施
- 有効期限が近づいた資格は自動的に通知
- 期限切れスキルは skill_status を EXPIRED に変更
- 評価は年1回以上実施することを推奨
- プロジェクト経験回数は実績管理システムと連携

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - スキル記録トランザクションテーブルの詳細定義 |