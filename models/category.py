from odoo import models, fields, api

class CategoryModel(models.Model):
    _name = 'iscapop.category_model'
    _description = 'Model for the category'
    _order = 'name'
    _sql_constraints = [('iscapop_category_name_unique',
                         'UNIQUE (name)',
                         'There cannot be two categories with the same name!'),]

    name = fields.Char(string="Name", required=True)
    description = fields.Html(string="Description")
    fullName = fields.Char(string="Full Name", compute="getFullName", store=True, readonly=True)
    item_ids = fields.One2many(string="Items", comodel_name="iscapop.item_model", inverse_name="category_id")
    catParent_id = fields.Many2one(string="Parent Category", comodel_name="iscapop.category_model", index=True, ondelete="cascade")
    catChildren_ids = fields.One2many(string="Child Categories", comodel_name="iscapop.category_model", inverse_name="catParent_id")

    @api.depends('name')
    def getFullName(self):
        for record in self:
            if record.catParent_id:
                if record.name:
                    record.fullName = record.catParent_id.fullName + "/" + record.name
                else:
                    record.fullName = record.catParent_id.fullName
            else:
                record.fullName = record.name