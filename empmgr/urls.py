from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="home.html"), name='home'),

    # Web views
    path('accounts/', include('accounts.urls')),
    path('forms/', include('formbuilder.urls')),
    path('employees/', include('employees.urls')),

    # APIs
    path('api/', include('api.urls')),
]
