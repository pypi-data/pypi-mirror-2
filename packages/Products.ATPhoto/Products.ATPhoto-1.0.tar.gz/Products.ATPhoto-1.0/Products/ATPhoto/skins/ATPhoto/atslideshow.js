/* 
 * Script for AT slide show
 * By Gael Pasgrimaud <gael@gawel.org>
 */

/******************************
 * various configuration option
 ******************************
 */
function SlideShow_configSlideShow() {
    this.max_items_in_navigation = 18;
    this.large_delay = 3000;
    this.max_retry = 10;
    this.wait_delay = 1000;
}
/*
 ******************************
 */


/* only use for developement */
var debug_mode = 0;

/* global vars */

var SlideShow = new Object;
var PhotoTimer = 0;



/* slide show */

function SlideShow_getNodeFromPhoto(photo) {
    /* create a node object from photo */
    try { var newNode = document.createElementNS('http://www.w3.org/1999/xhtml', 'img'); }
    catch (e) { var newNode = document.createElement('img'); }
    newNode.src = photo.getScaleUrl();
    newNode.width = photo.getWidth();
    newNode.height = photo.getHeight();
    newNode.alt = photo.Title;
    newNode.title = photo.Title;
    this.newNode = newNode;
}

function SlideShow_updateHTML() {
   /* update innerHTML */
   var nodes;
   document.title=Batch.current.Title;
   nodes = cssQuery('h1.documentFirstHeading');
   if (nodes.length > 0) { nodes[0].innerHTML=Batch.current.Title; }
   nodes = cssQuery('div.documentDescription');
   if (nodes.length > 0) { nodes[0].innerHTML=Batch.current.Description; }
   this.photo_size.innerHTML = Batch.current.getObjSize;
   this.content_type.innerHTML = Batch.current.content_type;
   if (!context.is_folderish) { fixHTML(); }
}

function SlideShow_incrPhotoCounter() {

   if (this.isStarted()) { Batch.next(); }

   if (Batch.iterator < Batch.len()-1) {
       /* preload next photo */
       Batch.getitem[Batch.iterator+1].updateSrc();
   }
}

function SlideShow_updatePhoto() {
   /* this is the core function of the slide show */


   this.resetTimer();

   var length = Batch.len();

   if (Batch.iterator > Batch.len()) {
        if (this.isStarted()) {
            this.toggleStartStop();
        }
        return;
   }

   //debug('update photo');
   var photo = Batch.current;

   if (!photo) { return ;}

   var delay = this.large_delay;

   photo.preloadNextPhotos();

   if (photo.isAvailable()) {
       /* if the photo is upload then we show it and update timer */
       //debug('try to show image ' + (Batch.iterator + 1) + ' of ' + length);
       this.retry_counter = 0;

       if (Batch.iterator <= 1) { this.showControls(); }


       this.getNodeFromPhoto(photo);
       this.callBack = eval(this.callBackName);
       this.callBack();
       return;

   } else {
       //debug('failed to get photo ' + photo.getId + ' retry ' + this.retry_counter + ' of ' + this.max_retry);
       if (this.retry_counter < this.max_retry) {
           /* else we use smallDelay to wait for it */
           this.retry_counter = this.retry_counter + 1;
           this.setTimer(this.wait_delay,1);
       } else {
           /* after retries we skip the photo :\ */
           this.retry_counter = 0;
           this.incrPhotoCounter();
           this.setTimer(100);
       }
   }

   if (Batch.iterator > Batch.len()) {
        if (this.isStarted()) {
            this.toggleStartStop();
        }
        return;
   }
}

function SlideShow_isInCallBack() {
    /* return true if slidshow is in callback */
    if (this.is_in_callback == 1) { return true; }
    return false;
}

function SlideShow_isStarted() {
    /* return true if slidshow is started */
    if (this.is_started == 1) { return true; }
    return false;
}

function SlideShow_toggleStartStop() {
   /* start or stop slide show */
   if (this.isStarted()) {
       this.is_started = 0;
       this.resetTimer();
       this.form.StartStopButton.value = 'Start';
   } else {
       this.is_started = 1;
       if (Batch.iterator > Batch.len()-1) {
            Batch.init(0);
       }
       this.updatePhoto();
       this.form.StartStopButton.value = 'Stop';
   }
}

function SlideShow_setTimer(delay, force) {
    if(delay) {
        if (!this.isInCallBack()) {
            if (this.isStarted() || force) { 
                PhotoTimer = setTimeout("SlideShow.updatePhoto()", delay);
            }
        } else {
            PhotoTimer = setTimeout("SlideShow.callBack()", delay);
        }
    } else {
        this.updatePhoto();
    }
}

function SlideShow_resetTimer() {
    if(PhotoTimer) {
        clearTimeout(PhotoTimer);
        PhotoTimer  = 0;
    }
}

function SlideShow_getNavigation() {
    /* replace navigation content */
    Batch.getBatch(Batch.iterator);
    if (!context.is_folderish) { Batch.setBatchUrl(Batch.current.getURL + '/view'); }
    Batch.showNavigation();
}

function SlideShow_showControls() {
    var element = document.getElementById('image_infos');
    element.style.visibility = 'visible';
    element = document.getElementById('slideshow_control');
    element.style.visibility = 'visible';
    this.getNavigation();
}

function SlideShow_setDelay() {
    var delay = this.form.DelayList.options[this.form.DelayList.selectedIndex].value;
    createCookie('transition_delay',delay,30);
    this.large_delay = parseInt(delay) * 1000;
}

function SlideShow_setCallback() {
    /* register callback from form ! */

    createCookie('transition',this.form.TransitionList.options[this.form.TransitionList.selectedIndex].value,30);

    this.callBackName = eval(this.form.TransitionList.options[this.form.TransitionList.selectedIndex].value);
}

function SlideShow_getScale() {
    return this.scale;
}

function SlideShow_setScale() {

    this.scale = this.form.ScaleList.options[this.form.ScaleList.selectedIndex].value;

    debug('changing scale '+ this.getScale());

    this.resetTimer();

    /* for large scale we use plone fullscreen mode */
    var body = cssQuery('body')[0];
    if (this.scale == 'fullscreen') {
        if (!hasClassName(body, 'fullscreen')) {
            toggleFullScreenMode();
            this.scale = 'large';
        }
    } else {
        if (hasClassName(body, 'fullscreen')) {
            toggleFullScreenMode();
        }
    }

    createCookie('size',this.getScale(),30);

    var i;

    for (i = 0; i < Batch.len(); i++) {
        Batch.getitem[i].resetSrc();
    }

    try { Batch.current.updateSrc(); }
    catch (e) { Batch.previous();
    Batch.current.updateSrc(); }

    this.setTimer(1000,1);
}

function SlideShow_gotoPhoto(index) {
   /* goto a photo item */

   debug('goto photo '+index)

   this.resetTimer();

   Batch.iterator = index-1;
   Batch.next();
   var delay = 1;

   if (Batch.current.isAvailable() != 1) {
        debug('photo '+index+' not yet available')
        Batch.current.updateSrc();
        delay = 1000;
   }


   this.setTimer(delay, 1);

   return false;
}

function SlideShowObject() {
    /* constructor */

    this.configSlideShow = SlideShow_configSlideShow;
    this.configSlideShow();

    /* html objects */
    this.form = document.forms['SlideShowControl'];
    if (!this.form) { return false; }
    this.photo_size =  document.getElementById('PhotoSize');
    this.content_type =  document.getElementById('ContentType');
    this.wrapper = document.getElementById('PhotoWrapper');

    /* vars */
    this.retry_counter = 0;
    this.is_started = 0;
    this.is_in_callback = 0;
    this.scale = this.form.ScaleList.options[this.form.ScaleList.selectedIndex].value;
    this.currentNode = document.SlideImage;
    this.nextNode = null;

    /* methods */
    this.updatePhoto = SlideShow_updatePhoto;

    this.toggleStartStop = SlideShow_toggleStartStop;
    this.isStarted = SlideShow_isStarted;
    this.isInCallBack = SlideShow_isInCallBack;

    this.resetTimer = SlideShow_resetTimer;
    this.setTimer = SlideShow_setTimer;

    this.updateHTML = SlideShow_updateHTML;
    this.incrPhotoCounter = SlideShow_incrPhotoCounter;
    this.getNavigation = SlideShow_getNavigation;
    this.showControls = SlideShow_showControls;

    this.setDelay = SlideShow_setDelay;
    this.setCallback = SlideShow_setCallback;
    this.getScale = SlideShow_getScale;
    this.setScale = SlideShow_setScale;

    this.gotoPhoto = SlideShow_gotoPhoto;
    
    this.getNodeFromPhoto = SlideShow_getNodeFromPhoto;

}

/* utilities */

function initSlideShow() {
    /* init slide show context */
    
    if (!context) { getContext(); }

    if (!W3CDOM) {
        /* redirect to the standard album view */
        window.location = context.getURL + '/atphotoalbum_view';
        return;
    }

    var wrapper = document.getElementById('PhotoWrapper');
    if (!wrapper) { return false; }

    SlideShow = new SlideShowObject;

    var options = SlideShow.form.TransitionList.options;

    var transition = null;

    var t = readCookie('transition');   
    if (!t) { 
        t = 'ATPhoto_fadeCallBack';
        createCookie('transition','ATPhoto_fadeCallBack');
    }

    for (var i = 0; i < TransitionsCallbacks.length; i++) {
        transition = TransitionsCallbacks[i];
        options[options.length] = new Option(transition.id, transition.method);
        if (transition.method == t) { 
            SlideShow.form.TransitionList.selectedIndex = i;
            SlideShow.callBackName = t;
        }
    }

    options = SlideShow.form.ScaleList.options;
    options[options.length] = new Option('fullscreen', 'fullscreen');

    Batch.setBatchSize(1);
    Batch.setCallback('SlideShow.gotoPhoto');
    Batch.setBatchUrl(context.getURL);

    var show_folderish = false;
    getSlideShowContents(show_folderish);

    if (b_start < Batch.len()) { Batch.init(b_start); }
    else { Batch.init(Batch.len() -1) }

    Batch.current.updateSrc();
    Batch.current.preloadNextPhotos();
    // last photo is available in nav so we preload it at startup
    Batch.getitem[Batch.len()-1].updateSrc();

    /* init call back */
    SlideShow.setCallback();

    if (context.is_folderish) {
        SlideShow.toggleStartStop();
    } else {
        SlideShow.showControls();
    }
}
registerPloneFunction(initSlideShow);

function debug(text) {
    if (debug_mode) {
        var Debug =  document.getElementById('Debug');
        if (Debug) {
            Debug.style.visibility = 'visible';
            var html = Debug.innerHTML + '\n' + text;
            Debug.innerHTML = html;
        }
    }
}

