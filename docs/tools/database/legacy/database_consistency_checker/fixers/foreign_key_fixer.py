"""
外部キー修正機能
外部キー整合性エラーの修正提案を生成する
"""
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
import re

from core.models import CheckResult, CheckSeverity, FixSuggestion, FixType
from core.logger import ConsistencyLogger


class ForeignKeyFixer:
    """外部キー修正機能"""
    
    def __init__(self, logger: Optional[ConsistencyLogger] = None):
        self.logger = logger or ConsistencyLogger()
    
    def generate_foreign_key_fixes(
        self,
        check_results: List[CheckResult],
        ddl_dir: Path,
        yaml_details_dir: Path
    ) -> List[FixSuggestion]:
        """外部キー整合性エラーの修正提案を生成"""
        suggestions = []
        
        # 外部キーエラーを分類
        fk_errors = self._classify_foreign_key_errors(check_results)
        
        # 各エラータイプに対する修正提案を生成
        for error_type, errors in fk_errors.items():
            if error_type == "missing_target_column":
                suggestions.extend(self._generate_missing_column_fixes(errors, ddl_dir, yaml_details_dir))
            elif error_type == "cascade_mismatch":
                suggestions.extend(self._generate_cascade_mismatch_fixes(errors, ddl_dir, yaml_details_dir))
            elif error_type == "missing_foreign_key":
                suggestions.extend(self._generate_missing_fk_fixes(errors, ddl_dir, yaml_details_dir))
        
        return suggestions
    
    def _classify_foreign_key_errors(self, check_results: List[CheckResult]) -> Dict[str, List[CheckResult]]:
        """外部キーエラーを分類"""
        classified_errors = {
            "missing_target_column": [],
            "cascade_mismatch": [],
            "missing_foreign_key": [],
            "other": []
        }
        
        for result in check_results:
            if result.check_name == "foreign_key_consistency" and result.severity in [CheckSeverity.ERROR, CheckSeverity.WARNING]:
                issue_type = result.details.get('issue_type', '')
                
                if 'missing_target_column' in issue_type:
                    classified_errors["missing_target_column"].append(result)
                elif 'on_update_mismatch' in issue_type or 'on_delete_mismatch' in issue_type:
                    classified_errors["cascade_mismatch"].append(result)
                elif 'missing' in issue_type and 'foreign_key' in issue_type:
                    classified_errors["missing_foreign_key"].append(result)
                else:
                    classified_errors["other"].append(result)
        
        return classified_errors
    
    def _generate_missing_column_fixes(
        self,
        errors: List[CheckResult],
        ddl_dir: Path,
        yaml_details_dir: Path
    ) -> List[FixSuggestion]:
        """参照先カラム不足エラーの修正提案を生成"""
        suggestions = []
        
        for error in errors:
            fk_name = error.details.get('foreign_key_name', 'unknown')
            target_table = error.details.get('target_table', 'unknown')
            target_column = error.details.get('target_column', 'id')
            available_columns = error.details.get('available_columns', [])
            
            # 適切な参照先カラムを推測
            suggested_column = self._suggest_reference_column(target_table, target_column, available_columns)
            
            fix_content = f"""
## 外部キー参照先カラム修正: {fk_name}

### 問題：
外部キー `{fk_name}` の参照先カラム `{target_table}.{target_column}` が存在しません。

### 利用可能なカラム：
{chr(10).join(f'- {col}' for col in available_columns)}

### 推奨修正：
参照先カラムを `{suggested_column}` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- {error.table_name}テーブルから外部キー制約を削除
ALTER TABLE {error.table_name} DROP FOREIGN KEY {fk_name};
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE {error.table_name} 
ADD CONSTRAINT {fk_name}
    FOREIGN KEY (参照元カラム名) 
    REFERENCES {target_table}({suggested_column})
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {error.table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: {fk_name}
    column: 参照元カラム名
    reference_table: {target_table}
    reference_column: {suggested_column}
    on_update: CASCADE
    on_delete: SET NULL
    description: {target_table}への参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください
"""
            
            suggestions.append(FixSuggestion(
                fix_type=FixType.ALL,
                table_name=error.table_name,
                description=f"外部キー{fk_name}の参照先カラムを{suggested_column}に修正",
                fix_content=fix_content,
                file_path="",
                backup_required=True,
                critical=True
            ))
        
        return suggestions
    
    def _generate_cascade_mismatch_fixes(
        self,
        errors: List[CheckResult],
        ddl_dir: Path,
        yaml_details_dir: Path
    ) -> List[FixSuggestion]:
        """カスケード設定不一致エラーの修正提案を生成"""
        suggestions = []
        
        # テーブル別にエラーをグループ化
        errors_by_table = {}
        for error in errors:
            table_name = error.table_name
            if table_name not in errors_by_table:
                errors_by_table[table_name] = []
            errors_by_table[table_name].append(error)
        
        for table_name, table_errors in errors_by_table.items():
            suggestion = self._generate_table_cascade_fix(table_name, table_errors, ddl_dir, yaml_details_dir)
            if suggestion:
                suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_table_cascade_fix(
        self,
        table_name: str,
        errors: List[CheckResult],
        ddl_dir: Path,
        yaml_details_dir: Path
    ) -> Optional[FixSuggestion]:
        """単一テーブルのカスケード設定修正提案を生成"""
        
        fix_content = f"""
## 外部キーカスケード設定統一: {table_name}

### 不一致が検出された外部キー：
"""
        
        ddl_fixes = []
        yaml_fixes = []
        
        for error in errors:
            fk_name = error.details.get('foreign_key_name', 'unknown')
            issue_type = error.details.get('issue_type', '')
            
            if 'on_update_mismatch' in issue_type:
                setting_type = 'ON UPDATE'
                ddl_setting = error.details.get('ddl_on_update', 'RESTRICT')
                yaml_setting = error.details.get('yaml_on_update', 'RESTRICT')
                recommended = error.details.get('recommended_setting', 'CASCADE')
            else:
                setting_type = 'ON DELETE'
                ddl_setting = error.details.get('ddl_on_delete', 'RESTRICT')
                yaml_setting = error.details.get('yaml_on_delete', 'RESTRICT')
                recommended = error.details.get('recommended_setting', 'SET NULL')
            
            fix_content += f"""
#### {fk_name} - {setting_type}設定
- **DDL**: {ddl_setting}
- **YAML**: {yaml_setting}
- **推奨**: {recommended}
"""
            
            ddl_fixes.append({
                'fk_name': fk_name,
                'setting_type': setting_type,
                'recommended': recommended
            })
            
            yaml_fixes.append({
                'fk_name': fk_name,
                'setting_type': setting_type.lower().replace(' ', '_'),
                'recommended': recommended
            })
        
        fix_content += f"""
### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成
"""
        
        for fix in ddl_fixes:
            fix_content += f"""
-- {fix['fk_name']}の修正
ALTER TABLE {table_name} DROP FOREIGN KEY {fix['fk_name']};
ALTER TABLE {table_name} ADD CONSTRAINT {fix['fk_name']}
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
"""
        
        fix_content += """```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
"""
        
        for fix in yaml_fixes:
            fix_content += f"""  - name: {fix['fk_name']}
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
"""
        
        fix_content += """```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください
"""
        
        return FixSuggestion(
            fix_type=FixType.ALL,
            table_name=table_name,
            description=f"{table_name}の外部キーカスケード設定を統一",
            fix_content=fix_content,
            file_path="",
            backup_required=True,
            critical=False
        )
    
    def _generate_missing_fk_fixes(
        self,
        errors: List[CheckResult],
        ddl_dir: Path,
        yaml_details_dir: Path
    ) -> List[FixSuggestion]:
        """外部キー不足エラーの修正提案を生成"""
        suggestions = []
        
        for error in errors:
            issue_type = error.details.get('issue_type', '')
            
            if 'missing_ddl_foreign_key' in issue_type:
                suggestion = self._generate_missing_ddl_fk_fix(error, ddl_dir)
            elif 'missing_yaml_foreign_key' in issue_type:
                suggestion = self._generate_missing_yaml_fk_fix(error, yaml_details_dir)
            else:
                continue
            
            if suggestion:
                suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_missing_ddl_fk_fix(self, error: CheckResult, ddl_dir: Path) -> Optional[FixSuggestion]:
        """DDL外部キー不足の修正提案を生成"""
        source_columns = error.details.get('source_columns', [])
        target_table = error.details.get('target_table', 'unknown')
        target_columns = error.details.get('target_columns', [])
        
        fk_name = f"fk_{error.table_name.lower()}_{source_columns[0] if source_columns else 'unknown'}"
        
        fix_content = f"""
## DDL外部キー追加: {error.table_name}

### 不足している外部キー：
- **参照元カラム**: {', '.join(source_columns)}
- **参照先テーブル**: {target_table}
- **参照先カラム**: {', '.join(target_columns)}

### DDL修正手順：

#### {error.table_name}.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE {error.table_name}
ADD CONSTRAINT {fk_name}
    FOREIGN KEY ({', '.join(source_columns)})
    REFERENCES {target_table}({', '.join(target_columns)})
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください
"""
        
        return FixSuggestion(
            fix_type=FixType.DDL,
            table_name=error.table_name,
            description=f"DDLに外部キー{fk_name}を追加",
            fix_content=fix_content,
            file_path=str(ddl_dir / f"{error.table_name}.sql"),
            backup_required=True,
            critical=True
        )
    
    def _generate_missing_yaml_fk_fix(self, error: CheckResult, yaml_details_dir: Path) -> Optional[FixSuggestion]:
        """YAML外部キー不足の修正提案を生成"""
        source_columns = error.details.get('source_columns', [])
        target_table = error.details.get('target_table', 'unknown')
        target_columns = error.details.get('target_columns', [])
        
        fk_name = f"fk_{error.table_name.lower()}_{source_columns[0] if source_columns else 'unknown'}"
        
        fix_content = f"""
## YAML外部キー追加: {error.table_name}

### 不足している外部キー：
- **参照元カラム**: {', '.join(source_columns)}
- **参照先テーブル**: {target_table}
- **参照先カラム**: {', '.join(target_columns)}

### YAML修正手順：

#### {error.table_name}_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: {fk_name}
    column: {source_columns[0] if source_columns else 'unknown'}
    reference_table: {target_table}
    reference_column: {target_columns[0] if target_columns else 'id'}
    on_update: CASCADE
    on_delete: SET NULL
    description: {target_table}への参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください
"""
        
        return FixSuggestion(
            fix_type=FixType.YAML,
            table_name=error.table_name,
            description=f"YAMLに外部キー{fk_name}を追加",
            fix_content=fix_content,
            file_path=str(yaml_details_dir / f"{error.table_name}_details.yaml"),
            backup_required=True,
            critical=True
        )
    
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
    
    def generate_foreign_key_standards_guide(self) -> str:
        """外部キー設計標準ガイドを生成"""
        guide = """# 外部キー設計標準ガイド

## 命名規則
- 外部キー制約名: `fk_{テーブル名}_{カラム名}`
- 外部キーカラム名: `{参照先テーブル名}_id`

## カスケード設定標準
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

## 例外的なカスケード設定
- **ON DELETE CASCADE**: 親子関係が強い場合（例：注文-注文明細）
- **ON DELETE RESTRICT**: 削除を禁止する場合（例：マスタデータ）

## DDL記述例
```sql
ALTER TABLE TRN_Order
ADD CONSTRAINT fk_trn_order_customer_id
    FOREIGN KEY (customer_id)
    REFERENCES MST_Customer(customer_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

## YAML記述例
```yaml
foreign_keys:
  - name: fk_trn_order_customer_id
    column: customer_id
    reference_table: MST_Customer
    reference_column: customer_id
    on_update: CASCADE
    on_delete: SET NULL
    description: 顧客マスタへの参照
```
"""
        return guide
