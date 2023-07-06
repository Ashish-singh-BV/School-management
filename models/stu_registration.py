from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class StuRegistation(models.Model):
    _name = 'student.registration'
    _description = 'New admission student model'
    _rec_name = 'student_name'
    _inherit = 'mail.thread'

    # About student fields
    student_name = fields.Char(string="Name", required=True)
    student_class = fields.Integer(string="Class")

    stream = fields.Selection(selection=[
        ('Science', 'Science'), ('Commerce', 'Commerce'), ('Art', 'Art')
    ], string="Stream")

    student_div = fields.Selection(string="Section", selection=[
                                   ('A', 'A'), ('B', 'B')])
    class_teacher = fields.Many2one(
        'school.teachers', compute='class_teacher_asign', string="Class Teacher")
    roll_no = fields.Integer(string="Roll Number")
    enr_no = fields.Char(string="Enrollment Number", readonly=True)
    student_dob = fields.Date(string="DOB", required=True)
    student_age = fields.Integer(string="Age", compute='_compute_age')
    student_phone = fields.Char(string="Phone", tracking = True)
    
    # for group by month
    dob_month = fields.Char(string='Birth Month', compute='_compute_dob_month', store=True)


    # student parents fields
    parent_name = fields.Char(string="Name")
    parent_relation = fields.Char(string="Relation")
    parent_ph_no = fields.Char(string="Phone")
    parent_email = fields.Char(string="Email")

    # address fields
    adr_street = fields.Char(string="Address")
    adr_street2 = fields.Char()
    adr_pincode = fields.Char()
    adr_contry = fields.Many2one('res.country')
    adr_state = fields.Many2one(
        'res.country.state', domain="[('country_id', '=' , adr_contry)]")
    adr_city = fields.Char()

    # school details
    pre_school_name = fields.Char(string="School Name")
    pre_school_enr_no = fields.Char(string="Your Enrollment Number")
    pre_school_addmisstion_date = fields.Date(string="Admission date")
    pre_school_leave_date = fields.Date(string="Leaving Date")

# constrans for phone no
    @api.constrains('student_phone', 'parent_ph_no')
    def valid_phone_no(self):
        for record in self:
            stu_ph = record.student_phone
            parent_ph = record.parent_ph_no
            if not (stu_ph and (len(stu_ph) == 10) and stu_ph.isdigit()):
                raise ValidationError("Student Phone no. should be 10 digits")
            else:
                existing_record = self.env['student.registration'].search([
                    ('id', '!=', record.id),
                    ('student_phone', '=', stu_ph),
                ], limit=1)
                if existing_record:
                    raise ValidationError(
                        'Student Phone no. should be unique.')

            if not (parent_ph and (len(parent_ph) == 10) and parent_ph.isdigit()):
                raise ValidationError("Parent Phone no. should be 10 digits")
            
    #  constrans for stream field       
    @api.constrains('student_class', 'stream')
    def _check_stream_required(self):
        if ((self.student_class in [11,12]) and not self.stream):
            raise ValidationError("Stream field is required for class 12.")

# Age caluculation---------------
    @api.depends('student_dob')
    def _compute_age(self):
        today = date.today()
        if self.student_dob:
            age = (today - self.student_dob).days // 365
            if age < 4:
                raise ValidationError("Age should be more than 4 years")
            self.student_age = age

        else:
            self.student_age = 0
                
# for group by month            
    @api.depends('student_dob')
    def _compute_dob_month(self):
        for record in self:
            if record.student_dob:
                # dob_date = fields.Date.from_string(record.student_dob)
                month = record.student_dob.strftime('%B')
                record.dob_month = month

# for teacher assign-----------
    @api.depends('student_class', 'student_div','stream')
    def class_teacher_asign(self):
        teachers = self.env['school.teachers']
        if (0<self.student_class < 11):
            asign_teacher = teachers.search([
                ('asign_class', '=', self.student_class),
                ('respect_div', '=', self.student_div)
            ], limit=1)
            self.class_teacher = asign_teacher.id
            self.stream = False
        elif (self.student_class < 13):
            asign_teacher = teachers.search([
                ('asign_class', '=', self.student_class),
                ('respect_div', '=', self.student_div),
                ('assign_stream', '=', self.stream)
            ], limit=1)
            self.class_teacher = asign_teacher.id
        else:
            raise ValidationError("Our School only have 1-12 classes")

    @api.model
    def create(self, vals):
        record = super(StuRegistation, self).create(vals)
        record.enr_no = "ENR-" + str(record.id).zfill(4)
        return record

    def write(self, vals):
        old_stu_no = self.student_phone
        old_stu_name = self.student_name
        new_record = super(StuRegistation, self).write(vals)
        if old_stu_name != self.student_name:
            pass
        if old_stu_no != self.student_phone:
            pass
        return new_record
    
    @api.constrains('pre_school_addmisstion_date', 'pre_school_leave_date')
    def valid_addmisstion_and_leave_date(self):
        add_date = self.pre_school_addmisstion_date
        leave_date =  self.pre_school_leave_date
        if add_date and leave_date:
            if leave_date < add_date or leave_date > date.today():
                raise ValidationError("Invaild addmission and leave date")
       