from odoo import models
from mjrengo.engine import GlyphTagEngine, GlyphResult
from mjrengo.replace import make_replace_fn
from mjrengo.data.mj import glyph_table as glyph_table_mj
from mjrengo.data.mj_plus import glyph_table as glyph_table_mj_plus

class GlyphService(models.AbstractModel):
    _name = "joo_mjrengo.glyph_service"
    _description = "Glyph Tag Normalization and Rendering Service"

    def _get_engine(self) -> GlyphTagEngine:
        conf = self.env['ir.config_parameter'].sudo()
        set_name=conf.get_param('joo_mjrengo.set', 'mj_plus'),

        if set_name=='mj_plus':
            fn = make_replace_fn(glyph_table_mj_plus, set_name)
        else:
            fn = make_replace_fn(glyph_table_mj, set_name)
        
        return GlyphTagEngine(fn)

    def normalize_tags(self, text) -> GlyphResult:
        engine = self._get_engine()
        result = engine.normalize_tags(text)
        return result

    def render_text(self, text, use_rep=False) -> str:
        engine = self._get_engine()

        result = engine.render_text(text, use_rep=use_rep)
        return result
