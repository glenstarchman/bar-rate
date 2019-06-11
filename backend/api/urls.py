from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .views import BarViewSet, BartenderViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'bar', BarViewSet)
router.register(r'bartender', BartenderViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url('', include(router.urls)),
]
