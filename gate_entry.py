def on_update_after_submit(self,method=None):

	if self.custom_purpose == "Sales":
		if frappe.db.exists("Sales Invoice", {"gate_entry": self.name}):
			sales_invoice = frappe.get_doc("Sales Invoice", {"gate_entry": self.name})
			if sales_invoice:
				si_item = frappe.get_doc("Sales Invoice Item", {"parent": sales_invoice.get('name')})
				if frappe.get_value("Warehouse", si_item.warehouse,  "custom_validate_ewaybill") :
					if sales_invoice.get("e_waybill_status") != "Not Applicable" and not sales_invoice.get("ewaybill"): 
						frappe.throw(f" The E-waybill, which is applicable for Sales Invoice {sales_invoice.get('name')}, has not been generated.")
		
		elif frappe.db.exists("Delivery Note", {"gate_entry": self.name}):
			delivery_note = frappe.get_doc("Delivery Note", {"gate_entry": self.name})
			if delivery_note:
				if  frappe.get_value("Warehouse", delivery_note.set_warehouse,  "custom_validate_ewaybill") :
					if delivery_note.billing_address_gstin != delivery_note.company_gstin and delivery_note.docstatus == 1:
						if not delivery_note.ewaybill :
							frappe.throw(f" The E-waybill, which is applicable for Delivery Note {delivery_note.get('name')}, has not been generated.")
