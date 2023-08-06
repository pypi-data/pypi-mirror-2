jq(document).ready(function() {
    var start_slideshow_buttons = jq(".template-gallery_view .xhostplusGalleryStartSlideshow");
    var slideshow_interval_time = parseInt(jq("#xhostplus_gallery_slideshow_interval").html()) * 1000;
    var slideshow_interval = null;

    var gallery_elements = jq(".template-gallery_view .photoAlbumEntry a").not(".template-gallery_view .photoAlbumFolder a");
    var portlet_elements = jq(".portletGallery .portletItem a");

    gallery_elements.xhostplusbox({
        'titleShow'     : true,
        'transitionIn'  : 'elastic',
        'transitionOut' : 'elastic',
        'cyclic'        : true,
        'onClosed'      : function() {
            if(slideshow_interval)
                window.clearInterval(slideshow_interval);
            slideshow_interval = null;
            jq("#xhostplusbox-left, #xhostplusbox-right").css({
                'visibility' : 'visible'
            });
        }
    });

    portlet_elements.xhostplusbox({
        'titleShow'     : true,
        'transitionIn'  : 'elastic',
        'transitionOut' : 'elastic'
    });

    start_slideshow_buttons.click(function() {
        jq("#xhostplusbox-left, #xhostplusbox-right").css({
            'visibility' : 'hidden'
        });
        gallery_elements.first().trigger('click');
        slideshow_interval = window.setInterval($.xhostplusbox.next, slideshow_interval_time);
        return false;
    });
});