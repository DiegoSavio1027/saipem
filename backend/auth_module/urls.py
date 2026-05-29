from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import login_view, me_view, logout_view, CustomTokenObtainPairView, dev_quick_login_accounts

urlpatterns = [
    # JWT Token endpoints
    path('login/', login_view, name='auth_login'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User info endpoints
    path('me/', me_view, name='auth_me'),
    path('logout/', logout_view, name='auth_logout'),

    # Development endpoints
    path('dev/quick-login-accounts/', dev_quick_login_accounts, name='dev_quick_login_accounts'),
]
