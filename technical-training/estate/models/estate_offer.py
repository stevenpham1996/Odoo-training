from odoo import fields, models


class EstateOffer(models.Model):
    _name = "estate.offer"
    _description = "Real Estate Offers"

    # --------------------------------------- Fields Declaration ----------------------------------

    price = fields.Float("Offered Price", required=True)
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
