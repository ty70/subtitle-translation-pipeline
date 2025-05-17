#!/usr/bin/env python3
# ------------------------------------------
# ass_replace_with_translation.py
#
# 概要:
#   ASS形式の字幕ファイルのセリフを、翻訳済みの日本語テキスト（JSON形式）で置換するスクリプト。
#
# 用途:
#   英語のASS字幕を、日本語訳に差し替えて動画に焼き込む用途に使用。
#
# 入力:
#   --input     : 置換対象のASS字幕ファイル（.ass）
#   --json      : 日本語訳が格納されたJSONファイル（output.json形式）
#   --output    : 出力先ASS字幕ファイルパス
#
# 出力:
#   指定されたパスに、日本語訳が反映されたASS字幕ファイルを保存。
# ------------------------------------------

import json
import argparse

def replace_ass_text(input_ass, output_json, output_ass):
    # JSON読み込み
    with open(output_json, "r", encoding="utf-8") as f:
        translations = json.load(f)

    # 行番号 → テキストのマップを作成
    translation_map = {}
    for entry in translations:
        for i, ja_line in enumerate(entry["ja"]):
            line_num = entry["start_line"] + i
            translation_map[line_num] = ja_line

    # ASS変換処理
    output_lines = []
    line_counter = 0
    in_events = False

    with open(input_ass, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("[Events]"):
                in_events = True
                output_lines.append(line)
                continue

            if in_events and line.startswith("Dialogue:"):
                line_counter += 1
                if line_counter in translation_map:
                    parts = line.strip().split(",", 9)
                    if len(parts) == 10:
                        parts[-1] = translation_map[line_counter]
                        new_line = ",".join(parts) + "\n"
                        output_lines.append(new_line)
                    else:
                        output_lines.append(line)
                else:
                    output_lines.append(line)
            else:
                output_lines.append(line)

    # 書き出し
    with open(output_ass, "w", encoding="utf-8") as f:
        f.writelines(output_lines)

    print(f"✅ 字幕を日本語に置換しました: {output_ass}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ASS字幕ファイルの英語テキストを翻訳済み日本語に置換")
    parser.add_argument('--input', required=True, help='元のASS字幕ファイル（.ass）')
    parser.add_argument('--json', required=True, help='翻訳結果のJSONファイル（output.json）')
    parser.add_argument('--output', required=True, help='置換後に保存するASSファイルの出力パス')

    args = parser.parse_args()

    replace_ass_text(args.input, args.json, args.output)
