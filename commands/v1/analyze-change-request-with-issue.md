---
allowed-tools: ["Read", "Write", "Grep", "Glob", "Task", "Bash"]
description: "Issue連動分析フェーズ（Step1-4）: Issue情報を起点とした分析"
---

# Issue連動分析フェーズ: $ARGUMENTS

## 概要
GitHub Issue情報を起点として変更要求分析を実行。
成果物を `docs/issue-[番号]/analysis/` に保存し、Issue進捗を更新。

## 実行前提条件
- GitHub Issue番号: $ARGUMENTS
- Issue内容: 変更要求・仕様の記載
- 事前実行: `/user:v1:start-workflow-from-issue $ARGUMENTS` 

## 分析フェーズ実行

### Step 1: コードベース分析・データフロー特定

#### Issue内容の分析
```bash
# Issue詳細情報の読み込み
!cat "docs/issue-$ARGUMENTS/original-issue.md"

# Issue内容から要求事項・キーワードを抽出
# (Issue本文から変更要求の技術的要素を特定)
```

#### コードベース調査
```bash
# 進捗状況更新
!cat "docs/issue-$ARGUMENTS/workflow-status.json" | jq '.phases.analysis.steps.step1_codebase_analysis = "in_progress"' > temp.json && mv temp.json "docs/issue-$ARGUMENTS/workflow-status.json"

# プロジェクト構造の調査
!find . -type f -name "*.py" | head -20 > "docs/issue-$ARGUMENTS/project-structure.txt"
!ls -la | grep -E "(pyproject|setup|requirements|Pipfile|uv)" >> "docs/issue-$ARGUMENTS/project-structure.txt"

# Issue要求に関連するキーワード検索
# (Issueから抽出したキーワードを使用)
!rg -i "キーワード1|キーワード2" --type py -A 3 -B 3 > "docs/issue-$ARGUMENTS/related-code-search.txt"
```

#### 成果物生成
```markdown
# docs/issue-$ARGUMENTS/01-codebase-analysis.md
# Step 1: コードベース分析結果

## Issue要求概要
[Issue #$ARGUMENTS の要求内容要約]

## プロジェクト構造分析
### 現在のアーキテクチャ
[レイヤード構造・設計パターンの特定]

### 技術スタック
[使用ライブラリ・フレームワーク]

## Issue要求との関連性分析
### 関連する既存機能
[Issue要求に類似する既存実装]

### 必要な新規実装
[Issue要求で新規に必要となる実装]

## データフロー分析
### 現在のデータフロー
[既存のデータ処理パターン]

### Issue要求によるデータフロー変更
[新規要求による処理フローの変更点]

## 次ステップへの情報
### 重要調査対象ファイル
[Step 2で詳細分析すべきファイル]
```

### Step 2: 関連ファイル特定・影響範囲分析

#### 影響ファイルの特定
```bash
# 進捗状況更新
!cat "docs/issue-$ARGUMENTS/workflow-status.json" | jq '.phases.analysis.steps.step2_file_identification = "in_progress"' > temp.json && mv temp.json "docs/issue-$ARGUMENTS/workflow-status.json"

# 直接影響ファイルの特定
!rg -i "関連クラス|関連関数" --type py -l > "docs/issue-$ARGUMENTS/direct-impact-files.txt"

# 間接影響ファイル（import関係）の特定
!rg -i "import.*関連モジュール|from.*関連モジュール" --type py -l > "docs/issue-$ARGUMENTS/indirect-impact-files.txt"

# テストファイルの特定
!find . -name "*test*" -name "*.py" | xargs rg -l "関連キーワード" > "docs/issue-$ARGUMENTS/test-files.txt"
```

#### 影響度評価・JSON生成
```json
// docs/issue-$ARGUMENTS/02-related-files.json
{
  "issue_number": "$ARGUMENTS",
  "analysis_timestamp": "2024-06-26T14:30:22Z",
  "impact_analysis": {
    "direct_impact": [
      {
        "file_path": "src/service/example_service.py",
        "impact_level": "high",
        "change_type": "modification",
        "reason": "Issue要求の主要機能実装"
      }
    ],
    "indirect_impact": [
      {
        "file_path": "src/models/example_model.py", 
        "impact_level": "medium",
        "change_type": "extension",
        "reason": "新規フィールド追加の可能性"
      }
    ],
    "test_impact": [
      {
        "file_path": "tests/test_example_service.py",
        "impact_level": "high", 
        "change_type": "addition",
        "reason": "新機能のテストケース追加"
      }
    ]
  },
  "summary": {
    "total_files": 15,
    "high_impact": 5,
    "medium_impact": 7,
    "low_impact": 3
  }
}
```

### Step 3: 変更計画策定・実装設計

#### Issue要求に基づく実装計画
```bash
# 進捗状況更新
!cat "docs/issue-$ARGUMENTS/workflow-status.json" | jq '.phases.analysis.steps.step3_implementation_plan = "in_progress"' > temp.json && mv temp.json "docs/issue-$ARGUMENTS/workflow-status.json"
```

#### 実装計画書作成
```markdown
# docs/issue-$ARGUMENTS/03-implementation-plan.md
# Step 3: 実装計画

## Issue要求実現方針
### 要求仕様の解釈
[Issue #$ARGUMENTS の技術的解釈]

### 実装アプローチ
[選択した実装手法・パターン]

## アーキテクチャ影響分析
### 既存アーキテクチャとの適合性
[レイヤード設計への適合性]

### 新規コンポーネント設計
[Issue要求で必要となる新規コンポーネント]

## ファイル別実装計画
### 新規ファイル
- `src/service/new_feature_service.py`: Issue要求のメイン機能
- `src/models/new_feature_model.py`: 新規データモデル

### 既存ファイル修正
- `src/api/main_api.py`: 新エンドポイント追加
- `src/repository/base_repository.py`: 新規データアクセス

## データモデル設計
### 新規データ構造
[Issue要求に必要な新規データ構造]

### 既存データ拡張
[既存モデルの拡張要件]

## API設計
### 新規エンドポイント
[Issue要求で必要となるAPI仕様]
```

### Step 4: エッジケース分析・リスク検証

#### Issue要求特有のリスク分析
```bash
# 進捗状況更新
!cat "docs/issue-$ARGUMENTS/workflow-status.json" | jq '.phases.analysis.steps.step4_risk_analysis = "in_progress"' > temp.json && mv temp.json "docs/issue-$ARGUMENTS/workflow-status.json"
```

#### リスク分析レポート作成
```markdown
# docs/issue-$ARGUMENTS/04-risk-analysis.md
# Step 4: リスク分析

## Issue要求特有のリスク
### 技術的リスク
- [Issue要求の技術的難易度・制約]
- [既存システムとの整合性リスク]

### パフォーマンスリスク
- [新機能による性能影響]
- [スケーラビリティへの影響]

### セキュリティリスク
- [新機能による脆弱性の可能性]
- [データ保護・プライバシーへの影響]

## エッジケース分析
### 入力データの境界値
[Issue要求における異常値・境界値の処理]

### 例外処理
[エラーハンドリングの考慮点]

### 運用上の考慮事項
[デプロイメント・設定変更の影響]

## リスク対策
### 高リスク項目の対策
[重要リスクへの対応策]

### 検証方法
[リスク検証のためのテスト戦略]
```

## 分析フェーズ完了処理

### 統合レポート生成
```markdown
# docs/issue-$ARGUMENTS/05-analysis-summary.md
# Issue #$ARGUMENTS 分析フェーズ統合レポート

## Issue要求サマリー
[Issue内容の技術的要約]

## 主要分析結果
### 技術的実現可能性
[実装可能性の評価]

### アーキテクチャ影響
[既存システムへの影響度]

### 実装複雑度
[実装の難易度評価]

## 重要な発見事項
### 技術的課題
[実装時の主要課題]

### 依存関係
[他システム・コンポーネントとの依存]

## 推奨実装アプローチ
[Step 3で策定したアプローチの要約]

## ユーザー判断必要事項
1. **リスク受け入れ判断**: [主要リスクの受け入れ可否]
2. **実装アプローチ承認**: [技術的アプローチの承認]
3. **スコープ確認**: [実装範囲の最終確認]

## 次フェーズ準備
- 実装ガイド作成に必要な情報整理完了
- Issue要求の技術的解釈確定
```

### 進捗状況最終更新
```bash
# 分析フェーズ完了
!cat "docs/issue-$ARGUMENTS/workflow-status.json" | jq '.phases.analysis.status = "completed" | .phases.analysis.steps.step1_codebase_analysis = "completed" | .phases.analysis.steps.step2_file_identification = "completed" | .phases.analysis.steps.step3_implementation_plan = "completed" | .phases.analysis.steps.step4_risk_analysis = "completed"' > temp.json && mv temp.json "docs/issue-$ARGUMENTS/workflow-status.json"
```

### Issue進捗コメント
```bash
# 分析完了をIssueに報告
!gh issue comment $ARGUMENTS --body "## 🔍 分析フェーズ完了

### 📋 成果物
- [コードベース分析](docs/issue-$ARGUMENTS/01-codebase-analysis.md)
- [関連ファイル・影響範囲](docs/issue-$ARGUMENTS/02-related-files.json)  
- [実装計画](docs/issue-$ARGUMENTS/03-implementation-plan.md)
- [リスク分析](docs/issue-$ARGUMENTS/04-risk-analysis.md)
- [📊 統合レポート](docs/issue-$ARGUMENTS/05-analysis-summary.md)

### ✅ レビュー必要項目
1. **リスク分析結果** - 受け入れ可能なリスクか判断
2. **実装アプローチ** - 技術的方向性の承認  
3. **影響範囲** - 特定されたファイル範囲の確認

### 🚀 次ステップ
承認後、実装ガイド作成フェーズに進行:
\`\`\`bash
/user:v1:create-implementation-guide-with-issue $ARGUMENTS
\`\`\`"

# ラベル更新
!gh issue edit $ARGUMENTS --add-label "analysis-completed,review-needed"
```

---

## 実行完了確認

### チェック項目
- [ ] 全ステップの成果物生成完了
- [ ] `docs/issue-$ARGUMENTS/` に全ファイル保存完了
- [ ] 進捗状況JSON更新完了
- [ ] Issue進捗コメント投稿完了

### 次フェーズ移行
```bash
/user:v1:create-implementation-guide-with-issue $ARGUMENTS
```