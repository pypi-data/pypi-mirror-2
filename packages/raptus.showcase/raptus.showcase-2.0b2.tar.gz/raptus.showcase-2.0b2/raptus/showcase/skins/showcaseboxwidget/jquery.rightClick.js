// jQuery Right-Click Plugin
//
// Version 1.01
//
// Cory S.N. LaViska
// A Beautiful Site (http://abeautifulsite.net/)
// 20 December 2008
//
// Visit http://abeautifulsite.net/notebook/68 for more information
//
// Usage:
//
//		// Capture right click
//		$("#selector").rightClick( function(e) {
//			// Do something
//		});
//		
//		// Capture right mouse down
//		$("#selector").rightMouseDown( function(e) {
//			// Do something
//		});
//		
//		// Capture right mouseup
//		$("#selector").rightMouseUp( function(e) {
//			// Do something
//		});
//		
//		// Disable context menu on an element
//		$("#selector").noContext();
// 
// History:
//
//		1.01 - Updated (20 December 2008)
//		     - References to 'this' now work the same way as other jQuery plugins, thus
//		       the el parameter has been deprecated.  Use this or $(this) instead
//		     - The mouse event is now passed to the callback function
//		     - Changed license to GNU GPL
//
//		1.00 - Released (13 May 2008)
//
// License:
// 
// This plugin is dual-licensed under the GNU General Public License and the MIT License
// and is copyright 2008 A Beautiful Site, LLC. 
//
if(jQuery) (function(){
	
	jq.extend(jq.fn, {
		
		rightClick: function(handler) {
			jq(this).each( function() {
				jq(this).mousedown( function(e) {
					var evt = e;
					jq(this).mouseup( function() {
						jq(this).unbind('mouseup');
						if( evt.button == 2 ) {
							handler.call( jq(this), evt );
							return false;
						} else {
							return true;
						}
					});
				});
				jq(this)[0].oncontextmenu = function() {
					return false;
				}
			});
			return jq(this);
		},		
		
		rightMouseDown: function(handler) {
			jq(this).each( function() {
				jq(this).mousedown( function(e) {
					if( e.button == 2 ) {
						handler.call( jq(this), e );
						return false;
					} else {
						return true;
					}
				});
				jq(this)[0].oncontextmenu = function() {
					return false;
				}
			});
			return jq(this);
		},
		
		rightMouseUp: function(handler) {
			jq(this).each( function() {
				jq(this).mouseup( function(e) {
					if( e.button == 2 ) {
						handler.call( jq(this), e );
						return false;
					} else {
						return true;
					}
				});
				jq(this)[0].oncontextmenu = function() {
					return false;
				}
			});
			return jq(this);
		},
		
		noContext: function() {
			jq(this).each( function() {
				jq(this)[0].oncontextmenu = function() {
					return false;
				}
			});
			return jq(this);
		}
		
	});
	
})(jQuery);	