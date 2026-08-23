from odoo import models, fields, api

class GlyphEntry(models.Model):
    """
    Represents a single glyph entry inside a glyph set.
    Each entry defines the UCS sequence, representative character,
    and metadata required for glyph tag normalization and rendering.
    """
    _name = "joo_mjrengo.glyph_entry"
    _description = "Glyph Entry"
    _order = "name, id"

    active = fields.Boolean(
        default=True,
        string="Active",
        help="If unchecked, this glyph entry is archived and will not be used."
    )

    name = fields.Char(
        required=True,
        string="Glyph Name",
        help="Identifier of the glyph entry (e.g., 'MJ0001')."
    )

    ucs = fields.Char(
        required=True,
        string="UCS Sequence",
        help="UCS codepoints for this glyph (e.g., 'U+4E00 U+E0100')."
    )

    rep = fields.Char(
        required=True,
        string="Representative UCS",
        help="Representative UCS codepoint (e.g., 'U+4E00')."
    )

    set_id = fields.Many2one(
        "joo_mjrengo.glyph_set",
        required=True,
        string="Glyph Set",
        ondelete="cascade",
        help="Glyph set to which this entry belongs."
    )
