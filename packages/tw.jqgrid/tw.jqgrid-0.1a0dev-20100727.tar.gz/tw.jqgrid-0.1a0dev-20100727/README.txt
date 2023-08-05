
tw.jqgrid documentation
=======================


tw.jqmultiselect is a tosca widget wrapper around jquery grid plugin
 which can be found here :

`http://www.trirand.com/blog/`_

the version released with this package is 3.7.2

in the view controller ::

    from tw.jqgrid import JqGrid
    colNames = ['ID','Title', 'Synopsis']
    colModel = [
                {'name':'id', 'index':'id', 'width':20, 'align':'right'},
                {'name':'title', 'index':'title','width':100, 'align':'left'},
                {'name':'synopsis', 'index':'synopsis','width':580, 'align':'left', 'sortable':False},
               ]
    search_options = {
          "caption": "Search...",
          "Find": "Find",
          "Reset": "Reset",
          "sopt" : ['cn', 'bw'],
          "closeOnEscape":True,
    }

    navbuttons_options = {
                          "view":False,
                          "edit": False,
                          "add": False,
                          "del": False,
                          "search":True,
                          "refresh":True,
                          }

    grid_local = JqGrid(id='movie_list', url='fetch', caption='Movies',
                colNames=colNames, colModel=colModel,
                rowList=[5,10], rowNum=5,
                sortname='title',
                viewrecords=True,
                autowidth=True,
                shrinkToFit=True,
                search_options = search_options,
                navbuttons_options = navbuttons_options,
    )


    class MoviesController(BaseRestController):

        @expose('project.templates.movies.get_all')
        def get_all(self):
            pylons.c.grid = grid_local
            return dict(page='all movies')

in the template::

    ${tmpl_context.grid()}

now to feed data we need a controller::

    @expose('json')
    def fetch(self, page=1, rows=10, sidx=1, sord='asc', _search='false',\
              searchOper=u'', searchField=u'', searchString=u'', **kwargs):
        offset = (int(page)-1) * int(rows)
        q = Movie.query
        search_bool = eval(_search.capitalize())
        if (search_bool):
            field = str(searchField)
            field_attr = Movie.__getattribute__(Movie, field)
            if searchOper == u'cn':
                q = medias_q.filter(field_attr.like(u'%%%s%%' % searchString))
            if searchOper == u'bw':
                q = q.filter(field_attr.like(u'%s%%' % searchString))

        result_count = medias_q.count()
        total = 1 + result_count / int(rows)
        column = getattr(Movie.table.c, sidx)
        movies = q.order_by(getattr(column,sord)()).offset(offset).limit(rows)
        rows = [{'id'  : movie.id,
                 'cell': [movie.id,  '<a href="/medias/%s/">%s</a>' % (movie.id, movie.title),
                          movie.synopsis]} for movie in movies]
        return dict(page=page, total=total, records=result_count, rows=rows)



.. note:: this is written for an elixir model, adapt to your need