from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    """
    Configuration settings for joo_mjrengo module.
    Allows selecting the glyph set and the font used
    for glyph rendering in the system.
    """
    _inherit = 'res.config.settings'

    joo_glyph_set_id = fields.Many2one(
        "joo_mjrengo.glyph_set",
        string="Glyph Set",
        help="Select the glyph set used for glyph tag normalization."
    )

    joo_font = fields.Selection(
        [
            ('ipamjm', 'IPAmj Mincho'),
            ('dwpimincho', 'DWPI Mincho'),
            ('dwpiexmincho', 'DWPI Extended Mincho'),
        ],
        string="Glyph Font",
        default="dwpiexmincho",
        help="Select the font used for glyph rendering."
    )

    # ------------------------------------------------------------
    # Save configuration values
    # ------------------------------------------------------------
    def set_values(self):
        super().set_values()
        conf = self.env['ir.config_parameter']

        conf.set_param(
            'joo_mjrengo.glyph_set_id',
            self.joo_glyph_set_id.id or False
        )
        conf.set_param(
            'joo_mjrengo.font',
            self.joo_font
        )

    # ------------------------------------------------------------
    # Load configuration values
    # ------------------------------------------------------------
    @api.model
    def get_values(self):
        res = super().get_values()
        conf = self.env['ir.config_parameter'].sudo()

        glyph_set_id = int(conf.get_param('joo_mjrengo.glyph_set_id', 0))
        glyph_set = self.env['joo_mjrengo.glyph_set'].sudo().browse(glyph_set_id)
        if not glyph_set.exists():
            glyph_set = False

        res.update(
            joo_glyph_set_id=glyph_set,
            joo_font=conf.get_param('joo_mjrengo.font', 'ipamjm'),
        )
        return res
