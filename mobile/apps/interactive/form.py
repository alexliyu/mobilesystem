#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Created on 2011-8-25

@author: alex
'''
from django import forms
from apps.interactive.models import Interactive_User, Interactive_Info
from django.conf import settings
from datetime import datetime
from random import random
from checkbox.properties import File
from django.http.multipartparser import FILE

class PostForm(forms.ModelForm):
    content = forms.CharField(label=u' 回答', required=False, \
            widget=forms.Textarea(attrs={'cols':'95', 'rows':'14'}))
    attachments = forms.Field(label=u'附件', required=False, \
            widget=forms.SelectMultiple())

    class Meta:
        model = Interactive_User
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.slug = Interactive_Info.objects.get(pk=kwargs.pop('slug', None))
        self.file = kwargs.pop('file', None)
        super(PostForm, self).__init__(*args, **kwargs)
        
    def save_file(self, file):
        filename = datetime.now().strftime('%Y%m%d%H%M%S%f') + '.' + file.name.split('.')[-1:][0]
        filepath = open(settings.UPLOADS_ROOT + '/' + filename, 'wb+')
        for chunk in file.chunks():
            filepath.write(chunk)
        filepath.close()
        return filepath.name
    def save(self):
        content = self.cleaned_data['content']
        file = self.cleaned_data['attachments']
        interactiveuser, create = Interactive_User.objects.get_or_create(interactive_user=self.user, interactive_info=self.slug)
        interactiveuser.content = content
        interactiveuser.upload_file = self.save_file(self.file)
        interactiveuser.save()
        return interactiveuser

