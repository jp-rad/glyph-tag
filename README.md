# 📘 Glyph Tag Specification  
**Version:** 0.2.0  
**Status:** Complete  
**Author:** [jp-rad](https://github.com/jp-rad)  
**Last Updated:** 2026-08-20  


# 1. Purpose（目的）

Glyph Tag は、MJ/GJ などフォント固有の図形名（glyph name）を  
Unicode・IVS（異体字セレクタ）・fallback を伴って安全に扱うための  
**文字抽象化タグ形式**である。

本仕様は、以下の課題を体系的に扱う新しいレイヤーを提供する：

- 字形（フォント固有の形）  
- 字体（抽象的な構造）  
- Unicode 包摂  
- 異体字（IVS）  
- 文字同定  
- JSON / Web / RPC で安全に扱える表現形式  

さらに、  
**行政事務標準文字テクニカルレポート（デジタル庁）**  
および  
**行政事務標準文字ガイドライン**  
で示される「文字同定・包摂・異体字管理」の考え方を参照し、  
行政文書・住民情報・戸籍・地名などで求められる  
**正確な文字識別・異体字管理**に対応できるよう設計されている。

**地方公共団体情報システムにおける文字の標準化（公式URL）：**  
[https://www.digital.go.jp/policies/local_governments/character-specification](https://www.digital.go.jp/policies/local_governments/character-specification)

Glyph Tag の `u=` は **UCS（ISO/IEC 10646）に基づく Unicode コードポイント列**であり、  
`fb=` は **代替文字（fallback character）** として、  
u が表示できない環境でも文字情報を安全に保持・表示するために用いる。

さらに、Glyph Tag の `u=` と `fb=` の関係は、  
行政事務標準文字で定義される **縮退マップ（Reduction Map）** の  
「縮退前の文字 → 縮退後の代表文字」という構造と完全に一致する。


# 2. Syntax（構文）

Glyph Tag は **2つの表記形式**を許容する。

## 2.1 完全形式

```
{glyph:<図形名> [u=<UnicodeSeq>] [fb=<UnicodeSeq>] [set=<体系名>]}
```

## 2.2 省略形式

```
{<図形名> [u=<UnicodeSeq>] [fb=<UnicodeSeq>] [set=<体系名>]}
```

### ✔ glyph: は省略可能  
省略しても意味は完全に同じ。


## 2.3 UnicodeSeq（Unicode列）

`UnicodeSeq` は **JSON Unicode エスケープ（\uXXXX）を連結したもの**。

### BMP内文字  
```
\u4E00
```

### BMP外文字（絵文字など）  
UTF‑16 サロゲートペアで表現する：

```
\uD83D\uDE00   # 😀
```

### IVS（異体字セレクタ）  
基本文字 + セレクタ（VS17〜VS256）

例：U+4E00 + U+E0100 → UTF‑16 で

```
\u4E00\uD83C\uDC00
```

### 複数コードポイント  
```
\u4E00\u4E8C\u4E09
```


# 3. Attributes（属性）

| 属性 | 説明 |
|------|------|
| **glyph** | 図形名（MJ0001 / GJ0431 / EMOJI001 など）。省略形式ではタグ先頭の識別子が glyph 名となる。 |
| **u** | 本来の文字を表す UnicodeSeq（JSONエスケープ形式）。IVS を含むことがある。縮退マップの「縮退前の文字」に相当する。 |
| **fb** | **代替文字（fallback）**。u が表示できない環境で代わりに使用する UnicodeSeq。行政事務標準文字の「代替表記」および縮退マップの「縮退後の代表文字」に相当する。 |
| **set** | 字形体系（mj / gj / emoji / 他体系）。 |


# 4. Rendering rules（レンダリング仕様）

```
mode="u"     → u → fb → unknown
mode="fb"    → fb → u → unknown
mode="auto"  → u → fb → unknown（既定）
```

unknown は `"□"` など任意指定。


# 5. Tag completion（タグ補完）

Tag Completion は、  
**波括弧 `{}` 内の glyph タグを、glyph 変換テーブルを参照して完全なタグへ補完する処理**である。

補完対象：

- `{MJ0001}`
- `{glyph:MJ0001}`
- `{GJ0431 fb=\u9AD8}`
- `{glyph:GJ0431 fb=\u9AD8}`
- `{MJ0001 u=\u4E00 set=mj}`

補完対象外：

- `MJ0001`（タグ外の生 glyph 名）
- `GJ0431`（タグ外の生 glyph 名）


# 6. UnicodeSeq（JSONエスケープ）仕様

### 6.1 BMP  
```
\u4E00
```

### 6.2 BMP外（絵文字）  
```
\uD83D\uDE00
```

### 6.3 IVS  
```
\u4E00\uD83C\uDC00
```

### 6.4 複数コードポイント  
```
\u4E00\u4E8C\u4E09
```


# 7. Reference implementation（Python）  
Pythonによるリファレンス実装を示す。

```python
# -*- coding: utf-8 -*-
"""
Glyph Tag – Tag Completion & Rendering (Version 0.2.0)
"""

import re
import codecs

# ----------------------------------------------------------------------
# 1. Glyph table (example)
# ----------------------------------------------------------------------

GLYPH_TABLE = {
    "MJ0001": {
        "u":  r"\u4E00\uD83C\uDC00",  # U+4E00 + U+E0100 (IVS)
        "fb": r"\u4E00",
        "set": "mj",
    },
    "GJ0431": {
        "u":  r"\u9AD8\uD83C\uDC01",  # U+9AD8 + U+E0101 (IVS)
        "fb": r"\u9AD8",
        "set": "gj",
    },
    "EMOJI001": {
        "u":  r"\uD83D\uDE00",        # 😀
        "fb": r"\uD83D\uDE00",
        "set": "emoji",
    },
}

# ----------------------------------------------------------------------
# 2. Tag pattern (glyph: is optional)
# ----------------------------------------------------------------------

GLYPH_TAG_PATTERN = re.compile(
    r'\{(?:glyph:)?(?P<glyph>[A-Za-z0-9]+)'
    r'(?:\s+u=(?P<u>(?:\\u[0-9A-Fa-f]{4})+))?'
    r'(?:\s+fb=(?P<fb>(?:\\u[0-9A-Fa-f]{4})+))?'
    r'(?:\s+set=(?P<set>[A-Za-z0-9_]+))?'
    r'\}'
)

# ----------------------------------------------------------------------
# 3. Utilities
# ----------------------------------------------------------------------

def json_escape_to_text(s: str) -> str:
    if not s:
        return ""
    return codecs.decode(s, "unicode_escape")


def build_tag(glyph_name: str, info: dict) -> str:
    parts = [f"glyph:{glyph_name}"]
    if info.get("u"):
        parts.append(f"u={info['u']}")
    if info.get("fb"):
        parts.append(f"fb={info['fb']}")
    if info.get("set"):
        parts.append(f"set={info['set']}")
    return "{" + " ".join(parts) + "}"


# ----------------------------------------------------------------------
# 4. Tag completion
# ----------------------------------------------------------------------

def expand_tag(match: re.Match) -> str:
    glyph = match.group("glyph")
    info = GLYPH_TABLE.get(glyph)
    if not info:
        return match.group(0)
    return build_tag(glyph, info)


def expand_all(text: str) -> str:
    return GLYPH_TAG_PATTERN.sub(expand_tag, text)


# ----------------------------------------------------------------------
# 5. Parsing tags for rendering
# ----------------------------------------------------------------------

def parse_tag(match: re.Match) -> dict:
    return {
        "glyph": match.group("glyph"),
        "u": match.group("u"),
        "fb": match.group("fb"),
        "set": match.group("set"),
    }


# ----------------------------------------------------------------------
# 6. Rendering
# ----------------------------------------------------------------------

def render(parsed: dict, mode: str = "auto", unknown: str = "□") -> str:
    u = parsed.get("u")
    fb = parsed.get("fb")

    if mode == "u":
        if u:
            return json_escape_to_text(u)
        if fb:
            return json_escape_to_text(fb)
        return unknown

    if mode == "fb":
        if fb:
            return json_escape_to_text(fb)
        if u:
            return json_escape_to_text(u)
        return unknown

    if u:
        return json_escape_to_text(u)
    if fb:
        return json_escape_to_text(fb)
    return unknown


def render_text(text: str, mode: str = "auto", unknown: str = "□") -> str:
    def _replace(m: re.Match) -> str:
        parsed = parse_tag(m)
        return render(parsed, mode=mode, unknown=unknown)

    return GLYPH_TAG_PATTERN.sub(_replace, text)
```


# 8. Security（安全性）

- Glyph Tag は任意の文字列中に埋め込めるが、  
  HTML / JSON / URL などの外部形式に変換する際は  
  **レンダリング後の文字列を適切にエスケープすること**。
- Tag Completion は **タグ外の文字列を変更しない**。
- IVSは Unicode として安全に扱える。


# 9. Extensibility（拡張性）

- `set=` は任意体系を追加可能（mj / gj / koseki / emoji / etc）  
- `u=` と `fb=` は UnicodeSeq のため  
  **任意の Unicode / IVS / 絵文字 / CJK拡張**を扱える  
- 将来的に属性追加が可能  
  例：`src=`, `ver=`, `note=`


# 10. Examples（例）

```
{MJ0001}
{glyph:MJ0001}

{GJ0431 fb=\u9AD8}
{glyph:GJ0431 fb=\u9AD8}

{MJ0001 u=\u4E00\uD83C\uDC00 fb=\u4E00 set=mj}
{glyph:MJ0001 u=\u4E00\uD83C\uDC00 fb=\u4E00 set=mj}

{EMOJI001 u=\uD83D\uDE00 fb=\uD83D\uDE00 set=emoji}
```
