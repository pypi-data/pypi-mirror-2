/**
 * A jQuery plugin for Plone that add tabbing feature for portlets.
 * Take some standard Plone portlets all around the page the merge them togheter obtaining
 * a new portlet that show them all.
 * 
 * Old portlets are someway analyzed and some DOM elements are stealed from them. Then the old portlet
 * is removed from the page itself.
 * 
 * Whatever portlet you grab from the page, this plugin generate a new portlet like this:
 * 
 * <portletNodeType class="portletNodeClasses-1 [portletNodeClasses-2 ...] portletNodeAdditionalClasses1 [portletNodeAdditionalClasses2 ...]">
 *     <portletHeaderNodeType class="portletHeaderNodeClasses-1 [portletHeaderNodeClasses-2 ...]">
 *         <ul class="portletTabs">
 *            <li class="portletTab">
 *                <a href="javascript:;">{Header text}</a>
 *            </li>
 *            [...]
 *         </ul>
 *     </portletHeaderNodeType>
 *     <portletDataNodeType class="portletDataNodeClasses1 [portletDataNodeClasses2 ...]">
 *         {same content as in the old portlet}
 *     </portletDataNodeType>
 *     [...]
 * </portletNodeType>
 * 
 */

/**
 * Generate a portlet structure that can contains the tabbing infrastructure.
 * The portlet structure is based on the Plone CMS ones, but the plugin try to be generic
 * as possible.
 * You can customize your preference with the options parameter with:
 * * portletNodeType (String) - HTML element that store a portlet. Default 'dl'
 * * portletNodeClasses (Array) - list of CSS classes that must be added to the generated portlet but also
 * found in the portlet that became a new tab. Default 'portlet'
 * * portletNodeAdditionalClasses (Array) - additional list of classes that will be added to the generated
 * portlet (use this if you want to add to tabbed portlet some new classes). Default 'portletTabGenerated'
 * * portletHeaderNodeType (String) - the element used to generate the portlet header (and also must be the
 * header of all portlet that became new tab. Default 'dt'
 * portletHeaderNodeClasses (Array) - list of CSS classes that must be added to the generated header but
 * also found in the header of the portlet that became a new tab. Default 'portletHeader'
 * portletDataNodeType (String) - the element used to generate the portlet element (and also must be the
 * element type inside all portlet that became new tab. Default 'dd'
 * portletDataNodeClasses (Array) - array of classes for portletDataNodeType elements that are valid to be
 * used as elements inside the new portlet. Elements that aren't using at least one of those CSS classes
 * will not be moved to the tab and simply disappear from the page after makeTab() call.
 * * id (String) - an optional HTML id to be added to the portlet. Default null.
 * 
 * @param {Object} options preferences when using structure different from default
 * @return {Object} object with features that make possible to store tab inside
 */
jQuery.tabbedportlet = function(options) {
	var ops = jQuery.extend({}, jQuery.tabbedportlet.defaults, options);
	
	var portlet = jQuery('<'+ops.portletNodeType+'/>')
			.addClass(ops.portletNodeClasses.join(" "))
			.addClass(ops.portletNodeAdditionalClasses.join(" "))
			.append('<'+ops.portletHeaderNodeType+'/>').children()
			.addClass(ops.portletHeaderNodeClasses.join(" "))
			.append('<ul class="portletTabs"></ul>')
			.end();
	if (ops.id) portlet.attr('id', ops.id);

	var that = this;
	
	/**
	 * Add a new tab to this portlet.
	 * 
	 * @param {Object} jqe a DOM element or a jQuery selector that will be used as a tab 
	 * @param {Object} options an object that contains preferences.
	 * You can also use following values:
	 * * cutChars (Integer) - don't display the whole header, but cut it limiting some characters (default: 0, so use the whole label)
	 * * label (String) - force a specific label
	 * * id (String) - use a portlet id (default: not used)
	 * * select (Boolean) - select this portlet (default: the first portlet is selected)
	 */
	that.makeTab = function(jqe, options) {
		var tabOps = jQuery.extend({}, that.makeTab.defaults, options);
		
		// Be sure that jqe is a valid element for creating a new tab
		jqe = jQuery(jqe).get(0);
		if (!jqe)
			return;
		jqe = jQuery(jqe);
		if (!jqe.length)
			return;

		var filters = [];
		for (var i=0;i<ops.portletDataNodeClasses.length;i++)
			filters.push(ops.portletDataNodeType+'.'+ops.portletDataNodeClasses[i]);
		var elements = jQuery(filters.join(','), jqe).remove();
		
		var header_text = jQuery.trim(jQuery(ops.portletHeaderNodeType+'.'+ops.portletHeaderNodeClasses.join('.'), jqe).remove().children().text());
		if (tabOps.cutChars && header_text.length>tabOps.cutChars-1)
			header_text=header_text.substr(0,tabOps.cutChars)+"&hellip;";
		else if (tabOps.label)
			header_text = tabOps.label;
		var header_element = jQuery('<li class="portletTab"></li>').append('<a href="javascript:;">'+header_text+'</a>');
		jQuery(".portletTabs", portlet).append(header_element);
		var header_elements = jQuery('.portletTab', portlet);
		header_elements.removeClass('firstPortletTab').filter(':first').addClass('firstPortletTab');
		header_elements.removeClass('lastPortletTab').filter(":last").addClass('lastPortletTab');
		// Now elements
		header_element.data('tabbedElements', elements).click(function(e) {
			var thisJq = jQuery(this);
			showElements(thisJq.data('tabbedElements'));
			jQuery('a.selected', portlet).removeClass('selected');
			jQuery('a', thisJq).addClass('selected');
			e.preventDefault();
		});
		jqe.remove();
		// If this is the first portlet or we get the select parameter, select it
		if (tabOps.select || header_elements.filter(':first').get(0)==header_element.get(0))
			header_element.click();
	}

	/**
	 * If you commonly use non-default defaults for makeTab, you can change them here.
	 */
	that.makeTab.defaults = {
		cutChars: 0,
		label: null,
		select: false
	};

	/**
	 * Display a tab
	 * @param {jQuery} jqe the jQuery object containing a tab
	 */
	var showElements = function(jqe) {
		portlet.children(':not(.'+ops.portletHeaderNodeClasses.join('.')+')').remove();
		portlet.append(jqe);
	}

	/**
	 * Get the jQuery object of the whole portlet
	 * @return {jQuery} the portlet DOM element wrapped unside jQuery object
	 */
	that.getPortlet = function() {
		return portlet;
	}

	return that
}

/**
 * Change those defaults if you commonly use non-standard portet structure
 */
jQuery.tabbedportlet.defaults = {
	portletNodeType: 'dl',
	portletNodeClasses: ['portlet'],
	portletNodeAdditionalClasses: ['portletTabGenerated'],
	portletHeaderNodeType: 'dt',
	portletHeaderNodeClasses: ['portletHeader'],
	portletDataNodeType: 'dd',
	portletDataNodeClasses: ['portletItem', 'portletFooter'],
	id: null	
};




jq(document).ready(function() {
	// var exPortlets = jq("#portal-column-two .portletWrapper").remove();
	
	var generatedPortlet = jq.tabbedportlet({
		id: 'tabbing'
	});
	generatedPortlet.makeTab("#portal-column-two .portletNews", {cutChars: 5});
	generatedPortlet.makeTab("#portal-column-two .portlet-static-in-primo-piano", {label: 'Primo', select: true});
	generatedPortlet.makeTab("#portal-column-two .portlet-static-in-xxx", {label: 'Xxx'});
	jq("#portal-column-two .visualPadding").prepend(generatedPortlet.getPortlet());	
	
});
