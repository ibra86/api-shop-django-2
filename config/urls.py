from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from users.views import home_view, HomeView

urlpatterns = [
    # path('', home_view, name='home'),
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
]
