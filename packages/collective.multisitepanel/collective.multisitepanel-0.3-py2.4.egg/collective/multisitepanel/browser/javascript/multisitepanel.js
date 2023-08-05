jq(document).ready(function() {	
	jq('.product-link').click(function (e){
		e.preventDefault();
		productId = jq(this).attr('id');
        jq('#fieldsetlegend-details').click();
		window.scrollTo(0, jq('a[@name="'+productId+'"]').position().top);
	});
	jq('table.multisitepanel_table').tableHover({colClass: 'highlighted',
                                                 rowClass: 'highlighted',
                                                 clickClass: 'msp_click',
                                                 ignoreCols: [1],})

});