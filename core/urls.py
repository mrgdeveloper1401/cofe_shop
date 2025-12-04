from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from debug_toolbar.toolbar import debug_toolbar_urls


schema = get_schema_view(
    info=openapi.Info(
        title="cofe",
        default_version="1.0.0",
        license=openapi.License(name="MIT")
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("template/",include("apps.template.urls")),
    path("product/",include("apps.product.urls")),
    path("auth/",include("apps.authentication.urls")),
    path("cart/",include("apps.cart.urls")),
    path("",schema.with_ui("swagger",cache_timeout=0),name="swagger"),
]

if settings.DEBUG :
    from django.conf.urls.static import static 
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

if settings.DEBUG_TOOLBAR:
    urlpatterns += debug_toolbar_urls()
