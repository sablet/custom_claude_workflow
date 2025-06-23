---
allowed-tools: ["Read", "Write", "Grep", "Glob", "Edit"]
description: "受け入れテスト作成：高抽象・低コスト・実行可能なテスト"
---

# 受け入れテスト作成: $ARGUMENTS

## 前提条件

### 入力ドキュメント
実装計画書: @$ARGUMENTS

### テスト方針
- **高抽象レベル**: ユーザーの視点からの動作確認
- **低実行コスト**: 高速実行・最小限のセットアップ
- **Red Phase対応**: 最初は失敗し、実装完了で成功するテスト

## 受け入れテスト設計

### 1. メインユースケーステスト

#### 正常系シナリオ
```python
# tests/acceptance/test_main_feature.py
import pytest
from unittest.mock import Mock
from src.api.main_api import MainAPI
from src.models.input_model import InputModel
from src.models.output_model import OutputModel

class TestMainFeatureAcceptance:
    """メイン機能の受け入れテスト"""
    
    @pytest.fixture
    def mock_dependencies(self):
        """依存関係のモック（低コスト化）"""
        return {
            'repository': Mock(),
            'external_service': Mock(),
            'config': Mock()
        }
    
    @pytest.fixture
    def api_client(self, mock_dependencies):
        """APIクライアントのセットアップ"""
        return MainAPI(dependencies=mock_dependencies)
    
    def test_main_use_case_success_path(self, api_client):
        """
        シナリオ: ユーザーが正常な入力でメイン機能を実行
        期待結果: 期待する出力が得られる
        """
        # Given: 正常な入力データ
        input_data = InputModel(
            field1="valid_value",
            field2=42,
            field3=["item1", "item2"]
        )
        
        # When: メイン機能を実行
        result = api_client.process_main_feature(input_data)
        
        # Then: 成功レスポンスを取得
        assert result.status == "success"
        assert result.data is not None
        assert isinstance(result.data, OutputModel)
        assert result.data.computed_field > 0
    
    def test_main_use_case_with_edge_values(self, api_client):
        """
        シナリオ: 境界値での入力
        期待結果: 適切に処理される
        """
        # Given: 境界値入力
        input_data = InputModel(
            field1="",  # 最小値
            field2=0,   # 境界値
            field3=[]   # 空リスト
        )
        
        # When: 機能実行
        result = api_client.process_main_feature(input_data)
        
        # Then: 適切な処理
        assert result.status in ["success", "partial_success"]
        if result.status == "success":
            assert result.data is not None
```

#### 異常系シナリオ
```python
    def test_main_use_case_invalid_input(self, api_client):
        """
        シナリオ: 不正な入力データ
        期待結果: 適切なエラーレスポンス
        """
        # Given: 不正な入力
        invalid_input = {
            "field1": None,  # 必須フィールドが null
            "field2": -1,    # 不正な値
            "field3": "not_a_list"  # 型エラー
        }
        
        # When/Then: バリデーションエラーが発生
        with pytest.raises(ValueError) as excinfo:
            api_client.process_main_feature(invalid_input)
        
        assert "validation error" in str(excinfo.value).lower()
    
    def test_main_use_case_system_error(self, api_client, mock_dependencies):
        """
        シナリオ: システムエラー発生
        期待結果: 適切なエラーハンドリング
        """
        # Given: システムエラーを発生させる
        mock_dependencies['repository'].load_data.side_effect = ConnectionError("DB接続エラー")
        
        input_data = InputModel(field1="test", field2=1, field3=["item"])
        
        # When: 機能実行
        result = api_client.process_main_feature(input_data)
        
        # Then: エラーレスポンス
        assert result.status == "error"
        assert "connection" in result.error_message.lower()
```

### 2. 統合シナリオテスト

#### データフロー確認
```python
class TestDataFlowAcceptance:
    """データフロー全体の受け入れテスト"""
    
    def test_end_to_end_data_processing(self, api_client):
        """
        シナリオ: データ入力から出力まで全体フロー
        期待結果: データが正しく変換・処理される
        """
        # Given: 実際のデータ構造
        input_data = InputModel(
            field1="sample_data",
            field2=100,
            field3=["data1", "data2", "data3"]
        )
        
        # When: 全体処理を実行
        result = api_client.process_main_feature(input_data)
        
        # Then: データが適切に変換されている
        assert result.status == "success"
        assert result.data.processed_count == 3  # field3の要素数と一致
        assert result.data.summary_value == 100  # field2の値を基に計算
        assert "sample_data" in result.data.metadata
    
    def test_multiple_requests_consistency(self, api_client):
        """
        シナリオ: 複数リクエストの一貫性
        期待結果: 同じ入力に対して同じ出力
        """
        # Given: 同じ入力データ
        input_data = InputModel(field1="test", field2=50, field3=["a", "b"])
        
        # When: 複数回実行
        result1 = api_client.process_main_feature(input_data)
        result2 = api_client.process_main_feature(input_data)
        
        # Then: 結果が一致
        assert result1.data.computed_field == result2.data.computed_field
        assert result1.data.summary_value == result2.data.summary_value
```

### 3. パフォーマンス・制約テスト

#### 応答時間テスト
```python
import time
from concurrent.futures import ThreadPoolExecutor

class TestPerformanceAcceptance:
    """パフォーマンス受け入れテスト"""
    
    def test_response_time_within_limit(self, api_client):
        """
        シナリオ: 応答時間の制約確認
        期待結果: 規定時間内に処理完了
        """
        # Given: 標準的な入力
        input_data = InputModel(field1="test", field2=100, field3=["item"] * 10)
        
        # When: 処理時間を測定
        start_time = time.time()
        result = api_client.process_main_feature(input_data)
        end_time = time.time()
        
        # Then: 応答時間が許容範囲内
        processing_time = end_time - start_time
        assert processing_time < 2.0  # 2秒以内
        assert result.status == "success"
    
    def test_concurrent_requests_handling(self, api_client):
        """
        シナリオ: 同時リクエストの処理
        期待結果: 並行処理が正常に動作
        """
        # Given: 複数の入力データ
        inputs = [
            InputModel(field1=f"test_{i}", field2=i, field3=[f"item_{i}"])
            for i in range(5)
        ]
        
        # When: 並行処理実行
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(api_client.process_main_feature, input_data)
                for input_data in inputs
            ]
            results = [future.result() for future in futures]
        
        # Then: すべて成功
        assert all(result.status == "success" for result in results)
        assert len(results) == 5
```

### 4. セキュリティ・堅牢性テスト

#### 入力検証テスト
```python
class TestSecurityAcceptance:
    """セキュリティ受け入れテスト"""
    
    @pytest.mark.parametrize("malicious_input", [
        {"field1": "'; DROP TABLE users; --"},  # SQL injection試行
        {"field1": "<script>alert('xss')</script>"},  # XSS試行
        {"field1": "../../../etc/passwd"},  # Path traversal試行
        {"field2": "9" * 1000},  # 巨大数値
        {"field3": ["item"] * 10000},  # 巨大リスト
    ])
    def test_malicious_input_rejection(self, api_client, malicious_input):
        """
        シナリオ: 悪意ある入力の処理
        期待結果: 適切に拒否される
        """
        # When: 悪意ある入力で実行
        with pytest.raises((ValueError, SecurityError, ValidationError)):
            api_client.process_main_feature(malicious_input)
    
    def test_sensitive_data_not_logged(self, api_client, caplog):
        """
        シナリオ: 機密データの漏洩防止
        期待結果: ログに機密情報が残らない
        """
        # Given: 機密情報を含む入力
        input_data = InputModel(
            field1="user_password_123",
            field2=1,
            field3=["secret_token"]
        )
        
        # When: 処理実行
        api_client.process_main_feature(input_data)
        
        # Then: ログに機密情報が含まれない
        log_output = caplog.text
        assert "password" not in log_output.lower()
        assert "secret" not in log_output.lower()
```

## テスト実行・検証

### テスト実行コマンド
```bash
# 受け入れテスト実行
uv run --frozen pytest tests/acceptance/ -v

# 特定のテストクラス実行
uv run --frozen pytest tests/acceptance/test_main_feature.py::TestMainFeatureAcceptance -v

# 失敗時詳細出力
uv run --frozen pytest tests/acceptance/ -v -s --tb=long
```

### Red Phase確認
```bash
# 最初の実行（すべて失敗するはず）
uv run --frozen pytest tests/acceptance/ -v
# Expected: すべてのテストが失敗 (実装前なので)

# 実装後の確認
uv run --frozen pytest tests/acceptance/ -v
# Expected: すべてのテストが成功
```

### カバレッジ確認
```bash
# 受け入れテストのカバレッジ
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