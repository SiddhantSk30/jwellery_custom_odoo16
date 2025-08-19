/** @odoo-module **/

import { ErrorDialog } from "@web/core/errors/error_dialogs";
import { RPCErrorDialog } from "@web/core/errors/error_dialogs";
import { WarningDialog } from "@web/core/errors/error_dialogs";
import { RedirectWarningDialog } from "@web/core/errors/error_dialogs";
import { SessionExpiredDialog } from "@web/core/errors/error_dialogs";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";

patch(RPCErrorDialog.prototype, "ag_odoo_debrand.RPCErrorDialog", {
    setup() {
        this._super.apply(this, arguments);
        const odoo_tittle_name = session.odoo_tittle_name || 'Dreamwarez';
        var error_type_title = this.props.message;
        error_type_title = error_type_title.replace("Odoo", odoo_tittle_name);
        this.props.message = error_type_title;
        var error_title = this.title;
        error_title = error_title.replace("Odoo", odoo_tittle_name);
        this.title = error_title;
    }
});

patch(WarningDialog.prototype, "ag_odoo_debrand.WarningDialog", {
    setup() {
        this._super.apply(this, arguments);
        const odoo_tittle_name = session.odoo_tittle_name || 'Dreamwarez';
        var error_type_title = this.props.message;
        error_type_title = error_type_title.replace("Odoo", odoo_tittle_name);
        this.props.message = error_type_title;
        var warning_title = this.title;
        warning_title = warning_title.replace("Odoo", odoo_tittle_name)
        this.title = warning_title;
    }
});

patch(RedirectWarningDialog.prototype, "ag_odoo_debrand.RedirectWarningDialog", {
    setup() {
        this._super.apply(this, arguments);
        const odoo_tittle_name = session.odoo_tittle_name || 'Dreamwarez';
        var error_type_title = this.props.message;
        error_type_title = error_type_title.replace("Odoo", odoo_tittle_name);
        this.props.message = error_type_title;
        var warning_title = this.title;
        warning_title = warning_title.replace("Odoo", odoo_tittle_name)
        this.title = warning_title;
    }
});

// patch(SessionExpiredDialog.prototype, "ag_odoo_debrand.SessionExpiredDialog", {
//     setup() {
//         this._super.apply(this, arguments);
//         console.log("**SessionExpiredDialog*****************", this, this.bodyTemplate);
//         const odoo_tittle_name = session.odoo_tittle_name || 'Dreamwarez';
//         var session_expire_title = this.title;
//         session_expire_title = session_expire_title.replace("Odoo", odoo_tittle_name)
//         this.title = session_expire_title;
//     }
// });