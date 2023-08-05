(function($){
  $.extend({
    jGFeedContextual : function(url, fnk, container, num){
      // Make sure url to get is defined
      if(url == null) return false;
      // Build Google Feed API URL
      var gurl = "http://ajax.googleapis.com/ajax/services/feed/load?v=1.0&callback=?&q="+url;
      if(num != null) gurl += "&num="+num;
      // AJAX request the API
      $.getJSON(gurl, function(data){
        if(typeof fnk == 'function')
		  fnk.call(this, container, data.responseData.feed);
		else
		  return false;
      });
    }
  });
})(jQuery);

$(document).ready(function() {
  $("dl.portletRss").each(function(el) {
    feed_url = $(this).find("a.portletRssFeedMoreLink").attr("href");
    count = $(this).find("a.portletRssFeedMoreLink").attr("count");
    $.jGFeedContextual(feed_url,
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
        // do whatever you want with feeds here
        for(var i=0; i<feeds.entries.length; i++){
          var entry = feeds.entries[i];
          $("<dd class='portletItem'>").insertBefore(more_link_elem.parent());
          $("<a class='tile' href='" + entry.link + "'>" + entry.title + "</a>").insertBefore(more_link_elem.parent());
          $("</dd>").insertBefore(more_link_elem.parent());
        }

        more_link_elem.attr("href", feeds.link);
    }, $(this), count);
  });
});
