---
allowed-tools: ["Read", "Write", "Edit", "MultiEdit", "Bash"]
description: "シグネチャ実装：テスト失敗確認用の最小実装"
---

# シグネチャ実装: $ARGUMENTS

## 前提条件

### 入力ドキュメント
受け入れテストファイル: @$ARGUMENTS

### TDD Red Phase 方針
- **最小実装**: テストが実行できる最小限のコード
- **意図的な失敗**: ビジネスロジックは未実装でテスト失敗を確保
- **型安全性**: pyright チェック合格
- **レイヤード構造**: 適切な層分離を維持

## 実装戦略

### 1. 実装順序（下位層から）

#### フェーズ1: モデル層シグネチャ (`src/models/`)
```python
# src/models/input_model.py
from pydantic import BaseModel, Field
from typing import List, Optional

class InputModel(BaseModel):
    """入力データモデル"""
    field1: str = Field(..., description="必須文字列フィールド")
    field2: int = Field(..., ge=0, description="非負整数フィールド")
    field3: List[str] = Field(default_factory=list, description="文字列リスト")
    
    class Config:
        validate_assignment = True
        extra = "forbid"

# src/models/output_model.py
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class OutputModel(BaseModel):
    """出力データモデル"""
    status: str = Field(..., description="処理ステータス")
    data: Optional['ProcessedData'] = None
    error_message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class ProcessedData(BaseModel):
    """処理結果データ"""
    computed_field: float = Field(..., description="計算結果")
    processed_count: int = Field(..., description="処理件数")
    summary_value: float = Field(..., description="要約値")
    metadata: Dict[str, Any] = Field(default_factory=dict)

# 前方参照の解決
OutputModel.model_rebuild()
```

#### フェーズ2: リポジトリ層シグネチャ (`src/repository/`)
```python
# src/repository/base_repository.py
from abc import ABC, abstractmethod
from typing import Any, Optional, List

class BaseRepository(ABC):
    """リポジトリの基底クラス"""
    
    @abstractmethod
    async def load_data(self, source: str) -> List[Any]:
        """データ読み込み"""
        pass
    
    @abstractmethod
    async def save_data(self, data: Any, destination: str) -> bool:
        """データ保存"""
        pass

# src/repository/data_repository.py
from src.repository.base_repository import BaseRepository
from src.models.input_model import InputModel
from typing import List

class DataRepository(BaseRepository):
    """データアクセス実装（シグネチャのみ）"""
    
    async def load_data(self, source: str) -> List[InputModel]:
        """データ読み込み - TODO: 実装予定"""
        # Red Phase: 意図的な未実装
        raise NotImplementedError("load_data implementation pending")
    
    async def save_data(self, data: Any, destination: str) -> bool:
        """データ保存 - TODO: 実装予定"""
        # Red Phase: 意図的な未実装
        raise NotImplementedError("save_data implementation pending")
```

#### フェーズ3: サービス層シグネチャ (`src/service/`)
```python
# src/service/main_service.py
from src.models.input_model import InputModel
from src.models.output_model import OutputModel, ProcessedData
from src.repository.data_repository import DataRepository
from typing import Optional

class MainService:
    """メインビジネスロジック（シグネチャのみ）"""
    
    def __init__(self, repository: Optional[DataRepository] = None):
        self.repository = repository or DataRepository()
    
    async def process_main_feature(self, input_data: InputModel) -> OutputModel:
        """
        メイン機能処理 - TODO: ビジネスロジック実装予定
        
        Args:
            input_data: 入力データ
            
        Returns:
            OutputModel: 処理結果
        """
        # Red Phase: 最小限の応答（失敗するはず）
        try:
            # 型チェック通過用の最小実装
            processed_data = ProcessedData(
                computed_field=0.0,  # 間違った値
                processed_count=0,   # 間違った値
                summary_value=0.0,   # 間違った値
                metadata={}
            )
            
            return OutputModel(
                status="error",  # わざと失敗ステータス
                data=processed_data,
                error_message="Implementation pending"
            )
        except Exception as e:
            return OutputModel(
                status="error",
                error_message=f"Unexpected error: {str(e)}"
            )
    
    def _calculate_business_logic(self, input_data: InputModel) -> ProcessedData:
        """ビジネスロジック計算 - TODO: 実装予定"""
        # Red Phase: 意図的な未実装
        raise NotImplementedError("Business logic implementation pending")
```

#### フェーズ4: API層シグネチャ (`src/api/`)
```python
# src/api/main_api.py
from src.models.input_model import InputModel
from src.models.output_model import OutputModel
from src.service.main_service import MainService
from typing import Dict, Any, Optional

class MainAPI:
    """メインAPIインターフェース（シグネチャのみ）"""
    
    def __init__(self, dependencies: Optional[Dict[str, Any]] = None):
        """
        API初期化
        
        Args:
            dependencies: テスト用の依存関係注入
        """
        self.dependencies = dependencies or {}
        self.service = MainService(
            repository=self.dependencies.get('repository')
        )
    
    def process_main_feature(self, input_data: InputModel) -> OutputModel:
        """
        メイン機能のAPIエンドポイント - TODO: 実装予定
        
        Args:
            input_data: 入力データ（InputModel または dict）
            
        Returns:
            OutputModel: 処理結果
        """
        try:
            # 入力データの正規化
            if isinstance(input_data, dict):
                input_data = InputModel(**input_data)
            
            # Red Phase: 最小限の処理
            # 実際の処理は後で実装
            result = OutputModel(
                status="error",  # わざと失敗
                error_message="API implementation pending"
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

# FastAPI用の場合（オプション）
try:
    from fastapi import APIRouter, HTTPException, Depends
    
    router = APIRouter()
    
    @router.post("/main-feature", response_model=OutputModel)
    async def process_main_feature_endpoint(
        request: InputModel,
        api: MainAPI = Depends()
    ) -> OutputModel:
        """FastAPI エンドポイント"""
        result = api.process_main_feature(request)
        if result.status == "error":
            raise HTTPException(status_code=400, detail=result.error_message)
        return result
        
except ImportError:
    # FastAPI が利用できない環境では無視
    pass
```

### 2. プロジェクト構造セットアップ

#### ディレクトリ構造作成
```python
# src/__init__.py
"""メインパッケージ"""
__version__ = "0.1.0"

# src/models/__init__.py
"""データモデル層"""
from .input_model import InputModel
from .output_model import OutputModel, ProcessedData

__all__ = ["InputModel", "OutputModel", "ProcessedData"]

# src/repository/__init__.py
"""データアクセス層"""
from .base_repository import BaseRepository
from .data_repository import DataRepository

__all__ = ["BaseRepository", "DataRepository"]

# src/service/__init__.py
"""ビジネスロジック層"""
from .main_service import MainService

__all__ = ["MainService"]

# src/api/__init__.py
"""APIインターフェース層"""
from .main_api import MainAPI

__all__ = ["MainAPI"]
```

#### 設定ファイル
```python
# config/settings.py
from pydantic import BaseSettings
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    """アプリケーション設定"""
    
    # データ関連
    data_dir: Path = Path("data")
    output_dir: Path = Path("output")
    
    # ログ設定
    log_level: str = "INFO"
    log_format: str = "json"
    
    # API設定
    api_host: str = "localhost"
    api_port: int = 8000
    
    # 外部サービス
    external_service_url: Optional[str] = None
    external_service_timeout: int = 30
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# 設定インスタンス
settings = Settings()
```

## 検証・テスト実行

### 型チェック実行
```bash
# 型安全性確認
uv run --frozen pyright src/

# 期待結果: エラーなし（型定義が正しい）
```

### リント・フォーマット
```bash
# コード品質チェック
uv run --frozen ruff check src/
uv run --frozen ruff format src/

# 期待結果: リントエラーなし
```

### Red Phase確認
```bash
# 受け入れテスト実行（失敗するはず）
uv run --frozen pytest tests/acceptance/ -v

# 期待結果: ほとんどのテストが失敗
# - NotImplementedError または
# - 期待値と異なる結果による assertion error
```

### インポート・基本動作確認
```python
# tests/test_signatures.py
def test_basic_imports():
    """基本的なインポートが動作することを確認"""
    from src.models.input_model import InputModel
    from src.models.output_model import OutputModel
    from src.api.main_api import MainAPI
    
    # 基本的なインスタンス作成
    input_data = InputModel(field1="test", field2=1, field3=["item"])
    api = MainAPI()
    
    # 基本的な実行（失敗はするが例外は発生しない）
    result = api.process_main_feature(input_data)
    assert isinstance(result, OutputModel)
    assert result.status == "error"  # Red Phase なので失敗
```

## 品質保証チェックリスト

### コード品質
- [ ] **型チェック合格**: pyright でエラーなし
- [ ] **リント合格**: ruff check でエラーなし
- [ ] **フォーマット**: ruff format 適用済み
- [ ] **インポート**: 各モジュールが正しくインポート可能

### 構造品質
- [ ] **レイヤー分離**: 適切な依存関係の方向
- [ ] **命名規則**: 一貫した命名パターン
- [ ] **docstring**: 各クラス・メソッドに説明
- [ ] **型ヒント**: 全引数・戻り値に型注釈

### テスト準備
- [ ] **Red Phase**: 受け入れテストが失敗することを確認
- [ ] **実行可能性**: テストが例外なく実行できる
- [ ] **エラーメッセージ**: 適切なエラーメッセージ出力

---

## 次ステップ

### Red Phase確認
```bash
/user:verify-red-phase [この実装ディレクトリ]
```

### GitHub Issue 更新
シグネチャ実装完了をissueに反映し、次フェーズに進む