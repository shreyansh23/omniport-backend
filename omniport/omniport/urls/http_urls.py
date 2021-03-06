from django.urls import path, include
from django.views.generic import TemplateView

from omniport.admin.site import omnipotence
from omniport.views.csrf import EnsureCsrf
from omniport.views.manifest import Manifest

http_urlpatterns = [
    path('', TemplateView.as_view(template_name='hello.html'), name='hello'),

    # Progressive Web App manifest
    path('manifest/', Manifest.as_view(), name='manifest'),

    # Ensures a CSRF cookie on the client
    path('ensure_csrf/', EnsureCsrf.as_view(), name='ensure_csrf'),

    # Django admin URL dispatcher
    path('omnipotence/', omnipotence.urls),

    # PyPI packages URL dispatcher
    path('tinymce/', include('tinymce.urls')),

    # The almighty swappable kernel
    path('kernel/', include('kernel.http_urls')),

    # Authentication
    path('base_auth/', include('base_auth.http_urls')),
    path('session_auth/', include('session_auth.http_urls')),
    path('token_auth/', include('token_auth.http_urls')),
    path('open_auth/', include('open_auth.http_urls')),

    # Bootstrapping
    path('bootstrap/', include('bootstrap.http_urls')),
]
