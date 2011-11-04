#-*- coding:utf-8 -*-
"""
这是项目的home应用模块的主视图.

创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
"""
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template import loader, Context, RequestContext
from django import forms
from django.shortcuts import render_to_response

from baseutils.views import BaseView
from baseutils.breadcrumbs import *
from favourites import get_favourites
from wurfl import device_parents
import conf
from models import UserMessage
from forms import UserMessageFormSet
from sms.models import sms_entry

class IndexView(BaseView):
    """
    Renders the portal home page
    """

    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(self.conf.local_name,
                          None,
                          '主页',
                          lazy_reverse('index'))
    def handle_GET(self, request, context):
        # Check whether the referer header is from the same host as the server
        # is responding as
        try:
            referer_host = request.META.get('HTTP_REFERER', '').split('/')[2]
            internal_referer = referer_host == request.META.get('HTTP_HOST')
        except IndexError:
            internal_referer = False

        # Redirects if the user is a desktop browser who hasn't been referred
        # from this site. Also extra checks for preview mode and DEBUG.
        if ("generic_web_browser" in device_parents[request.device.devid]
            and not request.session.get('home:desktop_shown', False)
            and not request.GET.get('preview') == 'true'
            and not internal_referer
            and not settings.DEBUG
            and conf.has_app('apps.desktop')
            and request.REQUEST.get('format') is None):
            return self.redirect(reverse('desktop:index'), request)
        
        # Add any one-off messages to be shown to this user
        messages = []
        
        if not request.session.get('home:opera_mini_warning', False) \
          and request.browser.mobile_browser == u'Opera Mini':
            messages.append("""Please note that the "Mobile View" on Opera Mini
                            does not display this site correctly. To ensure
                            correct operation of this site, ensure "Mobile View"
                            is set to Off in Opera settings""")
            request.session['home:opera_mini_warning'] = True

        applications = [{
            'application_name': app.application_name,
            'local_name': app.local_name,
            'title': app.title,
            'url': reverse('%s:index' % app.local_name) \
                    if app.has_urlconf else None,
            'display_to_user': app.display_to_user,
        } for app in conf.all_apps()]

        # Add accesskeys to the first 9 apps to be displayed to the user
        for i, app in enumerate(
                [app for app in applications if app['display_to_user']][:9]
            ):
            app['accesskey'] = i + 1

        context = {
            'applications': applications,
            'hide_feedback_link': True,
            'is_christmas': datetime.now().month == 12,
            'messages': messages,
            'xiaofang':sms_entry().get_random(),
           
        }
        return self.render(request, context, 'home/index',
                           expires=timedelta(minutes=10))

    def get_metadata(self, request):
        return {
            'exclude_from_search': True,
        }

    def handle_POST(self, request, context):
        no_desktop_about = request.POST.get('no_desktop_about')
        if no_desktop_about == 'true':
            request.session['home:desktop_about_shown'] = True
        elif no_desktop_about == 'false':
            request.session['home:desktop_about_shown'] = False

        return self.redirect(reverse('home:index'), request)

class StaticDetailView(BaseView):
    @BreadcrumbFactory
    def breadcrumb(self, request, context, title, template):
        return Breadcrumb(
            self.conf.local_name, None, title,
            lazy_reverse('static', args=[template])
        )

    def handle_GET(self, request, context, title, template):
        t = loader.get_template('static/%s.html' % template)

        context.update({
            'title': title,
            'content': t.render(Context()),
        })
        return self.render(request, context, 'home/static_detail',
                           expires=timedelta(days=365))

class UserMessageView(BaseView):
    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name, None, 'View messages from the developers',
            lazy_reverse('messages')
        )

    def initial_context(self, request):
        try:
            formset = UserMessageFormSet(
                request.POST or None,
                queryset=UserMessage.objects.filter(
                    session_key=request.session.session_key
                )
            )
        except forms.ValidationError:
            formset = UserMessageFormSet(
                None,
                queryset=UserMessage.objects.filter(
                    session_key=request.session.session_key
                )
            )
        return {
            'formset': formset,
        }

    def handle_GET(self, request, context):
        messages = UserMessage.objects.filter(
                session_key=request.session.session_key
            )
        messages.update(read=True)
        return self.render(request, context, 'home/messages')

    def handle_POST(self, request, context):
        if context['formset'].is_valid():
            context['formset'].save()

        return self.redirect(reverse('home:messages'), request)
