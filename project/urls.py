from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from store import views
from django.conf.urls.static import static
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path("", include('store.urls')),
    path('api/v1/', include('core.urls')),
    path('', views.homepage, name='homepage'),
    path('product/', views.productpage, name='productpage'),
    path('productdetail/', views.productdetailpage, name='productdetailpage'),
    path('cart/', views.cartpage, name='cartpage'),
    path('account/', views.accountpage, name='accountpage'),
    path('add/', views.addproduct, name='add_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


