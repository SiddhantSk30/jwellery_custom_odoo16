/** @odoo-module **/

import { Dialog } from "@web/core/dialog/dialog";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";

patch(Dialog.prototype, "ag_odoo_debrand.Dialog", {
    setup() {
        this._super.apply(this, arguments);
        const odoo_tittle_name = session.odoo_tittle_name || "Dreamwarez";
        this.title = odoo_tittle_name;
    },
});

