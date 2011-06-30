import urllib
from datetime import timedelta

from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from models import Links
from mobile.molly.utils.views import BaseView
from mobile.molly.utils.breadcrumbs import BreadcrumbFactory, Breadcrumb, lazy_reverse


class IndexView(BaseView):
    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name, None, 'Links',
            lazy_reverse('index'))
    
    def handle_GET(self, request, context):
        linkslist=Links.objects.all()
        context['linkslist']=linkslist
        context.update({
           'sent': request.GET.get('sent') == 'true',
           'referer': request.GET.get('referer', ''),
        })
        return self.render(request, context, 'links/index',
                           expires=timedelta(days=7))
    