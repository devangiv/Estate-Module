from odoo import models, fields, api


class Property(models.Model):
    _name = 'test.model'

    city = fields.Char(string="City")
    test_id = fields.Many2one('test.model', string="Test")
    test_ids = fields.One2many("estate.property", "parent_id", string="Tests")


class TestModel(models.Model):
    _name = 'estate.property'

    partner_id = fields.Many2one('res.partner', 'Contact')
    parent_id = fields.Many2one("test.model")


    @api.constrains('selling_price')
    def selling_price_check(self):
        for rec in self:
            if rec.selling_price <= 0:
                print("The selling price must be a positive value.")

    @api.depends('living_area', 'garden_area')
    def compute_area(self):
        for res in self:
            res.total_area = ( res.living_area +  res.garden_area )

    @api.onchange('garden')
    def onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0.0
            self.garden_orientation = False

    title = fields.Char(string="Title")
    description = fields.Text()
    contact = fields.Char(string="Contact")
    city = fields.Char()
    name = fields.Char(default="Unknown")
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    postcode = fields.Char(string="postcode")
    date_availability = fields.Date(string="Date availability", copy=False)
    expected_price = fields.Float(string="Expected price")
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    total_area = fields.Float(compute="compute_area", string="Total area", store=True)
    status = fields.Selection(
        string="Status", default='new',
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('cancelled', 'Cancelled')]
    )
    offer = fields.Char(string="Offer")
    price = fields.Float(string="Price",required=True)
    status_check = fields.Selection(
        string="Status check",
        selection=[('refused', 'Refused'), ('accepted', 'Accepted')]
    )
    other_Info = fields.Text(string="other_Info")
    state = fields.Selection(
        string="State", required=True,
        selection=[('new', 'New'), ('sold', 'Sold'), ('cancelled', 'Cancelled')]
    )
    sequence = fields.Integer('Sequence', help="Used to order stages. Lower is better.")
