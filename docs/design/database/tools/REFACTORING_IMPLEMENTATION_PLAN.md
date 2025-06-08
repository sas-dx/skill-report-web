# データベース整合性チェックツール リファクタリング実装計画

## 🎯 Phase 1: アダプター統合（1-2日）

### 1.1 共通アダプター基盤の強化

#### TableDefinitionAdapter の統合
```python
# shared/adapters/table_adapter.py
class TableDefinitionAdapter(BaseAdapter):
    """統合テーブル定義アダプター"""
    
    def __init__(self, config: DatabaseToolsConfig):
        super().__init__(config)
        self.yaml_parser = YamlParser()
        self.ddl_generator = DDLGenerator()
        self.markdown_generator = MarkdownGenerator()
        self.sample_data_generator = SampleDataGenerator()
    
    def load_from_yaml(self, yaml_file: Path) -> TableDefinition:
        """YAMLファイルからテーブル定義読み込み"""
        yaml_data = self.yaml_parser.parse_file(yaml_file)
        return create_table_definition_from_yaml(yaml_data)
    
    def generate_ddl(self, table_def: TableDefinition) -> str:
        """DDL生成"""
        return self.ddl_generator.generate(table_def)
    
    def generate_markdown(self, table_def: TableDefinition) -> str:
        """Markdown生成"""
        return self.markdown_generator.generate(table_def)
    
    def generate_sample_data(self, table_def: TableDefinition) -> str:
        """サンプルデータ生成"""
        return self.sample_data_generator.generate(table_def)
    
    def validate_definition(self, table_def: TableDefinition) -> List[str]:
        """テーブル定義検証"""
        errors = []
        
        # 基本項目チェック
        if not table_def.name:
            errors.append("テーブル名が設定されていません")
        
        if not table_def.logical_name:
            errors.append("論理名が設定されていません")
        
        if not table_def.columns:
            errors.append("カラム定義が存在しません")
        
        # プライマリキーチェック
        primary_keys = [col for col in table_def.columns if col.primary_key]
        if not primary_keys:
            errors.append("プライマリキーが定義されていません")
        
        # カラム名重複チェック
        column_names = [col.name for col in table_def.columns]
        if len(column_names) != len(set(column_names)):
            errors.append("重複するカラム名が存在します")
        
        return errors
```

#### ConsistencyCheckAdapter の統合
```python
# shared/adapters/consistency_adapter.py
class ConsistencyCheckAdapter(BaseAdapter):
    """統合整合性チェックアダプター"""
    
    def __init__(self, config: DatabaseToolsConfig):
        super().__init__(config)
        self.yaml_parser = YamlParser()
        self.ddl_parser = DDLParser()
        self.markdown_parser = MarkdownParser()
        self.issues: List[ConsistencyIssue] = []
    
    def load_all_definitions(self, yaml_dir: Path, ddl_dir: Path, markdown_dir: Path) -> Dict[str, Dict[str, TableDefinition]]:
        """全定義ファイルの読み込み"""
        return {
            'yaml': self.load_yaml_definitions(yaml_dir),
            'ddl': self.load_ddl_definitions(ddl_dir),
            'markdown': self.load_markdown_definitions(markdown_dir)
        }
    
    def compare_definitions(self, source: TableDefinition, target: TableDefinition, source_type: str, target_type: str) -> List[ConsistencyIssue]:
        """定義比較"""
        issues = []
        
        # カラム比較
        source_columns = {col.name: col for col in source.columns}
        target_columns = {col.name: col for col in target.columns}
        
        # カラム存在チェック
        source_only = set(source_columns.keys()) - set(target_columns.keys())
        target_only = set(target_columns.keys()) - set(source_columns.keys())
        
        for col_name in source_only:
            issues.append(ConsistencyIssue(
                check_type=CheckType.COLUMN_CONSISTENCY,
                severity="error",
                table_name=source.name,
                column_name=col_name,
                message=f"{source_type}にのみ存在するカラムです"
            ))
        
        for col_name in target_only:
            issues.append(ConsistencyIssue(
                check_type=CheckType.COLUMN_CONSISTENCY,
                severity="error",
                table_name=target.name,
                column_name=col_name,
                message=f"{target_type}にのみ存在するカラムです"
            ))
        
        # 共通カラムの詳細比較
        common_columns = set(source_columns.keys()) & set(target_columns.keys())
        for col_name in common_columns:
            source_col = source_columns[col_name]
            target_col = target_columns[col_name]
            
            if source_col.type != target_col.type:
                issues.append(ConsistencyIssue(
                    check_type=CheckType.DATA_TYPE_CONSISTENCY,
                    severity="error",
                    table_name=source.name,
                    column_name=col_name,
                    message=f"データ型不一致: {source_type}({source_col.type}) ≠ {target_type}({target_col.type})"
                ))
        
        return issues
    
    def validate_foreign_keys(self, table_def: TableDefinition, all_tables: Dict[str, TableDefinition]) -> List[ConsistencyIssue]:
        """外部キー検証"""
        issues = []
        
        for fk in table_def.foreign_keys:
            ref_table = fk.references.get("table")
            ref_columns = fk.references.get("columns", [])
            
            # 参照先テーブル存在チェック
            if ref_table not in all_tables:
                issues.append(ConsistencyIssue(
                    check_type=CheckType.FOREIGN_KEY_CONSISTENCY,
                    severity="error",
                    table_name=table_def.name,
                    message=f"外部キー {fk.name} の参照先テーブル '{ref_table}' が存在しません"
                ))
                continue
            
            # 参照先カラム存在チェック
            ref_table_def = all_tables[ref_table]
            ref_table_columns = {col.name: col for col in ref_table_def.columns}
            
            for ref_col in ref_columns:
                if ref_col not in ref_table_columns:
                    issues.append(ConsistencyIssue(
                        check_type=CheckType.FOREIGN_KEY_CONSISTENCY,
                        severity="error",
                        table_name=table_def.name,
                        message=f"外部キー {fk.name} の参照先カラム '{ref_table}.{ref_col}' が存在しません"
                    ))
        
        return issues
```

### 1.2 既存アダプターの移行

#### table_generator/core/adapters.py の簡素化
```python
# table_generator/core/adapters.py (リファクタリング後)
from ...shared.adapters.table_adapter import TableDefinitionAdapter
from ...shared.core.models import GenerationResult

class TableGeneratorService:
    """テーブル生成サービス（統合アダプター使用）"""
    
    def __init__(self):
        self.table_adapter = TableDefinitionAdapter(config)
    
    def process_table(self, table_name: str, yaml_dir: Path, output_dirs: Dict[str, Path]) -> GenerationResult:
        """テーブル処理（統合アダプター使用）"""
        try:
            # YAML読み込み
            yaml_file = yaml_dir / f"{table_name}_details.yaml"
            table_def = self.table_adapter.load_from_yaml(yaml_file)
            
            # 検証
            errors = self.table_adapter.validate_definition(table_def)
            if errors:
                result = GenerationResult(table_name=table_name)
                for error in errors:
                    result.add_error(error)
                result.set_failed()
                return result
            
            # ファイル生成
            return self.generate_table_files(table_def, output_dirs)
            
        except Exception as e:
            result = GenerationResult(table_name=table_name)
            result.add_error(str(e))
            result.set_failed()
            return result
    
    def generate_table_files(self, table_def: TableDefinition, output_dirs: Dict[str, Path]) -> GenerationResult:
        """ファイル生成（統合アダプター使用）"""
        result = GenerationResult(table_name=table_def.name)
        
        try:
            # DDL生成
            if 'ddl' in output_dirs:
                ddl_content = self.table_adapter.generate_ddl(table_def)
                ddl_file = output_dirs['ddl'] / f"{table_def.name}.sql"
                ddl_file.parent.mkdir(parents=True, exist_ok=True)
                ddl_file.write_text(ddl_content, encoding='utf-8')
                result.add_generated_file(ddl_file)
            
            # Markdown生成
            if 'tables' in output_dirs:
                markdown_content = self.table_adapter.generate_markdown(table_def)
                markdown_file = output_dirs['tables'] / f"テーブル定義書_{table_def.name}_{table_def.logical_name}.md"
                markdown_file.parent.mkdir(parents=True, exist_ok=True)
                markdown_file.write_text(markdown_content, encoding='utf-8')
                result.add_generated_file(markdown_file)
            
            # サンプルデータ生成
            if 'data' in output_dirs:
                sample_data_content = self.table_adapter.generate_sample_data(table_def)
                sample_data_file = output_dirs['data'] / f"{table_def.name}_sample_data.sql"
                sample_data_file.parent.mkdir(parents=True, exist_ok=True)
                sample_data_file.write_text(sample_data_content, encoding='utf-8')
                result.add_generated_file(sample_data_file)
            
            result.set_success()
            return result
            
        except Exception as e:
            result.add_error(str(e))
            result.set_failed()
            return result
```

#### database_consistency_checker/core/adapters.py の簡素化
```python
# database_consistency_checker/core/adapters.py (リファクタリング後)
from ...shared.adapters.consistency_adapter import ConsistencyCheckAdapter
from ...shared.core.models import CheckResult

class DatabaseConsistencyService:
    """整合性チェックサービス（統合アダプター使用）"""
    
    def __init__(self):
        self.consistency_adapter = ConsistencyCheckAdapter(config)
    
    def run_all_checks(self, yaml_dir: Path, ddl_dir: Path, markdown_dir: Path, 
                      check_types: Optional[List[CheckType]] = None) -> List[CheckResult]:
        """全チェック実行（統合アダプター使用）"""
        results = []
        
        # 全定義読み込み
        all_definitions = self.consistency_adapter.load_all_definitions(yaml_dir, ddl_dir, markdown_dir)
        
        # 各チェック実行
        if CheckType.TABLE_EXISTENCE in (check_types or list(CheckType)):
            result = self.check_table_existence_consistency(all_definitions)
            results.append(result)
        
        if CheckType.COLUMN_CONSISTENCY in (check_types or list(CheckType)):
            result = self.check_column_consistency(all_definitions['yaml'], all_definitions['ddl'])
            results.append(result)
        
        # その他のチェック...
        
        return results
    
    def check_column_consistency(self, yaml_defs: Dict[str, TableDefinition], 
                               ddl_defs: Dict[str, TableDefinition]) -> CheckResult:
        """カラム整合性チェック（統合アダプター使用）"""
        result = CheckResult(check_name="column_consistency")
        
        common_tables = set(yaml_defs.keys()) & set(ddl_defs.keys())
        
        for table_name in common_tables:
            yaml_table = yaml_defs[table_name]
            ddl_table = ddl_defs[table_name]
            
            # 統合アダプターを使用した比較
            issues = self.consistency_adapter.compare_definitions(yaml_table, ddl_table, "YAML", "DDL")
            
            for issue in issues:
                if issue.severity == "error":
                    result.add_error(f"{issue.table_name}.{issue.column_name}: {issue.message}")
                elif issue.severity == "warning":
                    result.add_warning(f"{issue.table_name}.{issue.column_name}: {issue.message}")
        
        if result.errors:
            result.set_failed()
        else:
            result.set_success()
        
        return result
```

## 🔧 Phase 2: チェック機能拡張（2-3日）

### 2.1 高度なチェック機能の追加

#### パフォーマンス影響チェック
```python
# shared/checkers/performance_checker.py
class PerformanceChecker(BaseChecker):
    """パフォーマンス影響チェック"""
    
    def check_index_coverage(self, table_def: TableDefinition) -> PerformanceReport:
        """インデックスカバレッジチェック"""
        report = PerformanceReport(table_name=table_def.name)
        
        # 外部キーカラムのインデックス存在チェック
        fk_columns = set()
        for fk in table_def.foreign_keys:
            fk_columns.update(fk.columns)
        
        indexed_columns = set()
        for idx in table_def.indexes:
            indexed_columns.update(idx.columns)
        
        unindexed_fk_columns = fk_columns - indexed_columns
        if unindexed_fk_columns:
            report.add_warning(f"外部キーカラムにインデックスがありません: {', '.join(unindexed_fk_columns)}")
        
        return report
    
    def check_table_size_estimation(self, table_def: TableDefinition) -> PerformanceReport:
        """テーブルサイズ推定チェック"""
        report = PerformanceReport(table_name=table_def.name)
        
        # カラム数チェック
        if len(table_def.columns) > 50:
            report.add_warning(f"カラム数が多すぎます: {len(table_def.columns)}列")
        
        # VARCHAR長チェック
        for col in table_def.columns:
            if col.type.startswith("VARCHAR"):
                length_match = re.search(r'VARCHAR\((\d+)\)', col.type)
                if length_match:
                    length = int(length_match.group(1))
                    if length > 1000:
                        report.add_warning(f"VARCHAR長が大きすぎます: {col.name}({length})")
        
        return report
```

#### セキュリティ準拠チェック
```python
# shared/checkers/security_checker.py
class SecurityChecker(BaseChecker):
    """セキュリティ準拠チェック"""
    
    def check_sensitive_data_protection(self, table_def: TableDefinition) -> SecurityReport:
        """機密データ保護チェック"""
        report = SecurityReport(table_name=table_def.name)
        
        sensitive_keywords = ["password", "secret", "token", "key", "ssn", "credit_card"]
        
        for col in table_def.columns:
            col_name_lower = col.name.lower()
            for keyword in sensitive_keywords:
                if keyword in col_name_lower:
                    # 暗号化設定チェック
                    if not col.comment or "暗号化" not in col.comment:
                        report.add_error(f"機密データカラム {col.name} に暗号化設定がありません")
        
        return report
    
    def check_audit_trail(self, table_def: TableDefinition) -> SecurityReport:
        """監査証跡チェック"""
        report = SecurityReport(table_name=table_def.name)
        
        required_audit_columns = ["created_at", "updated_at", "created_by", "updated_by"]
        existing_columns = {col.name for col in table_def.columns}
        
        missing_audit_columns = set(required_audit_columns) - existing_columns
        if missing_audit_columns:
            report.add_warning(f"監査証跡カラムが不足しています: {', '.join(missing_audit_columns)}")
        
        return report
```

#### マルチテナント準拠チェック
```python
# shared/checkers/multitenant_checker.py
class MultitenantChecker(BaseChecker):
    """マルチテナント準拠チェック"""
    
    def check_tenant_isolation(self, table_def: TableDefinition) -> MultitenantReport:
        """テナント分離チェック"""
        report = MultitenantReport(table_name=table_def.name)
        
        # tenant_idカラム存在チェック
        tenant_columns = [col for col in table_def.columns if col.name == "tenant_id"]
        if not tenant_columns:
            report.add_error("tenant_idカラムが存在しません")
        else:
            tenant_col = tenant_columns[0]
            
            # NOT NULL制約チェック
            if tenant_col.nullable:
                report.add_error("tenant_idカラムにNOT NULL制約がありません")
            
            # インデックス存在チェック
            tenant_indexed = any("tenant_id" in idx.columns for idx in table_def.indexes)
            if not tenant_indexed:
                report.add_warning("tenant_idカラムにインデックスがありません")
        
        return report
    
    def check_foreign_key_tenant_consistency(self, table_def: TableDefinition, all_tables: Dict[str, TableDefinition]) -> MultitenantReport:
        """外部キーテナント整合性チェック"""
        report = MultitenantReport(table_name=table_def.name)
        
        for fk in table_def.foreign_keys:
            # 複合外部キーでtenant_idが含まれているかチェック
            if "tenant_id" not in fk.columns:
                report.add_error(f"外部キー {fk.name} にtenant_idが含まれていません")
        
        return report
```

### 2.2 レポート機能の強化

#### 複数形式レポーター
```python
# shared/reporters/multi_format_reporter.py
class MultiFormatReporter:
    """複数形式レポーター"""
    
    def __init__(self):
        self.text_reporter = TextReporter()
        self.json_reporter = JsonReporter()
        self.markdown_reporter = MarkdownReporter()
        self.html_reporter = HtmlReporter()
    
    def generate_report(self, results: List[CheckResult], issues: List[ConsistencyIssue], 
                       format_type: str, output_file: Optional[Path] = None) -> str:
        """指定形式でレポート生成"""
        
        if format_type == "text":
            content = self.text_reporter.generate(results, issues)
        elif format_type == "json":
            content = self.json_reporter.generate(results, issues)
        elif format_type == "markdown":
            content = self.markdown_reporter.generate(results, issues)
        elif format_type == "html":
            content = self.html_reporter.generate(results, issues)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
        
        if output_file:
            output_file.write_text(content, encoding='utf-8')
        
        return content
```

#### HTML可視化レポーター
```python
# shared/reporters/html_reporter.py
class HtmlReporter(BaseReporter):
    """HTML可視化レポーター"""
    
    def generate(self, results: List[CheckResult], issues: List[ConsistencyIssue]) -> str:
        """HTML形式レポート生成"""
        
        # サマリー統計
        summary = self.calculate_summary(results, issues)
        
        # チャート用データ
        chart_data = self.prepare_chart_data(results, issues)
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>データベース整合性チェック結果</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .summary { background: #f5f5f5; padding: 15px; border-radius: 5px; }
                .error { color: #d32f2f; }
                .warning { color: #f57c00; }
                .success { color: #388e3c; }
                .chart-container { width: 400px; height: 400px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <h1>データベース整合性チェック結果</h1>
            
            <div class="summary">
                <h2>サマリー</h2>
                <p>総チェック数: {total_checks}</p>
                <p class="success">成功: {passed_checks}</p>
                <p class="error">失敗: {failed_checks}</p>
                <p class="error">エラー: {total_errors}</p>
                <p class="warning">警告: {total_warnings}</p>
            </div>
            
            <div class="chart-container">
                <canvas id="resultsChart"></canvas>
            </div>
            
            <h2>詳細結果</h2>
            {detailed_results}
            
            <script>
                const ctx = document.getElementById('resultsChart').getContext('2d');
                new Chart(ctx, {{
                    type: 'doughnut',
                    data: {chart_data},
                    options: {{
                        responsive: true,
                        plugins: {{
                            title: {{
                                display: true,
                                text: 'チェック結果分布'
                            }}
                        }}
                    }}
                }});
            </script>
        </body>
        </html>
        """.format(
            total_checks=summary['total_checks'],
            passed_checks=summary['passed_checks'],
            failed_checks=summary['failed_checks'],
            total_errors=summary['total_errors'],
            total_warnings=summary['total_warnings'],
            chart_data=json.dumps(chart_data),
            detailed_results=self.generate_detailed_results_html(results, issues)
        )
        
        return html_template
```

## 🧪 Phase 3: テスト体系強化（1-2日）

### 3.1 包括的テストスイート

#### 統合テスト強化
```python
# tests/integration/test_adapter_integration.py
class TestAdapterIntegration:
    """アダプター統合テスト"""
    
    @pytest.fixture
    def sample_table_definitions(self):
        """サンプルテーブル定義"""
        return {
            "MST_Employee": TableDefinition(
                name="MST_Employee",
                logical_name="社員基本情報",
                columns=[
                    ColumnDefinition(name="id", type="VARCHAR(50)", nullable=False, primary_key=True),
                    ColumnDefinition(name="tenant_id", type="VARCHAR(50)", nullable=False),
                    ColumnDefinition(name="emp_no", type="VARCHAR(20)", nullable=False),
                    ColumnDefinition(name="name", type="VARCHAR(100)", nullable=False)
                ],
                indexes=[
                    IndexDefinition(name="idx_employee_tenant", columns=["tenant_id"])
                ],
                foreign_keys=[]
            )
        }
    
    def test_table_adapter_integration(self, sample_table_definitions, tmp_path):
        """テーブルアダプター統合テスト"""
        config = DatabaseToolsConfig()
        adapter = TableDefinitionAdapter(config)
        
        table_def = sample_table_definitions["MST_Employee"]
        
        # DDL生成テスト
        ddl_content = adapter.generate_ddl(table_def)
        assert "CREATE TABLE MST_Employee" in ddl_content
        assert "tenant_id VARCHAR(50) NOT NULL" in ddl_content
        
        # Markdown生成テスト
        markdown_content = adapter.generate_markdown(table_def)
        assert "# MST_Employee (社員基本情報)" in markdown_content
        
        # 検証テスト
        errors = adapter.validate_definition(table_def)
        assert len(errors) == 0
    
    def test_consistency_adapter_integration(self, sample_table_definitions):
        """整合性チェックアダプター統合テスト"""
        config = DatabaseToolsConfig()
        adapter = ConsistencyCheckAdapter(config)
        
        table_def = sample_table_definitions["MST_Employee"]
        
        # 外部キー検証テスト
        issues = adapter.validate_foreign_keys(table_def, sample_table_definitions)
        assert len(issues) == 0  # 外部キーなしなのでエラーなし
        
        # 定義比較テスト
        modified_table = copy.deepcopy(table_def)
        modified_table.columns[0].type = "VARCHAR(100)"  # 型変更
        
        issues = adapter.compare_definitions(table_def, modified_table, "YAML", "DDL")
        assert len(issues) == 1
        assert issues[0].check_type == CheckType.DATA_TYPE_CONSISTENCY
```

#### パフォーマンステスト
```python
# tests/performance/test_large_scale_processing.py
class TestLargeScaleProcessing:
    """大規模処理パフォーマンステスト"""
    
    def test_large_table_processing(self, benchmark):
        """大量テーブル処理性能テスト"""
        
        def process_large_dataset():
            # 100テーブルの処理をシミュレート
            service = TableGeneratorService()
            results = []
            
            for i in range(100):
                table_name = f"TEST_TABLE_{i:03d}"
                # 処理実行
                result = service.process_table(table_name, yaml_dir, output_dirs)
                results.append(result)
            
            return results
        
        # ベンチマーク実行
        results = benchmark(process_large_dataset)
        
        # 性能要件チェック
        assert len(results) == 100
        # 100テーブル処理が30秒以内に完了することを確認
        assert benchmark.stats['mean'] < 30.0
    
    def test_consistency_check_performance(self, benchmark):
        """整合性チェック性能テスト"""
        
        def run_consistency_checks():
            service = DatabaseConsistencyService()
            return service.run_all_checks(yaml_dir, ddl_dir, markdown_dir)
        
        results = benchmark(run_consistency_checks)
        
        # 整合性チェックが10秒以内に完了することを確認
        assert benchmark.stats['mean'] < 10.0
```

## ✨ Phase 4: 新機能追加（2-3日）

### 4.1 インタラクティブモード

#### CLIウィザード
```python
# shared/interactive/cli_wizard.py
class DatabaseToolsWizard:
    """データベースツールウィザード"""
    
    def __init__(self):
        self.console = Console()
    
    def run_table_generation_wizard(self):
        """テーブル生成ウィザード"""
        self.console.print("[bold blue]テーブル生成ウィザード[/bold blue]")
        
        # テーブル名入力
        table_name = Prompt.ask("テーブル名を入力してください")
        
        # 生成オプション選択
        options = [
            "DDLファイルのみ",
            "Markdownファイルのみ", 
            "サンプルデータのみ
