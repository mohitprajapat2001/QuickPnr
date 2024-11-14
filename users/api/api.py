from rest_framework import mixins, viewsets, permissions, views, status
from rest_framework.response import Response
from utils.utils import get_model
from users.api.serializers import (
    RegistrationSerializer,
    LoginSerializer,
    UserSerializer,
    EmailUpdateSerializer,
    EmailVerifySerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    GoogleAuthenticationLogin,
    GoogleAuthenticationSignup,
)
from users.tasks import (
    generate_otp,
    reset_password_otp,
    reset_password_done,
)
from utils.utils import AuthService
from rest_framework.generics import UpdateAPIView, CreateAPIView
from users.constants import ResponseMessages

User = get_model("users", "User")


class RegistrationApiView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """User Registeration API View"""

    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """Register New User"""
        instance = super().create(request, *args, **kwargs)
        return instance


class LoginApiView(views.APIView):
    """User Login API View"""

    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(
            data=self.request.data, context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            AuthService().get_auth_tokens_for_user(serializer.validated_data),
            status=status.HTTP_200_OK,
        )


class UserProfileView(views.APIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        """Return User Object"""
        return self.request.user

    def get(self, *args, **kwargs):
        """Return User Profile"""
        instance = self.get_object(*args, **kwargs)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """Update User Profile"""
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class EmailUpdateView(views.APIView):
    """User Email Update View"""

    serializer_class = EmailUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, *args, **kwargs):
        """Update User Email"""
        serializer = self.serializer_class(
            self.request.user, data=self.request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmailVerifyView(UpdateAPIView):
    """Email Verification API View"""

    serializer_class = EmailVerifySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Send Email Verification OTP"""
        generate_otp.delay(request.user.id)
        try:
            return Response(
                {"message": ResponseMessages.OTP_GENERATED}, status=status.HTTP_200_OK
            )
        except Exception as err:
            raise Response(
                {
                    "message": ResponseMessages.FAILED_TO_GENERATE_OTP.format(err=err),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request, *args, **kwargs):
        """Verify User Email"""
        serializer = self.serializer_class(
            instance=request.user, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": ResponseMessages.EMAIL_VERIFIED},
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(UpdateAPIView):
    """Change Password API View"""

    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """Change User Password"""
        serializer = self.serializer_class(
            instance=request.user, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": ResponseMessages.PASSWORD_CHANGED_DONE},
            status=status.HTTP_200_OK,
        )


class ForgotPasswordView(UpdateAPIView):
    """Forgot Password API View"""

    serializer_class = ForgotPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """Forgot Password Send Password Reset OTP to User"""
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        reset_password_otp.delay(User.objects.get(email=request.data["email"]).id)
        return Response(
            {"message": ResponseMessages.PASSWORD_RESET_OTP_GENERATED},
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        """Update User Password After Verification"""
        user = User.objects.get(email=request.data["email"])
        serializer = self.serializer_class(
            instance=user, data=request.data, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        reset_password_done.delay(user.id)
        return Response(
            {"message": ResponseMessages.PASSWORD_RESET_DONE},
            status=status.HTTP_200_OK,
        )


class GoogleSignupView(CreateAPIView):
    """Google Signup API View"""

    permission_classes = [permissions.AllowAny]
    serializer_class = GoogleAuthenticationSignup

    def post(self, request, *args, **kwargs):
        """Create New User"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GoogleLoginView(CreateAPIView):
    """Google Login API View"""

    permission_classes = [permissions.AllowAny]
    serializer_class = GoogleAuthenticationLogin

    def post(self, request, *args, **kwargs):
        """Google Login"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            return Response(
                AuthService().get_auth_tokens_for_user(
                    User.objects.get(google_id=serializer.data["google_id"])
                ),
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"message": ResponseMessages.USER_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )
