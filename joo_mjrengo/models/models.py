# from odoo import models, fields, api


# class joo_mjrengo(models.Model):
#     _name = 'joo_mjrengo.joo_mjrengo'
#     _description = 'joo_mjrengo.joo_mjrengo'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

