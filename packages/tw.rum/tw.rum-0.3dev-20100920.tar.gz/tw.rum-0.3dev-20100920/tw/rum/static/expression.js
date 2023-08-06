dojo.require("dojo.NodeList-traverse");
dojo.addOnLoad(
    function(){
        var operatorselectfield_propagate_css_class=function(osf){
            var arity='binary';
               var option_node = dojo.query('[value="'+osf.value+'"]', osf)[0];
               dojo.forEach(
                   //target.classList,
                   option_node.className.split(" "),
                   function(selected_class) {
                       dojo.forEach(arity_classes, function(cls){
                           if (selected_class==cls){
                               arity=cls;
                           }
                       });
                   });    
               
               var query_widget = dojo.NodeList(osf).closest('.rum-querybuilder-expression');
               dojo.forEach(arity_classes, function(cls){
                   query_widget.removeClass(cls);
               });
               query_widget.addClass(arity);

               query_widget = query_widget[0];

               if (arity=='unary'){
                   dojo.forEach(dojo.query(".argumentfield", query_widget), dojo.destroy);
                   dojo.forEach(dojo.query(".argumentfield-element", query_widget), dojo.destroy);
               }
               if (arity=='binary'){
                   dojo.forEach(dojo.query(".argumentfield-element", query_widget), dojo.destroy);
                   if (dojo.query(".argumentfield", query_widget).length==0){
                       //recreate elements
                       
                       dojo.create("input", {
                            type:'text',
                            name: osf['name'].slice(0,-2)+".a",
                            class: 'argumentfield'
                            },
                            query_widget,
                            'last'
                            );
                   }
               }
               if (arity=='n-ary'){
                   dojo.forEach(dojo.query(".argumentfield", query_widget), dojo.destroy);
                      if (dojo.query(".argumentfield-element", query_widget).length==0){
                          //recreate elements
                          var i;
                          for (i=0;i<5;i++){
                          dojo.create("input", {
                               type:'text',
                               name: osf['name'].slice(0,-2)+".a-"+i,
                               class: 'argumentfield-element'
                               },
                               query_widget,
                               'last'
                               );
                           }
                      }
                  }

               
        }
        arity_classes=['n-ary','binary', 'unary'];
        dojo.forEach(dojo.query('.operatorselectfield'), function(osf){
            operatorselectfield_propagate_css_class(osf);
        });
        dojo.query('.operatorselectfield').connect('change', function (event){
           operatorselectfield_propagate_css_class(event.target);
        });

});