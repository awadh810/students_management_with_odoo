from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move' 

    def doSomeThing(self):
        print(self, 'do Some Thing')
