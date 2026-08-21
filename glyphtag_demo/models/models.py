from odoo import models, fields, api

class GlyphDemo(models.Model):
    _name = 'glyphtag_demo.glyph_demo'
    _description = 'Glyph Tag Demo'

    name = fields.Char(string="Normalized Text")
    glyph_text = fields.Char(string="Glyph Tag Text")
    ucs_text = fields.Char(string="UCS Text")
    rep_text = fields.Char(string="Representative Text")

    glyph_set_id = fields.Many2one(
        "joo_mjrengo.glyph_set",
        string="Glyph Set",
        required=True,
    )

    @api.onchange("glyph_text", "glyph_set_id")
    def _onchange_glyph_text(self):
        if not self.glyph_text or not self.glyph_set_id:
            return

        service = self.env["glyph.service"]

        # 1. 正規化（補完）— エスケープ解除しない
        normalized = service.expand_all(self.glyph_text, self.glyph_set_id)
        self.name = normalized

        # 2. UCS レンダリング
        self.ucs_text = service.render_text(normalized, mode="ucs", glyph_set=self.glyph_set_id)

        # 3. rep レンダリング
        self.rep_text = service.render_text(normalized, mode="rep", glyph_set=self.glyph_set_id)

    # @api.model
    # def create(self, vals):
    #     rec = super().create(vals)
    #     rec._onchange_glyph_text()
    #     return rec

    # def write(self, vals):
    #     res = super().write(vals)
    #     self._onchange_glyph_text()
    #     return res
