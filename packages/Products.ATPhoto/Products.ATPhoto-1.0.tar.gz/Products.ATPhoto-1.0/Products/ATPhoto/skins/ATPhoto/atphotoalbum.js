var ATPhotoAlbum = null;

function ATPhotoAlbum_createNode(type,className,title,url,content) {
    try { var newNode = document.createElementNS('http://www.w3.org/1999/xhtml', type); }
    catch (e) { var newNode = document.createElement(type); }
    if (className) { newNode.className = className; }
    if (title) { 
        newNode.title = title;
        if (type == 'img') { newNode.alt = title; }
    }
    if (url) { 
        if (type == 'img') { newNode.src = url; }
        if (type == 'a') { newNode.href = url; }
    }
    if (content) { newNode.innerHTML = content; }
    return newNode
}

function ATPhotoAlbum_addPhotoNode() {
    var photo = Batch.current;
    if (!photo) { return false; }
    if (photo.is_folderish) {
        var newNode = this.createNode('div','photoWrapper even');
    } else {
        var newNode = this.createNode('div','photoWrapper odd');
    }
    newNode.id = photo.getId;

    var linkNode = this.createNode('a',null,photo.Title,photo.getURL+'/view');
    var imageNode = this.createNode('img',null,photo.Title,photo.getURL+'/image_'+this.getScale());
    var textNode = this.createNode('a',null,photo.Title,photo.getURL+'/view',photo.Title);
    linkNode.appendChild(imageNode);
    newNode.appendChild(linkNode);
    newNode.appendChild(textNode);
    var wrapper = document.getElementById('AlbumWrapper');
    wrapper.appendChild(newNode);
}

function ATPhotoAlbum_setBatchSize() {
    var batch_size = this.form.BatchSizeList.options[this.form.BatchSizeList.selectedIndex].value;
    createCookie('batch_size',batch_size,30);
    Batch.setBatchSize(parseInt(batch_size));
    this.gotoPage(0);
}

function ATPhotoAlbum_gotoPage(index) {

    Batch.getBatch(index);

    var wrapper = document.getElementById('AlbumWrapper');
    while (wrapper.hasChildNodes()) { wrapper.removeChild(wrapper.firstChild);}
    wrapper.innerHTML = '';
    
    while (!Batch.at_end()) {
        this.addPhotoNode();
        Batch.next();
    }
    var newNode = this.createNode('div','visualClear','','','&nbsp;');
    wrapper.appendChild(newNode);
    Batch.showNavigation();
}

function ATPhotoAlbumObject () {
    this.scale = 'thumb';
    this.form = document.getElementById('AlbumControl');
    this.getScale = function () { return this.scale; }
    this.gotoPage = ATPhotoAlbum_gotoPage;
    this.setBatchSize = ATPhotoAlbum_setBatchSize;
    this.addPhotoNode = ATPhotoAlbum_addPhotoNode;
    this.createNode = ATPhotoAlbum_createNode;
}

function initATPhotoAlbum () {

    if (!context) { getContext(); }

    if (!W3CDOM) {
        /* redirect to the standard album view */
        window.location = context.getURL + '/atphotoalbum_view';
        return;
    }

    var wrapper = document.getElementById('album_control');
    if (!wrapper) { return false; }

    ATPhotoAlbum = new ATPhotoAlbumObject();

    var show_folderish = true;
    getSlideShowContents(show_folderish);

    if (parseInt(ATPhotoAlbum.form.BatchSizeList.options[0].value) > Batch.len()) {
        wrapper.style.visibility = 'hidden';
        wrapper.style.display = 'none';
    }

    var batch_size = ATPhotoAlbum.form.BatchSizeList.options[ATPhotoAlbum.form.BatchSizeList.selectedIndex].value;
    Batch.setBatchSize(parseInt(batch_size));
    Batch.setCallback('ATPhotoAlbum.gotoPage');
    Batch.setBatchUrl(context.getURL);

    if (b_start < Batch.len()) { Batch.init(b_start); }
    else { Batch.init(Batch.len() -1) }

    Batch.current.updateSrc();
    Batch.current.preloadNextPhotos();
    debug('album init');
    ATPhotoAlbum.gotoPage(0);
}

registerPloneFunction(initATPhotoAlbum);
