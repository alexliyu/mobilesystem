import logging

from baseutils.views import BaseView
from baseutils.breadcrumbs import *

logger = logging.getLogger("apps.service_status.views")

class IndexView(BaseView):
    """
    View to display the OUCS service status information.
    """

    def get_metadata(self, request):
        return {
            'title': 'Service Status',
            'additional': 'Check whether OUCS and OLIS services are available',
        }

    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb('service_status', None,
                          'Service Status',
                          lazy_reverse('index'))

    def handle_GET(self, request, context):
        services = []
        for provider in self.conf.providers:
            try:
                status = provider.get_status()
            except Exception, e:
                logger.warn("Failed to load service status", exc_info=True)
            else:
                services.append((
                    provider.slug, provider.name,
                    status['lastBuildDate'], status['services'],
                    provider.get_announcements(),
                ))

        
        context['services'] = services

        return self.render(request, context, 'service_status/index')

