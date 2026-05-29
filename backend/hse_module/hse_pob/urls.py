from django.urls import path
from . import views

urlpatterns = [
    # POB Log endpoints
    path('pob/', views.api_pob_log, name='api_pob_log'),
]
