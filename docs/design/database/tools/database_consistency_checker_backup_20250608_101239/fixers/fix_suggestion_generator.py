"""
修正提案生成器
データベース整合性チェックで検出された問題に対する修正提案を生成する
"""
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass

from core.models import CheckResult, CheckSeverity, FixSuggestion, FixType
from core.logger import ConsistencyLogger


@dataclass
class FixContext:
    """修正提案のコンテキスト情報"""
    base_dir: Path
    ddl_dir: Path
    yaml_details_dir: Path
    table_list_file: Path
    entity_relationships_file: Path


class FixSuggestionGenerator:
    """修正提案生成器"""
    
    def __init__(self, logger: Optional[ConsistencyLogger] = None):
        self.logger = logger or ConsistencyLogger()
    
    def generate_fix_suggestions(
        self,
        check_results: List[CheckResult],
        fix_context: FixContext,
        fix_types: List[FixType] = None
    ) -> List[FixSuggestion]:
        """チェック結果から修正提案を生成"""
        if fix_types is None:
            fix_types = [FixType.ALL]
        
        suggestions = []
        
        # エラーと警告のみを対象とする
        error_results = [r for r in check_results if r.severity in [CheckSeverity.ERROR, CheckSeverity.WARNING]]
        
        for result in error_results:
            result_suggestions = self._generate_suggestions_for_result(result, fix_context, fix_types)
            suggestions.extend(result_suggestions)
        
        # 重複する提案を除去
        unique_suggestions = self._deduplicate_suggestions(suggestions)
        
        # 優先度順にソート
        sorted_suggestions = self._sort_suggestions_by_priority(unique_suggestions)
        
        return sorted_suggestions
    
    def _generate_suggestions_for_result(
        self,
        result: CheckResult,
        fix_context: FixContext,
        fix_types: List[FixType]
    ) -> List[FixSuggestion]:
        """単一のチェック結果に対する修正提案を生成"""
        suggestions = []
        
        # チェック名と問題タイプに基づいて適切な修正提案を生成
        if result.check_name == "table_existence":
            suggestions.extend(self._generate_table_existence_fixes(result, fix_context, fix_types))
        elif result.check_name == "foreign_key_consistency":
            suggestions.extend(self._generate_foreign_key_fixes(result, fix_context, fix_types))
        elif result.check_name == "constraint_consistency":
            suggestions.extend(self._generate_constraint_fixes(result, fix_context, fix_types))
        elif result.check_name == "data_type_consistency":
            suggestions.extend(self._generate_data_type_fixes(result, fix_context, fix_types))
        elif result.check_name == "yaml_format_consistency":
            suggestions.extend(self._generate_yaml_format_fixes(result, fix_context, fix_types))
        
        return suggestions
    
    def _generate_table_existence_fixes(
        self,
        result: CheckResult,
        fix_context: FixContext,
        fix_types: List[FixType]
    ) -> List[FixSuggestion]:
        """テーブル存在チェックの修正提案を生成"""
        suggestions = []
        
        if "テーブル一覧.mdに定義されていません" in result.message:
            # テーブル一覧.mdへの追加提案
            if FixType.ALL in fix_types or FixType.INSERT in fix_types:
                table_name = result.table_name
                
                # テーブルカテゴリの推測
                category = self._guess_table_category(table_name)
                
                fix_content = f"""
## テーブル一覧.mdへの追加提案

以下の行をテーブル一覧.mdの適切な位置に追加してください：

```markdown
| {table_name} | {self._generate_table_description(table_name)} | {category} |
```

### 追加手順：
1. `{fix_context.table_list_file}` を開く
2. {category}セクションを見つける
3. アルファベット順に適切な位置に上記の行を挿入
4. ファイルを保存
"""
                
                suggestions.append(FixSuggestion(
                    fix_type=FixType.INSERT,
                    table_name=table_name,
                    description=f"テーブル一覧.mdに{table_name}を追加",
                    fix_content=fix_content,
                    file_path=str(fix_context.table_list_file),
                    backup_required=True,
                    critical=True
                ))
        
        elif "DDLファイルが存在しません" in result.message:
            # DDLファイル作成提案
            if FixType.ALL in fix_types or FixType.DDL in fix_types:
                table_name = result.table_name
                
                fix_content = f"""
## DDLファイル作成提案

以下のテンプレートを使用して `{table_name}.sql` を作成してください：

```sql
-- {table_name} テーブル定義
CREATE TABLE {table_name} (
    id VARCHAR(50) NOT NULL COMMENT 'ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (id),
    INDEX idx_{table_name.lower()}_tenant_id (tenant_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='{self._generate_table_description(table_name)}';
```

### 作成手順：
1. `{fix_context.ddl_dir}/{table_name}.sql` ファイルを作成
2. 上記のテンプレートをベースに実際のカラム定義を追加
3. 適切な制約と外部キーを設定
"""
                
                suggestions.append(FixSuggestion(
                    fix_type=FixType.DDL,
                    table_name=table_name,
                    description=f"{table_name}のDDLファイルを作成",
                    fix_content=fix_content,
                    file_path=str(fix_context.ddl_dir / f"{table_name}.sql"),
                    backup_required=False,
                    critical=True
                ))
        
        elif "YAML詳細ファイルが存在しません" in result.message:
            # YAML詳細ファイル作成提案
            if FixType.ALL in fix_types or FixType.YAML in fix_types:
                table_name = result.table_name
                
                fix_content = f"""
## YAML詳細ファイル作成提案

以下のテンプレートを使用して `{table_name}_details.yaml` を作成してください：

```yaml
table_name: {table_name}
description: {self._generate_table_description(table_name)}
category: {self._guess_table_category(table_name)}

columns:
  - name: id
    logical_name: ID
    data_type: VARCHAR(50)
    nullable: false
    primary_key: true
    comment: ID
  
  - name: tenant_id
    logical_name: テナントID
    data_type: VARCHAR(50)
    nullable: false
    comment: テナントID
  
  - name: created_at
    logical_name: 作成日時
    data_type: TIMESTAMP
    nullable: false
    default_value: CURRENT_TIMESTAMP
    comment: 作成日時
  
  - name: updated_at
    logical_name: 更新日時
    data_type: TIMESTAMP
    nullable: false
    default_value: CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    comment: 更新日時

indexes:
  - name: idx_{table_name.lower()}_tenant_id
    columns: [tenant_id]
    unique: false
    description: テナントID検索用インデックス

foreign_keys: []

constraints: []

sample_data: []

notes: []

business_rules: []
```

### 作成手順：
1. `{fix_context.yaml_details_dir}/{table_name}_details.yaml` ファイルを作成
2. 上記のテンプレートをベースに実際のカラム定義を追加
3. 適切な外部キーと制約を設定
"""
                
                suggestions.append(FixSuggestion(
                    fix_type=FixType.YAML,
                    table_name=table_name,
                    description=f"{table_name}のYAML詳細ファイルを作成",
                    fix_content=fix_content,
                    file_path=str(fix_context.yaml_details_dir / f"{table_name}_details.yaml"),
                    backup_required=False,
                    critical=True
                ))
        
        return suggestions
    
    def _generate_foreign_key_fixes(
        self,
        result: CheckResult,
        fix_context: FixContext,
        fix_types: List[FixType]
    ) -> List[FixSuggestion]:
        """外部キー整合性チェックの修正提案を生成"""
        suggestions = []
        
        issue_type = result.details.get('issue_type', '')
        
        if 'on_update_mismatch' in issue_type or 'on_delete_mismatch' in issue_type:
            # カスケード設定の統一提案
            if FixType.ALL in fix_types or FixType.DDL in fix_types or FixType.YAML in fix_types:
                fk_name = result.details.get('foreign_key_name', 'unknown')
                recommended_setting = result.details.get('recommended_setting', 'CASCADE')
                
                if 'on_update_mismatch' in issue_type:
                    setting_type = 'ON UPDATE'
                    ddl_setting = result.details.get('ddl_on_update', 'RESTRICT')
                    yaml_setting = result.details.get('yaml_on_update', 'RESTRICT')
                else:
                    setting_type = 'ON DELETE'
                    ddl_setting = result.details.get('ddl_on_delete', 'RESTRICT')
                    yaml_setting = result.details.get('yaml_on_delete', 'RESTRICT')
                
                fix_content = f"""
## 外部キーカスケード設定統一提案

外部キー `{fk_name}` の{setting_type}設定を統一してください。

### 現在の設定：
- DDL: {ddl_setting}
- YAML: {yaml_setting}

### 推奨設定：
- 統一設定: {recommended_setting}

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE {result.table_name} DROP FOREIGN KEY {fk_name};

-- 新しい外部キー制約を追加
ALTER TABLE {result.table_name} ADD CONSTRAINT {fk_name}
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE {recommended_setting}
    ON DELETE {recommended_setting if 'DELETE' in setting_type else 'SET NULL'};
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: {fk_name}
    # ... 他の設定 ...
    on_update: {recommended_setting}
    on_delete: {recommended_setting if 'DELETE' in setting_type else 'SET NULL'}
```
"""
                
                suggestions.append(FixSuggestion(
                    fix_type=FixType.ALL,
                    table_name=result.table_name,
                    description=f"外部キー{fk_name}の{setting_type}設定を統一",
                    fix_content=fix_content,
                    file_path="",
                    backup_required=True,
                    critical=False
                ))
        
        elif 'missing_target_column' in issue_type:
            # 参照先カラム名の修正提案
            if FixType.ALL in fix_types or FixType.DDL in fix_types or FixType.YAML in fix_types:
                fk_name = result.details.get('foreign_key_name', 'unknown')
                target_table = result.details.get('target_table', 'unknown')
                target_column = result.details.get('target_column', 'id')
                available_columns = result.details.get('available_columns', [])
                
                # 適切な参照先カラムを推測
                suggested_column = self._suggest_reference_column(target_table, target_column, available_columns)
                
                fix_content = f"""
## 外部キー参照先カラム修正提案

外部キー `{fk_name}` の参照先カラム `{target_table}.{target_column}` が存在しません。

### 利用可能なカラム：
{chr(10).join(f'- {col}' for col in available_columns)}

### 推奨修正：
参照先カラムを `{suggested_column}` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE {result.table_name} DROP FOREIGN KEY {fk_name};

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE {result.table_name} ADD CONSTRAINT {fk_name}
    FOREIGN KEY (...) REFERENCES {target_table}({suggested_column})
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: {fk_name}
    # ... 他の設定 ...
    reference_table: {target_table}
    reference_column: {suggested_column}
```
"""
                
                suggestions.append(FixSuggestion(
                    fix_type=FixType.ALL,
                    table_name=result.table_name,
                    description=f"外部キー{fk_name}の参照先カラムを修正",
                    fix_content=fix_content,
                    file_path="",
                    backup_required=True,
                    critical=True
                ))
        
        return suggestions
    
    def _generate_constraint_fixes(
        self,
        result: CheckResult,
        fix_context: FixContext,
        fix_types: List[FixType]
    ) -> List[FixSuggestion]:
        """制約整合性チェックの修正提案を生成"""
        suggestions = []
        
        issue_type = result.details.get('issue_type', '')
        
        if 'missing_primary_key' in issue_type:
            # PRIMARY KEY制約の修正提案
            missing_columns = result.details.get('missing_columns', [])
            
            if 'in_ddl' in issue_type:
                target_file = "DDL"
                fix_type = FixType.DDL
            else:
                target_file = "YAML"
                fix_type = FixType.YAML
            
            fix_content = f"""
## PRIMARY KEY制約修正提案

{target_file}ファイルにPRIMARY KEYカラムが不足しています。

### 不足しているカラム：
{chr(10).join(f'- {col}' for col in missing_columns)}

### 修正手順：

#### {target_file}ファイルの修正：
"""
            
            if fix_type == FixType.DDL:
                fix_content += f"""
```sql
-- PRIMARY KEY制約を追加
ALTER TABLE {result.table_name} ADD PRIMARY KEY ({', '.join(missing_columns)});
```
"""
            else:
                fix_content += f"""
```yaml
columns:
{chr(10).join(f'  - name: {col}' for col in missing_columns)}
{chr(10).join(f'    primary_key: true' for col in missing_columns)}
```
"""
            
            suggestions.append(FixSuggestion(
                fix_type=fix_type,
                table_name=result.table_name,
                description=f"PRIMARY KEY制約を{target_file}に追加",
                fix_content=fix_content,
                file_path="",
                backup_required=True,
                critical=True
            ))
        
        return suggestions
    
    def _generate_data_type_fixes(
        self,
        result: CheckResult,
        fix_context: FixContext,
        fix_types: List[FixType]
    ) -> List[FixSuggestion]:
        """データ型整合性チェックの修正提案を生成"""
        suggestions = []
        
        # データ型の不一致に対する修正提案
        if "データ型が一致しません" in result.message:
            # メッセージからデータ型情報を抽出（簡易実装）
            fix_content = f"""
## データ型整合性修正提案

カラムのデータ型が一致していません。

### 修正手順：
1. DDLファイルとYAMLファイルのデータ型定義を確認
2. より制限の厳しい方（通常はYAML）に合わせて統一
3. 必要に応じてデータ移行を実施

### 注意事項：
- データ型変更は既存データに影響する可能性があります
- 本番環境での変更前に十分なテストを実施してください
"""
            
            suggestions.append(FixSuggestion(
                fix_type=FixType.ALL,
                table_name=result.table_name,
                description="データ型の整合性を修正",
                fix_content=fix_content,
                file_path="",
                backup_required=True,
                critical=False
            ))
        
        return suggestions
    
    def _generate_yaml_format_fixes(
        self,
        result: CheckResult,
        fix_context: FixContext,
        fix_types: List[FixType]
    ) -> List[FixSuggestion]:
        """YAMLフォーマット整合性チェックの修正提案を生成"""
        suggestions = []
        
        if FixType.ALL in fix_types or FixType.YAML in fix_types:
            fix_content = f"""
## YAMLフォーマット修正提案

YAMLファイルのフォーマットに問題があります。

### 修正手順：
1. YAMLファイルの構文を確認
2. 必須フィールドが存在することを確認
3. データ型と制約の妥当性を検証

### 標準テンプレートに準拠してください：
- table_name: 必須
- description: 必須
- columns: 必須（配列形式）
- indexes: オプション
- foreign_keys: オプション
- constraints: オプション
"""
            
            suggestions.append(FixSuggestion(
                fix_type=FixType.YAML,
                table_name=result.table_name,
                description="YAMLフォーマットを修正",
                fix_content=fix_content,
                file_path="",
                backup_required=True,
                critical=False
            ))
        
        return suggestions
    
    def _guess_table_category(self, table_name: str) -> str:
        """テーブル名からカテゴリを推測"""
        if table_name.startswith('MST_'):
            return 'マスタ'
        elif table_name.startswith('TRN_'):
            return 'トランザクション'
        elif table_name.startswith('SYS_'):
            return 'システム'
        elif table_name.startswith('LOG_'):
            return 'ログ'
        else:
            return 'その他'
    
    def _generate_table_description(self, table_name: str) -> str:
        """テーブル名から説明を生成"""
        # 簡易的な説明生成（実際の実装では、より詳細なロジックが必要）
        if table_name.startswith('MST_'):
            base_name = table_name[4:]  # MST_を除去
            return f"{base_name}マスタ"
        elif table_name.startswith('TRN_'):
            base_name = table_name[4:]  # TRN_を除去
            return f"{base_name}トランザクション"
        else:
            return f"{table_name}テーブル"
    
    def _suggest_reference_column(self, target_table: str, missing_column: str, available_columns: List[str]) -> str:
        """適切な参照先カラムを推測"""
        # 一般的なパターンに基づく推測
        common_id_patterns = [
            f"{target_table.lower()}_id",
            "id",
            f"{target_table[4:].lower()}_id" if target_table.startswith('MST_') else f"{target_table.lower()}_id"
        ]
        
        for pattern in common_id_patterns:
            if pattern in available_columns:
                return pattern
        
        # IDで終わるカラムを探す
        id_columns = [col for col in available_columns if col.endswith('_id') or col == 'id']
        if id_columns:
            return id_columns[0]
        
        # 最初の利用可能なカラムを返す
        return available_columns[0] if available_columns else 'id'
    
    def _deduplicate_suggestions(self, suggestions: List[FixSuggestion]) -> List[FixSuggestion]:
        """重複する修正提案を除去"""
        seen = set()
        unique_suggestions = []
        
        for suggestion in suggestions:
            # ユニークキーを生成（テーブル名、修正タイプ、説明の組み合わせ）
            key = (suggestion.table_name, suggestion.fix_type, suggestion.description)
            if key not in seen:
                seen.add(key)
                unique_suggestions.append(suggestion)
        
        return unique_suggestions
    
    def _sort_suggestions_by_priority(self, suggestions: List[FixSuggestion]) -> List[FixSuggestion]:
        """修正提案を優先度順にソート"""
        def priority_key(suggestion: FixSuggestion) -> Tuple[int, int, str]:
            # 優先度: (critical, fix_type_priority, table_name)
            critical_priority = 0 if suggestion.critical else 1
            
            fix_type_priority = {
                FixType.DDL: 1,
                FixType.YAML: 2,
                FixType.INSERT: 3,
                FixType.ALL: 4
            }.get(suggestion.fix_type, 5)
            
            return (critical_priority, fix_type_priority, suggestion.table_name)
        
        return sorted(suggestions, key=priority_key)
    
    def generate_fix_summary(self, suggestions: List[FixSuggestion]) -> str:
        """修正提案のサマリーを生成"""
        if not suggestions:
            return "修正提案はありません。"
        
        summary = f"## 修正提案サマリー\n\n"
        summary += f"総修正提案数: {len(suggestions)}\n\n"
        
        # 修正タイプ別の統計
        type_counts = {}
        critical_count = 0
        
        for suggestion in suggestions:
            fix_type = suggestion.fix_type.value
            type_counts[fix_type] = type_counts.get(fix_type, 0) + 1
            if suggestion.critical:
                critical_count += 1
        
        summary += "### 修正タイプ別統計:\n"
        for fix_type, count in type_counts.items():
            summary += f"- {fix_type}: {count}件\n"
        
        summary += f"\n### 重要度:\n"
        summary += f"- 重要: {critical_count}件\n"
        summary += f"- 通常: {len(suggestions) - critical_count}件\n"
        
        return summary
