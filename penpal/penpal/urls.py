"""
URL configuration for penpal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from .health_check import health_check


# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Penpal API",
        default_version="v1",
        description="API documentation for Penpal Backend",
        terms_of_service="https://www.penpal.com/terms/",
        contact=openapi.Contact(email="support@penpal.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Optional: for SWAGGER_SETTINGS["DEFAULT_INFO"]
api_info = openapi.Info(
    title="Penpal API",
    default_version="v1",
    description="Core API endpoints for Penpal",
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health-check'),
    path('api/swagger/', schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path('api/redoc/', schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path('api/swagger.json/', schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path('api/users/', include("accounts.urls")),
    path('api/documents/', include("document.urls"))
]


