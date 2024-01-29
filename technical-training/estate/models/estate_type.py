from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstateType(models.Model):
    _name = "estate.type"
    _description = "Real Estate Type"

    def _default_date_availability(self):
        return (fields.Date.today() + relativedelta(months=3)).strftime("%Y-%m-%d")

    # --------------------------------------- Fields Declaration ----------------------------------

    name = fields.Char("Name", required=True)
    # type = fields.Char("Property Type", required=True)
    # postcode = fields.Char("Postcode")
    # date_availability = fields.Date(
    #     "Available From",
    #     default=lambda self: self._default_date_availability(),
    #     copy=False,
    # )
    # expected_price = fields.Float("Expected Price", required=True)
    # selling_price = fields.Float("Selling Price", copy=False, readonly=True)

    # --------------------------------------- Relational Fields ----------------------------------
    # partner
