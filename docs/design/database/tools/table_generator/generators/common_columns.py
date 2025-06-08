#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル生成ツール - 共通カラム定義

全テーブルで共通的に使用されるカラム定義を提供します。

対応要求仕様ID: PLT.2-DB.1, PLT.2-TOOL.1
"""

from typing import List, Dict, Any
from shared.core.models import ColumnDefinition


class CommonColumns:
    """共通カラム定義クラス
    
    全テーブルで共通的に使用されるカラム定義を管理します。
    基本カラム、監査カラム、テナントカラムなどを提供します。
    """
    
    @staticmethod
    def get_base_columns() -> List[ColumnDefinition]:
        """基本カラム定義を取得
        
        Returns:
            List[ColumnDefinition]: 基本カラム定義リスト
        """
        return [
            ColumnDefinition(
                name='id',
                logical='ID',
                data_type='VARCHAR',
                length=50,
                null=False,
                primary=True,
                description='プライマリキー（UUID）',
                data_generation={
                    'type': 'pattern',
                    'pattern': 'uuid',
                    'unique': True
                }
            ),
            ColumnDefinition(
                name='is_deleted',
                logical='削除フラグ',
                data_type='BOOLEAN',
                null=False,
                default=False,
                description='論理削除フラグ',
                data_generation={
                    'type': 'fixed',
                    'fixed_value': False
                }
            )
        ]
    
    @staticmethod
    def get_audit_columns() -> List[ColumnDefinition]:
        """監査カラム定義を取得
        
        Returns:
            List[ColumnDefinition]: 監査カラム定義リスト
        """
        return [
            ColumnDefinition(
                name='created_at',
                logical='作成日時',
                data_type='TIMESTAMP',
                null=False,
                default='CURRENT_TIMESTAMP',
                description='レコード作成日時',
                data_generation={
                    'type': 'faker',
                    'method': 'date_time_between',
                    'start_date': '-1y',
                    'end_date': 'now'
                }
            ),
            ColumnDefinition(
                name='updated_at',
                logical='更新日時',
                data_type='TIMESTAMP',
                null=False,
                default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                description='レコード更新日時',
                data_generation={
                    'type': 'faker',
                    'method': 'date_time_between',
                    'start_date': '-1y',
                    'end_date': 'now'
                }
            ),
            ColumnDefinition(
                name='created_by',
                logical='作成者',
                data_type='VARCHAR',
                length=50,
                null=False,
                description='レコード作成者のユーザーID',
                data_generation={
                    'type': 'reference',
                    'reference_table': 'MST_Employee',
                    'reference_column': 'id'
                }
            ),
            ColumnDefinition(
                name='updated_by',
                logical='更新者',
                data_type='VARCHAR',
                length=50,
                null=False,
                description='レコード更新者のユーザーID',
                data_generation={
                    'type': 'reference',
                    'reference_table': 'MST_Employee',
                    'reference_column': 'id'
                }
            )
        ]
    
    @staticmethod
    def get_tenant_columns() -> List[ColumnDefinition]:
        """テナントカラム定義を取得
        
        Returns:
            List[ColumnDefinition]: テナントカラム定義リスト
        """
        return [
            ColumnDefinition(
                name='tenant_id',
                logical='テナントID',
                data_type='VARCHAR',
                length=50,
                null=False,
                description='マルチテナント識別子',
                data_generation={
                    'type': 'choice',
                    'choices': ['TENANT_001', 'TENANT_002', 'TENANT_003'],
                    'weights': [60, 30, 10]
                }
            )
        ]
    
    @staticmethod
    def get_version_columns() -> List[ColumnDefinition]:
        """バージョン管理カラム定義を取得
        
        Returns:
            List[ColumnDefinition]: バージョン管理カラム定義リスト
        """
        return [
            ColumnDefinition(
                name='version',
                logical='バージョン',
                data_type='INTEGER',
                null=False,
                default=1,
                description='楽観的排他制御用バージョン番号',
                data_generation={
                    'type': 'range',
                    'min_value': 1,
                    'max_value': 5,
                    'distribution': 'normal'
                }
            )
        ]
    
    @staticmethod
    def get_sort_columns() -> List[ColumnDefinition]:
        """ソート用カラム定義を取得
        
        Returns:
            List[ColumnDefinition]: ソート用カラム定義リスト
        """
        return [
            ColumnDefinition(
                name='sort_order',
                logical='ソート順',
                data_type='INTEGER',
                null=True,
                description='表示順序',
                data_generation={
                    'type': 'sequence',
                    'start': 1,
                    'step': 10
                }
            )
        ]
    
    @staticmethod
    def get_status_columns() -> List[ColumnDefinition]:
        """ステータス管理カラム定義を取得
        
        Returns:
            List[ColumnDefinition]: ステータス管理カラム定義リスト
        """
        return [
            ColumnDefinition(
                name='status',
                logical='ステータス',
                data_type='VARCHAR',
                length=20,
                null=False,
                default='ACTIVE',
                description='レコードステータス',
                data_generation={
                    'type': 'choice',
                    'choices': ['ACTIVE', 'INACTIVE', 'PENDING', 'SUSPENDED'],
                    'weights': [70, 15, 10, 5]
                }
            ),
            ColumnDefinition(
                name='is_active',
                logical='有効フラグ',
                data_type='BOOLEAN',
                null=False,
                default=True,
                description='有効/無効フラグ',
                data_generation={
                    'type': 'choice',
                    'choices': [True, False],
                    'weights': [85, 15]
                }
            )
        ]
    
    @staticmethod
    def get_approval_columns() -> List[ColumnDefinition]:
        """承認管理カラム定義を取得
        
        Returns:
            List[ColumnDefinition]: 承認管理カラム定義リスト
        """
        return [
            ColumnDefinition(
                name='approval_status',
                logical='承認ステータス',
                data_type='VARCHAR',
                length=20,
                null=False,
                default='PENDING',
                description='承認ステータス',
                data_generation={
                    'type': 'choice',
                    'choices': ['PENDING', 'APPROVED', 'REJECTED', 'CANCELLED'],
                    'weights': [30, 50, 15, 5]
                }
            ),
            ColumnDefinition(
                name='approved_by',
                logical='承認者',
                data_type='VARCHAR',
                length=50,
                null=True,
                description='承認者のユーザーID',
                data_generation={
                    'type': 'reference',
                    'reference_table': 'MST_Employee',
                    'reference_column': 'id',
                    'nullable_rate': 0.3
                }
            ),
            ColumnDefinition(
                name='approved_at',
                logical='承認日時',
                data_type='TIMESTAMP',
                null=True,
                description='承認日時',
                data_generation={
                    'type': 'faker',
                    'method': 'date_time_between',
                    'start_date': '-6m',
                    'end_date': 'now',
                    'nullable_rate': 0.3
                }
            )
        ]
    
    @staticmethod
    def get_period_columns() -> List[ColumnDefinition]:
        """期間管理カラム定義を取得
        
        Returns:
            List[ColumnDefinition]: 期間管理カラム定義リスト
        """
        return [
            ColumnDefinition(
                name='start_date',
                logical='開始日',
                data_type='DATE',
                null=True,
                description='有効開始日',
                data_generation={
                    'type': 'faker',
                    'method': 'date_between',
                    'start_date': '-1y',
                    'end_date': 'today'
                }
            ),
            ColumnDefinition(
                name='end_date',
                logical='終了日',
                data_type='DATE',
                null=True,
                description='有効終了日',
                data_generation={
                    'type': 'faker',
                    'method': 'date_between',
                    'start_date': 'today',
                    'end_date': '+1y'
                }
            )
        ]
    
    @staticmethod
    def get_all_common_columns(table_name: str, include_tenant: bool = True) -> List[ColumnDefinition]:
        """全共通カラムを取得
        
        Args:
            table_name (str): テーブル名
            include_tenant (bool): テナントカラムを含めるかどうか
            
        Returns:
            List[ColumnDefinition]: 全共通カラム定義リスト
        """
        columns = []
        
        # 基本カラム
        columns.extend(CommonColumns.get_base_columns())
        
        # テナントカラム（システムテーブル以外）
        if include_tenant and not table_name.startswith('SYS_'):
            columns.extend(CommonColumns.get_tenant_columns())
        
        # 監査カラム
        columns.extend(CommonColumns.get_audit_columns())
        
        return columns
    
    @staticmethod
    def get_columns_by_category(category: str) -> List[ColumnDefinition]:
        """カテゴリ別カラム定義を取得
        
        Args:
            category (str): カテゴリ名
            
        Returns:
            List[ColumnDefinition]: カテゴリ別カラム定義リスト
        """
        category_mapping = {
            'base': CommonColumns.get_base_columns,
            'audit': CommonColumns.get_audit_columns,
            'tenant': CommonColumns.get_tenant_columns,
            'version': CommonColumns.get_version_columns,
            'sort': CommonColumns.get_sort_columns,
            'status': CommonColumns.get_status_columns,
            'approval': CommonColumns.get_approval_columns,
            'period': CommonColumns.get_period_columns
        }
        
        if category in category_mapping:
            return category_mapping[category]()
        else:
            return []
    
    @staticmethod
    def get_skill_specific_columns() -> List[ColumnDefinition]:
        """スキル管理システム固有カラム定義を取得
        
        Returns:
            List[ColumnDefinition]: スキル管理システム固有カラム定義リスト
        """
        return [
            ColumnDefinition(
                name='skill_level',
                logical='スキルレベル',
                data_type='INTEGER',
                null=False,
                description='スキルレベル（1:初級、2:中級、3:上級、4:エキスパート）',
                data_generation={
                    'type': 'choice',
                    'choices': [1, 2, 3, 4],
                    'weights': [10, 30, 40, 20]
                }
            ),
            ColumnDefinition(
                name='evaluation_date',
                logical='評価日',
                data_type='DATE',
                null=True,
                description='スキル評価実施日',
                data_generation={
                    'type': 'faker',
                    'method': 'date_between',
                    'start_date': '-1y',
                    'end_date': 'today'
                }
            ),
            ColumnDefinition(
                name='evaluator_id',
                logical='評価者ID',
                data_type='VARCHAR',
                length=50,
                null=True,
                description='評価者のユーザーID',
                data_generation={
                    'type': 'reference',
                    'reference_table': 'MST_Employee',
                    'reference_column': 'id'
                }
            )
        ]
    
    @staticmethod
    def get_project_specific_columns() -> List[ColumnDefinition]:
        """プロジェクト管理システム固有カラム定義を取得
        
        Returns:
            List[ColumnDefinition]: プロジェクト管理システム固有カラム定義リスト
        """
        return [
            ColumnDefinition(
                name='project_code',
                logical='プロジェクトコード',
                data_type='VARCHAR',
                length=20,
                null=False,
                unique=True,
                description='プロジェクト識別コード',
                data_generation={
                    'type': 'pattern',
                    'pattern': 'PRJ{:04d}',
                    'start': 1,
                    'unique': True
                }
            ),
            ColumnDefinition(
                name='priority',
                logical='優先度',
                data_type='INTEGER',
                null=False,
                default=3,
                description='優先度（1:最高、2:高、3:中、4:低、5:最低）',
                data_generation={
                    'type': 'choice',
                    'choices': [1, 2, 3, 4, 5],
                    'weights': [5, 15, 50, 25, 5]
                }
            ),
            ColumnDefinition(
                name='progress_rate',
                logical='進捗率',
                data_type='DECIMAL',
                length=5,  # DECIMAL(5,2) for 0.00-100.00
                null=False,
                default=0.00,
                description='進捗率（%）',
                data_generation={
                    'type': 'range',
                    'min_value': 0.00,
                    'max_value': 100.00,
                    'distribution': 'uniform'
                }
            )
        ]
    
    @staticmethod
    def get_master_table_columns() -> List[ColumnDefinition]:
        """マスタテーブル固有カラム定義を取得
        
        Returns:
            List[ColumnDefinition]: マスタテーブル固有カラム定義リスト
        """
        return [
            ColumnDefinition(
                name='code',
                logical='コード',
                data_type='VARCHAR',
                length=20,
                null=False,
                unique=True,
                description='マスタコード',
                data_generation={
                    'type': 'pattern',
                    'pattern': 'MST{:03d}',
                    'start': 1,
                    'unique': True
                }
            ),
            ColumnDefinition(
                name='name',
                logical='名称',
                data_type='VARCHAR',
                length=100,
                null=False,
                description='マスタ名称',
                data_generation={
                    'type': 'faker',
                    'method': 'word'
                }
            ),
            ColumnDefinition(
                name='description',
                logical='説明',
                data_type='TEXT',
                null=True,
                description='マスタ説明',
                data_generation={
                    'type': 'faker',
                    'method': 'text',
                    'max_nb_chars': 200
                }
            )
        ]
