from odoo import models, fields, api

class GlyphSet(models.Model):
    _name = "joo_mjrengo.glyph_set"
    _description = "Glyph System"
    _order = "name, id"

    name = fields.Char(required=True)        # 例: "mj+"
    version = fields.Char()
    description = fields.Char()

    entry_ids = fields.One2many("joo_mjrengo.glyph_entry", "set_id")
