function slideShow(target, interval, repeat, links) {
    var running = true;
    var timer;
    
    // Speeds can be "fast", "slow", or a numerical value (in milliseconds).
    // Set to 0 to disable the effect.
    var imageShowSpeed = "slow";
    var imageHideSpeed = "slow";
    var captionShowSpeed = "slow";
    var captionHideSpeed = "fast";

    (function($) {
        //append a LI item to the UL list for displaying caption
        caption = $('<li class="caption slideshow-caption"><div class="slideshow-caption-container"><h3></h3><p></p></div></li>');
        if(links)
            $('div', caption).append('<a class="read-more" href="">Read More</a>');
        $('ul.slideshow', target).append(caption);

        //Hide all slideshow images
        $('.slideshow-image', target).hide();
        
        //Get the first image and display it (set it to full opacity)
        first = $('.slideshow-image:first', target)
        first.addClass('show').show();
        
        //Get the caption of the first image from REL attribute and display it
        $('.slideshow-caption', target)
            .find('h3').html($('img', first).attr('title'))
            .find('p').html($('img', first).attr('alt'));
        if(links)    
            $('.slideshow-caption a', target).attr('href', $('a'. first).attr('href'));
        
        var gallery = function() {
            var current = $('.slideshow-image.show', target);
            //Get next image, if it reached the end of the slideshow, rotate it back to the first image
            var next = current.next('.slideshow-image');
            if (next.length == 0){
                if(repeat) {
                    next = $('.slideshow-image:first', target);
                } else {
                    running = false;
                    return;
                }
            }
            
            //Get next image caption
            var title = $('img', next).attr('title');
            var desc = $('img', next).attr('alt');
            var href = links ? $('a', next).attr('href') : '';
            
            //Set the fade in effect for the next image, show class has higher z-index
            next.fadeIn(imageShowSpeed).addClass('show');
            
            //Hide the caption first, and then set and display the caption
            $('.slideshow-caption', target).slideUp(captionHideSpeed, function () {
                $('h3', this).html(title);
                $('p', this).html(desc);
                if(links)
                    $('a', this).attr('href', href);
                $(this).slideDown(captionShowSpeed);
            });
            
            //Hide the current image
            current.fadeOut(imageHideSpeed).removeClass('show');
            timer = setTimeout(gallery, interval);
        };
        
        //Call the gallery function to run the slideshow
        timer = setTimeout(gallery, interval);
        
        //pause the slideshow on mouse over
        $('ul.slideshow', target).hover(
            function () {
                if(running)
                    clearTimeout(timer);
            },
            function () {
                if(running)
                    timer = setTimeout(gallery, interval);
            }
        );
    })(jQuery);

}
