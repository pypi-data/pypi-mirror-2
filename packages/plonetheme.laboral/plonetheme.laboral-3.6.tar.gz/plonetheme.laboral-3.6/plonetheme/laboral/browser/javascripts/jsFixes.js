LaboralJsFixes = {};

LaboralJsFixes.fixCaptions = function ()
{
	var leadimage = jq(".newsImageContainer a img");
	var width = leadimage.width();
	jq(".newsImageContainer p").css({'max-width' : width});
};

LaboralJsFixes.fixSquareThumbnails = function ()
{
	jq(".relatedImage").each(function ()
	{
		var image = jq(this);
		var width = image.width(); //get image width
		var height = image.height(); //get image height
		
		image.css({
			'margin-top': '-'+height/2+'px',
			'margin-left': '-'+width/2+'px',
			'top' : '50%',
			'left' : '50%',
			'position':'relative',
			'display':'block'});
	});
};

LaboralJsFixes.extendThumbnailStructure = function ()
{
	jq(".relatedImage").each(function ()
	{
		if(jq(this).parent().attr('class') != 'collectionImage')
		{
			jq(this).wrap('<div class="collectionImage" />');
		}
	});
}

LaboralJsFixes.fixShareButtonsHoverState = function ()
{
	jq(".addthis_toolbox a").each(function() {
		jq(this).mouseenter(function(){
			jq(this).find(".shareButton").hide();
			jq(this).find(".shareButtonHover").show();
		});
		jq(this).mouseleave(function() {
			jq(this).find(".shareButtonHover").hide();
			jq(this).find(".shareButton").show();
		});
	});
}

LaboralJsFixes.hideZeroShareCount = function ()
{
	jq('.addthis_button_expanded').each(function(){
		if(jq(this).text() == "0")
		{
			jq(this).hide();
		}
	});
}

LaboralJsFixes.runFixes = function ()
{
	//Add new fixes to this list to activate them
	//LaboralJsFixes.extendThumbnailStructure();
	LaboralJsFixes.fixShareButtonsHoverState();
	LaboralJsFixes.fixCaptions();
};


LaboralJsFixes.runSpecialFixes = function ()
{
	//Add new fixes to this list to activate them and ONLY RUN WHEN THE FULL PAGE IS LOADED
	//LaboralJsFixes.fixSquareThumbnails();
	LaboralJsFixes.hideZeroShareCount();
};

//run all the fixes when the DOM is completely loaded and the special ones when everything is loaded;
jq(window).load(function () {LaboralJsFixes.runSpecialFixes();});
jq(document).ready(function () {LaboralJsFixes.runFixes();}); 
