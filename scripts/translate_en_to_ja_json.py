#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
英語文（行番号付きJSON形式）を翻訳し、
元の英語行数に応じて日本語文を自然な箇所で分割してJSON出力するスクリプト。

使用方法:
    python translate_en_to_ja_json.py --input input.json --output output.json
"""

import argparse
import json
import re
from deep_translator import GoogleTranslator


def natural_split(text, line_count):
    """
    日本語の文を、行数に合わせて自然に分割する（句点、読点、長さに応じて）。
    """
    clauses = re.split(r'(?<=[。．！？!?])|(?<=[、,])', text)
    clauses = [clause.strip() for clause in clauses if clause.strip()]

    if len(clauses) <= line_count:
        while len(clauses) < line_count:
            clauses.append('')
        return clauses

    total_length = sum(len(c) for c in clauses)
    avg_length = total_length // line_count

    result = []
    current = ""

    for clause in clauses:
        if len(result) < line_count - 1:
            current += clause
            if len(current) >= avg_length or clause.endswith(("。", "．", "!", "？", "?")):
                result.append(current.strip())
                current = ""
        else:
            current += clause
    if current:
        result.append(current.strip())

    while len(result) < line_count:
        result.append("")
    while len(result) > line_count:
        result[-2] += result[-1]
        result.pop()

    return result


def translate_entries(entries):
    translator = GoogleTranslator(source="en", target="ja")
    translated_blocks = []

    for entry in entries:
        start = entry.get("start_line")
        end = entry.get("end_line")
        line_count = end - start + 1
        text = entry.get("text", "").strip()

        try:
            translated = translator.translate(text)
        except Exception as e:
            translated = f"[翻訳エラー]: {str(e)}"

        split_lines = natural_split(translated, line_count)

        translated_blocks.append({
            "start_line": start,
            "end_line": end,
            "ja": split_lines
        })

    return translated_blocks


def main():
    parser = argparse.ArgumentParser(description="翻訳して自然に分割した結果をJSON出力")
    parser.add_argument("--input", required=True, help="入力ファイル（JSON形式）")
    parser.add_argument("--output", required=True, help="出力ファイル（JSON形式）")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as infile:
        entries = json.load(infile)

    translated_blocks = translate_entries(entries)

    with open(args.output, "w", encoding="utf-8") as outfile:
        json.dump(translated_blocks, outfile, ensure_ascii=False, indent=2)

    print(f"{len(translated_blocks)}個のエントリを翻訳し {args.output} に保存しました。")


if __name__ == "__main__":
    main()
