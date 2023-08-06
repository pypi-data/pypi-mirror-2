/**
 * An "adapter-like" structure for making choises inside the highlightStep and doStep methods
 * 
 * the idea:
 * 
 * type_obj: {
 *		highlight: function() {...},
 *		step: function() {...}
 * },
 * ...
 * 
 */

AmberjackPlone.stepAdapters = {
		
		
	/* collective.amberjack.windmill integration   @author: Andrea Benetti##################################################*/	
		w_click: {
			highlight: function(obj) {
				jq(obj).addClass(AmberjackPlone.theAJClass+' '+AmberjackPlone.theAJClassBehaviour);
				},
			step: function(obj,locator,options,locatorValue) {
			
					if(locator=='link'){
						AmberjackPlone.setAmberjackCookies();
						controller.click(obj);
					}
					else{
						if(jq(obj).attr('class')=='context'){
							jq(obj).click();	
							return;
						}
					controller.click(obj);
					}
				},
				
			checkStep: null
		},
		
		w_highlight:{
				
				highlight: function(locators){
					for(var i=0; i<locators.length;i++){
						jq(locators[i]).addClass(AmberjackPlone.theAJClass);
					}
			
				},
				
				
				step:null,
				checkStep: null
			
			
		},

		w_type: {
			highlight: null,
			step: function(obj,locator,options,locatorValue) {
				var testo=options.text;
				controller.type(obj,testo);
				},
			checkStep: function (obj, options,locatorValue) {
				var testo=options.text;
	            if (testo !== "") {
					return jq(obj).val() == testo;
				}
				else {
					return true;
				}
	        }
		},
		
		w_select: {
			highlight: null,
			checkStep: null,
			step: function(obj,locator,options,locatorValue) {
				AmberjackPlone.setAmberjackCookies();
				for(var i; i<options.length; i++){
					var opt=i;
					var value=options[i];
					controller.select(obj,opt, value);
					break;
				}
			}
		},
		
		w_check: {
			highlight: function(obj) {
				jq(obj).parent().addClass(AmberjackPlone.theAJClass);
				jq(obj).addClass(AmberjackPlone.theAJClassBehaviour);
				},
			step: function(obj,locator,options,locatorValue) {
				controller.check(obj);
				},
			checkStep: null
		},
		
		w_radio: {
			highlight: null, // AmberjackPlone.stepAdapters.checkbox.highlight,
			checkStep: null, // AmberjackPlone.stepAdapters.checkbox.checkStep,
			step:function(obj,locator,options,locatorValue) {
				controller.radio(obj);
				}
		},
		
		w_editor:{
			  highlight:function(obj){
				jq('#'+obj.id+'_ifr').addClass(AmberjackPlone.theAJClass);
				},
			  step:function(obj,locator,options,locatorValue) {
				  var tx=options.editor;
				  tx=tx.replace(/&lt\;/g,'<');
				  tx=tx.replace(/&gt\;/g,'>');
				  controller.editor(tx,locatorValue);
				},
			  checkStep:null
			/*checkStep: function (obj,options,locatorValue) {
				  var tx=options['editor']
				  return (tinyMCE.get(locatorValue).getContent({format : 'text'}).replace(/<[^>]+>/gi, "")==tx || tinyMCE.get(locatorValue).getContent()==tx)
		        }*/
		},
		
		w_editorSelect:{
			highlight:null,
			step:function(obj,locator,options,locatorValue) {
				var bookmark=options.bookmark;
				controller.editorSelect(locatorValue, bookmark);
				},
			checkStep:null
			/*checkStep: function (obj,options,locatorValue) {
				 var selected=options['text'];
				 return tinyMCE.get(locatorValue).selection.getContent({format : 'text'})==selected
	        }*/
			
		}
	
};