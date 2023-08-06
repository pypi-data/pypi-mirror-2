## coding: utf-8
<%inherit file="layout.mako"/>

<%def name="extrahead()">
    <link rel="stylesheet" href="${pathto('_static/AnythingSlider/css/page.css', 1)}" type="text/css" media="screen" />
    <link rel="stylesheet" href="${pathto('_static/AnythingSlider/css/slider.css', 1)}" type="text/css" media="screen" />
    
    <script type="text/javascript" src="${pathto('_static/AnythingSlider/js/jquery.easing.1.2.js', 1)}"></script>
    <script type="text/javascript" src="${pathto('_static/AnythingSlider/js/jquery.anythingslider.js', 1)}"></script>

    <script type="text/javascript">
        function formatText(index, panel) {
		  return index + "";
	    }
    
        $(function () {
        
            $('.anythingSlider').anythingSlider({
                easing: "easeInOutExpo",        // Anything other than "linear" or "swing" requires the easing plugin
                autoPlay: true,                 // This turns off the entire FUNCTIONALY, not just if it starts running or not.
                delay: 8000,                    // How long between slide transitions in AutoPlay mode
                startStopped: false,            // If autoPlay is on, this can force it to start stopped
                animationTime: 600,             // How long the slide transition takes
                hashTags: true,                 // Should links change the hashtag in the URL?
                buildNavigation: false,          // If true, builds and list of anchor links to link to each slide
        	pauseOnHover: true,             // If true, and autoPlay is enabled, the show will pause on hover
        	startText: "",             // Start text
		stopText: "",               // Stop text
		navigationFormatter: formatText       // Details at the top of the file on this use (advanced use)
            });
            
        });
    </script>
</%def>
<%def name="related()"></%def>

${next.body()}
