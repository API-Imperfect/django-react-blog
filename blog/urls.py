from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]

admin.site.site_header = "Django React Blog Admin"
admin.site.site_title = "Django React Blog Admin Portal"
admin.site.index_title = "Welcome to Blog Portal"
