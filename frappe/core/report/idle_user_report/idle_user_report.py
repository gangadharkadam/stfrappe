from __future__ import unicode_literals
import frappe
def get_columns():
	return ["User Name:295", "Last Logged on:Date:230","Site Name:395"]

def execute(filters=None):
	columns = get_columns()
	data = []
	dbname=frappe.db.sql("""select site_name from `tabSubAdmin Info` """,as_dict=1)
	lst=[]
	qry_srt='select name,last_login from('
	for key in dbname:
		temp1 =key['site_name']
		temp =key['site_name']
		if temp.find('.')!= -1:
		  temp=temp.split('.')[0][:16]
	    	else:
		  temp=temp[:16]
		qry="SELECT name,last_login,'%s' as site_name FROM  "%(temp1)
		if temp :
			qry+=temp+'.tabUser where name not in ("Guest","Administrator") and (hour(timediff(now(), last_login)) > 24 || last_login is null )'  
			lst.append(qry)
	fin_qry=' UNION '.join(lst)
	qry=qry_srt+fin_qry+" where doc_name='Administrator')foo ORDER BY creation DESC limit 5"
	act_details=frappe.db.sql(fin_qry,as_list=1,debug=1)
	data=act_details
	return columns, data

def get_columns():
	return [
		"User Name:Data:220",
		"Last Logged in on:Date:220",
		"Site Name:Data:320"		
	]