"""netstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from topikstore.views import *

#генератор путей для запросов
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

'''class MyCustomRouter(routers.SimpleRouter):
    routes = [
        routers.Route(url=r'^{prefix}$',
                mapping={'get': 'list',},
                name='{basename}-list',
                detail=False,
                initkwargs={'suffix': 'List'}),
        routers.Route(url=r'^{prefix}/{lookup}$',
            mapping={'get': 'retrieve',},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'})
    ]'''

#router = routers.SimpleRouter()
#роутер для формирования опреденных запросов по опреденному пути, без обратного слеша
'''router = MyCustomRouter()
router.register(r'category', CategoryViewSet, basename='category')
print(router.urls)'''

urlpatterns = [
    path('admin/', admin.site.urls),

    path('user/', include('user.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('favorites/', include('favorites.urls', namespace = 'favorites')),
    path('', include('topikstore.urls')),

    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #для обновления access-token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        
    path('api/v1/category/', CategoryAPIList.as_view()),
    path('api/v1/category/<slug:cat_slug>/', CategoryAPIUpdate.as_view()),
    path('api/v1/categorydelete/<slug:cat_slug>/', CategoryAPIDestroy.as_view()),

    path('api/v1/product/', ProductAPIList.as_view()),
    path('api/v1/product/<int:product_pk>/', ProductAPIUpdate.as_view()),

    #позволяет проводить авторизацию, аутенфикацию, регистрацию и изменение пользователей
    #аутенфикация по токенам
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)