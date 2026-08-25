from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    """
    Configuration settings for joo_mjrengo module.
    Allows selecting the glyph set and the font used
    for glyph rendering in the system.
    """
    _inherit = 'res.config.settings'

    joo_set = fields.Selection(
        [
            ('mj', 'MJ'),
            ('mj_plus', 'MJ+'),
        ],
        string="Glyph Set",
        default="mj_plus",
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
            'joo_mjrengo.set',
            self.joo_set
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

        res.update(
            joo_set=conf.get_param('joo_mjrengo.set', 'mj_plus'),
            joo_font=conf.get_param('joo_mjrengo.font', 'dwpiexmincho'),
        )
        return res
