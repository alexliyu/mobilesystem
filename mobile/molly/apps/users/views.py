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

from mobile.molly.utils.views import BaseView
from mobile.molly.utils.breadcrumbs import *
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from mobile.molly.apps.users.decorators import allow_lazy_user
from mobile.molly.apps.users.exceptions import NotLazyError
from mobile.molly.apps.users.forms import UserCreationForm
from mobile.molly.apps.users.models import LazyUser
from mobile.molly.utils.views import BaseView
from mobile.molly.utils.breadcrumbs import *

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
        return self.convert(request)
    
    
    @allow_lazy_user
    def convert(self, request, form_class=UserCreationForm, redirect_field_name='redirect_to',
                anonymous_redirect=settings.LOGIN_URL):
        """ Convert a temporary user to a real one. Reject users who don't
        appear to be temporary users (ie. they have a usable password)
        """
        redirect_to = 'lazysignup_convert_done'
    
        # If we've got an anonymous user, redirect to login
        if request.user.is_anonymous():
            return HttpResponseRedirect(anonymous_redirect)
    
        if request.method == 'POST':
            redirect_to = request.POST.get(redirect_field_name) or redirect_to
            form = form_class(request.POST, instance=request.user)
            if form.is_valid():
                try:
                    user = LazyUser.objects.convert(form)
                except NotLazyError:
                    # If the user already has a usable password, return a Bad Request to
                    # an Ajax client, or just redirect back for a regular client.
                    if request.is_ajax():
                        return HttpResponseBadRequest(content=_(u"Already converted."))
                    else:
                        return redirect(redirect_to)
    
                # Re-log the user in, as they'll now not be authenticatable with the Lazy
                # backend
                login(request, authenticate(**form.get_credentials()))
    
                # If we're being called via AJAX, then we just return a 200 directly
                # to the client. If not, then we redirect to a confirmation page or
                # to redirect_to, if it's set.
                if request.is_ajax():
                    return HttpResponse()
                else:
                    return redirect(redirect_to)
        else:
            form = form_class()
    
        if request.is_ajax():
            return HttpResponseBadRequest(content=str(form.errors))
        else:
            return direct_to_template(
                request,
                'lazysignup/convert.html',
                { 'form': form,
                  'redirect_to': redirect_to
                },
                )


