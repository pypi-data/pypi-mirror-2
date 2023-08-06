%if archive_file:    
	<a href="files/${archive_file}">Download</a> as a zip archive.    
	<p><br>
%endif
	                                         
	<table id="networks" class="tablesorter">     
		<thead>           
			<tr>    
				<th>Network</th>    
				<th>Type</th>
				<th>Geo Extent</th>
				<th>Geo Location</th>         
				<th>Classification</th>
				<th>Layer</th>   
				<th>Network Date</th>  
				<th>Download</th>
				<th>Source</th>     
				<th>Comments</th>
			</tr>       
		</thead>                    
		<tbody>   
		%for name, data in sorted(html_data.items()):    
			<tr>             
				<td>${name}</td>       
				<td>${data['Type']}</td>       
				<td>${data['GeoExtent']}</td>  
				<td>${data['GeoLocation']}</td>   
				<td>${data['Classification']}</td>
				<td>${data['Layer']}</td>
				<td>${data['NetworkDate']}</td>     
				<td><a href="files/${name}.gml">GML</a> <a href="files/${name}.graphml">GraphML</a></td>
				<td><a href="${data['Source']}">Link</a></td>       
				<td>${data['Note']}</td>
			</tr>    
		%endfor        
		</tbody>           
	</table>              

                
	<% net_count = len(html_data)%>
	${net_count} Networks
	<br>
	Updated ${date}       
                                        
