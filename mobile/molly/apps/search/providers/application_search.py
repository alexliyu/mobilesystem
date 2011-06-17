import logging

from mobile.molly.apps.search.providers import BaseSearchProvider

from mobile.molly.conf import all_apps

logger = logging.getLogger('molly.providers.apps.search.application_search')

class ApplicationSearchProvider(BaseSearchProvider):
    def __init__(self, local_names=None):
        self.local_names = local_names
        self.applications = None
        
    def perform_search(self, request, query, application=None):
        if self.applications == None:
            self.find_applications()
        
        if application:
            if not application in self.applications:
                return []
            apps = [self.applications[application]]
        else:
            apps = self.applications.values()

        results = []
        for app in apps:
            try:
                results += app.perform_search(request, query, application != None)
            except Exception, e:
                logger.exception("Application search provider raised exception: %r", e)

        return results
        
    def find_applications(self):
        self.applications = {}
        for application in all_apps():
            
            if self.local_names and not application in self.local_names:
                continue
            try:
                search_module_name = '%s.search' % application.application_name
                _temp = __import__(search_module_name,
                                   globals(), locals(),
                                   ['ApplicationSearch'], -1)
                if not hasattr(_temp, 'ApplicationSearch'):
                    raise ImportError
            except ImportError:
                continue
            else:
                search_provider = _temp.ApplicationSearch(application)

            self.applications[application.local_name] = search_provider