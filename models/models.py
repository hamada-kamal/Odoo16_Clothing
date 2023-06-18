from odoo import models, fields, api


class employee(models.Model):
    _name = 'nike.employee'
    _description = "Employees Records"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    phone = fields.Char(string="Phone", size=11)
    photo = fields.Binary(string="Photo")
    salary = fields.Float(string="Salary")
    address = fields.Char()


class client(models.Model):
    _name = 'nike.client'
    _description = "Clients Records"
    _rec_name = "name"

    name = fields.Char()
    address = fields.Char()
    phone = fields.Char(size=11)


class product(models.Model):
    _name = 'nike.product'
    _description = "Products Records"
    _rec_name = "name"

    name = fields.Char()
    price = fields.Float()





class product_line(models.Model):
    _name = 'nike.product_line'
    _description = "Product Line"
    _rec_name = "name"

    @api.onchange("name","qty")
    def update_sub_total(self):
        for line in self:
            line.sub_total=line.qty * line.name.price

    @api.onchange('name')   ##change price when the product change
    def update_price(self):
        for line in self:
            line.product_price = line.name.price

    # @api.onchange('name','qty')
    # def update_sub_total(self):
    #     if self.name:
    #         print("self: ",self.name.price)
    #         self.sub_total = self.name.price * self.qty

    # @api.onchange('qty')
    # def update_sub_total2(self):
    #     if self.name:
    #         self.sub_total = self.name.price * self.qty

    name = fields.Many2one('nike.product', string="Product", required=True)
    qty = fields.Integer(string="Quantity", required=True, default=1)
    order_id = fields.Many2one('nike.order', string='Order Owner', invisible=True)
    product_price = fields.Float(compute="update_price", help='This filed is read only.')
    sub_total = fields.Float(compute="update_sub_total", help='This filed is read only.')



class order(models.Model):
    _name = 'nike.order'
    _description = "Orders Records"
    _rec_name = 'order_owner'
    @api.onchange('line')
    def calc_order_price(self):
        # if self.line:             #self.line >>>> the lines of this order
        #     t=0.0
        #     for l in self.line:
        #         # print(l.name.name)
        #         t+=l.name.price*l.qty
        #     self.total=t
        for order in self:
            order.total = sum(l.sub_total for l in order.line)
            print("this is self: ",order.total)
    order_maker = fields.Many2one(comodel_name="nike.employee", string="Employee", required=True)
    order_owner = fields.Many2one(comodel_name="nike.client", string="Client", required=True)
    line = fields.One2many("nike.product_line", 'order_id', required=True)
    order_date = fields.Date(string='Order Date', required=True)
    total = fields.Float(compute="calc_order_price")