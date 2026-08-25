# from odoo import http


# class JooMjrengo(http.Controller):
#     @http.route('/joo_mjrengo/joo_mjrengo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/joo_mjrengo/joo_mjrengo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('joo_mjrengo.listing', {
#             'root': '/joo_mjrengo/joo_mjrengo',
#             'objects': http.request.env['joo_mjrengo.joo_mjrengo'].search([]),
#         })

#     @http.route('/joo_mjrengo/joo_mjrengo/objects/<model("joo_mjrengo.joo_mjrengo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('joo_mjrengo.object', {
#             'object': obj
#         })

