from odoo import models
import re

class GlyphService(models.AbstractModel):
    _name = "joo_mjrengo.glyph_service"
    _description = "Glyph Tag Normalization and Rendering Service"

    TAG_PATTERN = re.compile(
        r'\{(?P<glyph>[A-Za-z0-9]+)'
        r'(?:\s+ucs=(?P<ucs>(?:U\+[0-9A-Fa-f]{4,6}(?:\s+U\+[0-9A-Fa-f]{4,6})*)))?'
        r'(?:\s+rep=(?P<rep>(?:U\+[0-9A-Fa-f]{4,6}(?:\s+U\+[0-9A-Fa-f]{4,6})*)))?'
        r'(?:\s+set=(?P<set>[A-Za-z0-9_+\-]+))?'
        r'\}'
    )

    TAG_LB = "{_LB_}"
    ESCAPED_LB = "{_LB_ESCAPED_}"

    # ------------------------------------------------------------
    # "{{" を内部トークンに置換
    # ------------------------------------------------------------
    def escape(self, text):
        text = text or ""
        return text.replace("{{", self.ESCAPED_LB)

    def unescape(self, text):
        text = text or ""
        return text.replace(self.ESCAPED_LB, "{{")

    # ------------------------------------------------------------
    # 設定から GlyphSet を取得（レコード or False）
    # ------------------------------------------------------------
    def _get_default_glyph_set(self):
        param = self.env["ir.config_parameter"].sudo()
        glyph_set_id = int(param.get_param("joo_mjrengo.glyph_set_id", 0))
        if not glyph_set_id:
            return False
        rec = self.env["joo_mjrengo.glyph_set"].sudo().browse(glyph_set_id)
        return rec if rec.exists() else False

    # ------------------------------------------------------------
    # Tag 正規化（{MJ0001} → {MJ0001 ucs=... rep=... set=...}）
    # ------------------------------------------------------------
    def normalize_tags(self, text, glyph_set=False):
        # 1. エスケープ処理（"{{" → 内部トークン）
        text = self.escape(text)
        errors = []

        # 2. glyph_set が無効なら設定から取得
        if not glyph_set or not getattr(glyph_set, "exists", lambda: False)():
            glyph_set = self._get_default_glyph_set()

        # 3. 設定にも存在しない場合 → エラー
        if not glyph_set or not glyph_set.exists():
            return {
                "success": False,
                "text": text,
                "errors": ["GlyphSet が指定されていません（フィールドまたは Odoo 設定）。"],
            }

        # 4. 正規化処理
        def _replace(m):
            glyph = m.group("glyph")

            # 削除済み（active=False）のエントリ
            archived = glyph_set.entry_ids.with_context(active_test=False).filtered(
                lambda e: e.name == glyph and not e.active
            )
            if archived:
                errors.append(
                    f"図形名 '{glyph}' は GlyphSet '{glyph_set.name}' で削除されています（active=False）。"
                )
                return m.group(0)

            # active=True のエントリ
            entry = glyph_set.entry_ids.filtered(lambda e: e.name == glyph)
            if not entry:
                errors.append(
                    f"図形名 '{glyph}' が GlyphSet '{glyph_set.name}' に存在しません。"
                )
                return m.group(0)

            entry = entry[0]

            # 正規形
            return "{%s ucs=%s rep=%s set=%s}" % (
                glyph,
                entry.ucs,
                entry.rep,
                glyph_set.name,
            )

        result = self.TAG_PATTERN.sub(_replace, text)

        # 5. エスケープ解除
        result = self.unescape(result)

        return {
            "success": len(errors) == 0,
            "text": result,
            "errors": errors,
        }

    # ------------------------------------------------------------
    # レンダリング（use_rep=True → rep / False → ucs）
    # tofu は UCS コードポイント（例: "U+25A1"）
    # ------------------------------------------------------------
    def render_text(self, text, use_rep=False, glyph_set=False, tofu="U+25A1"):
        result = self.normalize_tags(text, glyph_set)
        if not result["success"]:
            return result

        expanded = result["text"]
        expanded = expanded.replace("{{", self.TAG_LB)

        def _replace(m):
            ucs = m.group("ucs")
            rep = m.group("rep")
            return self._render_single(ucs, rep, use_rep, tofu)

        rendered = self.TAG_PATTERN.sub(_replace, expanded)
        result["text"] = rendered.replace(self.TAG_LB, "{")
        return result

    # ------------------------------------------------------------
    # use_rep=True のときだけ rep、それ以外は ucs（既定）
    # ------------------------------------------------------------
    def _render_single(self, ucs, rep, use_rep, tofu):
        seq = rep if use_rep else ucs

        if not seq:
            return self._ucs_to_text(tofu)

        return self._ucs_to_text(seq)

    # ------------------------------------------------------------
    # "U+XXXX ..." → 実際の文字列へ変換
    # ------------------------------------------------------------
    def _ucs_to_text(self, seq):
        cps = re.findall(r"U\+([0-9A-Fa-f]{4,6})", seq)
        return "".join(chr(int(cp, 16)) for cp in cps)
