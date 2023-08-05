/* photo object */

function fixHTML() {
    /* replace all url / title */
    getATPhotoInfos();
    replaceInNodes('div.contenttype-atphoto',/(>)[\w\s\.]+(<\/a>)/,'$1'+Batch.current.Title+'$2');
    replaceInNodes('portal-breadcrumbs',/(<span>)[\w\s\.]+(<\/span>)/,'$1'+Batch.current.Title+'$2');

    var url_regex = /(\shref=")\S+(\/\S*"(>|\s))/g;
    replaceInNodes('div.contenttype-atphoto',url_regex,'$1'+Batch.current.getURL+'$2');
    replaceInNodes('dd.actionMenuContent',url_regex,'$1'+Batch.current.getURL+'$2');
    replaceInNodes('ul.contentViews',url_regex,'$1'+Batch.current.getURL+'$2');
    replaceInNodes('calendar-previous',url_regex,'$1'+Batch.current.getURL+'$2');
    replaceInNodes('calendar-next',url_regex,'$1'+Batch.current.getURL+'$2');
}

function hideATPhotoInfos() {
    var wrapper = document.getElementById('EXIF');
    var field = document.getElementById('EXIFHeader');
    if (field) field.innerHTML = '';
    if (wrapper) wrapper.style.visibility = 'hidden';
    wrapper = document.getElementById('IPTC');
    field = document.getElementById('IPTCHeader');
    if (field) field.innerHTML = '';
    if (wrapper) wrapper.style.visibility = 'hidden';
}

function showATPhotoInfos () {
    /* callback function for exif/iptc infos */
    if (this.readyState == 4) {
        var wrapper;
        var field;
        var showed = false;
        if(this.parseError == 0) {
            var node = false;
            var value = false;
            var element_id = '';
            if (this.firstChild) {
                var root = this.firstChild;
                for (var i = 0; i < root.childNodes.length; i++) {
                    var node = root.childNodes[i];
                    if (node && node.firstChild) {
                        element_id = node.tagName.toUpperCase();
                        wrapper = document.getElementById(element_id);
                        field = document.getElementById(element_id+'Header');
                        value = node.firstChild.nodeValue;
                        if (value && value.match(/(table|div)/)) {
                            if (field) field.innerHTML = value;
                            if (wrapper) wrapper.style.visibility = 'visible';
                        } else {
                            if (field) field.innerHTML = '';
                            if (wrapper) wrapper.style.visibility = 'hidden';
                        }
                    }
                    activateCollapsibles();
                    showed = true;
                }
            } else { showed = false; }
        }
        if (!showed) {
            hideATPhotoInfos();
        } 
    }
}

function getATPhotoInfos () {
    /* we get exif/iptc infos with sarissa */

    if (context.is_folderish) { return false; }

    var xmlDoc = Sarissa.getDomDocument();
    xmlDoc.async = true;
    var uri =  Batch.current.getURL +  '/atphoto_infos'; 
    xmlDoc.onreadystatechange = showATPhotoInfos;
    /* Sarissa don't work with KHTML browsers */
    try { xmlDoc.load(uri); } catch(e) { hideATPhotoInfos(); }
}

function ATPhoto_imageOnload() {
    /* image on load event */
    var index = parseInt(this.name);
    var photo = Batch.getitem[index];
    photo.available = 1;
    //debug('photo '+ photo.index + ' loaded');
    photo.preloadNextPhotos();
}

function ATPhoto_preloadNextPhotos() {
    /* preloading next photos */
    var index = Batch.iterator+1;
    var max_index = index + Batch.max_items_in_navigation * 2;
    if (index >= Batch.len() - Batch.max_items_in_navigation) {
        index = Batch.len() - Batch.max_items_in_navigation;
    }
    var photo;
    for (var i = index; i < max_index + 2; i++) {
        photo = Batch.getitem[i];
        if (photo && !photo.img.src) {
            photo.updateSrc();
            break;
        }
    }
}

function ATPhoto_imageOnerror() {
    /* image on error event */
    var photo = Batch.getitem[this.name];
    photo.available = -1;
    debug(photo.getId + ' as error');
}

function ATPhoto_isAvailable() {
    /* return true if photo is loaded */
    if (this.available == -1) { return false; }
    if (this.available) { return true; }
    return false;
}

function ATPhoto_updateSrc() {
    /* update image src to preload it */
    if (!this.img.src) {
        this.img.src = this.getScaleUrl();
        //debug('preloading photo ' + this.index );
    }
}

function ATPhoto_getScaleUrl() {
    /* update image src to preload it */
    var scale = this.getScale();
    var url;

    url = eval('this.size_'+scale+'_url');
    if (url) { return url }

    if (scale == 'full') {
        url = this.getURL + '/image';
    } else {
        url = this.getURL + '/image_' + scale;
    }
    return url;
}

function ATPhoto_resetSrc() {
    /* reset image at init or after scale change */
    try { this.img = document.createElementNS('http://www.w3.org/1999/xhtml', 'img'); }
    catch (e) { this.img = document.createElement('img'); }

    this.img.onload = ATPhoto_imageOnload;
    this.img.onerror = ATPhoto_imageOnerror;

    this.img.name = this.index;
    this.available = 0;
}

function ATPhoto_setSize(id,width,height,url) {
    /* facility to init image sizes */
    var size = new Object;
    size.id = id;
    eval('this.size_'+id+'_width = width;');
    eval('this.size_'+id+'_height = height;');
    if (url)
        eval('this.size_'+id+'_url = url;');
}

function ATPhoto_getWidth() {
    var scale = this.getScale();
    var size;
    size = eval('this.size_'+scale+'_width');
    if (size) { return size }
    return 0;
}

function ATPhoto_getHeight() {
    var scale = this.getScale();
    var size;
    size = eval('this.size_'+scale+'_height');
    if (size) { return size }
    return 0;
}

function ATPhoto(object,index,content_type) {
    /* ATPhoto implementation */

    object.index = index;
    object.content_type = content_type;
    object.available = 0;

    object.getScale = function () {
        if (SlideShow.form) { return SlideShow.getScale() }
        if (ATPhotoAlbum) { return ATPhotoAlbum.getScale() }
        return 'preview';
    }

    object.sizes = new Array;
    object.setSize = ATPhoto_setSize;
    object.getWidth = ATPhoto_getWidth;
    object.getHeight = ATPhoto_getHeight;
    object.getScaleUrl = ATPhoto_getScaleUrl;

    object.updateSrc = ATPhoto_updateSrc;
    object.preloadNextPhotos = ATPhoto_preloadNextPhotos;
    object.isAvailable = ATPhoto_isAvailable;
    object.resetSrc = ATPhoto_resetSrc;

    object.resetSrc();
}

function initATPhoto() {

    if (!context) { getContext(); }

    if (!context.is_folderish) {
        /* replace some html contents to get correct nodes for ajax stuff */
        var wrapper;
        var header;
        wrapper = cssQuery('div.discussion')[0];
        if (wrapper) {
            wrapper.className = '';
            wrapper.id = 'DISCUSSION';
            try { header = document.createElementNS('http://www.w3.org/1999/xhtml', 'div'); }
            catch (e) { header = document.createElement('div'); }
            header.className = 'discussion';
            header.id = 'DISCUSSIONHeader';
            header.innerHTML = wrapper.innerHTML;
            wrapper.innerHTML = '';
            wrapper.appendChild(header);
        }
        wrapper = cssQuery('div.documentByLine')[0];
        if (wrapper) {
            wrapper.className = '';
            wrapper.id = 'DOCUMENTBYLINE';
            try { header = document.createElementNS('http://www.w3.org/1999/xhtml', 'div'); }
            catch (e) { header = document.createElement('div'); }
            header.className = 'documentByLine';
            header.id = 'DOCUMENTBYLINEHeader';
            header.innerHTML = wrapper.innerHTML;
            wrapper.innerHTML = '';
            wrapper.appendChild(header);
        }
    }
}

registerPloneFunction(initATPhoto);
