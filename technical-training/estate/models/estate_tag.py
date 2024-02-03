from odoo import models, fields
from dateutil.relativedelta import relativedelta


class EstateTag(models.Model):
    _name = "estate.tag"
    _description = "Real Estate Tag"

    # --------------------------------------- Fields Declaration ----------------------------------

    name = fields.Char("Name", required=True)

    # SQL constraints
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The tag name must be unique"),
    ]
