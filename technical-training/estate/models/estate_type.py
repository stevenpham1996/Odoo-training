from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstateType(models.Model):
    _name = "estate.type"
    _description = "Real Estate Type"

    def _default_date_availability(self):
        return (fields.Date.today() + relativedelta(months=3)).strftime("%Y-%m-%d")

    # --------------------------------------- Fields Declaration ----------------------------------

    name = fields.Char("Name", required=True)
    # SQL constraints
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The tag name must be unique"),
    ]
    
    # --------------------------------------- Relational Fields ----------------------------------
    # partner
