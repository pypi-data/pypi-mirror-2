dojo.require("dojo.string");
rum_grid_show_column = function(selected_class){
    var column_cells=dojo.query("."+ selected_class);
    column_cells.removeClass("hidden-column");
    var shower=dojo.query("."+selected_class+".shower");
    shower.addClass("hidden-column");
}
rum_grid_hide_column = function(selected_class){
    var column_cells=dojo.query("."+ selected_class);
    column_cells.addClass("hidden-column");
    var shower=dojo.query("."+selected_class+".shower");
    shower.removeClass("hidden-column");
}
dojo.addOnLoad(function()
{   
    dojo.query(".rum-grid tr").connect("click", function(e){
        var show_links=dojo.query(".rum-grid-show", e.currentTarget);
        console.log(show_links[0]["href"]);
        if (show_links.length>0){
            window.location = show_links[0]["href"];
        }
        
        
        

    });
    dojo.query(".rum-grid a").connect("click", function(e){
        
      e.stopPropagation();  
    });
    /*dojo.query(".shower").addClass("hidden-column");*/
    dojo.query(".hider").connect("click",function(e){
        e.preventDefault();
        e.stopPropagation();
        var target = e.target;
        dojo.forEach(
            target.classList,
            function(selected_class) {
                if (selected_class.indexOf("named_column_")==0){
                    rum_grid_hide_column(selected_class);
                }
            }
        );
      
    });
    dojo.query(".shower").connect("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var target = e.currentTarget;
        dojo.forEach(
            target.classList,
            function(selected_class) {
                if (selected_class.indexOf("named_column_")==0){
                    rum_grid_show_column(selected_class);
                }
            }
        );
      
    });
});
