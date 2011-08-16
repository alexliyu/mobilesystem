from django.contrib import admin
from apps.fetcharticle.admin.feedadmin import FeedAdmin, FeedsRresultAdmin, TempImagesAdmin
from apps.fetcharticle.models import  FeedList, FeedSet, FeedsResult, TempImages

admin.site.register(FeedList, FeedAdmin)
admin.site.register(FeedSet)
admin.site.register(TempImages, TempImagesAdmin)
admin.site.register(FeedsResult, FeedsRresultAdmin)
