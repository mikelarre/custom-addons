# -*- coding: utf-8 -*-
# © 2015 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Astikar - Custom",
    "version": "8.0.3.22.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>",
        "Esther Martín <esthermartin@avanzosc.es>",
        "Ainara Galdona <ainaragaldona@avanzosc.es>",
        "Daniel Campos <danielcampos@avanzosc.es>",
    ],
    "depends": [
        "account",
        "account_analytic_analysis",
        "account_due_list",
        "account_invoice_line_stock_move_info",
        "account_payment_partner",
        "analytic",
        "base_user_signature_logo",
        "base_vat",
        "delivery",
        "mrp",
        "mrp_repair",
        "mrp_repair_analytic",
        "mrp_repair_cancel_reason",
        "mrp_repair_customer_lot",
        "mrp_repair_date",
        "mrp_repair_estimated_qty",
        "mrp_repair_fee",
        "mrp_repair_partner_analytic",
        "mrp_repair_pricelist_rules",
        "mrp_repair_proforma_report",
        "mrp_repair_type",
        "mrp_repair_warranty",
        "project",
        "purchase",
        "purchase_last_price_info",
        "report",
        "res_partner_analytic",
        "sale_order_type",
        "stock",
        "stock_account",
        "stock_valued_picking_report",
        "warning",
        "web",
        "mrp_repair_estimated_cost",
        "report_webkit"
    ],
    "data": [
        "views/account_analytic_view.xml",
        "views/account_invoice_view.xml",
        "views/astikar_custom_view.xml",
        "views/astikar_layout_view.xml",
        "views/astikar_reports.xml",
        "views/mrp_repair_fee_view.xml",
        "views/mrp_repair_line_view.xml",
        "views/mrp_repair_view.xml",
        "views/product_view.xml",
        "views/purchase_order_view.xml",
        "views/res_partner_view.xml",
        "views/res_users_view.xml",
        "views/stock_history_view.xml",
        "views/stock_quant_view.xml",
        "views/res_company_view.xml",
        "report/report_purchase_order.xml",
    ],
    "installable": True,
}
