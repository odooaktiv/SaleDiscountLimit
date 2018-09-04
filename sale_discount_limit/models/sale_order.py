# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full copyright
# and licensing details.

from odoo import api, models, _
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    """Check Discount amount."""

    _inherit = "sale.order.line"

    @api.constrains('discount')
    def _check_discount(self):
        if self.discount:
            discount_amt = False
            for group in self.env['sales.discount.limit'].search([]):
                if self._uid in group.group_id.users.ids and not discount_amt:
                    discount_amt = group.discount
                    break
            if discount_amt and self.discount > discount_amt:
                raise UserError(
                    _('You are not eligible to give discount '
                      'more than %s %%.' % group.discount))
