from django.urls import path, re_path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('audit', views.AuditViewset)
router.register('contract', views.ContractViewset)


urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.index, name='index')
]