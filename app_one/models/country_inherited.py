from odoo import models

class CountryInherited(models.Model):
    _name = 'country.inherited'
    _inherit = 'country'
    