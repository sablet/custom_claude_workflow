---
allowed-tools: ["Bash", "Read"]
description: "GitHub Issue から開発再開：中断箇所の特定と適切なステップ再開"
---

# Issue から開発再開: $ARGUMENTS

## 前提条件

### 引数
Issue番号: $ARGUMENTS

## 再開処理

### 1. Issue 状態分析
!echo "Issue #$ARGUMENTS の状態を分析中..."

#### Issue 基本情報取得
!gh issue view $ARGUMENTS --json title,state,body,labels,comments

#### ラベルベースの進捗判定
!echo "=== 現在の開発段階判定 ==="

```bash
LABELS=$(gh issue view $ARGUMENTS --json labels -q '.labels[].name' | tr '\n' ' ')
echo "検出されたラベル: $LABELS"

# 進捗段階の判定
case "$LABELS" in
  *"development-complete"*)
    CURRENT_STAGE="完了"
    NEXT_COMMAND="開発は完了しています"
    ;;
  *"integration-complete"*)
    CURRENT_STAGE="統合テスト完了"
    NEXT_COMMAND="/user:update-issue $ARGUMENTS \"プロジェクト完了確認\""
    ;;
  *"green-phase-complete"*)
    CURRENT_STAGE="Green Phase完了"
    NEXT_COMMAND="/user:create-integration-tests [実装ディレクトリ]"
    ;;
  *"red-phase-verified"*)
    CURRENT_STAGE="Red Phase確認完了" 
    NEXT_COMMAND="/user:implement-logic [実装ディレクトリ]"
    ;;
  *"acceptance-tests-ready"*)
    CURRENT_STAGE="受け入れテスト作成完了"
    NEXT_COMMAND="/user:implement-signatures [受け入れテストパス]"
    ;;
  *"planning-complete"*)
    CURRENT_STAGE="実装計画完了"
    NEXT_COMMAND="/user:create-acceptance-tests [計画書パス]"
    ;;
  *"design-complete"*)
    CURRENT_STAGE="アーキテクチャ設計完了"
    NEXT_COMMAND="/user:plan-implementation [設計書パス]"
    ;;
  *"architecture-reviewed"*)
    CURRENT_STAGE="アーキテクチャ確認完了"
    # 設計要否をコメントから判定
    NEEDS_DESIGN=$(gh issue view $ARGUMENTS --json comments -q '.comments[].body' | grep -i "変更必要\|design\|設計" | wc -l)
    if [ "$NEEDS_DESIGN" -gt 0 ]; then
      NEXT_COMMAND="/user:design-architecture [仕様書パス]"
    else
      NEXT_COMMAND="/user:plan-implementation [仕様書パス]"
    fi
    ;;
  *"analysis-complete"*)
    CURRENT_STAGE="要求分析完了"
    NEXT_COMMAND="/user:check-architecture [仕様書パス]"
    ;;
  *)
    CURRENT_STAGE="開始前または不明"
    NEXT_COMMAND="/user:clarify-requirements [要求内容]"
    ;;
esac

echo "📍 現在の段階: $CURRENT_STAGE"
echo "➡️ 次のコマンド: $NEXT_COMMAND"
```

### 2. 成果物パス特定
```bash
echo "=== 成果物ファイルの特定 ==="

# Issue コメントから成果物パスを抽出
COMMENTS=$(gh issue view $ARGUMENTS --json comments -q '.comments[].body')

# 仕様書パス
SPEC_PATH=$(echo "$COMMENTS" | grep -oE '仕様書: [^\s]+' | head -1 | cut -d' ' -f2)
if [ -n "$SPEC_PATH" ]; then
  echo "📄 仕様書: $SPEC_PATH"
fi

# 設計書パス
DESIGN_PATH=$(echo "$COMMENTS" | grep -oE '設計書: [^\s]+' | head -1 | cut -d' ' -f2)
if [ -n "$DESIGN_PATH" ]; then
  echo "🏗️ 設計書: $DESIGN_PATH"
fi

# 実装計画書パス
PLAN_PATH=$(echo "$COMMENTS" | grep -oE '計画書: [^\s]+' | head -1 | cut -d' ' -f2)
if [ -n "$PLAN_PATH" ]; then
  echo "📝 実装計画書: $PLAN_PATH"
fi

# 実装ディレクトリパス
IMPL_PATH=$(echo "$COMMENTS" | grep -oE '実装ディレクトリ: [^\s]+' | head -1 | cut -d' ' -f2)
if [ -n "$IMPL_PATH" ]; then
  echo "💻 実装ディレクトリ: $IMPL_PATH"
fi
```

### 3. 環境状態確認
```bash
echo "=== 開発環境状態確認 ==="

# プロジェクトディレクトリの確認
if [ -n "$IMPL_PATH" ] && [ -d "$IMPL_PATH" ]; then
  echo "✅ 実装ディレクトリ存在: $IMPL_PATH"
  
  # Python環境確認
  if [ -f "$IMPL_PATH/pyproject.toml" ]; then
    echo "✅ Python プロジェクト構成確認"
    cd "$IMPL_PATH"
    
    # 依存関係状態
    if command -v uv &> /dev/null; then
      echo "📦 uv 環境:"
      uv --version
    else
      echo "⚠️ uv がインストールされていません"
    fi
    
    # プロジェクト構造
    echo "📂 プロジェクト構造:"
    find . -name "*.py" -type f | head -10
    
    # テスト状態
    if [ -d "tests" ]; then
      echo "🧪 テストディレクトリ存在"
      find tests -name "*.py" | wc -l | xargs echo "テストファイル数:"
    fi
  fi
else
  echo "📁 実装ディレクトリ未作成またはパス不明"
fi
```

### 4. 具体的な再開コマンド生成
```bash
echo "=== 再開コマンド生成 ==="

# パス情報を含む具体的なコマンド
case "$CURRENT_STAGE" in
  "要求分析完了")
    if [ -n "$SPEC_PATH" ]; then
      CONCRETE_COMMAND="/user:check-architecture $SPEC_PATH"
    else
      CONCRETE_COMMAND="/user:check-architecture [仕様書パスを指定]"
    fi
    ;;
  
  "アーキテクチャ確認完了")
    if [ -n "$SPEC_PATH" ]; then
      if [ "$NEEDS_DESIGN" -gt 0 ]; then
        CONCRETE_COMMAND="/user:design-architecture $SPEC_PATH"
      else
        CONCRETE_COMMAND="/user:plan-implementation $SPEC_PATH"
      fi
    else
      CONCRETE_COMMAND="$NEXT_COMMAND"
    fi
    ;;
  
  "アーキテクチャ設計完了")
    if [ -n "$DESIGN_PATH" ]; then
      CONCRETE_COMMAND="/user:plan-implementation $DESIGN_PATH"
    else
      CONCRETE_COMMAND="/user:plan-implementation [設計書パスを指定]"
    fi
    ;;
  
  "実装計画完了")
    if [ -n "$PLAN_PATH" ]; then
      CONCRETE_COMMAND="/user:create-acceptance-tests $PLAN_PATH"
    else
      CONCRETE_COMMAND="/user:create-acceptance-tests [計画書パスを指定]"
    fi
    ;;
  
  "受け入れテスト作成完了")
    if [ -n "$IMPL_PATH" ]; then
      CONCRETE_COMMAND="/user:implement-signatures $IMPL_PATH"
    else
      CONCRETE_COMMAND="/user:implement-signatures [実装ディレクトリを指定]"
    fi
    ;;
  
  "Red Phase確認完了")
    if [ -n "$IMPL_PATH" ]; then
      CONCRETE_COMMAND="/user:implement-logic $IMPL_PATH"
    else
      CONCRETE_COMMAND="/user:implement-logic [実装ディレクトリを指定]"
    fi
    ;;
  
  "Green Phase完了")
    if [ -n "$IMPL_PATH" ]; then
      CONCRETE_COMMAND="/user:create-integration-tests $IMPL_PATH"
    else
      CONCRETE_COMMAND="/user:create-integration-tests [実装ディレクトリを指定]"
    fi
    ;;
  
  *)
    CONCRETE_COMMAND="$NEXT_COMMAND"
    ;;
esac

echo "🚀 実行推奨コマンド:"
echo "$CONCRETE_COMMAND"
```

### 5. 再開前チェックリスト表示
```bash
echo "=== 再開前チェックリスト ==="

cat << 'EOF'
## ✅ 開発再開前の確認事項

### 環境確認
- [ ] GitHub CLI (gh) が利用可能
- [ ] リポジトリへのアクセス権限確認
- [ ] Python 環境 (uv) がセットアップ済み
- [ ] 既存の成果物ファイルが利用可能

### コンテキスト確認
- [ ] Issue の要求内容を再確認
- [ ] 前回の作業内容をコメントで確認
- [ ] 既存の実装・テストファイルを確認
- [ ] チーム・プロジェクトの最新状況を確認

### 作業準備
- [ ] 作業ブランチを適切に設定
- [ ] 前回の変更がコミット・プッシュ済み
- [ ] 必要な成果物ファイルが手元にある
- [ ] 集中できる作業環境を準備

## 🔄 推奨再開手順

1. **現在状況の最終確認**
   ```bash
   gh issue view $ARGUMENTS
   ```

2. **推奨コマンド実行**
   ```bash
   $CONCRETE_COMMAND
   ```

3. **進捗をIssueに更新**
   ```bash
   /user:update-issue $ARGUMENTS "再開" "開発作業を再開しました"
   ```

EOF
```

### 6. チーム通知（オプション）
```bash
echo "=== チーム通知 ==="

# Issue に再開コメント追加
gh issue comment $ARGUMENTS --body "## 🔄 開発作業再開

**再開時刻**: $(date '+%Y-%m-%d %H:%M:%S')
**現在段階**: $CURRENT_STAGE
**次のステップ**: $CONCRETE_COMMAND

### 📋 作業再開チェックリスト
- [x] Issue状態確認完了
- [x] 成果物パス特定完了
- [x] 開発環境確認完了
- [ ] 次段階作業開始予定

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

echo "✅ Issue に再開通知を追加しました"
```

## エラーハンドリング

### Issue 存在確認
```bash
# Issue存在確認は再開処理内で実行
```

### ラベル不整合の場合
```bash
if [ "$CURRENT_STAGE" = "開始前または不明" ]; then
  echo "⚠️ 警告: 開発段階が特定できません"
  echo ""
  echo "手動でのラベル確認・追加が必要な可能性があります:"
  echo "- analysis-complete: 要求分析完了"
  echo "- architecture-reviewed: アーキテクチャ確認完了"
  echo "- design-complete: 設計完了"
  echo "- planning-complete: 実装計画完了"
  echo ""
  echo "現在のラベル: $LABELS"
fi
```

### 成果物不在の場合
```bash
if [ -z "$SPEC_PATH" ] && [[ "$CURRENT_STAGE" != "開始前または不明" ]]; then
  echo "⚠️ 警告: 成果物パスが特定できません"
  echo ""
  echo "Issueコメントに以下の形式で成果物パスを記載してください:"
  echo "- 仕様書: /path/to/specification.md"
  echo "- 設計書: /path/to/design.md"
  echo "- 計画書: /path/to/plan.md"
  echo "- 実装ディレクトリ: /path/to/implementation/"
fi
```

---

## 使用例

### 基本的な再開
```bash
# Issue #42 から開発再開
/user:resume-from-issue 42
```

### 複数Issue の一括確認
```bash
# 複数のIssueの状態確認
for issue in 40 41 42; do
  echo "=== Issue #$issue ==="
  /user:resume-from-issue $issue
  echo ""
done
```

### チーム での進捗共有
```bash
# アクティブなIssueの進捗確認
gh issue list --assignee @me --state open | while read line; do
  issue_num=$(echo $line | cut -d'#' -f2 | cut -d' ' -f1)
  /user:resume-from-issue $issue_num
done
```

---

完全な開発プロセス管理システムが完成しました。GitHub Issueとの完全連携により、いつでも開発を中断・再開できる体制が整いました。