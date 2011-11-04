"""Forms for admin"""
from django import forms
from django.db.models import ManyToOneRel
from django.db.models import ManyToManyRel
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

from userena.models import UserProfile
from apps.lottery.models import lottery
from apps.entry.admin.widgets import TreeNodeChoiceField
from apps.entry.admin.widgets import MPTTFilteredSelectMultiple
from apps.entry.admin.widgets import MPTTModelMultipleChoiceField



class Lottery_listAdminForm(forms.ModelForm):
    """Form for Entry's Admin"""
    UserProfile = MPTTModelMultipleChoiceField(
        UserProfile.objects.all(), required=False, label=_('User'),
        widget=MPTTFilteredSelectMultiple(_('users'), False,
                                          attrs={'rows': '10'}))

    def __init__(self, *args, **kwargs):
        super(Lottery_listAdminForm, self).__init__(*args, **kwargs)
        rel_user = ManyToManyRel(UserProfile, 'id')
        self.fields['UserProfile'].widget = RelatedFieldWidgetWrapper(
            self.fields['UserProfile'].widget, rel_user, self.admin_site)
       

    class Meta:
        """EntryAdminForm's Meta"""
        model = lottery
