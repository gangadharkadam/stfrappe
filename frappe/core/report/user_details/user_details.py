from __future__ import unicode_literals
import frappe



# def execute(filters=None):
# 	if not filters: filters = {}
	
# 	columns = get_columns()
# 	data = get_details(filters)
# 	#gt=get_totalQty(filters)
# 	return columns,data


def get_columns():
	return ["User Name:95", "Password:130"]

def execute(filters=None):
	frappe.errprint("in the py")
	columns = get_columns()
	data = []
	dbname=frappe.db.sql("""select site_name from `tabSubAdmin Info` where active=1""",as_dict=1)

	frappe.errprint(dbname)
	lst=[]
	qry_srt='select name,password from('
	for key in dbname:
		temp =key['site_name']
		qry="SELECT name,password,'%s' as site_name FROM "%(temp)
		if temp :
			qry+=temp+'.tabUser'
			lst.append(qry)
	fin_qry=' UNION '.join(lst)
	qry=qry_srt+fin_qry+" where doc_name='Administrator')foo ORDER BY creation DESC limit 5"
	act_details=frappe.db.sql(fin_qry,as_list=1,debug=1)
	frappe.errprint(act_details)
	data=act_details


	return columns, data



	







