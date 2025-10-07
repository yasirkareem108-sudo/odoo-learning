/* @odoo-module */

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class LibrarySystray extends Component {
    setup() {
        this.orm = useService("orm");
        this.user = useService("user");   // ✅ user service
        this.state = useState({ count: 0 });
        this.loadData();
    }

    async loadData() {
        try {
            const partnerId = this.user.partnerId;   // ✅ safer than env.session.uid

            // Count borrowed books
            const borrowedCount = await this.orm.call(
                "library.borrow",
                "search_count",
                [[["student_id", "=", partnerId], ["state", "=", "borrowed"]]]
            );

            this.state.count = borrowedCount;
            console.log("📚 Borrowed books fetched:", borrowedCount);
        } catch (error) {
            console.error("❌ Failed to fetch borrowed books:", error);
        }
    }
}

LibrarySystray.template = "library_management.LibrarySystray";

registry.category("actions").add("LibrarySystray", LibrarySystray);

console.log("✅ [LibrarySystray] client action loaded successfully");