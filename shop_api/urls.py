from django.contrib import admin
from django.urls import path, include
from . import swagger
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/', include('product.urls')),
]
urlpatterns += swagger.urlpatterns