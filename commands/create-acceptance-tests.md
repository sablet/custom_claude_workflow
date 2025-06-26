---
allowed-tools: ["Read", "Write", "Grep", "Glob", "Edit"]
description: "受け入れテスト作成：高抽象・低コスト・実行可能なテスト"
---

# 受け入れテスト作成: $ARGUMENTS

## 前提条件

### 入力ドキュメント
実装計画書: @$ARGUMENTS

### 受け入れテスト基準の確認
!find . -name "*acceptance-criteria*" -name "*.md" | head -3

### テスト方針
- **高抽象レベル**: ユーザーの視点からの動作確認
- **低実行コスト**: 高速実行・最小限のセットアップ
- **Red Phase対応**: 最初は失敗し、実装完了で成功するテスト

### 簡素なテスト原則
- **核心機能のみ**: ビジネス価値のある機能のみテスト
- **公開インターフェース重視**: 内部実装ではなく外部仕様をテスト
- **最小モック**: 必要最小限のモックのみ使用
- **保守性優先**: 実装変更時にテスト修正が不要な設計

## 受け入れテスト設計

### 1. Given-When-Then基準の実装

#### 受け入れテスト基準からのテストケース生成
まず定義済みの受け入れテスト基準を参照し、Given-When-Thenシナリオを実装可能なテストコードに変換します。

### 2. メインユースケーステスト

#### 正常系シナリオ
```python
# tests/acceptance/test_main_feature.py
import pytest
from unittest.mock import Mock
from src.api.main_api import MainAPI
from src.models.input_model import InputModel
from src.models.output_model import OutputModel

class TestMainFeatureAcceptance:
    """Main feature acceptance tests"""
    
    @pytest.fixture
    def mock_dependencies(self):
        """Mock dependencies (low cost)"""
        return {
            'repository': Mock(),
            'external_service': Mock(),
            'config': Mock()
        }
    
    @pytest.fixture
    def api_client(self, mock_dependencies):
        """API client setup"""
        return MainAPI(dependencies=mock_dependencies)
    
    def test_main_use_case_success_path(self, api_client):
        """
        Scenario: User executes main feature with valid input
        Expected result: Expected output is obtained
        """
        # Given: Valid input data
        input_data = InputModel(
            field1="valid_value",
            field2=42,
            field3=["item1", "item2"]
        )
        
        # When: Execute main feature
        result = api_client.process_main_feature(input_data)
        
        # Then: Success response obtained (simple validation)
        assert result.status == "success"
        assert result.data is not None  # Only verify that data is returned
    
    def test_main_use_case_with_edge_values(self, api_client):
        """
        Scenario: Input with boundary values
        Expected result: Processed appropriately
        """
        # Given: Boundary value input
        input_data = InputModel(
            field1="",  # Minimum value
            field2=0,   # Boundary value
            field3=[]   # Empty list
        )
        
        # When: Feature execution
        result = api_client.process_main_feature(input_data)
        
        # Then: Appropriate processing
        assert result.status in ["success", "partial_success"]
        if result.status == "success":
            assert result.data is not None
```

#### 異常系シナリオ
```python
    def test_main_use_case_invalid_input(self, api_client):
        """
        Scenario: Invalid input data
        Expected result: Appropriate error response
        """
        # Given: Invalid input
        invalid_input = {
            "field1": None,  # Required field is null
            "field2": -1,    # Invalid value
            "field3": "not_a_list"  # Type error
        }
        
        # When/Then: Validation error occurs
        with pytest.raises(ValueError) as excinfo:
            api_client.process_main_feature(invalid_input)
        
        assert "validation error" in str(excinfo.value).lower()
    
    def test_main_use_case_system_error(self, api_client, mock_dependencies):
        """
        Scenario: System error occurs
        Expected result: Appropriate error handling
        """
        # Given: Trigger system error
        mock_dependencies['repository'].load_data.side_effect = ConnectionError("DB connection error")
        
        input_data = InputModel(field1="test", field2=1, field3=["item"])
        
        # When: Feature execution
        result = api_client.process_main_feature(input_data)
        
        # Then: Error response
        assert result.status == "error"
        assert "connection" in result.error_message.lower()
```

### 2. 統合シナリオテスト

#### データフロー確認
```python
class TestDataFlowAcceptance:
    """End-to-end data flow acceptance tests"""
    
    def test_end_to_end_data_processing(self, api_client):
        """
        Scenario: Complete flow from data input to output
        Expected result: Data is correctly transformed and processed
        """
        # Given: Actual data structure
        input_data = InputModel(
            field1="sample_data",
            field2=100,
            field3=["data1", "data2", "data3"]
        )
        
        # When: Execute complete processing
        result = api_client.process_main_feature(input_data)
        
        # Then: Data is appropriately transformed (simple validation)
        assert result.status == "success"
        assert result.data.processed_count > 0  # Verify processing was executed
        assert result.data.summary_value >= 0   # Verify aggregate value was calculated
        assert result.data.metadata is not None # Verify metadata was generated
    
    def test_multiple_requests_consistency(self, api_client):
        """
        Scenario: Multiple request consistency
        Expected result: Same output for same input
        """
        # Given: Same input data
        input_data = InputModel(field1="test", field2=50, field3=["a", "b"])
        
        # When: Execute multiple times
        result1 = api_client.process_main_feature(input_data)
        result2 = api_client.process_main_feature(input_data)
        
        # Then: Results match (simple validation)
        assert result1.status == result2.status  # Verify same status is returned
        assert (result1.data is None) == (result2.data is None)  # Verify data presence matches
```

### 3. パフォーマンス・制約テスト

#### 応答時間テスト
```python
import time
from concurrent.futures import ThreadPoolExecutor

class TestPerformanceAcceptance:
    """Performance acceptance tests"""
    
    def test_response_time_within_limit(self, api_client):
        """
        Scenario: Response time constraint verification
        Expected result: Processing completed within specified time
        """
        # Given: Standard input
        input_data = InputModel(field1="test", field2=100, field3=["item"] * 10)
        
        # When: Measure processing time
        start_time = time.time()
        result = api_client.process_main_feature(input_data)
        end_time = time.time()
        
        # Then: Response time within acceptable range
        processing_time = end_time - start_time
        assert processing_time < 2.0  # Within 2 seconds
        assert result.status == "success"
    
    def test_concurrent_requests_handling(self, api_client):
        """
        Scenario: Concurrent request processing
        Expected result: Parallel processing works normally
        """
        # Given: Multiple input data
        inputs = [
            InputModel(field1=f"test_{i}", field2=i, field3=[f"item_{i}"])
            for i in range(5)
        ]
        
        # When: Execute parallel processing
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(api_client.process_main_feature, input_data)
                for input_data in inputs
            ]
            results = [future.result() for future in futures]
        
        # Then: All succeed
        assert all(result.status == "success" for result in results)
        assert len(results) == 5
```

### 4. セキュリティ・堅牢性テスト

#### 入力検証テスト
```python
class TestSecurityAcceptance:
    """Security acceptance tests"""
    
    @pytest.mark.parametrize("malicious_input", [
        {"field1": "'; DROP TABLE users; --"},  # SQL injection attempt
        {"field1": "<script>alert('xss')</script>"},  # XSS attempt
        {"field1": "../../../etc/passwd"},  # Path traversal attempt
        {"field2": "9" * 1000},  # Large number
        {"field3": ["item"] * 10000},  # Large list
    ])
    def test_malicious_input_rejection(self, api_client, malicious_input):
        """
        Scenario: Processing malicious input
        Expected result: Appropriately rejected
        """
        # When: Execute with malicious input
        with pytest.raises((ValueError, SecurityError, ValidationError)):
            api_client.process_main_feature(malicious_input)
    
    def test_sensitive_data_not_logged(self, api_client, caplog):
        """
        Scenario: Prevent sensitive data leakage
        Expected result: No sensitive information remains in logs
        """
        # Given: Input containing sensitive information
        input_data = InputModel(
            field1="user_password_123",
            field2=1,
            field3=["secret_token"]
        )
        
        # When: Execute processing
        api_client.process_main_feature(input_data)
        
        # Then: No sensitive information in logs
        log_output = caplog.text
        assert "password" not in log_output.lower()
        assert "secret" not in log_output.lower()
```

## テスト実行・検証

### テスト実行コマンド
```bash
# Acceptance test execution
uv run --frozen pytest tests/acceptance/ -v

# Specific test class execution
uv run --frozen pytest tests/acceptance/test_main_feature.py::TestMainFeatureAcceptance -v

# Detailed output on failure
uv run --frozen pytest tests/acceptance/ -v -s --tb=long
```

### Red Phase確認
```bash
# Initial execution (all should fail)
uv run --frozen pytest tests/acceptance/ -v
# Expected: All tests fail (before implementation)

# Post-implementation verification
uv run --frozen pytest tests/acceptance/ -v
# Expected: All tests succeed
```

### カバレッジ確認
```bash
# Acceptance test coverage
uv run --frozen pytest tests/acceptance/ --cov=src --cov-report=html --cov-report=term
```

## テスト品質指標

### 成功基準
- [ ] **テスト実行時間**: 全受け入れテスト30秒以内
- [ ] **テスト成功率**: 実装完了後100%成功
- [ ] **シナリオカバレッジ**: 主要ユースケース100%カバー
- [ ] **エラーパス**: 異常系シナリオ80%以上カバー

### メンテナンス性
- [ ] **テスト独立性**: 各テストが独立して実行可能
- [ ] **テストデータ管理**: フィクスチャによる適切なデータ管理
- [ ] **モック使用**: 外部依存を最小化
- [ ] **可読性**: テストの意図が明確

---

## 次ステップ

### シグネチャ実装開始
```bash
/user:implement-signatures [この受け入れテストパス]
```

### GitHub Issue 更新
受け入れテスト作成完了をissueに反映