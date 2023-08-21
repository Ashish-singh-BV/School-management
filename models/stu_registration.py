from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class StuRegistation(models.Model):
    _name = 'student.registration'
    _description = 'New admission student model'
    _rec_name = 'student_name'
    _inherit = 'mail.thread'

    # About student fields
    student_name = fields.Char(string="Name", required=True, tracking=True)
    student_class = fields.Integer(string="Class")
    student_image = fields.Binary()

    stream = fields.Selection(selection=[
        ('Science', 'Science'), ('Commerce', 'Commerce'), ('Art', 'Art')
    ], string="Stream")

    student_div = fields.Selection(string="Section", selection=[
                                   ('A', 'A'), ('B', 'B')])
    class_teacher = fields.Many2one(
        'school.teachers', compute='class_teacher_asign', string="Class Teacher", store=True)
    roll_no = fields.Integer(string="Roll Number")
    enr_no = fields.Char(string="Enrollment Number", readonly=True)
    student_dob = fields.Date(string="DOB", required=True)
    student_age = fields.Integer(
        string="Age", compute='_compute_age', store=True)
    student_phone = fields.Char(string="Phone", tracking=True)
    # student_email = fields.Char(string="Student Email")

    # for group by month
    dob_month = fields.Char(string='Birth Month',
                            compute='_compute_dob_month', store=True)

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

# constrains for phone no
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
        if ((self.student_class in [11, 12]) and not self.stream):
            raise ValidationError("Stream field is required for class 12.")

# Age caluculation---------------
    @api.depends('student_dob')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.student_dob:
                age = (today - record.student_dob).days // 365
                if age < 4:
                    raise ValidationError("Age should be more than 4 years")
                record.student_age = age

            else:
                record.student_age = 0

# for group by month
    @api.depends('student_dob')
    def _compute_dob_month(self):
        for record in self:
            if record.student_dob:
                # dob_date = fields.Date.from_string(record.student_dob)
                month = record.student_dob.strftime('%B')
                record.dob_month = month

# for teacher assign-----------
    @api.depends('student_class', 'student_div', 'stream')
    def class_teacher_asign(self):
        teachers = self.env['school.teachers']
        for record in self:
            if (0 < record.student_class < 11):
                asign_teacher = teachers.search([
                    ('asign_class', '=', record.student_class),
                    ('respect_div', '=', record.student_div)
                ], limit=1)
                record.class_teacher = asign_teacher.id
                record.stream = False
            elif (record.student_class < 13):
                asign_teacher = teachers.search([
                    ('asign_class', '=', record.student_class),
                    ('respect_div', '=', record.student_div),
                    ('assign_stream', '=', record.stream)
                ], limit=1)
                record.class_teacher = asign_teacher.id
            else:
                raise ValidationError("Our School only have 1-12 classes")

    @api.model_create_multi
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
        leave_date = self.pre_school_leave_date
        if add_date and leave_date:
            if leave_date < add_date or leave_date > date.today():
                raise ValidationError("Invaild addmission and leave date")

    # def name_get(self):
    #     result = []

    #     for rec in self:

    #         result.append((rec.id, f'{rec.phone_code}-{rec.name}'))

    #     return result

    # @api.model
    # def name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
    #     args = list(args or [])
    #     if name :
    #         args += ['|', ('name', operator, name), ('phone_code', operator, name)]
    #     return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    ########### Email##################

    def action_send_email_copy(self):
        for rec in self:
            ir_model_data = self.env['ir.model.data']
            try:
                template_id = ir_model_data._xmlid_lookup(
                    'school_managment.email_template')[2]
            except ValueError:
                template_id = False
            try:
                compose_form_id = ir_model_data._xmlid_lookup(
                    'mail.email_compose_message_wizard_form')[2]
            except ValueError:
                compose_form_id = False
                template_id = self.env.ref(
                    'school_managment.email_template')[2]
            ctx = {
                'default_model': 'student.registration',
                'default_res_id': rec.ids[0],
                'default_use_template': bool(template_id),
                'default_template_id': template_id,
                'default_composition_mode': 'comment',
                'mark_so_as_sent': True,
                'force_email': True,
            }
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'mail.compose.message',
                'views': [(compose_form_id, 'form')],
                'view_id': compose_form_id,
                'target': 'new',
                'context': ctx,
            }

    def action_send_email(self):
        template_id = self.env.ref('school_managment.email_template')
        for rec in self:
            if rec.parent_email:
                template_id.send_mail(rec.id)
            else:
                raise ValidationError("Fill Email Box First")

    def cron_demo_method(self):
        print("preeeeeeeee  cronnn", self)
        # records = self.env['student.registration'].search([])
        # records = self.search([])
        # template_id = self.env.ref('school_managment.email_template')
        # print("before iffffyopooo",template_id,records)

        # for record in records:
        #     print("after iffffyopooo",record.parent_email)

        #     if record.parent_email:

        #         template_id.send_mail(record.id)
        #     else:
        #         print("after else iffff",record,"yopooo",template_id)

    def unlink(self):
        config_value = int(self.env['ir.config_parameter'].get_param(
            'school_managment.cancel_admission'))
        for rec in self:
            print(type(rec.student_age), "demonnnnnnnnnnn", config_value)
            if rec.student_age > config_value:
                return super(StuRegistation, rec).unlink()
            else:
                raise ValidationError(
                    f"'{rec.student_name}' Age should be greater then '{config_value}' To delete his information")
