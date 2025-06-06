"""
テーブル一覧修正機能
テーブル一覧.mdの不足テーブル追加提案を生成する
"""
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
import re

from core.models import CheckResult, CheckSeverity, FixSuggestion, FixType
from core.logger import ConsistencyLogger


class TableListFixer:
    """テーブル一覧修正機能"""
    
    def __init__(self, logger: Optional[ConsistencyLogger] = None):
        self.logger = logger or ConsistencyLogger()
    
    def generate_table_list_fixes(
        self,
        check_results: List[CheckResult],
        table_list_file: Path,
        ddl_dir: Path,
        yaml_details_dir: Path
    ) -> List[FixSuggestion]:
        """テーブル一覧.mdの修正提案を生成"""
        suggestions = []
        
        # テーブル存在エラーから不足テーブルを抽出
        missing_tables = self._extract_missing_tables(check_results)
        
        if not missing_tables:
            return suggestions
        
        # 現在のテーブル一覧を解析
        current_tables = self._parse_current_table_list(table_list_file)
        
        # 各不足テーブルに対する修正提案を生成
        for table_name in missing_tables:
            suggestion = self._generate_table_addition_suggestion(
                table_name, table_list_file, ddl_dir, yaml_details_dir, current_tables
            )
            if suggestion:
                suggestions.append(suggestion)
        
        # 一括修正提案も生成
        if len(missing_tables) > 1:
            batch_suggestion = self._generate_batch_addition_suggestion(
                missing_tables, table_list_file, ddl_dir, yaml_details_dir, current_tables
            )
            if batch_suggestion:
                suggestions.append(batch_suggestion)
        
        return suggestions
    
    def _extract_missing_tables(self, check_results: List[CheckResult]) -> Set[str]:
        """チェック結果から不足テーブルを抽出"""
        missing_tables = set()
        
        for result in check_results:
            if (result.check_name == "table_existence" and 
                result.severity == CheckSeverity.ERROR and
                "テーブル一覧.mdに定義されていません" in result.message):
                missing_tables.add(result.table_name)
        
        return missing_tables
    
    def _parse_current_table_list(self, table_list_file: Path) -> Dict[str, Dict[str, str]]:
        """現在のテーブル一覧.mdを解析"""
        current_tables = {}
        
        if not table_list_file.exists():
            return current_tables
        
        try:
            with open(table_list_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # テーブル定義行を抽出（| テーブル名 | 説明 | カテゴリ | 形式）
            table_pattern = r'\|\s*([A-Z_][A-Z0-9_]*)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|'
            matches = re.findall(table_pattern, content)
            
            for match in matches:
                table_name = match[0].strip()
                description = match[1].strip()
                category = match[2].strip()
                
                current_tables[table_name] = {
                    'description': description,
                    'category': category
                }
        
        except Exception as e:
            self.logger.warning(f"テーブル一覧.mdの解析に失敗: {e}")
        
        return current_tables
    
    def _generate_table_addition_suggestion(
        self,
        table_name: str,
        table_list_file: Path,
        ddl_dir: Path,
        yaml_details_dir: Path,
        current_tables: Dict[str, Dict[str, str]]
    ) -> Optional[FixSuggestion]:
        """単一テーブルの追加提案を生成"""
        
        # テーブル情報を収集
        table_info = self._collect_table_info(table_name, ddl_dir, yaml_details_dir)
        
        # 挿入位置を決定
        insertion_info = self._determine_insertion_position(table_name, table_info, current_tables)
        
        fix_content = f"""
## テーブル一覧.md修正提案: {table_name}

### 追加するテーブル情報：
- **テーブル名**: {table_name}
- **説明**: {table_info['description']}
- **カテゴリ**: {table_info['category']}

### 追加する行：
```markdown
| {table_name} | {table_info['description']} | {table_info['category']} |
```

### 挿入位置：
{insertion_info['position_description']}

### 修正手順：
1. `{table_list_file}` をテキストエディタで開く
2. {insertion_info['section_name']}セクションを見つける
3. {insertion_info['insert_after']}の後に上記の行を挿入
4. ファイルを保存

### 注意事項：
- テーブル名はアルファベット順に並べてください
- 説明は簡潔で分かりやすくしてください
- カテゴリは既存の分類に合わせてください
"""
        
        return FixSuggestion(
            fix_type=FixType.INSERT,
            table_name=table_name,
            description=f"テーブル一覧.mdに{table_name}を追加",
            fix_content=fix_content,
            file_path=str(table_list_file),
            backup_required=True,
            critical=True
        )
    
    def _generate_batch_addition_suggestion(
        self,
        missing_tables: Set[str],
        table_list_file: Path,
        ddl_dir: Path,
        yaml_details_dir: Path,
        current_tables: Dict[str, Dict[str, str]]
    ) -> Optional[FixSuggestion]:
        """複数テーブルの一括追加提案を生成"""
        
        # テーブル情報を収集してカテゴリ別に分類
        tables_by_category = {}
        
        for table_name in sorted(missing_tables):
            table_info = self._collect_table_info(table_name, ddl_dir, yaml_details_dir)
            category = table_info['category']
            
            if category not in tables_by_category:
                tables_by_category[category] = []
            
            tables_by_category[category].append({
                'name': table_name,
                'description': table_info['description']
            })
        
        # 修正内容を生成
        fix_content = f"""
## テーブル一覧.md一括修正提案

### 追加対象テーブル数: {len(missing_tables)}件

"""
        
        for category, tables in tables_by_category.items():
            fix_content += f"""
#### {category}カテゴリ ({len(tables)}件):
```markdown
"""
            for table in tables:
                fix_content += f"| {table['name']} | {table['description']} | {category} |\n"
            
            fix_content += "```\n"
        
        fix_content += f"""
### 一括修正手順：
1. `{table_list_file}` をバックアップ
2. ファイルをテキストエディタで開く
3. 各カテゴリセクションに対応するテーブルを追加
4. アルファベット順に並び替え
5. ファイルを保存

### カテゴリ別挿入ガイド：
"""
        
        for category in tables_by_category.keys():
            fix_content += f"- **{category}**: 既存の{category}テーブルの後に追加\n"
        
        fix_content += """
### 注意事項：
- 必ずバックアップを取ってから作業してください
- テーブル名はアルファベット順に並べてください
- 説明は統一された形式で記載してください
- 不明な点があれば個別に確認してください
"""
        
        return FixSuggestion(
            fix_type=FixType.INSERT,
            table_name="",  # 複数テーブルなので空
            description=f"テーブル一覧.mdに{len(missing_tables)}件のテーブルを一括追加",
            fix_content=fix_content,
            file_path=str(table_list_file),
            backup_required=True,
            critical=True
        )
    
    def _collect_table_info(
        self,
        table_name: str,
        ddl_dir: Path,
        yaml_details_dir: Path
    ) -> Dict[str, str]:
        """テーブル情報を収集"""
        info = {
            'description': self._generate_default_description(table_name),
            'category': self._guess_category(table_name)
        }
        
        # YAMLファイルから情報を取得
        yaml_path = yaml_details_dir / f"{table_name}_details.yaml"
        if yaml_path.exists():
            yaml_info = self._extract_yaml_info(yaml_path)
            if yaml_info:
                info.update(yaml_info)
        
        # DDLファイルから情報を取得
        ddl_path = ddl_dir / f"{table_name}.sql"
        if ddl_path.exists():
            ddl_info = self._extract_ddl_info(ddl_path)
            if ddl_info:
                # YAMLの情報を優先し、不足分をDDLで補完
                for key, value in ddl_info.items():
                    if not info.get(key) or info[key] == self._generate_default_description(table_name):
                        info[key] = value
        
        return info
    
    def _extract_yaml_info(self, yaml_path: Path) -> Optional[Dict[str, str]]:
        """YAMLファイルから情報を抽出"""
        try:
            import yaml
            
            with open(yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            info = {}
            if 'description' in data:
                info['description'] = data['description']
            if 'category' in data:
                info['category'] = data['category']
            
            return info
        
        except Exception as e:
            self.logger.warning(f"YAML情報の抽出に失敗 {yaml_path}: {e}")
            return None
    
    def _extract_ddl_info(self, ddl_path: Path) -> Optional[Dict[str, str]]:
        """DDLファイルから情報を抽出"""
        try:
            with open(ddl_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            info = {}
            
            # COMMENTからテーブル説明を抽出
            comment_pattern = r"COMMENT\s*=\s*['\"]([^'\"]+)['\"]"
            comment_match = re.search(comment_pattern, content, re.IGNORECASE)
            if comment_match:
                info['description'] = comment_match.group(1)
            
            return info
        
        except Exception as e:
            self.logger.warning(f"DDL情報の抽出に失敗 {ddl_path}: {e}")
            return None
    
    def _generate_default_description(self, table_name: str) -> str:
        """デフォルトの説明を生成"""
        if table_name.startswith('MST_'):
            base_name = table_name[4:]  # MST_を除去
            return f"{base_name}マスタ"
        elif table_name.startswith('TRN_'):
            base_name = table_name[4:]  # TRN_を除去
            return f"{base_name}トランザクション"
        elif table_name.startswith('SYS_'):
            base_name = table_name[4:]  # SYS_を除去
            return f"{base_name}システム"
        elif table_name.startswith('LOG_'):
            base_name = table_name[4:]  # LOG_を除去
            return f"{base_name}ログ"
        else:
            return f"{table_name}テーブル"
    
    def _guess_category(self, table_name: str) -> str:
        """テーブル名からカテゴリを推測"""
        if table_name.startswith('MST_'):
            return 'マスタ'
        elif table_name.startswith('TRN_'):
            return 'トランザクション'
        elif table_name.startswith('SYS_'):
            return 'システム'
        elif table_name.startswith('LOG_'):
            return 'ログ'
        elif table_name.startswith('VW_'):
            return 'ビュー'
        else:
            return 'その他'
    
    def _determine_insertion_position(
        self,
        table_name: str,
        table_info: Dict[str, str],
        current_tables: Dict[str, Dict[str, str]]
    ) -> Dict[str, str]:
        """挿入位置を決定"""
        category = table_info['category']
        
        # 同じカテゴリのテーブルを抽出
        same_category_tables = [
            name for name, info in current_tables.items()
            if info['category'] == category
        ]
        
        if not same_category_tables:
            return {
                'position_description': f"{category}セクションの最初",
                'section_name': category,
                'insert_after': f"{category}セクションのヘッダー"
            }
        
        # アルファベット順での挿入位置を決定
        same_category_tables.sort()
        
        insert_after = None
        for existing_table in same_category_tables:
            if existing_table < table_name:
                insert_after = existing_table
            else:
                break
        
        if insert_after:
            return {
                'position_description': f"{category}セクションの{insert_after}の後",
                'section_name': category,
                'insert_after': f"| {insert_after} |"
            }
        else:
            return {
                'position_description': f"{category}セクションの最初",
                'section_name': category,
                'insert_after': f"{category}セクションのヘッダー"
            }
    
    def validate_table_list_format(self, table_list_file: Path) -> List[str]:
        """テーブル一覧.mdのフォーマットを検証"""
        issues = []
        
        if not table_list_file.exists():
            issues.append("テーブル一覧.mdファイルが存在しません")
            return issues
        
        try:
            with open(table_list_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 基本的なフォーマットチェック
            if '| テーブル名 |' not in content:
                issues.append("テーブル定義のヘッダーが見つかりません")
            
            # テーブル定義行の形式チェック
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if line.strip().startswith('|') and 'テーブル名' not in line and '---' not in line:
                    parts = [part.strip() for part in line.split('|')]
                    if len(parts) < 4:  # 空の最初と最後の要素を含めて4つ以上
                        issues.append(f"行{i}: テーブル定義の形式が不正です")
                    elif not re.match(r'^[A-Z_][A-Z0-9_]*$', parts[1]):
                        issues.append(f"行{i}: テーブル名の形式が不正です: {parts[1]}")
        
        except Exception as e:
            issues.append(f"ファイルの読み込みエラー: {e}")
        
        return issues
    
    def generate_table_list_template(self) -> str:
        """テーブル一覧.mdのテンプレートを生成"""
        template = """# テーブル一覧

## マスタテーブル

| テーブル名 | 説明 | カテゴリ |
|-----------|------|----------|

## トランザクションテーブル

| テーブル名 | 説明 | カテゴリ |
|-----------|------|----------|

## システムテーブル

| テーブル名 | 説明 | カテゴリ |
|-----------|------|----------|

## ログテーブル

| テーブル名 | 説明 | カテゴリ |
|-----------|------|----------|

## その他

| テーブル名 | 説明 | カテゴリ |
|-----------|------|----------|
"""
        return template
