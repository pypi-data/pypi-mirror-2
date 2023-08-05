AjStep = function(type,jq,value){
	this._JQ = jq;
	this._TYPE = type;
	this._VALUE = value;
}

AjStep.prototype = {
	getJq: function(){
		return this._JQ;
	},
	getType: function() {
		return this._TYPE;
	},
	getValue: function() {
		return this._VALUE;
	},
	getObj: function() {
		var type_obj = this._TYPE;
		if(this._JQ=='') return jq(AjStandardSteps[this._TYPE]);
		else return jq(this._JQ);
	},
}


/**
 * Utility function that prepare the page for the tour
 * @author Massimo Azzolini
 * @author Giacomo Spettoli
 */
function ajTour() {
	/* 
	 * sets the plone elements that can be "pressed" as "highlight"
	 * next we need to alert the user if he tries to click somewhere else..
	 */
	
	var theAJClass = 'ajHighlight';
	var theAJClassBehaviour = 'ajedElement';
	
	jq('.' + theAJClassBehaviour).click(function(){
		setAmberjackCookies()
	});
	
	// manages the << >> buttons
	var ajNext = jq('#ajNext');
	var ajPrev = jq('#ajPrev');
	
	ajNext.click(function(){
		setAmberjackCookies()
	});
}

/**
 * Function for disabling all links that can break the tour.
 * @author Giacomo Spettoli
 * @author Massimo Azzolini
 */
function disableLinks(){
	if(Amberjack.pageId){
		var notAj = jq("a").not(".ajHighlight,.ajedElement,[id^='aj'],[class^='aj']");
		//NOTE: we assume that there are no other 'ajXXX' ids
		notAj.click(function(){
			alert("You cannot click on other links, please use the console's exit button");
			return false;
		});
		notAj.addClass("aj_link_inactive");
		var actionAjtour = jq("#ajtour").addClass("aj_link_inactive");
		var ajClose = jq("#ajClose");
		var goHome = false;
		
		var sURL = unescape(window.location.pathname);
		if(goHome)
			ajClose.attr("onClick","Amberjack.close();location.href='" + Amberjack.BASE_URL + "';return false");
		else
			ajClose.attr("onClick","Amberjack.close();location.href = window.location.pathname;return false");

		var ajNext = jq("#ajNext");
		ajNext.attr("onClick","if(checkAllStep()){" + ajNext.attr('onClick') + "}");
	}
}

/**
 * Get all current page's step
 * @author Giacomo Spettoli
 * @return steps array of current page step's id
 */
function getPageSteps(){
	var steps = [];
	if(Amberjack.pageId){
		var link = jq(Amberjack.pages[Amberjack.pageId].content).find('a[class^="ajStep"]');
		link.each(function(i){
			var allClasses = jq(this).attr('class').split(' ');
			var firstClass = allClasses[0].split('-');
			steps.push(firstClass[1]);
		});
	}
	return steps;
}


/**
 * Highlight the step for better view
 * @author Giacomo Spettoli
 * 
 * @param num dictionary's label of the step
 */
function highlightStep(num){
	if(Amberjack.pageId){
		
		var theAJClass = 'ajHighlight';
		var theAJClassBehaviour = 'ajedElement';
		var obj;
		try{
			obj = AjSteps[num].getObj();
		}catch(e){
			alert("Error in highlightStep(): Step " + num +" not found");
			return false;
		}
		var type_obj = AjSteps[num].getType();
		
		if(type_obj=="checkbox" || type_obj=="radio"){
			jq("label[for="+obj.attr('id')+"]").addClass(theAJClass);
			obj.addClass(theAJClassBehaviour);
		}
		else if (type_obj=="select"){
			var highlightThis = jq(obj + " option[value="+ AjSteps[num].getValue() +"]");
			highlightThis.addClass(theAJClass);
			obj.addClass(theAJClassBehaviour);
		}
		else if (type_obj=="multiple_select"){
			var tmp = AjSteps[num].getValue().split(",");
			for (var i=0;i<tmp.length;i++){
				jq("option[value="+tmp[i]+"]").addClass(theAJClass);
			}
			obj.addClass(theAJClassBehaviour);
		}
		else if (type_obj.match("menu")){
			obj.addClass(theAJClass);
			obj.children('dt').children('a').addClass(theAJClassBehaviour);
		}
		else{
			obj.addClass(theAJClass);
			obj.addClass(theAJClassBehaviour);
		}
	}
}

/**
 * Highlight all current page's steps
 * @author Giacomo Spettoli
 */
function highlightAllStep(){
	var steps = getPageSteps();
	for(var i =0; i < steps.length;i++){
		highlightStep(steps[i]);
	}
}

function switchClass(obj, remClass, addClass){
	obj.removeClass(remClass);
	obj.addClass(addClass);
}

/**
 * Change the value of a textbox
 * @author Giacomo Spettoli
 *
 * @param obj object to modify
 * @param value new value of the object
 */
function changeValue(obj, value){
	obj.focus();
	obj.val(value);
	obj.blur();
}

function changeSelectValue(obj, value){
	var o = obj[0].options;   
	var oL = o.length;
	for(var i = 0; i<oL; i++){
	  if (o[i].value == value){
	      o[i].selected = true
	  }
	}
	
	jq(obj[0]).trigger('change', true)
}

/**
 * Function for doing steps
 * @author Giacomo Spettoli
 * 
 * @param num dictionary's label of the step
 * 
 * BBB needs to be revised: type_obj is not a complete range of all the cases
 */
function doStep(step){
	var obj, type_obj, jq_obj, value;
	
	var allClasses = jq(step).attr("class").split(" ");
	var firstClass = allClasses[0].split('-');
	var num = firstClass[1];

	try{
		obj = AjSteps[num].getObj();
		type_obj = AjSteps[num].getType();
		jq_obj = AjSteps[num].getJq();
		value = AjSteps[num].getValue();
	}catch(e){
		alert("Error in doStep(): Step " + num +" not found");
		return false;
	}
        
	if (type_obj == 'link') {
		setAmberjackCookies()
		location.href = obj.attr('href');
	}
	else if (type_obj == 'button')
		obj.click();
    else if (type_obj == 'collapsible') {
		if (value == 'collapse') 
			switchClass(obj, 'expandedInlineCollapsible', 'collapsedInlineCollapsible');
		else 
			switchClass(obj, 'collapsedInlineCollapsible', 'expandedInlineCollapsible');
	}
	else if (type_obj == "text") 
		changeValue(obj, value);
	else if (type_obj == "select") {
		setAmberjackCookies()
		changeSelectValue(obj, value);
	}else if(type_obj == "checkbox" || type_obj == "radio"){
        if (obj.is(':checked'))
            obj.attr('checked', false)
        else
            obj.attr('checked', true)
	}
	else if(type_obj == "multiple_select"){
		var tmp = value.split(",");
		for (var i=0;i<tmp.length;i++){
			jq("option[value="+tmp[i]+"]").attr("selected","selected");
		}
	}
    else if(type_obj=="form_text"){
        var kupu_contents = jq('#kupu-editor-iframe-text').contents().find('p')
        kupu_contents.replaceWith("<p>" + value + "</p>")
    }
	else if(type_obj=="form_save_new" || type_obj=="form_save" || type_obj=="form_actions_save" || type_obj=="form_save_default_page"){
		var form = obj.parents("form");
		form.submit(function(){
			setAmberjackCookies();
		});
		// For some reason, using form.submit ignores the kupu content...
		// ... so we simulate the click
		window.onbeforeunload = null;
		jq(obj).click()
	}
	// STANDARD STEPS
	else if(obj.attr('type')=='file') {alert(this.aj_plone_consts['BrowseFile'])} //
	else if(type_obj.match("menu")){
		if(value=='deactivate') switchClass(obj, 'activated', 'deactivated');
		else switchClass(obj,'deactivated','activated');
	}
	else if(value!=""){
		changeValue(obj,value);
	}
	else if(jq_obj==""){
		obj.click(function(){
            setAmberjackCookies()
		});	
		obj.click();
		if(obj.attr("href"))
			location.href = obj.attr("href");
	}	
}

/*
 * BBB: refactor the calls to this function
 */
function setAmberjackCookies(){
	Amberjack.createCookie('ajcookie_tourId', Amberjack.tourId, 1);
    Amberjack.createCookie('ajcookie_skinId', Amberjack.skinId, 1);
	Amberjack.createCookie('ajcookie_pageCurrent', Amberjack.pageCurrent + 1)
}

/**
 * Check that the step has been done.
 * @author Giacomo Spettoli
 *  
 * @param num dictionary's label of the step
 * @return true if done else false
 */
function checkStep(num){
	var obj;
	try{
		obj = AjSteps[num].getObj();
	}catch(e){
		alert("Error in checkStep(): Step " + num +" not found");
		return false;
	}
	
	var type_obj = AjSteps[num].getType();
	var value = AjSteps[num].getValue();
	var stepDone = false;
    if(type_obj == ""){
        stepDone = true
    }
	if(type_obj == "collapsible"){
		if(value=="collapse") {
			stepDone = obj.hasClass("collapsedInlineCollapsible");
		}
		else stepDone = obj.hasClass("expandedInlineCollapsible");
	}
	else if(type_obj == "checkbox" || type_obj == "radio") stepDone = obj.attr("checked");
	else if(type_obj == "select" || type_obj == "text") stepDone = (obj.val()==value?true:false);
	return stepDone;
}

/**
 * Check all current page's steps
 * @author Giacomo Spettoli
 * 
 * @return true if all steps done else false
 */
function checkAllStep(){
    var allDone = true;
    var thisStep = true;

    var steps = getPageSteps();
    for(i =0; i < steps.length;i++){
		thisStep = checkStep(steps[i]);
		if(!thisStep){
			alert("Step " + steps[i] + " not completed");
			allDone = false;
			break;
		}
		allDone = allDone && thisStep;
	}
    return allDone;
}

function initAjPlone(){
	highlightAllStep();
	ajTour();
    // restore previous window position
    AmberjackPlone.restoreWindowPosition()
	disableLinks();
    var last_step = jq('#ajControl').find('#ajLastStep')
    // if it's the last step add this tour to the completed cookie
    if(last_step.length !== 0){
        completed = Amberjack.readCookie('ajcookie_completed')
        if(completed){
            completed = completed + '#another one'
        } else {
            completed = 'first one'
        }
        Amberjack.createCookie('ajcookie_completed', completed, 1);
    }
	jq('#ajControl').draggable({ 
                        handle: '#ajControlNavi', 
                        cursor: 'crosshair',
                        containment: 'body',
                        stop: function(event, ui) {
                            Amberjack.createCookie('ajcookie_controlposition', ui.position.left + "#" + ui.position.top, 10);
                        }
                    })
	jq('#ajControlNavi').css('cursor', 'move')
}



AmberjackPlone = {
    /**
     * some utility constants
     * BBB: we may move all the functions as methods here
     */
    aj_xpath_exists:     'aj_xpath_exists',    // used to just check if a given xpath exists on a page
    aj_any_url:          'aj_any_url',         // we accept any url in the title
	aj_plone_consts:     {},                   // all the plone constants we need to check
    aj_canMove_validators: ['validationError'],// set of use case in which aj cannot go further to the next step
    
	/**
	 *  checks if saving an object we get a validation error
	 */
	validationError: function(){
		return !(
		  (jq('#region-content dl.portalMessage.error dt').text() == this.aj_plone_consts['Error']) &
		  (jq('#region-content dl.portalMessage.error dd').text() == this.aj_plone_consts['ErrorValidation'])
		  )
	},
	
	canMoveToNextStep: function(){
        canMove = true
	    for (i = 0; i < this.aj_canMove_validators.length; i++){
			canMove = (canMove & this[this.aj_canMove_validators[i]]())
	    }
		return canMove
	}, 
    
    restoreWindowPosition: function(){
        coords = Amberjack.readCookie('ajcookie_controlposition')
        if (coords){
            point = coords.split('#')
            jq('#ajControl').css('left', point[0]+'px').css('top',point[1]+ 'px');
        } else {
            var winW = jq(window).width();
            var startPosition = winW/2-jq('#ajControl').width()/2; 
            jq('#ajControl').css('left', startPosition + 'px').css('top','30px');
        }
    }
}


/**
 * Start the tour and set some timeout
 * @author Giacomo Spettoli
 */
registerPloneFunction(function () {
	loadDefaults();
	Amberjack.open();
	setTimeout("initAjPlone()", 300);
})
