var PROJEKKTOR_CONFIG = {
    playerFlashMP4:'/playerMP4.swf',
    playerFlashMP3:'/playerMP3.swf',
    logoDelay:3,
};




(function( $ ){
    $.fn.ploneVideoProjekktor = function() {
	widget = $(this);
	var vLink = widget.find("a.projekktor-video-link");
	var vPoster = widget.find("img.projekktor-video-poster");
	var vMime = widget.find("span.projekktor-video-mimetype").html();
	var vWidth = vPoster.attr("width");
	var vHeight = vPoster.attr("height");		
	var vSrc = vLink.attr("href");
	var vPosterImg = vPoster.attr("src");
	var srcHtml = '<source src="'+vSrc+'" />';		
	widget.find(".projekktor-video-alternative").each(function(i) {
		srcHtml += '<source src="'+$(this).attr("href")+'" />';
	    });
	var vHtml = '<video class=\"plone-projekktor\" poster="'+vPosterImg+'" width="'+vWidth+'" height="'+vHeight+'" controls>'+srcHtml+'</video>';
	widget.html(vHtml);				
	proj = widget.find('video.plone-projekktor');
	new projekktor_player(proj).initialize()		
    },
    $.fn.ploneAudioProjekktor = function() 
	{
	    widget = $(this);
	    var vLink = widget.find("a.projekktor-audio-link");
	    var vPoster = widget.find("img.projekktor-audio-poster");
	    var vMime = widget.find("span.projekktor-audio-mimetype").html();
	    var vWidth = vPoster.attr("width");
	    var vHeight = vPoster.attr("height");		
	    var vSrc = vLink.attr("href");
	    var vPosterImg = vPoster.attr("src");
	    var srcHtml = '';
	    srcHtml += '<source src="'+vSrc+'"  />';
	    widget.find(".projekktor-audio-alternative").each(function(i) {
		    srcHtml += '<source src="'+$(this).attr("href")+'" />';
		});
	    var vHtml = '<audio class=\"plone-projekktor\" poster="'+vPosterImg+'" width="'+vWidth+'" height="'+vHeight+'" controls>'+srcHtml+'</audio>';
	    widget.html(vHtml);				
	    proj = widget.find('audio.plone-projekktor');
	    new projekktor_player(proj).initialize()
	}
})( jQuery );


var loadProjekktor = function () 
{
    $(".projekktor-video-widget").ploneVideoProjekktor();
    $(".projekktor-audio-widget").ploneAudioProjekktor();
};

$(document).ready(loadProjekktor);
