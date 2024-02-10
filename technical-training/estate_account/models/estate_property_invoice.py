from odoo import models, Command


class PropertyInvoice(models.Model):

    _inherit = "estate.property"

    def action_sold(self):
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        for prop in self:
            self.env["account.move"].create(
                {
                    "partner_id": prop.buyer_id.id,
                    "move_type": "out_invoice",
                    "journal_id": journal.id,
                    "invoice_line_ids": [
                        Command.create({
                            "name": prop.name,
                            "quantity": 1.0,
                            "price_unit": prop.selling_price * 6.0 / 100.0,
                    }),
                        Command.create({
                            "name": prop.name,
                            "quantity": 1.0,
                            "price_unit": 100.00,
                    }),
                ],
            }
        )
        return super().action_sold()
