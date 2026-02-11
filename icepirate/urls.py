from django.urls import include, path, re_path
from django.views.generic.base import RedirectView

from message.views import short_url_redirect
from core import views as core_views

from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('allauth.urls')),
    path('login/', RedirectView.as_view(url='/accounts/login/')),
    path('user-management/', core_views.user_management, name='user_management'),

    path('', include('member.urls')),

    path('message/', include('message.urls')),
    re_path(r'^r/(?P<code>[^/]+)/?$', short_url_redirect),

    path('', RedirectView.as_view(url='/accounts/login/')),
]
