"""
Markdown統一ジェネレーター

YAMLデータからMarkdown形式のテーブル定義書を生成
"""

from typing import Dict, Any, List
from datetime import datetime

from .base_generator import BaseGenerator
from ..core import ValidationResult, GenerationError


class MarkdownGenerator(BaseGenerator):
    """Markdown専用ジェネレーター"""
    
    def __init__(self):
        super().__init__("markdown")
    
    def get_supported_formats(self) -> List[str]:
        """サポートする出力形式"""
        return ['md', 'markdown']
    
    def generate(self, data: Dict[str, Any], output_path: str, **kwargs) -> bool:
        """
        YAMLデータからMarkdownファイルを生成
        
        Args:
            data: YAML解析データ
            output_path: 出力ファイルパス
            **kwargs: 追加オプション
                - include_sample_data: サンプルデータ含有フラグ
                - include_revision_history: 改版履歴含有フラグ
                - table_style: テーブルスタイル ('standard', 'compact')
                
        Returns:
            生成成功フラグ
            
        Raises:
            GenerationError: 生成エラー
        """
        # データ検証
        validation_result = self.validate_data(data)
        if not validation_result.is_valid:
            raise GenerationError(f"データ検証エラー: {validation_result.get_error_summary()}")
        
        # 出力パス検証
        self._validate_output_path(output_path)
        self._validate_file_writable(output_path)
        
        # オプション取得
        include_sample_data = kwargs.get('include_sample_data', True)
        include_revision_history = kwargs.get('include_revision_history', True)
        table_style = kwargs.get('table_style', 'standard')
        
        try:
            # Markdown生成
            markdown_content = self._generate_markdown(
                data, include_sample_data, include_revision_history, table_style
            )
            
            # バックアップ作成
            self._backup_existing_file(output_path)
            
            # ファイル書き込み
            self._write_file(output_path, markdown_content)
            
            self.logger.info(f"Markdownファイルを生成: {output_path}")
            return True
            
        except Exception as e:
            if isinstance(e, GenerationError):
                raise
            raise GenerationError(f"Markdown生成エラー: {str(e)}")
    
    def validate_data(self, data: Dict[str, Any]) -> ValidationResult:
        """
        生成用データの妥当性を検証
        
        Args:
            data: 検証対象データ
            
        Returns:
            検証結果
        """
        result = ValidationResult(is_valid=True)
        
        # 必須フィールドの検証
        required_fields = ['table_name', 'logical_name', 'columns']
        for field in required_fields:
            if field not in data:
                result.add_error(f"必須フィールドが不足: {field}")
        
        # テーブル名の検証
        table_name = data.get('table_name', '')
        if not table_name:
            result.add_error("テーブル名が空です")
        
        # 論理名の検証
        logical_name = data.get('logical_name', '')
        if not logical_name:
            result.add_error("論理名が空です")
        
        # カラム定義の検証
        columns = data.get('columns', [])
        if not isinstance(columns, list):
            result.add_error("カラム定義はリスト形式である必要があります")
        elif len(columns) == 0:
            result.add_error("最低1つのカラム定義が必要です")
        else:
            self._validate_columns(columns, result)
        
        # 必須セクションの検証（🔴 絶対省略禁止）
        self._validate_required_sections(data, result)
        
        return result
    
    def _generate_markdown(self, data: Dict[str, Any], include_sample_data: bool, 
                          include_revision_history: bool, table_style: str) -> str:
        """Markdown文書を生成"""
        
        sections = []
        
        # ヘッダー
        sections.append(self._generate_header(data))
        
        # 改版履歴
        if include_revision_history and data.get('revision_history'):
            sections.append(self._generate_revision_history(data))
        
        # テーブル概要
        sections.append(self._generate_overview(data))
        
        # カラム定義
        sections.append(self._generate_column_definitions(data, table_style))
        
        # インデックス定義
        if data.get('indexes'):
            sections.append(self._generate_index_definitions(data))
        
        # 外部キー制約
        if data.get('foreign_keys'):
            sections.append(self._generate_foreign_key_definitions(data))
        
        # 特記事項
        sections.append(self._generate_notes(data))
        
        # 業務ルール
        sections.append(self._generate_business_rules(data))
        
        # サンプルデータ
        if include_sample_data and data.get('sample_data'):
            sections.append(self._generate_sample_data(data))
        
        return "\n\n".join(sections) + "\n"
    
    def _generate_header(self, data: Dict[str, Any]) -> str:
        """ヘッダーセクションを生成"""
        table_name = data.get('table_name', '')
        logical_name = data.get('logical_name', '')
        category = data.get('category', '')
        priority = data.get('priority', '')
        requirement_id = data.get('requirement_id', '')
        comment = data.get('comment', '')
        
        header = f"""# テーブル定義書: {table_name}

## 基本情報

| 項目 | 内容 |
|------|------|
| **テーブル名** | `{table_name}` |
| **論理名** | {logical_name} |
| **カテゴリ** | {category} |
| **優先度** | {priority} |
| **要求仕様ID** | {requirement_id} |
| **説明** | {comment} |
| **生成日時** | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |"""
        
        return header
    
    def _generate_revision_history(self, data: Dict[str, Any]) -> str:
        """改版履歴セクションを生成"""
        revision_history = data.get('revision_history', [])
        
        section = "## 改版履歴\n\n"
        section += "| バージョン | 日付 | 作成者 | 変更内容 |\n"
        section += "|------------|------|--------|----------|\n"
        
        for revision in revision_history:
            version = revision.get('version', '')
            date = revision.get('date', '')
            author = revision.get('author', '')
            changes = revision.get('changes', '')
            section += f"| {version} | {date} | {author} | {changes} |\n"
        
        return section
    
    def _generate_overview(self, data: Dict[str, Any]) -> str:
        """概要セクションを生成"""
        overview = data.get('overview', '')
        
        section = "## テーブル概要\n\n"
        if overview:
            # 複数行の場合は適切にフォーマット
            formatted_overview = overview.strip()
            if '\n' in formatted_overview:
                section += formatted_overview
            else:
                section += formatted_overview
        else:
            section += "（概要が設定されていません）"
        
        return section
    
    def _generate_column_definitions(self, data: Dict[str, Any], table_style: str) -> str:
        """カラム定義セクションを生成"""
        columns = data.get('columns', [])
        
        section = "## カラム定義\n\n"
        
        if table_style == 'compact':
            # コンパクトスタイル
            section += "| カラム名 | 型 | NULL | PK | UK | デフォルト | 説明 |\n"
            section += "|----------|----|----|----|----|------------|------|\n"
            
            for column in columns:
                name = column.get('name', '')
                data_type = column.get('type', '')
                nullable = "○" if column.get('nullable', True) else "×"
                pk = "○" if column.get('primary_key', False) else ""
                unique = "○" if column.get('unique', False) else ""
                default = column.get('default', '')
                comment = column.get('comment', '')
                
                section += f"| `{name}` | {data_type} | {nullable} | {pk} | {unique} | {default} | {comment} |\n"
        else:
            # 標準スタイル
            section += "| カラム名 | データ型 | NULL許可 | 主キー | 一意制約 | デフォルト値 | 説明 | 要求仕様ID |\n"
            section += "|----------|----------|----------|--------|----------|--------------|------|------------|\n"
            
            for column in columns:
                name = column.get('name', '')
                data_type = column.get('type', '')
                nullable = "○" if column.get('nullable', True) else "×"
                pk = "○" if column.get('primary_key', False) else ""
                unique = "○" if column.get('unique', False) else ""
                default = column.get('default', '')
                comment = column.get('comment', '')
                requirement_id = column.get('requirement_id', '')
                
                section += f"| `{name}` | {data_type} | {nullable} | {pk} | {unique} | {default} | {comment} | {requirement_id} |\n"
        
        return section
    
    def _generate_index_definitions(self, data: Dict[str, Any]) -> str:
        """インデックス定義セクションを生成"""
        indexes = data.get('indexes', [])
        
        section = "## インデックス定義\n\n"
        section += "| インデックス名 | 対象カラム | 一意制約 | 説明 |\n"
        section += "|----------------|------------|----------|------|\n"
        
        for index in indexes:
            name = index.get('name', '')
            columns = ', '.join(index.get('columns', []))
            unique = "○" if index.get('unique', False) else ""
            comment = index.get('comment', '')
            
            section += f"| `{name}` | {columns} | {unique} | {comment} |\n"
        
        return section
    
    def _generate_foreign_key_definitions(self, data: Dict[str, Any]) -> str:
        """外部キー制約セクションを生成"""
        foreign_keys = data.get('foreign_keys', [])
        
        section = "## 外部キー制約\n\n"
        section += "| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |\n"
        section += "|--------|--------|--------------|------------|--------|--------|------|\n"
        
        for fk in foreign_keys:
            name = fk.get('name', '')
            columns = ', '.join(fk.get('columns', []))
            ref_table = fk.get('references', {}).get('table', '')
            ref_columns = ', '.join(fk.get('references', {}).get('columns', []))
            on_update = fk.get('on_update', 'RESTRICT')
            on_delete = fk.get('on_delete', 'RESTRICT')
            comment = fk.get('comment', '')
            
            section += f"| `{name}` | {columns} | {ref_table} | {ref_columns} | {on_update} | {on_delete} | {comment} |\n"
        
        return section
    
    def _generate_notes(self, data: Dict[str, Any]) -> str:
        """特記事項セクションを生成"""
        notes = data.get('notes', [])
        
        section = "## 特記事項\n\n"
        if notes:
            for i, note in enumerate(notes, 1):
                section += f"{i}. {note}\n"
        else:
            section += "（特記事項はありません）"
        
        return section
    
    def _generate_business_rules(self, data: Dict[str, Any]) -> str:
        """業務ルールセクションを生成"""
        rules = data.get('rules', [])
        
        section = "## 業務ルール\n\n"
        if rules:
            for i, rule in enumerate(rules, 1):
                section += f"{i}. {rule}\n"
        else:
            section += "（業務ルールはありません）"
        
        return section
    
    def _generate_sample_data(self, data: Dict[str, Any]) -> str:
        """サンプルデータセクションを生成"""
        sample_data = data.get('sample_data', [])
        columns = data.get('columns', [])
        
        section = "## サンプルデータ\n\n"
        
        if not sample_data:
            section += "（サンプルデータはありません）"
            return section
        
        # ヘッダー行を生成
        column_names = [col['name'] for col in columns]
        header = "| " + " | ".join(column_names) + " |\n"
        separator = "|" + "|".join(["-" * (len(name) + 2) for name in column_names]) + "|\n"
        
        section += header + separator
        
        # データ行を生成
        for row in sample_data:
            values = []
            for col_name in column_names:
                value = row.get(col_name, '')
                if isinstance(value, str):
                    values.append(f"`{value}`")
                else:
                    values.append(str(value))
            
            section += "| " + " | ".join(values) + " |\n"
        
        return section
    
    def _validate_columns(self, columns: List[Dict[str, Any]], result: ValidationResult) -> None:
        """カラム定義の検証"""
        for i, column in enumerate(columns):
            if not isinstance(column, dict):
                result.add_error(f"カラム[{i}]は辞書形式である必要があります")
                continue
            
            # 必須フィールドの検証
            required_fields = ['name', 'type', 'comment']
            for field in required_fields:
                if field not in column:
                    result.add_error(f"カラム[{i}]に必須フィールド '{field}' がありません")
            
            # カラム名の検証
            column_name = column.get('name', '')
            if not column_name:
                result.add_error(f"カラム[{i}]の名前が空です")
    
    def _validate_required_sections(self, data: Dict[str, Any], result: ValidationResult) -> None:
        """必須セクションの検証（🔴 絶対省略禁止）"""
        
        # revision_history の検証
        revision_history = data.get('revision_history', [])
        if not revision_history:
            result.add_error("🔴 必須セクション 'revision_history' が存在しません")
        elif not isinstance(revision_history, list) or len(revision_history) == 0:
            result.add_error("🔴 'revision_history' は最低1エントリが必要です")
        
        # overview の検証
        overview = data.get('overview', '')
        if not overview:
            result.add_error("🔴 必須セクション 'overview' が存在しません")
        elif len(overview.strip()) < 50:
            result.add_error(f"🔴 'overview' は最低50文字以上の説明が必要です (現在: {len(overview.strip())}文字)")
        
        # notes の検証
        notes = data.get('notes', [])
        if not notes:
            result.add_error("🔴 必須セクション 'notes' が存在しません")
        elif not isinstance(notes, list) or len(notes) < 3:
            result.add_error("🔴 'notes' は最低3項目が必要です")
        
        # rules の検証
        rules = data.get('rules', [])
        if not rules:
            result.add_error("🔴 必須セクション 'rules' が存在しません")
        elif not isinstance(rules, list) or len(rules) < 3:
            result.add_error("🔴 'rules' は最低3項目が必要です")
    
    def get_output_filename(self, data: Dict[str, Any], format_type: str) -> str:
        """出力ファイル名を生成"""
        table_name = data.get('table_name', 'unknown')
        logical_name = data.get('logical_name', '')
        
        if logical_name:
            return f"テーブル定義書_{table_name}_{logical_name}.md"
        else:
            return f"テーブル定義書_{table_name}.md"
