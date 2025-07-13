---
allowed-tools: ["Read", "Write", "Edit", "Bash"]
description: "Orchestrates recursive business process decomposition using interview tool"
---

# Business Process Decomposition Orchestrator

**前提**: このコマンドは `@commands/v2/decompose-business-process.md` ヒアリングツールを再帰的に制御して、完全なBusinessProcessDefinitionを構築します。

## Target Specification

**分解対象:** $ARGUMENTS

初期ビジネス要求またはプロセス名を指定してください。

## Phase 1: Root Process Discovery

### 1.1 初期プロセス定義
ルートプロセスの基本プロパティを収集します：

**実行アクション:**
- `/project:decompose-business-process $ARGUMENTS` を実行
- ルートプロセスの基本情報を収集
- ProcessNode構造をJSONで生成・保存

**成果物:**
- `output/data/root-process-YYYYMMDD-HHMMSS.json`

### 1.2 分解要否判定
ルートプロセスのタイプに基づいて分解戦略を決定：

**primitive プロセスの場合:**
- 分解完了：単一ProcessNodeとしてBusinessProcessDefinition生成

**compound プロセスの場合:**
- Phase 2へ進行：サブプロセス特定を開始

## Phase 2: Sub-Process Identification

### 2.1 複雑度評価と分解戦略
ルートプロセスの複雑度を評価して分解アプローチを決定：

**質問1: プロセス構成要素の特定**
このプロセスはどのような構成要素（サブプロセス）で成り立っていますか？
- 各構成要素の名称と役割
- 構成要素間の関係性（依存関係、並行性等）
- 既存プロセスとの組み合わせ可能性

**質問2: プロセス組み合わせパターン**
このプロセスはどのような実行パターンで構成されますか？
- 順次実行（A→B→C）
- 条件分岐（条件に応じてA or B）
- 並行実行（AとBを同時実行）
- 繰り返し実行（条件を満たす間Aを反復）
- 複合パターン（上記の組み合わせ）

**質問3: 再利用可能プロセスの特定**
既存の業務プロセスや標準的なプロセスパターンを活用できますか？
- 他の業務で使用している類似プロセス
- 標準的なビジネスパターン（承認、検証、通知等）
- 組織共通のプロセス資産

### 2.2 プロセス組み合わせ候補の提示と選択
プロセスの組み合わせ候補を生成・提示してユーザー確認を実施：

**組み合わせ候補生成:**

**候補A: 階層型組み合わせ**
- 機能的プロセス群による階層構造
- 入力→業務ロジック→出力の明確な分離
- **概要:** 理解しやすく保守性が高い標準的パターン
- **メリット:** 分業化しやすい、影響範囲が限定的
- **デメリット:** 処理時間が長くなる可能性
- **適用場面:** 安定性重視、チーム開発

**候補B: パイプライン型組み合わせ**
- プロセス間のデータフローを最適化
- 並行処理による性能向上
- **概要:** 高速処理を重視したストリーミングパターン
- **メリット:** 高性能、リアルタイム処理可能
- **デメリット:** 設計・デバッグが複雑
- **適用場面:** 大量データ処理、リアルタイム要件

**候補C: イベント駆動型組み合わせ**
- 非同期イベントによる疎結合
- 動的なプロセス組み合わせ
- **概要:** 柔軟性と拡張性を重視したパターン
- **メリット:** 高い拡張性、システム間連携が容易
- **デメリット:** 実行順序の制御が困難
- **適用場面:** 複雑な業務フロー、システム統合

**組み合わせ選択確認:**
- どの組み合わせ候補が要件に適していますか？
- 各候補の概要説明で不明な点はありますか？
- 複数候補の要素を組み合わせたいですか？
- カスタムな組み合わせパターンが必要ですか？

## Phase 3: Flow Control Definition

### 3.1 高度なプロセス制御フロー設計
複雑なプロセス組み合わせに対応する制御フロー定義：

**拡張フロータイプ:**
- **SEQUENCE**: 順次実行（A→B→C）
- **PARALLEL**: 並行実行（A, B, C を同時実行）
- **BRANCH**: 条件分岐（条件によってA or B or C）
- **LOOP**: 反復実行（条件を満たす間A-B-Cを繰り返し）
- **PIPELINE**: パイプライン実行（Aの出力をBが処理中にAが次を処理）
- **EVENT_DRIVEN**: イベント駆動（イベント発生時にプロセス実行）
- **HYBRID**: 複合パターン（上記の組み合わせ）

**制御フロー最適化:**
- 並行実行機会の最大化
- 依存関係の最小化
- リソース競合の回避
- デッドロック防止設計

### 3.2 ProcessFlow候補提示と選択
収集した情報から複数のProcessFlow候補を生成・提示：

**候補生成戦略:**
1. 最適性能重視パターン（並行処理最大化）
2. 安全性重視パターン（順次処理・エラー処理強化）
3. 柔軟性重視パターン（動的分岐・拡張性確保）
4. 簡潔性重視パターン（シンプルな制御フロー）

**候補提示とユーザー確認:**

**候補A: 性能最適化パターン**
```yaml
flow_type: "PARALLEL"
概要: 並行実行を最大化し、処理時間を最短化
メリット: 高速処理、リソース効率化
デメリット: 複雑性増加、依存関係管理が必要
適用場面: 高処理量、時間制約が厳しい場合
```

**候補B: 安全性重視パターン**
```yaml
flow_type: "SEQUENCE"
概要: 順次実行でエラー発生時の影響を最小化
メリット: デバッグ容易、安定性高い
デメリット: 処理時間が長い
適用場面: 重要業務、確実性が求められる場合
```

**候補C: 柔軟性重視パターン**
```yaml
flow_type: "HYBRID"
概要: 条件に応じて動的に実行パターンを変更
メリット: 様々な状況に対応可能
デメリット: 設計・テストが複雑
適用場面: 多様な条件・例外が想定される場合
```

**候補選択と確認:**
- どの候補が要件に最も適していますか？
- 各候補の概要で不明な点はありますか？
- 候補を組み合わせたカスタムパターンが必要ですか？
- 修正・調整したい箇所はありますか？

## Phase 4: Recursive Sub-Process Definition

### 4.1 サブプロセス詳細化
特定された各サブプロセスについて再帰的に詳細を定義：

**各サブプロセスに対して実行:**
1. `/project:decompose-business-process [SUB-PROCESS-NAME]` を実行
2. サブプロセスの詳細プロパティを収集
3. ProcessNode構造を生成・保存

**成果物:**
- `output/data/process-[SUB-PROCESS-ID]-YYYYMMDD-HHMMSS.json`

**プロセス完了時の状態保存:**
- `output/sessions/decomposition-session-[SESSION_ID]-YYYYMMDD-HHMMSS.json`

### 4.2 プロセス組み合わせの再帰展開
compound プロセスの組み合わせパターンを再帰的に展開：

**展開継続条件:**
- プロセスがさらなる組み合わせで構成される場合
- 組み合わせ最適化の余地がある場合
- 新しいプロセスパターンが発見された場合

**展開アクション:**
- プロセス組み合わせパターンの深度展開（制限なし）
- 組み合わせ最適化の継続実行
- プロセス資産ライブラリとの照合・統合

## Phase 5: Integration & Validation

### 5.1 プロセス統合
すべてのプロセス定義を統合してBusinessProcessDefinitionを構築：

**統合処理:**
1. 全ProcessNodeファイルの読み込み
2. プロセス参照整合性の検証
3. データフロー連続性の検証
4. 制約条件の整合性確認

### 5.2 完全性検証
定義された構造の完全性を検証：

**検証項目:**
1. **参照整合性**: すべてのprocess_refが定義済み
2. **データフロー**: 入力→出力の連続性
3. **制約充足**: 全制約事項の確認
4. **循環参照**: 無限ループの防止

**検証失敗時の対応:**
- 不整合箇所の特定・報告
- 修正が必要なプロセスの再ヒアリング実行

## Phase 6: Output Generation

### 6.1 最終成果物生成
完全なBusinessProcessDefinitionと関連ドキュメントを生成：

**生成ファイル:**
1. **完全なBusinessProcessDefinition**
   - `output/docs/business-process-definition-YYYYMMDD-HHMMSS.json`

2. **プロセス階層構造図**
   - `output/docs/process-hierarchy-YYYYMMDD-HHMMSS.md`

3. **分解プロセスサマリー**
   - `output/reports/decomposition-process-YYYYMMDD-HHMMSS.html`

4. **プロセス一覧表**
   - `output/reports/process-list-YYYYMMDD-HHMMSS.csv`

### 6.2 次のステップ提案
生成されたBusinessProcessDefinitionの活用方法を提案：

**活用オプション:**
- 実装計画書の生成
- テストケースの生成
- 業務フロー図の作成
- システム要件定義書への変換

## Execution Control

### プロセス組み合わせ最適化制御
無限展開を防ぎつつ最適な組み合わせを追求：

**最適化指針:**
- プロセス再利用性の最大化
- 組み合わせパターンの多様性確保
- 実行効率とメンテナンス性のバランス

**制御機構:**
- 循環参照の検出・回避
- プロセス依存関係のグラフ解析
- 組み合わせ複雑度の動的評価
- ユーザーによる展開継続判断

### プロセス組み合わせ進捗管理
プロセス組み合わせ最適化の進捗を管理：

**進捗情報:**
- 定義済みプロセス数（制限なし）
- プロセス組み合わせパターン数
- 再利用可能プロセス識別率
- 組み合わせ最適化完了度

**継続・拡張機能:**
- 組み合わせセッション状態の保存
- プロセス資産ライブラリへの蓄積
- 段階的組み合わせ最適化の実行
- 組み合わせパターンの進化的改善

## Session Management & Resume

### セッション状態保存
各プロセス完了タイミングで途中経過を自動保存：

**保存タイミング:**
- 各個別プロセス定義完了時
- フロー制御定義完了時
- プロセス統合・検証完了時
- ユーザーによる明示的保存要求時

**保存内容（DecompositionSession）:**
```yaml
session_id: "[一意セッションID]"
created_at: "[作成日時]"
last_updated: "[最終更新日時]"
status: "[active/paused/completed]"
target_process: "[対象プロセス名]"
current_phase: "[現在のフェーズ]"
progress:
  defined_processes: "[定義済みプロセスリスト]"
  pending_processes: "[未定義プロセスリスト]"
  process_relationships: "[プロセス間関係]"
  flow_definitions: "[定義済みフロー]"
artifacts:
  process_files: "[生成済みプロセスファイルパス]"
  session_data: "[セッション固有データ]"
next_actions: "[次の実行アクション]"
user_context: "[ユーザー提供コンテキスト]"
```

**保存先:**
- `output/sessions/decomposition-session-[SESSION_ID]-YYYYMMDD-HHMMSS.json`

### セッション再開機能

**再開コマンド:**
`/project:orchestrate-decomposition --resume [SESSION_ID]`

**再開処理:**
1. セッションファイルの読み込み
2. 既存プロセス定義の復元
3. 進行状況の表示
4. 中断箇所からの継続実行

**再開時の確認事項:**
- 前回セッションの進捗状況表示
- 定義済みプロセス一覧の確認
- 次に実行すべきアクションの提示
- ユーザーによる継続可否の確認

### セッション管理コマンド

**セッション一覧表示:**
`/project:orchestrate-decomposition --list-sessions`

**セッション詳細表示:**
`/project:orchestrate-decomposition --show-session [SESSION_ID]`

**セッション削除:**
`/project:orchestrate-decomposition --delete-session [SESSION_ID]`

---

**使用方法:**
- 新規分解: `/project:orchestrate-decomposition [初期ビジネス要求またはプロセス名]`
- セッション再開: `/project:orchestrate-decomposition --resume [SESSION_ID]`
- セッション管理: `/project:orchestrate-decomposition --list-sessions | --show-session [ID] | --delete-session [ID]`

**特徴:**
このコマンドはプロセス組み合わせを重視した設計により、単一プロセス定義ツールを再帰的に制御します。数的制限を設けず、最適なプロセス組み合わせパターンを探求し、再利用性と拡張性に優れたBusinessProcessDefinitionを生成します。プロセス資産の蓄積と継続的最適化を支援します。