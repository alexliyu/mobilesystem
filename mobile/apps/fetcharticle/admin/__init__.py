from django.contrib import admin
from lincdm.app.fetchblog.admin.feedadmin import FeedAdmin, FeedsRresultAdmin, TempImagesAdmin
from lincdm.app.fetchblog.models import  FeedList, FeedSet, FeedsResult, TempImages

admin.site.register(FeedList, FeedAdmin)
admin.site.register(FeedSet)
admin.site.register(TempImages, TempImagesAdmin)
admin.site.register(FeedsResult, FeedsRresultAdmin)
