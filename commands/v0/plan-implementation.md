---
allowed-tools: ["Read", "Write", "Grep", "Glob"]
description: "実装計画書作成：TDD方針とタスク分解"
---

# 実装計画: $ARGUMENTS

## 前提条件

### 入力ドキュメント
設計書または仕様書: @$ARGUMENTS

### 開発方針
- **テスト駆動開発**: Red → Green → Refactor サイクル
- **レイヤード実装**: 下位層から上位層への段階的実装
- **継続的品質保証**: uv + ruff + pyright による品質チェック

### コード設計原則
- **DRY原則**: 重複コードを排除、同一機能は一箇所に集約
- **簡潔性優先**: 同等機能なら最もコンパクトな記述を採用
- **冗長性の最小化**: 必要性が高い場合を除いて冗長な記述は避ける
- **関数・構成の効率化**: 類似処理は統合、共通パターンは抽象化

## 実装戦略

### 1. 実装順序の決定

#### フェーズ1: モデル層 (`src/models/`)
**理由**: 他の層の基盤となるデータ構造を最初に確立
- [ ] **Pydanticモデル定義**: データスキーマの実装
- [ ] **バリデーションロジック**: データ整合性の確保
- [ ] **型定義**: 型安全性の確立

#### フェーズ2: リポジトリ層 (`src/repository/`)
**理由**: データアクセスの基盤を確立
- [ ] **データアクセスインターフェース**: 抽象基底クラス定義
- [ ] **具象実装**: ファイル/DB/API アクセス実装
- [ ] **モック実装**: テスト用のダミー実装

#### フェーズ3: サービス層 (`src/service/`)
**理由**: ビジネスロジックの中核実装
- [ ] **ユースケース実装**: 主要機能の実装
- [ ] **ビジネスルール**: ドメイン特有の制約実装
- [ ] **エラーハンドリング**: 例外処理の統一

#### フェーズ4: API層 (`src/api/`)
**理由**: 外部インターフェースの実装
- [ ] **エンドポイント定義**: REST/CLI/MCP等の実装
- [ ] **入出力変換**: リクエスト/レスポンス処理
- [ ] **認証・認可**: セキュリティ機能

### 2. TDD実装サイクル

#### 受け入れテスト作成 (高抽象・低コスト)
```python
# tests/acceptance/test_[feature]_acceptance.py
import pytest
from src.api.[feature]_api import [FeatureAPI]

class TestFeatureAcceptance:
    def test_main_use_case_happy_path(self):
        """Main use case normal path test"""
        # Given: Normal input data
        input_data = {...}
        
        # When: Execute main feature
        result = feature_api.process(input_data)
        
        # Then: Get expected result
        assert result.status == "success"
        assert result.data is not None
    
    def test_main_use_case_error_handling(self):
        """Main use case error handling test"""
        # Error case definition
        pass
```

#### ユニットテスト作成 (各層別)
```python
# tests/unit/test_[layer]_[module].py
import pytest
from unittest.mock import Mock, patch
from src.[layer].[module] import [TargetClass]

class Test[TargetClass]:
    @pytest.fixture
    def target(self):
        return [TargetClass]()
    
    def test_method_normal_case(self, target):
        """Normal case test"""
        pass
    
    def test_method_boundary_case(self, target):
        """Boundary value test"""
        pass
    
    def test_method_error_case(self, target):
        """Error case test"""
        pass
```

#### 実装サイクル詳細
1. **Red Phase**: テストを書き、失敗することを確認
2. **Green Phase**: テストが通る最小限の実装
3. **Refactor Phase**: コード品質の改善

## 詳細実装計画

### フェーズ1: モデル層実装

#### タスク分解
- [ ] **基底モデルクラス**: 共通機能の実装
  ```python
  # src/models/base.py
  from pydantic import BaseModel
  from typing import Any
  
  class BaseModel(BaseModel):
      class Config:
          validate_assignment = True
          extra = "forbid"
  ```

- [ ] **主要エンティティ**: ドメインオブジェクトの定義
  ```python
  # src/models/[entity].py
  from src.models.base import BaseModel
  from typing import Optional
  from datetime import datetime
  
  class [EntityModel](BaseModel):
      id: Optional[str] = None
      created_at: datetime
      # Other fields
  ```

- [ ] **バリューオブジェクト**: 値オブジェクトの実装

#### 検証項目
- [ ] **型チェック**: `uv run pyright src/models/`
- [ ] **バリデーション**: 不正データでの例外発生確認
- [ ] **シリアライゼーション**: JSON変換の動作確認

### フェーズ2: リポジトリ層実装

#### タスク分解
- [ ] **抽象インターフェース**: Repository パターンの基底クラス
  ```python
  # src/repository/base.py
  from abc import ABC, abstractmethod
  from typing import List, Optional
  
  class BaseRepository(ABC):
      @abstractmethod
      async def find_by_id(self, id: str) -> Optional[Any]:
          pass
  ```

- [ ] **具象実装**: 実際のデータアクセス
  ```python
  # src/repository/[entity]_repository.py
  from src.repository.base import BaseRepository
  from src.models.[entity] import [EntityModel]
  
  class [EntityRepository](BaseRepository):
      async def find_by_id(self, id: str) -> Optional[[EntityModel]]:
          # Implementation
          pass
  ```

#### 検証項目
- [ ] **データアクセス**: 実際のファイル/DB操作
- [ ] **エラーハンドリング**: 接続エラー・データ不整合の処理
- [ ] **パフォーマンス**: データ読み込み速度の測定

### フェーズ3: サービス層実装

#### タスク分解
- [ ] **主要ユースケース**: ビジネスロジックの実装
  ```python
  # src/service/[feature]_service.py
  from src.models.[entity] import [EntityModel]
  from src.repository.[entity]_repository import [EntityRepository]
  
  class [FeatureService]:
      def __init__(self, repository: [EntityRepository]):
          self.repository = repository
      
      async def execute_use_case(self, input: [InputModel]) -> [OutputModel]:
          # Business logic implementation
          pass
  ```

#### 検証項目
- [ ] **ビジネスルール**: ドメイン制約の正しい実装
- [ ] **統合動作**: リポジトリ層との連携確認
- [ ] **例外処理**: ビジネス例外の適切なハンドリング

### フェーズ4: API層実装

#### タスク分解
- [ ] **エンドポイント実装**: 外部インターフェース
  ```python
  # src/api/[feature]_api.py
  from fastapi import APIRouter, Depends
  from src.service.[feature]_service import [FeatureService]
  
  router = APIRouter()
  
  @router.post("/[endpoint]")
  async def [endpoint_function](
      request: [RequestModel],
      service: [FeatureService] = Depends()
  ) -> [ResponseModel]:
      return await service.execute_use_case(request)
  ```

#### 検証項目
- [ ] **エンドツーエンド**: 実際のリクエスト処理
- [ ] **セキュリティ**: 認証・認可の動作確認
- [ ] **エラーレスポンス**: 統一的なエラー形式

## 品質保証計画

### コード品質チェック
```bash
# 各フェーズ完了時に実行
uv run --frozen ruff check .
uv run --frozen ruff format .
uv run --frozen pyright
```

### テスト実行
```bash
# ユニットテスト
uv run --frozen pytest tests/unit/ -v

# 受け入れテスト  
uv run --frozen pytest tests/acceptance/ -v

# カバレッジ確認
uv run --frozen pytest --cov=src --cov-report=html
```

### パフォーマンス検証
- [ ] **メモリ使用量**: プロファイラーによる測定
- [ ] **実行時間**: 各層の処理時間測定
- [ ] **スケーラビリティ**: 負荷テストの実施

## スケジュール・マイルストーン

### フェーズ1完了条件
- [ ] 全Pydanticモデルが型チェック合格
- [ ] モデル層のユニットテスト100%通過
- [ ] バリデーション動作の確認完了

### フェーズ2完了条件
- [ ] リポジトリの抽象・具象実装完了
- [ ] データアクセステスト全通過
- [ ] モック実装によるテスト環境構築

### フェーズ3完了条件
- [ ] 主要ユースケースの実装完了
- [ ] サービス層統合テスト全通過
- [ ] ビジネスルール検証完了

### フェーズ4完了条件
- [ ] API エンドポイント実装完了
- [ ] エンドツーエンドテスト全通過
- [ ] セキュリティ検証完了

---

## 次ステップ

### TDD開始
```bash
/user:create-acceptance-tests [この計画書のパス]
```

### GitHub Issue 更新
実装計画確定をissueに反映し、開発作業開始