/* Javascript for the related content slider */

RelSlider = {};

RelSlider.slides = [];
RelSlider.ids = [];
RelSlider.current = 0;
RelSlider.numSlides = 0;
RelSlider.currentAnchor = "not set";
RelSlider.NumItemsToLoadOnStartup = 3;

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
                var imagelink = link.parent().children('.imageLinkOnSlider');
                
                link.parent().prepend(jq(this));
                
                /*if(imagelink.length == 1)
                {
                    imagelink.prepend(jq(this));
                }
                else
                {
                    link.parent().prepend(jq(this));
                }*/
                
                link.remove();
                if(jq(this).height() > 0)
                {
                    jq(this).css({'top': 225 - jq(this).height()/2, 'left': 300 - jq(this).width()/2});
                }
            })
            .attr('src', url);
    });
};

RelSlider.isOfType = function (num, section)
{
    return jq(RelSlider.slides[num]).attr("class").match("slider-"+section);
}

RelSlider.gotoSection = function (section)
{
    if(section == 'Documentation')
    {
        var docId = jq('.slider-button-Documentation').attr('name');
        if(docId != "")
        {
            document.location.hash = jq('.slider-button-Documentation').attr('name');
            jq(".slider-button-Documentation").addClass("slider-button-active");
            jq(".slider-button-People").removeClass("slider-button-active");
            jq(".slider-button-Works").removeClass("slider-button-active");
        }
    }
    else
    {
        for(var i=1; i<RelSlider.slides.length; i++)
        {
            if(RelSlider.isOfType(i, section))
            {
                RelSlider.changeAnchor(i);
                break;
            }
        }
    }
}

RelSlider.gotoSlide = function (num)
{
    if(num >= 0 && num < RelSlider.numSlides && num != RelSlider.current)
    {
        jq(RelSlider.slides[num]).show();
        jq(RelSlider.slides[num]).children(".slider-item-image").css({'top': 225 - jq(RelSlider.slides[num]).children(".slider-item-image").height()/2, 'left': 300 - jq(RelSlider.slides[num]).children(".slider-item-image").width()/2});
        if (num != RelSlider.current)
        {
            jq(RelSlider.slides[RelSlider.current]).hide();   
        }
        RelSlider.current = num;
        
        RelSlider.activateSectionButton();
    }
};

RelSlider.activateSectionButton = function ()
{
    if(RelSlider.current == 0)
    {
        jq(".slider-button-Documentation").removeClass("slider-button-active");
        jq(".slider-button-People").removeClass("slider-button-active");
        jq(".slider-button-Works").removeClass("slider-button-active");
        return;
    }
    
    var type = jq(RelSlider.slides[RelSlider.current]).attr("class").substring(19);
    if( RelSlider.findId(RelSlider.decode(document.location.hash).substring(1,RelSlider.currentAnchor.length)) >= RelSlider.findId(jq(".slider-button-Documentation").attr("name")))
    {
        jq(".slider-button-Documentation").addClass("slider-button-active");
        jq(".slider-button-People").removeClass("slider-button-active");
        jq(".slider-button-Works").removeClass("slider-button-active");
        return;
    }
    if (type == "Work")
    {
        jq(".slider-button-Works").addClass("slider-button-active");
        jq(".slider-button-People").removeClass("slider-button-active");
        jq(".slider-button-Documentation").removeClass("slider-button-active");
        return;
    }
    else if (type == "Person")
    {
        jq(".slider-button-People").addClass("slider-button-active");
        jq(".slider-button-Works").removeClass("slider-button-active");
        jq(".slider-button-Documentation").removeClass("slider-button-active");
        return;
    }
    else if (type == "File")
    {
        jq(".slider-button-People").removeClass("slider-button-active");
        jq(".slider-button-Works").removeClass("slider-button-active");
        jq(".slider-button-Documentation").removeClass("slider-button-active");
        return;
    }
    else if (type == "Event")
    {
        jq(".slider-button-People").removeClass("slider-button-active");
        jq(".slider-button-Works").removeClass("slider-button-active");
        jq(".slider-button-Documentation").removeClass("slider-button-active");
        return;
    }
};

RelSlider.hideAll = function()
{
    jq(RelSlider.slides).each(function () {if(jq(this).attr("name") != jq(RelSlider.slides[RelSlider.current]).attr("name")){jq(this).hide()}});
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
        var id = jq(RelSlider.slides[i]).attr('name');
        RelSlider.ids[i] = id;
    }
};

RelSlider.checkAnchor = function ()
{
    if(RelSlider.currentAnchor != RelSlider.decode(document.location.hash))
    {
        RelSlider.currentAnchor = RelSlider.decode(document.location.hash);
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

RelSlider.decode = function(str) {
    var encoded = str;
    return decodeURIComponent(encoded.replace(/\+/g, " "));
} 

RelSlider.changeAnchor = function (num)
{
    document.location.hash = RelSlider.ids[num];
}

RelSlider.setup = function ()
{
    if (RelSlider.getSliderElement() && RelSlider.getNumberOfSlides() > 0)
    {
        //RelSlider.getSliderElement().show();
        setInterval("RelSlider.checkAnchor()", 300); 
        RelSlider.slides = jq('.slider-item').get().reverse();
        RelSlider.readIds();
        RelSlider.hideAll();
        if(RelSlider.getNumberOfSlides() < RelSlider.NumItemsToLoadOnStartup)
        {
            RelSlider.loadImages();
        }
        else
        {
            RelSlider.loadFirstImages();
        }
    }
};

RelSlider.loadFirstImages = function()
{
    var items = jq(jq('.slider-item-image-link').get().reverse()).slice(0,RelSlider.NumItemsToLoadOnStartup)
    
    $(items).each(function(){
        var link = jq(this);
        var url = link.attr('href');
        var img = new Image();
        jq(img)
            .addClass('slider-item-image')
            .load(function (){
                var imagelink = link.parent().children('.imageLinkOnSlider');
                
                link.parent().prepend(jq(this));
                
                /*if(imagelink.length == 1)
                {
                    imagelink.prepend(jq(this));
                }
                else
                {
                    link.parent().prepend(jq(this));
                }*/
                
                link.remove();
                if(jq(this).height() > 0)
                {
                    jq(this).css({'top': 225 - jq(this).height()/2, 'left': 300 - jq(this).width()/2});
                }
            })
            .attr('src', url);
    });
}

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

jq(window).load(function () {
    RelSlider.loadImages();
});

jq(document).ready(function () {
    RelSlider.setup();
    $(document).keydown(function(e){
        if(document.activeElement == document.body)
        {
            if (e.keyCode == 37) { 
               RelSlider.stepBack();
            }
            else if (e.keyCode == 39) 
            {
               RelSlider.step();
            }
        }
        return true;
    });

});