"""jupyterkz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import path
from fiesta import views
from jupyterkz import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', views.register_form),
    path('register/', views.register_form),
    path('login', views.login_form),
    path('login/', views.login_form),
    path('logout', views.logout_form),
    path('logout/', views.logout_form),
    path('show/custom.css', views.custom_css),
    path('custom.css', views.custom_css),
    path('show/<str:filename>', views.show),
    path('remove/<str:filename>', views.remove),
    path('', views.index),
    path('<str:folder_name>', views.index),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
