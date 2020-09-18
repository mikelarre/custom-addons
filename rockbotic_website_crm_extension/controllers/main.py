# -*- coding: utf-8 -*-
# Copyright © 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp.addons.rockbotic_website_crm.controllers.main import StudentSignUp

class StudentSignUpCustom(StudentSignUp):

    def get_contacus_response(self, values, kwargs):
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://rockbotic.com/gracias-extraescolares/',
            'target': 'self',
            'res_id': self.id,
        }

