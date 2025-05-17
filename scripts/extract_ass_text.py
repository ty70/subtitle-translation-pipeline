#!/usr/bin/env python3
# ------------------------------------------
# extract_ass_text.py
#
# 概要:
#   ASS字幕ファイルから英語テキストを抽出
#
# 用途:
#   英語のASS字幕を、日本語訳に差し替えて動画に焼き込む用途に使用。
#
# 入力:
#   --input     : 抽出対象のASS字幕ファイル（.ass）
#   --output    : 抽出された英文（.txt)
#
# 出力:
#   指定されたパスに、抽出された英文を保存。
# ------------------------------------------

import argparse
import sys

def extract_text_from_ass(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    text_lines = []
    is_event_section = False
    for i, line in enumerate(lines):
        if i < 14:
            continue  # 15行目以降を処理
        if line.startswith("Dialogue:"):
            # print(f"line: {line}")
            try:
                # Dialogue の各要素を分割し、10番目以降が Text（9個のカンマで区切られた後）
                parts = line.split(",", 9)
                if len(parts) >= 10:
                    text = parts[9].strip()
                    # print(f"text: {text}")
                    text_lines.append(text)
            except Exception as e:
                print(f"Error processing line: {line}\n{e}")

    with open(output_file, 'w', encoding='utf-8') as out:
        for text in text_lines:
            # print(text)
            out.write(text + "\n")

    print(f"抽出完了: {len(text_lines)} 行のテキストを {output_file} に保存しました。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ASS字幕ファイルから英文を抽出")
    parser.add_argument('--input', required=True, help='ASS字幕ファイル')
    parser.add_argument('--output', required=True, help='抽出された英文')

    args = parser.parse_args()
    extract_text_from_ass(args.input, args.output)
