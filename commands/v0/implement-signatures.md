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

### コード設計原則
- **DRY原則**: 重複コードを排除、同一機能は一箇所に集約
- **簡潔性優先**: 同等機能なら最もコンパクトな記述を採用
- **冗長性の最小化**: 必要性が高い場合を除いて冗長な記述は避ける
- **関数・構成の効率化**: 類似処理は統合、共通パターンは抽象化

## 実装戦略

### 1. 実装順序（下位層から）

#### フェーズ1: モデル層シグネチャ (`src/models/`)
```python
# src/models/input_model.py
from pydantic import BaseModel, Field
from typing import List, Optional

class InputModel(BaseModel):
    """Input data model"""
    field1: str = Field(..., description="Required string field")
    field2: int = Field(..., ge=0, description="Non-negative integer field")
    field3: List[str] = Field(default_factory=list, description="String list")
    
    class Config:
        validate_assignment = True
        extra = "forbid"

# src/models/output_model.py
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class ProcessedData(BaseModel):
    """Processed result data"""
    computed_field: float = Field(..., description="Computed result")
    processed_count: int = Field(..., description="Processing count")
    summary_value: float = Field(..., description="Summary value")
    metadata: Dict[str, Any] = Field(default_factory=dict)

class OutputModel(BaseModel):
    """Output data model"""
    status: str = Field(..., description="Processing status")
    data: Optional[ProcessedData] = None
    error_message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
```

#### フェーズ2: リポジトリ層シグネチャ (`src/repository/`)
```python
# src/repository/base_repository.py
from abc import ABC, abstractmethod
from typing import Any, Optional, List

class BaseRepository(ABC):
    """Base repository class"""
    
    @abstractmethod
    async def load_data(self, source: str) -> List[Any]:
        """Load data"""
        pass
    
    @abstractmethod
    async def save_data(self, data: Any, destination: str) -> bool:
        """Save data"""
        pass

# src/repository/data_repository.py
from src.repository.base_repository import BaseRepository
from src.models.input_model import InputModel
from typing import List

class DataRepository(BaseRepository):
    """Data access implementation (signature only)"""
    
    async def load_data(self, source: str) -> List[InputModel]:
        """Load data - TODO: Implementation pending"""
        # Red Phase: Intentionally unimplemented
        raise NotImplementedError("load_data implementation pending")
    
    async def save_data(self, data: Any, destination: str) -> bool:
        """Save data - TODO: Implementation pending"""
        # Red Phase: Intentionally unimplemented
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
    """Main business logic (signature only)"""
    
    def __init__(self, repository: Optional[DataRepository] = None):
        self.repository = repository or DataRepository()
    
    async def process_main_feature(self, input_data: InputModel) -> OutputModel:
        """
        Main feature processing - TODO: Business logic implementation pending
        
        Args:
            input_data: Input data
            
        Returns:
            OutputModel: Processing result
        """
        # Red Phase: Minimal response (should fail)
        try:
            # Minimal implementation for type checking
            processed_data = ProcessedData(
                computed_field=0.0,  # Wrong value
                processed_count=0,   # Wrong value
                summary_value=0.0,   # Wrong value
                metadata={}
            )
            
            return OutputModel(
                status="error",  # Intentionally failing status
                data=processed_data,
                error_message="Implementation pending"
            )
        except Exception as e:
            return OutputModel(
                status="error",
                error_message=f"Unexpected error: {str(e)}"
            )
    
    def _calculate_business_logic(self, input_data: InputModel) -> ProcessedData:
        """Business logic calculation - TODO: Implementation pending"""
        # Red Phase: Intentionally unimplemented
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
    """Main API interface (signature only)"""
    
    def __init__(self, dependencies: Optional[Dict[str, Any]] = None):
        """
        API initialization
        
        Args:
            dependencies: Dependency injection for testing
        """
        self.dependencies = dependencies or {}
        self.service = MainService(
            repository=self.dependencies.get('repository')
        )
    
    def process_main_feature(self, input_data: InputModel) -> OutputModel:
        """
        Main feature API endpoint - TODO: Implementation pending
        
        Args:
            input_data: Input data (InputModel or dict)
            
        Returns:
            OutputModel: Processing result
        """
        try:
            # Input data normalization
            if isinstance(input_data, dict):
                input_data = InputModel(**input_data)
            
            # Red Phase: Minimal processing
            # Actual processing to be implemented later
            result = OutputModel(
                status="error",  # Intentionally failing
                error_message="API implementation pending"
            )
            
            return result
            
        except ValueError as e:
            # Validation error
            return OutputModel(
                status="error",
                error_message=f"Validation error: {str(e)}"
            )
        except Exception as e:
            # System error
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
        """FastAPI endpoint"""
        result = api.process_main_feature(request)
        if result.status == "error":
            raise HTTPException(status_code=400, detail=result.error_message)
        return result
        
except ImportError:
    # Ignore in environments where FastAPI is not available
    pass
```

### 2. プロジェクト構造セットアップ

#### ディレクトリ構造作成
```python
# src/__init__.py
"""Main package"""
__version__ = "0.1.0"

# src/models/__init__.py
"""Data model layer"""
from .input_model import InputModel
from .output_model import OutputModel, ProcessedData

__all__ = ["InputModel", "OutputModel", "ProcessedData"]

# src/repository/__init__.py
"""Data access layer"""
from .base_repository import BaseRepository
from .data_repository import DataRepository

__all__ = ["BaseRepository", "DataRepository"]

# src/service/__init__.py
"""Business logic layer"""
from .main_service import MainService

__all__ = ["MainService"]

# src/api/__init__.py
"""API interface layer"""
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
    """Application settings"""
    
    # Data related
    data_dir: Path = Path("data")
    output_dir: Path = Path("output")
    
    # Log settings
    log_level: str = "INFO"
    log_format: str = "json"
    
    # API settings
    api_host: str = "localhost"
    api_port: int = 8000
    
    # External services
    external_service_url: Optional[str] = None
    external_service_timeout: int = 30
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Settings instance
settings = Settings()
```

## 検証・テスト実行

### 型チェック実行
```bash
# Type safety verification
uv run --frozen pyright src/

# Expected result: No errors (correct type definitions)
```

### リント・フォーマット
```bash
# Code quality check
uv run --frozen ruff check src/
uv run --frozen ruff format src/

# Expected result: No lint errors
```

### Red Phase確認
```bash
# Acceptance test execution (should fail)
uv run --frozen pytest tests/acceptance/ -v

# Expected result: Most tests should fail
# - NotImplementedError or
# - Assertion error due to unexpected results
```

### インポート・基本動作確認
```python
# tests/test_signatures.py
def test_basic_imports():
    """Verify that basic imports work"""
    from src.models.input_model import InputModel
    from src.models.output_model import OutputModel
    from src.api.main_api import MainAPI
    
    # Basic instance creation
    input_data = InputModel(field1="test", field2=1, field3=["item"])
    api = MainAPI()
    
    # Basic execution (will fail but no exceptions)
    result = api.process_main_feature(input_data)
    assert isinstance(result, OutputModel)
    assert result.status == "error"  # Should fail in Red Phase
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