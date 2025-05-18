# 🎥 Subtitle Translation Pipeline – ASS字幕英日翻訳ツール集

このプロジェクトは、ASS形式の英語字幕ファイル（.ass）を自然な日本語字幕に変換するためのステップバイステップのツール群です。

## 🔍 概要

YouTubeなどの動画に付属する字幕ファイル（ASS形式）を対象に、次の処理を順に行います：

1. **英語字幕の抽出**（`scripts/extract_ass_text.py`）
2. **文の結合・整形**（`scripts/merge_sentences.py`）
3. **日本語への翻訳と自然な文分割**（`scripts/translate_en_to_ja_json.py`）
4. **ASSファイル内の字幕置換**（`scripts/ass_replace_with_translation.py`）

また、本ツールは [YouTube Subtitle Pipeline](http://github.com/ty70/youtube-subtitle-pipeline.git) を使って英語の音声文字起こしから `.ass` 字幕ファイル（例：`input/input.ass`）を作成した後の後処理ツール群としても活用できます。

---

## ♻️ 使用例

```bash
# ステップ1: ASS字幕ファイルから英語テキストを抽出
python scripts/extract_ass_text.py --input input/input.ass --output extracted_en.txt

# ステップ2: 文を自然な区切りでマージして翻訳しやすい形に整形
python scripts/merge_sentences.py --input extracted_en.txt --output merged_en.json

# ステップ3: 翻訳と自然な日本語への分割結果をJSON形式で出力
python scripts/translate_en_to_ja_json.py --input merged_en.json --output output.json

# ステップ4: ASS字幕内の英語テキストを日本語字幕で置換（モード指定可能）
python scripts/ass_replace_with_translation.py --input input/input.ass --json output.json --output modified_output.ass --mode replace
```

---

## 🔧 各スクリプトの説明

### `extract_ass_text.py`（完成度：✅ OK）
ASSファイルの [Events] セクションから15行直前以降の `Text` 部分を抽出し、プレーンな英語テキストとして出力します。

### `merge_sentences.py`（完成度：⚠️ ピリオドで整形されるが、翻訳時にやや不自然）
複数の字幕にまたがる文を一つにまとめ、句点（ピリオド）で整形することで、翻訳の質を高めます。

### `translate_en_to_ja_json.py`（完成度：⚠️ 英訳も微妙（これは文だけで翻訳しているので、ある程度仕方ない）しっかり行数に日本語を分けてくれない，改善する必要あり）
Deep Translatorなどを使って英語文を日本語に翻訳し、対応する行数に応じて自然に分割します。`output.json` 形式で保存します。

### `ass_replace_with_translation.py`（完成度：✅ OK）
元の `.ass` ファイルを読み取り、JSONファイルに基づいて英語のセリフを日本語に置換した字幕ファイルまたは日英両方の字幕を生成します。

🆕 オプション機能：日英両字幕対応（日本語上、英語下）

--mode オプションに dual を指定することで、英語字幕の下に翻訳された日本語字幕を追加できます。
---

## 🧽 処理フロー図

```
input/input.ass
      ↓
scripts/extract_ass_text.py
      ↓
extracted_en.txt
      ↓
scripts/merge_sentences.py
      ↓
merged_en.txt
      ↓
scripts/translate_en_to_ja_json.py
      ↓
output.json
      ↓
scripts/ass_replace_with_translation.py
      ↓
modified_output.ass
```

---

## 🚀 必要なライブラリ

```bash
pip install deep-translator
```

---

## 🌍 ライセンス

MIT [License](./LICENSE) を適用しています。

---

## 🙇‍♂️ 貢献

バグ報告や機能改善リクエスト、プルリク大歓迎です！

