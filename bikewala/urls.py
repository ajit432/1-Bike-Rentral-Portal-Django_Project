"""
URL configuration for bikewala project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('customer.urls')),
#     path('renter/', include('renter.urls'))
# ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('customer.urls')),
    path('renter/', include('renter.urls'))
]

# This is the crucial part for serving media files in production (with DEBUG=False)
# Add this line at the end of the file.
if settings.DEBUG is False: #if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# If you want it to also work in development, you can use this instead:
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
