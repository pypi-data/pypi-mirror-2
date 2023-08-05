var imgSrcs = [];
var curSrc = 0;

var frontFrame;
var backFrame;

var fadeSpeed;
var imageTimeout;

// image class
function img(src, alt)
{
	this.src = src;
	this.alt = alt;
}

jQuery.fn.bannerrotator = function(xmlFile, settings)
{
	var banner = this;
	settings = jQuery.extend({
		fade: 6000,
		timeout: 10000
	}, settings);

	fadeSpeed = settings.fade;
	imageTimeout = settings.timeout;

	// load image sources
	jQuery.get(xmlFile, function(xml)
	{
		var i = 0;
		
		// iterate xml
		jQuery(xml).find('image').each(function()
		{
			var node = jQuery(this);
			
			// append image to array
			imgSrcs[i++] = new img(node.attr('src'), node.attr('alt'));
		});

		// make sure there are at least 2 elements
		if (imgSrcs.length < 2) return;

		// only create element if it's not already there
		if (banner.length == 1) banner.append(document.createElement('img'));

		// get array of img elements to swap
		var imgs = banner.find("img");
		frontFrame = imgs[1];
		backFrame = imgs[0];

		// start toggling!
		toggleBanner();
	});
};
	
function toggleBanner()
{
	// move to next image
	if (++curSrc >= imgSrcs.length) curSrc = 0;

	// swap frames
	var temp = frontFrame;
	frontFrame = backFrame;
	backFrame = temp;
		
	// set current image to hide next
	frontFrame.className = "";
	frontFrame.removeAttribute('style');

	// prepare to swap image
	backFrame.className = "show";
	backFrame.src = imgSrcs[curSrc].src;
	backFrame.alt = imgSrcs[curSrc].alt;

	// fade in next image and repeat
	setTimeout(function() { jQuery(backFrame).fadeIn(fadeSpeed, toggleBanner); }, imageTimeout);	
}