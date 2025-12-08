from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from debug_toolbar.toolbar import debug_toolbar_urls
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


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
    path("template/v1/", include("apps.template.urls", namespace="v1_template")),
    path("product/v1/", include("apps.product.urls", namespace="v1_product")),
    path("auth/v1/", include("apps.authentication.urls")),
    path("cart/v1/", include("apps.cart.urls")),
    # path("docs/v1/", schema.with_ui("swagger",cache_timeout=0), name="swagger"),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path("core/v1/", include("apis.v1.core.urls", namespace="v1_core")),
    
    # swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG :
    from django.conf.urls.static import static 
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

if settings.DEBUG_TOOLBAR:
    urlpatterns += debug_toolbar_urls()
