---
allowed-tools: {{ common.base_tools | tojson }}
description: "{{ individual_elements.description[step_id] }}"
---

# {{ step_references[step_id] }}

## 概要
{{ individual_elements.overview[step_id] }}

{% if phase_structure.enable_overview and step_id in phase_structure.show_on_steps %}
## プロジェクト全体構想

この手順は以下の全体的なフェーズ構造の一部です：

{% for phase_id, phase_data in phase_structure.phases.items() %}
### {{ phase_data.title }}
{{ phase_data.description }}
{% for step in phase_data.steps %}
├── {{ step.filename }}{% if step.id == step_id %} **← 現在のステップ**{% endif %} # {{ step.description }}
{% endfor %}

{% endfor %}

{{ sequential_questioning.principle }}

{% endif %}
## 実行手順

### 1. 前ステップの成果物確認
該当するステップのドキュメントを確認し、作業ディレクトリを準備してください：

```bash
!mkdir -p {{ common.output_path }}
```

### 2. 情報収集の原則
不足している情報について、必ず一つずつ順番に質問してください。複数の項目について確認が必要な場合は、必ず一つずつ順番に処理し、各質問の回答を確認してから次の質問に進むこと。

**選択肢形式の質問を優先**：
ユーザーの入力負荷を軽減するため、可能な限り選択肢形式で質問を行う。

**段階的質問テンプレート**：
{{ sequential_questioning.template_format }}

### 前ステップ成果物確認
{% if individual_elements.dependencies_check[step_id] %}
{% for dep in individual_elements.dependencies_check[step_id] %}
* {{ step_references[dep] }}
{% endfor %}
{% else %}
なし
{% endif %}

{% set deps_from_to = individual_elements.dependencies_from_to[step_id] %}
{% set dependencies_from = deps_from_to.from %}
{% set dependencies_to = deps_from_to.to %}

## 依存関係
- **依存元**: {% if dependencies_from is string %}{{ dependencies_from }}{% else %}{% for dep in dependencies_from %}{{ step_references[dep] }}{% if not loop.last %}、{% endif %}{% endfor %}{% endif %}

- **依存先**: {% if dependencies_to is string %}{{ dependencies_to }}{% else %}{% for dep in dependencies_to %}{{ step_references[dep] }}{% if not loop.last %}、{% endif %}{% endfor %}{% endif %}

### 3. 不足情報の確認と質問
**確認すべき項目:**
{% for question in individual_elements.specific_questions[step_id] %}
- {{ question }}
{% endfor %}

不足している情報について、必ず一つずつ順番に質問してください。

{% if special_processes and special_processes[step_id] %}
{% for process_name, process_content in special_processes[step_id].items() %}

{{ process_content }}
{% endfor %}
{% endif %}

### 4. 設計案の提示と承認
収集した情報を基に、設計案を提示し、ユーザーの承認を得てください。

### 5. 最終確認とドキュメント作成

承認された内容を @{{ common.output_path }}{{ step_id }}.md に出力してください

## 重要な対話ポイント
{{ individual_elements.interaction_points[step_id] }}

## 共通の対話原則
{{ common.common_interaction_points }}

{% if next_step_guidance.enable %}
### 6. ステップ完了後の次ステップガイド
{{ next_step_guidance.guidance_instruction }}
{% endif %}