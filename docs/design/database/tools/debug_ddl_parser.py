#!/usr/bin/env python3
"""
DDLパーサーのデバッグスクリプト
"""
import sys
from pathlib import Path

# パスを追加
sys.path.append(str(Path(__file__).parent))

from database_consistency_checker.parsers.ddl_parser import EnhancedDDLParser

def debug_ddl_parsing():
    """DDL解析のデバッグ"""
    parser = EnhancedDDLParser()
    ddl_file = Path("../ddl/MST_Skill.sql")
    
    print(f"DDLファイル: {ddl_file}")
    print(f"ファイル存在: {ddl_file.exists()}")
    
    if not ddl_file.exists():
        print("DDLファイルが見つかりません")
        return
    
    # 生のファイル内容を確認
    with open(ddl_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("\n=== CREATE TABLE文の抽出テスト ===")
    import re
    
    # CREATE TABLE文を抽出
    create_table_pattern = r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)\s*\((.*?)\)\s*([^;]*);'
    create_table_match = re.search(create_table_pattern, content, re.IGNORECASE | re.DOTALL)
    
    if create_table_match:
        table_name = create_table_match.group(1)
        columns_section = create_table_match.group(2)
        table_options = create_table_match.group(3)
        
        print(f"テーブル名: {table_name}")
        print(f"カラムセクション長: {len(columns_section)}")
        print(f"テーブルオプション長: {len(table_options)}")
        
        print("\n=== カラムセクション（最初の1000文字）===")
        print(columns_section[:1000])
        print("...")
        
        # カラム分割のテスト
        print("\n=== カラム分割テスト ===")
        column_lines = []
        current_line = ""
        paren_count = 0
        in_quotes = False
        quote_char = None
        
        for i, char in enumerate(columns_section):
            # 引用符の処理
            if char in ["'", '"'] and (i == 0 or columns_section[i-1] != '\\'):
                if not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char:
                    in_quotes = False
                    quote_char = None
            
            current_line += char
            
            if not in_quotes:
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                elif char == ',' and paren_count == 0:
                    line = current_line.strip()[:-1]  # 末尾のカンマを除去
                    if line:
                        column_lines.append(line)
                    current_line = ""
        
        if current_line.strip():
            column_lines.append(current_line.strip())
        
        print(f"分割されたカラム数: {len(column_lines)}")
        for i, line in enumerate(column_lines[:5], 1):  # 最初の5行のみ表示
            print(f"  {i:2d}. {line[:100]}...")
    else:
        print("CREATE TABLE文が見つかりませんでした")
    
    # DDL解析を実行
    ddl_table = parser.parse_ddl_file_detailed(ddl_file)
    
    if ddl_table:
        print(f"\n=== DDL解析結果 ===")
        print(f"テーブル名: {ddl_table.table_name}")
        print(f"カラム数: {len(ddl_table.columns)}")
        print("\nカラム一覧:")
        for i, column in enumerate(ddl_table.columns, 1):
            print(f"  {i:2d}. {column.name} - {column.data_type}")
            if column.length:
                print(f"      長さ: {column.length}")
            if column.enum_values:
                print(f"      ENUM値: {column.enum_values}")
    else:
        print("DDL解析に失敗しました")

if __name__ == "__main__":
    debug_ddl_parsing()
