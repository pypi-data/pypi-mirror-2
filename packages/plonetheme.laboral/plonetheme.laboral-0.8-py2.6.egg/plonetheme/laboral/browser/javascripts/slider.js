/* Javascript for the related content slider */

RelSlider = {};

RelSlider.slides = [];
RelSlider.ids = [];
RelSlider.current = 0;
RelSlider.numSlides = 0;
RelSlider.currentAnchor = "not set";

RelSlider.getNumberOfSlides = function()
{
    if(RelSlider.numSlides == 0)
    {
        RelSlider.numSlides = jq('.slider-item').get().length;
        return RelSlider.numSlides;
    }
    else
    {
        return RelSlider.numSlides;
    }
}

RelSlider.getSliderElement = function ()
{
    return jq('.slider');
};

RelSlider.loadImages = function ()
{
    jq(jq('.slider-item-image-link').get().reverse()).each(function(){
        var link = jq(this);
        var url = link.attr('href');
        var img = new Image();
        jq(img)
            .addClass('slider-item-image')
            .load(function (){
                link.parent().prepend(jq(this));
                link.remove();
                if(jq(this).height() > 0)
                {
                    jq(this).css({'top': 225 - jq(this).height()/2, 'left': 300 - jq(this).width()/2});
                }
            })
            .attr('src', url);
    });
};

RelSlider.gotoSlide = function (num)
{
    if(num >= 0 && num < RelSlider.numSlides)
    {
        jq(RelSlider.slides[num]).show();
        jq(RelSlider.slides[num]).children(".slider-item-image").css({'top': 225 - jq(RelSlider.slides[num]).children(".slider-item-image").height()/2, 'left': 300 - jq(RelSlider.slides[num]).children(".slider-item-image").width()/2});
        if (num != RelSlider.current)
        {
            jq(RelSlider.slides[RelSlider.current]).hide();   
        }
        RelSlider.current = num;
    }
};

RelSlider.hideAll = function()
{
    jq(RelSlider.slides).hide();
}

RelSlider.findId = function (id)
{
    for (var i=0; i<RelSlider.ids.length; i++ )
    {
        if(RelSlider.ids[i] == id)
        {
            return i;
        }
    }
    return -1;
};

RelSlider.readIds = function ()
{
    for (var i=0; i<RelSlider.slides.length; i++ )
    {
        var id = jq(RelSlider.slides[i]).attr('id');
        RelSlider.ids[i] = id;
    }
};

RelSlider.checkAnchor = function ()
{
    if(RelSlider.currentAnchor != document.location.hash)
    {
        RelSlider.currentAnchor = document.location.hash;
        if(!RelSlider.currentAnchor)
        {
             //There is no anchor, go to 0
             RelSlider.gotoSlide(0);
        }
        else{
            var num = RelSlider.findId(RelSlider.currentAnchor.substring(1,RelSlider.currentAnchor.length));
            RelSlider.gotoSlide(num);
        }
    }
};

RelSlider.changeAnchor = function (num)
{
    document.location.hash = RelSlider.ids[num];
}

RelSlider.setup = function ()
{
    if (RelSlider.getSliderElement() && RelSlider.getNumberOfSlides() > 0)
    {
        RelSlider.getSliderElement().show();
        setInterval("RelSlider.checkAnchor()", 300); 
        RelSlider.slides = jq('.slider-item').get().reverse();
        RelSlider.readIds();
        RelSlider.hideAll();
        RelSlider.loadImages();
    }
};

RelSlider.step = function ()
{
    if(RelSlider.current == RelSlider.getNumberOfSlides()-1)
    {
        RelSlider.changeAnchor(0);
    }
    else
    {
        RelSlider.changeAnchor(RelSlider.current+1);
    }
};


RelSlider.stepBack = function ()
{
    if(RelSlider.current == 0)
    {
        RelSlider.changeAnchor(RelSlider.getNumberOfSlides()-1);
    }
    else
    {
        RelSlider.changeAnchor(RelSlider.current-1);
    }
};

jq(document).ready(function () {RelSlider.setup();});