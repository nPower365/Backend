from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
# from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    # path(
    #     "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    # ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),

    # User management
    # path("users/", include("fidle_backend.authentication.urls", namespace="authentication")),
    # path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # API base url

    # # djoser url
    # re_path(r'^auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),


    path("", include("power_365.authentication.urls",
                     namespace="authentication")),
    path("", include("power_365.notifications.urls",
                     namespace="notifications")),
    path("", include("power_365.core.urls", namespace="core")),
    path("", include("power_365.delivery.urls", namespace="delivery")),
    path("", include("power_365.wallets.urls", namespace="wallets")),



    path("schema/", SpectacularAPIView.as_view(), name="api-schema", ),
    path("docs/", SpectacularSwaggerView.as_view(url_name="api-schema"),
         name="api-docs",),


]


# Websocket URLS

if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]
    except ImportError:
        pass
