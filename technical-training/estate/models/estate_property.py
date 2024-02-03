from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero, float_compare
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

    # SQL constraints
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must be greater than 0",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price > 0)",
            "The selling price must be greater than 0",
        ),
    ]

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
    offer_ids = fields.One2many("estate.offer", "property_id", string="Offers")

    # --------------------------------------- Calculated Fields ----------------------------------

    total_area = fields.Float(compute="_compute_total_area", string="Total Area")
    best_price = fields.Float(compute="_compute_best_price", string="Best Price")

    # --------------------------------------- Compute Methods ----------------------------------

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = record.expected_price

    # --------------------------------------- Onchange Methods ----------------------------------
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "N"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # --------------------------------------- Action Methods ----------------------------------

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("A canceled property can not be sold.")
            return record.write({"state": "sold"})

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property can not be canceled.")
            return record.write({"state": "canceled"})


# ----------------------------------------- constraint methods ----------------------------------


@api.constrains("expected_price", "selling_price")
def _check_selling_price(self):
    for record in self:
        if (
            not float_is_zero(record.selling_price, precision_rounding=0.01)
            and float_compare(
                record.selling_price,
                record.expected_price * 90.0 / 100.0,
                precision_rounding=0.01,
            )
            < 0
        ):
            raise ValidationError(
                "The selling price must be greater than the expected price."
            )
