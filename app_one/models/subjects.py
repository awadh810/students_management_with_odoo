from odoo import  models, fields, api
from odoo.exceptions import ValidationError


class Subject(models.Model):
    _name = 'subjects'

    no_subject = fields.Integer(string='Subject Number', required=True)  #default=int('_default_id + 1'), readonly=True
    name = fields.Char(string='Subject Name' , required=True)
    level = fields.Selection([
        ("first","First"),
        ("second","Second"),
        ("third","Third"),
        ("fourth","Fourth"),
        ], string='Levels', default='first', required=True
    )
    #mark = fields.Float(string='Subject Mark', required=True)
    

    _sql_constraints = [
        ('unique_no', 'unique("no")' , 'This number is existed'),
        ('unique_name', 'unique("name")' , 'This name is existed')
    ]