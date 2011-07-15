"""Views for entry authors"""
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list

from ..models import Author
from settings import PAGINATION
from .decorators import update_queryset
from .decorators import template_name_for_entry_queryset_filtered
from django.views.decorators.cache import cache_page

author_list = update_queryset(object_list, Author.published.all)

@cache_page(60 * 300)
def author_detail(request, username, page=None, **kwargs):
    """Display the entries of an author"""
    extra_context = kwargs.pop('extra_context', {})

    author = get_object_or_404(Author, username=username)
    if not kwargs.get('template_name'):
        kwargs['template_name'] = template_name_for_entry_queryset_filtered(
            'author', author.username)

    extra_context.update({'author': author})
    kwargs['extra_context'] = extra_context

    return object_list(request, queryset=author.entries_published(),
                       paginate_by=PAGINATION, page=page,
                       **kwargs)
