from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    BusRouteViewSet,
    UserViewSet,
)

from core.views import DynamicFormView, select_form_view

router = DefaultRouter()
router.register(r'bus-route', BusRouteViewSet, basename='busroute')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),

    path('forms/', select_form_view, name='select_form'),
    path('form/<str:model_name>/', DynamicFormView.as_view(), name='dynamic_form'),
]