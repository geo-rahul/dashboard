/** @odoo-module **/

import { Component, onWillStart, useState, onMounted, useRef} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { DashboardItemWizard } from "./dashboard_item_wizard";


export class DashboardApp extends Component {
  // Declare the props that the ActionManager will pass in:
  static props = {
    action:           { type: Object,   optional: true },
    actionId:         { type: [String, Number], optional: true },
    updateActionState:{ type: Function, optional: true },
    className:        { type: String,   optional: true },
  };

  static components = { DashboardItemWizard };

  static services = [rpc];
  setup() {
    this.notification = useService("notification");
    this.actionService = useService("action");
    this.state = useState({
      dashboards: [],
      currentDashboardId: null,
      quickAccessOptions: [
        { id: 'overview', label: 'Overview' },
        { id: 'reports',  label: 'Reports'  },
      ],
      quickAccess: null,
      configOptions: [
        { id: 'settings', label: 'Settings' },
        { id: 'users',    label: 'Users'    },
      ],
      configOption: null,
      companyId: null,
      userId: null,
      templates: [],
      templateId: null,
      dateFilterOptions: [
        { id: 'today',      label: 'Today'      },
        { id: 'this_week',  label: 'This Week'  },
        { id: 'this_month', label: 'This Month' },
      ],
      dateFilter: null,
      globalFilterOptions: [
        { id: 'all',    label: 'All'      },
        { id: 'mine',   label: 'My Items' },
      ],
      globalFilter: null,
      items: [],
      loading: true,
      editMode: false,
      /* new-dashboard modal state */
      modalOpen:            false,
      newName:              '',
      newMenuName:          '',
      newTemplateId:        null,
      newParentMenuId:      null,
      newSequence:          1,
      newIsPublic:          false,
      availableTemplates:   [],  // loaded on init
      availableMenus:       [],  // top-level menus
      availableGroups:      [],  // loaded on init
      newGroupIds:          [],
      groupDropdownOpen:  false,
      groupSearch: '',
      availableCompanies: [], // for the dropdown
      newCompanyId:       null,
      showItemWizard: false,
      wizardItemId: false,
    });
    this.editMode = useState({ value: false });
    this.history = [];
    this.future  = [];
    this.gridRef = useRef("grid");
    onWillStart(this.loadInitialData.bind(this));
    document.addEventListener('click', this._onDocumentClick.bind(this));
    // Run this once the component is in the DOM

    onMounted(() => this._initGridStack());

  }

  // Initialize GridStack once the DOM is ready
  _initGridStack = () => {
    const container = this.gridRef.el;
    if (!container) {
      console.error("DashboardApp: <div t-ref='grid'> not found");
      return;
    }
    // init and store the instance
    this.grid = window.GridStack.init({
      disableOneColumnMode: true,
      float:                false,
      cellHeight:          120,
      margin:               10,
      // start locked
      disableDrag:   true,
      disableResize: true,
    }, container);
    this.grid.on("change", this._onGridChange);
  }

  async loadInitialData() {
    try {
      console.log('calling RPC')
      const res = await rpc("/dashboard/app/init");
      console.log('asda',res)
      this.state.dashboards = res.dashboards || [];
      if (this.state.dashboards.length > 0) {
        this.state.currentDashboardId = this.state.dashboards[0].id;
        this.state.items = res.items || [];
      } else {
        this.state.currentDashboardId = null;
        this.state.items = [];
      }
      this.state.templates   = res.templates   || [];
      this.state.templateId  = this.state.templates.length > 0 ? this.state.templates[0].id : null;
      this.state.companyId   = res.companyId   || null;
      this.state.userId      = res.userId      || null;
      this.state.availableMenus     = (await rpc('/dashboard/app/menus',{})).menus;
      const grp = await rpc('/dashboard/app/groups',{});
      this.state.availableGroups = grp.groups || [];
//      this.state.availableGroups    = (await rpc('/dashboard/app/groups',{})).groups;
      const compRes = await rpc('/dashboard/app/companies', {});
      this.state.availableCompanies = compRes.companies || [];
      this.state.newCompanyId = this.state.availableCompanies[0]?.id ?? null;
    } catch (e) {
      console.error("Failed to initialize dashboard data:", e);
      this.state.dashboards = [];
      this.state.currentDashboardId = null;
      this.state.items = [];
      this.state.templates = [];
      // load templates, menus, groups for wizard
//      this.state.availableTemplates = await rpc('/dashboard/app/templates',{});

    } finally {
      this.state.loading = false;
    }
  }

  async changeDashboard(ev) {
    const id = parseInt(ev.target.value, 10);
    this.state.currentDashboardId = id;
    this.state.loading = true;
    try {
      const res = await rpc("/dashboard/item/load",{ dashboard_id: id });
      this.state.items = res.items || [];
    } catch (e) {
      console.error("Failed to load items:", e);
      this.state.items = [];
    } finally {
      this.state.loading = false;
    }
  }

  openDashboardWizard() {
    Object.assign(this.state, {
      modalOpen:       true,
      newName:         '',
      newMenuName:     '',
      groupSearch:     '',
//      newTemplateId:   this.state.availableTemplates[0]?.id ?? null,
      newParentMenuId: this.state.availableMenus[0]?.id ?? null,
      newSequence:     this.state.dashboards.length + 1,
      newIsPublic:     false,
      newGroupIds:     [],
      newCompanyId:    this.state.availableCompanies[0]?.id ?? null,
    });
  }

  // helper to get group name by id
  getGroupName(id) {
    const g = this.state.availableGroups.find(g => g.id === id);
    return g ? g.name : '';
  }

  // called when you click the input area
  toggleGroupDropdown(ev) {
    ev.stopPropagation();
    this.state.groupDropdownOpen = !this.state.groupDropdownOpen;
    if (this.state.groupDropdownOpen) {
      this.state.groupSearch = '';
    }
  }

  toggleGroup(id) {
    const idx = this.state.newGroupIds.indexOf(id);
    if (idx === -1) {
      this.state.newGroupIds.push(id);
    } else {
      this.state.newGroupIds.splice(idx, 1);
    }
  }

  // close when clicking elsewhere
  _onDocumentClick() {
    if (this.state.groupDropdownOpen) {
      this.state.groupDropdownOpen = false;
    }
  }

  // checkbox toggles membership
  toggleGroup = (id) => {
    const idx = this.state.newGroupIds.indexOf(id);
    if (idx === -1) {
      this.state.newGroupIds.push(id);
    } else {
      this.state.newGroupIds.splice(idx, 1);
    }
  }

  removeGroup = (ev, id) => {
      ev.stopPropagation();
      const idx = this.state.newGroupIds.indexOf(id);
      if (idx !== -1) {
        this.state.newGroupIds.splice(idx, 1);
      }
    }



  // don’t forget to clean up!
  willUnmount() {
    document.removeEventListener('click', this._onDocumentClick);
  }

  closeWizard() {
    this.state.modalOpen = false;
  }

  async createDashboard() {
      // 1) Build the base params
      const params = {
        name:           this.state.newName,
        menu_name:      this.state.newMenuName,
        parent_menu_id: this.state.newParentMenuId,
        sequence:       this.state.newSequence,
        is_public:      this.state.newIsPublic,
        group_ids:      this.state.newGroupIds,
      };

      // 2) Only add company_id if the user picked a valid number
      if (Number.isInteger(this.state.newCompanyId)) {
        params.company_id = this.state.newCompanyId;
      }

      try {
        // 3) Send the RPC with exactly the keys we want
        const res = await rpc("/dashboard/app/create", params);

        // 4) Update UI: add + select the new dashboard
        this.state.dashboards.push({ id: res.id, name: res.name });
        this.state.currentDashboardId = res.id;
        this.state.modalOpen = false;

        // 5) Reload items for the newly created dashboard
        await this.changeDashboard({ target: { value: res.id } });

        // 6) Success toast
        this.notification.add(
          _t('"%1" has been successfully created.', [res.name]),
          {
            title:  _t("Dashboard Created"),
            type:   "success",
            sticky: false,
          }
        );
      } catch (e) {
        console.error("Create Dashboard failed:", e);
        this.notification.add(
          _t("Could not create dashboard:\n%1", [e.message]),
          {
            title:  _t("Error"),
            type:   "danger",
            sticky: true,
          }
        );
      }
    }


  onQuickAccess(option) {
    this.state.quickAccess = option;
    // handle quick access logic…
  }

  onConfig(option) {
    this.state.configOption = option;
    // handle configuration logic…
  }

  changeTemplate(templateId) {
    this.state.templateId = templateId;
    // optionally reload items…
  }

  changeDateFilter(filterId) {
    this.state.dateFilter = filterId;
    // re-filter items…
  }

  changeGlobalFilter(filterId) {
    this.state.globalFilter = filterId;
    // re-filter items…
  }

  toggleEditMode() {
      this.editMode.value = !this.editMode.value;
      if (this.grid) {
        this.grid.enableMove(this.editMode.value);
        this.grid.enableResize(this.editMode.value);
      }
    }

  _onGridChange(/* event, items */) {
    this.history.push(this._serializeLayout());
    this.future = [];
  }

  _serializeLayout() {
    return this.grid.engine.nodes.map(node => ({
      id:     node.el.getAttribute("data-gs-id"),
      x:      node.x,
      y:      node.y,
      width:  node.w,
      height: node.h,
    }));
  }

  _applyLayout(layout) {
    layout.forEach(l => {
      const el = this.refs.grid.querySelector(`[data-gs-id="${l.id}"]`);
      this.grid.update(el, { x: l.x, y: l.y, w: l.width, h: l.height });
    });
  }

  undo() {
    if (this.history.length) {
      const last = this.history.pop();
      this.future.push(this._serializeLayout());
      this._applyLayout(last);
    }
  }

  redo() {
    if (this.future.length) {
      const next = this.future.pop();
      this.history.push(this._serializeLayout());
      this._applyLayout(next);
    }
  }

  async saveLayout() {
    const layout = this._serializeLayout();
    await rpc("/dashboard/item/save_layout", {
      layout,
      dashboard_id: this.state.currentDashboardId,
    });
    this.toggleEditMode();
    this.notification.add(
      _t("Layout saved successfully."),
      { title: _t("Success"), type: "success" }
    );
  }

  openChartWizard(itemId = null) {
    this.state.showItemWizard = true;
    this.state.wizardItemId = itemId;
  }

  closeChartWizard = () => {
        this.state.showItemWizard = false;
        this.state.wizardItemId = false;
    }

}

DashboardApp.template = "dynamic_dashboard_builder.DashboardApp";
registry.category("actions").add("dynamic_dashboard_builder.dashboard_canvas_app", DashboardApp);