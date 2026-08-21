import re
from odoo import models

class GlyphService(models.AbstractModel):
    _name = "glyph.service"
    _description = "Glyph Tag Normalization and Rendering Service"

    TAG_PATTERN = re.compile(
        r'\{(?:glyph:)?(?P<glyph>[A-Za-z0-9]+)'
        r'(?:\s+ucs=(?P<ucs>(?:U\+[0-9A-Fa-f]{4,6}(?:\s+U\+[0-9A-Fa-f]{4,6})*)))?'
        r'(?:\s+rep=(?P<rep>(?:U\+[0-9A-Fa-f]{4,6}(?:\s+U\+[0-9A-Fa-f]{4,6})*)))?'
        r'(?:\s+set=(?P<set>[A-Za-z0-9_+\-]+))?'
        r'\}'
    )

    ESCAPED = "{_LB_}"

    # ------------------------------------------------------------
    # エスケープ処理（解除しない）
    # ------------------------------------------------------------
    def escape(self, text):
        return text.replace("{{", self.ESCAPED)

    # ------------------------------------------------------------
    # Tag Completion（補完）
    # ------------------------------------------------------------
    def expand_all(self, text, glyph_set):
        text = self.escape(text)

        def _replace(m):
            glyph = m.group("glyph")
            entry = glyph_set.entry_ids.filtered(lambda e: e.name == glyph)
            if not entry:
                return m.group(0)
            return "{glyph:%s ucs=%s rep=%s set=%s}" % (
                glyph,
                entry.ucs,
                entry.rep,
                glyph_set.name,
            )

        # ★ エスケープ解除しない（{_LB_} を残す）
        return self.TAG_PATTERN.sub(_replace, text)

    # ------------------------------------------------------------
    # レンダリング（ucs / rep / auto）
    # ------------------------------------------------------------
    def render_text(self, text, mode="auto", glyph_set=None):
        expanded = self.expand_all(text, glyph_set)

        def _replace(m):
            ucs = m.group("ucs")
            rep = m.group("rep")
            return self._render_single(ucs, rep, mode)

        return self.TAG_PATTERN.sub(_replace, expanded)

    def _render_single(self, ucs, rep, mode):
        seq = None
        if mode == "ucs":
            seq = ucs or rep
        elif mode in ("rep", "reduce"):
            seq = rep or ucs
        else:
            seq = ucs or rep

        if not seq:
            return "□"

        return self._ucs_to_text(seq)

    def _ucs_to_text(self, seq):
        cps = re.findall(r"U\+([0-9A-Fa-f]{4,6})", seq)
        return "".join(chr(int(cp, 16)) for cp in cps)
