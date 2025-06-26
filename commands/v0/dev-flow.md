---
allowed-tools: ["Read", "Write", "Bash"]
description: "全体開発プロセス管理と GitHub issue 連携"
---

# 開発フロー管理: $ARGUMENTS

## プロセス概要

### 1. 要求分析
`/user:clarify-requirements $ARGUMENTS`を実行して要求を明確化

### 2. アーキテクチャ確認
生成された仕様書を基に`/user:check-architecture [仕様書パス]`でアーキテクチャ変更要否を判定

### 3. 設計（必要時のみ）
アーキテクチャ変更が必要な場合のみ`/user:design-architecture [仕様書パス]`を実行

### 4. 受け入れテスト基準定義
`/user:define-acceptance-criteria [仕様書パス]`でGiven-When-Then方式の受け入れテスト基準を作成

**📝 分析・設計フェーズ完了後は `/compact` を実行して会話履歴を圧縮してください**

### 5. 実装計画
`/user:plan-implementation [受け入れテスト基準パス]`でテスト方針含む実装計画書を作成

**📝 計画フェーズ完了後は `/compact` を実行して会話履歴を圧縮してください**

### 6. TDD実装サイクル
- `/user:create-acceptance-tests [計画書パス]` - 受け入れテスト作成
- `/user:implement-signatures [計画書パス]` - シグネチャのみ実装
- `/user:verify-red-phase [テスト対象]` - テスト失敗確認
- `/user:implement-logic [テスト対象]` - ロジック実装 **→ 完了後 `/compact` 推奨**
- `/user:create-integration-tests [機能名]` - 統合テスト実行 **→ 完了後 `/compact` 推奨**

**📝 実装フェーズ完了後は `/compact` を実行して会話履歴を圧縮してください**

### 7. 分析レポート作成
- `/user:create-analysis-report [要求分析結果パス]` - サンプルデータ検証とHTMLレポート生成

### 8. 進捗管理
- `/user:update-issue [issue番号] [ステータス]` - GitHub issue更新
- `/user:resume-from-issue [issue番号]` - 中断箇所から再開

## GitHub Issue 作成

!gh issue create --title "Feature: $ARGUMENTS" --body "$(cat <<'EOF'
## 要求内容
$ARGUMENTS

## 開発ステップ
- [ ] 要求分析 (clarify-requirements)
- [ ] アーキテクチャ確認 (check-architecture)
- [ ] 設計 (design-architecture) ※必要時のみ
- [ ] 受け入れテスト基準定義 (define-acceptance-criteria)
- [ ] 📝 `/compact` 実行（分析・設計フェーズ完了）
- [ ] 実装計画 (plan-implementation)
- [ ] 📝 `/compact` 実行（計画フェーズ完了）
- [ ] 受け入れテスト作成 (create-acceptance-tests)
- [ ] シグネチャ実装 (implement-signatures)
- [ ] Red Phase 確認 (verify-red-phase)
- [ ] ロジック実装 (implement-logic) → `/compact` 推奨
- [ ] 統合テスト (create-integration-tests) → `/compact` 推奨
- [ ] 📝 `/compact` 実行（実装フェーズ完了）
- [ ] 分析レポート作成 (create-analysis-report)

## 成果物
- [ ] 仕様書.md
- [ ] 設計書.md (必要時)
- [ ] 受け入れテスト基準.md
- [ ] 実装計画書.md
- [ ] テストコード
- [ ] 実装コード
- [ ] 分析レポート.html

🤖 Generated with [Claude Code](https://claude.ai/code)
EOF
)"

## 次のステップ

GitHub issue作成後、以下のコマンドで開発を開始してください：

```
/user:clarify-requirements $ARGUMENTS
```

作成されたissue番号をメモして、各ステップ完了時に更新してください。

## 📝 /compact について

**使用タイミング:**
- 分析・設計フェーズ完了後（論理的区切り）
- 計画フェーズ完了後（論理的区切り）
- 重いコマンド完了後（`implement-logic`, `create-integration-tests`）
- 実装フェーズ完了後（論理的区切り）

**効果:**
- 会話履歴を圧縮してトークン使用量を削減
- 全体の開発フローとコンテキストは保持
- 長時間開発セッションでのパフォーマンス向上