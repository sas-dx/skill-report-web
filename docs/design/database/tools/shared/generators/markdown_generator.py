"""
Markdownジェネレーター
テーブル定義からMarkdown形式のテーブル定義書を生成する機能

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム
"""

from typing import List, Optional
from datetime import datetime

from .base_generator import BaseGenerator
from ..core.models import TableDefinition, ColumnDefinition, IndexDefinition, ForeignKeyDefinition


class MarkdownGenerator(BaseGenerator):
    """Markdownジェネレーター"""
    
    def __init__(self, config=None):
        super().__init__(config)
        self.include_toc = self.config.get('include_toc', True)
        self.include_revision_history = self.config.get('include_revision_history', True)
        self.include_sample_data = self.config.get('include_sample_data', False)
        self.table_style = self.config.get('table_style', 'github')  # github, simple
    
    def generate(self, table_def: TableDefinition, output_path: Optional[str] = None) -> str:
        """
        テーブル定義からMarkdownを生成
        
        Args:
            table_def: テーブル定義オブジェクト
            output_path: 出力ファイルパス（未使用）
            
        Returns:
            str: 生成されたMarkdown
        """
        self._log_generation_start(table_def)
        
        try:
            sections = []
            
            # ヘッダー
            sections.append(self._generate_header(table_def))
            
            # 目次
            if self.include_toc:
                sections.append(self._generate_toc())
            
            # 改訂履歴
            if self.include_revision_history:
                sections.append(self._generate_revision_history())
            
            # テーブル概要
            sections.append(self._generate_table_overview(table_def))
            
            # カラム定義
            sections.append(self._generate_column_definitions(table_def))
            
            # インデックス定義
            if table_def.indexes:
                sections.append(self._generate_index_definitions(table_def))
            
            # 外部キー制約
            if table_def.foreign_keys:
                sections.append(self._generate_foreign_key_definitions(table_def))
            
            # サンプルデータ
            if self.include_sample_data:
                sections.append(self._generate_sample_data_section(table_def))
            
            # 備考
            sections.append(self._generate_notes_section(table_def))
            
            markdown_content = '\n\n'.join(filter(None, sections))
            
            self._log_generation_complete(table_def)
            return markdown_content
            
        except Exception as e:
            raise self._handle_generation_error(e, table_def, "Markdown生成エラー")
    
    def get_file_extension(self) -> str:
        """ファイル拡張子を取得"""
        return '.md'
    
    def _generate_header(self, table_def: TableDefinition) -> str:
        """ヘッダーの生成"""
        logical_name = table_def.logical_name or table_def.name
        
        lines = [
            f"# テーブル定義書_{table_def.name}_{logical_name}",
            "",
            f"**テーブル名**: {table_def.name}  ",
            f"**論理名**: {logical_name}  ",
            f"**カテゴリ**: {table_def.category}  ",
            f"**要求仕様ID**: {table_def.requirement_id}  ",
            f"**作成日**: {datetime.now().strftime('%Y-%m-%d')}  "
        ]
        
        if table_def.comment:
            lines.extend([
                "",
                "## 概要",
                "",
                table_def.comment
            ])
        
        return '\n'.join(lines)
    
    def _generate_toc(self) -> str:
        """目次の生成"""
        lines = [
            "## 目次",
            "",
            "- [改訂履歴](#改訂履歴)",
            "- [テーブル概要](#テーブル概要)",
            "- [カラム定義](#カラム定義)",
            "- [インデックス定義](#インデックス定義)",
            "- [外部キー制約](#外部キー制約)",
            "- [備考](#備考)"
        ]
        
        if self.include_sample_data:
            lines.insert(-1, "- [サンプルデータ](#サンプルデータ)")
        
        return '\n'.join(lines)
    
    def _generate_revision_history(self) -> str:
        """改訂履歴の生成"""
        lines = [
            "## 改訂履歴",
            "",
            "| 版数 | 改訂日 | 改訂者 | 改訂内容 |",
            "|------|--------|--------|----------|",
            f"| 1.0 | {datetime.now().strftime('%Y-%m-%d')} | AI駆動開発チーム | 初版作成 |"
        ]
        
        return '\n'.join(lines)
    
    def _generate_table_overview(self, table_def: TableDefinition) -> str:
        """テーブル概要の生成"""
        lines = [
            "## テーブル概要",
            "",
            "| 項目 | 内容 |",
            "|------|------|",
            f"| テーブル名 | {table_def.name} |",
            f"| 論理名 | {table_def.logical_name or table_def.name} |",
            f"| カテゴリ | {table_def.category} |",
            f"| 要求仕様ID | {table_def.requirement_id} |"
        ]
        
        if table_def.comment:
            lines.append(f"| 説明 | {table_def.comment} |")
        
        # 統計情報
        pk_count = len([col for col in table_def.columns if col.primary_key])
        nullable_count = len([col for col in table_def.columns if col.nullable])
        
        lines.extend([
            f"| カラム数 | {len(table_def.columns)} |",
            f"| プライマリキー数 | {pk_count} |",
            f"| NULL許可カラム数 | {nullable_count} |",
            f"| インデックス数 | {len(table_def.indexes) if table_def.indexes else 0} |",
            f"| 外部キー数 | {len(table_def.foreign_keys) if table_def.foreign_keys else 0} |"
        ])
        
        return '\n'.join(lines)
    
    def _generate_column_definitions(self, table_def: TableDefinition) -> str:
        """カラム定義の生成"""
        lines = [
            "## カラム定義",
            "",
            "| # | カラム名 | データ型 | NULL | デフォルト | PK | UK | 説明 |",
            "|---|----------|----------|------|------------|----|----|------|"
        ]
        
        for i, column in enumerate(table_def.columns, 1):
            row = self._generate_column_row(i, column)
            lines.append(row)
        
        return '\n'.join(lines)
    
    def _generate_column_row(self, index: int, column: ColumnDefinition) -> str:
        """カラム行の生成"""
        # NULL許可
        nullable = "○" if column.nullable else "×"
        
        # デフォルト値
        default = column.default if column.default is not None else "-"
        if isinstance(default, str) and len(default) > 20:
            default = default[:17] + "..."
        
        # プライマリキー
        pk = "○" if column.primary_key else "-"
        
        # ユニークキー
        uk = "○" if column.unique and not column.primary_key else "-"
        
        # 説明
        comment = column.comment or "-"
        if len(comment) > 50:
            comment = comment[:47] + "..."
        
        return f"| {index} | {column.name} | {column.type} | {nullable} | {default} | {pk} | {uk} | {comment} |"
    
    def _generate_index_definitions(self, table_def: TableDefinition) -> str:
        """インデックス定義の生成"""
        lines = [
            "## インデックス定義",
            "",
            "| # | インデックス名 | 種別 | カラム | 説明 |",
            "|---|----------------|------|--------|------|"
        ]
        
        for i, index in enumerate(table_def.indexes, 1):
            row = self._generate_index_row(i, index)
            lines.append(row)
        
        return '\n'.join(lines)
    
    def _generate_index_row(self, index_num: int, index: IndexDefinition) -> str:
        """インデックス行の生成"""
        # 種別
        index_type = "UNIQUE" if index.unique else "INDEX"
        if index.type and index.type != 'btree':
            index_type += f" ({index.type})"
        
        # カラム
        columns = ', '.join(index.columns)
        
        # 説明
        comment = index.comment or "-"
        
        return f"| {index_num} | {index.name} | {index_type} | {columns} | {comment} |"
    
    def _generate_foreign_key_definitions(self, table_def: TableDefinition) -> str:
        """外部キー制約の生成"""
        lines = [
            "## 外部キー制約",
            "",
            "| # | 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |",
            "|---|--------|--------|--------------|------------|--------|--------|------|"
        ]
        
        for i, fk in enumerate(table_def.foreign_keys, 1):
            row = self._generate_foreign_key_row(i, fk)
            lines.append(row)
        
        return '\n'.join(lines)
    
    def _generate_foreign_key_row(self, fk_num: int, fk: ForeignKeyDefinition) -> str:
        """外部キー行の生成"""
        # カラム
        columns = ', '.join(fk.columns)
        
        # 参照カラム
        ref_columns = ', '.join(fk.references_columns)
        
        # アクション
        on_update = fk.on_update or "RESTRICT"
        on_delete = fk.on_delete or "RESTRICT"
        
        # 説明
        comment = fk.comment or "-"
        
        return f"| {fk_num} | {fk.name} | {columns} | {fk.references_table} | {ref_columns} | {on_update} | {on_delete} | {comment} |"
    
    def _generate_sample_data_section(self, table_def: TableDefinition) -> str:
        """サンプルデータセクションの生成"""
        lines = [
            "## サンプルデータ",
            "",
            "```sql",
            f"-- {table_def.name} サンプルデータ",
            f"INSERT INTO {table_def.name} (",
            "    " + ", ".join([col.name for col in table_def.columns]),
            ") VALUES",
            "    -- サンプルデータをここに記載",
            "    ;",
            "```"
        ]
        
        return '\n'.join(lines)
    
    def _generate_notes_section(self, table_def: TableDefinition) -> str:
        """備考セクションの生成"""
        lines = [
            "## 備考",
            "",
            "### 設計上の注意点",
            "",
            "- マルチテナント対応のため、全操作でtenant_idによるフィルタリングが必要",
            "- 論理削除を採用している場合は、is_deletedフラグを考慮すること",
            "- 作成日時・更新日時は自動設定されるため、手動での設定は不要",
            "",
            "### パフォーマンス考慮事項",
            "",
            "- 大量データが想定される場合は、適切なインデックス設計を行うこと",
            "- 検索条件として使用される可能性の高いカラムにはインデックスを設定済み",
            "",
            "### セキュリティ考慮事項",
            "",
            "- 個人情報を含む場合は、暗号化やアクセス制御を適切に実装すること",
            "- 監査証跡が必要な場合は、操作ログの記録を実装すること"
        ]
        
        # テーブル固有の備考があれば追加
        if hasattr(table_def, 'notes') and table_def.notes:
            lines.extend([
                "",
                "### テーブル固有の注意点",
                "",
                table_def.notes
            ])
        
        return '\n'.join(lines)
    
    def _generate_filename(self, table_def: TableDefinition) -> str:
        """ファイル名の生成（オーバーライド）"""
        logical_name = table_def.logical_name or table_def.name
        return f"テーブル定義書_{table_def.name}_{logical_name}.md"


# ジェネレーターファクトリーへの登録
from .base_generator import GeneratorFactory
GeneratorFactory.register_generator('.md', MarkdownGenerator)


# 便利関数
def generate_markdown(table_def: TableDefinition, config=None) -> str:
    """
    テーブル定義からMarkdownを生成する便利関数
    
    Args:
        table_def: テーブル定義オブジェクト
        config: 設定オブジェクト
        
    Returns:
        str: 生成されたMarkdown
    """
    generator = MarkdownGenerator(config)
    return generator.generate(table_def)


def generate_markdown_file(table_def: TableDefinition, output_path: str, config=None) -> None:
    """
    テーブル定義からMarkdownファイルを生成する便利関数
    
    Args:
        table_def: テーブル定義オブジェクト
        output_path: 出力ファイルパス
        config: 設定オブジェクト
    """
    generator = MarkdownGenerator(config)
    generator.generate_to_file(table_def, output_path)
