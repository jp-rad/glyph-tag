from odoo import models
from mjrengo.builder import build_engine
from mjrengo.engine import GlyphTagEngine, GlyphResult

class GlyphService(models.AbstractModel):
    _name = "joo_mjrengo.glyph_service"
    _description = "Glyph Tag Normalization and Rendering Service"

    def _get_engine(self) -> GlyphTagEngine:
        conf = self.env['ir.config_parameter'].sudo()
        param_set=conf.get_param('joo_mjrengo.set', 'mj_plus'),

        if param_set and param_set[0] == 'mj_plus':
            engine = build_engine("mj_plus", "4.10")
        else:
            engine = build_engine("mj_plusx", "1.20")
        return engine

    def normalize_tags(self, text) -> GlyphResult:
        engine = self._get_engine()
        result = engine.normalize_tags(text)
        return result

    def render_text(self, text, use_base=False) -> str:
        engine = self._get_engine()

        result = engine.render_text(text, use_base=use_base)
        return result
