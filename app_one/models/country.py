from odoo import  models, fields, api
from odoo.exceptions import ValidationError

class Country(models.Model):
    _name = "country"
    _description = "country Record"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    code = fields.Integer(required=True)
    name = fields.Char(required=True)
    city = fields.Char(required=True)    
    students_ids = fields.One2many(
        string='students',
        comodel_name='students',  
        inverse_name='country_id'
    )

    _sql_constraints = [
        ('unique_no', 'unique("code")' , 'This number is existed'),
        ('unique_name', 'unique("name")' , 'This name is existed')
    ]

    
    

