#!/usr/bin/env python3
"""
SYS_SystemLogテーブルの最終修正
"""

import os
import yaml
from datetime import datetime

def fix_sys_systemlog_final():
    """SYS_SystemLogテーブルの最終修正"""
    file_path = "docs/design/database/table-details/テーブル詳細定義YAML_SYS_SystemLog.yaml"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data or 'columns' not in data:
            return False, "columnsセクションが見つかりません"
        
        columns = data['columns']
        
        # 重複カラムを除去し、正しい順序に並び替え
        # 1. 重複する主キーカラムを除去（systemlog_idを削除）
        # 2. 正しいカラム順序に並び替え
        
        # カラムを辞書形式で管理（重複除去）
        column_dict = {}
        for col in columns:
            col_name = col['name']
            # systemlog_idは重複なので除去
            if col_name == 'systemlog_id':
                continue
            column_dict[col_name] = col
        
        # SYS_SystemLog用の正しいカラム順序
        desired_order = [
            'id', 'tenant_id', 'log_level', 'message', 'component_name',
            'user_id', 'session_id', 'correlation_id', 'error_code', 'stack_trace',
            'request_url', 'request_method', 'request_body', 'response_status',
            'response_body', 'user_agent', 'ip_address', 'log_category',
            'response_time', 'server_name', 'thread_name',
            'is_deleted', 'created_at', 'updated_at'
        ]
        
        # 新しい順序でカラムを再構築
        new_columns = []
        for col_name in desired_order:
            if col_name in column_dict:
                new_columns.append(column_dict[col_name])
        
        # 順序リストにないカラムがあれば末尾に追加（is_deleted, created_at, updated_atより前）
        end_columns = ['is_deleted', 'created_at', 'updated_at']
        other_columns = []
        for col_name, col in column_dict.items():
            if col_name not in desired_order and col_name not in end_columns:
                other_columns.append(col)
        
        # 最終的なカラム順序を構築
        final_columns = []
        
        # 基本カラムを追加
        for col in new_columns:
            if col['name'] not in end_columns:
                final_columns.append(col)
        
        # その他のカラムを追加
        final_columns.extend(other_columns)
        
        # 終了カラムを追加
        for col_name in end_columns:
            if col_name in column_dict:
                final_columns.append(column_dict[col_name])
        
        data['columns'] = final_columns
        
        # バージョン履歴を更新
        if 'revision_history' not in data:
            data['revision_history'] = []
        
        data['revision_history'].append({
            'version': f'FINAL.{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'author': 'SYS_SystemLog最終修正ツール',
            'changes': '重複主キーカラム除去とカラム順序の最終修正'
        })
        
        # ファイルを保存
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        return True, f"SYS_SystemLog最終修正完了（{len(final_columns)}カラム）"
        
    except Exception as e:
        return False, f"エラー: {str(e)}"

def main():
    """メイン処理"""
    print("🔧 SYS_SystemLogテーブルの最終修正を開始...")
    print("=" * 50)
    
    success, result = fix_sys_systemlog_final()
    if success:
        print(f"  ✅ {result}")
    else:
        print(f"  ❌ {result}")
    
    print()
    print("🎉 SYS_SystemLog最終修正完了！")

if __name__ == "__main__":
    main()
