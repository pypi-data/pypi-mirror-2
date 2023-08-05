/*
 * Multimedia Javascript for auslfe.portlet.multimedia 
 */

jQuery.auslfe_multimedia = {
    timeout: 30000
};

jq(document).ready(function() {
	
	/**
	 * A function for random sorting an array or aray-like object
	 */
	function randOrd(){
		return (Math.round(Math.random())-0.5);
	} 
	
	jq('.portletMultimedia .galleryMultimedia a').each(function() {
		jq(this).attr("href", "javascript:;").find("img").remove();
	});
	jq('.portletMultimedia').each(function(index) {
		var portlet = jq(this);
		var rnd = jq("span.random",portlet).length>0;
		var link = jq(".portletFooter a", portlet);
		// var timestamps = new Date().getTime();
		var images = null;
		
		function reorder(startHidden) {
			var startHidden = startHidden || false; 
			if (rnd) images.sort(randOrd);
			jq(".galleryMultimedia a", portlet).each(function(index) {
				var link = jq(this); 
				var curData = images[index];
				if (!curData.image)
					curData.image = jq('<img alt="'+curData.description+'" title="'+curData.title+'" src="'+curData.url+'/image_tile" '+(startHidden?' style="display:none"':'')+'/>')
				link.append(curData.image);
				link.attr("href", curData.url+"/image_view_fullscreen");
			});
		};
		
		jq.get(link.attr('href')+'/@@query_images', {}, function(data) {
			images = data;
			reorder();
			portlet.removeClass("hideFlag");
		}, dataType='json');
		
		// Client reload images?
		var client_reload = jq("span.client_reload",portlet).length>0;
		if (rnd && client_reload) {
			portlet.bind("imagesReload", function(event) {
				jq("img", portlet).fadeOut("fast", function() {
					jq("img", portlet).remove();
					reorder(true);
					jq("img", portlet).fadeIn("fast");
				});
			});
			setInterval(function() {
				portlet.trigger("imagesReload");
			}, jq.auslfe_multimedia.timeout);
		};
	});
});

