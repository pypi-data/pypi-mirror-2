JsFixes = {};

JsFixes.fixSquareThumbnails = function ()
{
	jq(".relatedImage").each(function ()
	{
		var image = jq(this);
		var width = image.width(); //get image width
		var height = image.height(); //get image height
		
		image.css({'margin-top': '-'+height/2+'px', 'margin-left': '-'+width/2+'px', 'top' : '50%', 'left' : '50%', 'position':'relative','display':'block'});
	});
};

JsFixes.runFixes = function ()
{
	//Add new fixes to this list to activate them.
};


JsFixes.runSpecialFixes = function ()
{
	//Add new fixes to this list to activate them and ONLY RUN WHEN THE FULL PAGE IS LOADED
	//JsFixes.fixSquareThumbnails();
};

//run all the fixes when the DOM is completely loaded and the special ones when everything is loaded;
jq(window).load(function () {JsFixes.runSpecialFixes();});
jq(document).ready(function () {JsFixes.runFixes();}); 
