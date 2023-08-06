dojo.require("dojo.string");
dojo.require("dojo.cookie");
registered_columns = Object()
register_column = function(column){
    registered_columns[column]=1;
}

dojo.addOnLoad(function()
{   
    var cookie_name= function(column){
        return "rum_column_visibility_"+column.match("--.*")[0].slice(2);
    };
    var rum_grid_restore_column_state = function(column){
        var modifier=cookie_name(column);
        var modifier_dict=dojo.cookie(modifier);
        if (modifier_dict==undefined){
            return undefined
        } else {
            modifier_dict=dojo.fromJson(modifier_dict);
        }
        return modifier_dict[column];

    }

    var rum_grid_save_column_state = function (column, state){
        var modifier=cookie_name(column);
        var modifier_dict=dojo.cookie(modifier);
        if (modifier_dict==undefined){
            modifier_dict=Object()
        } else {
            modifier_dict=dojo.fromJson(modifier_dict);
        }
        modifier_dict[column]=state;
        var cookie_val=dojo.toJson(modifier_dict);
        dojo.cookie(modifier, cookie_val, {
                    expires: 365*10, path:'/'
        });
        console.log('saved', column, state);
        console.log(dojo.cookie(modifier)==cookie_val);

    }
    var rum_grid_show_column = function(selected_class){
        rum_grid_save_column_state(selected_class, "show");
        rum_grid_show_column_raw(selected_class);
    }
    var rum_grid_hide_column = function(selected_class){
        rum_grid_save_column_state(selected_class, "hide");
        rum_grid_hide_column_raw(selected_class);
    }
    var rum_grid_show_column_raw= function(selected_class){
        var column_cells=dojo.query("."+ selected_class);
        column_cells.removeClass("hidden-column");
        var shower=dojo.query("."+selected_class+".shower");
        shower.addClass("hidden-column");
    }
    var rum_grid_hide_column_raw = function(selected_class){
        var column_cells=dojo.query("."+ selected_class);
        column_cells.addClass("hidden-column");
        var shower=dojo.query("."+selected_class+".shower");
        shower.removeClass("hidden-column");
    }
    
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
               rum_grid_show_column_raw(column);
           }
           if (state=="hide"){
               rum_grid_hide_column_raw(column);
           }
    }
   
});
