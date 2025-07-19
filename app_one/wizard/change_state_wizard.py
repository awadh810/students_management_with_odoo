from odoo import fields, models, api, _
from odoo.exceptions import UserError

class ChangeState(models.TransientModel):   # wizard is TransientModel

    _name = 'change.state'

    student_id = fields.Many2one('students')    
    state = fields.Selection([
        ('new', 'New'), 
        ('demonstrator', 'Demonstrator')                       
    ], default='new')
    reason = fields.Char()

    def action_confirm(self):
        if self.student_id.state == 'graduate':
            self.student_id.state = self.state
            self.student_id.create_history_record('graduate', self.state, self.reason)


    
