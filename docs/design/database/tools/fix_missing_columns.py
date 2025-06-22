#!/usr/bin/env python3
"""
不足しているcolumnsセクション修正スクリプト
YAMLファイルにcolumnsセクションを追加する
"""

import os
import yaml
import sys
from pathlib import Path
from typing import Dict, Any, List

def create_default_columns(table_name: str) -> List[Dict[str, Any]]:
    """
    テーブル名に基づいてデフォルトのカラム定義を作成
    
    Args:
        table_name: テーブル名
        
    Returns:
        デフォルトカラム定義のリスト
    """
    # 基本的なカラム定義
    columns = []
    
    # 主キー（テーブル名に基づく）
    if table_name.startswith('MST_'):
        pk_name = table_name.lower().replace('mst_', '') + '_id'
    elif table_name.startswith('TRN_'):
        pk_name = table_name.lower().replace('trn_', '') + '_id'
    elif table_name.startswith('HIS_'):
        pk_name = table_name.lower().replace('his_', '') + '_id'
    elif table_name.startswith('SYS_'):
        pk_name = table_name.lower().replace('sys_', '') + '_id'
    elif table_name.startswith('WRK_'):
        pk_name = table_name.lower().replace('wrk_', '') + '_id'
    else:
        pk_name = 'id'
    
    # 主キーカラム
    columns.append({
        'name': pk_name,
        'type': 'SERIAL',
        'nullable': False,
        'primary_key': True,
        'unique': False,
        'default': None,
        'comment': f'{table_name}の主キー',
        'requirement_id': 'PLT.1-WEB.1'
    })
    
    # テナントIDカラム（マルチテナント対応）
    if not table_name.startswith('SYS_'):
        columns.append({
            'name': 'tenant_id',
            'type': 'VARCHAR(50)',
            'nullable': False,
            'primary_key': False,
            'unique': False,
            'default': None,
            'comment': 'テナントID（マルチテナント対応）',
            'requirement_id': 'TNT.1-MGMT.1'
        })
    
    # 共通カラム
    columns.extend([
        {
            'name': 'created_at',
            'type': 'TIMESTAMP',
            'nullable': False,
            'primary_key': False,
            'unique': False,
            'default': 'CURRENT_TIMESTAMP',
            'comment': '作成日時',
            'requirement_id': 'PLT.1-WEB.1'
        },
        {
            'name': 'updated_at',
            'type': 'TIMESTAMP',
            'nullable': False,
            'primary_key': False,
            'unique': False,
            'default': 'CURRENT_TIMESTAMP',
            'comment': '更新日時',
            'requirement_id': 'PLT.1-WEB.1'
        }
    ])
    
    return columns

def create_default_indexes(table_name: str, columns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    デフォルトのインデックス定義を作成
    
    Args:
        table_name: テーブル名
        columns: カラム定義リスト
        
    Returns:
        インデックス定義のリスト
    """
    indexes = []
    
    # テナントIDのインデックス
    has_tenant_id = any(col['name'] == 'tenant_id' for col in columns)
    if has_tenant_id:
        indexes.append({
            'name': f'idx_{table_name.lower()}_tenant_id',
            'columns': ['tenant_id'],
            'unique': False,
            'comment': 'テナントID検索用インデックス'
        })
    
    return indexes

def fix_yaml_file(file_path: Path) -> bool:
    """
    YAMLファイルのcolumnsセクションを修正する
    
    Args:
        file_path: YAMLファイルのパス
        
    Returns:
        修正が行われた場合True
    """
    try:
        # YAMLファイルを読み込み
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data:
            return False
        
        # テーブル名を取得
        table_name = data.get('table_name', file_path.stem.replace('_details', ''))
        
        modified = False
        
        # columnsセクションが存在しない、または空の場合
        if 'columns' not in data or not data['columns']:
            print(f"🔧 columnsセクションを追加: {file_path.name}")
            data['columns'] = create_default_columns(table_name)
            modified = True
        
        # indexesセクションが存在しない、または空の場合
        if 'indexes' not in data or not data['indexes']:
            print(f"🔧 indexesセクションを追加: {file_path.name}")
            data['indexes'] = create_default_indexes(table_name, data['columns'])
            modified = True
        
        # foreign_keysセクションが存在しない場合
        if 'foreign_keys' not in data:
            print(f"🔧 foreign_keysセクションを追加: {file_path.name}")
            data['foreign_keys'] = []
            modified = True
        
        if modified:
            # ファイルに書き戻し
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            print(f"✅ 修正完了: {file_path.name}")
            return True
        else:
            print(f"ℹ️  修正不要: {file_path.name}")
            return False
            
    except Exception as e:
        print(f"❌ エラー: {file_path.name} - {e}")
        return False

def main():
    """メイン処理"""
    # ベースディレクトリの設定
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent.parent.parent
    yaml_dir = base_dir / "design" / "database" / "table-details"
    
    if not yaml_dir.exists():
        print(f"❌ YAMLディレクトリが見つかりません: {yaml_dir}")
        sys.exit(1)
    
    print("🔧 不足columnsセクション修正スクリプト開始")
    print(f"📁 対象ディレクトリ: {yaml_dir}")
    
    # YAMLファイルを検索
    yaml_files = list(yaml_dir.glob("*_details.yaml"))
    
    if not yaml_files:
        print("❌ YAMLファイルが見つかりません")
        sys.exit(1)
    
    print(f"📄 対象ファイル数: {len(yaml_files)}")
    
    # 各ファイルを処理
    modified_count = 0
    error_count = 0
    
    for yaml_file in sorted(yaml_files):
        try:
            if fix_yaml_file(yaml_file):
                modified_count += 1
        except Exception as e:
            print(f"❌ 処理エラー: {yaml_file.name} - {e}")
            error_count += 1
    
    # 結果表示
    print("\n" + "="*50)
    print("🎯 columnsセクション修正完了")
    print(f"📊 処理結果:")
    print(f"   - 総ファイル数: {len(yaml_files)}")
    print(f"   - 修正ファイル数: {modified_count}")
    print(f"   - エラーファイル数: {error_count}")
    print(f"   - 修正不要ファイル数: {len(yaml_files) - modified_count - error_count}")
    
    if error_count > 0:
        print(f"\n⚠️  {error_count}件のエラーが発生しました")
        sys.exit(1)
    else:
        print("\n✅ 全ての処理が正常に完了しました")

if __name__ == "__main__":
    main()
