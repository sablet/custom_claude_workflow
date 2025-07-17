---
allowed-tools: ["Read", "Write", "Edit", "Bash"]
description: "ユーザーとシステムのインタラクションをシーケンス図で設計"
---# Phase1-Step3（ユーザーインタラクション設計）

プロジェクトID: $ARGUMENTS

## 概要
ユーザーがシステムとどのように関わり、どのような情報交換が行われるかを**ユースケース別シーケンス図**を用いて視覚的に表現します。これにより、ユーザーとシステムの間のやり取り、およびインターフェースの振る舞いを明確にします。


## プロジェクト全体構想

この手順は以下の全体的なフェーズ構造の一部です：

### Phase 1: 要件定義フェーズ
プロジェクトの目的、ユーザー要件、インタラクション設計を明確化
- /Users/mikke/Documents/planning_docs/development_planning_v3/$ARGUMENTS/phase1-step1-idea-and-goals.md # アイデアと目標の明確化
- /Users/mikke/Documents/planning_docs/development_planning_v3/$ARGUMENTS/phase1-step2-user-requirements.md # ユーザー要件定義
- **🎯 /Users/mikke/Documents/planning_docs/development_planning_v3/$ARGUMENTS/phase1-step3-user-interaction.md** # ユーザーインタラクション設計 ← **現在のステップ**

### Phase 2: システム設計フェーズ
データ構造、システムフロー、API設計を策定
- /Users/mikke/Documents/planning_docs/development_planning_v3/$ARGUMENTS/phase2-step1-data-structure.md # データ構造定義
- /Users/mikke/Documents/planning_docs/development_planning_v3/$ARGUMENTS/phase2-step2-system-dataflow.md # システム全体データフロー設計
- /Users/mikke/Documents/planning_docs/development_planning_v3/$ARGUMENTS/phase2-step3-api-design.md # API設計（個別API）

### Phase 3: 実装準備フェーズ
テスト計画と実装設計を完成
- /Users/mikke/Documents/planning_docs/development_planning_v3/$ARGUMENTS/phase3-step1-test-plan.md # テスト計画策定
- /Users/mikke/Documents/planning_docs/development_planning_v3/$ARGUMENTS/phase3-step2-implementation-design.md # 実装設計


**複数の質問がある場合の処理原則**：
複数の項目について確認が必要な場合は、必ず一つずつ順番に処理し、各質問の回答を確認してから次の質問に進む。一度に全ての質問を提示することは避け、段階的なアプローチを取る。


## 実行手順

### 1. 前ステップの成果物確認

実際の作成済みファイル一覧
```bash
!mkdir -p /Users/mikke/Documents/planning_docs/development_planning_v3/$ARGUMENTS
!tree -L 2 /Users/mikke/Documents/planning_docs/development_planning_v3/$ARGUMENTS | ls -l /Users/mikke/Documents/planning_docs/development_planning_v3/$ARGUMENTS
```

### 2. 依存関係の確認

依存元のドキュメントを確認してから次に進んでください


- **依存元**: Phase1-Step2（ユーザー要件定義）
- **依存先**: Phase2-Step3（API設計）、Phase3-Step1（テスト計画策定）
### 3. 情報収集と質問

**対話原則：**
- ユーザーの入力負荷を軽減するため、選択肢形式での質問を優先
- 複数の質問がある場合は、必ず一つずつ順番に処理し、各質問の回答を確認してから次の質問に進む
- 曖昧な回答には具体例を提示して明確化を図る
- ユーザーの理解レベルや経験に合わせた現実的な提案を行う

**段階的質問テンプレート：**
```
[{purpose}]のため、まず最初の項目について番号で選択してください：

## {item_title}
以下から該当するものを選んでください（複数選択可）：
1. {option1_description}
2. {option2_description}
3. {option3_description}
4. その他（具体的に記入：_______）
---
User: 回答例: 1, 3
（{item_title}の回答を確認後、次の項目について質問）

---

## {next_item_title}
以下から最も近いものを選んでください：
1. {option1_description}
2. {option2_description}
3. {option3_description}
4. その他（具体的に記入：_______）

---
User: 回答例: 2
```


**確認すべき項目：**
- 各ユーザーストーリーの具体的なワークフローは明確ですか？
- ユーザーがシステムとどうやり取りするか具体的にイメージできますか？
- 各機能での入力・出力データは何ですか？
- エラーや例外ケースはどのようなものがありますか？
- UI/UXのイメージや選好はありますか？


### 4. 設計案の提示と承認
収集した情報を基に、設計案を提示し、ユーザーの承認を得てください。

### 5. 最終確認とドキュメント作成

承認された内容を @/Users/mikke/Documents/planning_docs/development_planning_v3/$ARGUMENTS/phase1-step3-user-interaction.md に出力してください

## 重要な対話ポイント
- ユーザーが「普通にやればいい」と答えた場合は、具体的なシナリオを例示して詳細を引き出してください
- UIのイメージが曖昧な場合は、他のサービスを例に出して具体化してください
- エラーケースは「どんなことがうまくいかないか」を具体的に想像してもらってください
- シーケンス図は最初はシンプルに、必要に応じて詳細化するアプローチを取ってください



### 6. ステップ完了後の次ステップガイド
### 🚀 次のステップガイド

このステップで収集・整理した情報を基に、次の候補ステップを提案してください：

**ガイド原則**:
- 今回の成果物の内容に基づいて適切な次ステップを提案
- 不要と思われるステップには理由とともにスキップ提案
- 各候補ステップで何をするかを簡潔に説明
- 実行コマンドを明示
- 最終的な選択はユーザーに委ねる

**スキップ判断基準例**:
- データ量が少ない/構造が単純 → phase2-step1（データ構造定義）をスキップしてphase2-step3（API設計）へ
- UIがない/最小限 → phase1-step3（インタラクション設計）をスキップしてphase2-step1へ
- データフローが単純 → phase2-step2（システム全体データフロー）をスキップしてphase2-step3へ
- テストより実装を優先 → phase3-step1（テスト計画）をスキップしてphase3-step2へ

