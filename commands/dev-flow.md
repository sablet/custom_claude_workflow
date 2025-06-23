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

### 4. 実装計画
`/user:plan-implementation [設計書パス]`でテスト方針含む実装計画書を作成

### 5. TDD実装サイクル
- `/user:create-acceptance-tests [計画書パス]` - 受け入れテスト作成
- `/user:implement-signatures [計画書パス]` - シグネチャのみ実装
- `/user:verify-red-phase [テスト対象]` - テスト失敗確認
- `/user:implement-logic [テスト対象]` - ロジック実装
- `/user:create-integration-tests [機能名]` - 統合テスト実行

### 6. 進捗管理
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
- [ ] 実装計画 (plan-implementation)
- [ ] 受け入れテスト作成 (create-acceptance-tests)
- [ ] シグネチャ実装 (implement-signatures)
- [ ] Red Phase 確認 (verify-red-phase)
- [ ] ロジック実装 (implement-logic)
- [ ] 統合テスト (create-integration-tests)

## 成果物
- [ ] 仕様書.md
- [ ] 設計書.md (必要時)
- [ ] 実装計画書.md
- [ ] テストコード
- [ ] 実装コード

🤖 Generated with [Claude Code](https://claude.ai/code)
EOF
)"

## 次のステップ

GitHub issue作成後、以下のコマンドで開発を開始してください：

```
/user:clarify-requirements $ARGUMENTS
```

作成されたissue番号をメモして、各ステップ完了時に更新してください。