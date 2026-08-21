from odoo import models, fields, api

class GlyphEntry(models.Model):
    _name = "joo_mjrengo.glyph_entry"
    _description = "Glyph Entry"
    _order = "name, set_id, id"

    name = fields.Char(required=True)        # 例: "MJ0001"
    ucs = fields.Char(required=True)         # "U+4E00 U+E0100"
    rep = fields.Char(required=True)         # "U+4E00"
    set_id = fields.Many2one("joo_mjrengo.glyph_set", required=True)
