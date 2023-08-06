jq(document).ready(function() {

    jq(".template-gallery_view .photoAlbumEntry a").not(".template-gallery_view .photoAlbumFolder a").xhostplusbox({
        'titleShow'     : true,
        'transitionIn'  : 'elastic',
        'transitionOut' : 'elastic'
    });


    jq(".portletGallery .portletItem a").xhostplusbox({
        'titleShow'     : true,
        'transitionIn'  : 'elastic',
        'transitionOut' : 'elastic'
    });
})