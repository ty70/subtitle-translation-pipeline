# -----------------------------------------------
# ass_replace_with_translation.py
#
# ASS形式の字幕ファイル（.ass）内の英語字幕を翻訳済みの日本語に置換するスクリプト。
#
# 用途:
#   JSONファイルで与えられた翻訳文（行番号と対応した日本語文）を用いて、
#   ASSファイルの字幕テキストを置換、または日英両表示に編集する。
#
# 入力:
#   --input    : 入力用のASS字幕ファイル（例: modify.ass）
#   --json     : 翻訳済みの字幕情報を含むJSONファイル（output.json）
#   --mode     : 表示モード（'replace'=日本語のみ表示, 'dual'=日本語+英語両方表示）
#
# 出力:
#   --output   : 日本語に置換されたASS字幕ファイル（例: modified_output.ass）
#
# 使用例:
#   python ass_replace_with_translation.py --input modify.ass --json output.json --output modified_output.ass --mode dual
# -----------------------------------------------
import argparse
import json
import re

def parse_args():
    parser = argparse.ArgumentParser(description="Replace ASS subtitle text using a JSON translation mapping")
    parser.add_argument('--input', required=True, help='Input ASS file path')
    parser.add_argument('--json', required=True, help='JSON file with translated subtitles')
    parser.add_argument('--output', required=True, help='Output ASS file path')
    parser.add_argument('--mode', choices=['replace', 'dual'], default='replace', help='Display mode: replace or dual-language')
    return parser.parse_args()

def load_translation(json_path):
    with open(json_path, encoding='utf-8') as f:
        return json.load(f)

def replace_subtitles(input_path, output_path, translation_data, mode='replace'):
    with open(input_path, encoding='utf-8') as f:
        lines = f.readlines()

    dialogue_lines = []
    current_line = 0
    for i, line in enumerate(lines):
        if line.startswith("Dialogue:"):
            dialogue_lines.append((i, current_line))
            current_line += 1

    for entry in translation_data:
        start, end, ja_lines = entry['start_line'], entry['end_line'], entry['ja']
        for i in range(start - 1, end):
            if i >= len(dialogue_lines):
                continue
            idx, _ = dialogue_lines[i]
            original_line = lines[idx]
            match = re.match(r"(Dialogue: [^,]+,[^,]+,[^,]+,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,)(.*)", original_line)
            if match:
                prefix = match.group(1)
                original_text = match.group(2).strip()
                if mode == 'replace':
                    new_text = '\\N'.join(ja_lines)
                elif mode == 'dual':
                    new_text = '\\N'.join(ja_lines + [original_text])  # 日本語上、英語下
                lines[idx] = prefix + new_text + '\n'

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def main():
    args = parse_args()
    translations = load_translation(args.json)
    replace_subtitles(args.input, args.output, translations, mode=args.mode)
    print(f"✅ Output saved to {args.output}")

if __name__ == '__main__':
    main()
