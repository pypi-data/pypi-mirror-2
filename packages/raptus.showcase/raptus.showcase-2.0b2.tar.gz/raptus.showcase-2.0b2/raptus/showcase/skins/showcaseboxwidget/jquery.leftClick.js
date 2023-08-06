// jQuery Left-Click Plugin
//
// Version 1.0
//
// Raptus AG
// A Beautiful Site (http://raptus.com/)
//
//
// Usage:
//
//      // Capture left click
//      $("#selector").rightClick( function(e) {
//          // Do something
//      });
//      
//      // Capture left mouse down
//      $("#selector").rightMouseDown( function(e) {
//          // Do something
//      });
//      
//      // Capture left mouseup
//      $("#selector").rightMouseUp( function(e) {
//          // Do something
//      });
// 
// History:
//
//
//      1.00 - Released (23 October 2009)
//
// License:
// 
// This plugin is GNU General Public License
//
if(jQuery) (function(){
    
    jq.extend(jq.fn, {
        
        leftClick: function(handler) {
            jq(this).each( function() {
                jq(this).mousedown( function(e) {
                    var evt = e;
                    jq(this).mouseup( function() {
                        jq(this).unbind('mouseup');
                        if( evt.button == 0 || evt.button == 1 ) {
                            handler.call( jq(this), evt );
                            return false;
                        } else {
                            return true;
                        }
                    });
                });
            });
            return jq(this);
        },      
        
        leftMouseDown: function(handler) {
            jq(this).each( function() {
                jq(this).mousedown( function(e) {
                    if( e.button == 0 || e.button == 1) {
                        handler.call( jq(this), e );
                        return false;
                    } else {
                        return true;
                    }
                });
            });
            return jq(this);
        },
        
        leftMouseUp: function(handler) {
            jq(this).each( function() {
                jq(this).mouseup( function(e) {
                    if( e.button == 0 || e.button == 1) {
                        handler.call( jq(this), e );
                        return false;
                    } else {
                        return true;
                    }
                });
            });
            return jq(this);
        }
        
    });
    
})(jQuery); 