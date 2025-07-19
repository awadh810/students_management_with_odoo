from odoo import models , fields

class ModelA(models.Model):
    _name = "model.a"
    _log_access = False  # This attr it used just with : models.Model

    no = fields.Integer()
    name = fields.Char()
    major = fields.Selection(
        [
            ('it' , 'IT') , 
            ('is' , 'IS') ,
            ('cs' , 'CS')
        ]
    )
    is_married = fields.Boolean(default=False)

class ModelB(models.TransientModel):
    _name = "model.b"
    
    no = fields.Integer()
    name = fields.Char()
    price = fields.Float(digits=(0 , 3)) # this digits attribute to Float numbers 


class ModelC(models.TransientModel): 
    _name = "model.c"   # in the db will be : model_c  
    _description = "Model C"

    date = fields.Date()
    note = fields.Text(string="write your note here")
    is_show = fields.Boolean()

    
class ModelD(models.AbstractModel):
    _name = "model.d"



