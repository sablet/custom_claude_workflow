---
allowed-tools: ["Read", "Write", "Grep", "Glob", "Task", "Bash", "Edit", "MultiEdit"]
description: "実装ガイドに基づく実装実行とPR作成"
---

# 実装ガイド実行・PR作成: $ARGUMENTS

## 概要
完全実装ガイドに基づいて実際のコード実装を実行し、
品質チェック・テスト実行を経てPull Requestを作成。

## 実行前提条件
- GitHub Issue番号: $ARGUMENTS
- 実装ガイド: `docs/issue-$ARGUMENTS/07-final-implementation-guide.md`
- 前フェーズ: `/user:v1:create-implementation-guide-with-issue $ARGUMENTS` 実行済み

## 実装実行フェーズ

### 1. 実装準備

#### 実装ガイドの読み込み
```bash
# 実装ガイドの確認
!cat "docs/issue-$ARGUMENTS/implementation/step7-final-implementation-guide.md"

# 実装チェックリストの確認
!cat "docs/issue-$ARGUMENTS/08-implementation-checklist.md"
```

#### ブランチ作成・環境準備
```bash
# 現在のgit状況確認
!git status

# Issue対応ブランチの作成
!git checkout -b "feature/issue-$ARGUMENTS-$(date +%m%d)"

# 依存関係の確認・追加（必要に応じて）
!ls pyproject.toml uv.lock 2>/dev/null || echo "No uv files found"
```

### 2. ファイル実装（実装ガイドに基づく）

#### 新規ファイルの作成
実装ガイドの「3. ファイル別詳細実装」セクションに基づいて、
各ファイルを段階的に実装：

##### データモデル実装
```bash
# 実装ガイドからモデルファイルの内容を抽出・実装
# (step7-final-implementation-guide.mdの該当セクションから)
```

##### サービス層実装
```bash
# 実装ガイドからサービスファイルの内容を抽出・実装
# (step7-final-implementation-guide.mdの該当セクションから)
```

##### API層実装
```bash
# 実装ガイドから既存ファイル修正の内容を抽出・実装
# (step7-final-implementation-guide.mdの該当セクションから)
```

### 3. テスト実装

#### ユニットテスト作成
```bash
# テストディレクトリの作成
!mkdir -p tests/unit tests/integration tests/performance

# 実装ガイドからテストコードを抽出・実装
# (step7-final-implementation-guide.mdの「4. テスト実装」セクションから)
```

#### 統合テスト作成
```bash
# 実装ガイドに基づく統合テストの実装
```

### 4. 品質保証実行

#### 自動化チェック実行
```bash
# 型チェック（uv環境対応）
!ls uv.lock && uv run --frozen pyright src/ || pyright src/

# リントチェック
!ls uv.lock && uv run --frozen ruff check . || ruff check .

# コードフォーマット
!ls uv.lock && uv run --frozen ruff format . || ruff format .
```

#### テスト実行
```bash
# ユニットテスト実行
!ls uv.lock && uv run --frozen pytest tests/unit/ -v || pytest tests/unit/ -v

# 統合テスト実行
!ls uv.lock && uv run --frozen pytest tests/integration/ -v || pytest tests/integration/ -v

# 全テスト実行
!ls uv.lock && uv run --frozen pytest tests/ -v || pytest tests/ -v

# テストカバレッジ確認
!ls uv.lock && uv run --frozen pytest --cov=src --cov-report=term-missing || pytest --cov=src --cov-report=term-missing
```

### 5. 実装状況確認・記録

#### 実装完了確認
```bash
# 実装されたファイルの確認
!git status

# 変更内容の確認
!git diff --name-only

# 実装チェックリストの確認
!cat "docs/issue-$ARGUMENTS/08-implementation-checklist.md"
```

#### 実装結果レポート作成
```markdown
# docs/issue-$ARGUMENTS/implementation/implementation-result.md
# Issue #$ARGUMENTS 実装結果レポート

## 実装概要
### Issue要求
[Issue #$ARGUMENTS の要求概要]

### 実装完了日時
$(date -u +%Y-%m-%dT%H:%M:%SZ)

## 実装内容
### 新規作成ファイル
- `src/models/issue_${ARGUMENTS}_model.py`: データモデル実装
- `src/service/issue_${ARGUMENTS}_service.py`: ビジネスロジック実装
- `tests/unit/test_issue_${ARGUMENTS}_service.py`: ユニットテスト
- `tests/integration/test_issue_${ARGUMENTS}_api.py`: 統合テスト

### 既存ファイル修正
- `src/api/main_api.py`: 新規エンドポイント追加

## 品質保証結果
### 自動化チェック結果
- [ ] 型チェック: 合格/不合格
- [ ] リントチェック: 合格/不合格
- [ ] コードフォーマット: 適用完了

### テスト実行結果
- [ ] ユニットテスト: X件中X件成功
- [ ] 統合テスト: X件中X件成功
- [ ] テストカバレッジ: X%

## Issue要求充足確認
### 実装完了項目
- [ ] [Issue要求項目1]: 実装完了
- [ ] [Issue要求項目2]: 実装完了

### 受け入れ基準充足
- [ ] [受け入れ基準1]: 充足
- [ ] [受け入れ基準2]: 充足

## 今後の作業
### PR作成準備
- コミットメッセージの作成
- PR説明の準備

### 残作業（あれば）
- [必要に応じて記載]
```

### 6. コミット・PR作成

#### ステージング・コミット作成
```bash
# 実装ファイルのステージング（安全に個別追加）
!git add src/models/issue_${ARGUMENTS}_model.py
!git add src/service/issue_${ARGUMENTS}_service.py  
!git add src/api/main_api.py
!git add tests/unit/test_issue_${ARGUMENTS}_service.py
!git add tests/integration/test_issue_${ARGUMENTS}_api.py

# ドキュメントファイルのステージング  
!git add docs/issue-$ARGUMENTS/implementation/implementation-result.md

# ステージング内容の確認
!git status
!git diff --cached

# コミット作成
!git commit -m "$(cat <<'EOF'
Implement Issue #$ARGUMENTS: [機能名の簡潔な説明]

- Add new data model for Issue #$ARGUMENTS functionality
- Implement service layer with business logic
- Add API endpoint for new feature
- Include comprehensive unit and integration tests
- Ensure type safety and code quality standards

Closes #$ARGUMENTS

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

#### リモートプッシュ・PR作成
```bash
# リモートブランチへプッシュ
!git push -u origin "feature/issue-$ARGUMENTS-$(date +%m%d)"

# Pull Request作成
!gh pr create --title "Issue #$ARGUMENTS: [機能名の簡潔な説明]" --body "$(cat <<'EOF'
## 概要
Issue #$ARGUMENTS の要求に基づく新機能実装

## 実装内容
### 新規機能
- [Issue要求の主要機能]

### 技術的実装
- **データモデル**: Pydantic v2によるスキーマ定義
- **サービス層**: ビジネスロジックの実装
- **API層**: RESTエンドポイントの追加
- **テスト**: ユニット・統合テストの完全実装

## 変更ファイル
### 新規作成
- `src/models/issue_${ARGUMENTS}_model.py`
- `src/service/issue_${ARGUMENTS}_service.py`
- `tests/unit/test_issue_${ARGUMENTS}_service.py`
- `tests/integration/test_issue_${ARGUMENTS}_api.py`

### 既存修正
- `src/api/main_api.py`

## テスト結果
- ✅ ユニットテスト: 全件成功
- ✅ 統合テスト: 全件成功  
- ✅ 型チェック: 合格
- ✅ リントチェック: 合格
- ✅ テストカバレッジ: [カバレッジ%]%

## レビューポイント
- [ ] Issue要求の実装完全性
- [ ] 既存コードとの整合性
- [ ] エラーハンドリングの適切性
- [ ] テストの網羅性

## 関連ドキュメント
- [分析レポート](docs/issue-$ARGUMENTS/analysis/analysis-summary.md)
- [実装ガイド](docs/issue-$ARGUMENTS/implementation/step7-final-implementation-guide.md)
- [実装結果](docs/issue-$ARGUMENTS/implementation/implementation-result.md)

Closes #$ARGUMENTS

🤖 Generated with [Claude Code](https://claude.ai/code)
EOF
)"
```

### 7. Issue最終更新

#### 実装完了報告
```bash
# PR作成完了をIssueに報告
!PR_NUMBER=$(gh pr view --json number --jq .number)
!gh issue comment $ARGUMENTS --body "## ✅ 実装完了・PR作成

### 🚀 Pull Request作成
- **PR**: #${PR_NUMBER}
- **ブランチ**: \`feature/issue-$ARGUMENTS-$(date +%m%d)\`

### 📋 実装内容
- Issue要求の全機能実装完了
- 包括的なテストケース実装完了
- 品質チェック（型・リント・テスト）全て合格

### 🔍 品質保証結果
- ✅ 型チェック合格
- ✅ リントチェック合格  
- ✅ ユニットテスト全件成功
- ✅ 統合テスト全件成功
- ✅ テストカバレッジ基準クリア

### 📁 完全なトレーサビリティ
- **要求分析**: [docs/issue-$ARGUMENTS/analysis/](docs/issue-$ARGUMENTS/analysis/)
- **実装ガイド**: [docs/issue-$ARGUMENTS/implementation/](docs/issue-$ARGUMENTS/implementation/)  
- **実装結果**: [docs/issue-$ARGUMENTS/implementation/implementation-result.md](docs/issue-$ARGUMENTS/implementation/implementation-result.md)
- **Pull Request**: #${PR_NUMBER}

### 🎯 次ステップ
1. PRレビュー・承認
2. マージ後のIssueクローズ
3. 必要に応じてリリースノート更新"

# 最終ラベル更新
!gh issue edit $ARGUMENTS --add-label "implementation-completed,pr-created" --remove-label "implementation-ready"
```

#### ワークフロー完了処理
```bash
# ワークフロー状況の最終更新
!cat "docs/issue-$ARGUMENTS/workflow-status.json" | jq '.workflow_status = "completed" | .end_time = "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'" | .implementation_completed = true | .pr_created = true' > temp.json && mv temp.json "docs/issue-$ARGUMENTS/workflow-status.json"

# 成果物サマリーの作成
!cat > "docs/issue-$ARGUMENTS/workflow-summary.md" << EOF
# Issue #$ARGUMENTS ワークフロー完了サマリー

## 概要
- **Issue**: #$ARGUMENTS
- **開始**: $(cat "docs/issue-$ARGUMENTS/workflow-status.json" | jq -r .start_time)
- **完了**: $(cat "docs/issue-$ARGUMENTS/workflow-status.json" | jq -r .end_time)
- **PR**: #${PR_NUMBER}

## 成果物
- **分析フェーズ**: docs/issue-$ARGUMENTS/analysis/
- **実装ガイド**: docs/issue-$ARGUMENTS/implementation/
- **実装結果**: feature/issue-$ARGUMENTS-$(date +%m%d) ブランチ

## 品質保証
- 全自動チェック合格
- 全テスト成功
- 完全なドキュメンテーション

## トレーサビリティ確保
Issue → 分析 → 実装ガイド → 実装 → PR の完全な履歴
EOF
```

---

## 実行完了確認

### 最終チェック項目
- [ ] 全実装ファイル作成・修正完了
- [ ] 全テスト実装・実行成功
- [ ] 品質チェック全て合格
- [ ] コミット・プッシュ完了
- [ ] Pull Request作成完了
- [ ] Issue進捗更新完了
- [ ] ドキュメント成果物完了

### 完了後の状況
- Issue #$ARGUMENTS: `implementation-completed,pr-created` ラベル
- PR #[番号]: レビュー待ち状態
- 全ドキュメント: `docs/issue-$ARGUMENTS/` に保存
- 実装成果物: PR内で確認可能

## 次ステップ

### PRレビュー・マージ後
```bash
# Issue自動クローズ（PRマージ時）
# 必要に応じてリリースノート作成
```