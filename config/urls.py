from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import settings

static_patterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
                  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = [
                  path('', include('app.urls')),
                  path('admin/', admin.site.urls),
                  path('users/', include('users.urls')),
                  path('users/', include('django.contrib.auth.urls')),
              ] + static_patterns
