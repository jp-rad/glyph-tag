from odoo import models, fields, api
from odoo.exceptions import ValidationError

class GlyphDemo(models.Model):
    _name = 'glyphtag_demo.glyph_demo'
    _description = 'Glyph Tag Demo'

    name = fields.Char(string='Name')
    glyph_text = fields.Char(string="Glyph Tag Text")
    normalized_text = fields.Char(string="Normalized Text")
    ucs_text = fields.Char(string="UCS Text")
    rep_text = fields.Char(string="Representative Text")

    glyph_set_id = fields.Many2one(
        "joo_mjrengo.glyph_set",
        string="Glyph Set",
        required=False,
    )

    # ------------------------------------------------------------
    # バリデーション（glyph_text に対して）
    # ------------------------------------------------------------
    @api.constrains("glyph_text", "glyph_set_id")
    def _check_glyph_text(self):
        for rec in self:
            if not rec.glyph_text:
                continue

            service = rec.env["joo_mjrengo.glyph_service"].sudo()

            # ★ glyph_set_id が None → GlyphService が設定から取得する
            result = service.normalize_tags(rec.glyph_text, rec.glyph_set_id)

            if not result["success"]:
                raise ValidationError("\n".join(result["errors"]))

    # ------------------------------------------------------------
    # onchange（例外を出さない）
    # ------------------------------------------------------------
    @api.onchange("glyph_text", "glyph_set_id")
    def _onchange_glyph_text(self):

        service = self.env["joo_mjrengo.glyph_service"].sudo()

        # ★ glyph_set_id が None → GlyphService が設定から取得する
        result = service.normalize_tags(self.glyph_text, self.glyph_set_id)
        if not result["success"]:
            return

        normalized = result["text"]
        self.normalized_text = normalized

        # UCS レンダリング
        ucs_result = service.render_text(normalized, use_rep=False, glyph_set=self.glyph_set_id)
        self.ucs_text = ucs_result["text"] if ucs_result["success"] else False

        # rep レンダリング
        rep_result = service.render_text(normalized, use_rep=True, glyph_set=self.glyph_set_id)
        self.rep_text = rep_result["text"] if rep_result["success"] else False
