# from odoo import http


# class GlyphtagDemo(http.Controller):
#     @http.route('/glyphtag_demo/glyphtag_demo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/glyphtag_demo/glyphtag_demo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('glyphtag_demo.listing', {
#             'root': '/glyphtag_demo/glyphtag_demo',
#             'objects': http.request.env['glyphtag_demo.glyphtag_demo'].search([]),
#         })

#     @http.route('/glyphtag_demo/glyphtag_demo/objects/<model("glyphtag_demo.glyphtag_demo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('glyphtag_demo.object', {
#             'object': obj
#         })

