import os
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.static import serve

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.join(BASE_DIR, 'site')

urlpatterns = [
                  path('', include('ads.urls')),
                  path('admin/', admin.site.urls),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('oauth/', include('social_django.urls', namespace='social')),
                  path('profile/', include('core.urls')),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('accounts/', include('django_registration.backends.one_step.urls')),
                  path('favicon.ico', serve, {
                      'path': 'favicon.ico',
                      'document_root': os.path.join(BASE_DIR, 'core/static'),
                  }),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


social_login = 'registration/login_social.html'
urlpatterns.insert(0,
                   path('accounts/login/', auth_views.LoginView.as_view(template_name=social_login))
                   )
