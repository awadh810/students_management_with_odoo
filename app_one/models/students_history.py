from odoo import models, fields, api

from odoo import models, fields, api
class NamaModel(models.Model):
    _name = 'students.history'
    _description = "student history"

    user_id = fields.Many2one('res.users')
    student_id = fields.Many2one('students')
    old_state = fields.Char()
    new_state = fields.Char()
    reason = fields.Char()
