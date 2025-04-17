from django.urls import path, include
from rest_framework.routers import DefaultRouter
from emtu_api.core.views import (
    AccessViewSet,
    BusRouteViewSet,
    CidViewSet,
    CityViewSet,
    GroupViewSet,
    ReportsViewSet,
    SearchViewSet,
    UserViewSet,
    VehicleViewSet
)

router = DefaultRouter()
router.register(r'access', AccessViewSet)
router.register(r'bus-route', BusRouteViewSet)
router.register(r'cid', CidViewSet)
router.register(r'city', CityViewSet)
router.register(r'group', GroupViewSet)
router.register(r'report', ReportsViewSet)
router.register(r'search', SearchViewSet)
router.register(r'user', UserViewSet)
router.register(r'vehicle', VehicleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
