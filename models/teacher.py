from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SchoolTeacher(models.Model):
    _name = 'school.teachers'
    _description = 'all teacher data'
    _rec_name = 'teacher_name'

    teacher_name = fields.Char(string='Teacher Name', default='ssss')
    asign_class = fields.Integer(string='Assign class to teacher')
    respect_div = fields.Selection(selection=[('A', 'A'), ('B', 'B')])
    assign_stream = fields.Selection(
        selection=[('Science', 'Science'), ('Commerce', 'Commerce'), ('Art', 'Art')])
    chek_action = fields.Char(string='action_chek')
    gen_seq = fields.Char(string='Genrating seq.')
    o2m_field = fields.One2many(
        comodel_name="student.registration", inverse_name="class_teacher", string="O2M")
    m2m_field = fields.Many2many(
        comodel_name="student.registration", string="M2M")

    #  constrains for stream field

    @api.constrains('asign_class', 'assign_stream')
    def _check_stream_required(self):
        if ((self.asign_class in [11, 12]) and not self.assign_stream):
            raise ValidationError("Stream field is required for class 12.")

    @api.model_create_multi
    def create(self, vals):
        all_teacher = self.env['school.teachers'].search([('asign_class', '=', vals['asign_class']),
                                                          ('respect_div', '=', vals['respect_div']), ('assign_stream', '=', vals['assign_stream'])]) or 0
        if all_teacher:
            raise ValidationError(
                f"This class already assign to '{all_teacher.teacher_name}'")
        return super(SchoolTeacher, self).create(vals)

    def url_redirect(self):
        return {
            "type": "ir.actions.act_url",
            "url": "https://odoo.com",
            # "target": "self",
        }

    def chek_func(record):
        record.chek_action = "from xml call"

    @api.model
    def default_get(self, fields):
        print(fields, "ggggggggggg")
        print("tttttttttttt", type(fields))
        res = super(SchoolTeacher, self).default_get(fields)

        # if not res['teacher_name']:
        res['teacher_name'] = "from default get"
        # else:
        res['chek_action'] = "default get else part"
        return res

    def genrate_sequence(self):
        self.gen_seq = self.env['ir.sequence'].next_by_code(
            'seq.school.teachers') or 'somthing wrong'

    def exc_query(self):
        query = f"""INSERT INTO school_teachers(teacher_name,asign_class,respect_div) VALUES('yooo',9,'A')"""

        self.env.cr.execute(query)
