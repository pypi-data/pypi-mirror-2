(function($){
    $.fn.imagesLoaded = function(callback){
      var elems = this.filter('img'),
          len   = elems.length;

      elems.bind('load',function(){
          if (--len <= 0){ callback.call(elems,this); }
      }).each(function(){
         // cached images don't fire load sometimes, so we reset src.
         if (this.complete || this.complete === undefined){
            var src = this.src;
            // webkit hack from http://groups.google.com/group/jquery-dev/browse_thread/thread/eee6ab7b2da50e1f
            this.src = '#';
            this.src = src;
         }  
      }); 
    };
    
    var timeout_id = 0;
    var active = false;
    
    function set_controls_position(container){
        var width = container.find('img').width();
        var left = (width/2) - 43;
        container.find('div.gallery-portlet-controls').css("left", left);
    }
    
    function get_image(link){
        if(active){
            return;
        }
        active = true;
        var container = link.parents('dl.applied-portlet-gallery');
        var controls = link.parents('div.gallery-portlet-controls');
        var portlet_item = link.parents('dd.portletItem');
        var next = controls.find('span.next a');
        var prev = controls.find('span.prev a');        
        var img = container.find('img');
        
        $.ajax({
            url : '@@get-image-for-gallery-portlet',
            data : link.attr('href').split('?')[1],
            type : 'GET',
            success : function(data, results){
                eval("var json="+data);
                //create new image now so it'll be done loading faster...
                var newimg = document.createElement('img');
                newimg.src = json.src;
                newimg.width = img.width();
                newimg = $(newimg);
                newimg.css('display', 'none');
                portlet_item.css('height', img.height());
                
                img.fadeOut(1000, function(){
                    img.replaceWith(newimg);
                    
                    newimg.imagesLoaded(function(){
                        portlet_item.animate({ height : $(this).height() }, 500, 'linear');
                        $(this).fadeIn(1000, function(){
                            active = false;
                        });
                    }, newimg)
                    
                    newimg.parent().attr('href', json['image-link']);
                    next.attr('href', next.attr('href').split('?')[0] + '?' + json['next-url']);
                    prev.attr('href', prev.attr('href').split('?')[0] + '?' + json['prev-url']);
                    set_controls_position(container);
                });
            }
        });
    }
    
    
    function perform_play(portlet){
        portlet.find('span.next a').trigger('click');
        timeout_id = setTimeout(function(){perform_play(portlet);}, 5000);
    }   
     
    function play(portlet){
        portlet.addClass('timed');
        portlet.find('span.play-pause').addClass('timed');
        timeout_id = setTimeout(function(){perform_play(portlet);}, 5000);
    }
    
    function pause(portlet){
        clearTimeout(timeout_id);
        portlet.removeClass('timed');
        portlet.find('span.play-pause').removeClass('timed');
    }
    
    $(document).ready(function(){
        
        $('dl.portletGallery span.next a,dl.portletGallery span.prev a').click(function(){
            get_image($(this));
            return false;
        });
        
        $('dl.portletGallery span.play-pause').css({'display':'inline'});
        
        var portlets = $('dl.portletGallery');
        portlets.addClass('applied-portlet-gallery');
        
        portlets.each(function(){
            var portlet = $(this);
            set_controls_position(portlet);
            if(portlet.hasClass('timed')){
                play(portlet);
            }else{
                pause(portlet);
            }
        });
        
        $('dl.portletGallery span.play-pause a').click(function(){
            var portlet = $(this).parent().parent().parent();
            if(portlet.hasClass('timed')){
                pause(portlet);
            }else{
                play(portlet);
            }
            return false;
        });
        
        $('dl.portletGallery').hover(
            function(){
                var controls = $(this).find('div.gallery-portlet-controls');
                controls.fadeIn();
            },
            function(){
                var controls = $(this).find('div.gallery-portlet-controls');
                controls.fadeOut();
            }
        );
    });
})(jQuery);