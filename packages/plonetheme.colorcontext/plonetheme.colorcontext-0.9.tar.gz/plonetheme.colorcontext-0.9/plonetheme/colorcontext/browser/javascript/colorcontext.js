/*javascript document*/

ColorContext = {};

ColorContext.languageSelectors = function()
{
	var elems = jq("#portal-languageselector li").click(function(){window.location = jq(this).find('a').attr('href');});
};

ColorContext.fixWidth = function()
{
	columnCount = jq("#portal-columns>tbody>tr>td").length;
	if(columnCount == 1)
	{
		jq("#portal-column-content").css('width', '979px');
	}
};

ColorContext.fixSquareThumbnails = function ()
{
	jq(".album_image").each(function ()
	{
		var image = jq(this).find("img:first-child");
		var width = image.width(); //get image width
		var height = image.height(); //get image height
		
		image.css({'margin-top': '-'+height/2+'px', 'margin-left': '-'+width/2+'px', 'top' : '50%', 'left' : '50%', 'position':'relative','display':'block'});
	});
};

ColorContext.fixCaptions = function ()
{
	var leadimage = jq(".newsImageContainer a img");
	var width = leadimage.width();
	jq(".newsImageContainer p").css({'max-width' : width});
};


ColorContext.runFixes = function ()
{
	//Add new fixes to this list to activate them.
	ColorContext.fixWidth();
	ColorContext.languageSelectors();
	ColorContext.fixCaptions();
};

ColorContext.runSpecialFixes = function ()
{
	//Add new fixes to this list to activate them and ONLY RUN WHEN THE FULL PAGE IS LOADED
	ColorContext.fixSquareThumbnails();
};

//run all the fixes when the DOM is completely loaded and the special ones when everything is loaded;
jq(window).load(function () {ColorContext.runSpecialFixes();});
jq(document).ready(function () {ColorContext.runFixes();}); 

