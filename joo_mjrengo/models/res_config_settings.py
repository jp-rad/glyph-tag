from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    joo_glyph_set_id = fields.Many2one(
        "joo_mjrengo.glyph_set",
        string="GlyphSet（字形体系）"
    )

    joo_font = fields.Selection([
            ('ipamjm', 'IPAmj Mincho'),
            ('dwpimincho', 'DWPI Mincho'),
            ('dwpiexmincho', 'DWPI Extended Mincho'),
        ],
        string="Joo Font（MJフォント）",
        default="dwpiexmincho",
    )

    def set_values(self):
        super().set_values()
        conf = self.env['ir.config_parameter']
        conf.set_param('joo_mjrengo.glyph_set_id', self.joo_glyph_set_id.id or False)
        conf.set_param('joo_mjrengo.font', self.joo_font)

    @api.model
    def get_values(self):
        res = super().get_values()
        conf = self.env['ir.config_parameter'].sudo()

    
        glyph_set_id = int(conf.get_param('joo_mjrengo.glyph_set_id', 0))
        glyph_set = self.env['joo_mjrengo.glyph_set'].sudo().browse(glyph_set_id) or False

        res.update(
            joo_glyph_set_id=glyph_set,
            joo_font=conf.get_param('joo_mjrengo.font', 'ipamjm'),
        )
        return res
