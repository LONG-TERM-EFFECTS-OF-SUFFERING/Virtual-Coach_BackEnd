from django.contrib import admin
from django.urls import path,include,re_path
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('routines/', include('routines.urls')),
]


#This line has to be uncommented for production
#urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]

#This line has to be deleted in production
urlpatterns += staticfiles_urlpatterns()