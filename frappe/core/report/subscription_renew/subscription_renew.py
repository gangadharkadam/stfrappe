from __future__ import unicode_literals
import frappe
def get_columns():
	return ["User Name:295", "Subscription Expiring date:Date:230","Site Name:395"]

def execute(filters=None):
	columns = get_columns()
	data = []
	dbname=frappe.db.sql("""select site_name from `tabSubAdmin Info` """,as_dict=1)
	lst=[]
	qry_srt='select name,validity_end_date from('
	for key in dbname:
		temp1 =key['site_name']
		temp =key['site_name']
		if temp.find('.')!= -1:
		  temp=temp.split('.')[0][:16]
	    	else:
		  temp=temp[:16]
		qry="SELECT name,DATE_FORMAT(validity_end_date,'%d/%m/%Y'),'"+temp1+"' as site_name FROM  "
		if temp :
			qry+=temp+'.tabUser where name not in ("Guest","Administrator")'  
			lst.append(qry)
	fin_qry=' UNION '.join(lst)
	qry=qry_srt+fin_qry+" where doc_name='Administrator')foo ORDER BY creation DESC limit 5"
	act_details=frappe.db.sql(fin_qry,as_list=1,debug=1)
	data=act_details
	return columns, data

def get_columns():
	return [
		"User Name:Data:220",
		"Subscriptio Expiring on:Date:220",
		"Site Name:Data:320"		
	]






