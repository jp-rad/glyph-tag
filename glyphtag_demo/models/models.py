from odoo import models, fields

class GlyphDemo(models.Model):
    _name = 'glyphtag_demo.glyph_demo'
    _description = 'Glyph Tag Demo'

    name = fields.Char(string="Title")
    glyph_text = fields.Char(string="Glyph Tag Text")
