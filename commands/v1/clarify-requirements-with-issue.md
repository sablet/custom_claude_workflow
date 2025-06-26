---
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task", "Bash"]
description: "Issue連動要求明確化：Issue内で曖昧な要求を実装可能な仕様に変換"
---

# Issue連動要求明確化: $ARGUMENTS

## 概要
GitHub Issue内の曖昧・抽象的な要求を分析し、実装可能な具体的仕様に変換。
明確化プロセスをIssue内で追跡し、後続ワークフローへの入力を準備。

## 実行前提条件
- GitHub Issue番号: $ARGUMENTS
- Issue内容: 曖昧または不完全な要求・仕様
- 成果物保存: `docs/issue-$ARGUMENTS/`

## 要求明確化フロー

### 1. Issue情報取得・初期化

#### Issue内容の読み込み
```bash
# Issue詳細情報の取得
!gh issue view $ARGUMENTS --json title,body,labels,assignees,milestone

# ドキュメント保存ディレクトリ作成
!mkdir -p "docs/issue-$ARGUMENTS"

# 元のIssue内容を保存
!gh issue view $ARGUMENTS > "docs/issue-$ARGUMENTS/00-original-issue.md"
```

### 2. 既存コードベース調査

#### 関連機能・パターンの特定
```bash
# Issue内容から関連キーワードを抽出して既存機能を調査
# (Issue本文から技術的キーワードを特定)

# 類似機能の検索
!rg -i "関連キーワード1|関連キーワード2" --type py -A 3 -B 3 > "docs/issue-$ARGUMENTS/existing-related-features.txt"

# 既存アーキテクチャパターンの確認
!find . -name "*.py" -path "*/service/*" | head -10 > "docs/issue-$ARGUMENTS/existing-architecture-patterns.txt"
!find . -name "*.py" -path "*/models/*" | head -10 >> "docs/issue-$ARGUMENTS/existing-architecture-patterns.txt"
```

### 3. 要求分析（Issue内容ベース）

#### Issue内容の構造化分析
```markdown
# docs/issue-$ARGUMENTS/01-requirements-analysis.md
# Issue #$ARGUMENTS 要求分析結果

## 元のIssue要求
[Issue #$ARGUMENTS の内容要約]

## What (何を実現するか)
### 機能の本質
- [ ] **主要機能**: [Issue要求から導出される核となる機能]
- [ ] **入力データ**: [処理対象となるデータの種類・形式]
- [ ] **出力結果**: [生成される結果・成果物の形式]
- [ ] **計算・処理ロジック**: [入力から出力への変換処理の特性]

### 機能スコープ
- [ ] **責任範囲**: [この機能が担当する処理の境界]
- [ ] **対象外範囲**: [意図的に除外する機能・処理]
- [ ] **既存機能との関係**: [利用・拡張・置換する既存コンポーネント]

## Why (なぜ必要か)
### 解決したい課題
- [ ] **現在の問題**: [既存の制約・不足・非効率性]
- [ ] **目標とする改善**: [実装により達成したい状態]
- [ ] **対象ユーザー**: [この機能の利用者・受益者]

### 技術的背景
- [ ] **技術的制約**: [現在のアーキテクチャで対応困難な理由]
- [ ] **システム上の位置づけ**: [全体アーキテクチャにおける役割]
- [ ] **発展可能性**: [将来的な機能拡張・改良の方向性]

## How (どのように実装するか)
### 実装対象ファイル（レイヤード設計）
#### 新規作成予定
- [ ] `src/service/[feature_service].py` - [ビジネスロジック層]
- [ ] `src/models/[feature_model].py` - [ドメインモデル層]
- [ ] `src/api/[feature_api].py` - [API/インターフェース層]
- [ ] `tests/test_[feature_module].py` - [対応するテストファイル]

#### 修正対象予定
- [ ] `src/service/[existing_service].py` - [既存サービスの拡張]
- [ ] `src/models/[data_models].py` - [データモデルの変更]

### インターフェース設計方針
#### 主要関数シグネチャ
```python
def [main_function_name](
    input_data: [InputDataType],
    config: [ConfigType] = None,
    **options
) -> [OutputType]:
    """[Issue要求に基づく機能の説明]
    
    Args:
        input_data: [入力データの説明・制約]
        config: [設定パラメータの説明]
        **options: [追加オプション]
    
    Returns:
        [OutputType]: [出力結果の説明・構造]
    
    Raises:
        [ExceptionType]: [発生条件]
    """
```

#### データ型設計
- `InputDataType`: [DataFrame/dict/list/custom class 等]
- `ConfigType`: [設定の構造・形式]
- `OutputType`: [結果の構造・形式]

### アーキテクチャ整合性
#### 統合方針
- [ ] **既存パターンとの整合**: [現在のアーキテクチャパターンを踏襲]
- [ ] **依存関係管理**: [新規依存ライブラリの最小化]
- [ ] **設定管理**: [既存の設定パターンとの統一]

#### データフロー設計
- [ ] **入力元**: [データソースの特定]
- [ ] **処理パイプライン**: [既存処理フローへの統合方法]
- [ ] **出力先**: [結果の保存・利用方法]

## 受け入れ基準
### 機能要件
- [ ] **What の実現**: [定義した主要機能が動作する]
- [ ] **Why の達成**: [期待する課題解決が得られる]
- [ ] **既存システムとの統合**: [既存機能と適切に連携する]
- [ ] **エラーハンドリング**: [適切な例外処理と回復機能]

### 品質要件
- [ ] **テスト対象**: [ユニット・統合・エンドツーエンドテストの範囲]
- [ ] **パフォーマンス**: [処理時間・メモリ使用量の目標値]
- [ ] **保守性**: [コードの可読性・拡張性]
- [ ] **セキュリティ**: [入力検証・権限管理の実装]

### テスト戦略
#### 受け入れテスト（主要テスト）
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

#### 単体テスト（最小限実装）
受け入れテストでカバーできない最小限のもののみ実装：
- [ ] **複雑なアルゴリズム**: 受け入れテストでは検証困難な計算処理
- [ ] **エラーハンドリング**: 異常系の境界値処理
- [ ] **純粋関数**: 副作用のない数値計算・データ変換の正確性

#### 特別要件テスト（該当する場合）
- [ ] **外部連携機能**: API・MCP等の外部サービス連携
- [ ] **機械学習機能**: 特徴量リーケージ・データ分離検証
- [ ] **パフォーマンス**: 大容量データ・高負荷時の動作

## 不明点・要確認事項
[分析時点で未解決・要確認の事項]

## 次ステップ
Issue要求の明確化完了。分析フェーズに進行可能。
```

### 4. Issue更新・明確化結果の共有

#### 明確化結果をIssueにコメント
```bash
!gh issue comment $ARGUMENTS --body "## 📋 要求明確化完了

### 🔍 分析結果
Issue要求の詳細分析を完了しました。

### 📄 成果物
- [要求分析結果](docs/issue-$ARGUMENTS/01-requirements-analysis.md)
- [既存機能調査](docs/issue-$ARGUMENTS/existing-related-features.txt)
- [アーキテクチャパターン確認](docs/issue-$ARGUMENTS/existing-architecture-patterns.txt)

### ✅ 明確化された内容
#### 主要機能
- [What セクションの要約]

#### 解決課題
- [Why セクションの要約]

#### 実装方針
- [How セクションの要約]

### 🎯 受け入れ基準
- [機能要件・品質要件の要約]

### ❓ 要確認事項
[未解決・要確認事項があれば記載]

### 🚀 次ステップ
要求明確化完了。以下コマンドで分析フェーズに進行:
\`\`\`bash
/user:v1:analyze-change-request-with-issue $ARGUMENTS
\`\`\`"

# ラベル更新
!gh issue edit $ARGUMENTS --add-label "requirements-clarified,ready-for-analysis"
```

### 5. 不明点の質問・確認

#### 要確認事項がある場合の処理
```bash
# 不明点がある場合は追加のコメントで質問
if [ -n "$UNCLEAR_POINTS" ]; then
!gh issue comment $ARGUMENTS --body "## ❓ 要求明確化での確認事項

以下の点について追加情報・判断が必要です：

### 技術的判断が必要な項目
- [技術選択肢・アーキテクチャ判断]

### 機能仕様の詳細確認
- [入出力仕様・処理詳細]

### 優先度・スコープの確認
- [実装範囲・段階的実装の可否]

**回答後、分析フェーズに進行可能です。**"
fi
```

## 完了処理

### 明確化状況の記録
```bash
# 明確化プロセスの完了記録
!cat > "docs/issue-$ARGUMENTS/clarification-status.json" << EOF
{
  "issue_number": "$ARGUMENTS",
  "clarification_completed": true,
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "unclear_points_count": 0,
  "ready_for_analysis": true,
  "artifacts": {
    "requirements_analysis": "docs/issue-$ARGUMENTS/01-requirements-analysis.md",
    "existing_features": "docs/issue-$ARGUMENTS/existing-related-features.txt",
    "architecture_patterns": "docs/issue-$ARGUMENTS/existing-architecture-patterns.txt"
  }
}
EOF
```

---

## 実行完了確認

### チェック項目
- [ ] Issue要求の曖昧性解消完了
- [ ] 実装可能な具体的仕様への変換完了
- [ ] 既存システムとの整合性確認完了
- [ ] Issue内での明確化プロセス記録完了
- [ ] 分析フェーズ開始準備完了

### 次フェーズ移行
```bash
/user:v1:analyze-change-request-with-issue $ARGUMENTS
```

## 使用例

```bash
# 曖昧なIssueの要求明確化
/user:v1:clarify-requirements-with-issue 123

# 不完全な仕様のIssueの詳細化
/user:v1:clarify-requirements-with-issue 456
```