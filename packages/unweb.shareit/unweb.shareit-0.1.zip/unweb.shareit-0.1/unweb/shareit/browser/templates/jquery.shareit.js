/*
 * ShareIt - jQuery Plugin
 * Share content on facebook and iwiw
 *
 * Author: Matyas Juhasz
 * Documentation: http://joohi.hu/shareit
 * No license. Use it however you want. Just keep this notice included.
 *
 * Version: 1.0.2 (2010-07-09)
 * Requires: jQuery v1.3+
 *
 */

(function($) {
  $.fn.extend({
    shareIt: function(givenOptions) {
        var self = $(this),
            options = $.extend({
              title: "Share this page",
              twitter_icon: "++resource++unweb.shareit.images/twitter.gif.ico",
              facebook_icon: "++resource++unweb.shareit.images/facebook.png",
              iwiw_icon: "++resource++unweb.shareit.images/iwiw.png",
              delicious_icon: "++resource++unweb.shareit.images/delicious.gif",
              digg_icon: "++resource++unweb.shareit.images/digg.gif",
              koprol_icon: "++resource++unweb.shareit.images/koprol.png",
              orkut_icon: "++resource++unweb.shareit.images/orkut.png",
              icons: [],
              twitter: true,
              facebook: true,
              delicious: true,
              digg: false,
              koprol: true,
              orkut: true
            }, givenOptions);

        var shareitbox;

        function showShareBox() {
          $("body").append(
            shareitbox = $('<div id="shareit-box" class="shareit-box"></div>')
          );

          shareitbox.css("left", $(self).offset().left+"px");
          shareitbox.css("top", $(self).offset().top+$(self).height()+6+"px");

          if (options.twitter)
            shareitbox.append(twitter_button = '<a href="http://twitter.com/home?status='+document.title.replace(/ /g, '+')+'+'+document.location+'" target="_blank" title="twitter"><img src="'+options.twitter_icon+'" /></a>');
          if (options.facebook)
            shareitbox.append(facebook_button = '<a href="http://www.facebook.com/sharer.php?u='+document.location+'&t='+document.title.replace(/ /g, '+')+'" target="_blank" title="facebook""><img src="'+options.facebook_icon+'" /></a>');
          if (options.delicious)
            shareitbox.append(delicious_button = '<a href="http://del.icio.us/post?url='+document.location+'&title='+document.title.replace(/ /g, '+')+'" target="_blank" title="delicious"><img src="'+options.delicious_icon+'" /></a>');
          if (options.orkut)
            shareitbox.append(orkut_button = '<a href="http://promote.orkut.com/preview?nt=orkut.com&tt='+document.title.replace(/ /g, '+')+'&du='+document.location+'" target="_blank" title="orkut"><img src="'+options.orkut_icon+'" /></a>');
          if (options.digg)
            shareitbox.append(digg_button = '<a href="http://digg.com/submit?phase=2&url='+document.location+'&title='+document.title.replace(/ /g, '+')+'" target="_blank" title="digg"><img src="'+options.digg_icon+'" /></a>');


          $(options.icons).each(function() {
            shareitbox.append('<a href="'+this[0]+'" target="_blank"><img src="'+this[1]+'" /></a>');
          });

          $("*").bind("click.shareit", function() {
            $(".shareit-box").remove();
            $("*").unbind("click.shareit");
          });

        }

        function doIt() {
          self.click(function() {
            showShareBox();
            return false;
          });
        }
        doIt();
    }
  });
})(jQuery);


$(document).ready(function() {
  jq("#document-action-share a").shareIt();
});

/* Jquery alternative to use a template and an overlay
$(function(){$('#document-action-share a').prepOverlay({
    subtype:'ajax',
    urlmatch:'$',urlreplace:' #content > *'
    })});
*/
