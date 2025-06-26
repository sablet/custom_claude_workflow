---
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
description: "要求分析・明確化：曖昧な要求から実装可能な仕様を定義"
---

# 要求分析・明確化: $ARGUMENTS

## 概要
**特殊用途**: 正式Issue化前の事前要求分析用。
曖昧・抽象的な要求を分析し、実装可能な具体的仕様に変換する。
分析結果を基にIssue作成を行う。

**注意**: 既存Issueがある場合は `/user:v1:clarify-requirements-with-issue [Issue番号]` を使用してください。

## 実行前提条件
- 分析対象: @$ARGUMENTS (要求文書・Issue・仕様の断片)
- 成果物保存: `docs/requirements-analysis-$(date +%Y%m%d-%H%M%S)/`

## 要求分析フロー

### 1. 既存コードベース調査

#### 関連機能・パターンの特定
```bash
# 出力ディレクトリ作成
!mkdir -p "docs/requirements-analysis-$(date +%Y%m%d-%H%M%S)"
!echo "docs/requirements-analysis-$(date +%Y%m%d-%H%M%S)" > output/current-requirements-dir.txt

# 既存の類似機能・関連モジュールを調査
# (要求内容から抽出したキーワードで検索)
```

### 2. 要求分析（全体フロー向け）

#### What (何を実現するか)
**機能の本質**
- [ ] **主要機能**: [ユーザー要求から導出される核となる機能]
- [ ] **入力データ**: [処理対象となるデータの種類・形式]
- [ ] **出力結果**: [生成される結果・成果物の形式]
- [ ] **計算・処理ロジック**: [入力から出力への変換処理の特性]

**機能スコープ**
- [ ] **責任範囲**: [この機能が担当する処理の境界]
- [ ] **対象外範囲**: [意図的に除外する機能・処理]
- [ ] **既存機能との関係**: [利用・拡張・置換する既存コンポーネント]

#### Why (なぜ必要か)
**解決したい課題**
- [ ] **現在の問題**: [既存の制約・不足・非効率性]
- [ ] **目標とする改善**: [実装により達成したい状態]
- [ ] **対象ユーザー**: [この機能の利用者・受益者]

**技術的背景**
- [ ] **技術的制約**: [現在のアーキテクチャで対応困難な理由]
- [ ] **システム上の位置づけ**: [全体アーキテクチャにおける役割]
- [ ] **発展可能性**: [将来的な機能拡張・改良の方向性]

### 3. 成果物定義（実装指向）

#### 実装対象ファイル（レイヤード設計）
**新規作成予定**
- [ ] `src/service/[feature_service].py` - [ビジネスロジック層]
- [ ] `src/models/[feature_model].py` - [ドメインモデル層]
- [ ] `src/api/[feature_api].py` - [API/インターフェース層]
- [ ] `tests/test_[feature_module].py` - [対応するテストファイル]
- [ ] `config/[feature_config].py` - [設定ファイル（必要時）]

**修正対象予定**
- [ ] `src/service/[existing_service].py` - [既存サービスの拡張]
  - 関数: `existing_function()` - [統合・拡張内容]
  - クラス: `ExistingService` - [新機能追加]
- [ ] `src/models/[data_models].py` - [データモデルの変更]
  - クラス: `DataModel` - [新規フィールド・メソッド追加]

#### インターフェース設計方針
**主要関数シグネチャ**
```python
def [main_function_name](
    input_data: [InputDataType],
    config: [ConfigType] = None,
    **options
) -> [OutputType]:
    """[Description of main function defined in What section]
    
    Args:
        input_data: [Description and constraints of input data]
        config: [Description of configuration parameters]
        **options: [Additional options]
    
    Returns:
        [OutputType]: [Description and structure of output result]
    
    Raises:
        [ExceptionType]: [Occurrence conditions]
    """
```

**データ型設計**
- `InputDataType`: [DataFrame/dict/list/custom class 等]
- `ConfigType`: [設定の構造・形式]
- `OutputType`: [結果の構造・形式]

**API設計思想**
- **シンプルさ**: [複雑な設定を内部で処理]
- **柔軟性**: [複数の入力形式・オプションに対応]
- **一貫性**: [既存の命名規則・パターンを踏襲]

#### アーキテクチャ整合性の確認
**統合方針**
- [ ] **既存パターンとの整合**: [現在のアーキテクチャパターンを踏襲]
- [ ] **依存関係管理**: [新規依存ライブラリの最小化]
- [ ] **設定管理**: [既存の設定パターンとの統一]

**データフロー設計**
- [ ] **入力元**: [データソースの特定]
- [ ] **処理パイプライン**: [既存処理フローへの統合方法]
- [ ] **出力先**: [結果の保存・利用方法]

### 4. 受け入れ基準（開発向け）

#### 機能要件
- [ ] **What の実現**: [定義した主要機能が動作する]
- [ ] **Why の達成**: [期待する課題解決が得られる]
- [ ] **既存システムとの統合**: [既存機能と適切に連携する]
- [ ] **エラーハンドリング**: [適切な例外処理と回復機能]

#### 品質要件
- [ ] **テスト対象**: [ユニット・統合・エンドツーエンドテストの範囲]
- [ ] **パフォーマンス**: [処理時間・メモリ使用量の目標値]
- [ ] **保守性**: [コードの可読性・拡張性]
- [ ] **セキュリティ**: [入力検証・権限管理の実装]

#### テスト戦略判定
要求内容に基づいて適切なテスト戦略を選択：

**一般ケース**
- [ ] **標準テスト**: シンプルな単体テスト・統合テスト・受け入れテスト

**追加テスト（該当する場合）**
- [ ] **A: 外部連携機能** (API、MCP等)
  - インターフェース契約テスト
  - 外部サービスとの統合テスト
  - APIレスポンス形式・エラーハンドリングテスト

- [ ] **B: 機械学習系機能**
  - 特徴量リーケージ対策テスト
    - ラベルと特徴量の相関係数チェック（閾値: 0.8以上でテスト失敗）
    - 時系列データでの未来情報使用検出
    - 訓練・テストデータ分離の検証

#### 検証方法
**自動テスト（uv + ruff + pyright）**
```bash
# テスト実行
uv run --frozen pytest tests/test_[feature_module].py -v

# カバレッジ付きテスト
uv run --frozen pytest --cov=src --cov-report=html

# コード品質チェック
uv run --frozen ruff check .
uv run --frozen ruff format .
uv run --frozen pyright
```

**手動確認**
1. [主要機能の動作確認手順]
2. [エラーケース・境界値の確認]
3. [既存機能への影響確認]

## 成果物生成

### 要求分析レポート作成
`docs/requirements-analysis-*/requirements-specification.md` に以下内容を出力:

```markdown
# 要求分析結果: [要求名]

## 1. 要求概要
### 元の要求
[分析対象の原文・要約]

### 解決したい課題
[Why セクションの分析結果]

## 2. 機能仕様
### 主要機能定義
[What セクションの分析結果]

### 機能スコープ
[実装範囲・除外範囲の明確化]

## 3. 技術仕様
### アーキテクチャ要件
[既存システムとの統合方針]

### 実装対象
[新規作成・修正対象ファイルの詳細]

### インターフェース設計
[関数シグネチャ・データ型の具体的設計]

## 4. 品質・テスト要件
### 受け入れ基準
[機能・品質要件の具体的基準]

### テスト戦略
[必要なテストの種類・範囲]

## 5. 実装準備
### 次ステップ
- Issue作成またはワークフロー開始の準備完了
- 実装可能な具体的仕様への変換完了

### 残課題
[分析時点で未解決・要確認の事項]
```

## 実行完了処理

### GitHub Issue作成準備
```bash
# Issue作成用の情報整理
!cat > "$(cat output/current-requirements-dir.txt)/issue-template.md" << 'EOF'
# Feature: [要求名]

## 概要
[要求分析結果の要約]

## 仕様書
- [要求分析レポート]($(cat output/current-requirements-dir.txt)/requirements-specification.md)

## 受け入れ基準
[品質要件から抜粋した基準]

## 実装方針
[技術仕様セクションの要約]
EOF
```

### ワークフロー連携準備
要求分析完了後、以下の選択肢を提示：

1. **GitHub Issue作成**
```bash
gh issue create --title "Feature: [要求名]" --body-file "$(cat output/current-requirements-dir.txt)/issue-template.md"
```

2. **直接ワークフロー開始**
```bash
/user:v1:start-workflow-from-issue [作成されたIssue番号]
```

---

## 実行完了確認

### チェック項目
- [ ] 要求の曖昧性解消完了
- [ ] 実装可能な具体的仕様への変換完了
- [ ] 既存システムとの整合性確認完了
- [ ] Issue作成またはワークフロー開始準備完了

### 次ステップ選択
- **Issue作成**: 要求を正式なIssueとして管理
- **ワークフロー開始**: 直接実装フェーズに移行

## 使用例

```bash
# 曖昧な要求文書の分析
/user:v1:clarify-requirements "ユーザーがデータをアップロードして分析結果を見られるようにしたい"

# Issue内容の詳細化
/user:v1:clarify-requirements "Issue #123の要求を詳細化"

# 仕様書の補完
/user:v1:clarify-requirements specs/rough-requirements.md
```