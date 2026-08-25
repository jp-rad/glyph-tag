from odoo import models
import re
from mjrengo.engine import GlyphTagEngine
from mjrengo.replace import make_replace_fn
from mjrengo.data.mj import glyph_table

class MjrengoService(models.AbstractModel):
    _name = "joo_mjrengo.mjrengo_service"
    _description = "Mjrengo Tag Normalization and Rendering Service"

    def normalize_tags(self, text, glyph_set=False):
        engine = GlyphTagEngine()
        fn = make_replace_fn(glyph_table)
        result = engine.normalize_tags(text, fn)
        return result

    def render_text(self, text, use_rep=False, glyph_set=False, tofu="U+25A1"):
        engine = GlyphTagEngine()
        fn = make_replace_fn(glyph_table)

        result = engine.render_text(text, fn, use_rep=use_rep, tofu=tofu)
        return result
