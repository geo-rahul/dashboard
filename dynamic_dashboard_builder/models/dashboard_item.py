
from odoo import models, fields


class DashboardItem(models.Model):
    _name = 'dashboard.item'
    _description = 'Dashboard Item'
    _order = 'sequence, name'

    # --- GENERAL ---
    name = fields.Char(required=True)
    dashboard_id = fields.Many2one('dashboard.dashboard', required=True, ondelete='cascade')
    model_id = fields.Many2one('ir.model', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    item_type = fields.Selection([
        ('kpi', 'KPI Tile'),
        ('bar', 'Bar Chart'),
        ('hbar', 'Horizontal Bar Chart'),
        ('line', 'Line Chart'),
        ('area', 'Area Chart'),
        ('pie', 'Pie Chart'),
        ('doughnut', 'Doughnut Chart'),
        ('polar', 'Polar Area Chart'),
        ('scatter', 'Scatter Chart'),
        ('radar', 'Radar Chart'),
        ('radial', 'Radial Bar Chart'),
        ('flower', 'Flower View'),
        ('funnel', 'Funnel Chart'),
        ('bullet', 'Bullet Chart'),
        ('list', 'List View'),
        ('map', 'Map View'),
    ], required=True)
    sequence = fields.Integer(default=10)
    description = fields.Text()
    help_text = fields.Text()

    # --- DATA CONFIGURATION ---
    measure_field_ids = fields.Many2many('ir.model.fields', 'dashboard_item_measure_rel', 'item_id', 'field_id', ondelete='cascade')
    secondary_measure_ids = fields.Many2many('ir.model.fields', 'dashboard_item_secondary_measure_rel', 'item_id', 'field_id', ondelete='cascade')
    data_aggregation = fields.Selection([('count', 'Count'), ('sum', 'Sum'), ('avg', 'Average')], default='count')
    data_aggregation_field_id = fields.Many2one('ir.model.fields', ondelete='cascade')

    # --- GROUPING / SORTING ---
    group_by_field_id = fields.Many2one('ir.model.fields', ondelete='cascade')
    group_by_date_unit = fields.Selection([
        ('minute', 'Minute'), ('hour', 'Hour'), ('day', 'Day'), ('week', 'Week'), ('month', 'Month'),
        ('quarter', 'Quarter'), ('year', 'Year'), ('month_year', 'Month-Year')
    ])
    sub_group_by_field_id = fields.Many2one('ir.model.fields', ondelete='cascade')
    sort_field_id = fields.Many2one('ir.model.fields', ondelete='cascade')
    sort_order = fields.Selection([('asc', 'Ascending'), ('desc', 'Descending')], default='desc')
    limit_enabled = fields.Boolean(default=False)
    limit_value = fields.Integer(default=10)

    # --- FILTERING ---
    domain = fields.Char()
    date_field_id = fields.Many2one('ir.model.fields', ondelete='cascade')
    default_date_range = fields.Selection([
        ('l_none', 'None'),
        ('l_day', 'Today'),
        ('t_week', 'This Week'),
        ('t_month', 'This Month'),
        ('t_quarter', 'This Quarter'),
        ('t_year', 'This Year'),
        ('td_week', 'Week to Date'),
        ('td_month', 'Month to Date'),
        ('td_quarter', 'Quarter to Date'),
        ('td_year', 'Year to Date'),
        ('n_day', 'Next Day'),
        ('n_week', 'Next Week'),
        ('n_month', 'Next Month'),
        ('n_quarter', 'Next Quarter'),
        ('n_year', 'Next Year'),
        ('ls_day', 'Last Day'),
        ('ls_week', 'Last Week'),
        ('ls_month', 'Last Month'),
        ('ls_quarter', 'Last Quarter'),
        ('ls_year', 'Last Year'),
        ('l_week', 'Last 7 days'),
        ('l_month', 'Last 30 days'),
        ('l_quarter', 'Last 90 days'),
        ('l_year', 'Last 365 days'),
        ('ls_past_until_now', 'Past Till Now'),
        ('ls_pastwithout_now', ' Past Excluding Today'),
        ('n_future_starting_now', 'Future Starting Now'),
        ('n_futurestarting_tomorrow', 'Future Starting Tomorrow'),
        ('l_custom', 'Custom Filter'),
    ], default='l_none',string='Date Range')

    # --- DISPLAY OPTIONS ---
    number_format = fields.Selection([('english', 'English'), ('indian', 'Indian'), ('exact', 'Exact')])
    show_unit = fields.Boolean(string="Show Unit")
    unit_type = fields.Selection([('currency', 'Currency'), ('custom', 'Custom')],string="Unit Type")
    char_unit = fields.Char(string="Unit")
    item_theme = fields.Char(string="Theme")
    background_color = fields.Char(string="Custom Background Color (RGBA)")
    font_color = fields.Char(string="Font Color (RGBA)")

    value_format = fields.Selection([('currency', 'Currency'), ('integer', 'Integer'), ('decimal', 'Decimal')])
    decimal_places = fields.Integer(default=2)
    is_stacked = fields.Boolean()
    color_palette = fields.Selection([('default', 'Default'), ('cool', 'Cool'), ('warm', 'Warm'), ('neon', 'Neon')], default='default')
    value_suffix = fields.Char()
    label_position = fields.Selection([('top', 'Top'), ('inside', 'Inside'), ('outside', 'Outside')])
    icon = fields.Char()

    # --- ADVANCED CONFIG ---
    show_legend = fields.Boolean(default=True)
    show_values_on_chart = fields.Boolean()
    use_multiplier = fields.Boolean()
    multiplier_line_ids = fields.One2many('dashboard.item.multiplier', 'item_id')

    # --- TARGET SUPPORT ---
    enable_target = fields.Boolean()
    target_value = fields.Float()
    target_type = fields.Selection([('line', 'Line'), ('bar', 'Bar')])
    target_line_ids = fields.One2many('dashboard.item.target.line', 'item_id')

    # --- INTERACTIVITY / ACTIONS ---
    action_model = fields.Char()
    action_domain = fields.Text()

    # --- LAYOUT INFO ---
    position_x = fields.Integer(default=0)
    position_y = fields.Integer(default=0)
    width = fields.Integer(default=4)
    height = fields.Integer(default=2)
    refresh_interval = fields.Integer(help="In seconds (e.g., 30, 60, 300)", default=0)
    is_global_item = fields.Boolean()

    # --- PATCHED FIELDS (ENHANCED FUNCTIONALITY) ---
    secondary_model_id = fields.Many2one('ir.model', string="Secondary KPI Model")
    secondary_measure_field_id = fields.Many2one('ir.model.fields', string="Secondary KPI Measure Field")
    secondary_aggregation_type = fields.Selection([
        ('count', 'Count'), ('sum', 'Sum'), ('average', 'Average')
    ], string="Secondary KPI Aggregation", default='sum')
    secondary_domain = fields.Char(string="Secondary KPI Domain")
    secondary_date_field_id = fields.Many2one('ir.model.fields', string="Secondary KPI Date Field")
    secondary_date_range = fields.Selection([
        ('this_month', 'This Month'), ('last_month', 'Last Month'), ('this_year', 'This Year'),
        ('last_year', 'Last Year'), ('last_7_days', 'Last 7 Days'), ('last_30_days', 'Last 30 Days'),
        ('custom', 'Custom'),
    ], string="Secondary KPI Date Filter")

    is_cumulative = fields.Boolean(string="Cumulative Graph")
    cumulative_measure_field_ids = fields.Many2many('ir.model.fields','cumulative_measure_field_rel', string="Cumulative Fields")
    line_measure_field_ids = fields.Many2many('ir.model.fields','line_measure_field_rel', string="Line Overlay Measures")
    semi_circle_mode = fields.Boolean(string="Semi Circle Display")
    stacked_chart = fields.Boolean(string="Stacked Chart")

    record_limit_enabled = fields.Boolean(string="Enable Record Limit")
    record_limit = fields.Integer(string="Record Limit", default=10)

    icon_class = fields.Char(string="Icon Class")
    icon_color = fields.Char(string="Icon Color", default="#ffffff")
    background_color = fields.Char(string="Background Color", default="#ffffff")
    font_color = fields.Char(string="Font Color", default="#000000")
    layout_mode = fields.Selection([
        ('layout1', 'Layout 1'), ('layout2', 'Layout 2'), ('layout3', 'Layout 3')
    ], default='layout1', string="Layout")
    theme = fields.Char(string="Theme", default="white")

    date_filter_selection = fields.Selection([
        ('this_month', 'This Month'), ('last_month', 'Last Month'), ('this_year', 'This Year'),
        ('last_year', 'Last Year'), ('last_7_days', 'Last 7 Days'), ('last_30_days', 'Last 30 Days'),
        ('custom', 'Custom'),
    ], string="Date Filter")
    date_from = fields.Datetime(string="Start Date")
    date_to = fields.Datetime(string="End Date")

    enable_custom_unit = fields.Boolean(string="Use Custom Unit")
    custom_unit_label = fields.Char(string="Custom Unit Label", size=5)
    currency_id = fields.Many2one('res.currency', string="Currency")
    number_format_style = fields.Selection([
        ('english', 'English'), ('indian', 'Indian'), ('exact', 'Exact')
    ], string="Number Format")

    action_window_id = fields.Many2one('ir.actions.act_window', string="Open Window Action")
    client_action_id = fields.Many2one('ir.actions.client', string="Client Action")
    enable_record_click = fields.Boolean(string="Allow Click to Open Records")

    pagination_limit = fields.Integer(string="Pagination Limit", default=20)

    domain_override = fields.Char(string="Extended Domain Filter")
