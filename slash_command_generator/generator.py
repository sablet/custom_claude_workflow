"""
複数テンプレート対応スラッシュコマンド生成スクリプト

YAMLの設定ファイルとJinjaテンプレートから統一されたスラッシュコマンドを生成します。
複数のテンプレート+設定ペアを扱えます。
"""

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
import argparse
import shutil


def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(
        description="Universal template対応スラッシュコマンド生成スクリプト"
    )
    
    parser.add_argument(
        "config_name",
        nargs="?",
        default="software-dev",
        help="使用する設定名（デフォルト: software-dev）"
    )
    
    args = parser.parse_args()
    
    # ファイルパスの設定
    script_dir = Path(__file__).parent
    config_file = script_dir / "configs" / f"{args.config_name}.yaml"
    template_file = script_dir / "templates" / "universal-template.md"
    
    # ファイル存在確認
    if not config_file.exists():
        print(f"✗ エラー: 設定ファイルが見つかりません: {config_file}")
        return
    
    if not template_file.exists():
        print(f"✗ エラー: テンプレートファイルが見つかりません: {template_file}")
        return
    
    # 設定ファイルの読み込み
    print(f"設定ファイルを読み込み中... ({config_file})")
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # output_pathのtilde展開処理
    config['common']['output_path'] = str(Path(config['common']['output_path']).expanduser().resolve())
    
    # 出力ディレクトリの設定（tilde展開対応）
    output_dir = Path(config['common']['commands_output_dir']).expanduser().resolve()
    
    # Jinjaテンプレートの設定
    print(f"テンプレートを設定中... ({template_file})")
    env = Environment(
        loader=FileSystemLoader(template_file.parent),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    template = env.get_template(template_file.name)
    
    # 出力ディレクトリの削除と再作成
    if output_dir.exists():
        print(f"既存の出力ディレクトリを削除中... ({output_dir})")
        shutil.rmtree(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"出力ディレクトリを作成しました: {output_dir}")
    
    # 各ステップのコマンドを生成
    print(f"コマンドファイル生成中... (設定: {args.config_name})")
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