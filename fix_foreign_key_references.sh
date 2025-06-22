#!/bin/bash

# 外部キー参照の修正スクリプト
# MST_Employeeテーブルの参照を統一

echo "外部キー参照の修正を開始..."

# TRN_SkillRecord_details.yamlの修正
file="docs/design/database/table-details/TRN_SkillRecord_details.yaml"
if [ -f "$file" ]; then
    echo "修正中: $file"
    
    # バックアップ作成
    cp "$file" "$file.bak"
    
    # MST_Employeeテーブルへの外部キー参照でemp_idをidに修正
    sed -i 's/- emp_id/- id/g' "$file"
    
    echo "完了: $file"
else
    echo "ファイルが見つかりません: $file"
fi

# 他のファイルも同様に修正
other_files=(
    "docs/design/database/table-details/HIS_AuditLog_details.yaml"
    "docs/design/database/table-details/TRN_Notification_details.yaml"
    "docs/design/database/table-details/SYS_SystemLog_details.yaml"
)

for file in "${other_files[@]}"; do
    if [ -f "$file" ]; then
        echo "修正中: $file"
        
        # バックアップ作成
        cp "$file" "$file.bak"
        
        # MST_Employeeテーブルへの外部キー参照でemp_idをidに修正
        sed -i 's/- emp_id/- id/g' "$file"
        
        echo "完了: $file"
    else
        echo "ファイルが見つかりません: $file"
    fi
done

echo "外部キー参照の修正が完了しました。"
echo "バックアップファイル（.bak）が作成されています。"
