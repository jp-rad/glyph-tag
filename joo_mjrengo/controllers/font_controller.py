from odoo import http

class FontController(http.Controller):

    @http.route('/joo_mjrengo/font', type='json', auth='user')
    def get_font(self):
        return request.env['ir.config_parameter'].sudo().get_param('joo_mjrengo.font', 'ipamjm')
