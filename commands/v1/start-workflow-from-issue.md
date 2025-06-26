---
allowed-tools: ["Read", "Write", "Grep", "Glob", "Task", "Bash"]
description: "GitHub Issue起点でワークフローを開始し、進捗を追跡"
---

# Issue連動ワークフロー開始: $ARGUMENTS

## 概要
GitHub Issueを起点としてワークフローを開始し、全ての成果物・進捗をIssueに連動させる。
ドキュメント成果物は `docs/issue-[番号]/` に保存し、完全なトレーサビリティを確保。

## 実行前提条件
- GitHub Issue番号: $ARGUMENTS (例: 123)
- Issue内容: 変更要求・仕様書への参照を含む

## 初期化・セットアップ

### 1. Issue情報取得
```bash
# Issue詳細の取得
!gh issue view $ARGUMENTS --json title,body,labels,assignees,milestone

# Issue情報をワークスペースに保存
!mkdir -p "docs/issue-$ARGUMENTS"
!gh issue view $ARGUMENTS > "docs/issue-$ARGUMENTS/original-issue.md"
```

### 2. ワークフロー管理ディレクトリ作成
```bash
# ドキュメント保存用ディレクトリ
!mkdir -p "docs/issue-$ARGUMENTS"

# コード中間生成物用ディレクトリ
!mkdir -p "output/issue-$ARGUMENTS-$(date +%Y%m%d-%H%M%S)"

# 現在のワークフロー情報を保存
!echo "issue-$ARGUMENTS" > output/current-issue.txt
!echo "docs/issue-$ARGUMENTS" > output/current-docs-dir.txt
!echo "output/issue-$ARGUMENTS-$(date +%Y%m%d-%H%M%S)" > output/current-output-dir.txt
```

### 3. Issue進捗トラッキング初期化
```bash
# 進捗管理JSONの作成
cat > "docs/issue-$ARGUMENTS/workflow-status.json" << 'EOF'
{
  "issue_number": "$ARGUMENTS",
  "workflow_status": "started",
  "start_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "phases": {
    "analysis": {
      "status": "pending",
      "steps": {
        "step1_codebase_analysis": "pending",
        "step2_file_identification": "pending", 
        "step3_implementation_plan": "pending",
        "step4_risk_analysis": "pending"
      }
    },
    "implementation_guide": {
      "status": "pending",
      "steps": {
        "step6_syntax_validation": "pending",
        "step7_final_guide": "pending"
      }
    }
  },
  "artifacts": {
    "docs_dir": "docs/issue-$ARGUMENTS",
    "output_dir": "output/issue-$ARGUMENTS-$(date +%Y%m%d-%H%M%S)"
  }
}
EOF
```

## フェーズ1: 分析実行

### 分析フェーズ開始
```bash
# Issue内容を分析対象として分析フェーズ実行
/user:v1:analyze-change-request-with-issue $ARGUMENTS
```

### Issue進捗更新（分析フェーズ完了時）
```bash
# 分析完了をIssueにコメント
!gh issue comment $ARGUMENTS --body "## 🔍 分析フェーズ完了

### 成果物
- [コードベース分析](docs/issue-$ARGUMENTS/01-codebase-analysis.md)
- [関連ファイル特定](docs/issue-$ARGUMENTS/02-related-files.json)
- [実装計画](docs/issue-$ARGUMENTS/03-implementation-plan.md)
- [リスク分析](docs/issue-$ARGUMENTS/04-risk-analysis.md)
- [統合レポート](docs/issue-$ARGUMENTS/05-analysis-summary.md)

### ✅ レビュー必要項目
1. **リスク分析結果の受け入れ判断** - [Step 4レポート](docs/issue-$ARGUMENTS/04-risk-analysis.md)
2. **実装アプローチの承認** - [実装計画](docs/issue-$ARGUMENTS/03-implementation-plan.md)
3. **影響範囲の妥当性確認** - [関連ファイル](docs/issue-$ARGUMENTS/02-related-files.json)

### 次ステップ
承認後、以下コマンドで実装ガイド作成フェーズに進行:
\`\`\`bash
/user:v1:create-implementation-guide-with-issue $ARGUMENTS
\`\`\`"

# ラベル更新
!gh issue edit $ARGUMENTS --add-label "analysis-completed,review-needed"
```

## フェーズ2: 実装ガイド作成

### 実装ガイド作成フェーズ開始
```bash
# 分析結果を使って実装ガイド作成
/user:v1:create-implementation-guide-with-issue $ARGUMENTS
```

### Issue進捗更新（実装ガイド完了時）
```bash
# 実装ガイド完了をIssueにコメント
!gh issue comment $ARGUMENTS --body "## 📋 実装ガイド作成完了

### 成果物
- [技術検証レポート](docs/issue-$ARGUMENTS/06-syntax-validation.md)
- [完全実装ガイド](docs/issue-$ARGUMENTS/07-final-implementation-guide.md)
- [実装チェックリスト](docs/issue-$ARGUMENTS/08-implementation-checklist.md)

### 🚀 実装準備完了
完全な実装指示書（10-15K tokens）が作成されました。

### 次ステップ: 実装開始
以下コマンドで実装を開始:
\`\`\`bash
/user:v1:implement-from-guide $ARGUMENTS
\`\`\`"

# ラベル更新
!gh issue edit $ARGUMENTS --add-label "implementation-ready" --remove-label "review-needed"
```

## 実装・PR作成フェーズ

### 実装実行とPR作成
```bash
# 実装ガイドに基づく実装とPR作成
/user:v1:implement-and-create-pr $ARGUMENTS
```

### 完了時のIssue更新
```bash
# PR作成完了をIssueにコメント
!gh issue comment $ARGUMENTS --body "## ✅ 実装完了・PR作成

### 📋 実装完了
- 実装ガイドに基づく全ての変更を完了
- テストケースの実装・実行完了
- 品質チェック（lint, type check）完了

### 🔄 Pull Request作成
- PR: #[PR番号] 
- レビュー準備完了

### 📁 成果物一覧
- **ワークフロー文書**: [docs/issue-$ARGUMENTS/](docs/issue-$ARGUMENTS/)
- **実装成果物**: [output/issue-$ARGUMENTS-*/](output/issue-$ARGUMENTS-*)

### 🔗 トレーサビリティ
Issue → 分析 → 実装ガイド → 実装 → PR の完全な履歴を確保"

# 最終ラベル更新
!gh issue edit $ARGUMENTS --add-label "implementation-completed,pr-created" --remove-label "implementation-ready"
```

## ディレクトリ構造

### ドキュメント成果物 (`docs/issue-[番号]/`)
```
docs/issue-123/
├── 00-original-issue.md           # 元のIssue内容
├── 01-codebase-analysis.md        # Step1: コードベース分析
├── 02-related-files.json          # Step2: 関連ファイル特定
├── 03-implementation-plan.md      # Step3: 実装計画
├── 04-risk-analysis.md            # Step4: リスク分析
├── 05-analysis-summary.md         # 分析フェーズ統合レポート
├── 06-syntax-validation.md        # Step6: 技術検証
├── 07-final-implementation-guide.md # Step7: 完全実装ガイド
├── 08-implementation-checklist.md # 実装チェックリスト
├── 09-implementation-result.md    # 実装結果レポート
├── 10-workflow-summary.md         # ワークフロー完了サマリー
└── workflow-status.json           # 進捗管理
```

### コード中間生成物 (`output/issue-[番号]-[timestamp]/`)
```
output/issue-123-20240626-143022/
├── temp-analysis/                 # 一時的な分析データ
├── code-snippets/                 # コード断片
├── test-data/                     # テスト用データ
└── build-artifacts/               # ビルド成果物
```

## 進捗追跡・再開

### 現在のワークフロー状況確認
```bash
# 進捗状況の確認
!cat "docs/issue-$ARGUMENTS/workflow-status.json" | jq .

# Issue状況の確認
!gh issue view $ARGUMENTS --json state,labels,comments
```

### ワークフロー再開
```bash
# 特定フェーズからの再開
/user:v1:resume-workflow-from-issue $ARGUMENTS [phase_name]
```

---

## 実行コマンド

**Issue起点ワークフロー開始:**
```bash
/user:v1:start-workflow-from-issue [Issue番号]
```

**進捗確認:**
```bash
/user:v1:check-workflow-status [Issue番号]
```