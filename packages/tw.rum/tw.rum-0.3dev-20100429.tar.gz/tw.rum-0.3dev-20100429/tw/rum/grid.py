from genshi.input import HTML
from tw import framework
from tw.api import Link, CSSLink
from tw.forms import DataGrid
from tw.forms.datagrid import Column
from rum import app
from rum.query import asc, desc
from rum.fields import Number
from tw.dojo import dojo_js
from tw.api import JSLink
modname = "tw.rum"

grid_js = JSLink(
    modname=modname,
    filename='static/grid.js',
    javascript=[dojo_js]
)

class RumDataGrid(DataGrid):
    css_class = "rum-grid"
    css = [CSSLink(modname=modname, filename="static/grid.css")]
    javascript = [grid_js]
    actions = ["show", "edit", "confirm_delete"]
    params = ["actions", "icons", "query", "hidden_columns"]
    hidden_columns=[]
    icons = {
        'edit': Link(modname=modname, filename="static/pencil.png"),
        'show': Link(modname=modname, filename="static/pencil_go.png"),
        'confirm_delete': Link(modname=modname,
                               filename="static/pencil_delete.png"),
        }
    template="tw.rum.templates.datagrid"
    def __init__(self, *args, **kw):
        super(RumDataGrid, self).__init__(*args, **kw)
        self.fields.insert(0, (' ', self.row_links))

    def row_links(self, row):
        tpl = u'<a class="rum-grid-action rum-grid-%(action)s noprint" href="%(url)s" title="%(title)s">'\
              u'<img alt="%(title)s" src="%(src)s" /></a>'
        return HTML('<span class="rum-grid-action">' +''.join(tpl % {
            'url': app.url_for(obj=row, action=action),
            'src': self.icons[action].link,
            'title': framework.translator(action),
            'action': action
            } for action in self.actions) +"</span>")



    
    def row_class(self, i, row):
        if i%2==1:
            return "odd"
        else:
            return "even"
    
    def update_params(self, d):
        super(RumDataGrid, self).update_params(d)
        query = d.query
        
        def css_for_column_header(i, col):
            res=["col_"+str(i)]
            if query.sort:
                first=query.sort[0]
                if first==asc(col.name):
                    res.append("rum-data-grid-asc")
                else:
                    if first==desc(col.name):
                        res.append("rum-data-grid-desc")
            return " ".join(res)
        def data_field_class(col):
            field=col.options.get("field", None)
            if isinstance(field, Number):
                return "number_field"
            else:
                return "normal_field"
        def field_classifier(col):
            return "named_column_"+col.name

                
        def link_for_sort_key(sort_key):
            if query.sort:
                old_sort=[c for c in query.sort if not c in [asc(sort_key),desc(sort_key)]]
            else:
                old_sort=[]
            prepend=asc(sort_key)
            if query.sort and query.sort[0]==asc(sort_key):
                prepend=desc(sort_key)
            new_sort=[prepend]+old_sort
            new_query = query.clone(sort=new_sort)
            action=app.request.routes['action']
            return app.url_for(action=action, **new_query.as_flat_dict())
        def sortable_column(col):
            return "field" in col.options and getattr(col.options["field"], "sortable", False)
        d.link_for_sort_key = link_for_sort_key
        d.css_for_column_header=css_for_column_header
        d.sortable_column=sortable_column
        d.data_field_class=data_field_class
        d.field_classifier = field_classifier
        d.row_class = self.row_class