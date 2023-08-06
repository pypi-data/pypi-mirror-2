/*
 * first cut: 17. Oct 2006
 * Amberjack 0.9 - Site Tour Creator - Simple. Free. Open Source.
 *
 * $Id: amberjack.js,v 1.17 2007/02/09 20:46:24 aya Exp $
 *
 * Copyright (C) 2006 Arash Yalpani <arash@yalpani.de>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.

 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */

/**
 * Capsulates some static helper functions
 * @author Arash Yalpani
 *
 * This one is mainly for myself, but you can learn from that.
 *
 *
 * How this library works -
 *
 * Hint: to change Amberjack's default behavior, set values
 *       prior to the call to Amberjack.open() (in the wizard's output)
 *
 * 1. Amberjack.open() is called through the HTML code the wizard spit out
 *    you should have includet in your site's template file
 *
 * 2. Amberjack.open()...:
 *
 *    2.1. ... checks for tourId and skinId url param...
 *      2.1.1. ...and stops execution, if no tourId was passed by url
 *      2.2.1. ...and sets skinId to default 'model_t' if none  was
 *                passed by url
 *
 *    2.2. ... reads your web page's DOM structure, searches for the tour
 *             definition (you should have pasted into your site's
 *             template), parses it to create the array 'Amberjack.pages'
 *             and to calculate the tour's params (i.e. number of tour
 *             pages, closeUrl)
 *
 *    2.3. ... fetches control.tpl.js and style.css from
 *             http://amberjack.org/src/stable/skin/<skinname>/
 *             (default setting) OR from your own site, if you have set
 *             Amberjack.BASE_URL's value accordingly
 *
 *    2.4. ... covers your web page's body with a transparent layer (DIV) if
 *             Amberjack.doCoverBody is 'true' which is the default option
 *
 * 3. In step '2.3', I explained that control.tpl.js is fetched from
 *    either amberjack.org or your own server. control.tpl.js is the
 *    template file of a skin and what it does is to call the function
 *    AmberjackControl.open('<div ... </div>') like this. The HTML
 *    inside is the control's template.
 *
 *    3.1. AmberjackControl.open() ...
 *      3.1.1. ... fills the template's placeholders with values
 *      3.1.2. ... creates a DIV for the control
 *      3.1.3. ... fills the DIV's content with the assembled skin
 *                 template (see 2.3)
 *      3.1.4. ... hides the control's close button if no closeUrl
 *                 was specified through wizard's output and
 *                 option 'onCloseClickStay' was not set to true
 *      3.1.4. ... checks for optional Amberjack.ADD_STYLE and
 *                 Amberjack.ADD_SCRIPT and post fetches them if set.
 *                 You can use this to manipulate tour's behaviour
 *                 right after it gets visible. Maximum flexibility!
 *
 * That's it, basically!
 */


var AmberjackBase = {

  /**
   * Proxy alerter
   * @author Arash Yalpani
   *
   * @param str Text for alert
   *
   * @example alert('An error occurred')
   */

  alert: function (str,title) {
  	if (title === undefined)
		title = AmberjackPlone.aj_plone_consts['AlertDefaultTitle'];
    if (jq.fn.dialog)
		jq('<div id="ajMessage">'+str+'<div>').dialog({ modal: true, title: title, zIndex: 500000 });
	else
		alert(title+': ' + str);
	// For "uncomplete" check, remove the submitting (see #656917)
	jq(":submit.submitting").removeClass("submitting");
  },

  log: function (str, e) {
  	if (window.console && window.console.log) {
		window.console.log("Amberjack log:" +str);
		if (e && e.description) window.console.log("Amberjack log:" +e.description);
	}
  },

  /**
   * Returns FIRST matching element by tagname
   * @author Arash Yalpani
   *
   * @param tagName name of tags to filter
   * @return first matching dom node or false if none exists
   *
   * @example getByTagName('div') => domNode
   * @example getByTagName('notexistent') => false
   */

  getByTagName: function (tagName) {
    var els = document.getElementsByTagName(tagName);
    if (els.length > 0) {
      return els[0];
    }

    return false;
  },

  /**
   * Returns an array of matching DOM nodes
   * @author Arash Yalpani
   *
   * @param tagName name of tags to filter
   * @param attrName name of attribute, matching tags must contain
   * @param attrValue value of attribute, matching tags must contain
   * @param domNode optional: dom node to start filtering from
   * @return Array of matching dom nodes
   *
   * @example getElementsByTagNameAndAttr('div', 'class', 'highlight') => [domNode1, domNode2, ...]
   */
   getElementsByTagNameAndAttr: function (tagName, attrName, attrValue, domNode) {
    if (domNode) {
      els = domNode.getElementsByTagName(tagName);
    }
    else {
      els = document.getElementsByTagName(tagName);
    }

    if (els.length === 0) {
      return [];
    }

    var _els = [];
    for (var i = 0; i < els.length; i++) {
      if (attrName == 'class') {
        classNames = '';
        if (els[i].getAttribute('class')) {
          classNames = els[i].getAttribute('class');
        }
        else {
          if (els[i].getAttribute('className')) {
            classNames = els[i].getAttribute('className');
          }
        }

        var reg = new RegExp('(^| )'+ attrValue +'($| )');
        if (reg.test(classNames)) {
          _els.push(els[i]);
        }
      }
      else {
        if (els[i].getAttribute(attrName) == attrValue) {
          _els.push(els[i]);
        }
      }
    }

    return _els;
  },

  /**
   * Returns url param value
   * @author Arash Yalpani
   *
   * @param url The url to be queried
   * @param paramName The params name
   * @return paramName's value or false if param does not exist or is empty
   *
   * @example getUrlParam('http://localhost/?a=123', 'a') => 123
   * @example getUrlParam('http://localhost/?a=123', 'b') => false
   * @example getUrlParam('http://localhost/?a=',    'a') => false
   */

  getUrlParam: function (url, paramName) {
    var urlSplit = url.split('?');
    if (!urlSplit[1]) { // no query
      return false;
    }

    var paramsSplit = urlSplit[1].split('&');
    for (var i = 0; i < paramsSplit.length; i++) {
      paramSplit = paramsSplit[i].split('=');
      if (paramSplit[0] == paramName) {
        return paramSplit[1] ? paramSplit[1] : false;
      }
    }

    return false;
  },

  /**
   * Injects javascript or css file into document
   *
   * @author Arash Yalpani
   *
   * @param url The JavaScript/CSS file's url
   * @param type Either 'script' OR 'style'
   * @param onerror Optional: callback handler if loading did not work
   *
   * @example loadScript('http://localhost/js/dummy.js', function(){AmberjackBase.alert('could not load')})
   * Note that a HEAD tag needs to be existent in the current document
   */

  postFetch: function (url, type, onerror) {
    if (type === 'script') {
      scriptOrStyle = document.createElement('script');
      scriptOrStyle.type = 'text/javascript';
      scriptOrStyle.src  = url;
    }
    else {
      scriptOrStyle = document.createElement('link');
      scriptOrStyle.type = 'text/css';
      scriptOrStyle.rel  = 'stylesheet';
      scriptOrStyle.href = url;
    }

    if (onerror) { scriptOrStyle.onerror = onerror; }

    var head = AmberjackBase.getByTagName('head');
    if (head) {
      head.appendChild(scriptOrStyle);
      return ;
    }

    AmberjackBase.alert('HEAD tag is missing.');
  }
};


/**
 * Amberjack Control class
 * @author Arash Yalpani
 */

AmberjackControl = {

  /**
   * Callback handler for template files. Takes template HTML and fills placeholders
   * @author Arash Yalpani
   *
   * @param tplHtml HTML code including Amberjack placeholders
   *
   * @example AmberjackControl.open('<div>{body}</div>')
   * Note that this method should be called directly through control.tpl.js files
   */

  open: function (tplHtml) {
    var urlSplit = false;
    var urlQuery = false;

    tplHtml = tplHtml.replace(/{skinId}/, Amberjack.skinId);
    if (Amberjack.pages[Amberjack.pageId].prevUrl) {
      var prevUrl = Amberjack.pages[Amberjack.pageId].prevUrl;
      urlSplit = prevUrl.split('?');
      urlQuery = urlSplit[1] ? urlSplit[1] : false;
      if (Amberjack.urlPassTourParams) {
        prevUrl+= (urlQuery ? '&' : '?') + 'tourId=' + Amberjack.tourId + (Amberjack.skinId ? '&skinId=' + Amberjack.skinId : '');
      }

      tplHtml = tplHtml.replace(/{prevClick}/,   "location.href='" + prevUrl + "';return false;");
      tplHtml = tplHtml.replace(/{prevClass}/,   '');
    }
    else {
      tplHtml = tplHtml.replace(/{prevClick}/,   'return false;');
      tplHtml = tplHtml.replace(/{prevClass}/,   'disabled');
    }

    if (Amberjack.pages[Amberjack.pageId].nextUrl && AmberjackPlone.checkAllDoitmanually()) {
      var nextUrl = Amberjack.pages[Amberjack.pageId].nextUrl;
      urlSplit = nextUrl.split('?');
      urlQuery = urlSplit[1] ? urlSplit[1] : false;
      if (Amberjack.urlPassTourParams && (!Amberjack.hasExitPage || Amberjack.pages[nextUrl].nextUrl)) { // do not append params for exit page (if exit page exists)
        nextUrl+= (urlQuery ? '&' : '?') + 'tourId=' + Amberjack.tourId + (Amberjack.skinId ? '&skinId=' + Amberjack.skinId : '');
      }

      tplHtml = tplHtml.replace(/{nextClick}/,       "location.href='" + nextUrl + "';return false;");
      tplHtml = tplHtml.replace(/{nextClass}/,       '');
	  tplHtml = tplHtml.replace(/{nextTitle}/,       AmberjackPlone.aj_plone_consts['GoToNextStepLinkMessage']);
    }
    else {
      tplHtml = tplHtml.replace(/{nextClick}/,       'return false;');
      tplHtml = tplHtml.replace(/{nextClass}/,       'disabled');
	  tplHtml = tplHtml.replace(/{nextTitle}/,       AmberjackPlone.aj_plone_consts['GoToNextStepLinkErrorMessage']);
    }

    tplHtml = tplHtml.replace(/{textOf}/,          Amberjack.textOf);
    tplHtml = tplHtml.replace(/{textClose}/,       Amberjack.textClose);
    tplHtml = tplHtml.replace(/{textPrev}/,        Amberjack.textPrev);
    tplHtml = tplHtml.replace(/{textNext}/,        Amberjack.textNext);
    tplHtml = tplHtml.replace(/{currPage}/,        Amberjack.pageCurrent);
    tplHtml = tplHtml.replace(/{pageCount}/,       Amberjack.pageCount);
	
	tplHtml = tplHtml.replace(/{body}/,            Amberjack.pages[Amberjack.pageId].content.innerHTML);
	
    var div = document.createElement('div');
    div.id = 'AmberjackControl';
    div.innerHTML = tplHtml;

    document.body.appendChild(div);

    // Amberjack.doHighlight();

    // No URL was set AND no click-close-action was configured:
    if (!Amberjack.closeUrl && !Amberjack.onCloseClickStay) {
      document.getElementById('ajClose').style.display = 'none';
    }

    // post fetch a CSS file you can define by setting Amberjack.ADD_STYLE
    // right before the call to Amberjack.open();
    if (Amberjack.ADD_STYLE) {
      AmberjackBase.postFetch(Amberjack.ADD_STYLE, 'style');
    }

    // post fetch a script you can define by setting Amberjack.ADD_SCRIPT
    // right before the call to Amberjack.open();
    if (Amberjack.ADD_SCRIPT) {
      AmberjackBase.postFetch(Amberjack.ADD_SCRIPT, 'script');
    }
    AmberjackPlone.init();
  },

  /**
   * Removes AmberjackControl div from DOM
   * @author Arash Yalpani
   *
   * @example AmberjackControl.close()
   */

  close: function() {
    e = document.getElementById('AmberjackControl');
    e.parentNode.removeChild(e);
  }
};


/**
 * Amberjack's main class
 * @author Arash Yalpani
 */

Amberjack = {

  // constants

  BASE_URL: 'http://amberjack.org/src/stable/', // do not forget trailing slash!

  // explicit attributes

  // - set these through url (...&tourId=MyTour&skinId=Safari...)
  // - OR in your tour template right above the call to Amberjack.open()

  tourId:    false,     // mandatory: if not set, tour will not open
  skinId:    false,     // optional: if not set, skin "model_t" will be used

  // - set these in your tour template right above the call to Amberjack.open()

  textOf:    'of',      // text of splitter between "2 of 3"
  textClose: 'x',       // text of close button
  textPrev:  '&laquo;', // text of previous button
  textNext:  '&raquo;', // text of next button

  // - set set these in your tour template right above the call to Amberjack.open()

  onCloseClickStay     : false, // set this to 'true', if you want the close button to close tour but remain on current page
  doCoverBody          : true,  // set this to 'false' if you don't want your site's page to be covered
  bodyCoverCloseOnClick: false, // set this to 'true', if a click on the body cover should force it to close
  urlPassTourParams    : true,  // set this to false, if you have hard coded the tourId and skinId in your tour
                                //     template. the tourId and skindId params will not get passed on prev/next button click




  // private attributes - don't touch

  pageId:    false,
  pages:     {},
  pageCount: 0,
  hasExitPage: false,
  interval: false,

  /**
   * use inside getIdPart
   */
  pageIdParts: {'title': 0, 'xpath': 1, 'xcontent': 2},  

  /**
   * Gets the tourId from the url or from a cookie 'ajcookie_tourId'
   *
   * @author Massimo Azzolini
   *
   */
  getTourId: function(){
	Amberjack.tourId = Amberjack.tourId ? Amberjack.tourId : AmberjackBase.getUrlParam(location.href, 'tourId');
	if (!Amberjack.tourId) {
      Amberjack.tourId = Amberjack.readCookie('ajcookie_tourId');
	  Amberjack.eraseCookie('ajcookie_tourId');
    }
    return Amberjack.tourId;
  },

  /**
   * Gets the skinId from the url or from a cookie 'ajcookie_skinId'
   *
   * @author Massimo Azzolini
   *
   */
    getSkinId: function(){
	Amberjack.skinId = Amberjack.skinId ? Amberjack.skinId : AmberjackBase.getUrlParam(location.href, 'skinId');
	if (!Amberjack.skinId) {
      Amberjack.skinId = Amberjack.readCookie('ajcookie_skinId');
	  Amberjack.eraseCookie('ajcookie_skinId');
    }
    return Amberjack.skinId;
  },

  /**
   * Gets the pageId form the cookie ajcookie_pageCurrent
   */
  getCurrentPageId: function(_children){
  	// try to get the pageCurrent: look at the cookie, if available, else let's assume it's the No 1
	pageCurrent = AmberjackBase.getUrlParam(location.href, 'pageCurrent');
	pageCurrent = pageCurrent? pageCurrent : Amberjack.readCookie('ajcookie_pageCurrent');
	Amberjack.eraseCookie('ajcookie_pageCurrent');
    if (!pageCurrent) {
        pageCurrent = 0
    } else {
		if (AmberjackPlone.canMoveToNextStep()){
			pageCurrent -= 1
		} else {
		    pageCurrent -= 2	
		}
	}
    pageId = Amberjack.getPageId(_children, pageCurrent);
    if (!(Amberjack.matchPage(_children[pageCurrent]) && _children[pageCurrent].innerHTML !== '')) {
        pageId = false;
    }
	return {pageId:pageId, pageCurrent:pageCurrent + 1};
  },

  /**
   * Initializes tour, creates transparent layer and causes AmberjackControl
   * to open the skin's template (control.tpl.js) into document. Call this
   * manually right after inclusion of this library. Don't forget to pass
   * tourId param through URL to show tour!
   *
   * Iterates child DIVs of DIV.ajTourDef, extracts tour pages
   *
   * @author Arash Yalpani
   *
   * @example Amberjack.open()
   * Note that a HEAD tag needs to be existent in the current document
   */

  open: function() {
    Amberjack.tourId = Amberjack.getTourId();
    Amberjack.skinId = Amberjack.getSkinId();

    if (!Amberjack.tourId) { // do nothing if tourId is not passed 
      return;
    }


    if (!Amberjack.skinId) { // set default skinId
      Amberjack.skinId = 'light_grey';
    }

    var tourDef = false;
    var tourDefElements = AmberjackBase.getElementsByTagNameAndAttr('div', 'class', 'ajTourDef');
    for (i = 0; i < tourDefElements.length; i++) {
      if (tourDefElements[i].getAttribute('id') === Amberjack.tourId) {
        tourDef = tourDefElements[i];
      }
    }

    if (!tourDef) {
      AmberjackBase.alert('DIV with CLASS "ajTourDef" and ID "' + Amberjack.tourId + '" is not defined.');
    }
	
    // Is there a specified closeUrl (title attribute of DIV.ajTourDef)?
    // Don't show close button if not set
    Amberjack.closeUrl = tourDef.getAttribute('title') ? tourDef.getAttribute('title') : false;

    var children = tourDef.childNodes;
    var _children = []; // cleaned up version...
    for (i = 0; i < children.length; i++) {
      if (!children[i].tagName || children[i].tagName.toLowerCase() != 'div') { continue ; }
      _children.push(children[i]);
    }

    // init tour pages
    for (i = 0; i < _children.length; i++) {
      Amberjack.pages[Amberjack.getPageId(_children, i)] = {};
    }

    for (i = 0; i < _children.length; i++) {
      if (!_children[i].tagName || _children[i].tagName.toLowerCase() != 'div') { continue ; }

      if (!_children[i].getAttribute('title')) {
        AmberjackBase.alert('Attribute TITLE is missing.');
        return;
      }

      Amberjack.pageCount++;
      if (i >= 1 && i < _children.length) {
        Amberjack.pages[Amberjack.getPageId(_children, i)].prevUrl = _children[i - 1].getAttribute('title');
      }
      if (i < _children.length - 1) {
        Amberjack.pages[Amberjack.getPageId(_children, i)].nextUrl = _children[i + 1].getAttribute('title');
      }
	  Amberjack.pages[Amberjack.getPageId(_children, i)].content = _children[i]
    }
    
	// get the current page Id
	currPage = Amberjack.getCurrentPageId(_children);
	Amberjack.pageId = currPage.pageId
	Amberjack.pageCurrent = currPage.pageCurrent
	
    if (_children[i-1].innerHTML === '') { // empty page div reduces pageCount by 1
      Amberjack.pageCount = Amberjack.pageCount - 1;
      Amberjack.hasExitPage = true;
    }

    if (!Amberjack.pageId) {
      AmberjackBase.alert('You can: <ul><li><a href="'+Amberjack.BASE_URL+
							'">close the tour</a></li><li><a href="'+Amberjack.BASE_URL+
							'?tourId='+Amberjack.tourId+
							'&skinId='+Amberjack.skinId+
							'">restart the tour</a></li></ul>','Unexpected error!');
    }
	Amberjack.elements = _children
    AmberjackBase.postFetch(Amberjack.PORTAL_URL + 'skin/' + Amberjack.skinId.toLowerCase() + '/control.tpl.js', 'script');
    AmberjackBase.postFetch(Amberjack.PORTAL_URL + 'skin/' + Amberjack.skinId.toLowerCase() + '/style.css', 'style');

    if (Amberjack.doCoverBody) {
      Amberjack.coverBody();
    }
  },
  
  /**
   * Returns a pageId which is a "key" for the page itself
   *
   * @author Massimo Azzolini
   *
   * @param children an array of elements that are tour steps
   * @param pos position of a specific step inside the array 'children'
   *
   */
  getPageId: function(children, pos){
    var element = children[pos];
	var title = element.getAttribute('title');
	var xpath = element.getAttribute('xpath');
	var xcontent = element.getAttribute('xcontent');
	return '(' + title + ';' + xpath + ';' + xcontent + ';' + pos + ')'; 
  },

  /**
   * Returns a part of a PageId: title, xpath, xcontent.
   *
   * @author Massimo Azzolini
   *
   * @param id the pageId, commonly generated from getPageId method
   * @param part the part to extract. See Amberjack.pageIdParts
   *
   */
  getIdPart: function(id, part) {
	return id.substr(1, id.length-2).split(';')[Amberjack.pageIdParts[part]];
  },

  /**
   * Checks if the url and the title matches, if so tests if there is an xpath and if the content 
   * of the xpath-ed element contains what's in xcontent 
   * @author Massimo Azzolini
   *
   * @param element the element to be checked
   *
   */
  matchPage: function(element){
	var title = element.getAttribute('title');
	if (title === AmberjackPlone.aj_any_url) {
        return true
    }
	if (title.substr(title.length-1)==='/') {
		title = title.substr(0, title.length-1)
	}
	var loc = window.location.protocol +'//'+ window.location.host + window.location.pathname;
	if (this.urlMatch(title) || this.urlMatch(title+'/')) {
		var xpath = element.getAttribute('xpath');
		var xcontent = element.getAttribute('xcontent');
		if (xpath){
			// needs jquery
			if (jq) {
				if (xcontent === AmberjackPlone.aj_xpath_exists){
					return (jq(xpath).length > 0)
				}
				
				return (jq.trim(jq(xpath).text()) === xcontent);
			} else {
				return true;
			}
		} else {
			return true;
		}
	} else {
		return false;
	}
  },

  /**
   * Checks if passed href is *included* in current location's href
   * 
   * [edit] made some modification for working better in Plone
   *  
   * @author Arash Yalpani
   * @author Giacomo Spettoli
   *
   * @param href URL to be matched against
   *
   * @example Amberjack.urlMatch('http://mysite.com/domains/')
   */
  urlMatch: function(href) {
  	  var href = unescape(href);
  	  var params;
  	  var hasParams=false;
  	  if (href.indexOf('?')!=-1){						//added check for get the url parameters otherwise if the href contains them i get a "page not found" error
  	  params=href.substring(href.indexOf('?'));
  	  hasParams=true;
  	  }
	  var loc = unescape(window.location.protocol +'//'+ window.location.host + window.location.pathname) + (hasParams ? params : '');
	  if (href.match("portal_factory"))
		  return (loc.indexOf(href) != -1);
	  else return loc === href;
  },


  /**
    * Creates a cookie
    *
    * @param name cookie's name
    * @param value cookie's value
    * @param days cookie's duration in days 
    *
    */
  createCookie: function(name,value,days) {
	if (days) {
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		var expires = "; expires="+date.toGMTString();
	}
	else var expires = "";
	document.cookie = name+"="+value+expires+"; path=/";
  },

  /**
    * Reads a cookie
    *
    * @param name cookie's name
    *
    */
  readCookie: function(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)===' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length,c.length);
	}
	return null;
  },

  /**
    * Erases a cookie
    *
    * @param name cookie's name
    *
    */
  eraseCookie: function(name) {
	createCookie(name,"",-1);
  },


  /**
   * Return height of inner window
   * Copied and modified:
   * http://www.dynamicdrive.com/forums/archive/index.php/t-10373.html
   *
   * @author Arash Yalpani
   * @example Amberjack.getWindowInnerHeight()
   */
  getWindowInnerHeight: function() {
    var yInner;

    if (window.innerHeight && window.scrollMaxY) {
      yInner = window.innerHeight + window.scrollMaxY;
    }
    else if (document.body.scrollHeight > document.body.offsetHeight){ // all but Explorer Mac
      yInner = document.body.scrollHeight;
    }
    else if (document.documentElement && document.documentElement.scrollHeight > document.documentElement.offsetHeight){ // Explorer 6 strict mode
      yInner = document.documentElement.scrollHeight;
    }
    else { // Explorer Mac...would also work in Mozilla and Safari
      yInner = document.body.offsetHeight;
    }

    var windowWidth, windowHeight;
    if (self.innerHeight) { // all except Explorer
      windowHeight = self.innerHeight;
    }
    else if (document.documentElement && document.documentElement.clientHeight) { // Explorer 6 Strict Mode
      windowHeight = document.documentElement.clientHeight;
    }
    else if (document.body) { // other Explorers
      windowHeight = document.body.clientHeight;
    }

    // for small pages with total height less then height of the viewport
    return (yInner < windowHeight) ? windowHeight : yInner;
  },

  /**
   * Creates transparent layer and places it in the document, in front of
   * all other layers (through CSS z-index)
   * @author Arash Yalpani
   *
   * @example Amberjack.coverBody()
   */
  coverBody: function() {
    var div = document.createElement('div');
    div.id = 'ajBodyCover';

    div.style.height = Amberjack.getWindowInnerHeight() + 'px';

    if (Amberjack.bodyCoverCloseOnClick) {
      div.onclick = function() {
        Amberjack.uncoverBody();
      };
    }

    document.body.appendChild(div);
    Amberjack.interval = window.setInterval(Amberjack.refreshCover, 2000);
  },

  /**
   * refreshes transparent layer's height
   * @author Arash Yalpani
   *
   * @example Amberjack.refreshCover()
   */
  refreshCover: function() {
    document.getElementById('ajBodyCover').style.height = Amberjack.getWindowInnerHeight() + 'px';
  },

  /**
   * Removes transparent layer from document
   * @author Arash Yalpani
   *
   * @example Amberjack.uncoverBody()
   */
  uncoverBody: function() {
    window.clearInterval(Amberjack.interval);
    document.body.removeChild(document.getElementById('ajBodyCover'));
  },


  /**
   * Gets called, whenever the user clicks on the close button of Amberjack control
   * @author Arash Yalpani
   *
   * @example Amberjack.close()
   */
  close: function() {
    if (Amberjack.onCloseClickStay) {
      AmberjackControl.close();
      if (Amberjack.doCoverBody) {
        Amberjack.uncoverBody();
      }
      //delete cookies
      Amberjack.eraseCookie('ajcookie_tourId');
      Amberjack.eraseCookie('ajcookie_pageCurrent');
	  Amberjack.eraseCookie('next_tours_id');
      return null;
    }

    if (Amberjack.closeUrl) {
      window.location.href = Amberjack.closeUrl;
    }
    //delete cookies
    Amberjack.eraseCookie('ajcookie_tourId');
	Amberjack.eraseCookie('ajcookie_pageCurrent');
	Amberjack.eraseCookie('next_tours_id');
	
    return null;
  }
};
