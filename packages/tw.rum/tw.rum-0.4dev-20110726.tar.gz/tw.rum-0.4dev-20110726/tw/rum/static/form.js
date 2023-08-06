dojo.addOnLoad(
    function()   {
    var l=dojo.query('.listform input, .listform input, .listform select');
    var i;
    var node;
    for(i=0;i<l.length;i++){
        node=l[i];
        if (node['type']!='hidden') {
            node.focus();
            return;
        }
    }
});