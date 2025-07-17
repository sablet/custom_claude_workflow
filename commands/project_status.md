---
description: "全プロジェクトのproject_idとステータス・更新時刻を一覧表示（拡張対応）"
allowed-tools: ["Read", "LS", "Bash", "Glob"]
---

# プロジェクトステータス一覧表示（汎用版）

全ての設定済みプロジェクトのproject_idとステータス・直近更新時刻を確認します。
新しい設定ファイルが追加されても自動で検出・対応します。

## 実行手順

### 1. 設定ファイルの自動検出と読み込み

```bash
# 全設定ファイルを自動検出
!find ~/.claude/slash_command_generator/configs/ -name "*.yaml" -type f
```

各設定ファイルを順次読み込み、以下の情報を抽出:
- プロジェクト名（ファイル名から推定）
- phase_structure.phases
- commands_output_dir（出力ディレクトリパス）
- individual_elements.dependencies_check（依存関係）

### 2. 出力ディレクトリとファイル存在確認

設定ファイルから取得したcommands_output_dirを使用:

```bash
# 各プロジェクトの出力ディレクトリを確認
!ls -la ~/.claude/commands/development_planning_v3/
!ls -la ~/.claude/commands/travel_planning/
# 将来の設定追加時も自動対応
```

### 3. ファイル詳細情報とステータス判定

各 .md ファイルについて:
- 存在確認
- ファイルサイズ
- 更新時刻（mtime）取得
- ステータス判定

```bash
# ファイル詳細情報取得例
!stat ~/.claude/commands/development_planning_v3/phase1-step1.md
!stat ~/.claude/commands/travel_planning/phase1-step1-planning.md
```

### 4. 依存関係解析とブロック状態検出

各ステップのdependencies_checkを解析し:
- 依存するステップの完了状況確認
- ブロック状態の判定
- 実行可能な次ステップの特定

### 5. 統合レポート生成

```markdown
## 📊 プロジェクトステータス一覧 (${TIMESTAMP})

### 📈 全体サマリー
- **検出プロジェクト数**: X個
- **総ステップ数**: X個
- **完了済み**: X個 (XX%)
- **進行中**: X個 (XX%)
- **未着手**: X個 (XX%)
- **依存関係ブロック**: X個

---

### 🚀 [Project Name] (${CONFIG_FILE})
**出力先**: ${COMMANDS_OUTPUT_DIR}

| Phase | Step ID | Description | Status | Size | Last Modified | Dependencies |
|-------|---------|-------------|--------|------|---------------|--------------|
| Phase1 | step-id-1 | 説明 | ✅ 完了 | 2.1KB | 2024-01-15 14:30 | - |
| Phase1 | step-id-2 | 説明 | ⚠️ 部分 | 0.5KB | 2024-01-15 16:45 | step-id-1 |
| Phase2 | step-id-3 | 説明 | ❌ 未作成 | - | - | step-id-1,2 |
| Phase2 | step-id-4 | 説明 | 🔒 ブロック | - | - | step-id-3 |

**次の実行可能ステップ**: step-id-3 (依存関係満たし済み)

---

### 🧳 [Another Project] (${CONFIG_FILE})
[同様の形式で表示]

---

### 🔄 依存関係ツリー

#### [Project Name]
```
├── step-id-1 ✅ (2024-01-15 14:30)
├── step-id-2 ⚠️ (2024-01-15 16:45) ← step-id-1
├── step-id-3 ❌ ← step-id-1,2 🔒
└── step-id-4 ❌ ← step-id-3 🔒
```

#### [Another Project]
[同様の形式で表示]

### 🚦 アクション推奨

#### 即座に実行可能
- `/${COMMAND}` - step-id-3 (依存関係満たし済み)

#### 完了が推奨
- step-id-2 (部分完了状態)

#### ブロック解除待ち
- step-id-4 (step-id-3完了待ち)
```

## ステータス判定基準

- **✅ 完了**: .mdファイルが存在し、ファイルサイズが500バイト以上
- **⚠️ 部分**: .mdファイルは存在するが、ファイルサイズが500バイト未満
- **❌ 未作成**: .mdファイルが存在しない
- **🔒 ブロック**: 依存するステップが未完了のため実行不可

## 実装の拡張性

### 新しいプロジェクト設定の自動検出
1. `~/.claude/slash_command_generator/configs/` 配下の `.yaml` ファイルを動的スキャン
2. 各YAMLファイルの以下構造を解析:
   ```yaml
   common:
     commands_output_dir: "~/.claude/commands/[project_name]"
   phase_structure:
     phases: [...]
   individual_elements:
     dependencies_check: [...]
   ```

### 設定ファイル形式の標準化確認
- `phase_structure.phases` の存在確認
- `commands_output_dir` の有効性検証
- 標準的でない設定ファイルは警告表示

### エラーハンドリング
- 設定ファイル読み込みエラー
- 出力ディレクトリアクセスエラー
- YAML構造異常の検出と報告

## 使用例

```bash
# 基本実行
/project-status

# 詳細情報付き（ファイル内容プレビュー等）
/project-status --detailed

# 特定プロジェクトのみ
/project-status --filter development_planning_v3

# 更新時刻でソート
/project-status --sort-by-time

# 依存関係ツリーのみ表示
/project-status --tree-only
```