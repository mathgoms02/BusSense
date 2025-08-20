from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    BusRouteViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register(r'bus-route', BusRouteViewSet, basename='busroute')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
