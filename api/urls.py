from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^users/$', views.UserListView.as_view(), name="users"),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetailView.as_view(), name="user_details"),
    url(r'^users/create/$', views.CreateUserView.as_view(), name="create_user"),
    url(r'^guests/$', views.GuestView.as_view(), name="guests"),
    url(r'^guests/(?P<pk>[0-9]+)/$', views.GuestDetailView.as_view(), name="guest_details"),
    url(r'^guests/permissions/$', views.GuestPermissionView.as_view(), name="guest_permissions"),
    url(r'^guests/permissions/(?P<pk>[0-9]+)/$', views.GuestPermissionDetailView.as_view(), name="guest_permission_detauls")
]

# this allows us to specify data format (json, html) when using URLs. Appends format
# to be used to every URL in pattern
urlpatterns = format_suffix_patterns(urlpatterns)
