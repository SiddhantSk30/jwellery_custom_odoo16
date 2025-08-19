/** @odoo-module **/

import { WebClient } from "@web/webclient/webclient";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";

patch(WebClient.prototype, "ag_odoo_debrand.WebClient", {
    setup() {
        this._super.apply(this, arguments);
        const odoo_tittle_name = session.odoo_tittle_name || 'Dreamwarez';
        this.title.setParts({ zopenerp: odoo_tittle_name }); // zopenerp is easy to grep
    }
});