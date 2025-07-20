from odoo import models, fields


class Dashboard(models.Model):
    _name = 'dashboard.dashboard'
    _description = 'Dashboard'

    name = fields.Char(string="Dashboard Name", required=True)
    menu_name = fields.Char(string="Menu Name", required=True)
    parent_menu_id = fields.Many2one(
        'ir.ui.menu',
        string="Show Under Menu",
        domain="[('parent_id', '=', False)]"
    )
    sequence = fields.Integer(string="Sequence", default=1)

    user_id = fields.Many2one(
        'res.users',
        string="Owner",
        default=lambda self: self.env.user,
        required=True
    )
    is_public = fields.Boolean(string="Public", default=False)
    group_ids = fields.Many2many('res.groups', string="Visible to Groups")
    company_id = fields.Many2one(
        'res.company',
        string="Company",
    )
    item_ids = fields.One2many(
        'dashboard.item',
        'dashboard_id',
        string="Dashboard Items"
    )

    # ✅ Recommended additions
    client_action_id = fields.Many2one('ir.actions.client', string="Client Action")
    layout_config = fields.Text(string="Layout JSON")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
    ], string="Status", default='draft')
    color_theme = fields.Char(string="Theme Class")