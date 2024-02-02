from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


class EstateOffer(models.Model):
    _name = "estate.offer"
    _description = "Property Offers"

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
    # Computed Fields
    date_deadline = fields.Date(compute="_compute_deadline_date", inverse="_inverse_deadline_date", string="Deadline (days)")

    # --------------------------------------- Compute Methods ----------------------------------

    @api.depends("create_date", "validity")
    def _compute_deadline_date(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = date + relativedelta(days=record.validity)
            
    def _inverse_deadline_date(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - date).days