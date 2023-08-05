jQuery.noConflict();
(function(jQuery){
  jQuery.extend({
    jGFeedContextual : function(url, fnk, container, num){
      // Make sure url to get is defined
      if(url == null) return false;
      // Build Google Feed API URL
      var gurl = "http://ajax.googleapis.com/ajax/services/feed/load?v=1.0&callback=?&q="+url;
      if(num != null) gurl += "&num="+num;
      // AJAX request the API
      jQuery.getJSON(gurl, function(data){
        if(typeof fnk == 'function')
		  fnk.call(this, container, data.responseData.feed);
		else
		  return false;
      });
    }
  });
})(jQuery);

jQuery(document).ready(function() {
  jQuery("dl.portletRss").each(function(el) {
    feed_url = jQuery(this).find("a.portletRssFeedMoreLink").attr("href");
    count = jQuery(this).find("a.portletRssFeedMoreLink").attr("count");
    jQuery.jGFeedContextual(feed_url,
      function(container, feeds){
        // Check for errors
        if(!feeds){
          // there was an error
          return false;
        }
        header_link_elem = container.find("a.portletRssFeedHeaderLink");
        customtitle = header_link_elem.attr("customtitle")
        if(customtitle == 'no'){
          header_link_elem.html(feeds.title);
        }
        more_link_elem = container.find("a.portletRssFeedMoreLink");
        for(var i=0; i<feeds.entries.length; i++){
          var entry = feeds.entries[i];
          var pubdate = new Date(entry.publishedDate);
          if(pubdate == "Invalid Date"){
              pubdate = "";
          }else{
              pubdate = pubdate.toLocaleDateString();
          };
          if((i+1)%2 == 0){
            jQuery("<dd class='portletItem even'><a class='tile' href='" + entry.link + "'>" + entry.title + "</a><span class='portletItemDetails'>" + pubdate + "</span></dd>").insertBefore(more_link_elem.parent());
          }else{
            jQuery("<dd class='portletItem odd'><a class='tile' href='" + entry.link + "'>" + entry.title + "</a><span class='portletItemDetails'>" + pubdate + "</span></dd>").insertBefore(more_link_elem.parent());
          };
        }
        more_link_elem.attr("href", feeds.link);
    }, jQuery(this), count);
  });
});
