#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
英語テキストファイルを読み込み、ピリオド（.）で文を区切りつつ、
複数行にまたがる文を1文として連結します。

文ごとに元のテキストの行範囲（開始行～終了行）をメタ情報として記録し、
最終的に文とそのメタ情報をJSON形式で出力します。

使用方法:
    python merge_sentences.py --input input.txt --output output.json

引数:
    --input : 入力ファイル（英語テキストファイル）
    --output: 出力ファイル（連結された文と行番号メタ情報をJSONで保存）
"""

import argparse
import json
import re


def merge_lines_into_sentences_with_meta(lines):
    sentences = []
    meta_info = []
    current_sentence = ""
    current_start_line = 0

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        if not stripped_line:
            continue

        if not current_sentence:
            current_start_line = i + 1

        if current_sentence:
            current_sentence += " "

        current_sentence += stripped_line

        if re.search(r'\.\s*$', stripped_line):
            sentence = current_sentence.strip()
            sentences.append(sentence)
            meta_info.append({
                "start_line": current_start_line,
                "end_line": i + 1,
                "text": sentence
            })
            current_sentence = ""

    # 最後の文（ピリオドで終わらない場合）
    if current_sentence:
        sentence = current_sentence.strip()
        sentences.append(sentence)
        meta_info.append({
            "start_line": current_start_line,
            "end_line": len(lines),
            "text": sentence
        })

    return meta_info


def main():
    parser = argparse.ArgumentParser(description="英語テキストをピリオド区切りで連結し、メタ情報付きで出力")
    parser.add_argument("--input", required=True, help="入力ファイルのパス（英語テキスト）")
    parser.add_argument("--output", required=True, help="出力ファイルのパス（JSON形式）")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    results = merge_lines_into_sentences_with_meta(lines)

    with open(args.output, "w", encoding="utf-8") as outfile:
        json.dump(results, outfile, indent=2, ensure_ascii=False)

    print(f"{len(results)} 文を {args.output} に出力しました。")


if __name__ == "__main__":
    main()
