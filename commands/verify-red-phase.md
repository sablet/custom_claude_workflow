---
allowed-tools: ["Bash", "Read", "Grep"]
description: "Red Phase検証：テスト失敗確認とTDDサイクル準備"
---

# Red Phase 検証: $ARGUMENTS

## 前提条件

### 入力
実装ディレクトリ: $ARGUMENTS

### Red Phase の意義
- **TDD の出発点**: テストが失敗することで実装すべき内容を明確化
- **テスト品質確認**: テストが正しく期待値を検証していることを確認
- **実装ガイド**: 失敗メッセージから実装すべき機能を特定

## 検証実行

### 1. 環境・依存関係確認

#### Python環境チェック
!uv --version
!python --version

#### プロジェクト依存関係
!cd $ARGUMENTS && uv sync

#### パッケージ構造確認
!cd $ARGUMENTS && find src -name "*.py" | head -20

### 2. 静的解析実行

#### 型チェック（pyright）
!cd $ARGUMENTS && uv run --frozen pyright src/

**期待結果**: 型エラーなし（シグネチャが正しく定義されている）

#### リント・フォーマットチェック（ruff）
!cd $ARGUMENTS && uv run --frozen ruff check src/
!cd $ARGUMENTS && uv run --frozen ruff format --check src/

**期待結果**: リントエラーなし（コード品質が標準に準拠）

### 3. インポート・基本動作確認

#### 基本インポートテスト
!cd $ARGUMENTS && uv run python -c "
try:
    from src.models.input_model import InputModel
    from src.models.output_model import OutputModel
    from src.api.main_api import MainAPI
    from src.service.main_service import MainService
    print('✓ 基本インポート成功')
except ImportError as e:
    print(f'✗ インポートエラー: {e}')
    exit(1)
"

#### インスタンス作成テスト
!cd $ARGUMENTS && uv run python -c "
from src.models.input_model import InputModel
from src.api.main_api import MainAPI

try:
    # 正常なデータでのインスタンス作成
    input_data = InputModel(field1='test', field2=42, field3=['item1', 'item2'])
    api = MainAPI()
    print('✓ インスタンス作成成功')
    print(f'  入力データ: {input_data}')
except Exception as e:
    print(f'✗ インスタンス作成エラー: {e}')
    exit(1)
"

### 4. Red Phase テスト実行

#### 受け入れテスト実行（詳細出力）
!cd $ARGUMENTS && uv run --frozen pytest tests/acceptance/ -v -s --tb=short

#### テスト結果の分析
!cd $ARGUMENTS && uv run --frozen pytest tests/acceptance/ --tb=no -q

#### 個別テストクラス実行
!cd $ARGUMENTS && uv run --frozen pytest tests/acceptance/ -k "TestMainFeatureAcceptance" -v

### 5. 失敗パターン分析

#### 期待される失敗パターン確認
!cd $ARGUMENTS && uv run python -c "
from src.api.main_api import MainAPI
from src.models.input_model import InputModel

api = MainAPI()
input_data = InputModel(field1='test', field2=100, field3=['item'])

try:
    result = api.process_main_feature(input_data)
    print('実行結果:')
    print(f'  ステータス: {result.status}')
    print(f'  エラーメッセージ: {result.error_message}')
    
    if result.status == 'error':
        print('✓ 期待通り失敗ステータス（Red Phase正常）')
    else:
        print('⚠ 予期しない成功（実装が進んでいる可能性）')
        
except Exception as e:
    print(f'✓ 期待通り例外発生: {e}')
    if 'NotImplementedError' in str(e):
        print('✓ NotImplementedError確認（Red Phase正常）')
except:
    print('✗ 予期しないエラー形式')
"

### 6. テストカバレッジ確認

#### カバレッジ測定
!cd $ARGUMENTS && uv run --frozen pytest tests/acceptance/ --cov=src --cov-report=term-missing --cov-report=html

**期待結果**: 
- カバレッジレポート生成成功
- テスト実行時にソースコードが実行されている
- 未実装部分が明確に特定される

### 7. ログ・デバッグ情報確認

#### デバッグ実行
!cd $ARGUMENTS && uv run python -c "
import logging
logging.basicConfig(level=logging.DEBUG)

from src.api.main_api import MainAPI
from src.models.input_model import InputModel

api = MainAPI()
input_data = InputModel(field1='debug_test', field2=1, field3=['debug'])

print('=== デバッグ実行開始 ===')
try:
    result = api.process_main_feature(input_data)
    print(f'結果ステータス: {result.status}')
    if result.data:
        print(f'データ: {result.data}')
    if result.error_message:
        print(f'エラー: {result.error_message}')
except Exception as e:
    print(f'例外: {type(e).__name__}: {e}')
print('=== デバッグ実行終了 ===')
"

## Red Phase 検証結果

### ✅ 成功条件
- [ ] **型チェック合格**: pyright でエラーなし
- [ ] **リント合格**: ruff check でエラーなし  
- [ ] **インポート成功**: 全モジュールが正しくインポート可能
- [ ] **インスタンス作成**: 基本的なクラスインスタンス化が成功
- [ ] **テスト失敗**: 受け入れテストが期待通り失敗
- [ ] **失敗理由明確**: NotImplementedError または期待値不一致
- [ ] **カバレッジ測定**: テスト実行時にコードが実行されている

### ⚠️ 注意すべき状況
- **テストが成功**: 実装が予想以上に進んでいる
- **インポートエラー**: シグネチャ実装に問題
- **型エラー**: 型定義に不整合
- **予期しない例外**: エラーハンドリングに問題

### ❌ 問題のあるパターン
- **テストが実行されない**: テスト環境の問題
- **モジュールが見つからない**: プロジェクト構造の問題
- **型チェック失敗**: 型定義の問題
- **全テストが成功**: Red Phase の目的が達成されていない

## トラブルシューティング

### よくある問題と対処法

#### 1. インポートエラー
```bash
# PYTHONPATH の確認・設定
cd $ARGUMENTS && PYTHONPATH=. uv run python -c "import src.models.input_model"
```

#### 2. 型エラー
```bash
# 詳細な型エラー表示
cd $ARGUMENTS && uv run --frozen pyright src/ --verbose
```

#### 3. テスト環境問題
```bash
# テスト依存関係の確認
cd $ARGUMENTS && uv run --frozen pytest --version
cd $ARGUMENTS && uv run --frozen pytest --collect-only tests/acceptance/
```

#### 4. 予期しない成功
実装が進みすぎている場合は、以下を確認：
- ビジネスロジックが実装されていないか
- テストの期待値が正しく設定されているか
- モックが適切に設定されているか

## 品質保証チェックリスト

### 技術品質
- [ ] **型安全性**: pyright strict mode 合格
- [ ] **コード品質**: ruff 100%準拠
- [ ] **実行可能性**: 基本的な実行が可能
- [ ] **テスト実行**: pytest が正常に動作

### TDD品質
- [ ] **適切な失敗**: テストが期待通り失敗
- [ ] **失敗理由明確**: 何を実装すべきかが明確
- [ ] **段階的実装**: 一度にすべてを実装しない設計
- [ ] **リファクタ準備**: 後のリファクタに備えた構造

---

## 次ステップ

### Green Phase 開始
```bash
/user:implement-logic $ARGUMENTS
```

### GitHub Issue 更新
Red Phase確認完了をissueに反映し、実装フェーズに進む