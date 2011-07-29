#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.csrf.middleware import csrf_exempt

from forum.forms import EditPostForm, NewPostForm, ForumForm
from forum.models import Topic, Forum, Post
import forum.settings as lbf_settings
from utils.views import BaseView
from utils.breadcrumbs import *




class IndexView(BaseView):
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name, None, u'厦门掌上社区', lazy_reverse('index')
        )
        
    def handle_GET(self, request, context):
        template_name = "forum/index"
        if lbf_settings.LAST_TOPIC_NO_INDEX: 
            context['topics'] = Topic.objects.all().order_by('-last_reply_on')[:20]
        return self.render(request, context, template_name)
        
class forum(BaseView):
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context, forum_slug, topic_type='', topic_type2=''):
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index') , u'厦门掌上社区', lazy_reverse('forum_forum', args=[forum_slug, topic_type, topic_type2])
        )
        
    def handle_GET(self, request, context, forum_slug, topic_type='', topic_type2=''):
        template_name = "forum/forum"
    
        forum = get_object_or_404(Forum, slug=forum_slug)
        topics = forum.topic_set.all()
        if topic_type and topic_type != 'good':
            topic_type2 = topic_type
            topic_type = ''
        if topic_type == 'good':
            topics = topics.filter(level__gt=30)
            #topic_type = _("Distillate District")
        if topic_type2:
            topics = topics.filter(topic_type__slug=topic_type2)
        order_by = request.GET.get('order_by', '-last_reply_on')
        topics = topics.order_by('-sticky', order_by).select_related()
        form = ForumForm(request.GET)
        context['form'] = form
        context['forum'] = forum
        context['topics'] = topics 
        context['topic_type'] = topic_type
        context['topic_type2'] = topic_type2 

        return self.render(request, context, template_name)     

class recent(BaseView):
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index') , u'最新话题', lazy_reverse('forum_recent')
        )
        
    def handle_GET(self, request, context):
        template_name = "forum/recent"
        context['topics'] = Topic.objects.all().order_by('-last_reply_on').select_related()
       
        return self.render(request, context, template_name)  


class topic(BaseView):
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context, topic_id):
       
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index') , u'厦门掌上社区', lazy_reverse('forum_topic', topic_id=topic_id)
            
        )
        
    def handle_GET(self, request, context, topic_id):
        template_name = "forum/topic"
    
        topic = get_object_or_404(Topic, id=topic_id)
        topic.num_views += 1
        topic.save()
        posts = topic.posts
        if lbf_settings.STICKY_TOPIC_POST:#sticky topic post
            posts = posts.filter(topic_post=False)
        posts = posts.order_by('created_on').select_related()
        context['topic'] = topic
        context['posts'] = posts
        context['has_replied'] = topic.has_replied(request.user)
        
        return self.render(request, context, template_name) 
      


class post(BaseView):
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context, post_id):
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index') , u'厦门掌上社区', lazy_reverse('forum_post', args=[post_id])
        )
        
    def handle_POST(self, request, context, post_id):
        post = get_object_or_404(Post, id=post_id)
        return self.redirect(post.get_absolute_url_ext())

#def post(request, post_id):
#    post = get_object_or_404(Post, id=post_id)
#    return HttpResponseRedirect(post.get_absolute_url_ext())

class markitup_preview(BaseView):
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index') , u'厦门掌上社区', lazy_reverse('markitup_preview')
        )
    @login_required    
    def handle_GET(self, request, context):
        template_name = "forum/markitup_preview"
    
        context['message'] = request.POST['data']
        
        
        return self.render(request, context, template_name) 
    
#@csrf_exempt
#def markitup_preview(request, template_name="forum/markitup_preview.html"):
#    return render(request, template_name, {'message': request.POST['data']})


class new_post(BaseView):
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context, forum_id=None, topic_id=None, form_class=NewPostForm,):
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index') , u'发布新话题', lazy_reverse('forum_new_topic', args=[forum_id, topic_id, form_class ])
        )
    @login_required
    def handle_GET(self, request, context, forum_id=None, topic_id=None, form_class=NewPostForm,):
        template_name = "forum/post"
    
        qpost = topic = forum = first_post = preview = None
        post_type = _('topic')
        topic_post = True
        if forum_id:
            forum = get_object_or_404(Forum, pk=forum_id)
        if topic_id:
            post_type = _('reply')
            topic_post = False
            topic = get_object_or_404(Topic, pk=topic_id)
            forum = topic.forum
            first_post = topic.posts.order_by('created_on').select_related()[0]
        if request.method == "POST":
            form = form_class(request.POST, user=request.user, forum=forum, topic=topic, \
                    ip=request.META['REMOTE_ADDR'])
            preview = request.POST.get('preview', '')
            if form.is_valid() and request.POST.get('submit', ''):
                post = form.save()
                
                if topic:
                    return self.redirect (post.get_absolute_url_ext())
                else:
                    return self.redirect (reverse("forum:forum_forum", args=[forum.slug]))
        else:
            initial = {}
            qid = request.GET.get('qid', '')
            if qid:
                qpost = get_object_or_404(Post, id=qid)
                initial['message'] = "[quote=%s]%s[/quote]" % (qpost.posted_by.username, qpost.message)
            form = form_class(initial=initial, forum=forum)
        context['forum'] = forum
        context['form'] = form
        context['topic'] = topic
        context['first_post'] = first_post
        context['post_type'] = post_type
        context['preview'] = preview
        context['unpublished_attachments'] = request.user.attachment_set.all().filter(activated=False)
        context['is_new_post'] = True
        context['topic_post'] = topic_post
        context['session_key'] = request.session.session_key
        
        return self.render(request, context, template_name) 
    


class edit_post(BaseView):
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context, post_id, form_class=EditPostForm):
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index') , u'编辑话题', lazy_reverse('forum_new_topic', args=[post_id, form_class])
        )
    @login_required
    def handle_GET(self, request, context, post_id, form_class=EditPostForm):
        template_name = "forum/post" 
        preview = None
        post_type = _('reply')
        edit_post = get_object_or_404(Post, id=post_id)
        if edit_post.topic_post:
            post_type = _('topic')
        if request.method == "POST":
            form = form_class(instance=edit_post, user=request.user, data=request.POST)
            preview = request.POST.get('preview', '')
            if form.is_valid() and request.POST.get('submit', ''):
                edit_post = form.save()
                return HttpResponseRedirect('../')
        else:
            form = form_class(instance=edit_post)
        context['form'] = form
        context['post'] = edit_post
        context['topic'] = edit_post.topic
        context['forum'] = edit_post.topic.forum
        context['post_type'] = post_type
        context['preview'] = preview
        context['unpublished_attachments'] = request.user.attachment_set.all().filter(activated=False)
        context['topic_post'] = edit_post.topic_post
        context['session_key'] = request.session.session_key
        
        return self.render(request, context, template_name) 



class user_topics(BaseView):
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context, user_id):
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index') , u'用户发布的话题', lazy_reverse('forum_user_topics', args=[user_id])
        )
    @login_required   
    def handle_GET(self, request, context, user_id):
        template_name = "forum/user_topics"
    
        view_user = User.objects.get(pk=user_id)
        topics = view_user.topic_set.order_by('-created_on').select_related()
        context['topics'] = topics
        context['view_user'] = view_user
        
        return self.render(request, context, template_name) 

class user_posts(BaseView):
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context, user_id):
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index') , u'用户参与的话题', lazy_reverse('forum_user_posts', args=[user_id])
        )
    @login_required   
    def handle_GET(self, request, context, user_id):
        template_name = "forum/user_posts"
    
        view_user = User.objects.get(pk=user_id)
        posts = view_user.post_set.order_by('-created_on').select_related()
        context['posts'] = posts
        context['view_user'] = view_user
        
        return self.render(request, context, template_name) 
    

#Feed...
#Add Post
#Add Topic
