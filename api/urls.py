from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^users/$', views.UserList.as_view(), name="users"),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name="user_details"),
    url(r'^users/create/$', views.CreateUser.as_view(), name="create_user"),
]

# this allows us to specify data format (json, html) when using URLs. Appends format
# to be used to every URL in pattern
urlpatterns = format_suffix_patterns(urlpatterns)
