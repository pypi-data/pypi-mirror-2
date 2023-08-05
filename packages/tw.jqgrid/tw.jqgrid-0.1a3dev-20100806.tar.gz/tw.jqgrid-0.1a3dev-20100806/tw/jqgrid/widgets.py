from tw.api import Widget, JSLink, CSSLink, js_function
from tw.jquery import jquery_js
from tw.jquery.ui import jquery_ui_all_js

__all__ = ["JqGrid","jqgrid_css","jqgrid_search_css"]

# declare your static resources here
i18n_jqgrid = JSLink(modname=__name__,
               filename='static/i18n/grid.locale-en.js',
               javascript=[])

jquery_jqgrid = JSLink(modname=__name__,
               filename='static/javascript/jquery.jqGrid.min.js',
               javascript=[jquery_js, jquery_ui_all_js, i18n_jqgrid])


from tw.uitheme import smoothness_css

jqgrid_css = CSSLink(modname=__name__, filename='static/css/ui.jqgrid.css')
jqgrid_search_css = CSSLink(modname=__name__, filename='static/css/jquery.searchFilter.css')


class JqGrid(Widget):
    """
    jqgrid full options : http://www.trirand.com/jqgridwiki/doku.php?id=wiki:options
    """
    template = """
             <table id="${id}"></table>
             <div id="${id}_pager"></div>
             <div id="${id}_search"></div>
             """

    javascript = [jquery_jqgrid]
    css = [smoothness_css, jqgrid_css, jqgrid_search_css]

    params = {
           "url": "Tells us where to get the data.",
           "datatype" : "This tells jqGrid the type of information being returned so it can construct the grid.",
           "mtype" :"Tells us how to make the ajax call: either 'GET' or 'POST'.",
           "colNames" :"An array in which we place the names of the columns. ",
           # column model options : http://www.trirand.com/jqgridwiki/doku.php?id=wiki:colmodel_options
           "colModel" :"An array that describes the model of the columns.",
           "pager" :"Defines that we want to use a pager bar to navigate through the records.",
           "rowNum" :"Sets how many records we want to view in the grid.",
           "rowList" :"An array to construct a select box element in the pager in which we can change the number of the visible rows.",
           "sortname" :"Sets the initial sorting column.",
           "sortorder": "Sets the initial sort order",
           "viewrecords" :"Defines whether we want to display the number of total records from the query in the pager bar",
           "caption" :"Sets the caption for the grid.",
           "height" : "The height of the grid.",
           "shrinkToFit" : "if True, every column width is scaled according to the defined option width.",
           "width" : "If this option is set, the initial width of each column is set according to the value of shrinkToFit option.",
           "toolbar" : "This option defines the toolbar of the grid. This is array with two values in which the first value enables the toolbar and the second defines the position relative to body Layer.",
           "rownumbers" : "If this option is set to true, a new column at left of the grid is added.",
           "toppager" : "When enabled this option place a pager element at top of the grid below the caption (if available).",
           "autowidth" : "When set to true, the grid width is recalculated automatically to the width of the parent element.",
           "multiselect" : "If this flag is set to true a multi selection of rows is enabled.",
           "multiselectWidth" : "Determines the width of the multiselect column if multiselect is set to true.",
           "subGrid" : "If set to true this enables using a subgrid.",
           "subGridUrl" : "This option points to the file from which we get the data for the subgrid. jqGrid adds the id of the row to this url as parameter. If there is a need to pass additional parameters, use the params option in subGridModel",
           "subGridModel" : "It is an array in which we describe the column model for the subgrid data",
           "subGridWidth" : "Determines the width of the subGrid column if subgrid is enabled. ",
           "subGridRowExpanded" : "This event is raised when the subgrid is enabled and is executed when the user clicks on the plus icon of the grid.",
           }

    datatype = "json"
    mtype = "GET"
    subGrid = False
    toolbar = [False, '']
    rownumbers = False
    toppager = False
    autowidth = False
    multiselect = False
    multiselectWidth = 20
    navbuttons_options = {"view":False, "edit": False, "add": False,"del": False,
                          "search":True,"refresh":False}
    addbutton_options = {}
    editbutton_options = {}
    delbutton_options = {}
    viewbutton_options = {}

    def __init__(self, id, **kwargs):
        """
        """
        super(JqGrid, self).__init__(**kwargs)
#        if not kwargs.get("id", False):
#            raise ValueError, "JqGrid is supposed to have id"
        if not kwargs.get("url", False):
            raise ValueError, "JqGrid must have url for fetching data"
        if not kwargs.get("colModel", False):
            raise ValueError, "JqGrid must have colModel for setting up the columns"

        # default values
        self.pager = kwargs.get("pager", '%s_pager' % self.id)

    def update_params(self, d):
        super(JqGrid, self).update_params(d)
        grid_params = dict(url=self.url,
                           datatype=self.datatype,
                           mtype=self.mtype,
                           colNames=self.colNames,
                           colModel=self.colModel,
                           pager=self.pager,
                           rowNum=self.rowNum,
                           rowList=self.rowList,
                           sortname=self.sortname,
                           sortorder=self.sortorder,
                           viewrecords=self.viewrecords,
                           caption=self.caption,
                           height=self.height,
                           shrinkToFit=self.shrinkToFit,
                           width=self.width,
                           toolbar=self.toolbar,
                           rownumbers=self.rownumbers,
                           toppager=self.toppager,
                           autowidth=self.autowidth,
                           multiselect=self.multiselect,
                           multiselectWidth=self.multiselectWidth,

                           subGrid=self.subGrid,
                           subGridUrl=self.subGridUrl,
                           subGridModel=self.subGridModel,
                           subGridWidth=self.subGridWidth,
                           subGridRowExpanded=self.subGridRowExpanded,
                           )
        call = js_function('jQuery("#%s").jqGrid' % d.id)(grid_params)
        self.add_call(call)
        # search options documentation can be found at:
        # http://www.trirand.com/jqgridwiki/doku.php?id=wiki:singe_searching#options
        nav_call = js_function('jQuery("#%s").jqGrid' % d.id)\
                                 ('navGrid', '#%s_pager' % d.id,
                                     self.navbuttons_options,
                                     #  default settings for edit
                                     self.editbutton_options,
                                     # default settings for add
                                     self.addbutton_options,
                                     # default settings for delete
                                     self.delbutton_options,
                                     # search parameters
                                     self.search_options,
                                     # view parameters
                                     self.viewbutton_options,
                                     )

        self.add_call(nav_call)
