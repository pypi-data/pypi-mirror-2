/* Javascript for collective.mediaShow - By David Jonas */

mediaShow={};

//States of a slide
mediaShow.NOT_LOADED = 0;
mediaShow.LOADING = 1;
mediaShow.LOADED = 2;

//Hash cache to check for changes
mediaShow.lastHash = "";
mediaShow.hashCheckRunning = false;

//Start Checking for hash changes every second
mediaShow.startHashCheck = function ()
{
  if(!mediaShow.hashCheckRunning)
  {
    mediaShow.hashCheckRunning = true;
    
    setInterval(function() {
      if(mediaShow.lastHash != window.location.hash) {
          mediaShow.hashChanged();
          mediaShow.lastHash = window.location.hash;
      }
    }, 500);
  }
}


//Run if hash has changed
mediaShow.hashChanged = function ()
{
  mediaShow.readURLAndUpdate();
}

//Fixed height of the slideshows
mediaShow.containerHeight = 480;

//Array of slideshows
mediaShow.slideshows = new Array();

//This searches for slideshows on the DOM and creates the data structure in memory
mediaShow.findSlideshows = function ()
{
  $('.embededMediaShow a').each(function (){
        //Hide the link that generates the mediaShow
        $(this).css('display', 'none');
        $(this).parent().addClass('javascripted');
        //-------------------- Declaration of Slideshow ------------------
        mediaShow.slideshows.push(
                                  {"obj": $(this).parent(),
                                   "url": $(this).attr("href"),
                                   "currentSlide": 0,
                                   "slides": new Array(),
                                   "initialized": false,
                                   "size": 0,
                                   "hash": ""
                                  });
    });  
};

//This runs after findSlideshows for each slideShow found, Makes an AJAX call to
//get the content listing for that slideshow.
//ATTENTION: This is an asynch call. The slideshow is only marked initialized after
//           the call is sucessfull.
//TODO: handle URL failure and JSON error
mediaShow.getContentListing = function (slideshow)
{
    var URL = slideshow.url + '/mediaShowListing';
    
    $.getJSON(URL, function(data) {

        $.each(data, function(index, item) {
            //-------------------- Declaration of Slide ------------------
            slideshow.slides.push({
                "url":item.url,
                "UID" : item.UID,
                "loaded": mediaShow.NOT_LOADED
                });
            slideshow.size++;
        });
        
        mediaShow.markAsInitialized(slideshow);
    });
}

//This starts loading the content. Loads first item and recursively the others.
//loadNext is called twice to have allways two items loading at the same time.
mediaShow.startLoading = function (slideshow)
{
    mediaShow.loadNext(slideshow);
    mediaShow.loadNext(slideshow);
};

//This decides which is the next item that should be loaded and starts loading
mediaShow.loadNext = function (slideshow)
{
    if(slideshow.initialized)
    {
        var current = slideshow.currentSlide;
        if(slideshow.slides[current].loaded == mediaShow.NOT_LOADED)
        {
            slideshow.slides[current].loaded = mediaShow.LOADING;
            mediaShow.loadSlide(slideshow, current);
        }
        else
        {
            var distanceForward = -1;
            var distanceBackward = -1;
            var itemForward = -1;
            var itemBackward = -1;
            
            for(var i=current; i<slideshow.slides.length; i++)
            {
                if(slideshow.slides[i].loaded == mediaShow.NOT_LOADED)
                {
                    itemForward = i;
                    distanceForward = i-current;
                    break;
                }
            }
            
            for(var j=current; j>=0; j--)
            {
                if(slideshow.slides[j].loaded == mediaShow.NOT_LOADED)
                {
                    itemBackward = j;
                    distanceBackward = current-j;
                    break;
                }
            }
            
            if (distanceForward == -1 && distanceBackward == -1)
            {
                return;
            }
            if(distanceForward > -1 && distanceBackward == -1)
            {
                slideshow.slides[itemForward].loaded = mediaShow.LOADING;
                mediaShow.loadSlide(slideshow, itemForward);
            }
            else if (distanceBackward > -1 && distanceForward == -1)
            {
                slideshow.slides[itemBackward].loaded = mediaShow.LOADING;
                mediaShow.loadSlide(slideshow, itemBackward);
            }
            else if (distanceForward <= distanceBackward)
            {
                slideshow.slides[itemForward].loaded = mediaShow.LOADING;
                mediaShow.loadSlide(slideshow, itemForward);
            }
            else
            {
                slideshow.slides[itemBackward].loaded = mediaShow.LOADING;
                mediaShow.loadSlide(slideshow, itemBackward);
            }
        }
    }
}

//This starts loading a slide assynchrounosly and when it finishes loading it starts the next one
mediaShow.loadSlide = function (slideshow, slideNumber)
{
    var slide = slideshow.slides[slideNumber];
    var URL = slide.url + '/get_media_show_item';
    
    $.getJSON(URL, function(data) {
        var slideContainer = $(slideshow.obj).find(".mediaShowSlide_" + slideNumber);
        
        var titleDiv = '<div class="mediaShowTitle"><h2><a href="">'+data.title+'</a></h2></div>';
        var descriptionDiv = '<div class="mediaShowDescription">'+data.description+'</div>';
        var infoDiv = '<div class="mediaShowInfo">'+titleDiv+descriptionDiv+'</div>';
        
        slideContainer.append(infoDiv);
        
        slideContainer.append('<div class="mediaShowMedia mediaShowMediaType_'+data.media.type+'"><a href="'+slide.url+'"></a></div>');       
        
        slideContainer.find('.mediaShowMedia a').append(mediaShow.getMediaObject(data.media));
        
        slide.loaded = mediaShow.LOADED;
        mediaShow.loadNext(slideshow);
    });
}

//This generates the html for the media, here we add support for the different kinds of media
mediaShow.getMediaHTML = function (media)
{
  switch(media.type)
  {
    case "Image":
                  return '<img src="'+media.url+'" />'
                  break;
  }
}

//This generates a DOM object with the media loaded into it
mediaShow.getMediaObject = function(media)
{
  switch(media.type)
  {
    case "Image":
                  var img = new Image();
                  $(img)
                  .load(function (){
                      var sizeOfContainer = mediaShow.containerHeight;
                      if($(this).height() > 0 && $(this).height() < sizeOfContainer)
                      {
                        var margin = (sizeOfContainer - $(this).height())/2;
                        $(this).css('margin-top', margin);
                      }
                  })
                  .attr('src', media.url);
                  return img;
                  break;
  }
}


//This runs when the slideshow listing has arrived. We create the DOM wrappers for the slides here and then start loading content
mediaShow.markAsInitialized = function (slideshow)
{
    $.each(slideshow.slides, function (index, slide){
        slideshow.obj.append('<div class="mediaShowSlide mediaShowSlide_'+index+'"></div>');
      });
    
    slideshow.obj.find(".mediaShowSlide_"+slideshow.currentSlide).show();
    
    slideshow.initialized = true;
    mediaShow.hashChanged();
    mediaShow.startHashCheck();
    mediaShow.startLoading(slideshow);
};

//This returns the index of a given slideshow in the main slideshows array
mediaShow.indexOf = function (slideshow)
{
  var slideshowIndex = -1;
  
  $.each(mediaShow.slideshows, function (index, currentSlideshow)
       {
          if(currentSlideshow == slideshow)
          {
            slideshowIndex = index;
          }
       });
  
  return slideshowIndex;
}

//This function adds the navigation buttons to the slideshow
mediaShow.addButtons = function (slideshow)
{ 
  var slideshowIndex = mediaShow.indexOf(slideshow);
  var buttonNext = '<a href="#" class="buttonNext" onclick="return mediaShow.next('+slideshowIndex+')"> Next &raquo;</a>';
  var buttonPrev = '<a href="#" class="buttonPrev" onclick="return mediaShow.prev('+slideshowIndex+')">&laquo; Previous</a>';
  var container = '<div class="mediaShowButtons">'+buttonPrev+buttonNext+'</div>';
  
  slideshow.obj.append(container);
}

//Show the next slide in the given slideshow
mediaShow.next = function (slideshowIndex)
{
  var slideshow = mediaShow.slideshows[slideshowIndex];
  if(slideshow.currentSlide + 1 <= slideshow.size - 1)
  { 
    mediaShow.goToSlide(slideshow.currentSlide + 1, slideshow); 
  }
  else
  {
    mediaShow.goToSlide(0, slideshow);
  }
  
  return false;
}

//Show the previews slide in given slideshow
mediaShow.prev = function (slideshowIndex)
{
  var slideshow = mediaShow.slideshows[slideshowIndex];
  if(slideshow.currentSlide - 1 >= 0)
  {
    mediaShow.goToSlide(slideshow.currentSlide - 1, slideshow);
  }
  else
  {
    mediaShow.goToSlide(slideshow.size-1, slideshow);
  }
  
  return false;
}

//This returns the index of the slide with the provided UID.
mediaShow.idToIndex = function (slideshow, uid)
{
  var found = -1;
  $.each(slideshow.slides, function(index, slide){
    if(slide.UID == uid)
    {
      found = index;
    }
  });
  return found;
};

//This reads the URL hash and updates the slideshows acordingly
mediaShow.readURLAndUpdate = function ()
{
  var hash = document.location.hash;
  if(hash == "")
    return;
  
  var hash_split = hash.substring(1,hash.length).split(",");
  $.each(hash_split, function(index, hsh){
    $.each(mediaShow.slideshows, function(index, slideshow){
      var slideIndex = mediaShow.idToIndex(slideshow, hsh);
      if (slideIndex > -1)
      {
        slideshow.hash = hsh;
        mediaShow.goToSlide(slideIndex, slideshow);
        return false;
      }
      return true;
    });
  });
};

//This function will update the browser's url to the current state of the multiple slideshows.
mediaShow.updateURL = function (slideshow, slideNumber)
{
  var uid = slideshow.slides[slideNumber].UID;
  var old_hash = document.location.hash;
  var new_hash = uid;
  var hash_split = old_hash.substring(1,old_hash.length).split(",");
  var hash = new Array();
  
  var replaced = false;
  $.each(hash_split, function(index, hsh){
    if(hsh == slideshow.hash)
    {
      hash.push(new_hash);
      replaced = true;
    }
    else
    {
      hash.push(hsh);
    }
  });
  
  if(!replaced)
  {
    hash.push(new_hash);
  }
  
  document.location.hash = hash.join(",");
  slideshow.hash = new_hash;
};

//This shows slide number x on the given slideshow
mediaShow.goToSlide = function (x, slideshow)
{
  mediaShow.updateURL(slideshow, x);
  if(slideshow.slides[x].loaded == mediaShow.NOT_LOADED)
  {
    slideshow.currentSlide = x;
  }
  {
    slideshow.obj.find(".mediaShowSlide_"+x).show();
    var sizeOfContainer = mediaShow.containerHeight;
    var img = slideshow.obj.find(".mediaShowSlide_"+x).find('img')[0];
    height = $(img).attr('offsetHeight');
    if(height > 0 && height < sizeOfContainer)
    {
      var margin = (sizeOfContainer - height)/2;
      $(img).css('margin-top', margin);
    }
    
    slideshow.currentSlide = x;
    
    $.each(slideshow.slides, function (index, slide) {
                                if(index != x)
                                {
                                  slideshow.obj.find(".mediaShowSlide_"+index).hide();
                                }
                              });
  }
}

//This is the first function to run, finds slideshows on the page and initializes them
mediaShow.init = function ()
{
    mediaShow.findSlideshows();
    $.each(mediaShow.slideshows, function (index, slideshow)
           {
                mediaShow.getContentListing(slideshow);
                mediaShow.addButtons(slideshow)
           });
};


// This starts the whole process when the DOM is completely loaded
$(function(){
    mediaShow.init();
});