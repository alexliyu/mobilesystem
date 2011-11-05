from django.core.management.base import BaseCommand

from userena.models import UserProfile 
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Init UserProfile"
    
    def handle(self, **options):
        users = User.objects.all()
        for o in users:
            #LBForumUserProfile.objects.create(user=instance)
            try:
                o.UserProfile
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=o)
