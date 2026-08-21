from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    joo_font = fields.Selection([
        ('ipamjm', 'IPAmj Mincho'),
        ('dwpimincho', 'DWPI Mincho'),
        ('dwpiexmincho', 'DWPI Extended Mincho'),
    ], string="行政標準文字連合フォント")

    def set_values(self):
        super().set_values()
        self.env['ir.config_parameter'].set_param('joo_mjrengo.font', self.joo_font)

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update(
            joo_font=self.env['ir.config_parameter'].get_param('joo_mjrengo.font', 'ipamjm')
        )
        return res
