#!/usr/bin/env python3
"""
yaml_format_checker.pyの修正スクリプト
"""
import re

def fix_yaml_checker():
    """yaml_format_checker.pyを修正"""
    file_path = "checkers/yaml_format_checker.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修正パターン
    replacements = [
        (r'CheckStatus\.ERROR', 'CheckSeverity.ERROR'),
        (r'CheckStatus\.WARNING', 'CheckSeverity.WARNING'),
        (r'CheckStatus\.SUCCESS', 'CheckSeverity.SUCCESS'),
        (r'CheckStatus\.INFO', 'CheckSeverity.INFO'),
        (r'check_type="yaml_format_consistency"', 'check_name="yaml_format_consistency"'),
        (r'status=CheckSeverity', 'severity=CheckSeverity'),
        (r'r\.status == CheckSeverity', 'r.severity == CheckSeverity'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("yaml_format_checker.pyを修正しました")

if __name__ == '__main__':
    fix_yaml_checker()
