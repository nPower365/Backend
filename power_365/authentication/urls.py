from django.urls import re_path, path, include
from power_365.authentication.api import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
app_name = "users"
urlpatterns = [
    # API endpoints
 path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/login/$',
            view=views.CustomTokenObtainPairView.as_view(), name='account_login'),
    path('auth/register/$',
            view=views.RegisterUser.as_view(), name='account_signup'),
    path('auth/account/confirm-email/send/',
            views.EmailConfirmation.as_view(), name='resend_email_confirmation'),
    path('auth/account/confirm-email/',
            views.ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('auth/registration/complete/',
            views.complete_email_verification, name='account_confirm_complete'),
   path('user/update-password',
            view=views.UserViewSet.as_view({'put': 'update_password'})),
    path('auth/password/reset/',
            views.ResetPassword.as_view(), name='password_reset'),
    path(
        'auth/password/reset/confirm/', views.ConfirmPasswordResetView.as_view(), name='password_reset_confirm'),
    path('auth/facebook/',
            views.FacebookLogin.as_view(), name='fb_login'),
    path('auth/google/',
            views.GoogleLogin.as_view(), name='google_login'),
    path("account/update-profile-picture/",
         views.ChangeProfileImage.as_view(), name="change_profile_image"),
    path("account/set-pin", views.SetPinView.as_view(), name="set_pin"),
    path("account/change-pin", views.ChangePinView.as_view(), name="change_pin"),
    path("account/verify-pin", views.VerifyPinView.as_view(), name="verify_pin"),
]
