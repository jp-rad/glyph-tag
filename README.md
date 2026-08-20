# 📘 Glyph Tag Specification  
**Version:** 0.1  
**Status:** Complete  
**Author:** [jp-rad](https://github.com/jp-rad)  
**Last Updated:** 2026-08-20  


# 1. Purpose（目的）

Glyph Tag は、MJ/GJ などフォント固有の図形名（glyph name）を  
Unicode と fallback を伴って安全に扱うための **文字抽象化タグ形式**である。

この仕様は、  
- 字形（フォント固有の形）  
- 字体（抽象的な構造）  
- Unicode 包摂  
- 文字同定  
を体系的に扱うための新しいレイヤーを提供する。


# 2. Syntax（構文）

```
{glyph:<図形名> [u=<Unicode>] [fb=<fallback>] [set=<体系名>]}
```


# 3. Attributes（属性）

| 属性 | 説明 |
|------|------|
| **glyph** | 図形名（MJ0001 / GJ0431 / 他体系） |
| **u** | Unicode コードポイント（例: `U+4E00`） |
| **fb** | fallback（Unicode または文字） |
| **set** | 字形体系（mj / gj / 他体系） |


# 4. Rendering Rules（レンダリング仕様）

## 4.1 モード

```
mode="u"     → u → fb → unknown
mode="fb"    → fb → u → unknown
mode="auto"  → u → fb → unknown（既定）
```

## 4.2 unknown（不明文字）

`unknown` はレンダリング関数の引数で指定する。  
例： `"□"`, `"?"`, `"�"` など。


# 5. Tag Completion（タグ補完）

Tag Completion は、  
**波括弧 `{}` 内に存在する glyph タグを、glyph 変換テーブルを参照して完全なタグへ補完する処理である。**

## 5.1 補完対象

| 種類 | 例 | 説明 |
|------|------|------|
| 不完全タグ | `{glyph:MJ0001}` | 属性なし |
| 部分タグ | `{glyph:GJ0431 fb=U+9AD8}` | 属性が不足 |
| 完全タグ | `{glyph:MJ0001 u=U+4E00 fb=U+4E00 set=mj}` | 再補完（正規化） |

## 5.2 補完対象外

- `MJ0001`（生の glyph 名）
- `GJ0431`（タグ外の glyph 名）

## 5.3 補完の目的

タグ内部の情報が不完全であっても、  
glyph 変換テーブルを基準に **u, fb, set を補完し、完全なタグへ置き換える。**

例：

入力：
```
これは {glyph:MJ0001} と {glyph:GJ0431} のテスト。
```

出力：
```
これは {glyph:MJ0001 u=U+4E00 fb=U+4E00 set=mj}
と {glyph:GJ0431 fb=U+9AD8 set=gj} のテスト。
```


# 6. Reference Implementation (Python)  

Pythonでの実装例を示す。

## 6.1 Tag Completion（タグ補完）

```python
import re

# glyph変換テーブル（例）
GLYPH_TABLE = {
    "MJ0001": {"u": "U+4E00", "fb": "U+4E00", "set": "mj"},
    "GJ0431": {"u": None,     "fb": "U+9AD8", "set": "gj"},
}

# {glyph:...} のタグだけを対象とする
GLYPH_TAG_PATTERN = re.compile(
    r'\{glyph:(?P<glyph>[A-Za-z0-9]+)'
    r'(?:\s+u=(?P<u>U\+[0-9A-F]+))?'
    r'(?:\s+fb=(?P<fb>[^}]+))?'
    r'(?:\s+set=(?P<set>[A-Za-z0-9_]+))?'
    r'\}'
)

def build_tag(glyph_name, info):
    """変換テーブルから完全タグを構築する"""
    parts = [f"glyph:{glyph_name}"]

    if info.get("u"):
        parts.append(f"u={info['u']}")
    if info.get("fb"):
        parts.append(f"fb={info['fb']}")
    if info.get("set"):
        parts.append(f"set={info['set']}")

    return "{" + " ".join(parts) + "}"

def expand_tag(match):
    """不完全タグを完全タグに補完する"""
    glyph = match.group("glyph")
    info = GLYPH_TABLE.get(glyph)

    if not info:
        return match.group(0)  # テーブルにない → そのまま返す

    return build_tag(glyph, info)

def expand_all(text):
    """{} 内のタグだけを完全タグに補完する"""
    return GLYPH_TAG_PATTERN.sub(expand_tag, text)
```

## 6.2 Rendering（文字化）

```python
def unicode_to_char(u):
    if not u or not u.startswith("U+"):
        return u
    return chr(int(u[2:], 16))

def render(parsed, mode="auto", unknown="□"):
    """
    mode="u"    → u → fb → unknown
    mode="fb"   → fb → u → unknown
    mode="auto" → u → fb → unknown
    """
    u = parsed.get("u")
    fb = parsed.get("fb")

    if mode == "u":
        if u:
            return unicode_to_char(u)
        if fb:
            return unicode_to_char(fb)
        return unknown

    if mode == "fb":
        if fb:
            return unicode_to_char(fb)
        if u:
            return unicode_to_char(u)
        return unknown

    # auto
    if u:
        return unicode_to_char(u)
    if fb:
        return unicode_to_char(fb)
    return unknown
```

# 7. License（ライセンス）

MIT License

# 8. 参考

https://www.digital.go.jp/policies/local_governments/character-specification#document

[文字包括ガイドライン](https://www.digital.go.jp/assets/contents/node/basic_page/field_ref_resources/f3a1de20-1f15-44fd-ade8-4e0e9eb52e8b/4bce446b/20250718_policies_local_governments_specification_guideline_01.pdf)
