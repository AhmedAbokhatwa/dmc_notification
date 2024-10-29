import frappe
from frappe.utils import add_days, add_months, format_date, getdate, today


# # from frappe.desk.notifications import
# do bench migrate and excute it


def send_notification():
    emails = ["shaymaa@dmc.com", "ahmed.atef@gmail.com"]
    msg = "Renewal Date is coming next month"
    for email in emails:
        users = frappe.get_all(
            "Employee",
            fields=["name"],
            filters={"user_id": email},
        )
        for user in users:
            table = frappe.get_all(
                "Comprehensive Health Insurance",
                filters={"parent": user.name, "parenttype": "Employee"},
                fields=["renewal_date", "parent"],
            )
            today_date = getdate(today())
            last_month_date = add_months(today_date, -1)
            print("tab :", last_month_date)
            for row in table:
                if row["renewal_date"] == last_month_date:
                    try:
                        notification = frappe.new_doc("Notification Log")
                        notification.for_user = email
                        notification.set("type", "Alert")
                        notification.document_type = "User"
                        notification.document_name = email
                        notification.subject = msg
                        notification.insert()
                    except Exception:
                        frappe.msgprint("Failed to send reminder")
