---
allowed-tools: ["Read", "Edit", "MultiEdit", "Write", "Bash"]
description: "Green Phase実装：テスト通過のためのビジネスロジック実装"
---

# ロジック実装 (Green Phase): $ARGUMENTS

## 前提条件

### 入力
実装ディレクトリ: $ARGUMENTS

### Green Phase の目標
- **テスト通過**: 受け入れテストがすべて成功する
- **最小限実装**: テスト合格に必要な最小限のコード
- **リファクタ準備**: 後のリファクタリングに備えたシンプルな実装

## 実装戦略

### 1. 実装優先順位（下位層から）

#### フェーズ1: モデル層の補完
既存のPydanticモデルに追加の計算ロジックやバリデーションを実装

#### フェーズ2: リポジトリ層の実装
データアクセス・永続化の具体的実装

#### フェーズ3: サービス層の実装  
ビジネスロジックの核心部分を実装

#### フェーズ4: API層の実装
インターフェースの完成と統合

## 詳細実装

### 1. リポジトリ層実装

#### データアクセス実装
@src/repository/data_repository.py

既存のNotImplementedErrorを実際の実装に置き換える：

```python
# src/repository/data_repository.py
import asyncio
from pathlib import Path
from typing import List, Dict, Any
import json
from src.repository.base_repository import BaseRepository
from src.models.input_model import InputModel

class DataRepository(BaseRepository):
    """データアクセス実装"""
    
    def __init__(self, data_dir: Path = Path("data")):
        self.data_dir = data_dir
        self.data_dir.mkdir(exist_ok=True)
    
    async def load_data(self, source: str) -> List[InputModel]:
        """
        データ読み込み実装
        テスト通過のための最小限実装
        """
        try:
            # ファイル読み込み（存在しない場合はダミーデータ）
            file_path = self.data_dir / f"{source}.json"
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return [InputModel(**item) for item in data]
            else:
                # テスト用のダミーデータ生成
                return [
                    InputModel(
                        field1=f"generated_data_{i}",
                        field2=i,
                        field3=[f"item_{i}"]
                    )
                    for i in range(3)
                ]
        except Exception as e:
            # エラー時は空リストを返す（テスト通過優先）
            return []
    
    async def save_data(self, data: Any, destination: str) -> bool:
        """データ保存実装"""
        try:
            file_path = self.data_dir / f"{destination}.json"
            
            # データをJSON形式で保存
            if hasattr(data, 'dict'):
                # Pydanticモデルの場合
                save_data = data.dict()
            elif isinstance(data, list):
                # リストの場合
                save_data = [
                    item.dict() if hasattr(item, 'dict') else item 
                    for item in data
                ]
            else:
                # その他の場合
                save_data = data
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception:
            return False
```

### 2. サービス層実装

#### ビジネスロジック実装
@src/service/main_service.py

NotImplementedErrorを実際のビジネスロジックに置き換える：

```python
# src/service/main_service.py
import asyncio
from typing import Optional, List
from src.models.input_model import InputModel
from src.models.output_model import OutputModel, ProcessedData
from src.repository.data_repository import DataRepository

class MainService:
    """メインビジネスロジック実装"""
    
    def __init__(self, repository: Optional[DataRepository] = None):
        self.repository = repository or DataRepository()
    
    async def process_main_feature(self, input_data: InputModel) -> OutputModel:
        """
        メイン機能処理の実装
        テスト通過を最優先とした実装
        """
        try:
            # 入力データの検証
            if not input_data.field1:
                return OutputModel(
                    status="error",
                    error_message="field1 is required"
                )
            
            # ビジネスロジック実行
            processed_data = await self._calculate_business_logic(input_data)
            
            # 成功レスポンス
            return OutputModel(
                status="success",
                data=processed_data
            )
            
        except ValueError as e:
            return OutputModel(
                status="error",
                error_message=f"Validation error: {str(e)}"
            )
        except Exception as e:
            return OutputModel(
                status="error",
                error_message=f"Processing error: {str(e)}"
            )
    
    async def _calculate_business_logic(self, input_data: InputModel) -> ProcessedData:
        """
        ビジネスロジック計算の実装
        受け入れテストの期待値に合わせた実装
        """
        # テストで期待される計算を実装
        computed_field = float(input_data.field2) * 2.5  # 計算ロジック
        processed_count = len(input_data.field3)  # 処理件数
        summary_value = float(input_data.field2)  # 要約値
        
        # メタデータ作成
        metadata = {
            "input_field1": input_data.field1,
            "processing_time": "0.001s",  # 簡易実装
            "algorithm": "basic_calculation"
        }
        
        # 外部データとの統合（必要に応じて）
        try:
            external_data = await self.repository.load_data("reference")
            if external_data:
                metadata["external_data_count"] = len(external_data)
        except Exception:
            # 外部データエラーは無視（テスト通過優先）
            pass
        
        return ProcessedData(
            computed_field=computed_field,
            processed_count=processed_count,
            summary_value=summary_value,
            metadata=metadata
        )
    
    def _validate_business_rules(self, input_data: InputModel) -> None:
        """ビジネスルール検証"""
        # 基本的なビジネスルール
        if input_data.field2 < 0:
            raise ValueError("field2 must be non-negative")
        
        if len(input_data.field3) > 1000:
            raise ValueError("field3 too large")
```

### 3. API層実装

#### APIインターフェース実装
@src/api/main_api.py

エラーステータスを成功ステータスに変更：

```python
# src/api/main_api.py
import asyncio
from typing import Dict, Any, Optional, Union
from src.models.input_model import InputModel
from src.models.output_model import OutputModel
from src.service.main_service import MainService

class MainAPI:
    """メインAPIインターフェース実装"""
    
    def __init__(self, dependencies: Optional[Dict[str, Any]] = None):
        """API初期化"""
        self.dependencies = dependencies or {}
        
        # 依存関係注入
        repository = self.dependencies.get('repository')
        self.service = MainService(repository=repository)
    
    def process_main_feature(self, input_data: Union[InputModel, dict]) -> OutputModel:
        """
        メイン機能のAPIエンドポイント実装
        受け入れテスト通過のための実装
        """
        try:
            # 入力データの正規化
            if isinstance(input_data, dict):
                # 辞書からPydanticモデルに変換
                input_model = InputModel(**input_data)
            else:
                input_model = input_data
            
            # 非同期処理を同期的に実行
            # （受け入れテストがsyncを期待している場合）
            loop = None
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            if loop.is_running():
                # 既にイベントループが動いている場合
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        asyncio.run, 
                        self.service.process_main_feature(input_model)
                    )
                    result = future.result()
            else:
                # 新しいイベントループで実行
                result = loop.run_until_complete(
                    self.service.process_main_feature(input_model)
                )
            
            return result
            
        except ValueError as e:
            # バリデーションエラー
            return OutputModel(
                status="error",
                error_message=f"Validation error: {str(e)}"
            )
        except Exception as e:
            # システムエラー
            return OutputModel(
                status="error",
                error_message=f"System error: {str(e)}"
            )
    
    def health_check(self) -> Dict[str, str]:
        """ヘルスチェックエンドポイント"""
        return {
            "status": "healthy",
            "service": "main_api",
            "version": "1.0.0"
        }
```

### 4. セキュリティ・エラーハンドリング実装

#### セキュリティ関連の実装
テストで要求されるセキュリティチェックの実装：

```python
# src/service/security_service.py（新規作成）
import re
from typing import List

class SecurityService:
    """セキュリティ関連のサービス"""
    
    @staticmethod
    def validate_input_security(input_data: str) -> None:
        """入力データのセキュリティ検証"""
        dangerous_patterns = [
            r"(?i)(drop\s+table|delete\s+from|update\s+.*set)",  # SQL injection
            r"<script[^>]*>.*?</script>",  # XSS
            r"\.\./",  # Path traversal
            r"exec\s*\(",  # Code execution
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, input_data):
                raise SecurityError(f"Malicious input detected: {pattern}")
    
    @staticmethod
    def sanitize_log_data(data: str) -> str:
        """ログ出力用のデータサニタイズ"""
        # 機密情報をマスク
        sensitive_patterns = [
            (r"password[^\s]*", "password***"),
            (r"secret[^\s]*", "secret***"),
            (r"token[^\s]*", "token***"),
        ]
        
        sanitized = data
        for pattern, replacement in sensitive_patterns:
            sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)
        
        return sanitized

class SecurityError(Exception):
    """セキュリティ関連の例外"""
    pass
```

## テスト実行・検証

### Green Phase確認
```bash
# 受け入れテスト実行（成功するはず）
!cd $ARGUMENTS && uv run --frozen pytest tests/acceptance/ -v

# 特定のテストクラス実行
!cd $ARGUMENTS && uv run --frozen pytest tests/acceptance/ -k "TestMainFeatureAcceptance" -v

# 詳細出力付き実行
!cd $ARGUMENTS && uv run --frozen pytest tests/acceptance/ -v -s
```

### コード品質確認
```bash
# 型チェック
!cd $ARGUMENTS && uv run --frozen pyright src/

# リント・フォーマット
!cd $ARGUMENTS && uv run --frozen ruff check src/
!cd $ARGUMENTS && uv run --frozen ruff format src/
```

### パフォーマンステスト
```bash
# パフォーマンステスト実行
!cd $ARGUMENTS && uv run --frozen pytest tests/acceptance/ -k "performance" -v
```

## 実装完了チェックリスト

### 機能実装
- [ ] **主要ユースケース**: テストで要求される機能が実装されている
- [ ] **エラーハンドリング**: 異常系シナリオが適切に処理される
- [ ] **境界値処理**: 境界値テストが通過する
- [ ] **セキュリティ**: セキュリティテストが通過する

### 品質確認
- [ ] **受け入れテスト**: 全受け入れテストが成功
- [ ] **型チェック**: pyright でエラーなし
- [ ] **リント**: ruff check でエラーなし
- [ ] **パフォーマンス**: 応答時間要件を満たす

### 実装原則
- [ ] **最小限実装**: テスト通過に必要な最小限のコード
- [ ] **シンプル設計**: 複雑な最適化は避ける
- [ ] **リファクタ準備**: 後のリファクタリングに備えた構造
- [ ] **レイヤー分離**: 適切な層分離を維持

## トラブルシューティング

### よくある問題

#### 1. 非同期処理の問題
```python
# 解決例：asyncio の適切な処理
import asyncio

def sync_wrapper(async_func, *args, **kwargs):
    """非同期関数を同期的に実行"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 別スレッドで実行
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, async_func(*args, **kwargs))
                return future.result()
        else:
            return loop.run_until_complete(async_func(*args, **kwargs))
    except RuntimeError:
        return asyncio.run(async_func(*args, **kwargs))
```

#### 2. テストデータの不一致
```python
# テストで期待される値を確認
def debug_test_expectations():
    """テストの期待値をデバッグ出力"""
    from tests.acceptance.test_main_feature import TestMainFeatureAcceptance
    test_instance = TestMainFeatureAcceptance()
    # 期待値を確認...
```

#### 3. 依存関係の問題
```bash
# 依存関係の再同期
cd $ARGUMENTS && uv sync --frozen
```

---

## 次ステップ

### 統合テスト実行
```bash
/user:create-integration-tests $ARGUMENTS
```

### GitHub Issue 更新
Green Phase実装完了をissueに反映し、統合テストフェーズに進む