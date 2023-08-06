/**
 * Google Map Viewlet support for Plone
 */

jq(document).ready(function() {
	
	var map = null;
	var geocoder = null;
	var marker;
	
	var geocoder;
	
	var geoXml = [];
	var markers = [];
	
	var showAddress = function(address) {
	  geocoder.getLatLng(
		address,
		function(point) {
		  if (!point) {
			alert(address + " not found");
		  } else {
			map.setCenter(point, 13);
			var marker = new GMarker(point);
			map.addOverlay(marker);
			map.enableScrollWheelZoom();
			marker.openInfoWindowHtml(address);
		  }
		}
	  );
	}
	
	var loadGM = function() {
		if (window.GBrowserIsCompatible && GBrowserIsCompatible()) {
			map = new GMap2(document.getElementById("googlemaps"));
				
			// Use Small instead of Large for detailed zoom
			//map.addControl(new GSmallMapControl());
			map.addControl(new GLargeMapControl());
			map.addControl(new GScaleControl());
			// kind of map
			map.addControl(new GMapTypeControl());
			// show overview area map
			//map.addControl(new GOverviewMapControl());
	
	
			geocoder = new GClientGeocoder();
			
			addr = document.getElementById("gmaps-location").innerHTML;
			showAddress(addr);
			
			// BBB: very very very ugly, but IE seems to have some bad, non-predictable bug here
			//loadKml();
			setTimeout(loadKml, 3000);
			
			// If map has been loaded, I'll hide related contents
			jq("#relatedItemBox").hide();
		}
		else {
			jq("#googlemaps").text("Seems that your browser doesn't support Google Maps.");
		}
	}	
	
	var addAddressToCenterMap = function(response) {
	   if (!response || response.Status.code != 200) {
			//alert("Sorry, we were unable to geocode that address");
		} else {
			place = response.Placemark[0];
			point = new GLatLng(place.Point.coordinates[1], place.Point.coordinates[0]);
			map.setCenter(point,15)
		}
	}
		   
	var loadKml = function() {
		// Center and zoom on the map
		geocoder.getLocations(addr, addAddressToCenterMap);
		
		var kmls = jq("span.kmlurl");
		
		for (var i=0;i<kmls.length;i++) {
			geoXml.push(kmls[i].innerHTML);
			ngeo = new GGeoXml(geoXml[i]);
			markers.push(ngeo);
			map.addOverlay(ngeo);
		}
	}
	
	/**
	 * Enable/disable a overlay on the map.
	 * Overlays are all saved in the "markers" array.
	 * @param {CheckBox} check The checkbox that trigger the event.
	 * @param {Integer} id index of the overlay.
	 */
	jq(".kmlTrigger").each(function() {
		jq(this).click(function(event) {
			var $this = jq(this);
			var this_checked = $this.attr("checked");
			var id = $this.attr('id').substr(4);
			if (this_checked) {
				map.addOverlay(markers[id]);
			}
			else {
				map.removeOverlay(markers[id]);
			}
		});
	});
	
	loadGM();
});

