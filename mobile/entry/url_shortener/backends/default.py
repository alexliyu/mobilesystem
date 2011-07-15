"""Default url shortener backend for Lincdm"""
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from settings import PROTOCOL


def backend(entry):
    """Default url shortener backend for Zinnia"""
    return '%s://%s%s' % (PROTOCOL, Site.objects.get_current().domain,
                       reverse('entry_entry_shortlink', args=[entry.pk]))
