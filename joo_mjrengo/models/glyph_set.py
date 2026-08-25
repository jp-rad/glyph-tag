from odoo import models, fields, api

class GlyphSet(models.Model):
    """
    Represents a glyph set used for glyph tag normalization.
    Each glyph set contains multiple glyph entries that define
    UCS values, representative characters, and related metadata.
    """
    _name = "joo_mjrengo.glyph_set"
    _description = "Glyph Set"
    _order = "name, id"

    name = fields.Char(
        required=True,
        string="Name",
        help="Identifier of the glyph set (e.g., 'mj_plus')."
    )

    version = fields.Char(
        string="Version",
        help="Version string of the glyph set."
    )

    description = fields.Char(
        string="Description",
        help="Short description of the glyph set."
    )

    entry_ids = fields.One2many(
        "joo_mjrengo.glyph_entry",
        "set_id",
        string="Glyph Entries",
        help="List of glyph entries belonging to this glyph set."
    )
