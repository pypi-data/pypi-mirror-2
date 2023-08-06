LaboralJsFixes = {};

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

LaboralJsFixes.runFixes = function ()
{
	//Add new fixes to this list to activate them
	//LaboralJsFixes.extendThumbnailStructure();
};


LaboralJsFixes.runSpecialFixes = function ()
{
	//Add new fixes to this list to activate them and ONLY RUN WHEN THE FULL PAGE IS LOADED
	//LaboralJsFixes.fixSquareThumbnails();
};

//run all the fixes when the DOM is completely loaded and the special ones when everything is loaded;
jq(window).load(function () {LaboralJsFixes.runSpecialFixes();});
jq(document).ready(function () {LaboralJsFixes.runFixes();}); 
