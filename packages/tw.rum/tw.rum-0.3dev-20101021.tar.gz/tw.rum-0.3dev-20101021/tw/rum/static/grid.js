dojo.require("dojo.string");
dojo.require("dojo.cookie");
registered_columns = Object()
register_column = function(column){
    registered_columns[column]=1;
}
rum_grid_restore_column_state = function(column){
    var modifier="rum_column_visibility_"+column.match("--.*")[0].slice(2);
    var modifier_dict=dojo.cookie(modifier);
    if (modifier_dict==undefined){
        return undefined
    } else {
        modifier_dict=dojo.fromJson(modifier_dict);
    }
    return modifier_dict[column];
   
}

rum_grid_save_column_state = function (column, state){
    var modifier="rum_column_visibility_"+column.match("--.*")[0].slice(2);
    var modifier_dict=dojo.cookie(modifier);
    if (modifier_dict==undefined){
        modifier_dict=Object()
    } else {
        modifier_dict=dojo.fromJson(modifier_dict);
    }
    modifier_dict[column]=state;
    dojo.cookie(modifier, dojo.toJson(modifier_dict), {
                expires: 365*10
    });
    
}
rum_grid_show_column = function(selected_class){
    rum_grid_save_column_state(selected_class, "show");
    var column_cells=dojo.query("."+ selected_class);
    column_cells.removeClass("hidden-column");
    var shower=dojo.query("."+selected_class+".shower");
    shower.addClass("hidden-column");
}
rum_grid_hide_column = function(selected_class){
    rum_grid_save_column_state(selected_class, "hide");
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
            //target.classList,
            target.className.split(" "),
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
            //target.classList,
            target.className.split(" "),
            function(selected_class) {
                if (selected_class.indexOf("named_column_")==0){
                    rum_grid_show_column(selected_class);
                }
            }
        );
      
    });
    
    
   
    
    for (var column in registered_columns) {
        var state=rum_grid_restore_column_state(column);//dojo.cookie("column_state_"+column);
           if (state=="show"){
               rum_grid_show_column(column);
           }
           if (state=="hide"){
               rum_grid_hide_column(column);
           }
    }
   
});
