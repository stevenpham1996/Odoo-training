from odoo import fields, models, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class EstateOffer(models.Model):
    _name = "estate.offer"
    _description = "Property Offers"
    _order = "price desc"

    # --------------------------------------- Fields Declaration ----------------------------------

    price = fields.Float("Offered Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        default=False,
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    # Related Fields
    type_id = fields.Char("Type", related="property_id.type_id.name", store=True)
    # Computed Fields
    date_deadline = fields.Date(
        compute="_compute_deadline_date",
        inverse="_inverse_deadline_date",
        string="Deadline (days)",
    )
    # SQL constraints
    _sql_constraints = [
        (
            "check_offer_price",
            "CHECK(price > 0)",
            "The offer price must be greater than 0",
        ),
    ]

    # --------------------------------------- Compute Methods ----------------------------------

    @api.depends("create_date", "validity")
    def _compute_deadline_date(self):
        for record in self:
            date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.date_deadline = date + relativedelta(days=record.validity)

    def _inverse_deadline_date(self):
        for record in self:
            date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.validity = (record.date_deadline - date).days

    # --------------------------------------- Action Methods ----------------------------------

    def action_accept(self):
        if "accepted" in self.mapped("property_id.state"):
            raise UserError("The property is already sold")
        self.write(  # NOTE: write() only usable for fields within the developing model
            {"status": "accepted"}
        )
        return self.mapped("property_id").write(
            {
                "state": "offer_accepted",
                "selling_price": self.price,
                "buyer_id": self.partner_id,
            }
        )

    def action_refuse(self):
        for offer in self:
            if offer.status != "refused":
                offer.status = "refused"
                offer.property_id.selling_price = 0.0
                offer.property_id.buyer_id = False
