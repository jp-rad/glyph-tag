# from odoo import http


# class Glyphtag(http.Controller):
#     @http.route('/glyphtag/glyphtag', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/glyphtag/glyphtag/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('glyphtag.listing', {
#             'root': '/glyphtag/glyphtag',
#             'objects': http.request.env['glyphtag.glyphtag'].search([]),
#         })

#     @http.route('/glyphtag/glyphtag/objects/<model("glyphtag.glyphtag"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('glyphtag.object', {
#             'object': obj
#         })

