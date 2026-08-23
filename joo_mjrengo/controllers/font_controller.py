from odoo import http
from odoo.http import request

class FontController(http.Controller):
    """
    Controller for retrieving the configured font used by the joo_mjrengo module.
    This endpoint is called by font_loader.js to dynamically apply the font
    to elements using the 'joo-font' CSS class.
    """

    @http.route('/joo_mjrengo/font', type='json', auth='user')
    def get_font(self):
        """
        Return the configured font key stored in ir.config_parameter.
        Only authenticated users can access this value because it is part
        of system configuration.
        """
        return request.env['ir.config_parameter'].sudo().get_param(
            'joo_mjrengo.font',
            'dwpiexmincho'  # default font (consistent with settings model)
        )
