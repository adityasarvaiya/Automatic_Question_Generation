/**
 * @copyright
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *  
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *  
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *  
 * @author Stephane Roucheray
 * @see Plugin Page   : http://code.google.com/p/jquery-dynamic-form/
 * @see Author's Blog : http://sroucheray.org
 * @see Follow author : http://twitter.com/sroucheray
 * @extends jQuery (requires at version >= 1.4)
 * @version 1.0.3
 */
(function($){
/**
 * @param {String} plusSelector HTML element serving the duplication when clicking on it
 * @param {String} minusSelector HTML element deleting the cloned form element
 * @param {Object} options Optional object, can contain any of the parameters below : 
 *     limit      {Number}   : maximum number of duplicate fields authorized
 *     formPrefix {String}   : the prefix used to identify a form (if not defined will use normalized source selector)
 *     afterClone {Function} : a callback function called as soon as a duplication is done,
 *       this is useful for custom insertion (you can insert the duplicate anywhere in the DOM), 
 *       inserting specific validation on cloned field
 *       - this function will be passed the cloned element as a unique parameter
 *       - return false if the cloned element should not be inserted
 *     normalizeFullForm {Boolean} : normalize all fields in the form (even outside the template) for better server side script handling (default true)
 *     
 *     createColor {String} : color effect when duplicating (requires jQuery UI Effects module)
 *     removeColor {String} : color effect when removing duplicate (idem)
 *     duration    {Number} : color effect duration (idem)
 *     
 *     data        {Object} : A JSON based representation of the data which will prefill the form (equivalent of the inject method)
 *     
 */
$.fn.dynamicForm = function (plusSelector, minusSelector, options){
	var source = $(this),
	minus,
	plus,
	template,
	formFields = "input, checkbox, select, textarea",
	clones = [],
	defaults = {
		duration:1000,
		normalizeFullForm:true,
		isSubDynamicForm:false
	},
	subDynamicForm = [],
	formPrefix;
	
	// Set plus and minus elements within sub dynamic form clones
	if(options.internalSubDynamicForm){
		minus = $(options.internalContainer).find(minusSelector);
		plus = $(options.internalContainer).find(plusSelector);
	}else{	//Set normal plus an minus element
		minus = $(minusSelector);
		plus = $(plusSelector);
	}
	
	// Extend default options with those provided
	options = $.extend(defaults, options);
	//Set the form prefix
	formPrefix = options.formPrefix || source.selector.replace(/\W/g, "");
	
	
	/**
	 * Clone the form template
	 */
	function cloneTemplate(disableEffect){
		var clone, callBackReturn;
		clone = template.cloneWithAttribut(true);
		
		if (typeof options.afterClone === "function") {
			callBackReturn = options.afterClone(clone);
		}
		
		if(callBackReturn || typeof callBackReturn == "undefined"){
			clone.insertAfter(clones[clones.length - 1] || source);
		}
		
		clone.getSource = function(){
			return source;
		};

		/* Normalize template id attribute */
		if (clone.attr("id")) {
			clone.attr("id", clone.attr("id") + clones.length);
		}

		if (clone.effect && options.createColor && !disableEffect) {
			clone.effect("highlight", {color:options.createColor}, options.duration);
		}
		
		return clone;
	}
	
	/**
	 * On cloning make the form under the clone dynamic
	 * @param {Object} clone
	 */
	function dynamiseSubClones(clone){
		$(subDynamicForm).each(function(){
			var plus = this.getPlusSelector(), minus = this.getMinusSelector(), options = this.getOptions(), selector = this.selector;
			clone.find(this.selector).each(function(){
				options = $.extend(
					{
						internalSubDynamicForm:true, 
						internalContainer:clone, 
						isInAClone:true, 
						outerCloneIndex:clones.length,
						selector:selector
					}, options);
				$(this).dynamicForm(plus, minus, options);
			});
		});
	}
	
	/**
	 * Handle click on plus when plus element is inside the template
	 * @param {Object} event
	 */
	function innerClickOnPlus(event, extraParams){
		var clone,
		currentClone = clones[clones.length -1] || source;
		event.preventDefault();

		currentClone.find(minusSelector).show();
		currentClone.find(plusSelector).hide();

		if (clones.length === 0) {
			source.find(minusSelector).hide();
		}
		
		clone = cloneTemplate(extraParams);
		
		plus = clone.find(plusSelector);
		minus = clone.find(minusSelector);
		
		minus.get(0).removableClone = clone;
		minus.click(innerClickOnMinus);
		
		if (options.limit && (options.limit - 2) > clones.length) {
			plus.show();
			minus.show();
		}else{
			plus.hide();
			minus.show();
		}
		
		clones.push(clone);
		normalizeClone(clone, clones.length);
		
		dynamiseSubClones(clone);
	}
	
	/**
	 * Handle click on plus when plus element is outside the template
	 * @param {Object} event
	 */
	function outerClickOnPlus(event, extraParams){
		var clone;
		
		event.preventDefault();
		
		/* On first add, normalize source */
		if (clones.length === 0) {
			minus.show();
		}
		clone = cloneTemplate(extraParams);
		
		if (options.limit && (options.limit - 3) < clones.length) {
			plus.hide();
		}
		
		clones.push(clone);
		
		normalizeClone(clone, clones.length);
		
		dynamiseSubClones(clone);
	}
	/**
	 * Handle click on minus when minus element is inside the template
	 * @param {Object} event
	 */
	function innerClickOnMinus(event){
		event.preventDefault();
		
		if (this.removableClone.effect && options.removeColor) {
			that = this;
			this.removableClone.effect("highlight", {
				color: options.removeColor
			}, options.duration, function(){that.removableClone.remove();});
		} else {
		
			this.removableClone.remove();
		}
		clones.splice($.inArray(this.removableClone, clones),1);
		if (clones.length === 0){
			source.find(plusSelector).show();
		}else{
			clones[clones.length -1].find(plusSelector).show();
		}
	}
	
	/**
	 * Handle click on minus when minus element is outside the template
	 * @param {Object} event
	 */
	function outerClickOnMinus(event){
		event.preventDefault();
		var clone = clones.pop();
		if (clones.length >= 0) {
			if (clone.effect && options.removeColor) {
				that = this;
				clone.effect("highlight", {
					color: options.removeColor, mode:"hide"
				}, options.duration, function(){clone.remove();});
			} else {
				clone.remove();
			}
		}
		if (clones.length === 0) {
			minus.hide();
		}
		plus.show();
	}
	
	/**
	 * Normalize ids and name attributes of all children forms fields of an element
	 * @param {Object} elmnt
	 */
	function normalizeSource(elmnt, prefix, index){
		elmnt.find(formFields).each(function(){
			var that = $(this), 
			nameAttr = that.attr("name"), 
			origNameAttr = that.attr("origname"),
			idAttr = that.attr("id"),
			origId = that.attr("origid");

			/* Normalize field name attributes */
			if (!nameAttr) {
				//TODO: that.attr("name", formPrefix+"form"+index + "["+index+"]");
			}
			
			if(origNameAttr){
				//This is a subform (thus prefix is not the same as below)
				that.attr("name", prefix+"["+index+"]"+"["+origNameAttr+"]");
			}else{
				//This is the main form
				that.attr("origname", nameAttr);
				
				//This is the main normalization
				that.attr("name", prefix+"["+index+"]"+"["+nameAttr+"]");
			}
			
			/* Normalize field id attributes */
			if (idAttr) {
				/* Normalize attached label */
				that.attr("origid", idAttr);
				$("label[for='"+idAttr+"']").each(function(){
					$(this).attr("origfor", idAttr);
					$(this).attr("for", idAttr + index);
				});
				that.attr("id", idAttr + index);
			}
		});
	}
	
	function normalizeClone(elmnt, index){
		var match, matchRegEx = /(.+\[[^\[\]]+\]\[)(\d+)(\]\[[^\[\]]+\])$/;
		elmnt.find(formFields).each(function(){
			var that = $(this),
			nameAttr = that.attr("name"), 
			origNameAttr = that.attr("origname"),
			idAttr = that.attr("id"),
			newIdAttr = idAttr.slice(0,-1) + index,
			match = matchRegEx.exec(nameAttr);
			that.attr("name", match[1]+index+match[3]);
			
			if (idAttr) {
				that.attr("origid", idAttr);
				
				elmnt.find("label[for='"+idAttr+"']").each(function(){
					$(this).attr("for", newIdAttr);
				});
				that.attr("id", newIdAttr);
			}
		});
	}
	
	function normalizeSubClone(elmnt, formPrefix, index){
		var match, matchRegEx = /(.+)\[([^\[\]]+)\]$/;
		elmnt.find(formFields).each(function(){
			var that = $(this),
			nameAttr = that.attr("name"), 
			idAttr = that.attr("id"),
			newIdAttr = idAttr + index,
			match = matchRegEx.exec(nameAttr);
			that.attr("name", match[1]+"["+formPrefix+"]"+"["+index+"]"+"["+match[2]+"]");
			
			if (idAttr) {
				that.attr("origid", idAttr);
				
				elmnt.find("label[for='"+idAttr+"']").each(function(){
					$(this).attr("for", newIdAttr);
				});
				that.attr("id", newIdAttr);
			}
		});
	}
	
	//Add a function to enable sub dynamic forms to register themselves
	source.each(function(){
		$.extend(this, {
			addSubDynamicForm : function(dynamicForm){
				subDynamicForm.push(dynamicForm);
			},
			getFormPrefix : function(){
				return formPrefix;
			},
			getSource : function(){
				return source;
			}
		});
	});
	
	//Check if this dynamic form is a sub dynamic form
	var isMainForm = true;
	$(this).parentsUntil("body").each(function(){
		if($.isFunction(this.addSubDynamicForm) && !options.isSubDynamicForm){
			isMainForm = false;
			options.isSubDynamicForm = true;
			
			var suboptions = $.extend(
				{
					internalSubDynamicForm:true, 
					internalContainer:this
				}, options);
			this.addSubDynamicForm(source);
			formPrefix = this.getFormPrefix()+"[0]["+formPrefix+"]";
			return false;
		}
	});
	if(isMainForm && !options.isInAClone){
		//Main form name and prefix for the main form are the same for now
		formPrefix = formPrefix+"["+formPrefix+"]";
	}
	
	if(!options.isInAClone){
		normalizeSource(source, formPrefix, 0);
	}else{
		formPrefix = formPrefix || options.selector.replace(/\W/g, "");
		//Main form name and prefix for the main form are the same for now
		normalizeSubClone(source, formPrefix, 0);
	}
	if(isMainForm && options.normalizeFullForm && !options.isInAClone){
		//Normalize all forms outside duplicated template in order to ease server-side parsing
		$(this).parentsUntil("form").each(function(){
			var theForm = $(this).parent().get(0);
			$(theForm).find(formFields).filter("[type!=submit]").each(function(){
				var that = $(this), 
				nameAttr = that.attr("name"), 
				origNameAttr = that.attr("origname"),
				idAttr = that.attr("id"),
				origId = that.attr("origid");
				
				if(!origNameAttr){
					// Normalize field name attributes
					if (!nameAttr) {
						//TODO: that.attr("name", formPrefix+"form"+index + "["+index+"]");
					}

					//It's the main form
					that.attr("origname", nameAttr);
					
					//This is the main normalization
					that.attr("name", formPrefix+"["+nameAttr+"]");
				}
			});
			
		});
	}
	
	isPlusDescendentOfTemplate = source.find("*").filter(function(){
		return this == plus.get(0);
	});
	
	isPlusDescendentOfTemplate = isPlusDescendentOfTemplate.length > 0 ? true : false;
	
	/* Hide minus element */
	minus.hide();
	
	/* If plus element is within the template */
	if (isPlusDescendentOfTemplate) {
		/* Handle click on plus */
		plus.click(innerClickOnPlus);
		
	}else{
	/* If plus element is out of the template */
		/* Handle click on plus */
		plus.click(outerClickOnPlus);
		
		/* Handle click on minus */
		minus.click(outerClickOnMinus);
	}
	
	$.extend( source, {
		getPlus : function(){
			return plus;
		},
		getPlusSelector : function(){
			return plusSelector;
		},
		getMinus : function(){
			return minus;
		},
		getMinusSelector : function(){
			return minusSelector;
		},
		getOptions : function(){
			return options;
		},
		getClones : function(){
			var clonesAndSource = [source];
			return clonesAndSource.concat(clones);
		},
		getSource : function(){
			return source;
		},
		inject : function(data){
			/**
			 * Fill data of each main dynamic form clones
			 * @param {Object} formIndex
			 * @param {Object} formValue
			 */
			function fillData(formIndex, formValue){
				//Loop over data form array (each item will match a specific clone)
				var mainForm = this;
				//Shows required additional dynamic forms
				if(formIndex > 0){
					mainForm.getSource().getPlus().trigger("click", ["disableEffect"]);
				}
				var clone = mainForm.get(0).getSource().getClones()[formIndex];
				
				$.each(formValue, function(index, value){
					if($.isArray(value)){
						mainForm = clone.find("#"+index);
						if(typeof mainForm.get(0).getSource === "function"){
							$.each(value, $.proxy( fillData, mainForm.get(0).getSource()));
						}

					}else{
						var formElements = mainForm.getSource().getClones()[formIndex].find("[origname='"+index+"']");
						if(formElements){
							if(formElements.get(0).tagName.toLowerCase() == "input"){
								/* Fill in radio input */
								if(formElements.attr("type") == "radio"){
									formElements.filter("[value='"+value+"']").attr("checked", "checked");
								}else if(formElements.attr("type") == "checkbox"){/* Fill in checkbox input */
									formElements.attr("checked", "checked");
								}else{
									formElements.attr("value", value);
								}
							}else if(formElements.get(0).tagName.toLowerCase() == "textarea"){
								/* Fill in textarea */
								formElements.text(value);
							}else if(formElements.get(0).tagName.toLowerCase() == "select"){
								/* Fill in select */
								$(formElements.get(0)).find("option").each(function(){
									if($(this).text() == value || $(this).attr("value") == value){
										$(this).attr("selected", "selected");
									}
								});
							}
						}
					}
				});
			}
			//Loop over each form
			$.each(data, $.proxy( fillData, source ));
		}
	});
	
	template = source.cloneWithAttribut(true);
	
	if(options.data){
		source.inject(options.data);
	}
	
	return source;
};

/**
 * jQuery original clone method decorated in order to fix an IE < 8 issue
 * where attributs especially name are not copied 
 */
jQuery.fn.cloneWithAttribut = function( withDataAndEvents ){
	if ( jQuery.support.noCloneEvent ){
		return $(this).clone(withDataAndEvents);
	}else{
		$(this).find("*").each(function(){
			$(this).data("name", $(this).attr("name"));
		});
		var clone = $(this).clone(withDataAndEvents);
		
		clone.find("*").each(function(){
			$(this).attr("name", $(this).data("name"));
		});
		
		return clone;
	}
};

})(jQuery);
