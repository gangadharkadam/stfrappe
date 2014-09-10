from __future__ import unicode_literals
import frappe
from frappe import _
import frappe.defaults
import frappe.permissions
from frappe.core.doctype.user.user import get_system_users
from frappe.utils.csvutils import UnicodeWriter, read_csv_content_from_uploaded_file
from frappe.defaults import clear_default
import datetime

def formated_date(date_str):
	return  datetime.datetime.strptime(date_str , '%d-%m-%Y').strftime('%Y-%m-%d')
	 
@frappe.whitelist()
def get_sales_pie(from_date=None,to_date=None,currency=None,country=None):
	frappe.errprint("get_sales_pie")
	qry=''
	if from_date:
		from_date=from_date[6:] + "-" + from_date[3:5] + "-" + from_date[:2]
	if to_date:
		to_date=to_date[6:] + "-" + to_date[3:5] + "-" + to_date[:2]
	if not from_date and not to_date and not country and not currency:
		qry="SELECT substring(date_format(so.creation,'%Y-%M'),1,8)AS MONTH,SUM( COALESCE((SELECT SUM(COALESCE(sii.amount,0)) FROM `tabSales Invoice Item` sii WHERE sii.sales_order=so.name),0) ) /(case when 'USD'='INR' then 1 when 'USD'='USD' then (select value from tabSingles where doctype='Global Defaults' and field='currency_conversion_rate') else 1 end) AS sales_amount FROM `tabSales Order` so WHERE so.creation BETWEEN COALESCE(NULL,'1111-09-01 14:49:40') AND COALESCE(NULL,'9999-09-01 14:49:40') AND COALESCE(so.country,0)=COALESCE(NULL,COALESCE(so.country,0)) GROUP BY MONTH;" 
	elif not currency:
		currency='INR'
	elif country :
		qry="SELECT substring(date_format(so.creation,'%Y-%M'),1,8)AS MONTH,SUM( COALESCE((SELECT SUM(COALESCE(sii.amount,0)) FROM `tabSales Invoice Item` sii WHERE sii.sales_order=so.name),0) ) /(case when '"+currency+"'='INR' then 1 when '"+currency+"'='USD' then (select value from tabSingles where doctype='Global Defaults' and field='currency_conversion_rate') else 1 end) AS sales_amount FROM `tabSales Order` so WHERE so.creation BETWEEN COALESCE('"+from_date+"','1111-09-01 14:49:40') AND COALESCE('"+to_date+"','9999-09-01 14:49:40') AND COALESCE(so.country,0)=COALESCE('"+country+"',COALESCE(so.country,0)) GROUP BY MONTH;" 
	else:
		qry="SELECT substring(date_format(so.creation,'%Y-%M'),1,8)AS MONTH,SUM( COALESCE((SELECT SUM(COALESCE(sii.amount,0)) FROM `tabSales Invoice Item` sii WHERE sii.sales_order=so.name),0) ) /(case when '"+currency+"'='INR' then 1 when '"+currency+"'='USD' then (select value from tabSingles where doctype='Global Defaults' and field='currency_conversion_rate') else 1 end) AS sales_amount FROM `tabSales Order` so WHERE so.creation BETWEEN COALESCE('"+from_date+"','1111-09-01 14:49:40') AND COALESCE('"+to_date+"','9999-09-01 14:49:40') AND COALESCE(so.country,0)=COALESCE(NULL,COALESCE(so.country,0)) GROUP BY MONTH;" 	
	frappe.errprint(qry)
	data_dict = frappe.db.sql(qry,debug=1)
	return{
		"sales_order_total": data_dict
	}


@frappe.whitelist()
def get_sales_column(country=None,from_date=None,to_date=None,currency=None):
	frappe.errprint("get_sales sicolumn")
	# frappe.errprint(country)
	# frappe.errprint(currency)
	qry=''
	if from_date:
		from_date=from_date[6:] + "-" + from_date[3:5] + "-" + from_date[:2]
	if to_date:
		to_date=to_date[6:] + "-" + to_date[3:5] + "-" + to_date[:2]
	if not from_date and not to_date and not country and not currency:
		qry="SELECT substring(date_format(so.creation,'%Y-%M'),1,8)AS MONTH,SUM( COALESCE((SELECT SUM(COALESCE(sii.amount,0)) FROM `tabSales Invoice Item` sii WHERE sii.sales_order=so.name),0) ) /(case when 'INR'='INR' then 1 when 'USD'='USD' then (select value from tabSingles where doctype='Global Defaults' and field='currency_conversion_rate') else 1 end) AS sales_amount,SUM( COALESCE((SELECT SUM(CAST(REPLACE(total_amount,'INR','') AS INTEGER)) FROM `tabJournal Voucher` jv WHERE name IN( SELECT DISTINCT jvd.parent  FROM `tabJournal Voucher Detail` jvd JOIN `tabSales Invoice` si ON jvd.against_invoice=si.name JOIN `tabSales Invoice Item` sii ON sii.parent=si.name WHERE sii.sales_order=so.name)),0) )/(case when 'INR'='INR' then 1 when 'USD'='USD' then (select value from tabSingles where doctype='Global Defaults' and field='currency_conversion_rate') else 1 end)  AS jv_amount FROM `tabSales Order` so WHERE so.creation BETWEEN COALESCE(null,'1111-09-01 14:49:40') AND COALESCE(null,'9999-09-01 14:49:40') AND COALESCE(so.country,0)=COALESCE(null,COALESCE(so.country,0)) GROUP BY MONTH" 
	elif not currency:
		currency='INR'
	elif country :
		qry="SELECT substring(date_format(so.creation,'%Y-%M'),1,8)AS MONTH,SUM( COALESCE((SELECT SUM(COALESCE(sii.amount,0)) FROM `tabSales Invoice Item` sii WHERE sii.sales_order=so.name),0) ) /(case when '"+currency+"'='INR' then 1 when '"+currency+"'='USD' then (select value from tabSingles where doctype='Global Defaults' and field='currency_conversion_rate') else 1 end) AS sales_amount,SUM( COALESCE((SELECT SUM(CAST(REPLACE(total_amount,'INR','') AS INTEGER)) FROM `tabJournal Voucher` jv WHERE name IN( SELECT DISTINCT jvd.parent  FROM `tabJournal Voucher Detail` jvd JOIN `tabSales Invoice` si ON jvd.against_invoice=si.name JOIN `tabSales Invoice Item` sii ON sii.parent=si.name WHERE sii.sales_order=so.name)),0) )/(case when '"+currency+"'='INR' then 1 when '"+currency+"'='USD' then (select value from tabSingles where doctype='Global Defaults' and field='currency_conversion_rate') else 1 end)  AS jv_amount FROM `tabSales Order` so WHERE so.creation BETWEEN COALESCE('"+from_date+"','1111-09-01 14:49:40') AND COALESCE('"+to_date+"','9999-09-01 14:49:40') AND COALESCE(so.country,0)=COALESCE('"+country+"',COALESCE(so.country,0)) GROUP BY MONTH" 
	else:
		qry="SELECT substring(date_format(so.creation,'%Y-%M'),1,8)AS MONTH,SUM( COALESCE((SELECT SUM(COALESCE(sii.amount,0)) FROM `tabSales Invoice Item` sii WHERE sii.sales_order=so.name),0) ) /(case when '"+currency+"'='INR' then 1 when '"+currency+"'='USD' then (select value from tabSingles where doctype='Global Defaults' and field='currency_conversion_rate') else 1 end) AS sales_amount,SUM( COALESCE((SELECT SUM(CAST(REPLACE(total_amount,'INR','') AS INTEGER)) FROM `tabJournal Voucher` jv WHERE name IN( SELECT DISTINCT jvd.parent  FROM `tabJournal Voucher Detail` jvd JOIN `tabSales Invoice` si ON jvd.against_invoice=si.name JOIN `tabSales Invoice Item` sii ON sii.parent=si.name WHERE sii.sales_order=so.name)),0) )/(case when '"+currency+"'='INR' then 1 when '"+currency+"'='USD' then (select value from tabSingles where doctype='Global Defaults' and field='currency_conversion_rate') else 1 end)  AS jv_amount FROM `tabSales Order` so WHERE so.creation BETWEEN COALESCE('"+from_date+"','1111-09-01 14:49:40') AND COALESCE('"+to_date+"','9999-09-01 14:49:40') AND COALESCE(so.country,0)=COALESCE(null,COALESCE(so.country,0)) GROUP BY MONTH" 	
	frappe.errprint(qry)
	data_dict = frappe.db.sql(qry,debug=1)
	return{
		"sales_order_total": data_dict
	}

def make_cond(data_dict, from_date=None,to_date=None,currency=None):
	if from_date and to_date and currency:
		frappe.errprint("in the else")
		data_dict['cond'] = """ where %(cond_col)s between '%(from_date)s' and '%(to_date)s' and %(cncy)s = '%(currency)s'
			"""%{'cond_col': data_dict.get('cond_col'), 'from_date': formated_date(from_date),
					'to_date': formated_date(to_date),'currency':currency, 'cncy':data_dict.get('cncy')}

	elif from_date and to_date:
		data_dict['cond'] = """ where %(cond_col)s between '%(from_date)s' and '%(to_date)s' 
			"""%{'cond_col': data_dict.get('cond_col'), 'from_date': formated_date(from_date),
					'to_date': formated_date(to_date)}

	elif from_date and to_date and country:
		data_dict['cond'] = """ where %(cond_col)s between '%(from_date)s' and '%(to_date)s' and %(cncy)s = '%(currency)s'  and %(cntry)s = '%(country)s'
			"""%{'cond_col': data_dict.get('cond_col'), 'from_date': formated_date(from_date),
					'to_date': formated_date(to_date),'currency':currency, 'cncy':data_dict.get('cncy'),'country':country, 'cntry':data_dict.get('cntry')}
	else:
		data_dict['cond'] = ' '

def make_query(data_dict):
	frappe.errprint("in the get_data")
	frappe.errprint("select %(cols)s from %(tab)s %(cond)s"%data_dict)
	return frappe.db.sql("select %(cols)s from %(tab)s %(cond)s"%data_dict,debug=1)

@frappe.whitelist()
def get_activities():
	from frappe.utils import get_url, cstr
	frappe.errprint(get_url())
	frappe.errprint("in activities")
	if get_url()=='http://smarttailor':
		frappe.errprint("in the get_activities")
		dbname=frappe.db.sql("""select site_name from `tabSubAdmin Info` where active=1""",as_dict=1)
		frappe.errprint("dbname")
		lst=[]
		qry_srt='select feed_type,subject,site_name,creation from('
		for key in dbname:
			frappe.errprint("key")
			temp =key['site_name']
			if temp.find('.')!= -1:
				temp1=temp.split('.')[0][:16]
		 	else:
				temp1=temp[:16]
			qry="SELECT subject,creation,feed_type,'%s' as site_name FROM "%(temp)
			if temp :
				qry+=temp1+'.tabFeed'
				lst.append(qry)
		fin_qry=' UNION '.join(lst)
		frappe.errprint("fin qry")
		qry=qry_srt+fin_qry+" where doc_name='Administrator')foo ORDER BY creation desc limit 10"
		frappe.errprint(qry)
		act_details=frappe.db.sql(fin_qry,as_dict=1)
		frappe.errprint(act_details)
		if act_details:
			 frappe.errprint(act_details)
			 return act_details
		else:
			 return ' '

@frappe.whitelist()
def get_data_newsalecol(from_date=None,to_date=None,country=None):
	frappe.errprint("in new sales col")
	if from_date:
		from_date=from_date[6:] + "-" + from_date[3:5] + "-" + from_date[:2]
	if to_date:
		to_date=to_date[6:] + "-" + to_date[3:5] + "-" + to_date[:2]
	if not country:
		str1="""select substring(date_format(l.creation,'%Y-%M'),1,8)as month,count(distinct l.name) as lead_count,count(distinct c.name) as cust_count from tabLead l left join tabCustomer c on  l.name=c.lead_name where l.creation between coalesce('"+from_date+"','1111-09-01 14:49:40') and coalesce('"+to_date+"','9999-09-01 14:49:40') and coalesce(l.country,0)=coalesce(null,coalesce(l.country,0))group by date_format(l.creation,'%Y-%M')"""
	else:
		str1="select substring(date_format(l.creation,'%Y-%M'),1,8)as month,count(distinct l.name) as lead_count,count(distinct c.name) as cust_count from tabLead l left join tabCustomer c on  l.name=c.lead_name where l.creation between coalesce('"+from_date+"','1111-09-01 14:49:40') and coalesce('"+to_date+"','9999-09-01 14:49:40') and coalesce(l.country,0)=coalesce('"+country+"',coalesce(l.country,0)) group by date_format(l.creation,'%Y-%M')"
	if not from_date and not to_date and not country:
		str1="select substring(date_format(l.creation,'%Y-%M'),1,8)as month,count(distinct l.name) as lead_count,count(distinct c.name) as cust_count from tabLead l left join tabCustomer c on  l.name=c.lead_name where l.creation between coalesce(null,'1111-09-01 14:49:40') and coalesce(null,'9999-09-01 14:49:40') and coalesce(l.country,0)=coalesce(null,coalesce(l.country,0)) group by date_format(l.creation,'%Y-%M')"
	new_sales_details=frappe.db.sql(str1,debug=1)
	return{
		"order_total": new_sales_details
	}

@frappe.whitelist()
def get_data_newsalepie(from_date=None,to_date=None,country=None):
	if from_date:
		from_date=from_date[6:] + "-" + from_date[3:5] + "-" + from_date[:2]
	if to_date:
		to_date=to_date[6:] + "-" + to_date[3:5] + "-" + to_date[:2]
	if country:
		str1="select substring(date_format(creation,'%Y-%M'),1,8)as month,count(*) as lead_count from tabLead where creation between coalesce('"+from_date+"','1111-09-01 14:49:40') and coalesce('"+to_date+"','9999-09-01 14:49:40') and coalesce(country,0)=coalesce('"+country+"',coalesce(country,0)) group by date_format(creation,'%Y-%M')"	
	else:
		str1="""select substring(date_format(creation,'%Y-%M'),1,8)as month,count(*) as lead_count from tabLead where creation between coalesce('"+from_date+"','1111-09-01 14:49:40') and coalesce('"+to_date+"','9999-09-01 14:49:40') and coalesce(country,0)=coalesce(null,coalesce(country,0)) group by date_format(creation,'%Y-%M')"""
		
	if not from_date and not to_date and not country:
		str1="select substring(date_format(creation,'%Y-%M'),1,8)as month,count(*) as lead_count from tabLead where creation between coalesce(null,'1111-09-01 14:49:40') and coalesce(null,'9999-09-01 14:49:40') and coalesce(country,0)=coalesce(null,coalesce(country,0)) group by date_format(creation,'%Y-%M')"
	sales_details=frappe.db.sql(str1,debug=1)
	return{
		"order_total": sales_details
	}

@frappe.whitelist()
def get_pros(from_date=None,to_date=None,country=None):
	if from_date:
		from_date=from_date[6:] + "-" + from_date[3:5] + "-" + from_date[:2]
	if to_date:
		to_date=to_date[6:] + "-" + to_date[3:5] + "-" + to_date[:2]
	if not from_date and not to_date and not country:
		frappe.errprint("in the 1st")
		str2="""select substring(date_format(str_to_date(concat('01-',month,'-',year),'%d-%M-%Y'),'%Y-%M'),1,8) as month,sum(target_amount)as target_amount from ( SELECT  sp.name, td.fiscal_year, bdd.month, td.target_amount as  total_amount,bdd.percentage_allocation,(td.target_amount*bdd.percentage_allocation/100) as target_amount, (case when bdd.month in('January','February','March') then SUBSTRING_INDEX(SUBSTRING_INDEX(td.fiscal_year, '-', -1), ' ', -1)  else SUBSTRING_INDEX(SUBSTRING_INDEX(td.fiscal_year, '-', 1), ' ', -1) end) as year FROM `tabSales Person` sp,`tabTarget Detail`  td,`tabBudget Distribution` bd,`tabBudget Distribution Detail` bdd where sp.name=td.parent and td.target_distribution=bd.name and bdd.parent=bd.name and sp.country=coalesce(null,sp.country) )foo where date_format(str_to_date(concat('01-',month,'-',year),'%d-%M-%Y'),'%Y-%m') between coalesce(null,'2014-05-01') and coalesce(null,'2015-09-30') group by month"""
	elif country:
		frappe.errprint("in the country")
		str2="select substring(date_format(str_to_date(concat('01-',month,'-',year),'%d-%M-%Y'),'%Y-%M'),1,8) as month,sum(target_amount)as target_amount from ( SELECT  sp.name, td.fiscal_year, bdd.month, td.target_amount as  total_amount,bdd.percentage_allocation,(td.target_amount*bdd.percentage_allocation/100) as target_amount, (case when bdd.month in('January','February','March') then SUBSTRING_INDEX(SUBSTRING_INDEX(td.fiscal_year, '-', -1), ' ', -1)  else SUBSTRING_INDEX(SUBSTRING_INDEX(td.fiscal_year, '-', 1), ' ', -1) end) as year FROM `tabSales Person` sp,`tabTarget Detail`  td,`tabBudget Distribution` bd,`tabBudget Distribution Detail` bdd where sp.name=td.parent and td.target_distribution=bd.name and bdd.parent=bd.name and sp.country=coalesce('"+country+"',sp.country) )foo where date_format(str_to_date(concat('01-',month,'-',year),'%d-%M-%Y'),'%Y-%m') between coalesce(null,'2014-05-01') and coalesce(null,'2015-09-30') group by month"
	else:
		frappe.errprint("in the else")
		str2="select substring(date_format(expiry_date,'%Y-%M'),1,8)as month,count(*) as expiry_count from `tabSite Master` where expiry_date between coalesce('"+from_date+"','1111-09-01 14:49:40') and coalesce('"+to_date+"','9999-09-01 14:49:40') and coalesce(country,0)=coalesce(null,coalesce(country,0)) group by date_format(expiry_date,'%Y-%M')"
	# else:	
	subscription_details=frappe.db.sql(str2,debug=1)
	frappe.errprint(subscription_details)
	return{
		"order_total": subscription_details
	}

@frappe.whitelist()
def get_subscription(from_date=None,to_date=None,country=None):
	frappe.errprint("get_prospie")
	frappe.errprint(country)
	str2=''
	if from_date:
		from_date=from_date[6:] + "-" + from_date[3:5] + "-" + from_date[:2]
	if to_date:
		to_date=to_date[6:] + "-" + to_date[3:5] + "-" + to_date[:2]
	if not from_date and not to_date and not country:
		frappe.errprint("in the 1st")
		str2="""select substring(date_format(expiry_date,'%Y-%M'),1,8)as month,count(*) as expiry_count from `tabSite Master` where expiry_date between coalesce(null,'1111-09-01 14:49:40') and coalesce(null,'9999-09-01 14:49:40') and coalesce(country,0)=coalesce(null,coalesce(country,0)) group by date_format(expiry_date,'%Y-%M')"""			
	elif country:
		frappe.errprint("in the country")
		str2="select substring(date_format(expiry_date,'%Y-%M'),1,8)as month,count(*) as expiry_count from `tabSite Master` where expiry_date between coalesce('"+from_date+"','1111-09-01 14:49:40') and coalesce('"+to_date+"','9999-09-01 14:49:40') and coalesce(country,0)=coalesce('"+country+"',coalesce(country,0)) group by date_format(expiry_date,'%Y-%M')"
	else:
		frappe.errprint("in the else")
		str2="select substring(date_format(expiry_date,'%Y-%M'),1,8)as month,count(*) as expiry_count from `tabSite Master` where expiry_date between coalesce('"+from_date+"','1111-09-01 14:49:40') and coalesce('"+to_date+"','9999-09-01 14:49:40') and coalesce(country,0)=coalesce(null,coalesce(country,0)) group by date_format(expiry_date,'%Y-%M')"
	# else:	
	subscription_details=frappe.db.sql(str2,debug=1)
	frappe.errprint(subscription_details)
	return{
		"order_total": subscription_details
	}