from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404

from utils.views import BaseView
from utils.breadcrumbs import *
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


class IndexView(BaseView):
    def get_metadata(self, request):
        return {
            'title': 'News',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name, None, 'users', lazy_reverse('index')
        )
        
    def handle_GET(self, request, context):
        return '123'
    
    

