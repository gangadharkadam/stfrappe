from __future__ import unicode_literals
import frappe
def get_columns():
	return ["Site Name:220", "Site Created on:Date:120",
	"Customer Name:120","Country:80","Administrator Email Id:250"]

def execute(filters=None):
	columns = get_columns()
	qry="select name ,DATE(creation) ,client_name,country ,email_id__if_administrator  from `tabSite Master` order by creation asc"
	data = []	
	act_details=frappe.db.sql(qry,as_list=1,debug=1)
	data=act_details
	return columns, data

def get_columns():
	return [
		"Site Name:Data:220",
		"Site Created on:Date:120",
		"Customer Name:Data:120",
		"Country:Data:80",
        "Administrator Email Id:Data:250"
	]