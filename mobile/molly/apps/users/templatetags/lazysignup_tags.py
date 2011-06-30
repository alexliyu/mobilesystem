from django.template import Library
from mobile.molly.apps.users.utils import is_lazy_user

register = Library()
is_lazy_user = register.filter(is_lazy_user)
