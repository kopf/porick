"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    map.connect('/browse', controller='browse', action='main')
    map.connect('/browse/best', controller='browse', action='best')
    map.connect('/browse/worst', controller='browse', action='worst')
    map.connect('/browse/random', controller='browse', action='random')
    map.connect('/browse/tags', controller='browse', action='tags')
    map.connect('/browse/tags/{tag}', controller='browse', action='tags')
    map.connect('/browse/{ref_id}', controller='browse', action='view_one')

    map.connect('/create', controller='create', action='quote')

    map.connect('/signup', controller='account', action='create')

    map.connect('/api/vote/{direction}/{quote_id}', controller='vote', action='vote')

    map.connect('/', controller='home', action='main')

    map.redirect('/*(url)/', '/{url}', _redirect_code='301 Moved Permanently')

    return map
