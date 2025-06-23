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
    """レイヤー間統合テスト"""
    
    @pytest.fixture
    def temp_data_dir(self):
        """一時データディレクトリ"""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)
    
    @pytest.fixture
    def repository(self, temp_data_dir):
        """実際のリポジトリインスタンス"""
        return DataRepository(data_dir=temp_data_dir)
    
    @pytest.fixture
    def service(self, repository):
        """実際のサービスインスタンス"""
        return MainService(repository=repository)
    
    @pytest.fixture
    def api(self, repository):
        """実際のAPIインスタンス（リポジトリ注入）"""
        return MainAPI(dependencies={'repository': repository})
    
    def test_complete_data_flow(self, api, temp_data_dir):
        """
        完全なデータフロー統合テスト
        API → Service → Repository → ファイルシステム
        """
        # Given: 実際の入力データ
        input_data = InputModel(
            field1="integration_test",
            field2=100,
            field3=["item1", "item2", "item3"]
        )
        
        # When: API経由で処理実行
        result = api.process_main_feature(input_data)
        
        # Then: 正常な結果を取得
        assert result.status == "success"
        assert result.data is not None
        assert result.data.processed_count == 3
        assert result.data.summary_value == 100.0
        assert result.data.computed_field == 250.0  # 100 * 2.5
        
        # データベース/ファイルシステムへの副作用も確認
        # （必要に応じて）
    
    def test_repository_persistence(self, repository, temp_data_dir):
        """
        リポジトリの永続化統合テスト
        """
        # Given: テストデータ
        test_data = [
            InputModel(field1="test1", field2=1, field3=["a"]),
            InputModel(field1="test2", field2=2, field3=["b", "c"])
        ]
        
        # When: データ保存・読み込み
        save_success = asyncio.run(repository.save_data(test_data, "test_dataset"))
        loaded_data = asyncio.run(repository.load_data("test_dataset"))
        
        # Then: データが正しく永続化される
        assert save_success is True
        assert len(loaded_data) == 2
        assert loaded_data[0].field1 == "test1"
        assert loaded_data[1].field3 == ["b", "c"]
        
        # ファイルが実際に作成されていることを確認
        assert (temp_data_dir / "test_dataset.json").exists()
    
    def test_service_business_logic_integration(self, service):
        """
        サービス層のビジネスロジック統合テスト
        """
        # Given: 複雑な入力データ
        complex_input = InputModel(
            field1="complex_business_case",
            field2=999,
            field3=["item" + str(i) for i in range(50)]
        )
        
        # When: ビジネスロジック実行
        result = asyncio.run(service.process_main_feature(complex_input))
        
        # Then: ビジネスルールが正しく適用される
        assert result.status == "success"
        assert result.data.processed_count == 50
        assert result.data.computed_field == 2497.5  # 999 * 2.5
        assert "complex_business_case" in result.data.metadata["input_field1"]
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
    """エンドツーエンドテスト"""
    
    @pytest.fixture
    def real_environment_setup(self):
        """実環境に近いセットアップ"""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir) / "data"
            data_dir.mkdir()
            
            # 実際のデータファイルを作成
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
        現実的なユーザーシナリオ
        実際のファイル → 処理 → 結果確認
        """
        # Given: 実環境セットアップ
        data_dir = real_environment_setup["data_dir"]
        
        # APIを実際のデータディレクトリで初期化
        from src.repository.data_repository import DataRepository
        repository = DataRepository(data_dir=data_dir)
        api = MainAPI(dependencies={'repository': repository})
        
        # When: ユーザーが実際に行う操作
        user_inputs = [
            InputModel(field1="user_request_1", field2=50, field3=["task1", "task2"]),
            InputModel(field1="user_request_2", field2=75, field3=["task3"]),
            InputModel(field1="user_request_3", field2=25, field3=["task4", "task5", "task6"])
        ]
        
        results = []
        for input_data in user_inputs:
            result = api.process_main_feature(input_data)
            results.append(result)
        
        # Then: すべてのリクエストが適切に処理される
        assert all(result.status == "success" for result in results)
        
        # 個別結果の検証
        assert results[0].data.processed_count == 2
        assert results[1].data.processed_count == 1  
        assert results[2].data.processed_count == 3
        
        # ビジネスロジックの一貫性確認
        expected_computed = [125.0, 187.5, 62.5]  # field2 * 2.5
        actual_computed = [r.data.computed_field for r in results]
        assert actual_computed == expected_computed
    
    def test_concurrent_user_requests(self, real_environment_setup):
        """
        同時ユーザーリクエストのテスト
        """
        # Given: 実環境セットアップ
        data_dir = real_environment_setup["data_dir"]
        repository = DataRepository(data_dir=data_dir)
        
        # When: 複数のAPIインスタンスで同時処理
        apis = [MainAPI(dependencies={'repository': repository}) for _ in range(3)]
        inputs = [
            InputModel(field1=f"concurrent_{i}", field2=i*10, field3=[f"item_{i}"])
            for i in range(3)
        ]
        
        # 並行実行
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(api.process_main_feature, input_data)
                for api, input_data in zip(apis, inputs)
            ]
            results = [future.result() for future in futures]
        
        # Then: すべて成功
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
    """パフォーマンス統合テスト"""
    
    @pytest.fixture
    def performance_api(self):
        """パフォーマンステスト用API"""
        return MainAPI()
    
    def test_response_time_under_load(self, performance_api):
        """
        負荷時の応答時間テスト
        """
        # Given: 大量のリクエスト
        requests = [
            InputModel(
                field1=f"load_test_{i}",
                field2=i,
                field3=[f"item_{j}" for j in range(10)]
            )
            for i in range(100)
        ]
        
        # When: 負荷実行・時間測定
        start_time = time.time()
        
        response_times = []
        for request in requests[:10]:  # サンプル測定
            req_start = time.time()
            result = performance_api.process_main_feature(request)
            req_end = time.time()
            
            response_times.append(req_end - req_start)
            assert result.status == "success"
        
        total_time = time.time() - start_time
        
        # Then: パフォーマンス要件を満たす
        avg_response_time = statistics.mean(response_times)
        max_response_time = max(response_times)
        
        assert avg_response_time < 0.1  # 平均100ms以内
        assert max_response_time < 0.5  # 最大500ms以内
        assert total_time < 5.0  # 全体5秒以内
        
        print(f"平均応答時間: {avg_response_time:.3f}s")
        print(f"最大応答時間: {max_response_time:.3f}s")
    
    def test_memory_usage_stability(self, performance_api):
        """
        メモリ使用量安定性テスト
        """
        import psutil
        import os
        
        # Given: プロセス情報取得
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # When: 大量処理実行
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
        
        # Then: メモリ使用量が適切
        memory_increase = final_memory - initial_memory
        assert memory_increase < 100  # 100MB以下の増加
        
        print(f"初期メモリ: {initial_memory:.1f}MB")
        print(f"最終メモリ: {final_memory:.1f}MB")
        print(f"増加量: {memory_increase:.1f}MB")
    
    def test_concurrent_processing_stability(self, performance_api):
        """
        並行処理安定性テスト
        """
        # Given: 並行リクエスト準備
        concurrent_requests = [
            InputModel(
                field1=f"concurrent_{i}",
                field2=i*5,
                field3=[f"concurrent_item_{j}" for j in range(i % 10 + 1)]
            )
            for i in range(20)
        ]
        
        # When: 並行実行
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
        
        # Then: 並行処理が安定
        assert len(errors) == 0, f"並行処理エラー: {errors}"
        assert len(results) == 20
        assert all(result.status == "success" for result in results)
        
        # データ整合性確認
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
    """設定・環境統合テスト"""
    
    def test_different_environment_configs(self):
        """
        異なる環境設定での動作テスト
        """
        # Given: 異なる環境設定
        test_configs = [
            {"LOG_LEVEL": "DEBUG", "DATA_DIR": "/tmp/test_debug"},
            {"LOG_LEVEL": "INFO", "DATA_DIR": "/tmp/test_info"},
            {"LOG_LEVEL": "ERROR", "DATA_DIR": "/tmp/test_error"}
        ]
        
        for config in test_configs:
            # When: 環境変数設定でAPI実行
            with patch_env_vars(config):
                settings = Settings()
                api = MainAPI()
                
                result = api.process_main_feature({
                    "field1": f"config_test_{config['LOG_LEVEL']}",
                    "field2": 42,
                    "field3": ["config_item"]
                })
                
                # Then: 設定に関係なく正常動作
                assert result.status == "success"
                assert result.data is not None

@pytest.fixture
def patch_env_vars():
    """環境変数パッチャー"""
    def _patch_env_vars(env_vars):
        return patch.dict(os.environ, env_vars)
    return _patch_env_vars
```

## テスト実行・検証

### 統合テスト実行
```bash
# 統合テスト実行
!cd $ARGUMENTS && uv run --frozen pytest tests/integration/ -v

# パフォーマンステストのみ
!cd $ARGUMENTS && uv run --frozen pytest tests/integration/test_performance.py -v

# 詳細出力付き実行
!cd $ARGUMENTS && uv run --frozen pytest tests/integration/ -v -s --tb=long
```

### カバレッジ統合確認
```bash
# 統合テスト含むカバレッジ
!cd $ARGUMENTS && uv run --frozen pytest tests/ --cov=src --cov-report=html --cov-report=term
```

### 品質確認
```bash
# 全テスト実行（受け入れ + 統合）
!cd $ARGUMENTS && uv run --frozen pytest tests/ -v

# パフォーマンスレポート付き
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