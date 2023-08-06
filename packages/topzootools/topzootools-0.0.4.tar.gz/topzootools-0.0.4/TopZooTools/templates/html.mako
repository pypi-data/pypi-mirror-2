<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html>  
<head>
	<title>The Internet Topology Zoo</title>           
	
<style type="text/css">   
	
	body
	{
	font-family:verdana,helvetica,arial,sans-serif;
	}
	
	table, td, th
	{
	border:1px dotted #778899;         
	border-collapse:collapse;
	padding:4px 7px 4px 7px;	 
	font-size: small;
	}
	th
	{
	background-color:#778899;
	color:white;   
	font-weight:bold;  
	border:1px solid black;         
	}           
	
	tr td
	{
	background-color:#eeeeee;
	}
	
    tr.alt td 
	{
	color:#000000;
	background-color:#dddddd;
	}
	 
</style>
	
</head>   

<body>         
	
	<h1>The Internet Topology Zoo</h1>
	
<table id="networks">               
<tr>      
	% for name in metadata_headings:       
	<%          
	# Nicer column names
	column_names = {
		"GeoExtent": "Geo Extent",
		"GeoLocation": "Geo Location", 
		"LastAccess": "Last Access",
		"DateObtained": "Date Obtained",
		"NetworkDate": "Network Date",
		} 
	if name in column_names:     
		# replace with nicer name
		name = column_names[name]
	%>
	<th>${name}</th>
	%endfor 
</tr>         
<% index = 0 %>
% for name, data in sorted(html_data.items(), key=lambda x: (x[1]['Type'], x[1]['Network'].lower()) ):
% if index%2 == 0:     
<tr>\
%else:   
<tr class="alt">\
%endif  
<% index += 1 %>\
%for name in metadata_headings:    
%if name in data:      
<%
value = data[name]
if name == "Source":
	value = '<a href="' + value + '">Link</a>'
elif name == "Classification":
	value = value.replace("Backbone", "Back")    
	value = value.replace("Transit", "Tran")
	value = value.replace("Customer", "Cust")       
	value = value.replace("Access", "Acce") 
	value = value.replace("Testbed", "Test")
%>         
   <td>${value}</td>\
%endif
%endfor                  

</tr>    

%endfor        
 
</table>       
</body>

</html>                                            
