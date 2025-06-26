---
allowed-tools: ["Read", "Write", "Grep", "Glob"]
description: "新規アーキテクチャ設計とレイヤード構造の定義"
---

# アーキテクチャ設計: $ARGUMENTS

## 前提条件

### 入力
対象仕様書: @$ARGUMENTS

### 設計方針
- **レイヤード設計**: サービス層・モデル層・API層・リポジトリ層の分離
- **Python標準**: uv + ruff + pyright + Pydantic v2
- **テスト駆動**: 各層に対応するテストを設計

### コード設計原則
- **DRY原則**: 重複コードを排除、同一機能は一箇所に集約
- **簡潔性優先**: 同等機能なら最もコンパクトな記述を採用
- **冗長性の最小化**: 必要性が高い場合を除いて冗長な記述は避ける
- **関数・構成の効率化**: 類似処理は統合、共通パターンは抽象化

## アーキテクチャ設計

### 1. 層構造の定義

#### API/インターフェース層 (`src/api/`)
**責任**: 外部との入出力インターフェース
- [ ] **エンドポイント設計**: REST API/CLI/MCP等の外部接続点
- [ ] **リクエスト/レスポンス**: 入力検証・出力形式の統一
- [ ] **認証・認可**: セキュリティ制御の実装
- [ ] **エラーハンドリング**: 統一的な例外処理

```python
# src/api/[feature]_api.py
from fastapi import APIRouter
from src.models.[feature]_models import [FeatureRequest], [FeatureResponse]
from src.service.[feature]_service import [FeatureService]

router = APIRouter()

@router.post("/[endpoint]", response_model=[FeatureResponse])
async def [endpoint_function](request: [FeatureRequest]):
    service = [FeatureService]()
    return await service.process(request)
```

#### サービス/ビジネスロジック層 (`src/service/`)
**責任**: ビジネスルール・計算ロジックの実装
- [ ] **ユースケース実装**: 要求仕様の主要機能
- [ ] **ビジネスルール**: ドメイン特有の制約・計算
- [ ] **フロー制御**: 複数コンポーネントの協調処理
- [ ] **外部サービス連携**: 他システムとの統合

```python
# src/service/[feature]_service.py
from src.models.[feature]_models import [FeatureModel]
from src.repository.[feature]_repository import [FeatureRepository]

class [FeatureService]:
    def __init__(self):
        self.repository = [FeatureRepository]()
    
    async def process(self, data: [FeatureModel]) -> [ResultModel]:
        # Business logic implementation
        pass
```

#### ドメインモデル層 (`src/models/`)
**責任**: データ構造・ドメインオブジェクトの定義
- [ ] **データモデル**: Pydantic v2によるスキーマ定義
- [ ] **ドメインロジック**: データに密結合した操作
- [ ] **バリデーション**: データ整合性・制約の検証
- [ ] **型安全性**: 厳密な型定義

```python
# src/models/[feature]_models.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class [FeatureModel](BaseModel):
    field1: str = Field(..., description="Description")
    field2: Optional[float] = Field(None, ge=0.0)
    
    @validator('field1')
    def validate_field1(cls, v):
        # Custom validation
        return v
```

#### リポジトリ/データアクセス層 (`src/repository/`)
**責任**: データの永続化・外部データソースアクセス
- [ ] **データアクセス**: ファイル・DB・API等からのデータ取得
- [ ] **データ永続化**: 結果の保存・キャッシュ管理
- [ ] **データ変換**: 外部形式⇔内部モデルの変換
- [ ] **接続管理**: リソースの適切な管理

```python
# src/repository/[feature]_repository.py
from pathlib import Path
import pandas as pd
from src.models.[feature]_models import [FeatureModel]

class [FeatureRepository]:
    def __init__(self, data_dir: Path = Path("data")):
        self.data_dir = data_dir
    
    async def load_data(self, source: str) -> List[[FeatureModel]]:
        # Data loading implementation
        pass
```

### 2. 依存関係の設計

#### 依存関係の方向
```
API層 → サービス層 → リポジトリ層
  ↓        ↓           ↓
モデル層 ← モデル層 ← モデル層
```

#### 依存性注入パターン
- [ ] **インターフェース定義**: 抽象基底クラスによる契約
- [ ] **設定管理**: 設定ファイルによる実装切り替え
- [ ] **テスタビリティ**: モック・スタブによるテスト容易性

### 3. 技術的詳細設計

#### 設定管理 (`config/`)
```python
# config/settings.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    data_dir: Path = Path("data")
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
```

#### ログ・監視設計
- [ ] **構造化ログ**: JSON形式での統一ログ出力
- [ ] **パフォーマンス監視**: 処理時間・メモリ使用量の計測
- [ ] **エラー追跡**: スタックトレース・コンテキスト情報

#### 非同期処理設計
- [ ] **async/await**: I/O集約処理の非同期化
- [ ] **同期処理境界**: CPU集約処理との適切な分離
- [ ] **例外処理**: 非同期コンテキストでの例外管理

## 成果物

### 1. アーキテクチャドキュメント
- [ ] **層責任定義書**: 各層の責任範囲・境界
- [ ] **インターフェース仕様**: 層間通信の契約
- [ ] **データフロー図**: システム内でのデータの流れ
- [ ] **依存関係図**: コンポーネント間の依存関係

### 2. 実装ガイドライン
- [ ] **命名規則**: ファイル・クラス・関数の命名パターン
- [ ] **エラーハンドリング**: 統一的な例外処理方針
- [ ] **パフォーマンス指針**: 最適化の指針・計測方法
- [ ] **セキュリティ要件**: 各層でのセキュリティ実装

### 3. テスト戦略
- [ ] **ユニットテスト**: 各層の単体テスト方針
- [ ] **統合テスト**: 層間連携のテスト方針
- [ ] **エンドツーエンドテスト**: システム全体のテスト方針
- [ ] **テストデータ管理**: テスト用データの準備・管理

## 品質保証

### コード品質指標
- [ ] **テストカバレッジ**: 各層90%以上
- [ ] **型カバレッジ**: pyright strict mode合格
- [ ] **リント**: ruff ルール100%準拠
- [ ] **依存関係**: 循環依存の排除

### パフォーマンス要件
- [ ] **レスポンス時間**: API応答時間の目標値
- [ ] **メモリ使用量**: 各層のメモリ使用量上限
- [ ] **スケーラビリティ**: 負荷増加時の性能特性

---

## 次ステップ

### 実装計画への移行
```bash
/user:plan-implementation [この設計書のパス]
```

### GitHub Issue 更新
実装方針確定をissueに反映し、次フェーズに進む