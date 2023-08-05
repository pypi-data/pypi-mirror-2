/* 
 * Transitions Script for ATPhoto
 * By Gael Pasgrimaud <gael@gawel.org>
 */


/* callback registry */

var TransitionsCallbacks = new Array();

function registerTransitionCallBack (id,method) {
    var transition = new Object;
    transition.id = id;
    transition.method = method;
    TransitionsCallbacks.push(transition);
}

/* callback function */
    
function ATPhoto_basicCallBack() {
    /* this is the most basic callback function */
    this.wrapper.style.backgroundPosition = 'top center';
    this.wrapper.style.backgroundRepeat = 'no-repeat';
    this.wrapper.style.backgroundImage = 'url('+searchForAttr(this.wrapper,'src')+')';
    while (this.wrapper.hasChildNodes()) { this.wrapper.removeChild(this.wrapper.firstChild);}
    this.wrapper.innerHTML = '';
    this.wrapper.appendChild(this.newNode);
    this.updateHTML();
    this.getNavigation();
    this.incrPhotoCounter();
    this.currentNode = this.newNode;
    this.is_in_callback = 0;
    this.callback_counter = 0;
    this.wrapper.style.backgroundImage = '';
    this.setTimer(this.large_delay);
}

registerTransitionCallBack('basic','ATPhoto_basicCallBack');

function ATPhoto_switchCallBack() {
    /* this a callback function with timer
     * a good starting point for transition ;)
     */

    /* first let the SlideShow know that we are in a callback function */
    this.is_in_callback = true;

    /* init a counter */
    if (!this.callback_counter) { this.callback_counter = 1; }

    /* if it's not the first pic then do our transition */
    if (this.currentNode) {
        /* WATCHA here is the core transition */
        if (this.callback_counter == 2 || this.callback_counter == 4 || this.callback_counter == 6) {
            if (this.wrapper.hasChildNodes()) { this.wrapper.removeChild(this.wrapper.firstChild);}
            this.wrapper.appendChild(this.currentNode);
        } else {
            if (this.wrapper.hasChildNodes()) { this.wrapper.removeChild(this.wrapper.firstChild);}
            this.wrapper.appendChild(this.newNode);
        }
        this.getNavigation();
    } else {
        /* it's the first pic so just show it */
        this.wrapper.appendChild(this.newNode);
        this.callback_counter = 100;
        this.getNavigation();
        // this.incrPhotoCounter();
        this.setTimer(this.large_delay);
    }

    /* at the end of callback loop we switch the node and set callback ended */
    if (this.callback_counter >= 6) {
        this.updateHTML();
        this.incrPhotoCounter();
        this.currentNode = this.newNode;
        this.is_in_callback = false;
        this.callback_counter = null;
        this.setTimer(this.large_delay);
        return;
    }

    /* init timer. SlideShow know that we are in a callback function so he call it instead of updating photo ;) */
    this.callback_counter +=1;
    this.setTimer(100);

}

// registerTransitionCallBack('switch','ATPhoto_switchCallBack');

function ATPhoto_crossWipeCallBack() {
    /* cross wipe */

    /* first let the SlideShow know that we are in a callback function */
    this.is_in_callback = true;

    /* init a counter */
    if (!this.callback_counter) { this.callback_counter = 0; }

    this.wrapper.style.backgroundPosition = 'top center';
    this.wrapper.style.backgroundRepeat = 'no-repeat';

    if (this.wrapper.hasChildNodes() && this.wrapper.firstChild.id != 'transitionWrapper') {
        this.wrapper.style.backgroundImage = 'url('+searchForAttr(this.wrapper,'src')+')';
        while (this.wrapper.hasChildNodes()) { this.wrapper.removeChild(this.wrapper.firstChild);}
        this.wrapper.innerHTML = '';
    }
    if (!this.wrapper.hasChildNodes()) {
        try { var newNode = document.createElementNS('http://www.w3.org/1999/xhtml', 'div'); }
        catch (e) { var newNode = document.createElement('div'); }
        newNode.style.backgroundPosition = 'top center';
        newNode.style.backgroundRepeat = 'no-repeat';
        newNode.id = 'transitionWrapper';
        this.wrapper.appendChild(newNode);
    }
    var wrapper = this.wrapper.firstChild;
    this.wrapper.style.height = this.newNode.height + 'px';
    wrapper.style.backgroundImage = 'url('+this.newNode.src+')';
    wrapper.style.height = this.callback_counter +'px';
    if (this.callback_counter >= this.newNode.height) {
        this.updateHTML();
        this.getNavigation();
        this.incrPhotoCounter();
        this.wrapper.style.backgroundImage = 'url('+this.newNode.src+')';
        this.currentNode = this.newNode;
        this.is_in_callback = false;
        this.callback_counter = null;
        this.setTimer(this.large_delay);
        return;
    }

    this.callback_counter +=2;
    this.setTimer(20);
}

registerTransitionCallBack('cross wipe','ATPhoto_crossWipeCallBack');


function ATPhoto_fadeCallBack() {
    /* fading */

    /* first let the SlideShow know that we are in a callback function */
    this.is_in_callback = true;

    /* init a counter */
    if (!this.callback_counter) { this.callback_counter = 0; }

    this.wrapper.style.backgroundPosition = 'top center';
    this.wrapper.style.backgroundRepeat = 'no-repeat';

    if (this.wrapper.hasChildNodes() && this.wrapper.firstChild.id != 'transitionWrapper') {
        this.wrapper.style.backgroundImage = 'url('+searchForAttr(this.wrapper,'src')+')';
        while (this.wrapper.hasChildNodes()) { this.wrapper.removeChild(this.wrapper.firstChild);}
        this.wrapper.innerHTML = '';
    }
    if (!this.wrapper.hasChildNodes()) {
        try { var newNode = document.createElementNS('http://www.w3.org/1999/xhtml', 'div'); }
        catch (e) { var newNode = document.createElement('div'); }
        newNode.id = 'transitionWrapper';
        newNode.style.backgroundPosition = 'top center';
        newNode.style.backgroundRepeat = 'no-repeat';
        this.wrapper.appendChild(newNode);
    }
    var wrapper = this.wrapper.firstChild;
    this.wrapper.style.height = this.newNode.height + 'px';
    wrapper.style.backgroundImage = 'url('+this.newNode.src+')';
    wrapper.style.height = this.newNode.height +'px';

    try {
        /* ie use filter.alpha */
        wrapper.filters.alpha.opacity = (this.callback_counter*100);
    } catch (e) {
        wrapper.style.KhtmlOpacity = this.callback_counter;
        if (this.callback_counter >= 1) { 
            wrapper.style.MozOpacity = 0.9999999;
            wrapper.style.opacity = 0.9999999;
        } else {
            wrapper.style.MozOpacity = this.callback_counter;
            wrapper.style.opacity = this.callback_counter; }
    }

    if (this.callback_counter == 0.7) {
        this.updateHTML();
        this.getNavigation();
    }
        
    if (this.callback_counter >= 1) {
        this.incrPhotoCounter();
        this.wrapper.style.backgroundImage = 'url('+this.newNode.src+')';
        this.currentNode = this.newNode;
        this.is_in_callback = false;
        this.callback_counter = null;
        this.setTimer(this.large_delay);
        return;
    }

    this.callback_counter +=.10;
    this.setTimer(100);
}

registerTransitionCallBack('cross fade','ATPhoto_fadeCallBack');

