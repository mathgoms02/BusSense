from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    AccessViewSet,
    BusRouteViewSet,
    CidViewSet,
    CityViewSet,
    DynamicFormView,
    GroupViewSet,
    ReportsViewSet,
    SearchViewSet,
    UserViewSet,
    VehicleViewSet
)

router = DefaultRouter()
router.register(r'access', AccessViewSet, basename='access')
router.register(r'bus-route', BusRouteViewSet, basename='busroute')
router.register(r'cid', CidViewSet, basename='cid')
router.register(r'city', CityViewSet, basename='city')
router.register(r'group', GroupViewSet, basename='group')
router.register(r'report', ReportsViewSet, basename='report')
router.register(r'search', SearchViewSet, basename='search')
router.register(r'user', UserViewSet, basename='user')
router.register(r'vehicle', VehicleViewSet, basename='vehicle')

urlpatterns = [
    path('', include(router.urls)),
    path('dynamic-form/', DynamicFormView.as_view(), name='dynamic_form'),
]
