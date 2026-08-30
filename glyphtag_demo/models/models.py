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

    # ------------------------------------------------------------
    # バリデーション（glyph_text に対して）
    # ------------------------------------------------------------
    @api.constrains("glyph_text", "glyph_set_id")
    def _check_glyph_text(self):
        for rec in self:
            if not rec.glyph_text:
                continue

            service = self.env["joo_mjrengo.glyph_service"].sudo()
            result = service.normalize_tags(rec.glyph_text)

            if not result.success:
                msg = "\n".join(err.message for err in result.errors) if result.errors else "Unknown error"
                raise ValidationError(msg)

    # ------------------------------------------------------------
    # onchange（例外を出さない）
    # ------------------------------------------------------------
    @api.onchange("glyph_text", "glyph_set_id")
    def _onchange_glyph_text(self):

        service = self.env["joo_mjrengo.glyph_service"].sudo()
        result = service.normalize_tags(self.glyph_text)

        if not result.success:
            return

        normalized = result.text
        
        self.normalized_text = normalized
        self.ucs_text = service.render_text(normalized)
        self.rep_text = service.render_text(normalized, use_base=True)
