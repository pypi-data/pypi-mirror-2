/*
 * 
 */

jq(document).ready(function (){
    var showcasebox = new Showcasebox(15, 30);
});

function Showcasebox (_raster, _minSize) {
   _minSize = snapOnRaster(_minSize);
   if(_minSize<_raster)_minSize = _raster;
   
   
//attributs
   var _$showcase = jq('.showcasebox');
   
   
/*
 * first set a z index to the images...
 */
$wrapped_images = _$showcase.find('.wrapper')
var zindex = 1
$wrapped_images.each(function(i) {
    jq(this).css('z-index', zindex);
    zindex++;
    save(jq(this))
  });
   
//methods
  /*
   * this method remove all editable class in the Showcasebox
   */
    function clearables(){
        //remove moveable...
        _$showcase.find('.moveable').removeClass('moveable');
        
        //remove clippingable...
        _$showcase.find('.clippingable').removeClass('clippingable');
        
        //remove contextmenu...
        _$showcase.find('.contextmenu').remove();
        
        
    }
    
    function moveable($jquery){
        $jquery.addClass('moveable');
    }
    
    function clippingable($jquery){
        $jquery.addClass('clippingable');
    }
    
    function editablelayer($jquery, resetEvent){
        var resetEvent = (resetEvent == null) ? true : resetEvent;
        $editablelayer =_$showcase.find('.editablelayer');
        if($editablelayer.length != 8)
        {
            _$showcase.prepend('<div id="n-editablelayer"'+
                                            'class="editablelayer side">'+
                                       '</div>')
                              .prepend('<div id="e-editablelayer"'+
                                            'class="editablelayer side">'+
                                       '</div>')
                              .prepend('<div id="s-editablelayer"'+
                                            'class="editablelayer side">'+
                                       '</div>')
                              .prepend('<div id="w-editablelayer"'+
                                            'class="editablelayer side">'+
                                       '</div>')
                              .prepend('<div id="nw-editablelayer"'+
                                            'class="editablelayer corner">'+
                                       '</div>')
                              .prepend('<div id="ne-editablelayer"'+
                                            'class="editablelayer corner">'+
                                       '</div>')
                              .prepend('<div id="se-editablelayer"'+
                                            'class="editablelayer corner">'+
                                       '</div>')
                              .prepend('<div id="sw-editablelayer"'+
                                            'class="editablelayer corner">'+
                                       '</div>');
        }
        
        if(resetEvent)
        {   
            $editablelayer.unbind('mouseover');
            $editablelayer.unbind('mousedown');
            $editablelayer.unbind('mouseup');
            $editablelayer.unbind('mouseout');
            
            $editablelayer.mouseover(function(e){
                editablelayer($jquery, false);
                editable($jquery);
            });
            
            $editablelayer.mouseout(function(e){
                uneditable();
            });
            
            $editablelayer.leftMouseDown(function(e){
                clippingable($jquery);
                if     (jq(this).attr('id') == 'nw-editablelayer'){
                    clipping(e, 'nw');
                }
                else if(jq(this).attr('id') == 'ne-editablelayer'){
                    clipping(e, 'ne');
                }
                else if(jq(this).attr('id') == 'se-editablelayer'){
                    clipping(e, 'se');
                }
                else if(jq(this).attr('id') == 'sw-editablelayer'){
                    clipping(e, 'sw');                    
                }                   
                jq(document).mouseup(function(e){
                    uneditable();
                    clearables();
                    $editablelayer.unbind('mouseover');
                    $editablelayer.unbind('mousedown');
                    $editablelayer.unbind('mouseup');
                    $editablelayer.unbind('mouseout');
                    jq(this).unbind('mouseup');
                    jq(this).unbind('mousemove');
                });
            }); 
        }    
        
        $north = _$showcase.find('#n-editablelayer');
        $north.css( 'top',   (parseInt($jquery.css('top'))-parseInt($north.css('height')))+'px')
              .css( 'left',  $jquery.css('left'))
              .css( 'width', $jquery.css('width'))
              .show();
        
        $south = _$showcase.find('#s-editablelayer');
        $south.css( 'top',   (parseInt($jquery.css('top'))+parseInt($jquery.css('height')))+'px')
              .css( 'left',  $jquery.css('left'))
              .css( 'width', $jquery.css('width'))
              .show();
        
        $east = _$showcase.find('#e-editablelayer');
        $east.css( 'top',    $jquery.css('top'))
             .css( 'left',   (parseInt($jquery.css('left'))+parseInt($jquery.css('width')))+'px')
             .css( 'height', $jquery.css('height'))
             .show();
        
        $west = _$showcase.find('#w-editablelayer');
        $west.css( 'top',    $jquery.css('top'))
             .css( 'left',   (parseInt($jquery.css('left'))-parseInt($west.css('width')))+'px')
             .css( 'height', $jquery.css('height'))
             .show();
             
        $northwest = _$showcase.find('#nw-editablelayer');
        $northwest.css( 'top', (parseInt($jquery.css('top'))-parseInt($northwest.css('height'))/2)+'px')
                  .css( 'left',(parseInt($jquery.css('left'))-parseInt($northwest.css('width'))/2)+'px')
                  .show();
                  
        $northeast = _$showcase.find('#ne-editablelayer');
        $northeast.css( 'top', (parseInt($jquery.css('top'))-parseInt($northeast.css('height'))/2)+'px')
                  .css( 'left',(parseInt($jquery.css('left'))+parseInt($jquery.css('width'))-parseInt($northeast.css('width'))/2)+'px')
                  .show();
                  
        $southwest = _$showcase.find('#sw-editablelayer');
        $southwest.css( 'top', (parseInt($jquery.css('top'))+parseInt($jquery.css('height'))-parseInt($northeast.css('width'))/2)+'px')
                  .css( 'left',(parseInt($jquery.css('left'))-parseInt($southwest.css('width'))/2)+'px')
                  .show();
                  
        $southeast = _$showcase.find('#se-editablelayer');
        $southeast.css( 'top', (parseInt($jquery.css('top'))+parseInt($jquery.css('height'))-parseInt($northeast.css('height'))/2)+'px')
                  .css( 'left',(parseInt($jquery.css('left'))+parseInt($jquery.css('width'))-parseInt($northeast.css('width'))/2)+'px')
                  .show();
    }
    
    function editable($jquery){
        editablelayer($jquery);
        _$showcase.find('.editable').removeClass('editable');
        $jquery.addClass('editable');
    }
    
    function uneditable(){
        $editablelayer = _$showcase.find('.editablelayer');
        $editablelayer.hide();
        _$showcase.find('.editable').removeClass('editable');
    }
    
    function clipping(e, way){
        x = 0;
        y = 0;
        oldX = e.pageX;
        oldY = e.pageY;
        $image = _$showcase.find('.clippingable');
        $img = $image.find('.img');
        oldW = parseInt($image.css('width'));
        oldH = parseInt($image.css('height'));
        oldL = parseInt($image.css('left'));
        oldT = parseInt($image.css('top'));
        oldImgL = parseInt($img.css('left'));
        oldImgT = parseInt($img.css('top'));
        
        jq(document).mousemove( function(e){
            if($image.hasClass('clippingable')){
                if(way == 'nw'){
                    if(oldL+oldW-_minSize > oldL + (e.pageX - oldX) ){
                        buffer = snapOnRaster(e.pageX - oldX)
                        $img.css('left',   (oldImgL - buffer) + 'px');
                        $image.css('left', (oldL    + buffer) + 'px');
                        $image.css('width',(oldW    - buffer) + 'px');
                        
                    }else{
                        $img.css('left',   (oldImgL - oldW + _minSize) + 'px');
                        $image.css('left', (oldL+oldW-_minSize)        + 'px');
                        $image.css('width',(_minSize)                  + 'px');
                    }
                    
                    if(oldT+oldH-_minSize > (oldT + (e.pageY - oldY)) ){
                        buffer = snapOnRaster(e.pageY - oldY)
                        $img.css('top',      (oldImgT - buffer) + 'px');
                        $image.css('top',    (oldT    + buffer) + 'px');
                        $image.css('height', (oldH    - buffer) + 'px');
                    }else{
                        $img.css('top',      (oldImgT - oldH + _minSize) + 'px');
                        $image.css('top',    (oldT+oldH-_minSize)        + 'px');
                        $image.css('height', (_minSize)                  + 'px');
                    }
                }
                else if(way == 'ne'){
                    $image.css('width',  snapOnRaster(oldW+e.pageX-oldX) +'px');
                    
                    if(oldT+oldH-_minSize > oldT + (e.pageY - oldY) ){
                        buffer = snapOnRaster(e.pageY - oldY)
                        $img.css('top',     (oldImgT - buffer) + 'px');
                        $image.css('top',   (oldT    + buffer) + 'px');
                        $image.css('height',(oldH    - buffer) + 'px');
                    }else{
                        $img.css('top',     (oldImgT - oldH + _minSize) + 'px');
                        $image.css('top',   (oldT+oldH -_minSize)        + 'px');
                        $image.css('height',(_minSize)                  + 'px');
                    }
                }
                else if(way == 'se'){
                    oldW+e.pageX-oldX<0?w=0:w=oldW+e.pageX-oldX;
                    oldH+e.pageY-oldY<0?h=0:h=oldH+e.pageY-oldY;
                    $image.css('width',  snapOnRaster(w)+'px');
                    $image.css('height', snapOnRaster(h)+'px');
                }
                else if(way == 'sw'){
                    $image.css('height', snapOnRaster(oldH+e.pageY-oldY) +'px');
                    if(oldL+oldW-_minSize > oldL + (e.pageX - oldX) ){
                        buffer = snapOnRaster(e.pageX - oldX)
                        $img.css('left',    (oldImgL - buffer) + 'px');
                        $image.css('left',  (oldL    + buffer) + 'px');
                        $image.css('width', (oldW    - buffer) + 'px');
                    }else{
                        $img.css('left',    (oldImgL - oldW + _minSize) + 'px');
                        $image.css('left',  (oldL+oldW-_minSize) + 'px');
                        $image.css('width', (_minSize) + 'px');
                    }
                }
                trueclip($image);
                editablelayer($image);
                save($image)
            }
            
        });
    }
    
    function move(e){
        $image = _$showcase.find('.moveable');
        pos = $image.position();
        x = 0;
        y = 0;
        x = e.pageX-pos.left;
        y = e.pageY-pos.top;
        jq(document).unbind('mousemove')
        jq(document).mousemove( function(e){
            $image = _$showcase.find('.moveable');
            if ($image.length == 0) {
                jq(this).unbind('mousemove')
            }
            else {
                $image.css('left', e.pageX - x).css('top', e.pageY - y)
                trueposition($image);
                editablelayer($image);
            }
        });
    }
    
    function save($jquery){
        var uid    = $jquery.attr('id');
        var left   = $jquery.css('left');
        var top    = $jquery.css('top');
        var width  = $jquery.css('width');
        var height = $jquery.css('height');
        var zindex = $jquery.css('z-index');
        var $img   = $jquery.find('.img')
        var imgLeft = $img.css('left');
        var imgTop  = $img.css('top');
        
        $showcaseInputFields = jq('.showcaseInputFields')
        
        if($showcaseInputFields.find('.img'+uid).length == 0){
            $showcaseInputFields.append('<div class="img'+uid+'"></div>')
        }
        
        $showcaseInputFields.find('.img'+uid)
            .empty()
            .append('<input type="hidden" name="img.uid:records"    value="'+uid+'" />')
            .append('<input type="hidden" name="img.x:records"      value="'+left+'" />')
            .append('<input type="hidden" name="img.y:records"      value="'+top+'" />')
            .append('<input type="hidden" name="img.width:records"  value="'+width+'" />')
            .append('<input type="hidden" name="img.height:records" value="'+height+'" />')
            .append('<input type="hidden" name="img.zindex:records" value="'+zindex+'" />')
            .append('<input type="hidden" name="img.clipLeft:records" value="'+imgLeft+'" />')
            .append('<input type="hidden" name="img.clipTop:records" value="'+imgTop+'" />');
    }

    function trueclip($jquery){
        j_width  = parseInt( $jquery.css('width') );
        j_height = parseInt( $jquery.css('height'));
        j_left   = parseInt( $jquery.css('left')  );
        j_top    = parseInt( $jquery.css('top')   );
        
        $img = $jquery.find('.img')
        
        i_width  = parseInt( $img.css('width') );
        i_height = parseInt( $img.css('height'));
        i_top  = parseInt( $img.css('top') );
        i_left = parseInt( $img.css('left'));
        
        //check is not to big or to small...
        if (j_height<_minSize){
            $jquery.css('height', _minSize+'px');
        }
        if (j_width<_minSize){
            $jquery.css('width', _minSize+'px');
        }
        
        if ( j_width > (i_width+(i_left)) ){
            $jquery.css('width', ((i_width+(i_left)) - i_width%_raster)+'px');
        }
        if ( j_height > (i_height+(i_top)) ){
            $jquery.css('height', ((i_height+(i_top)) - i_height%_raster)+'px');
        }
        
        if(i_left>0){
             $img.css('left', '0px');
             $jquery.css('left', j_left + i_left);
             $jquery.css('width', j_width-i_left);
        }
        if(i_top>0){
             $img.css('top', '0px');
             $jquery.css('top', (j_top+i_top)+'px');
             $jquery.css('height', (j_height-i_top)+'px');
        }
    }
    
    /*
     * thsi method set the $jquery object on a raster position and after
     * it check is this position inside of the showcasebox
     */
    function trueposition($jquery) {
        j_width  = parseInt( $jquery.css('width') );
        j_height = parseInt( $jquery.css('height'));
        j_top    = parseInt( $jquery.css('top') );
        j_left   = parseInt( $jquery.css('left') );
        
        s_width  = parseInt( _$showcase.css('width') );
        s_height = parseInt( _$showcase.css('height'));
      
      //check is on the raster...
        if(j_top%_raster!=0)
        {
            //top position is not on raster...
            $jquery.css('top', snapOnRaster(j_top));
        }
        
        if(j_left%_raster!=0)
        {
            //top position is not on raster...
            $jquery.css('left', snapOnRaster(j_left));
        }
        
      //check is not outsite of shwocase
        if( 1 > j_top+j_height ){
            //outsite top... 
            $jquery.css('top', (_raster-(j_height%_raster)-j_height)+'px');
        }

        if( s_height <  j_top ){
            //outsite bottom...
            $jquery.css('top', s_height-_raster+(j_height%_raster));
        }
        
        if( 1 > j_left+j_width ){
            //outsite left... 
            $jquery.css('left', (_raster-(j_width%_raster)-j_width)+'px');
        }
        
        if( s_width <  j_left ){
            //outsite right...
            $jquery.css('left', s_width-_raster+(j_width%_raster));
        }
      
    }
    
    function snapOnRaster(pos){
        if ((pos % _raster) < (_raster / 2)){
            return pos-(pos % _raster);
        } else {
            return pos+(_raster - pos % _raster);
        }
    }
    
    function contextmenu($jquery, event){
        e = event;
        
        _$showcase.find('.contextmenu').remove(); 
        _$showcase.prepend('<div class="contextmenu" style="position: absolute;">'+
                               '<ul>'+
                                 '<li id="bring_to_front">Bring to Front</li>'+
                                 '<li id="bring_forwart">Bring Forward</li>'+
                                 '<li id="send_backward">Send Backward</li>'+
                                 '<li id="send_to_back">Send to Back</li>'+
                               '</ul>'+
                             '</div>');
        $contextmenu =  _$showcase.find('.contextmenu');
        pos = _$showcase.position();
        $contextmenu.css('left', e.pageX-pos.left-$contextmenu.width()/2)
                    .css('top',  e.pageY-pos.top-$contextmenu.find('li').height()/2);
        
        $contextmenu.find('#bring_to_front').leftMouseDown(function(e){
            removeContextmenu();
            bringToFront($jquery);
        });
        
        $contextmenu.find('#bring_forwart').leftMouseDown(function(e){
            removeContextmenu();
            bringForward($jquery);
        });
        
        $contextmenu.find('#send_backward').leftMouseDown(function(e){
            removeContextmenu();
             sendBackward($jquery);
        });
        
        $contextmenu.find('#send_to_back').leftMouseDown(function(e){
            removeContextmenu();
            sendToBack($jquery);
        });
        
        $contextmenu.mouseover(function(e){
            editablelayer($jquery);
        });
        
        jq(document).mousedown(function(e){
            removeContextmenu();
        });
    }
    
    function removeContextmenu(){
        $contextmenu = _$showcase.find('.contextmenu')
        $contextmenu.remove();
        $contextmenu.unbind('mouseover');
        jq(document).unbind('mousedown');
    }
    
    /*
     * help function for the contextmenu...
     */
    function bringForward($jquery) {
        $images = _$showcase.find('.wrapper');
        
        zindex = $jquery.css('z-index')
        if($images.length != zindex){
            for(i=0; i<$images.length; i++)
            {
                if($images.eq(i).attr('id') == $jquery.attr('id')) {
                    $images.eq(i).css('z-index', parseInt($images.eq(i).css('z-index'))+1);
                } else if( parseInt($images.eq(i).css('z-index')) == parseInt(zindex)+1) {
                    $images.eq(i).css('z-index', parseInt($images.eq(i).css('z-index'))-1);
                }
                save($images.eq(i))
            }
        }
    }
    
    /*
     * help function for the contextmenu...
     */
    function sendBackward($jquery) {
        $images = _$showcase.find('.wrapper');
        
        zindex = $jquery.css('z-index')
        if(1 != zindex){
            for(i=0; i<$images.length; i++)
            {
                if($images.eq(i).attr('id') == $jquery.attr('id')) {
                    $images.eq(i).css('z-index', parseInt($images.eq(i).css('z-index'))-1);
                } else if( parseInt($images.eq(i).css('z-index')) == parseInt(zindex)-1) {
                    $images.eq(i).css('z-index', parseInt($images.eq(i).css('z-index'))+1);
                }
                save($images.eq(i))
            }
        }
    }
    
    /*
     * help function for the contextmenu...
     */
    function bringToFront($jquery) {
        $images = _$showcase.find('.wrapper');
        
        zindex = $jquery.css('z-index')
        if($images.length != zindex){
            for(i=0; i<$images.length; i++)
            {
                if($images.eq(i).attr('id') == $jquery.attr('id')) {
                    $images.eq(i).css('z-index', $images.length);
                } else if( $images.eq(i).css('z-index') > zindex) {
                    $images.eq(i).css('z-index', parseInt($images.eq(i).css('z-index'))-1);
                }
                save($images.eq(i))
            }
        }
    }
    
    /*
     * help function for the contextmenu...
     */
    function sendToBack($jquery) {
        $images = _$showcase.find('.wrapper');
        
        zindex = $jquery.css('z-index')
        if(1 != zindex){
            for(i=0; i<$images.length; i++)
            {
                if($images.eq(i).attr('id') == $jquery.attr('id')) {
                    $images.eq(i).css('z-index', 1);
                } else if( $images.eq(i).css('z-index') < zindex) {
                    $images.eq(i).css('z-index', parseInt($images.eq(i).css('z-index'))+1);
                }
                save($images.eq(i))
            }
        }
    }
   
    var $images = _$showcase.find('.wrapper');
       
  //editablelayer with tools show and hide on mouse over
    $images.mouseover(function(e){
        uneditable();
        editable(jq(this));
    });
    
    $images.mouseout(function(e){
        if(_$showcase.find('.moveable').length == 0){
               uneditable();
        }
    });
    
  //events...
    
    _$showcase.noContext();
  
    $images.leftMouseDown(function(e){
        clearables();
        moveable(_$showcase.find('.editable'));
        move(e);
        
        jq(document).mouseup(function(e){
            clearables();
            uneditable();
            jq(this).unbind('mouseup');
        });
    });
    
    $images.leftMouseUp(function(e){
        save(jq(this));
        clearables();
        jq('body').unbind('mouseup');
        jq(document).unbind('mouseup');
        editable(_$showcase.find('.editable'));
    });
    
    $images.rightMouseDown(function(e){
        clearables();
        contextmenu(jq(this), e);
    });
    
    
  //showcase settings...
    var showcaseInterval = null;
    
    //showcase raster...
    showcaseRaster = jq('#showcaseRaster');
    _raster = showcaseRaster.attr('value');
    showcaseRaster.focus(function(e){
        showcaseInterval = window.setInterval(function(){
            _raster = showcaseRaster.attr('value');
        }, 100)
    });
    showcaseRaster.blur(function(e){
        window.clearInterval(showcaseInterval);
    });
    
    //showcase width...
    showcaseWidth= jq('#showcaseWidth');
   _$showcase.css('width', showcaseWidth.attr('value')+'px');
    showcaseWidth.focus(function(e){
        showcaseInterval = window.setInterval(function(){
            _$showcase.css('width', showcaseWidth.attr('value')+'px');
        }, 100)
    });
    showcaseWidth.blur(function(e){
        window.clearInterval(showcaseInterval);
    });
    
    //showcase height...
   showcaseHeight= jq('#showcaseHeight');
   _$showcase.css('height', showcaseHeight.attr('value')+'px');
    showcaseHeight.focus(function(e){
        showcaseInterval = window.setInterval(function(){
           _$showcase.css('height', showcaseHeight.attr('value')+'px');
        }, 100)
    });
    showcaseHeight.blur(function(e){
        window.clearInterval(showcaseInterval);
    });
    
}
