from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Students(models.Model): # models.Model it is one type of inheritance.
    _name = "students"
    _description = "Student Record"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'no'   
    active = fields.Boolean(default=True, string="Archive This Record")   # this field is responsible on archived or unarchived for records, default=True is this record not archived
    
    # Sequence fields
    ref = fields.Char(default='New', readonly=True) # This is the sequence number for each record    

    # Named Fields    
    no = fields.Integer(required=True, tracking=1) 
    name = fields.Char(required=True, size=20, tracking=1, translate=True)
    desc = fields.Text(tracking=1)    
    date_of_birth = fields.Date()  
    major = fields.Selection(
        [
            ('it' , 'IT'), 
            ('is' , 'IS'),
            ('cs' , 'CS')
        ], required=True, default="it", tracking=1)
    is_married = fields.Boolean(default=False) 
    state = fields.Selection([
            ('new', 'New'), # this status it mean this student is new in the collage(first level)
            ('demonstrator', 'Demonstrator'),
            ('graduate', 'Graduate'),
    ], string='Status', default='new', required=True)
    is_gradute = fields.Boolean(default=False, invisible=True)

    # Relation Fields
    country_id = fields.Many2one('country')
    subjects_ids =  fields.Many2many('subjects', required=True)
    
    # Computed Fields.   
    age = fields.Integer(compute='_compute_age', store=True, readonly=True, groups="app_one.student_manger_group")   

    # Related Fields    
    student_city = fields.Char(related='country_id.city', string='City Name')
    


    # ------------------------------------- *** --------------------------------------
    # Decorators &&  Constrains:
    @api.constrains('age')
    def _check_age(self):
        for rec in self:
            if rec.age <= 18:
                raise ValidationError("Your Age Not suitable to study in university")
    

    @api.constrains('name' , 'desc')
    def _check_description(self):
        for record in self:
            if record.name == record.desc:
                raise ValidationError("Fields name and description must be different")


    # _sql_constrain is  constrain implemented in DB tier(Postgres tier)
    _sql_constraints = [
        ('unique_no', 'unique("no")' , 'This number is existed'),
        ('unique_name', 'unique("name")' , 'This name is existed')
    ]

    @api.depends('date_of_birth', 'country_id.name')  
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = date.today()
                record.age = today.year - record.date_of_birth.year - ((today.month, today.day) < (record.date_of_birth.month, record.date_of_birth.day))
            else:
                record.age = 0
    
    @api.onchange('is_married')
    def change_state(self):       
        for rec in self:
            print('you are change the state')        
            return {
                    'warning': {'title' : 'warning', 'message' : 'You are Change The Value', 'type' : 'notification'}
            }

    # ------------------------------------- *** --------------------------------------
    # Custom CRUD Methods
    @api.model_create_multi
    def create(self, vals):
        res = super(Students, self).create(vals)           
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('students_seq')
        else:
            res.ref = self.env['ir.sequence'].next_by_code('students_seq')
        print("Record Add Successfully")
        return res
    
    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(Students, self)._search(domain, offset=0, limit=None, access_rights_uid=None)
        print("insid read method")
        return res

    def write(self, vals):
        res = super(Students, self).write(vals)         
        print("insid update method")
        return res
    
    def unlink(self):
        res = super(Students, self).unlink()
        print("insid delete method")
        return res   
    # ------------------------------------- *** --------------------------------------
    # States Action Methods
    def action_new(self):
        for rec in self:
            rec.create_history_record(rec.state, 'new', "")
            rec.state = 'new'   # is the same for rec.write({'state' : 'new'})
    
    def action_demonstrator(self):
        for rec in self:
           rec.create_history_record(rec.state, 'demonstrator', "")
           rec.write({'state' : 'demonstrator'})
    
    def action_graduate(self):
        for rec in self:
            rec.create_history_record(rec.state, 'graduate', "")
            rec.state = 'graduate' 

    # Create History Log on state field
    def create_history_record(self, old_state, new_state, reason):
        for rec in self:
            rec.env['students.history'].create({
                'user_id' : rec.env.uid,
                'student_id' : rec.id,
                'old_state' : old_state,
                'new_state' : new_state,
                'reason' : reason or "",
            }) 

    # Popup Window
    def Change_state_action_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.action_change_state_wizard')  # used this line to return the id of server action
        action['context'] = {'default_student_id' : self.id}    # self.name or self.id  To get the current value of the state in the opened record and set it as default value 
        return action          
    # ------------------------------------- *** --------------------------------------
    
    # Server Action
    def ChangeStateToDemonstrator(self):       
       print('action is excuted')      
       self.action_demonstrator()
        
    # Automated Action
    def check_gradute_students(self):              
        student_ids = self.search([]) #  This line self.search([]) is called search domain. and will retrieve all records in the model        
        for rec in student_ids:
            if rec.state == 'graduate': 
                rec.is_gradute = True

    # --------------------------------------------- ** --------------------------------
    # env object 
    def action_env(self):        
        # Search Domain
        print(self.search([]))  # will return All records

        print(self.search([('name' , '=', 'ahmed')]))

        # Operators to join more than one conditions
        print(self.search( [('name' , '=', 'ahmed'), ('country_id' , '=', 'Oman')] )) # and operator. tow conditions and this it mean the tow conditions must be correct
        print(self.search( ['&', ('name' , '=', 'ahmed'), ('country_id' , '=', 'Oman')] )) # and operator it the same for the first one, the , is the default if you have more than conditions and used between them the & 
        print(self.search( ['|', ('name' , '=', 'ahmed'), ('country_id' , '=', 'Oman')] )) # or operator 
        print(self.search( ['!', ('name' , '=', 'ahmed'), ('country_id' , '=', 'Oman')] )) # not operator is the same for: print(self.search( [('name' , '!=', 'ahmed'), ('country_id' , '=', 'Oman')] )) the operator is & between tow conditions


        # Deference between like and ilike is: the case of letters and ilike will return what like return it.
        print(self.search([('name' , 'like', 'ahmed')]))    # will return : ahmed, ahmed1, ahmed123, ahmed_
        print(self.search([('name' , 'like', 'ahmed')]))    # will return : Ahmed, Ahmed12, ... ,  +  ahmed, ahmed1, ahmed123, ahmed_
       
        print(self.search( [ ('name' , 'in', ['ahmed', 'Ali'] ) ] ) )  # is the same for print(self.search( [ ('name' , 'in', ('ahmed', 'Ali') ) ] ) )
        print('-----------------------------')

                        
        print(self.env['country'].search([]))  # This instructions will return all record in the country model 
       
    # Adding Smart Button. to open the form view of the country for the current user
    def action_open_related_country(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.action_country')  # used this line to return the id of server action of the country view
        view_id = self.env.ref('app_one.view_country_form').id # used the ref FUN. to access for teh id of form view
        action['res_id'] = self.country_id.id    # used this to open the form view for the current user             
        action['views'] = [[view_id, 'form']]    # by default the action that returned will show the tree view so we want to show the form view instead of tree view
        return action