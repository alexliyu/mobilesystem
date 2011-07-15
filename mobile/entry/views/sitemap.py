"""Views for entry sitemap"""
from django.views.generic.simple import direct_to_template

from entry.models import Entry
from entry.models import Category


def sitemap(*ka, **kw):
    """Wrapper around the direct to template generic view to
    force the update of the extra context"""
    kw['extra_context'] = {'entries': Entry.published.all(),
                           'categories': Category.tree.all()}
    return direct_to_template(*ka, **kw)
