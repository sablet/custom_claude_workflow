---
allowed-tools: {{ common.base_tools | tojson }}
description: "{{ individual_elements.description[step_id] }}"
---

{%- macro get_filename(step_id) -%}
  {%- for phase_id, phase_data in phase_structure.phases.items() -%}
    {%- for step in phase_data.steps -%}
      {%- if step.id == step_id -%}
        {{ step.filename }}
      {%- endif -%}
    {%- endfor -%}
  {%- endfor -%}
{%- endmacro -%}

# {{ step_references[step_id] }}

プロジェクトID: $ARGUMENTS

## 概要
{{ individual_elements.overview[step_id] }}

## プロジェクト全体構想

この手順は以下の全体的なフェーズ構造の一部です：

{% for phase_id, phase_data in phase_structure.phases.items() %}
### {{ phase_data.title }}
{{ phase_data.description }}
{% for step in phase_data.steps %}
{% if step.id == step_id %}
- **🎯 {{ common.output_path }}/$ARGUMENTS/{{ step.filename }}** # {{ step.description }} ← **現在のステップ**
{% else %}
- {{ common.output_path }}/$ARGUMENTS/{{ step.filename }} # {{ step.description }}
{% endif %}
{% endfor %}

{% endfor %}

{{ sequential_questioning.principle }}

## 実行手順

### 1. 前ステップの成果物確認

実際の作成済みファイル一覧
```bash
!mkdir -p {{ common.output_path }}/$ARGUMENTS
!tree -L 2 {{ common.output_path }}/$ARGUMENTS | ls -l {{ common.output_path }}/$ARGUMENTS
```

### 2. 依存関係の確認

依存元のドキュメントを確認してから次に進んでください

{% set deps_from_to = individual_elements.dependencies_from_to[step_id] %}
{% set dependencies_from = deps_from_to.from %}
{% set dependencies_to = deps_from_to.to %}

- **依存元**: {% if dependencies_from is string %}{{ dependencies_from }}{% else %}{% for dep in dependencies_from %}{{ step_references[dep] }}{% if not loop.last %}、{% endif %}{% endfor %}{% endif %}

- **依存先**: {% if dependencies_to is string %}{{ dependencies_to }}{% else %}{% for dep in dependencies_to %}{{ step_references[dep] }}{% if not loop.last %}、{% endif %}{% endfor %}{% endif %}

### 3. 情報収集と質問

**対話原則：**
- ユーザーの入力負荷を軽減するため、選択肢形式での質問を優先
- 複数の質問がある場合は、必ず一つずつ順番に処理し、各質問の回答を確認してから次の質問に進む
- 曖昧な回答には具体例を提示して明確化を図る
- ユーザーの理解レベルや経験に合わせた現実的な提案を行う

**段階的質問テンプレート：**
{{ sequential_questioning.template_format }}

**確認すべき項目：**
{% for question in individual_elements.specific_questions[step_id] %}
- {{ question }}
{% endfor %}

{% if special_processes and special_processes[step_id] %}
{% for process_name, process_content in special_processes[step_id].items() %}

{{ process_content }}
{% endfor %}
{% endif %}

### 4. 設計案の提示と承認
収集した情報を基に、設計案を提示し、ユーザーの承認を得てください。

### 5. 最終確認とドキュメント作成

承認された内容を @{{ common.output_path }}/$ARGUMENTS/{{ get_filename(step_id) }} に出力してください

## 重要な対話ポイント
{{ individual_elements.interaction_points[step_id] }}

{% if next_step_guidance.enable %}

### 6. ステップ完了後の次ステップガイド
{{ next_step_guidance.guidance_instruction }}
{% endif %}