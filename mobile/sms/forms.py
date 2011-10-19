"""Forms for Zinnia admin"""
from django import forms
from django.db.models import ManyToOneRel
from django.db.models import ManyToManyRel
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

from django.contrib.auth.models import User, Group
from sms.models import sms_list
from entry.admin.widgets import TreeNodeChoiceField
from entry.admin.widgets import MPTTFilteredSelectMultiple
from entry.admin.widgets import MPTTModelMultipleChoiceField



class Sms_listAdminForm(forms.ModelForm):
    """Form for Entry's Admin"""
    sms_users = MPTTModelMultipleChoiceField(
        User.objects.all(), required=False, label=_('User'),
        widget=MPTTFilteredSelectMultiple(_('users'), False,
                                          attrs={'rows': '10'}))
    sms_groups = MPTTModelMultipleChoiceField(
        Group.objects.all(), required=False, label=_('Group'),
        widget=MPTTFilteredSelectMultiple(_('groups'), False,
                                          attrs={'rows': '10'}))

    def __init__(self, *args, **kwargs):
        super(Sms_listAdminForm, self).__init__(*args, **kwargs)
        rel_user = ManyToManyRel(User, 'id')
        rel_group = ManyToManyRel(Group, 'id')
        self.fields['sms_users'].widget = RelatedFieldWidgetWrapper(
            self.fields['sms_users'].widget, rel_user, self.admin_site)
        self.fields['sms_groups'].widget = RelatedFieldWidgetWrapper(
            self.fields['sms_groups'].widget, rel_group, self.admin_site)
        #self.fields['site'].initial = [Site.objects.get_current()]

    class Meta:
        """EntryAdminForm's Meta"""
        model = sms_list
