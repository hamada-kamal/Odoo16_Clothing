from odoo import api, fields, models


class Wiz(models.TransientModel):
    _name = 'wiz.wiz'
    _description = "Nike Wizard"

    product_id = fields.Many2one(
        comodel_name='nike.product',
        string='Product',
        required=True)

    name = fields.Char()
    price = fields.Char()

    @api.onchange('product_id')
    def get_product_data(self):
        product = self.env['nike.product'].browse(self.product_id.id)
        self.name = product.name
        self.price = product.price
