from apps.security.views import *
from django.urls import path

urlpatterns = [
    path('login/', loginPage, name='login'),
    path('register/', registerPage, name='register'),
    path('profile/', ProfilePage.as_view(), name='profile'),
    path('password_reset/', PasswordReset.as_view(), name='password_reset'),
    path('logout/', logoutUser, name='logout'),
    path('error_403/', Error403.as_view(), name='error_403'),
    path('view_audit/', ViewAudit.as_view(), name='view_audit'),
]
