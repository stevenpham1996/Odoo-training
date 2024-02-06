from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


class EstateType(models.Model):
    _name = "estate.type"
    _description = "Real Estate Type"
    _order = "name desc"

    def _default_date_availability(self):
        return (fields.Date.today() + relativedelta(months=3)).strftime("%Y-%m-%d")

    # --------------------------------------- Fields Declaration ----------------------------------

    name = fields.Char("Name", required=True)
    sequence = fields.Integer(
        "Sequence", default=2, help="Used to order stages. Lower is better."
    )
    property_ids = fields.One2many("estate.property", "type_id", string="Properties")
    offer_ids = fields.Many2many("estate.offer", string="Offers", compute="_compute_offer_count")
    offer_count = fields.Integer(compute="_compute_offer_count", string="Num Offers")

    # SQL constraints
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The tag name must be unique"),
    ]

    # --------------------------------------- Relational Fields ----------------------------------
    # partner

    # --------------------------------------- Compute Methods ----------------------------------

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        data = self.env["estate.offer"].read_group(
            [("property_id.state", "!=", "canceled"), ("type_id", "!=", False)],
            ["ids:array_agg(id)", "type_id"],
            ["type_id"],
        )
        mapped_count = {d["type_id"][0]: d["type_id_count"] for d in data}
        mapped_ids = {d["type_id"][0]: d["ids"] for d in data}
        for prop_type in self:
            prop_type.offer_count = mapped_count.get(prop_type.id, 0)
            prop_type.offer_ids = mapped_ids.get(prop_type.id, [])

    # --------------------------------------- Action Methods ----------------------------------
    # def action_view_offers(self):
    #     res = self.env.ref("estate.estate_property_offer_action").read()[0]
    #     res["domain"] = [("id", "in", self.offer_ids.ids)]
    #     return res
