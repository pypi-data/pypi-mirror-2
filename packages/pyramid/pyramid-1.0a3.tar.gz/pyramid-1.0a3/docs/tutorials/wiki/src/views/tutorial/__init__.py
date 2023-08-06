from pyramid.configuration import Configurator
from repoze.zodbconn.finder import PersistentApplicationFinder
from tutorial.models import appmaker

def main(global_config, **settings):
    """ This function returns a WSGI application.
    
    It is usually called by the PasteDeploy framework during 
    ``paster serve``.
    """
    zodb_uri = settings.get('zodb_uri')
    if zodb_uri is None:
        raise ValueError("No 'zodb_uri' in application configuration.")

    finder = PersistentApplicationFinder(zodb_uri, appmaker)
    def get_root(request):
        return finder(request.environ)
    config = Configurator(root_factory=get_root, settings=settings)
    config.begin()
    config.load_zcml('configure.zcml')
    config.end()
    return config.make_wsgi_app()

