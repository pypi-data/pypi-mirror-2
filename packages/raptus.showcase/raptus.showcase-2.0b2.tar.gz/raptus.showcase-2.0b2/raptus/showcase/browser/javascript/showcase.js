jq(document).ready(function (){
    $showcasebox = jq('.showcasebox');
    $showcasebox.before('<div id="tooltip"></div>');
    $tooltip = jq('#tooltip');
    $tooltip.css('z-index', '100000001')
            .css('position', 'absolute')
            .css('display', 'none');
    $tooltip.append('<h1 class="tooltip_title"></h1>');
    $tooltip.append('<span class="tooltip_description"></span>');
 
    $image = $showcasebox.find('.wrapper');
    
    var interval = null;
    var titleBuffer = '';
    var descriptionBuffer = '';
    
    $image.mouseover(function(e){
        titleBuffer = jq(this).find('a').attr('title');
        descriptionBuffer = jq(this).attr('title');
        jq(this).find('a').removeAttr('title');
        jq(this).removeAttr('title');
    });
    
    $image.mousemove(function(e){
        $tooltip.css('display', 'none');
        window.clearInterval(interval);
        
        $tooltip.find('.tooltip_title').empty().append(titleBuffer);
        $tooltip.find('.tooltip_description').empty().append(descriptionBuffer);

        
        $tooltip.css('top',  (e.pageY)+'px');
        $tooltip.css('left', (e.pageX)+'px');
        
        if(jq(this).find('a').length != 0){
            $tooltip = jq('#tooltip')
            $tooltip.css('display', 'block');
        }
    });
    
    $image.mouseout(function(e){
        jq(this).find('a').attr('title' , titleBuffer);
        jq(this).attr('title', descriptionBuffer);
        $tooltip.css('display', 'none');
        window.clearInterval(interval);
    });
    
    $tooltip.mouseover(function(e){
        $tooltip.css('display', 'block');
    });
});