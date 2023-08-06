        
/* locators & methods used in windmill */
        
var windmillLocators = ['id','link','xpath','jsid', 'name','value','classname', 'tagname','label','jquery'];

var windmillMethods ={ 'click': {'locator': true, 'option': false}, 
                   'radio': {'locator': true, 'option': false },
                   'check': {'locator': true, 'option': false },
                   'select': {'locator': true, 'option': 'option,val,index'},
                   'type': {'locator': true, 'option': 'text'},
                   'editor':{'locator':true,'option':'editor'},
                   'editorSelect': {'locator': true, 'option': 'text,bookmark'},
                   'waits.sleep': {'locator': false, 'option': 'milliseconds' },
                   'waits.forElement': {'locator': true, 'option': 'timeout' },
                   'waits.forPageLoad': {'locator': false, 'option': 'timeout' },
                   'highlight' : {'locator': true, 'option': false }
                  };
                  

var helpers = new function(){
                      
                  this.normalizeNewlines = function(text){
                          return text.replace(/\r\n|\r/g, "\n");
                  };


                  this.repAll = function (OldString, FindString, ReplaceString) {
                        var SearchIndex = 0;
                        var NewString = ""; 
                        while (OldString.indexOf(FindString,SearchIndex) != -1)    {
                          NewString += OldString.substring(SearchIndex,OldString.indexOf(FindString,SearchIndex));
                          NewString += ReplaceString;
                          SearchIndex = (OldString.indexOf(FindString,SearchIndex) + FindString.length);         
                        }
                        NewString += OldString.substring(SearchIndex,OldString.length);
                        return NewString;
                      };

                  /**
                   * Replace multiple sequential spaces with a single space, and then convert &nbsp; to space.
                   */
                  this.normalizeSpaces = function(text)
                  {
                      // IE has already done this conversion, so doing it again will remove multiple nbsp
                      if (navigator.userAgent.indexOf('MSIE') != -1)
                      {
                          return text;
                      }

                      // Replace multiple spaces with a single space
                      // TODO - this shouldn't occur inside PRE elements
                      text = text.replace(/\ +/g, " ");

                      // Replace &nbsp; with a space
                      var nbspPattern = new RegExp(String.fromCharCode(160), "g");
                      if (navigator.userAgent.indexOf('Safari') != -1) {
                      return helpers.repAll(text, String.fromCharCode(160), " ");
                      } else {
                      return text.replace(nbspPattern, " ");
                      }
                  };

                  this.getParentWindow = function(node){
                        var ownerDoc = node.ownerDocument;
                        var win = null;
                        if (ownerDoc.defaultView){
                          win = ownerDoc.defaultView;
                        }
                        else {
                          win = ownerDoc.parentWindow;
                        }
                        if (win === null){
                          win = window;
                        }
                        
                        return win;
                      };

                  };

                  
var windEvents = new function() {

                      // Returns the text in this element
                      this.getText = function(element) {
                        var text = "";

                          text = windEvents.getTextContent(element);
                   
                        text = helpers.normalizeNewlines(text);
                        text = helpers.normalizeSpaces(text);
                        return jQuery.trim(text);
                      };

                      this.getTextContent = function(element, preformatted) {
                          var text = null;

                          if (element.nodeType == 3
                          /*Node.TEXT_NODE*/
                          ) {
                              text = element.data;
                              if (!preformatted) {
                                  text = text.replace(/\n|\r|\t/g, " ");

                              }
                              return text;

                          }
                          if (element.nodeType == 1
                          /*Node.ELEMENT_NODE*/
                          ) {

                              var childrenPreformatted = preformatted || (element.tagName == "PRE");
                              text = "";
                              for (var i = 0; i < element.childNodes.length; i++) {
                                  var child = element.childNodes.item(i);
                                  text += windEvents.getTextContent(child, childrenPreformatted);

                              }
                              // Handle block elements that introduce newlines
                              // -- From HTML spec:
                              //<!ENTITY % block
                              //     "P | %heading; | %list; | %preformatted; | DL | DIV | NOSCRIPT |
                              //      BLOCKQUOTE | F:wORM | HR | TABLE | FIELDSET | ADDRESS">
                              //
                              // TODO: should potentially introduce multiple newlines to separate blocks
                              if (element.tagName == "P" || element.tagName == "BR" || element.tagName == "HR" || element.tagName == "DIV") {
                                  text += "\n";

                              }
                              return text;

                          }
                          return '';

                      };

                      this.createEventObject = function(element, controlKeyDown, altKeyDown, shiftKeyDown, metaKeyDown) {
                          var evt = element.ownerDocument.createEventObject();
                          evt.shiftKey = shiftKeyDown;
                          evt.metaKey = metaKeyDown;
                          evt.altKey = altKeyDown;
                          evt.ctrlKey = controlKeyDown;
                          return evt;

                      };


                      /* Fire an event in a browser-compatible manner */
                      this.triggerEvent = function(element, eventType, canBubble, controlKeyDown, altKeyDown, shiftKeyDown, metaKeyDown) {
                          
						  var evt = null;
                          canBubble = (typeof(canBubble) === undefined) ? true: canBubble;
                          if (element.fireEvent && navigator.userAgent.indexOf('MSIE') != -1) {
                              evt = windEvents.createEventObject(element, controlKeyDown, altKeyDown, shiftKeyDown, metaKeyDown);
                              element.fireEvent('on' + eventType, evt);
                          }
                          else {
                              evt = document.createEvent('HTMLEvents');
                              evt.shiftKey = shiftKeyDown;
                              evt.metaKey = metaKeyDown;
                              evt.altKey = altKeyDown;
                              evt.ctrlKey = controlKeyDown;

                              evt.initEvent(eventType, canBubble, true);
                              element.dispatchEvent(evt);

                          }

                      };

                      this.getKeyCodeFromKeySequence = function(keySequence) {
                          var match = /^\\(\d{1,3})$/.exec(keySequence);
                          if (match !== null) {
                              return match[1];

                          }
                          match = /^.$/.exec(keySequence);
                          if (match !== null) {
                              return match[0].charCodeAt(0);

                          }
                          // this is for backward compatibility with existing tests
                          // 1 digit ascii codes will break however because they are used for the digit chars
                          match = /^\d{2,3}$/.exec(keySequence);
                          if (match !== null) {
                              return match[0];

                          }

                      };

                      this.triggerKeyEvent = function(element, eventType, keySequence, canBubble, controlKeyDown, altKeyDown, shiftKeyDown, metaKeyDown) {
                          var keycode = windEvents.getKeyCodeFromKeySequence(keySequence);
                          canBubble = (typeof(canBubble) === undefined) ? true: canBubble;
                          //Make sure we don't call fireEvent otuside of IE, mootools adds this to the prototype
                          if (element.fireEvent && navigator.userAgent.indexOf('MSIE') != -1) {
                              var keyEvent = windEvents.createEventObject(element, controlKeyDown, altKeyDown, shiftKeyDown, metaKeyDown);
                              keyEvent.keyCode = keycode;
                              element.fireEvent('on' + eventType, keyEvent);

                          }
                          else {
                              var evt;
                              if (window.KeyEvent) {
                                  evt = document.createEvent('KeyEvents');
                                  evt.initKeyEvent(eventType, true, true, window, controlKeyDown, altKeyDown, shiftKeyDown, metaKeyDown, keycode, keycode);
                              } 
                              else {
                                  evt = document.createEvent('UIEvent');
                                  evt.shiftKey = shiftKeyDown;
                                  evt.metaKey = metaKeyDown;
                                  evt.altKey = altKeyDown;
                                  evt.ctrlKey = controlKeyDown;

                                  evt.initUIEvent(eventType, true, true, window, 1);
                                  evt.charCode = keycode;
                                  evt.keyCode = keycode;
                                  evt.which = keycode;
                              }
                              element.dispatchEvent(evt);
                          }
                      };

                      /* Fire a mouse event in a browser-compatible manner */
                      this.triggerMouseEvent = function(element, eventType, canBubble, clientX, clientY, controlKeyDown, altKeyDown, shiftKeyDown, metaKeyDown) {
                          clientX = clientX ? clientX: 0;
                          clientY = clientY ? clientY: 0;
                          
                          //LOG.warn("windEvents.triggerMouseEvent assumes setting screenX and screenY to 0 is ok");
                          var screenX = 0;
                          var screenY = 0;
						  var evt = null;
						  
                          canBubble = (typeof(canBubble) === undefined) ? true: canBubble;

                          if (element.fireEvent && navigator.userAgent.indexOf('MSIE') != -1) {
                              //LOG.info("element has fireEvent");
                              evt = windEvents.createEventObject(element, controlKeyDown, altKeyDown, shiftKeyDown, metaKeyDown);
                              evt.detail = 0;
                              evt.button = 1;
                              evt.relatedTarget = null;
                              if (!screenX && !screenY && !clientX && !clientY) {
                                  //element.click();
                                  if (eventType == "click") {element.click(); }
                                  else { element.fireEvent('on' + eventType); }
                                  //eval("element." + eventType + "();");
                              }
                              else {
                                  evt.screenX = screenX;
                                  evt.screenY = screenY;
                                  evt.clientX = clientX;
                                  evt.clientY = clientY;

                                  // when we go this route, window.event is never set to contain the event we have just created.
                                  // ideally we could just slide it in as follows in the try-block below, but this normally
                                  // doesn't work.  This is why I try to avoid this code path, which is only required if we need to
                                  // set attributes on the event (e.g., clientX).
                                  try { window.event = evt; }
                                  catch(e) {
                                      // getting an "Object does not support this action or property" error.  Save the event away
                                      // for future reference.
                                      // TODO: is there a way to update window.event?
                                      // work around for http://jira.openqa.org/browse/SEL-280 -- make the event available somewhere:
                                  }
                                  element.fireEvent('on' + eventType, evt);

                              }

                          }
                          else {
         
                              //LOG.info("element doesn't have fireEvent");
                              evt = document.createEvent('MouseEvents');
                              if (evt.initMouseEvent) {
                                  //LOG.info("element has initMouseEvent");
                                  //Safari
                                  evt.initMouseEvent(eventType, canBubble, true, document.defaultView, 1, screenX, screenY, clientX, clientY, controlKeyDown, altKeyDown, shiftKeyDown, metaKeyDown, 0, null);

                              }
                              else {
                                  //LOG.warn("element doesn't have initMouseEvent; firing an event which should -- but doesn't -- have other mouse-event related attributes here, as well as controlKeyDown, altKeyDown, shiftKeyDown, metaKeyDown");
                                  evt.initEvent(eventType, canBubble, true);
                                  evt.shiftKey = shiftKeyDown;
                                  evt.metaKey = metaKeyDown;
                                  evt.altKey = altKeyDown;
                                  evt.ctrlKey = controlKeyDown;

                              }
                         
                              element.dispatchEvent(evt);

                          }

                      };

                  };

                
                  
var controller = new function() {


                  //Click function for Mozilla with Chrome
                  this.click = function(element){
                      windEvents.triggerEvent(element, 'focus', false);

                      // Add an event listener that detects if the default action has been prevented.
                      // (This is caused by a javascript onclick handler returning false)
                      // we capture the whole event, rather than the getPreventDefault() state at the time,
                      // because we need to let the entire event bubbling and capturing to go through
                      // before making a decision on whether we should force the href
                      var savedEvent = null;
						
					  if (element.addEventListener) { // Mozilla, Netscape, Firefox
							element.addEventListener('click', function(evt){
								savedEvent = evt;
							}, false);
					  }
					  else { //IE
						  	element.attachEvent('onclick', function(evt) {
	                          	savedEvent = evt;
	                      	});
					  }
                     
                      
                      // Trigger the event.
                      windEvents.triggerMouseEvent(element, 'mousedown', true);
                      windEvents.triggerMouseEvent(element, 'mouseup', true);

                      //if click options are attached for keyboard keys
                    /*  if (paramObject.options){
                        var arr = paramObject.options.split(',');
                        arr.unshift(element, 'click', true, null, null);
                        windEvents.triggerMouseEvent.apply(this, arr);
                      }
                      else {*/ windEvents.triggerMouseEvent(element, 'click', true);// }

                      try {
                          
                        // Perform the link action if preventDefault was set.
                        if (savedEvent !== null && !savedEvent.getPreventDefault()) {
                            if ((element.href) && (element.href != "#")) {
                                //windmill.controller.open({"url": element.href, 'reset':false});
                                if (element.target.length > 0) {
                                    
                                    window.location=element.href;
                                }
                                else {
                                    helpers.getParentWindow(element).location = element.href;
                                }
                            } 
                            else {
                                
                                var itrElement = element;
                                while (itrElement !== null) {
                                  if ((itrElement.href) && (itrElement.href != "#")) {
                                    helpers.getParentWindow(itrElement).location = itrElement.href;
                                    //windmill.controller.open({"url": itrElement.href, 'reset':false});
                                    break;
                                  }
                                  itrElement = itrElement.parentNode;
                                }
                            }
                        }
                      }
                      catch(err){}
                  };


                  this.check = function(element){
                    return this.click(element);    
                  };

                  
				  this.radio = function(element){
				      if(element) {
				          return jq(element).click();
				      } 
				  };


                  this.doubleClick = function(element) {
                   //Look up the dom element, return false if its not there so we can report failure
                       windEvents.triggerEvent(element, 'focus', false);
                       windEvents.triggerMouseEvent(element, 'dblclick', true);
                       windEvents.triggerEvent(element, 'blur', false);
                  };

                  //Type Function
                  this.type = function (element,text){
                     //clear the box
                     element.value = '';
                     //Get the focus on to the item to be typed in, or selected
                     windEvents.triggerEvent(element, 'focus', false);
                     windEvents.triggerEvent(element, 'select', true);
                      
                     //Make sure text fits in the textbox
                     var maxLengthAttr = element.getAttribute("maxLength");
                     var actualValue = text;
                     var stringValue = text;
                      
                     if (maxLengthAttr !== null) {
                       var maxLength = parseInt(maxLengthAttr, 10);
                       if (stringValue.length > maxLength) {
                         //truncate it to fit
                         actualValue = stringValue.substr(0, maxLength);
                       }
                     }
                     
                     var s = actualValue;
                     for (var c = 0; c < s.length; c++){
                       windEvents.triggerKeyEvent(element, 'keydown', s.charAt(c), true, false,false, false,false);
                       windEvents.triggerKeyEvent(element, 'keypress', s.charAt(c), true, false,false, false,false); 
                       if (s.charAt(c) == "."){
                         element.value += s.charAt(c);
                       }
                       windEvents.triggerKeyEvent(element, 'keyup', s.charAt(c), true, false,false, false,false);
                     }
                     //if for some reason the key events don't do the typing
                     if (element.value != s){
                       element.value = s;
                     }
                      
                     // DGF this used to be skipped in chrome URLs, but no longer.  Is xpcnativewrappers to blame?
                     //Another wierd chrome thing?
                     windEvents.triggerEvent(element, 'change', true);
                   };
                   
                   this.editor = function (editText,id){
                       tinyMCE.get(id).setContent(editText); 
                   };
                   
                   
                   this.select = function (element,param,value) {
                          
                          //if the index selector was used, select by index
                          if (param=='index'){
                            element.options[param].selected = true;
                            return true;
                          }
                              
                          //Sometimes we can't directly access these at this point, not sure why
                          try {
                            if (element.options[element.options.selectedIndex].text == value){
                              return true;
                            }
                          } catch(err){}
                          try {  
                            if (element.options[element.options.selectedIndex].value == value){
                              return true;
                            }
                          } catch(err){}
                          
                          windEvents.triggerEvent(element, 'focus', false);
                          var optionToSelect = null;
                          for (var opt = 0; opt < element.options.length; opt++){
                            try {
                              var el = element.options[opt];
                              if (param=='option'){
                                if(el.innerHTML.indexOf(value) != -1){
                                  if (el.selected && el.options[opt] == optionToSelect){
                                    continue;
                                  }
                                  optionToSelect = el;
                                  optionToSelect.selected = true;
                                  windEvents.triggerEvent(element, 'change', true);
                                  break;
                                }
                              }
                              else {
                                 if(el.value.indexOf(value) != -1){
                                    if (el.selected && el.options[opt] == optionToSelect){
                                      continue;
                                    }
                                    optionToSelect = el;
                                    optionToSelect.selected = true;
                                    windEvents.triggerEvent(element, 'change', true);
                                    break;
                                  }
                              }
                            }
                            catch(err){}
                          }
                          if (optionToSelect === null){
                            throw "Unable to select the specified option.";
                          }
                        };
                   
                   
                   this.editorSelect = function (id,bookmark){
                      tinyMCE.get(id).selection.moveToBookmark(eval("(" + bookmark + ")"));
                  //solution for show the tiny buttons that appear only when onMouseUp  
                    windEvents.triggerMouseEvent(tinyMCE.get(id).selection.getNode(), 'mouseup', true);
                   };


                   };
                   
                   

                   
var elementslib = new function(){
                   
                    var domNode = null;
                    //keep track of the locators we cant get via the domNode
                    var locators = {};
                    
                    //element constructor
                    this.Element = function(node){
                      if (node){ domNode = node;}
                      if (node.id){ id = node.id;}
                      if (node.name){ name = node.name;}
                      return domNode;
                    };
                    //getters
                    this.Element.exists = function(){
                      if (domNode){ return true; }
                      else{ return false; }
                    };
                    this.Element.getNode = function(){
                      return domNode;
                    };
                    //setters
                    this.Element.ID = function(s){
                      locators.id = s;
                      domNode = nodeSearch(nodeById, s);
                      return returnOrThrow(s);
                    };
                    this.Element.NAME = function(s){
                       locators.name = s;
                       domNode = nodeSearch(nodeByName, s);
                       return returnOrThrow(s);
                    };
                     
                    this.Element.LINK = function(s){
                      locators.link = s;
                      domNode = nodeSearch(nodeByLink, s);
                      return returnOrThrow(s);
                    };
                    this.Element.CLASSNAME = function(s){
                      locators.classname = s;
                      domNode = nodeSearch(nodeByClassname, s);
                      return returnOrThrow(s);
                    };
                    this.Element.TAGNAME = function(s){
                      locators.tagname = s;
                      domNode = nodeSearch(nodeByTagname, s);
                      return returnOrThrow(s);
                    };
                    this.Element.VALUE = function(s){
                      locators.value = s;
                      domNode = nodeSearch(nodeByValue, s);
                      return returnOrThrow(s);
                    };
                    this.Element.LABEL = function(s){
                      locators.labelname = s;
                      domNode = nodeSearch(nodeByLabel, s);
                      return returnOrThrow(s);
                    };
                    this.Element.XPATH = function(s){
                      locators.xpath = s;
                      domNode = nodeSearch(nodeByXPath, s, document);
                      //do the lookup, then set the domNode to the result
                      return returnOrThrow(s);
                    };
                    
                    //either returns the element, or throws an exception
                    var returnOrThrow = function(s){
                      if (!domNode){
                        //var e = {};
                        //e.message = "Element "+s+" could not be found";
                        //throw e;
                        return null;
                      }
                      else{
                        return domNode;
                      }
                    };
                    
                    //do the recursive search
                    //takes the function for resolving nodes and the string
                    var nodeSearch = function(func, s, doc){
                      var e = null;
                      //inline function to recursively find the element in the DOM, cross frame.
                      var recurse = function(w, func, s, doc){
                       //do the lookup in the current window
                       try{ element = func.call(w, s, doc);}
                       catch(err){ element = null; }
                       
                        if (!element){
                          var fc = w.frames.length;
                          var fa = w.frames;   
                          for (var i=0;i<fc;i++){
                            recurse(fa[i], func, s, doc); 
                          }
                       }
                       else { e = element; }
                      };
                      
                      //IE cross window problems require you to talk directly to opener
                       try{ element = func.call(window, s, doc);}
                       catch(err){ element = null; }
                       if (!element){
                         for (var i=0;i<window.frames.length;i++){
                           try { element = func.call(window.frames[i], s, doc); }
                           catch(err){ element = null; }
                         }
                       }
                          
                      if (element){ return element; }
                      recurse(window, func, s, doc);
                      
                      return e;
                    };
                    
                    //Lookup by ID
                    var nodeById = function (s){
                      return this.document.getElementById(s);
                    };
                    
                    //DOM element lookup functions, private to elementslib
                    var nodeByName = function (s) { //search nodes by name
                      var getElementsByAttribute = function(oElm, strTagName, strAttributeName, strAttributeValue){
                          var arrElements = (strTagName == "*" && oElm.all)? oElm.all : oElm.getElementsByTagName(strTagName);
                          var arrReturnElements = [];
                          var oAttributeValue = (typeof strAttributeValue != "undefined")? new RegExp("(^|\\s)" + strAttributeValue + "(\\s|$)", "i") : null;
                          var oCurrent;
                          var oAttribute;
                          for(var i=0; i<arrElements.length; i++){
                              oCurrent = arrElements[i];
                              oAttribute = oCurrent.getAttribute && oCurrent.getAttribute(strAttributeName);
                              if(typeof oAttribute == "string" && oAttribute.length > 0){
                                  if(typeof strAttributeValue == "undefined" || (oAttributeValue && oAttributeValue.test(oAttribute))){
                                      arrReturnElements.push(oCurrent);
                                  }
                              }
                          }
                          return arrReturnElements;
                      };
                        
                      if (navigator.userAgent.indexOf('MSIE') != -1){
                        var node = getElementsByAttribute(this.document, "*", "name", s);
                        if (node.length === 0){
                          return null;
                        }
                        return node[0];
                      } else {
                        //sometimes the win object won't have this object
                        try{
                          var els = this.document.getElementsByName(s);
                          if (els.length > 0) {
                            return els[0];
                          }
                        }
                        catch(err){}
                      }
                      return null;
                    };
                    
                    //Lookup by link
                    var nodeByLink = function (s) {//search nodes by link text
                      var getText = function(el){
                        var text = "";
                        if (el.nodeType == 3){ //textNode
                          if (el.data !== undefined){
                            text = el.data;
                          }
                          else{ text = el.innerHTML; }
                          text = text.replace(/\n|\r|\t/g, " ");
                        }
                        if (el.nodeType == 1){ //elementNode
                            for (var i = 0; i < el.childNodes.length; i++) {
                                var child = el.childNodes.item(i);
                                text += getText(child);
                            }
                            if (el.tagName == "P" || el.tagName == "BR" || 
                              el.tagName == "HR" || el.tagName == "DIV") {
                              text += "\n";
                            }
                        }
                        return text;
                      };
                      //sometimes the windows won't have this function
					  var links = [];
                      try {
                        links = this.document.getElementsByTagName('a');
                      }
                      catch(err){}
                      for (var i = 0; i < links.length; i++) {
                        var el = links[i];
                        var linkText = getText(el);
                        if (jQuery.trim(linkText) == jQuery.trim(s)) {
                          return el;
                        }
                      }
                      return null;
                    };
                    
                    //DOM element lookup functions, private to elementslib
                    var nodeByTagname = function (s) { //search nodes by name
                      //sometimes the win object won't have this object
					  var cn, idx = null;
                      if (s.indexOf(',') != -1){
                        cn = s.split(',');
                        idx = cn[1];
                        cn = cn[0];
                      }
                      else{
                        cn = s;
                        idx = 0;
                      }
                      return this.document.getElementsByTagName(cn)[idx];
                    };
                    
                    //DOM element lookup functions, private to elementslib
                    var nodeByClassname = function (s) { //search nodes by name
                      //sometimes the win object won't have this object
					  var cn, idx = null;
                      if (s.indexOf(',') != -1){
                        cn = s.split(',');
                        idx = cn[1];
                        cn = cn[0];
                      }
                      else{
                        cn = s;
                        idx = 0;
                      }
                      if (!this.document.getElementsByClassName){
                        this.document.getElementsByClassName = function(cl) {
                          var retnode = [];
                          var myclass = new RegExp('\\b'+cl+'\\b');
                          var elem = this.getElementsByTagName('*');
						  for (var i = 0; i < elem.length; i++) {
							var classes = elem[i].className;
							if (myclass.test(classes)) {
								retnode.push(elem[i]);
							}
						  }
                          return retnode;
                        };
                      }
                      return this.document.getElementsByClassName(cn)[idx];
                    };
                    
                    //Lookup DOM node by value attribute
                    var nodeByValue = function (s) {
                      var getElementsByAttribute = function(oElm, strTagName, strAttributeName, strAttributeValue){
                          var arrElements = (strTagName == "*" && oElm.all)? oElm.all : oElm.getElementsByTagName(strTagName);
                          var arrReturnElements = [];
                          var oAttributeValue = (typeof strAttributeValue != "undefined")? new RegExp("(^|\\s)" + strAttributeValue + "(\\s|$)", "i") : null;
                          var oCurrent;
                          var oAttribute;
                          for(var i=0; i<arrElements.length; i++){
                              oCurrent = arrElements[i];
                              oAttribute = oCurrent.getAttribute && oCurrent.getAttribute(strAttributeName);
                              if(typeof oAttribute == "string" && oAttribute.length > 0){
                                  if(typeof strAttributeValue == "undefined" || (oAttributeValue && oAttributeValue.test(oAttribute))){
                                      arrReturnElements.push(oCurrent);
                                  }
                              }
                          }
                          return arrReturnElements;
                      };
                      var node = getElementsByAttribute(this.document, "*", "value", s);
                      if (node.length === 0){
                        return null;
                      }
                      return node[0];
                    };
                    
                    var nodeByLabel = function (s) { //search nodes by name
                      //sometimes the win object won't have this object
                      var labels = this.document.getElementsByTagName('label');
                      var node = null;
                      var label = null;

                      //Find the label from all labels on the page
                      for (i = 0;i < labels.length; i++){
                        if (jQuery.trim(labels[i].innerHTML) == jQuery.trim(s)){
                          label = labels[i];
                        }
                      }
                      
                      //If we have a label, use its for attrib to get the id of the input
                      if (label !== null){
                        var iid = null;
						if (navigator.userAgent.indexOf('MSIE') != -1){
                          iid = label.getAttribute('htmlFor');
                        }
                        else {
                          iid = label.getAttribute('for');
                        }
                        node = this.document.getElementById(iid);
                      }
                      //either return the found input node, or null
                      return node;
                    };
 
                    //Lookup with xpath
                    var nodeByXPath = function (xpath, doc) {
                      //if there is built in document.evaluate
                      if (this.document.evaluate){
                        return this.document.evaluate(xpath, this.document, null, 0, null).iterateNext();
                      }
                      //Else pass the IDE window.document that has a document.evaluate
                      else {
                        return doc.evaluate(xpath, this.document, null, 0, null).iterateNext();
                      }
                    };
             };
