"""
Flask Web UIアプリケーション

要求仕様ID: PLT.1-WEB.1, SKL.1-HIER.1
設計書: docs/design/database/08-database-design-guidelines.md
実装内容: データベース設計ツールのWeb UI
"""

import os
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from typing import Dict, Any
import sys
import traceback

# パス設定
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.core.logger import get_logger
from shared.ai.code_generator import AICodeGenerator, GenerationRequest
from database_consistency_checker.main import DatabaseConsistencyChecker
from table_generator.main import TableGenerator

logger = get_logger(__name__)

def create_app(config: Dict[str, Any] = None) -> Flask:
    """Flaskアプリケーション作成
    
    Args:
        config: 設定辞書
        
    Returns:
        Flask: Flaskアプリケーション
    """
    app = Flask(__name__)
    
    # CORS設定
    CORS(app)
    
    # 設定
    app.config.update({
        'SECRET_KEY': 'database-tools-secret-key',
        'DEBUG': True,
        'TEMPLATES_AUTO_RELOAD': True
    })
    
    if config:
        app.config.update(config)
    
    # ツールインスタンス初期化
    app.ai_generator = AICodeGenerator()
    app.consistency_checker = DatabaseConsistencyChecker()
    app.table_generator = TableGenerator()
    
    # ルート登録
    register_routes(app)
    
    return app

def register_routes(app: Flask) -> None:
    """ルート登録
    
    Args:
        app: Flaskアプリケーション
    """
    
    @app.route('/')
    def index():
        """メインページ"""
        return render_template('index.html')
    
    @app.route('/ai-generator')
    def ai_generator():
        """AI生成ページ"""
        return render_template('ai_generator.html')
    
    @app.route('/consistency-checker')
    def consistency_checker():
        """整合性チェックページ"""
        return render_template('consistency_checker.html')
    
    @app.route('/table-generator')
    def table_generator():
        """テーブル生成ページ"""
        return render_template('table_generator.html')
    
    # API エンドポイント
    @app.route('/api/ai/generate', methods=['POST'])
    def api_ai_generate():
        """AI生成API"""
        try:
            data = request.get_json()
            
            if not data or 'description' not in data:
                return jsonify({
                    'success': False,
                    'error': '説明文が必要です'
                }), 400
            
            request_obj = GenerationRequest(
                description=data['description'],
                table_name=data.get('table_name'),
                target_format=data.get('target_format', 'yaml'),
                context=data.get('context')
            )
            
            result = app.ai_generator.generate_from_description(request_obj)
            
            return jsonify({
                'success': result.success,
                'content': result.content,
                'format': result.format,
                'metadata': result.metadata,
                'suggestions': result.suggestions
            })
            
        except Exception as e:
            logger.error(f"AI生成APIエラー: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/consistency/check', methods=['POST'])
    def api_consistency_check():
        """整合性チェックAPI"""
        try:
            data = request.get_json()
            table_name = data.get('table_name') if data else None
            
            # 整合性チェック実行
            result = app.consistency_checker.run_comprehensive_check(table_name)
            
            return jsonify({
                'success': True,
                'result': result
            })
            
        except Exception as e:
            logger.error(f"整合性チェックAPIエラー: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/table/generate', methods=['POST'])
    def api_table_generate():
        """テーブル生成API"""
        try:
            data = request.get_json()
            
            if not data or 'table_name' not in data:
                return jsonify({
                    'success': False,
                    'error': 'テーブル名が必要です'
                }), 400
            
            table_name = data['table_name']
            generate_types = data.get('generate_types', ['yaml', 'ddl', 'markdown'])
            
            # テーブル生成実行
            result = app.table_generator.generate_table_files(table_name, generate_types)
            
            return jsonify({
                'success': True,
                'result': result
            })
            
        except Exception as e:
            logger.error(f"テーブル生成APIエラー: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/tables/list', methods=['GET'])
    def api_tables_list():
        """テーブル一覧API"""
        try:
            # テーブル一覧取得
            tables = app.table_generator.get_table_list()
            
            return jsonify({
                'success': True,
                'tables': tables
            })
            
        except Exception as e:
            logger.error(f"テーブル一覧APIエラー: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/file/download/<file_type>/<table_name>')
    def api_file_download(file_type: str, table_name: str):
        """ファイルダウンロードAPI"""
        try:
            file_path = app.table_generator.get_file_path(table_name, file_type)
            
            if not os.path.exists(file_path):
                return jsonify({
                    'success': False,
                    'error': 'ファイルが見つかりません'
                }), 404
            
            return send_file(file_path, as_attachment=True)
            
        except Exception as e:
            logger.error(f"ファイルダウンロードAPIエラー: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.errorhandler(404)
    def not_found(error):
        """404エラーハンドラ"""
        return render_template('error.html', 
                             error_code=404, 
                             error_message='ページが見つかりません'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """500エラーハンドラ"""
        return render_template('error.html', 
                             error_code=500, 
                             error_message='内部サーバーエラー'), 500

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
