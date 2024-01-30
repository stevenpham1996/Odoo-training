from odoo import models, fields
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    # --------------------------------------- Default Methods ----------------------------------

    def _default_date_availability(self):
        return (fields.Date.today() + relativedelta(months=3)).strftime("%Y-%m-%d")

    # --------------------------------------- Fields Declaration ----------------------------------

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Available From",
        default=lambda self: self._default_date_availability(),
        copy=False,
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", copy=False, readonly=True)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("N", "North"),
            ("S", "South"),
            ("E", "East"),
            ("W", "West"),
        ],
        string="Garden Orientation",
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )

    # --------------------------------------- Relational Fields ----------------------------------
    type_id = fields.Many2one(
        "estate.type", string="Property Type", ondelete="set null", index=True
    )
    buyer_id = fields.Many2one(
        "res.partner", string="Buyer", ondelete="set null", default="Odoo"
    )
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        copy=False,
        ondelete="set null",
        index=True,
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many("estate.tag", string="Tags", index=True)
    offer_ids = fields.One2many(
        "estate.offer", "property_id", string="Offers"
    )
