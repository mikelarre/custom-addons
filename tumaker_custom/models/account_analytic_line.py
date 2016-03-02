# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api, exceptions, _


class AccountAnalyticAccount(models.Model):
    _name = "account.analytic.account"
    _inherit = "account.analytic.account"

    @api.one
    @api.depends('line_ids', 'line_ids.facturable_qty')
    def _calc_consumed_hours(self):
        lines = self.line_ids.filtered(lambda x: x.journal_id.type ==
                                       'general')
        self.consumed_hours = sum([a.facturable_qty for a in lines])

    @api.one
    @api.depends('quantity_max', 'consumed_hours')
    def _remaining_hours_calc(self):
        self.remaining_hours = (self.quantity_max and
                                (self.quantity_max - self.consumed_hours) or
                                0.0)

    consumed_hours = fields.Float(compute='_calc_consumed_hours',
                                  string="Consumed Hours", store=True)
    remaining_hours = fields.Float(compute='_remaining_hours_calc',
                                   string='Remaining Time',
                                   help='Computed using the formula: Maximum '
                                   'Time - Total Worked Time', store=True)


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    facturable_qty = fields.Float(string='Facturable qty')

    @api.model
    def _prepare_cost_invoice_line(self, invoice_id, product_id, uom, user_id,
                                   factor_id, account, analytic_lines,
                                   journal_type, data):
        product_obj = self.env['product.product']

        # uom_context = dict(context or {}, uom=uom)
        self = self.with_context(uom=uom)

        total_price = sum(l.amount for l in analytic_lines)
        total_qty = sum(l.facturable_qty for l in analytic_lines)

        if data.get('product'):
            # force product, use its public price
            if isinstance(data['product'], (tuple, list)):
                product_id = data['product'][0]
            else:
                product_id = data['product']
            unit_price = self._get_invoice_price(account, product_id, user_id,
                                                 total_qty)
        elif journal_type == 'general' and product_id:
            # timesheets, use sale price
            unit_price = self._get_invoice_price(account, product_id, user_id,
                                                 total_qty)
        else:
            # expenses, using price from amount field
            unit_price = total_price*-1.0 / total_qty

        factor = self.env['hr_timesheet_invoice.factor'].browse(factor_id)
        factor_name = factor.customer_name or ''
        curr_invoice_line = {
            'price_unit': unit_price,
            'quantity': total_qty,
            'product_id': product_id,
            'discount': factor.factor,
            'invoice_id': invoice_id,
            'name': factor_name,
            'uos_id': uom,
            'account_analytic_id': account.id,
        }
        general_account = analytic_lines[0].account_id
        if product_id:
            product = product_obj.browse(product_id)
            factor_name = product.name_get()[0][1]
            if factor.customer_name:
                factor_name += ' - ' + factor.customer_name

            general_account = (product.property_account_income or
                               product.categ_id.property_account_income_categ)
            if not general_account:
                raise exceptions.Warning(_("Configuration Error!") + '\n' +
                                         _("Please define income account for "
                                           "product '%s'.") % product.name)
            taxes = product.taxes_id or general_account.tax_ids
            tax = account.partner_id.property_account_position.map_tax(taxes)
            curr_invoice_line.update({
                'name': factor_name,
                'invoice_line_tax_id': [(6, 0, tax.ids)],
                'account_id': general_account.id,
            })

            note = []
            for line in analytic_lines:
                # set invoice_line_note
                details = []
                if data.get('date', False):
                    details.append(line['date'])
                if data.get('time', False):
                    if line['product_uom_id']:
                        details.append("%s %s" % (line.facturable_qty,
                                                  line.product_uom_id.name))
                    else:
                        details.append("%s" % (line['facturable_qty'], ))
                if data.get('name', False):
                    details.append(line['name'])
                if details:
                    note.append(u' - '.join(map(lambda x: unicode(x) or '',
                                                details)))
            if note:
                curr_invoice_line['name'] += "\n" + ("\n".join(
                    map(lambda x: unicode(x) or '', note)))
        return curr_invoice_line