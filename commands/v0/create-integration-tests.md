---
allowed-tools: ["Read", "Write", "Bash", "Edit"]
description: "統合テスト作成：実環境に近い条件での動作確認"
---

# 統合テスト作成: $ARGUMENTS

## 前提条件

### 入力
実装ディレクトリ: $ARGUMENTS

### 統合テストの目的
- **レイヤー間連携**: 各層が正しく連携して動作することを確認
- **実環境シミュレート**: 本番環境に近い条件でのテスト
- **エンドツーエンド**: ユーザーの操作から結果まで全体フローの確認
- **パフォーマンス**: 実際の負荷での性能確認

### テスト設計原則
- **簡素な検証**: 核心機能のみをテスト、実装詳細は避ける
- **公開インターフェース重視**: 内部実装ではなく外部APIをテスト
- **最小モック**: 必要最小限のモックのみ使用
- **保守性優先**: 実装変更時のテスト修正負荷を最小化

## 統合テスト設計

### 1. レイヤー間統合テスト

#### API → Service → Repository 統合
```python
# tests/integration/test_layer_integration.py
import pytest
import asyncio
import tempfile
from pathlib import Path
from src.api.main_api import MainAPI
from src.service.main_service import MainService
from src.repository.data_repository import DataRepository
from src.models.input_model import InputModel

class TestLayerIntegration:
    """Layer integration tests"""
    
    @pytest.fixture
    def temp_data_dir(self):
        """Temporary data directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)
    
    @pytest.fixture
    def repository(self, temp_data_dir):
        """Actual repository instance"""
        return DataRepository(data_dir=temp_data_dir)
    
    @pytest.fixture
    def service(self, repository):
        """Actual service instance"""
        return MainService(repository=repository)
    
    @pytest.fixture
    def api(self, repository):
        """Actual API instance (repository injection)"""
        return MainAPI(dependencies={'repository': repository})
    
    def test_complete_data_flow(self, api, temp_data_dir):
        """
        Complete data flow integration test
        API → Service → Repository → File system
        """
        # Given: Actual input data
        input_data = InputModel(
            field1="integration_test",
            field2=100,
            field3=["item1", "item2", "item3"]
        )
        
        # When: Execute processing via API
        result = api.process_main_feature(input_data)
        
        # Then: Get normal result (simple validation)
        assert result.status == "success"
        assert result.data is not None
        assert result.data.processed_count > 0  # Validate by range, not specific value
        assert result.data.summary_value > 0    # Resilient to business logic changes
        
        # Also check side effects to database/filesystem
        # (as needed)
    
    def test_repository_persistence(self, repository, temp_data_dir):
        """
        Repository persistence integration test
        """
        # Given: Test data
        test_data = [
            InputModel(field1="test1", field2=1, field3=["a"]),
            InputModel(field1="test2", field2=2, field3=["b", "c"])
        ]
        
        # When: Data save and load
        save_success = asyncio.run(repository.save_data(test_data, "test_dataset"))
        loaded_data = asyncio.run(repository.load_data("test_dataset"))
        
        # Then: Data is correctly persisted
        assert save_success is True
        assert len(loaded_data) == 2
        assert loaded_data[0].field1 == "test1"
        assert loaded_data[1].field3 == ["b", "c"]
        
        # Verify file is actually created
        assert (temp_data_dir / "test_dataset.json").exists()
    
    def test_service_business_logic_integration(self, service):
        """
        Service layer business logic integration test
        """
        # Given: Complex input data
        complex_input = InputModel(
            field1="complex_business_case",
            field2=999,
            field3=["item" + str(i) for i in range(50)]
        )
        
        # When: Execute business logic
        result = asyncio.run(service.process_main_feature(complex_input))
        
        # Then: Business rules are correctly applied (simple validation)
        assert result.status == "success"
        assert result.data.processed_count > 0  # Verify processing was executed
        assert result.data.computed_field > 0   # Verify calculation was executed
        assert result.data.metadata is not None # Verify metadata is set
```

### 2. エンドツーエンドテスト

#### 実環境シミュレーション
```python
# tests/integration/test_end_to_end.py
import pytest
import json
import tempfile
from pathlib import Path
from src.api.main_api import MainAPI
from src.models.input_model import InputModel

class TestEndToEnd:
    """End-to-end tests"""
    
    @pytest.fixture
    def real_environment_setup(self):
        """Setup close to real environment"""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir) / "data"
            data_dir.mkdir()
            
            # Create actual data files
            reference_data = [
                {"field1": "ref1", "field2": 10, "field3": ["r1"]},
                {"field1": "ref2", "field2": 20, "field3": ["r2", "r3"]}
            ]
            
            with open(data_dir / "reference.json", 'w') as f:
                json.dump(reference_data, f)
            
            yield {
                "data_dir": data_dir,
                "temp_dir": Path(temp_dir)
            }
    
    def test_realistic_user_scenario(self, real_environment_setup):
        """
        Realistic user scenario
        Actual file → Processing → Result verification
        """
        # Given: Real environment setup
        data_dir = real_environment_setup["data_dir"]
        
        # Initialize API with actual data directory
        from src.repository.data_repository import DataRepository
        repository = DataRepository(data_dir=data_dir)
        api = MainAPI(dependencies={'repository': repository})
        
        # When: Operations that user would actually perform
        user_inputs = [
            InputModel(field1="user_request_1", field2=50, field3=["task1", "task2"]),
            InputModel(field1="user_request_2", field2=75, field3=["task3"]),
            InputModel(field1="user_request_3", field2=25, field3=["task4", "task5", "task6"])
        ]
        
        results = []
        for input_data in user_inputs:
            result = api.process_main_feature(input_data)
            results.append(result)
        
        # Then: All requests are processed appropriately
        assert all(result.status == "success" for result in results)
        
        # Individual result validation
        assert results[0].data.processed_count == 2
        assert results[1].data.processed_count == 1  
        assert results[2].data.processed_count == 3
        
        # Business logic consistency verification
        expected_computed = [125.0, 187.5, 62.5]  # field2 * 2.5
        actual_computed = [r.data.computed_field for r in results]
        assert actual_computed == expected_computed
    
    def test_concurrent_user_requests(self, real_environment_setup):
        """
        Concurrent user request test
        """
        # Given: Real environment setup
        data_dir = real_environment_setup["data_dir"]
        repository = DataRepository(data_dir=data_dir)
        
        # When: Concurrent processing with multiple API instances
        apis = [MainAPI(dependencies={'repository': repository}) for _ in range(3)]
        inputs = [
            InputModel(field1=f"concurrent_{i}", field2=i*10, field3=[f"item_{i}"])
            for i in range(3)
        ]
        
        # Parallel execution
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(api.process_main_feature, input_data)
                for api, input_data in zip(apis, inputs)
            ]
            results = [future.result() for future in futures]
        
        # Then: All succeed
        assert all(result.status == "success" for result in results)
        assert len(results) == 3
```

### 3. パフォーマンス統合テスト

#### 負荷・性能テスト
```python
# tests/integration/test_performance.py
import pytest
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.api.main_api import MainAPI
from src.models.input_model import InputModel

class TestPerformanceIntegration:
    """Performance integration tests"""
    
    @pytest.fixture
    def performance_api(self):
        """API for performance testing"""
        return MainAPI()
    
    def test_response_time_under_load(self, performance_api):
        """
        Response time test under load
        """
        # Given: Large number of requests
        requests = [
            InputModel(
                field1=f"load_test_{i}",
                field2=i,
                field3=[f"item_{j}" for j in range(10)]
            )
            for i in range(100)
        ]
        
        # When: Load execution and time measurement
        start_time = time.time()
        
        response_times = []
        for request in requests[:10]:  # Sample measurement
            req_start = time.time()
            result = performance_api.process_main_feature(request)
            req_end = time.time()
            
            response_times.append(req_end - req_start)
            assert result.status == "success"
        
        total_time = time.time() - start_time
        
        # Then: Meet performance requirements
        avg_response_time = statistics.mean(response_times)
        max_response_time = max(response_times)
        
        assert avg_response_time < 0.1  # Average within 100ms
        assert max_response_time < 0.5  # Maximum within 500ms
        assert total_time < 5.0  # Total within 5 seconds
        
        print(f"Average response time: {avg_response_time:.3f}s")
        print(f"Maximum response time: {max_response_time:.3f}s")
    
    def test_memory_usage_stability(self, performance_api):
        """
        Memory usage stability test
        """
        import psutil
        import os
        
        # Given: Get process information
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # When: Execute large processing
        large_requests = [
            InputModel(
                field1=f"memory_test_{i}",
                field2=i,
                field3=[f"large_item_{j}" for j in range(100)]
            )
            for i in range(50)
        ]
        
        for request in large_requests:
            result = performance_api.process_main_feature(request)
            assert result.status == "success"
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Then: Memory usage is appropriate
        memory_increase = final_memory - initial_memory
        assert memory_increase < 100  # Increase under 100MB
        
        print(f"Initial memory: {initial_memory:.1f}MB")
        print(f"Final memory: {final_memory:.1f}MB")
        print(f"Increase: {memory_increase:.1f}MB")
    
    def test_concurrent_processing_stability(self, performance_api):
        """
        Concurrent processing stability test
        """
        # Given: Prepare concurrent requests
        concurrent_requests = [
            InputModel(
                field1=f"concurrent_{i}",
                field2=i*5,
                field3=[f"concurrent_item_{j}" for j in range(i % 10 + 1)]
            )
            for i in range(20)
        ]
        
        # When: Parallel execution
        results = []
        errors = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_request = {
                executor.submit(performance_api.process_main_feature, req): req
                for req in concurrent_requests
            }
            
            for future in as_completed(future_to_request):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    errors.append(e)
        
        # Then: Concurrent processing is stable
        assert len(errors) == 0, f"Concurrent processing errors: {errors}"
        assert len(results) == 20
        assert all(result.status == "success" for result in results)
        
        # Data consistency verification
        processed_counts = [r.data.processed_count for r in results]
        assert all(1 <= count <= 10 for count in processed_counts)
```

### 4. 環境・設定統合テスト

#### 設定・環境変数テスト
```python
# tests/integration/test_configuration.py
import pytest
import os
import tempfile
from pathlib import Path
from src.api.main_api import MainAPI
from config.settings import Settings

class TestConfigurationIntegration:
    """Configuration and environment integration tests"""
    
    def test_different_environment_configs(self):
        """
        Operation test with different environment settings
        """
        # Given: Different environment settings
        test_configs = [
            {"LOG_LEVEL": "DEBUG", "DATA_DIR": "/tmp/test_debug"},
            {"LOG_LEVEL": "INFO", "DATA_DIR": "/tmp/test_info"},
            {"LOG_LEVEL": "ERROR", "DATA_DIR": "/tmp/test_error"}
        ]
        
        for config in test_configs:
            # When: API execution with environment variable settings
            with patch_env_vars(config):
                settings = Settings()
                api = MainAPI()
                
                result = api.process_main_feature({
                    "field1": f"config_test_{config['LOG_LEVEL']}",
                    "field2": 42,
                    "field3": ["config_item"]
                })
                
                # Then: Normal operation regardless of settings
                assert result.status == "success"
                assert result.data is not None

@pytest.fixture
def patch_env_vars():
    """Environment variable patcher"""
    def _patch_env_vars(env_vars):
        return patch.dict(os.environ, env_vars)
    return _patch_env_vars
```

## テスト実行・検証

### 統合テスト実行
```bash
# Integration test execution
!cd $ARGUMENTS && uv run --frozen pytest tests/integration/ -v

# Performance tests only
!cd $ARGUMENTS && uv run --frozen pytest tests/integration/test_performance.py -v

# Detailed output execution
!cd $ARGUMENTS && uv run --frozen pytest tests/integration/ -v -s --tb=long
```

### カバレッジ統合確認
```bash
# Coverage including integration tests
!cd $ARGUMENTS && uv run --frozen pytest tests/ --cov=src --cov-report=html --cov-report=term
```

### 品質確認
```bash
# All test execution (acceptance + integration)
!cd $ARGUMENTS && uv run --frozen pytest tests/ -v

# With performance report
!cd $ARGUMENTS && uv run --frozen pytest tests/ --durations=10
```

## 成功基準

### 機能品質
- [ ] **レイヤー統合**: 各層が正しく連携
- [ ] **データ整合性**: データが正しく永続化・復元
- [ ] **エラー伝播**: エラーが適切に伝播・処理
- [ ] **設定反映**: 環境設定が正しく反映

### 性能品質  
- [ ] **応答時間**: 平均100ms、最大500ms以内
- [ ] **メモリ効率**: 大量処理でもメモリ使用量適切
- [ ] **並行安定性**: 並行処理でもデータ破損なし
- [ ] **スケーラビリティ**: 負荷増加に対する適切な動作

### 運用品質
- [ ] **環境適応**: 異なる環境設定での動作
- [ ] **ログ出力**: 適切なログレベル・内容
- [ ] **監視対応**: メトリクス収集可能
- [ ] **デバッグ支援**: 問題発生時の調査が容易

---

## 次ステップ

### GitHub Issue管理
```bash
/user:update-issue [issue番号] "統合テスト完了"
```

### プロジェクト完了確認
すべてのテストが通過したら、プロジェクト完了として最終レビューを実施