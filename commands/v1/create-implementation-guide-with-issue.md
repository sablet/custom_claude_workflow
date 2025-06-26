---
allowed-tools: ["Read", "Write", "Grep", "Glob", "Task", "Bash"]
description: "Issue連動実装ガイド作成（Step6-7）: 分析結果から完全実装ガイド作成"
---

# Issue連動実装ガイド作成: $ARGUMENTS

## 概要
分析フェーズの結果を活用し、Issue要求に対する完全な実装ガイドを作成。
成果物を `docs/issue-[番号]/implementation/` に保存し、Issue進捗を更新。

## 実行前提条件
- GitHub Issue番号: $ARGUMENTS
- 分析フェーズ完了: `docs/issue-$ARGUMENTS/analysis/` 成果物一式
- 前フェーズ: `/user:v1:analyze-change-request-with-issue $ARGUMENTS` 実行済み

## 実装ガイド作成フェーズ実行

### Step 6: 実コードベース検証・シンタックス確認

#### 分析結果の読み込み
```bash
# 進捗状況更新
!cat "docs/issue-$ARGUMENTS/workflow-status.json" | jq '.phases.implementation_guide.status = "in_progress" | .phases.implementation_guide.steps.step6_syntax_validation = "in_progress"' > temp.json && mv temp.json "docs/issue-$ARGUMENTS/workflow-status.json"

# 分析フェーズの結果読み込み
!cat "docs/issue-$ARGUMENTS/05-analysis-summary.md"
!cat "docs/issue-$ARGUMENTS/02-related-files.json"
!cat "docs/issue-$ARGUMENTS/03-implementation-plan.md"
```

#### 実装対象ファイルの詳細検証
```bash
# Step 2で特定されたファイルの詳細読み取り
# (02-related-files.jsonから対象ファイルを抽出)

# 既存コードの構文・スタイル確認
!find . -name "*.py" -exec head -20 {} \; | grep -E "(import|from|class|def)" > "docs/issue-$ARGUMENTS/existing-code-patterns.txt"

# 型チェック・リントの現状確認
!which pyright > "docs/issue-$ARGUMENTS/toolchain-status.txt" 2>&1 || echo "pyright not found" >> "docs/issue-$ARGUMENTS/toolchain-status.txt"
!which ruff >> "docs/issue-$ARGUMENTS/toolchain-status.txt" 2>&1 || echo "ruff not found" >> "docs/issue-$ARGUMENTS/toolchain-status.txt"
```

#### 技術的実現可能性検証
```markdown
# docs/issue-$ARGUMENTS/06-syntax-validation.md
# Step 6: 技術検証結果

## Issue要求の技術的検証
### 実装可能性評価
[Issue #$ARGUMENTS の技術的実現可能性]

## 既存コードベース整合性
### コードスタイル・パターン
[既存コードとの整合性確認]

### 型システム整合性  
[型ヒント・型チェッカーとの互換性]

### 依存関係検証
[Import・モジュール依存の実現可能性]

## 実装制約・課題
### 技術的制約
[実装時の技術的制限事項]

### 解決済み課題
[分析時の課題に対する解決策]

### 残存課題
[実装時に解決が必要な課題]

## テスト環境検証
### 既存テスト実行状況
[現在のテスト実行結果]

### 新規テスト要件
[Issue要求に必要なテスト実装]

## 品質保証準備
### 自動化ツール確認
[ruff, pyright等の利用可能性]

### CI/CD準備
[継続的インテグレーション環境の確認]
```

### Step 7: 最終実装計画・完全ガイド作成

#### 完全実装ガイドの作成
```bash
# 進捗状況更新
!cat "docs/issue-$ARGUMENTS/workflow-status.json" | jq '.phases.implementation_guide.steps.step7_final_guide = "in_progress"' > temp.json && mv temp.json "docs/issue-$ARGUMENTS/workflow-status.json"
```

#### 詳細実装ガイド（10-15K tokens）
```markdown
# docs/issue-$ARGUMENTS/07-final-implementation-guide.md
# Issue #$ARGUMENTS 完全実装ガイド

## 1. 実装概要
### Issue要求サマリー
[Issue #$ARGUMENTS の実装要求の明確化]

### 技術的アプローチ
[選択した実装手法の詳細]

### 全体アーキテクチャへの組み込み
[既存システムへの統合方法]

## 2. 実装前準備
### 環境セットアップ
```bash
# 必要な依存関係の追加
uv add 新規ライブラリ名

# 開発環境の準備
uv sync
```

### ブランチ戦略
```bash
# Issue対応ブランチの作成
git checkout -b feature/issue-$ARGUMENTS-[機能名]
```

### ディレクトリ準備
```bash
# 必要なディレクトリの作成
mkdir -p src/service/新機能
mkdir -p tests/unit/新機能
```

## 3. ファイル別詳細実装

### 3.1 新規ファイル: src/models/issue_$ARGUMENTS_model.py
```python
"""
Issue #$ARGUMENTS 対応の新規データモデル
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class Issue${ARGUMENTS}Model(BaseModel):
    """Issue #$ARGUMENTS で要求された機能のデータモデル"""
    
    # Issue要求に基づく具体的なフィールド定義
    field1: str = Field(..., description="Issue要求の主要データ")
    field2: Optional[int] = Field(None, ge=0, description="Issue要求の数値データ")
    created_at: datetime = Field(default_factory=datetime.now)
    
    @validator('field1')
    def validate_field1(cls, v):
        """Issue要求の制約に基づくバリデーション"""
        if not v.strip():
            raise ValueError("field1 cannot be empty")
        return v.strip()
    
    class Config:
        # 設定
        validate_assignment = True
        extra = "forbid"
```

### 3.2 新規ファイル: src/service/issue_$ARGUMENTS_service.py
```python
"""
Issue #$ARGUMENTS 対応のビジネスロジック
"""
from typing import List, Optional
from src.models.issue_${ARGUMENTS}_model import Issue${ARGUMENTS}Model
from src.repository.base_repository import BaseRepository

class Issue${ARGUMENTS}Service:
    """Issue #$ARGUMENTS で要求された機能のサービス層"""
    
    def __init__(self, repository: BaseRepository):
        self.repository = repository
    
    async def process_issue_request(self, data: Issue${ARGUMENTS}Model) -> Issue${ARGUMENTS}Model:
        """Issue要求のメイン処理ロジック"""
        
        # Issue要求に基づく具体的なビジネスロジック
        # 1. データ検証
        validated_data = self._validate_issue_data(data)
        
        # 2. ビジネスルール適用
        processed_data = self._apply_business_rules(validated_data)
        
        # 3. データ永続化
        result = await self.repository.save(processed_data)
        
        return result
    
    def _validate_issue_data(self, data: Issue${ARGUMENTS}Model) -> Issue${ARGUMENTS}Model:
        """Issue特有のデータ検証"""
        # Issue要求に基づく検証ロジック
        return data
    
    def _apply_business_rules(self, data: Issue${ARGUMENTS}Model) -> Issue${ARGUMENTS}Model:
        """Issue要求のビジネスルール適用"""
        # Issue要求に基づくビジネスロジック
        return data
```

### 3.3 既存ファイル修正: src/api/main_api.py
```python
# 既存のmain_api.pyに以下を追加

from src.service.issue_${ARGUMENTS}_service import Issue${ARGUMENTS}Service
from src.models.issue_${ARGUMENTS}_model import Issue${ARGUMENTS}Model

# 新規エンドポイントの追加
@router.post("/issue-$ARGUMENTS", response_model=Issue${ARGUMENTS}Model)
async def handle_issue_$ARGUMENTS(
    request: Issue${ARGUMENTS}Model,
    service: Issue${ARGUMENTS}Service = Depends()
) -> Issue${ARGUMENTS}Model:
    """Issue #$ARGUMENTS 対応の新規エンドポイント"""
    return await service.process_issue_request(request)
```

## 4. テスト実装戦略

### 4.1 受け入れテスト（主要テスト）: tests/acceptance/test_issue_$ARGUMENTS_acceptance.py
受け入れテストは以下の形式で記述し、ユーザーが実際に機能を使用する際の期待される動作を検証する：

**ユーザー要求形式:**
- [ ] **As a** [利用者], **I want to** [機能/処理] **so that** [得られる結果/価値]

**Given-When-Then (シナリオテスト) 形式:**
- [ ] **Given** [入力データ・環境条件]
- [ ] **When** [機能実行・処理開始]  
- [ ] **Then** [期待される出力・結果]

**機能統合テスト:**
- [ ] 機能がユーザーの要求をどのように満たすかを検証
- [ ] 入力から出力までの全体的な動作を確認
- [ ] 具体的な内部実装ではなく、機能の外部仕様・動作を重視

```python
"""
Issue #$ARGUMENTS 受け入れテスト
"""
import pytest
from fastapi.testclient import TestClient
from src.api.main_api import app

class TestIssue${ARGUMENTS}Acceptance:
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_user_story_as_api_user_i_want_to_process_issue_request(self, client):
        """ユーザーストーリー形式:
        As a API利用者, I want to Issue要求を処理 so that ビジネス価値を得られる
        """
        # Given [前提条件]
        valid_request_data = {
            "field1": "business_value_data",
            "field2": 100
        }
        
        # When [行動/イベント]
        response = client.post("/issue-$ARGUMENTS", json=valid_request_data)
        
        # Then [期待される結果]
        assert response.status_code == 200
        result = response.json()
        assert "field1" in result  # ビジネス価値の確認
        assert result["field2"] > 0  # ビジネスルール適用確認
    
    def test_feature_integration_complete_process(self, client):
        """機能統合テスト:
        Issue要求がユーザーの要求をどのように満たすかを検証
        """
        # Given: 実際のユースケースに基づく入力データ
        real_world_scenario_data = {
            "field1": "real_world_scenario",
            "field2": 250
        }
        
        # When: 機能実行・処理開始
        response = client.post("/issue-$ARGUMENTS", json=real_world_scenario_data)
        
        # Then: 期待される出力・結果
        assert response.status_code == 200
        result = response.json()
        # 機能の外部仕様・動作を重視した確認
        assert result["field1"] == "real_world_scenario"
        # 機能の動作がユーザー要求にどう応えるか確認
        assert "created_at" in result
```

### 4.2 単体テスト（最小限実装）: tests/unit/test_issue_$ARGUMENTS_service.py
受け入れテストでカバーできない最小限のもののみ実装：
- [ ] **複雑なアルゴリズム**: 受け入れテストでは検証困難な内部処理
- [ ] **エラーハンドリング**: 異常系の境界値処理
- [ ] **純粋関数**: 副作用のない計算処理の正確性

```python
"""
Issue #$ARGUMENTS サービスの単体テスト（最小限）
"""
import pytest
from unittest.mock import Mock, AsyncMock
from src.service.issue_${ARGUMENTS}_service import Issue${ARGUMENTS}Service
from src.models.issue_${ARGUMENTS}_model import Issue${ARGUMENTS}Model

class TestIssue${ARGUMENTS}ServiceMinimal:
    @pytest.fixture
    def mock_repository(self):
        repository = Mock()
        repository.save = AsyncMock()
        return repository
    
    @pytest.fixture
    def service(self, mock_repository):
        return Issue${ARGUMENTS}Service(mock_repository)
    
    @pytest.mark.asyncio
    async def test_complex_algorithm_internal_processing(self, service):
        """複雑なアルゴリズム: 受け入れテストでは検証困難な内部処理"""
        # 受け入れテストではカバーできない複雑な内部計算のみテスト
        pass
    
    @pytest.mark.asyncio
    async def test_error_handling_boundary_values(self, service):
        """エラーハンドリング: 異常系の境界値処理"""
        # 異常系の境界値のみ、受け入れテストでカバーしきれない場合にテスト
        invalid_data = Issue${ARGUMENTS}Model(
            field1="",  # 境界値エラー
            field2=-1   # 境界値エラー
        )
        
        with pytest.raises(ValueError):
            await service.process_issue_request(invalid_data)
    
    def test_pure_function_calculation_accuracy(self):
        """純粋関数: 副作用のない計算処理の正確性"""
        # 副作用のない純粋な計算のみ、必要に応じてテスト
        pass
```

## 5. 品質保証

### 5.1 コードレビュー項目
- [ ] Issue要求の実装完全性
- [ ] 既存コードとの整合性
- [ ] エラーハンドリングの適切性
- [ ] テストカバレッジの充分性
- [ ] ドキュメント整備

### 5.2 自動化検証
```bash
# 型チェック
uv run --frozen pyright src/

# リント
uv run --frozen ruff check .

# フォーマット
uv run --frozen ruff format .

# テスト実行
uv run --frozen pytest tests/ -v

# カバレッジ確認
uv run --frozen pytest --cov=src --cov-report=html
```

### 4.3 特別要件テスト（該当する場合）: tests/special/test_issue_$ARGUMENTS_special.py
- [ ] **外部連携機能**: API・MCP等の外部サービス連携
- [ ] **機械学習機能**: 特徴量リーケージ・データ分離検証
- [ ] **パフォーマンス**: 大容量データ・高負荷時の動作

```python
# tests/special/test_issue_$ARGUMENTS_special.py
def test_external_api_integration():
    """外部連携機能: API・MCP等の外部サービス連携"""
    # 外部サービス連携が必要な場合のみ実装
    pass

def test_machine_learning_data_leakage():
    """機械学習機能: 特徴量リーケージ・データ分離検証"""
    # 機械学習機能が含まれる場合のみ実装
    pass

def test_performance_requirements():
    """パフォーマンス: 大容量データ・高負荷時の動作"""
    # 大容量データ処理・パフォーマンス要件が重要な場合のみ実装
    pass
```

### 5.3 テスト戦略の実装優先度
1. **受け入れテスト**: 必須実装（ユーザー価値を検証）
2. **単体テスト**: 受け入れテストで不足する部分のみ最小限実装
3. **特別要件テスト**: プロジェクト要件に応じて選択的実装

## 6. デプロイメント

### 6.1 設定変更
```bash
# 環境変数の追加（必要に応じて）
echo "ISSUE_$ARGUMENTS_FEATURE_ENABLED=true" >> .env
```

### 6.2 マイグレーション（必要に応じて）
```python
# データベースマイグレーション等
```

### 6.3 ロールバック手順
```bash
# Issue #$ARGUMENTS 機能の無効化方法
# 1. 環境変数での機能無効化
# 2. API エンドポイントの無効化
# 3. 必要に応じてデータロールバック
```

## 7. 実装完了チェックリスト
- [ ] 全実装ファイルの作成・修正完了
- [ ] 受け入れテスト実装・実行成功（主要検証）
- [ ] 単体テスト実装・実行成功（最小限）
- [ ] 特別要件テスト実装・実行成功（必要に応じて）
- [ ] 品質チェック（lint, type, format）完了
- [ ] パフォーマンステスト実行・基準クリア
- [ ] エラーハンドリング確認完了
- [ ] ドキュメント更新完了
- [ ] ロールバック手順確認完了

## 8. 実装後の検証
### 8.1 機能テスト
- Issue要求の全機能が正常動作すること
- エラーケースが適切に処理されること
- パフォーマンス要件を満たすこと

### 8.2 回帰テスト
- 既存機能に影響がないこと
- 既存テストが全て成功すること
```

#### 実装チェックリスト作成
```markdown
# docs/issue-$ARGUMENTS/08-implementation-checklist.md
# Issue #$ARGUMENTS 実装チェックリスト

## 実装前準備
- [ ] 環境セットアップ完了
- [ ] ブランチ作成完了
- [ ] 依存関係追加完了

## コード実装
- [ ] データモデル実装完了
- [ ] サービス層実装完了
- [ ] API層実装完了
- [ ] リポジトリ層実装完了（必要に応じて）

## テスト実装（新戦略）
- [ ] 受け入れテスト実装完了（主要・必須）
- [ ] 単体テスト実装完了（最小限のみ）
- [ ] 特別要件テスト実装完了（必要に応じて）

## 品質保証
- [ ] 型チェック合格
- [ ] リント合格
- [ ] フォーマット適用
- [ ] テストカバレッジ基準クリア
- [ ] コードレビュー完了

## ドキュメント
- [ ] API仕様書更新
- [ ] README更新（必要に応じて）
- [ ] 実装ドキュメント作成

## デプロイ準備
- [ ] 設定ファイル更新
- [ ] マイグレーション準備
- [ ] ロールバック手順確認
- [ ] デプロイメントスクリプト更新

## 最終確認
- [ ] Issue要求の全項目実装完了
- [ ] 受け入れ基準全クリア
- [ ] パフォーマンス要件クリア
- [ ] セキュリティ要件クリア
```

## 実装ガイド完了処理

### 進捗状況最終更新
```bash
# 実装ガイド作成完了
!cat "docs/issue-$ARGUMENTS/workflow-status.json" | jq '.phases.implementation_guide.status = "completed" | .phases.implementation_guide.steps.step6_syntax_validation = "completed" | .phases.implementation_guide.steps.step7_final_guide = "completed"' > temp.json && mv temp.json "docs/issue-$ARGUMENTS/workflow-status.json"
```

### Issue進捗コメント
```bash
# 実装ガイド完了をIssueに報告
!gh issue comment $ARGUMENTS --body "## 📋 実装ガイド作成完了

### 🚀 成果物
- [技術検証レポート](docs/issue-$ARGUMENTS/06-syntax-validation.md)
- [**完全実装ガイド**](docs/issue-$ARGUMENTS/07-final-implementation-guide.md) (10-15K tokens)
- [実装チェックリスト](docs/issue-$ARGUMENTS/08-implementation-checklist.md)

### ✅ 実装準備完了
- 全ての技術的制約を解決
- コピー&ペースト可能な詳細実装指示
- 完全なテスト戦略・品質保証手順

### 🔧 実装開始
以下コマンドで実装を開始:
\`\`\`bash
/user:v1:implement-from-guide $ARGUMENTS
\`\`\`

### 📁 成果物アクセス
- **ワークフロー文書**: [docs/issue-$ARGUMENTS/](docs/issue-$ARGUMENTS/)"

# ラベル更新
!gh issue edit $ARGUMENTS --add-label "implementation-ready" --remove-label "analysis-completed,review-needed"
```

---

## 実行完了確認

### チェック項目
- [ ] Step 6, 7の成果物生成完了
- [ ] `docs/issue-$ARGUMENTS/` に全ファイル保存完了
- [ ] 進捗状況JSON更新完了
- [ ] Issue進捗コメント投稿完了

### 次フェーズ移行
```bash
/user:v1:implement-from-guide $ARGUMENTS
```