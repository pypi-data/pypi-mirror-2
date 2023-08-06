/*
    Set up the Structure overlay
*/

/*jslint white:false, onevar:true, undef:true, nomen:true, eqeqeq:true,
  plusplus:true, bitwise:true, regexp:true, newcap:true, immed:true,
  strict:false, browser:true */
/*global jQuery:false, document:false, window:false, location:false */

jQuery(function ($) {

    // set an initial history state
    var overlay_location = $('#structure a').attr('href'),
        slideTo;

    window.parent.history.replaceState({structure_href: overlay_location}, null, window.parent.location.href);

    positionPrimaryActions = function(){
        var actions = $('#primary-actions');
        actions.css('left', ($('#listing-table').width() - actions.width()) + 'px');
        actions.fadeIn();
    }

    // animate navigation to a new folder
    slideTo = function(href, dir) {
        if(overlay_location === href){
            return;
        }
        var $slider = $('.structure-slider'),
            width = $slider.outerWidth();

        $(window).trigger('structureStartSlideTo', [this, $slider, href, dir]);

        $('#structure-dialog').css({height: $slider.outerHeight()});
        $('<div class="structure-slider" style="width: 100%"><' + '/div>')
            .prependTo($('#structure-dialog'))
            .loadOverlay(href + ' .structure-slider>*', undefined, function(){
                $slider.remove();
                })
            .css({position: 'absolute', left: (dir === 'left'?width:-width), top: 0})
            .animate({left: 0}, 400, 'swing', function() {
                $('.structure-slider').css('position', 'static');
                $('#structure-dialog').css('height', 'auto');
                });
        $slider
            .css('position', 'relative')
            .animate({'left': (dir === 'left')?-width:width}, 400, 'swing', function(){
                $(document).trigger('structureEndSlideTo', [this, $slider, href, dir]);
                });
        overlay_location = href;
    };

    $(document).bind('structureEndSlideTo', function(){ 
        $("table.orderable").ploneDnD(); 
        positionPrimaryActions();
    });
    $(document).bind('endLoadOverlay', function(){ $("table.orderable").ploneDnD(); });
    $(document).bind('loadOverlay', function(){ 
        $("table.orderable").ploneDnD(); 
        positionPrimaryActions();
    });
    $(document).bind('formOverlayLoadSuccess', function(){ $("table.orderable").ploneDnD(); });

    /* current item actions need to be specially handled */
    $("a#structure-btn-cut,a#structure-btn-copy", $('#item-actions-menu')).live('click', function(e){
        $.ajax({
            url : $(this).attr('href'),
            complete : function(request, textStatus){
                $.plone.showNotifyFromElements(request.responseText);
            },
            type : 'POST'
        });
        return e.preventDefault();
    });


    // trigger navigation into child folders
    $('#structure-dialog a.link-child').live('click', function(e) {
        var href = $(this).attr('href');
        slideTo(href, 'left');
        window.parent.history.pushState({structure_href: href}, null, window.parent.location.href);
        return e.preventDefault();
    });

    // trigger navigation from breadcrumbs
    $('#structure-dialog a.link-parent').live('click', function(e) {
        var href = $(this).attr('href');
        slideTo(href, 'right');
        window.parent.history.pushState({structure_href: href}, null, window.parent.location.href);
        return e.preventDefault();
    });

    // update current folder after back/forward history navigation
    // XXX: Check this! addEventListner isn't support in IE < 9
    window.parent.addEventListener('popstate', function(e) {
        if (e.state !== null && e.state.structure_href !== undefined) {
            var href = e.state.structure_href;
            slideTo(href, (overlay_location.length > href.length ? 'right' : 'left'));
        }
    }, false);

});
