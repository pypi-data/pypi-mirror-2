

SAMLmetaJS.Constants = {
	'ns' : {
		'md': "urn:oasis:names:tc:SAML:2.0:metadata",
		'mdui': "urn:oasis:names:tc:SAML:metadata:ui",
		'mdattr': "urn:oasis:names:tc:SAML:metadata:attribute",
		'saml': "urn:oasis:names:tc:SAML:2.0:assertion",
		'xsd': "http://www.w3.org/2001/XMLSchema",
		'ds': "http://www.w3.org/2000/09/xmldsig#"
	},
	'certusage': {
		'both': 'Both',
		'signing': 'Signing',
		'encryption': 'Encryption'
	},
	'languages': {
		'en': 'English',
		'no': 'Norwegian (bokmål)',
		'nn': 'Norwegian (nynorsk)',
		'se': 'Sámegiella',
		'da': 'Danish',
		'de': 'German',
		'sv': 'Swedish',
		'fi': 'Finnish',
		'es': 'Español',
		'fr': 'Français',
		'it': 'Italian',
		'nl': 'Nederlands',
		'lb': 'Luxembourgish', 
		'cs': 'Czech',
		'sl': 'Slovenščina',
		'lt': 'Lietuvių kalba',
		'hr': 'Hrvatski',
		'hu': 'Magyar',
		'pl': 'Język polski',
		'pt': 'Português',
		'pt-BR': 'Português brasileiro',
		'tr': 'Türkçe',
		'el': 'ελληνικά',
		'ja': 'Japanese (日本語)'
	},
	'contactTypes' : {
		'admin' : 'Administrative',
		'technical': 'Technical',
		'support': 'Support'
	},
	'endpointTypes' : {
		'sp': {
			'AssertionConsumerService': 'AssertionConsumerService',
			'SingleLogoutService': 'SingleLogoutService'
		},
		'idp' : {}
	},
	'bindings': {
		'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect': 'HTTP Redirect',
		'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST': 'HTTP POST',
		'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Artifact': 'HTTP Artifact',
		'urn:oasis:names:tc:SAML:2.0:bindings:SOAP': 'SOAP',
		'urn:oasis:names:tc:SAML:2.0:bindings:PAOS': 'Reverse SOAP (PAOS)'
	},
	'attributes' : {
		'urn:oid:0.9.2342.19200300.100.1.1': 'uid',
		'urn:oid:0.9.2342.19200300.100.1.10': 'manager',
		'urn:oid:0.9.2342.19200300.100.1.2': 'textEncodedORAddress',
		'urn:oid:0.9.2342.19200300.100.1.20': 'homePhone',
		'urn:oid:0.9.2342.19200300.100.1.22': 'otherMailbox',
		'urn:oid:0.9.2342.19200300.100.1.3': 'mail',
		'urn:oid:0.9.2342.19200300.100.1.39': 'homePostalAddress',
		'urn:oid:0.9.2342.19200300.100.1.40': 'personalTitle',
		'urn:oid:0.9.2342.19200300.100.1.41': 'mobile',
		'urn:oid:0.9.2342.19200300.100.1.42': 'pager',
		'urn:oid:0.9.2342.19200300.100.1.43': 'co',
		'urn:oid:0.9.2342.19200300.100.1.6': 'roomNumber',
		'urn:oid:0.9.2342.19200300.100.1.60': 'jpegPhoto',
		'urn:oid:0.9.2342.19200300.100.1.7': 'photo',
		'urn:oid:1.2.840.113549.1.9.1': 'email',
		'urn:oid:1.3.6.1.4.1.2428.90.1.1': 'norEduOrgUniqueNumber',
		'urn:oid:1.3.6.1.4.1.2428.90.1.11': 'norEduOrgSchemaVersion',
		'urn:oid:1.3.6.1.4.1.2428.90.1.12': 'norEduOrgNIN',
		'urn:oid:1.3.6.1.4.1.2428.90.1.2': 'norEduOrgUnitUniqueNumber',
		'urn:oid:1.3.6.1.4.1.2428.90.1.3': 'norEduPersonBirthDate',
		'urn:oid:1.3.6.1.4.1.2428.90.1.4': 'norEduPersonLIN',
		'urn:oid:1.3.6.1.4.1.2428.90.1.5': 'norEduPersonNIN',
		'urn:oid:1.3.6.1.4.1.2428.90.1.6': 'norEduOrgAcronym',
		'urn:oid:1.3.6.1.4.1.2428.90.1.7': 'norEduOrgUniqueIdentifier',
		'urn:oid:1.3.6.1.4.1.2428.90.1.8': 'norEduOrgUnitUniqueIdentifier',
		'urn:oid:1.3.6.1.4.1.2428.90.1.9': 'federationFeideSchemaVersion',
		'urn:oid:1.3.6.1.4.1.250.1.57': 'labeledURI',
		'urn:oid:1.3.6.1.4.1.5923.1.1.1.1': 'eduPersonAffiliation',
		'urn:oid:1.3.6.1.4.1.5923.1.1.1.10': 'eduPersonTargetedID',
		'urn:oid:1.3.6.1.4.1.5923.1.1.1.2': 'eduPersonNickname',
		'urn:oid:1.3.6.1.4.1.5923.1.1.1.3': 'eduPersonOrgDN',
		'urn:oid:1.3.6.1.4.1.5923.1.1.1.4': 'eduPersonOrgUnitDN',
		'urn:oid:1.3.6.1.4.1.5923.1.1.1.5': 'eduPersonPrimaryAffiliation',
		'urn:oid:1.3.6.1.4.1.5923.1.1.1.6': 'eduPersonPrincipalName',
		'urn:oid:1.3.6.1.4.1.5923.1.1.1.7': 'eduPersonEntitlement',
		'urn:oid:1.3.6.1.4.1.5923.1.1.1.8': 'eduPersonPrimaryOrgUnitDN',
		'urn:oid:1.3.6.1.4.1.5923.1.1.1.9': 'eduPersonScopedAffiliation',
		'urn:oid:1.3.6.1.4.1.5923.1.2.1.2': 'eduOrgHomePageURI',
		'urn:oid:1.3.6.1.4.1.5923.1.2.1.3': 'eduOrgIdentityAuthNPolicyURI',
		'urn:oid:1.3.6.1.4.1.5923.1.2.1.4': 'eduOrgLegalName',
		'urn:oid:1.3.6.1.4.1.5923.1.2.1.5': 'eduOrgSuperiorURI',
		'urn:oid:1.3.6.1.4.1.5923.1.2.1.6': 'eduOrgWhitePagesURI',
		'urn:oid:1.3.6.1.4.1.5923.1.5.1.1': 'isMemberOf',
		'urn:oid:2.16.840.1.113730.3.1.241': 'displayName',
		'urn:oid:2.16.840.1.113730.3.1.3': 'employeeNumber',
		'urn:oid:2.16.840.1.113730.3.1.39': 'preferredLanguage',
		'urn:oid:2.16.840.1.113730.3.1.4': 'employeeType',
		'urn:oid:2.16.840.1.113730.3.1.40': 'userSMIMECertificate',
		'urn:oid:2.5.4.10': 'o',
		'urn:oid:2.5.4.11': 'ou',
		'urn:oid:2.5.4.12': 'title',
		'urn:oid:2.5.4.13': 'description',
		'urn:oid:2.5.4.16': 'postalAddress',
		'urn:oid:2.5.4.17': 'postalCode',
		'urn:oid:2.5.4.18': 'postOfficeBox',
		'urn:oid:2.5.4.19': 'physicalDeliveryOfficeName',
		'urn:oid:2.5.4.20': 'telephoneNumber',
		'urn:oid:2.5.4.21': 'telexNumber',
		'urn:oid:2.5.4.3': 'cn',
		'urn:oid:2.5.4.36': 'userCertificate',
		'urn:oid:2.5.4.4': 'sn',
		'urn:oid:2.5.4.41': 'name',
		'urn:oid:2.5.4.42': 'givenName',
		'urn:oid:2.5.4.7': 'l',
		'urn:oid:2.5.4.9': 'street'
	}
};






// This object allows you to update UI elements on the page, using various 
// simple functions to add and clear UI elements.
SAMLmetaJS.UI = {

	"maps": function(tabnode) {
		var geocoder = new google.maps.Geocoder();

		function geocodePosition(pos) {
			geocoder.geocode({
				latLng: pos
			}, function(responses) {
				if (responses && responses.length > 0) {
					updateMarkerAddress(responses[0].formatted_address);
				} else {
					updateMarkerAddress('Cannot determine address at this location.');
				}
			});
		}

		function updateMarkerStatus(str) {
//			$("#locationDescr").html(str);
//			document.getElementById('markerStatus').innerHTML = str;
		}

		function updateMarkerPosition(latLng) {
			$("input#geolocation").val(latLng.lat() + ',' + latLng.lng());
			// document.getElementById('info').innerHTML = [
			// latLng.lat(),
			// latLng.lng()
			// ].join(', ');
		}

		function updateMarkerAddress(str) {
			$("#locationDescr").html(str);
//			document.getElementById('address').innerHTML = str;
		}



		var latLng = new google.maps.LatLng(53.852527,14.238281);
		var myOptions = {
			zoom: 4,
			center: latLng,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		};

		// SAMLmetaJS.map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
		SAMLmetaJS.map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
	
		SAMLmetaJS.mapmarker = new google.maps.Marker({
			position: latLng,
			title: 'Point A',
			map: SAMLmetaJS.map,
			draggable: true
		});
	
		tabnode.tabs({
			"show": function(event, ui) {
				if (ui.panel.id == "location") {
					console.log('google resize');
					google.maps.event.trigger(SAMLmetaJS.map, 'resize');
			        // SAMLmetaJS.map.checkResize(); 
			    }
			}
		});


		// Update current position info.
		updateMarkerPosition(latLng);
		geocodePosition(latLng);

		// Add dragging event listeners.
		google.maps.event.addListener(SAMLmetaJS.mapmarker, 'dragstart', function() {
			updateMarkerAddress('Dragging...');
		});

		google.maps.event.addListener(SAMLmetaJS.mapmarker, 'drag', function() {
			updateMarkerStatus('Dragging...');
			updateMarkerPosition(SAMLmetaJS.mapmarker.getPosition());
		});

		google.maps.event.addListener(SAMLmetaJS.mapmarker, 'dragend', function() {
			updateMarkerStatus('Drag ended');
			updateMarkerPosition(SAMLmetaJS.mapmarker.getPosition());
			geocodePosition(SAMLmetaJS.mapmarker.getPosition());
			
			$("input#includeLocation").attr('checked', true);
		});


		
		
		
	},

	"embrace": function(node) {
	

		$(node).wrap('<div id="rawmetadata"></div>');
		$(node).parent().wrap('<div id="tabs" />');
	
		
		var metatab = $(node).parent();
		var tabnode = $(node).parent().parent();

		var pluginTabs = {'list': [], 'content': []};
		SAMLmetaJS.pluginEngine.execute('addTab', [pluginTabs]);

		
		metatab.append('<div>' +
							'<button class="prettify">Pretty format</button>' +
							'<button class="wipe">Wipe</button>' +
						'</div>');
		
		tabnode.prepend('<ul>' +
							'<li><a href="#rawmetadata">Metadata</a></li>' +
							'<li><a href="#info">Information</a></li>' +
 							'<li><a href="#contact">Contacts</a></li>' +
							'<li><a href="#location">Location</a></li>' +
							'<li><a href="#attributes">Attributes</a></li>' +
							'<li><a href="#saml2sp">SAML Endpoints</a></li>' +
							'<li><a href="#certs">Certificates</a></li>' +
							pluginTabs.list.join('') +
						'</ul>');
		tabnode.append('<div id="info">' +

							'<fieldset class="entityid"><legend>Entity ID</legend>' +
								'<div id="div-entityid">' +
									'<input style="width: 600px" type="text" name="entityid" id="entityid" value="" />' +
									'<p style="margin: 0px">The format MUST be an URI.</p>' +
								'</div>' +
							'</fieldset>' +

							'<fieldset class="name"><legend>Name of Service</legend>' +
								'<div id="infoname"></div>' +
								'<div>' +
									'<button class="addname">Add name in one more language</button>' +
								'</div>' +
							'</fieldset>' +


							'<fieldset class="description"><legend>Description of Service</legend>' +
								'<div id="infodescr"></div>' +
								'<div>' +
									'<button class="adddescr">Add description in one more language</button>' +
								'</div>' +
							'</fieldset>' +

						'</div>' +

						'<div id="contact">' +
							'<div class="content"></div>' +
							'<div><button class="addcontact">Add new contact</button></div>' +
						'</div>' +

						'<div id="location">' +
							'<div class="content">' +
							' <div id="map_info">' +
							'  <p><input type="checkbox" id="includeLocation" name="includeLocation" /> ' +
							'   <label for="includeLocation">Associate this entity with the location below.' +
							' Drag the marker to set the correct location.</label></p>' +
							'  <p><input type="input" id="geolocation" style="width: 30em" disabled="disabled" name="location" value="" />' + 
							'   <span id="locationDescr"></span>' +
							'  </p>' +
							' </div>' +
							' <div id="map_canvas" style="width:100%; height:500px"></div>' +
							'</div>' +
						'</div>' +

						'<div id="attributes">' +

							'<div class="content"></div>' +

							'<div>' +
								'<button class="selectall">Select all</button>' +
								'<button class="unselectall">Unselect all</button>' +
							'</div>' +

						'</div>' +

						'<div id="saml2sp">' +
							'<div class="content"></div>' +
							'<div><button class="addendpoint">Add new endpoint</button></div>' +
						'</div>' +

						'<div id="certs">' +

							'<div class="content"></div>' +
							'<div><button class="addcert">Add new certificate</button></div>' +

						'</div>'  + pluginTabs.content.join(''));

		
		this.maps(tabnode);
	
	},
	





	"clearInfoname": function() {
		$("div#info div#infoname").empty();
	},
	"clearInfodescr": function() {
		$("div#info div#infodescr").empty();
	},
	"setEntityID": function(entityid) {
		$("input#entityid").val(entityid);
	},
	"setLocation": function(location) {
		$("input#geolocation").val(location);
		$("input#includeLocation").attr('checked', true);
	},
	"addInfoname": function(lang, name) {
		var infoHTML;
		var randID = 'infoname' + Math.floor(Math.random() * 10000 + 1000);
		
		infoHTML = '<div class="infonamediv">' +
				'<select name="' + randID + '-lang-name" id="' + randID + '-lang">';

		var languageFound = false;
		for (var language in SAMLmetaJS.Constants.languages) {
			var checked = '';
			if (lang == language) {
				checked = ' selected="selected" ';
				languageFound = true;
			}
			infoHTML += '<option value="' + language + '" ' + checked + '>' + 
				SAMLmetaJS.Constants.languages[language] + 
				'</option>';
		}
		if (!languageFound) {
			infoHTML += '<option value="' + lang + '" selected="selected">Unknown language (' + lang + ')</option>';
		}
		
		
		infoHTML += '</select>' +
			'<input type="text" name="' + randID + '-name-name" id="' + randID + '-name" value="' + (name || '') + '" />' +
			'<button style="" class="removename">Remove</button>' +
			'</div>' 
		

		$(infoHTML).appendTo("div#info div#infoname").find('button.removename').click(function(e) {
			e.preventDefault();
			$(e.target).closest('div.infonamediv').remove();
		});
	},
	"addInfodescr": function(lang, descr) {
		var infoHTML;
		var randID = 'infodescr' + Math.floor(Math.random() * 10000 + 1000);
		
		infoHTML = '<div class="infodescrdiv"><div>' +
				'<select name="' + randID + '-lang-name" id="' + randID + '-lang">';
		
		var languageFound = false;
		for (var language in SAMLmetaJS.Constants.languages) {
			var checked = '';
			if (lang == language) {
				checked = ' selected="selected" ';
				languageFound = true;
			}
			infoHTML += '<option value="' + language + '" ' + checked + '>' + 
				SAMLmetaJS.Constants.languages[language] + 
				'</option>';
		}
		if (!languageFound) {
			infoHTML += '<option value="' + lang + '" selected="selected">Unknown language (' + lang + ')</option>';
		}
		
		
		infoHTML += '</select>' + 
			'<button style="" class="removedescr">Remove</button>' +
			'</div><div>' +
			'<textarea name="' + randID + '-name-name" id="' + randID + '-name">' + (descr || '') + '</textarea>' +

			'</div></div>' 
		
		$(infoHTML).appendTo("div#info div#infodescr").find('button.removedescr').click(function(e) {
			e.preventDefault();
			$(e.target).closest('div.infodescrdiv').remove();
		});
	},


	"addCert": function(use, cert) {
		
		var infoHTML;
		var randID = 'cert' + Math.floor(Math.random() * 10000 + 1000);
		
		infoHTML = '<fieldset><legend>Certificate</legend>' +
				'<select class="certuse" name="' + randID + '-use-name" id="' + randID + '-use">';
		

		for (var key in SAMLmetaJS.Constants.certusage) {
			var checked = '';
			if (key == use) checked = ' selected="selected" ';
			infoHTML += '<option value="' + key + '" ' + checked + '>' + 
				SAMLmetaJS.Constants.certusage[key] + 
				'</option>';
		}
		
		
		infoHTML += '</select>' +
			'<textarea class="certdata" style="" name="' + randID + '-data" id="' + randID + '-data-name">' + (cert || '') + '</textarea>' +
			'<button style="display: block" class="removecert">Remove</button>' +
			'</fieldset>';

		$(infoHTML).appendTo("div#certs > div.content").find('button.removecert').click(function(e) {
			e.preventDefault();
			$(e.target).closest('fieldset').remove();
		});
	},
	"clearCerts": function() {
		$("div#certs > div.content").empty();
	},

	"clearContacts": function() {
		$("div#contact > div.content").empty();
	},
	"addContact": function(contact) {
		
		var randID = Math.floor(Math.random() * 10000 + 1000);
		
		var contactHTML = '<fieldset><legend>Contact</legend>' +

			'<div>' +
				'<label for="contact-' + randID + '-type">Contact type: </label>' +
				'<select name="contact-' + randID + '-type-name" id="contact-' + randID + '-type">';


		for (var contactType in SAMLmetaJS.Constants.contactTypes) {
			var checked = '';
			if (contact.contactType == contactType) checked = ' selected="selected" ';
			contactHTML += '<option value="' + contactType + '" ' + checked + '>' + 
				SAMLmetaJS.Constants.contactTypes[contactType] + 
				'</option>';
		}
		
		
		contactHTML += '</select>' +
			'</div>' +
			
			'<div class="contactfield">' +
				'<label for="contact-' + randID + '-givenname">Given name: </label>' +
				'<input type="text" name="contact-' + randID + '-givenname-name" id="contact-' + randID + '-givenname" value="' + (contact.givenName || '') + '" />' +
			'</div>' +
			
			'<div class="contactfield">' +
				'<label for="contact-' + randID + '-surname">Surname: </label>' +
				'<input type="text" name="contact-' + randID + '-givenname-name" id="contact-' + randID + '-surname" value="' + (contact.surName || '') + '" />' +
			'</div>' +
			
			'<div class="contactfield">' +
				'<label for="contact-' + randID + '-email">E-mail: </label>' +
				'<input type="text" name="contact-' + randID + '-email-name" id="contact-' + randID + '-email" value="' + (contact.emailAddress || '')+ '" />' +
			'</div>' +
			
			'<button style="display: block; clear: both" class="remove">Remove</button>' +
			
		'</fieldset>';
		

		$(contactHTML).appendTo("div#contact > div.content").find('button.remove').click(function(e) {
			e.preventDefault();
			$(e.target).closest('fieldset').remove();
		});

	},
	"clearEndpoints": function() {
		$("div#saml2sp > div.content").empty();
	},
	"addEndpoint": function(endpoint, endpointname) {

		var checked, endpointHTML;		
		var randID ='endpoint-' + Math.floor(Math.random() * 10000 + 1000);
		
		// ---- Type of endpoint selector
		endpointHTML = '<fieldset><legend>' + (endpointname || 'Endpoint') + '</legend>' +
			'<div class="endpointfield">' +
				'<label for="' + randID + '-type">Endpoint type: </label>' +
				'<select class="datafield-type" name="' + randID + '-type-name" id="' + randID + '-type">';

		for (var endpointType in SAMLmetaJS.Constants.endpointTypes.sp) {
			checked = '';
			if (endpointType == endpointname) {
				checked = ' selected="selected" ';
			}
			endpointHTML += '<option value="' + endpointType + '" ' + checked + '>' + 
				SAMLmetaJS.Constants.endpointTypes.sp[endpointType] + 
				'</option>';
		}
		endpointHTML += '</select></div>';
		
		if (endpoint.index) {
			endpointHTML += '<input type="hidden" class="datafield-index" id="' + randID + '-binding" name="' + randID + '-index-name" value="' +
				endpoint.index + '" />';
		}
		

		// ---- Binding		
		endpointHTML += '<div class="endpointfield"><label for="' + randID + '-binding">Binding: </label>' +
				'<select class="datafield-binding" name="' + randID + '-binding-name" id="' + randID + '-binding">';

		var foundBinding = false;
		for (var binding in SAMLmetaJS.Constants.bindings) {
			checked = '';
			if (endpoint.Binding == binding) {
				checked = ' selected="selected" ';
				foundBinding = true;
			}
			endpointHTML += '<option value="' + binding + '" ' + checked + '>' + 
				SAMLmetaJS.Constants.bindings[binding] + 
				'</option>';
		}
		if (endpoint.Binding && !foundBinding) {
			endpointHTML += '<option value="' + endpoint.Binding + '" selected="selected">Unknown binding (' + endpoint.Binding + ')</option>';			
		}
		endpointHTML += '</select>' +
			'</div>';
		
		
		// Text field for location
		endpointHTML +=	'<div class="endpointfield endpointfield-location">' +
				'<label for="' + randID + '-location">  Location</label>' +
				'<input class="datafield-location" type="text" name="' + randID + '-location-name" id="contact-' + randID + '-location" value="' + (endpoint.Location || '') + '" /></div>';
		
		// Text field for response location
		endpointHTML +=	'<div class="endpointfield">' + 
				'<label for="' + randID + '-locationresponse">  Response location</label>' +
				'<input class="datafield-responselocation" type="text" name="' + randID + '-locationresponse-name" id="contact-' + randID + '-locationresponse" value="' + (endpoint.ResponseLocation || '') + '" />' +
			'</div>';
		
			
		endpointHTML += '<button style="display: block; clear: both" class="remove">Remove</button>' +
			'</fieldset>';
		
		$(endpointHTML).appendTo("div#saml2sp > div.content").find('button.remove').click(function(e) {
			e.preventDefault();
			$(e.target).closest('fieldset').remove();
		});

	},
	"setAttributes": function(attributes) {
	
		if (!attributes) attributes = {};
	
		var attributeHTML, checked;
		attributeHTML = '';
		for(var attrname in SAMLmetaJS.Constants.attributes) {
			checked = (attributes[attrname] ? 'checked="checked"' : '');
			attributeHTML += '<div style="float: left; width: 300px"><input type="checkbox" id="' + attrname + '-id" name="' + attrname + '" ' + checked + '/>' + 
				'<label for="' + attrname + '-id">' + SAMLmetaJS.Constants.attributes[attrname] + '</label></div>';

		}
		attributeHTML += '<br style="height: 0px; clear: both" />';
		$("div#attributes > div.content").empty();
		$("div#attributes > div.content").append(attributeHTML);		
	},
};



