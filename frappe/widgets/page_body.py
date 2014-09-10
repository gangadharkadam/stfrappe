# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt 

from __future__ import unicode_literals
redirect_template = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
<head>
<title>%s</title>
<meta http-equiv="REFRESH" content="0; url=%s"></HEAD>
<BODY style="font-family: Arial; padding: 8px; font-size: 14px; margin: 0px;">
Redirecting...
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
  ga('create', 'UA-54550495-1', 'auto');
  ga('send', 'pageview');
</script>
</BODY>
</HTML>'''