/* 
 * "Python like" Objects implementation
 * By Gael Pasgrimaud <gael@gawel.org>
 */

var context = null;

var label_previous = 'previous';
var label_next = 'next';
var label_items = 'items';

function searchForAttr(node,attr) {
    var regex = new RegExp('.*\\s'+ attr +'="(\\S+)"(\\s|>).*','mg');
    var match = node.innerHTML.replace(regex,'$1');
    if (match) { return match; }
    return '';
}

function replaceInNodes(identifier,regex,text) {
    /* text replacing with regexp */
    var node;
    var html;
    var nodes = cssQuery(identifier);
    if (!nodes || nodes.length == 0) {
        node = document.getElementById(identifier);
        if (node) {
            html = node.innerHTML;
            html = html.replace(regex,text);
            node.innerHTML = html;
        }
    } else {
        for (var i = 0; i < nodes.length; i++) {
            node = nodes[i];
            html = node.innerHTML;
            html = html.replace(regex,text);
            node.innerHTML = html;
        }
    }
}

function BaseContent(url,id,title,description,mtype,ptype,is_folderish,rstate,size) {
    /* base class for portal contents */

    this.getURL = url;
    this.getId = id;

    if (title) { this.Title = title; }
    else { this.Title = id; }

    this.Description = description;
    this.meta_type = mtype;
    this.Type = ptype;
    this.is_folderish = eval(is_folderish);
    this.review_state = rstate;
    this.getObjSize = size;
}

function Iterator(object) {
    /* a basic iterator object */
    object.iterator = 0;
    object.current = null;
    object.init = function (index) {
        if (!index) { index = 0; }
        this.iterator = index;
        this.current = this.getitem[index];
    }
    object.next = function () {
        if (this.iterator <= this.end) { this.iterator++; }
        this.current = this.getitem[this.iterator];
    }
    object.previous = function () {
        if (this.iterator > 0) { this.iterator--; }
        this.current = this.getitem[this.iterator];
    }
    object.at_end = function () {
        if (this.iterator >= this.end) { return true; }
        return false;
    }
}

function List(object) {
    /* a basic list object */
    object.getitem = new Array();
    object.len = function () { return this.getitem.length; }
    object.push = function (item) { this.getitem.push(item); }
    /* more pythonic alias for push ;) */
    object.additem = function (item) { this.getitem.push(item); }
}

function Batch_getLinkFor(index) {
    /* return a navigation item for index */
    var text = index + 1;

    if (index >= 1) { index = index * this.b_size; }
    if (index >= this.len()) { index = this.len() - 1; }
    if (index >= this.start && index < this.start + 1) {
        return '<span>['+text+']</span>\n';
    } else {
        var span = '<span>';
        span += '<a href="'+ this.url +'?b_start='+index+'"';
        span += ' onClick="javascript:return Batch.gotoPage('+index+');">'
        span += text+'</a></span>\n';
        return span;
    }
}

function Batch_showNavigation() {
    /* show navigation */

    if (!W3CDOM) {return false;}

    var navigation = document.getElementById(this.nav_bar);

    if (!navigation) { navigation = document.getElementByClass('listingBar')[0]; }

    if (!navigation) { return; }

    navigation.className = 'listingBar';

    var length = parseInt(this.len() / this.b_size);
    if ((this.len() % this.b_size) != 0) { length++; }

    if (length <= 1) {
        navigation.style.visibility = 'hidden';
        return;
    }

    var start = 0;
    var end = length - 2;
    var html = '';
    var index = 0;
    var items = 0;

    if (end - start > this.max_items_in_navigation) {
        if (this.start - this.max_items_in_navigation < 0) {
            end = this.max_items_in_navigation;
        } else {
            start = this.start - parseInt(this.max_items_in_navigation / 2);
            end = this.start + parseInt(this.max_items_in_navigation / 2);
        }
    }

    if (end > length - 2) {
        end = length - 2;
        start = end - this.max_items_in_navigation;
    }

    if (start < 1) { start = 0; }

    // previous
    if (this.start > 0) {
        index = this.start - this.b_size;
        items = this.b_size;
        if (index < 0) { 
            index = 0;
            items = this.start;
        }
        html += '<span class="previous">';
        if (this.url) {
            html += '<a href="'+this.url+'?b_start='+index+'"';
        } else {
            html += '<a href="#"';
        }
        html += ' onClick="javascript:return Batch.gotoPage('+index+');">'
        html += '<< '+ items + ' ' + label_previous + ' ' + label_items + '</a></span>\n';
    }        

    // next
    if (this.end < this.len()-1) {
        index = this.end;
        if (this.b_size == 1) { index++; }
        items = this.b_size;
        if (index >= this.len()) { 
            items = this.len()-1 - this.end;
            index = this.len()-1 - items;
        }
        if (index + items > this.len() - 1) {
            items = this.len()-1 - this.end;
        }
        html += '<span class="next">';
        if (this.url) {
            html += '<a href="'+this.url+'?b_start='+index+'"';
        } else {
            html += '<a href="#"';
        }
        html += ' onClick="javascript:return Batch.gotoPage('+index+');">'
        html += items + ' ' + label_next + ' ' + label_items + ' >></a></span>\n';
    }        

    // nav
    html = html + this.getLinkFor(0);

    if (start > 1) {
        html = html + '<span>...</span>\n';
    }

    if (start < 1) { start = 1; }

    for (var i = start; i <= end; i++) {
        html = html + this.getLinkFor(i);
    }

    if (end < length - 2) {
        html = html + '<span>...</span>\n';
    }

    html = html + this.getLinkFor(length-1);

    navigation.innerHTML = html;
    navigation.style.visibility = 'visible';
}

function BatchObject() {
    List(this);
    Iterator(this);

    this.max_items_in_navigation = 10;
    this.start = 0;

    this.getLinkFor = Batch_getLinkFor;
    this.showNavigation = Batch_showNavigation;

    this.gotoPage = function (index) {
        if (!W3CDOM) {return false;}
        this.getBatch(index);
        if (this.callbackFunction) {
            eval(this.callbackFunction+'(' + this.start + ');');
        }
        return false;
    }


    this.setNavBar = function (nav_bar) { 
        if (nav_bar) {
            if (this.nav_bar) {
                var navigation = document.getElementById(this.nav_bar);
                navigation.style.visibility = 'hidden';
            }
            this.nav_bar = nav_bar;
        } else { this.nav_bar = 'BatchNavigation'; }
    }
    this.setNavBar();

    this.setCallback = function (callback) {
        if (callback) { this.callbackFunction = callback; }
        else { this.callbackFunction = null; }
    }
    this.setCallback();

    this.setBatchSize = function (b_size) { if (b_size) { this.b_size = b_size; } else { this.b_size = 10; } }
    this.setBatchSize();

    this.setBatchUrl = function (url) { if (url) { this.url = url; } else { this.url = '#'; } }
    this.setBatchUrl();


    this.getBatch = function (start) {
        this.start = start;
        if (this.b_size == 1) { this.end = start; }
        else { this.end = start+this.b_size; }
        if (this.end > this.len()) { this.end = this.len() }
        this.iterator = start;
    }
}

var Batch = new BatchObject();

