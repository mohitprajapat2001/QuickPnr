"""Users Urls"""

from users.api.api import (
    RegistrationApiView,
    LoginApiView,
    UserProfileView,
    EmailUpdateView,
    EmailVerifyView,
    ChangePasswordView,
    ForgotPasswordView,
    GoogleLoginView,
    GoogleSignupView,
)
from django.urls import path, include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()


router.register("register", RegistrationApiView, basename="register")
urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginApiView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("update-email/", EmailUpdateView.as_view(), name="update-email"),
    path("verify-email/", EmailVerifyView.as_view(), name="verify-email"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("auth-google-signup/", GoogleSignupView.as_view(), name="auth-google-signup"),
    path("auth-google-login/", GoogleLoginView.as_view(), name="auth-google-login"),
]
