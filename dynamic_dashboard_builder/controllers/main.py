from odoo import http
from odoo.http import request

class DashboardController(http.Controller):

    @http.route('/dashboard/app/init', type='json', auth="public", csrf=False)
    def app_init(self):
        user = request.env.user
        D = request.env['dashboard.dashboard'].sudo()

        # 1) build domain of dashboards visible to this user:
        #    - public dashboards
        #    - OR owned by user
        #    - OR linked to a group the user belongs to
        domain = ['|', ('is_public', '=', True),
                  '|', ('user_id', '=', user.id),
                  ('group_ids', 'in', user.groups_id.ids)]
        dashboards = D.search(domain, order='name')

        # map to id/name
        dash_data = [
            {'id': d.id, 'name': d.name}
            for d in dashboards
        ]

        # 2) default: load items for the first dashboard (if any)
        items_data = []
        if dash_data:
            items_data = self._get_items(dash_data[0]['id'])

        return {
            'dashboards': dash_data,
            'items': items_data,
        }

    @http.route('/dashboard/item/load', type='json', auth="public", csrf=False)
    def load_items(self, dashboard_id):
        return {
            'items': self._get_items(dashboard_id)
        }

    def _get_items(self, dashboard_id):
        Item = request.env['dashboard.item'].sudo()
        items = Item.search([('dashboard_id', '=', dashboard_id)], order='sequence')
        return [
            {
                'id': it.id,
                'name': it.name,
                'item_type': it.type,
                # …any other fields you need
            }
            for it in items
        ]

    @http.route('/dashboard/app/create', type='json', auth='user')
    def create_dashboard(self, name, menu_name,
                         parent_menu_id, sequence, is_public,
                         group_ids,company_id=None):
        Dashboard = request.env['dashboard.dashboard'].sudo()
        print('werqwerqwerqwe',name,menu_name,parent_menu_id,sequence,is_public,group_ids,company_id)
        print('asdas',type(company_id),company_id)
        if not company_id:
            print('inside if')
            company_id = False
        print('werqwerqwerqwe',name,menu_name,parent_menu_id,sequence,is_public,group_ids,company_id)
        vals = {
            'name': name,
            'menu_name': menu_name,
            # 'template_id': template_id,
            'parent_menu_id': parent_menu_id or False,
            'sequence': sequence or 1,
            'is_public': bool(is_public),
            'company_id': company_id,
            'group_ids': [(6, 0, group_ids or [])],
        }
        dash = Dashboard.create(vals)
        return {
            'id': dash.id,
            'name': dash.name,
        }

    @http.route('/dashboard/app/menus', type='json', auth='user')
    def get_menus(self):
        """Return the sub‐menus under our Dashboards root, so the wizard can choose
        where to show the new dashboard."""
        Menu = request.env['ir.ui.menu'].sudo()
        try:
            # the “Dashboards” root menu we defined in XML
            root = request.env.ref('dynamic_dashboard_builder.menu_dashboard_canvas_root').sudo()
            children = Menu.search([('parent_id', '=', root.id)], order='sequence, name')
        except ValueError:
            # fallback: if the ref is missing, just return top‐level menus
            children = Menu.search([('parent_id', '=', False)], order='sequence, name')
        print('menu',children)
        return {
            'menus': [
                {'id': m.id, 'name': m.name}
                for m in children
            ]
        }

    @http.route('/dashboard/app/groups', type='json', auth='user')
    def get_groups(self):
        """Return all non‐share groups so you can restrict visibility of dashboards."""
        Group = request.env['res.groups'].sudo()
        groups = Group.search([('share', '=', False)], order='name')
        print('groups',groups)
        return {
            'groups': [
                {'id': g.id, 'name': g.name}
                for g in groups
            ]
        }

    @http.route('/dashboard/app/companies', type='json', auth='user')
    def get_companies(self):
        Company = request.env['res.company'].sudo()
        companies = Company.search([], order='name')
        return {
            'companies': [
                {'id': c.id, 'name': c.name}
                for c in companies
            ]
        }