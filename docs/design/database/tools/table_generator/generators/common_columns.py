#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル生成ツール - 共通カラム定義

全テーブルで共通的に使用されるカラム定義を提供します。

対応要求仕様ID: PLT.2-DB.1, PLT.2-TOOL.1
"""

from typing import List, Dict, Any
from shared.core.models import BusinessColumnDefinition


class CommonColumns:
    """共通カラム定義クラス
    
    全テーブルで共通的に使用されるカラム定義を管理します。
    基本カラム、監査カラム、テナントカラムなどを提供します。
    """
    
    @staticmethod
    def get_base_columns() -> List[BusinessColumnDefinition]:
        """基本カラム定義を取得
        
        Returns:
            List[BusinessColumnDefinition]: 基本カラム定義リスト
        """
        return [
            BusinessColumnDefinition(
                name='id',
                data_type='VARCHAR(50)',
                nullable=False,
                primary=True,
                comment='プライマリキー（UUID）'
            ),
            BusinessColumnDefinition(
                name='is_deleted',
                data_type='BOOLEAN',
                nullable=False,
                default=False,
                comment='論理削除フラグ'
            )
        ]
    
    @staticmethod
    def get_audit_columns() -> List[BusinessColumnDefinition]:
        """監査カラム定義を取得
        
        Returns:
            List[BusinessColumnDefinition]: 監査カラム定義リスト
        """
        return [
            BusinessColumnDefinition(
                name='created_by',
                data_type='VARCHAR(50)',
                nullable=False,
                comment='レコード作成者のユーザーID'
            ),
            BusinessColumnDefinition(
                name='updated_by',
                data_type='VARCHAR(50)',
                nullable=False,
                comment='レコード更新者のユーザーID'
            )
        ]
    
    
    @staticmethod
    def get_all_common_columns(table_name: str, include_tenant: bool = True) -> List[BusinessColumnDefinition]:
        """全共通カラムを取得
        
        Args:
            table_name (str): テーブル名
            include_tenant (bool): テナントカラムを含めるかどうか
            
        Returns:
            List[BusinessColumnDefinition]: 全共通カラム定義リスト
        """
        columns = []
        
        # 基本カラム
        columns.extend(CommonColumns.get_base_columns())
        
        # 監査カラム
        columns.extend(CommonColumns.get_audit_columns())
        
        # マスタテーブル固有カラム
        columns.extend(CommonColumns.get_master_table_columns())
        
        return columns
    
    
    @staticmethod
    def get_master_table_columns() -> List[BusinessColumnDefinition]:
        """マスタテーブル固有カラム定義を取得
        
        Returns:
            List[BusinessColumnDefinition]: マスタテーブル固有カラム定義リスト
        """
        return [
            BusinessColumnDefinition(
                name='created_at',
                data_type='TIMESTAMP',
                nullable=False,
                default='CURRENT_TIMESTAMP',
                comment='レコード作成日時'
            ),
            BusinessColumnDefinition(
                name='updated_at',
                data_type='TIMESTAMP',
                nullable=False,
                default='CURRENT_TIMESTAMP',
                comment='レコード更新日時'
            )
        ]
