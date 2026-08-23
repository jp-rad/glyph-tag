from odoo import models
import re

class GlyphService(models.AbstractModel):
    """
    Service for glyph tag normalization and rendering.

    Responsibilities:
    - Normalize short glyph tags such as {MJ0001} into the full form:
      {MJ0001 ucs=U+XXXX rep=U+YYYY set=mj_plus}
    - Render normalized tags into actual Unicode text using either
      UCS or representative codepoints.
    - Handle escaping of literal "{{" sequences inside text.
    """

    _name = "joo_mjrengo.glyph_service"
    _description = "Glyph Tag Normalization and Rendering Service"

    # Pattern for normalized glyph tags
    TAG_PATTERN = re.compile(
        r'\{(?P<glyph>[A-Za-z0-9]+)'
        r'(?:\s+ucs=(?P<ucs>(?:U\+[0-9A-Fa-f]{4,6}(?:\s+U\+[0-9A-Fa-f]{4,6})*)))?'
        r'(?:\s+rep=(?P<rep>(?:U\+[0-9A-Fa-f]{4,6}(?:\s+U\+[0-9A-Fa-f]{4,6})*)))?'
        r'(?:\s+set=(?P<set>[A-Za-z0-9_+\-]+))?'
        r'\}'
    )

    # Internal tokens for escaping literal "{{"
    TAG_LB = "{_LB_}"
    ESCAPED_LB = "{_LB_ESCAPED_}"

    # ------------------------------------------------------------
    # Escape literal "{{" to internal token (normalization phase)
    # ------------------------------------------------------------
    def escape(self, text):
        text = text or ""
        return text.replace("{{", self.ESCAPED_LB)

    # ------------------------------------------------------------
    # Unescape internal token back to "{{" (normalization phase)
    # ------------------------------------------------------------
    def unescape(self, text):
        text = text or ""
        return text.replace(self.ESCAPED_LB, "{{")

    # ------------------------------------------------------------
    # Rendering-specific brace protection
    # ------------------------------------------------------------
    def _render_protect_left_brace(self, text):
        """
        Replace literal '{{' with internal left-brace token.
        Used during rendering to avoid tag misinterpretation.
        """
        return (text or "").replace("{{", self.TAG_LB)

    def _render_restore_left_brace(self, text):
        """
        Restore internal left-brace token back to '{'.
        Used after rendering to produce final output text.
        """
        return (text or "").replace(self.TAG_LB, "{")

    # ------------------------------------------------------------
    # Retrieve default glyph set from system configuration
    # ------------------------------------------------------------
    def _get_default_glyph_set(self):
        param = self.env["ir.config_parameter"].sudo()
        glyph_set_id = int(param.get_param("joo_mjrengo.glyph_set_id", 0))
        if not glyph_set_id:
            return False

        rec = self.env["joo_mjrengo.glyph_set"].sudo().browse(glyph_set_id)
        return rec if rec.exists() else False

    # ------------------------------------------------------------
    # Normalize glyph tags: {MJ0001} → {MJ0001 ucs=... rep=... set=...}
    # ------------------------------------------------------------
    def normalize_tags(self, text, glyph_set=False):
        text = self.escape(text)
        errors = []

        # Resolve glyph set
        if not glyph_set or not getattr(glyph_set, "exists", lambda: False)():
            glyph_set = self._get_default_glyph_set()

        if not glyph_set or not glyph_set.exists():
            return {
                "success": False,
                "text": text,
                "errors": ["Glyph set is not specified (field or system configuration)."],
            }

        # Replacement logic
        def _replace(m):
            glyph = m.group("glyph")

            # Archived entry (active=False)
            archived = glyph_set.entry_ids.with_context(active_test=False).filtered(
                lambda e: e.name == glyph and not e.active
            )
            if archived:
                errors.append(
                    f"Glyph '{glyph}' is archived in glyph set '{glyph_set.name}'."
                )
                return m.group(0)

            # Active entry
            entry = glyph_set.entry_ids.filtered(lambda e: e.name == glyph)
            if not entry:
                errors.append(
                    f"Glyph '{glyph}' does not exist in glyph set '{glyph_set.name}'."
                )
                return m.group(0)

            entry = entry[0]

            # Normalized tag
            return "{%s ucs=%s rep=%s set=%s}" % (
                glyph,
                entry.ucs,
                entry.rep,
                glyph_set.name,
            )

        result = self.TAG_PATTERN.sub(_replace, text)
        result = self.unescape(result)

        return {
            "success": len(errors) == 0,
            "text": result,
            "errors": errors,
        }

    # ------------------------------------------------------------
    # Render normalized tags into actual Unicode text
    # use_rep=True → representative UCS
    # use_rep=False → original UCS (default)
    # tofu: fallback UCS codepoint (e.g., "U+25A1")
    # ------------------------------------------------------------
    def render_text(self, text, use_rep=False, glyph_set=False, tofu="U+25A1"):
        result = self.normalize_tags(text, glyph_set)
        if not result["success"]:
            return result

        expanded = self._render_protect_left_brace(result["text"])

        def _replace(m):
            ucs = m.group("ucs")
            rep = m.group("rep")
            return self._render_single(ucs, rep, use_rep, tofu)

        rendered = self.TAG_PATTERN.sub(_replace, expanded)
        result["text"] = self._render_restore_left_brace(rendered)
        return result

    # ------------------------------------------------------------
    # Select UCS or representative UCS based on use_rep flag
    # ------------------------------------------------------------
    def _render_single(self, ucs, rep, use_rep, tofu):
        seq = rep if use_rep else ucs
        if not seq:
            return self._ucs_to_text(tofu)
        return self._ucs_to_text(seq)

    # ------------------------------------------------------------
    # Convert "U+XXXX ..." into actual Unicode characters
    # ------------------------------------------------------------
    def _ucs_to_text(self, seq):
        """
        Convert a UCS codepoint sequence (e.g., "U+4E00 U+E0100") into
        an actual Unicode string.

        Processing steps:
        1. Extract all hexadecimal codepoints using a regular expression.
        - The pattern U+XXXX or U+XXXXX or U+XXXXXX is supported.
        - This covers BMP characters (U+0000-U+FFFF) and
            supplementary-plane characters (U+10000-U+10FFFF).

        2. For each extracted codepoint:
        - Convert the hexadecimal string into an integer.
        - Pass the integer to Python's built-in chr() function.
            chr() automatically handles:
            * BMP characters (1 code unit)
            * Supplementary characters (converted to surrogate pairs
                when encoded as UTF-16 internally)
            Therefore, no manual surrogate pair calculation is required.

        3. Join all resulting characters into a final Unicode string.

        Example:
            Input:  "U+4E00 U+E0100"
            Regex:  ["4E00", "E0100"]
            chr():  ["一", "\U000E0100"]
            Output: "一󠄀"

        This method is intentionally minimal and relies on Python's
        Unicode correctness rather than implementing UCS → UTF-16
        conversion manually.
        """
        cps = re.findall(r"U\+([0-9A-Fa-f]{4,6})", seq)
        return "".join(chr(int(cp, 16)) for cp in cps)
