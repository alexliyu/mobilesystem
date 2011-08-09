from datetime import datetime, timedelta

from utils.views import BaseView
from utils.breadcrumbs import *

from models import Weather

class IndexView(BaseView):
    def initial_context(self, request):
        try:
            observation = Weather.objects.get(location_id=self.conf.location_id)
        except Weather.DoesNotExist:
            observation = None
        return {
            'observation': observation,
            'forecasts': Weather.objects.filter(location_id=self.conf.location_id, observed_date__gte=datetime.now().date()).order_by('observed_date'),
        }

    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            'weather',
            None,
            'Weather',
            lazy_reverse('index'),
        )

    def handle_GET(self, request, context):
        return self.render(request, context, 'weather/index',
                           expires=timedelta(minutes=10))
