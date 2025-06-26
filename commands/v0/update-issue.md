---
allowed-tools: ["Bash", "Read"]
description: "GitHub Issue更新：開発進捗の追跡と状態更新"
---

# GitHub Issue 更新: $ARGUMENTS

## 前提条件

### 引数形式
`issue番号 ステータス [詳細メッセージ]`

例: `42 "実装完了" "Green Phase実装が完了しました"`

## Issue 更新処理

### 1. 引数解析
!echo "更新対象: $ARGUMENTS"

### 2. Issue 現在状態確認
!gh issue view $1 --json title,state,body,labels

### 3. 開発段階別ステータス更新

#### 要求分析段階
```bash
case "$2" in
  "要求分析完了")
    gh issue edit $1 \
      --add-label "analysis-complete" \
      --body "$(gh issue view $1 --json body -q .body)

## 📋 要求分析完了

✅ **要求明確化**: 完了
- 仕様書作成: ✅
- What/Why分析: ✅
- 成果物定義: ✅

**次ステップ**: アーキテクチャ確認
\`\`\`bash
/user:check-architecture [仕様書パス]
\`\`\`

🤖 Generated with [Claude Code](https://claude.ai/code)"
    
    echo "✅ 要求分析完了を記録"
    ;;
```

#### アーキテクチャ段階
```bash
  "アーキテクチャ確認完了")
    gh issue edit $1 \
      --add-label "architecture-reviewed" \
      --body "$(gh issue view $1 --json body -q .body)

## 🏗️ アーキテクチャ確認完了

✅ **アーキテクチャ変更要否**: 判定完了
- 既存構造分析: ✅
- 影響範囲評価: ✅
- 設計方針決定: ✅

**判定結果**: $3

**次ステップ**: $(if [[ "$3" == *"変更必要"* ]]; then echo "アーキテクチャ設計"; else echo "実装計画"; fi)
\`\`\`bash
$(if [[ "$3" == *"変更必要"* ]]; then echo "/user:design-architecture"; else echo "/user:plan-implementation"; fi) [前段階成果物パス]
\`\`\`"
    
    echo "✅ アーキテクチャ確認完了を記録"
    ;;

  "設計完了")
    gh issue edit $1 \
      --add-label "design-complete" \
      --body "$(gh issue view $1 --json body -q .body)

## 🎨 アーキテクチャ設計完了

✅ **新規アーキテクチャ設計**: 完了
- レイヤー構造定義: ✅
- 依存関係設計: ✅
- 技術詳細設計: ✅
- 品質保証計画: ✅

**次ステップ**: 実装計画作成
\`\`\`bash
/user:plan-implementation [設計書パス]
\`\`\`"
    
    echo "✅ アーキテクチャ設計完了を記録"
    ;;
```

#### 実装計画段階
```bash
  "実装計画完了")
    gh issue edit $1 \
      --add-label "planning-complete" \
      --body "$(gh issue view $1 --json body -q .body)

## 📝 実装計画完了

✅ **TDD実装計画**: 作成完了
- フェーズ分割: ✅
- テスト戦略: ✅
- 品質保証計画: ✅
- スケジュール定義: ✅

**次ステップ**: 受け入れテスト作成
\`\`\`bash
/user:create-acceptance-tests [計画書パス]
\`\`\`"
    
    echo "✅ 実装計画完了を記録"
    ;;
```

#### TDD実装段階
```bash
  "受け入れテスト作成完了")
    gh issue edit $1 \
      --add-label "acceptance-tests-ready" \
      --body "$(gh issue view $1 --json body -q .body)

## 🧪 受け入れテスト作成完了

✅ **受け入れテスト**: 作成完了
- メインユースケース: ✅
- 異常系シナリオ: ✅
- パフォーマンステスト: ✅
- セキュリティテスト: ✅

**次ステップ**: シグネチャ実装
\`\`\`bash
/user:implement-signatures [受け入れテストパス]
\`\`\`"
    
    echo "✅ 受け入れテスト作成完了を記録"
    ;;

  "Red Phase確認完了")
    gh issue edit $1 \
      --add-label "red-phase-verified" \
      --body "$(gh issue view $1 --json body -q .body)

## 🔴 Red Phase 確認完了

✅ **TDD Red Phase**: 確認完了
- シグネチャ実装: ✅
- テスト失敗確認: ✅
- 型チェック合格: ✅
- 実装ガイド明確化: ✅

**次ステップ**: ロジック実装 (Green Phase)
\`\`\`bash
/user:implement-logic [実装ディレクトリ]
\`\`\`"
    
    echo "✅ Red Phase確認完了を記録"
    ;;

  "Green Phase実装完了")
    gh issue edit $1 \
      --add-label "green-phase-complete" \
      --body "$(gh issue view $1 --json body -q .body)

## 🟢 Green Phase 実装完了

✅ **TDD Green Phase**: 実装完了
- ビジネスロジック実装: ✅
- 受け入れテスト通過: ✅
- コード品質確認: ✅
- エラーハンドリング: ✅

**次ステップ**: 統合テスト作成
\`\`\`bash
/user:create-integration-tests [実装ディレクトリ]
\`\`\`"
    
    echo "✅ Green Phase実装完了を記録"
    ;;

  "統合テスト完了")
    gh issue edit $1 \
      --add-label "integration-complete" \
      --body "$(gh issue view $1 --json body -q .body)

## 🔗 統合テスト完了

✅ **統合テスト**: 完了
- レイヤー間連携: ✅
- エンドツーエンド: ✅
- パフォーマンス: ✅
- 環境・設定テスト: ✅

**🎉 開発完了**: すべてのフェーズが完了しました

## 📊 最終確認チェックリスト
- [ ] 全テスト通過確認
- [ ] コード品質チェック
- [ ] ドキュメント更新
- [ ] プルリクエスト作成"
    
    echo "✅ 統合テスト完了を記録"
    ;;
```

#### 一般的なステータス更新
```bash
  *)
    # カスタムステータス更新
    gh issue comment $1 --body "## 📈 進捗更新

**ステータス**: $2
**詳細**: ${3:-進捗を更新しました}

**更新時刻**: $(date '+%Y-%m-%d %H:%M:%S')

🤖 Generated with [Claude Code](https://claude.ai/code)"
    
    echo "✅ ステータス更新: $2"
    ;;
esac
```

### 4. プロジェクト完了判定
```bash
# 完了ラベルチェック
LABELS=$(gh issue view $1 --json labels -q '.labels[].name' | tr '\n' ' ')

if echo "$LABELS" | grep -q "integration-complete"; then
  echo "🎉 プロジェクト開発完了！"
  
  # 完了サマリー作成
  gh issue comment $1 --body "## 🎯 開発完了サマリー

### ✅ 完了フェーズ
$(echo "$LABELS" | tr ' ' '\n' | grep -E "(analysis|architecture|planning|acceptance|red-phase|green-phase|integration)-" | sed 's/^/- ✅ /' | sed 's/-/ /')

### 📈 成果物
- 要求仕様書
- アーキテクチャ設計書
- 実装計画書
- 受け入れテスト
- 実装コード
- 統合テスト

### 🔧 品質保証
- TDD サイクル完了
- 型安全性確保 (pyright)
- コード品質確保 (ruff)
- テストカバレッジ確認

**開発期間**: $(gh issue view $1 --json createdAt -q .createdAt | cut -d'T' -f1) ～ $(date '+%Y-%m-%d')

🤖 Generated with [Claude Code](https://claude.ai/code)"
  
  # 完了ラベル追加
  gh issue edit $1 --add-label "development-complete"
fi
```

### 5. チーム通知（オプション）
```bash
# プロジェクト完了時の通知
if echo "$LABELS" | grep -q "development-complete"; then
  echo "🔔 チーム通知: 開発完了"
  
  # Slack通知やメール送信等（環境に応じて）
  # curl -X POST "$SLACK_WEBHOOK" -d "{'text': 'Issue #$1 開発完了 🎉'}"
fi
```

## エラーハンドリング

### GitHub CLI エラー
```bash
if ! command -v gh &> /dev/null; then
  echo "❌ エラー: GitHub CLI (gh) がインストールされていません"
  echo "インストール: https://cli.github.com/"
  exit 1
fi

# 認証はコマンド開始時にチェック済み
```

### Issue 存在確認
```bash
if ! gh issue view $1 &> /dev/null; then
  echo "❌ エラー: Issue #$1 が見つかりません"
  echo "利用可能なIssue一覧:"
  gh issue list --limit 10
  exit 1
fi
```

### 権限確認
```bash
REPO_PERMISSIONS=$(gh api repos/:owner/:repo --jq .permissions.push)
if [[ "$REPO_PERMISSIONS" != "true" ]]; then
  echo "⚠️  警告: リポジトリへの書き込み権限がない可能性があります"
fi
```

## 使用例

### 基本的な使用方法
```bash
# 要求分析完了
/user:update-issue 42 "要求分析完了"

# アーキテクチャ確認完了（変更不要）
/user:update-issue 42 "アーキテクチャ確認完了" "変更不要"

# カスタム進捗更新
/user:update-issue 42 "実装50%完了" "モデル層とリポジトリ層の実装が完了"
```

### チーム開発での活用
```bash
# 担当者変更
gh issue edit 42 --add-assignee @username

# マイルストーン設定
gh issue edit 42 --milestone "Sprint 1"

# 優先度変更
gh issue edit 42 --add-label "priority-high"
```

---

## 次ステップ

### Issue から再開
```bash
/user:resume-from-issue [issue番号]
```

### 開発完了時
プロジェクト完了ラベルが付与されたら、最終レビュー・プルリクエスト作成を実施