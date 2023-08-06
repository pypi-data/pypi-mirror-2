/*javascript document*/

CultureCab = {};

CultureCab.languageSelectors = function()
{
	var elems = jq("#portal-languageselector li").click(function(){window.location = jq(this).find('a').attr('href');});
};

CultureCab.fixWidth = function()
{
	columnCount = jq("#portal-columns>tbody>tr>td").length;
	if(columnCount > 1)
	{
		jq(".downloadPortlet").remove();
	}
};

CultureCab.fixSquareThumbnails = function ()
{
	jq(".album_image").each(function ()
	{
		var image = jq(this).find("img:first-child");
		var width = image.width(); //get image width
		var height = image.height(); //get image height
		
		image.css({'margin-top': '-'+height/2+'px', 'margin-left': '-'+width/2+'px', 'top' : '50%', 'left' : '50%', 'position':'relative','display':'block'});
	});
};

CultureCab.fixCaptions = function ()
{
	var leadimage = jq(".newsImageContainer a img");
	var width = leadimage.width();
	jq(".newsImageContainer p").css({'max-width' : width});
};


CultureCab.runFixes = function ()
{
	//Add new fixes to this list to activate them.
	CultureCab.fixWidth();
	//CultureCab.fixCaptions();
};

CultureCab.runSpecialFixes = function ()
{
	//Add new fixes to this list to activate them and ONLY RUN WHEN THE FULL PAGE IS LOADED
	//CultureCab.fixSquareThumbnails();
};

//run all the fixes when the DOM is completely loaded and the special ones when everything is loaded;
jq(window).load(function () {CultureCab.runSpecialFixes();});
jq(document).ready(function () {CultureCab.runFixes();}); 

