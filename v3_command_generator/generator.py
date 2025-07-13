#!/usr/bin/env python3
"""
v3プロジェクト企画フェーズのスラッシュコマンド生成スクリプト

YAMLの設定ファイルとJinjaテンプレートから統一されたスラッシュコマンドを生成します。
"""

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path


def main():
    """メイン実行関数"""
    
    # ファイルパスの設定
    script_dir = Path(__file__).parent
    config_file = script_dir / "config.yaml"
    template_file = script_dir / "template.md"
    
    # 設定ファイルの読み込み
    print("設定ファイルを読み込み中...")
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 出力ディレクトリの設定（script_dirからの相対パス）
    output_dir = script_dir.parent / config['common']['commands_output_dir']
    
    # Jinjaテンプレートの設定
    print("テンプレートを設定中...")
    env = Environment(
        loader=FileSystemLoader(script_dir),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    template = env.get_template("template.md")
    
    # 出力ディレクトリの作成
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 各ステップのコマンドを生成
    print("コマンドファイル生成中...")
    step_references = config['step_references']
    
    for step_id in step_references.keys():
        try:
            # テンプレートのレンダリング
            rendered_content = template.render(
                step_id=step_id,
                **config
            )
            
            # ファイル出力
            output_file = output_dir / f"{step_id}.md"
            output_file.write_text(rendered_content, encoding='utf-8')
            print(f"✓ 生成完了: {output_file}")
            
        except Exception as e:
            print(f"✗ エラー: {step_id} - {str(e)}")
    
    print("✓ 全ての生成処理が完了しました")


if __name__ == "__main__":
    main()