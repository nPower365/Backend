from dateutil.relativedelta import relativedelta
from django.db.models import Count
from itertools import chain
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from lib2to3.pgen2.parse import ParseError
from power_365.authentication import helpers
from power_365.authentication.models import *
from power_365.authentication.api.serializers import *
from rest_framework import generics
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.decorators import action, api_view
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db.models import Q, Sum
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from django.conf import settings
from djoser.serializers import PasswordResetConfirmRetypeSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    search_fields = ['first_name', 'last_name', 'username']
    filterset_fields = ['first_name', 'last_name']
    # def get_queryset(self, *args, **kwargs):
    #     # assert isinstance(self.request.user.id, int)
    #     return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(methods=['put'], detail=True)
    def update_password(self, request):
        self.serializer_class = serializers.UpdatePasswordSerializer
        serializer = serializers.UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'detail': 'Old password does not match, if you have forgotten your password, please use reset instead.'},
                                status=status.HTTP_400_BAD_REQUEST)
            elif not serializer.data.get('password') == serializer.data.get('confirm_password'):
                return Response('password and confirm password do not match', status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get('password'))
            user.save()
            return Response({'status': 'password updated'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class TokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = None

    www_authenticate_realm = 'api'

    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        email = serializer.validated_data.get('user').get('email')
        user = User.objects.get(email=email)
        if user:
            if not user.email_verified_at:
                self.request.user = user
                settings.EMAIL.activation(
                    self.request, {'request': request}).send(to=[user.email])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = CustomTokenObtainPairSerializer


class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):  # get the referrer code and credit the referrer
        referrer_code = self.request.data.get('referrer_code')
        referrer = None

        if referrer_code:
            referrer = models.User.objects.filter(
                referral_code=referrer_code).first()
        serializer.save()
        user = models.User.objects.get(email=serializer.data.get('email'))

        if user and referrer:
            # update the user
            user.referrer_id = referrer
            user.save()


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class EmailConfirmation(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.email_verified_at:
            return Response({'detail': 'Email already verified'}, status=status.HTTP_201_CREATED)

        settings.EMAIL.activation(
            self.request, {'request': request}).send(to=[request.user.email])
        return Response({'detail': 'Email confirmation sent'}, status=status.HTTP_201_CREATED)


class ConfirmEmailView(generics.CreateAPIView):
    serializer_class = CustomActivationSerializer
    token_generator = default_token_generator
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        if user:
            # get use with the email address and set it verified data
            user.email_verified_at = timezone.now()
            user.save()

            refresh = RefreshToken.for_user(user)

            return Response({'detail': _('ok'),
                             'refresh': str(refresh),
                             'access': str(refresh.access_token),
                             'user': serializers.UserCompleteSerializer(user).data
                             }, status=status.HTTP_200_OK)

        raise ParseError(detail="Could not verify token",
                         code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ResetPassword(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        user = models.User.objects.filter(email=email).first()
        if not user:
            return Response({'detail': f'Password reset mail has been sent to {email}.'}, status=status.HTTP_200_OK)
        context = {"user": user}
        to = [email]
        settings.EMAIL.password_reset(self.request, context).send(to)
        return Response({'detail': f'Password reset mail has been sent  to {email}'}, status=status.HTTP_201_CREATED)


class ConfirmPasswordResetView(generics.CreateAPIView):
    serializer_class = PasswordResetConfirmRetypeSerializer
    token_generator = default_token_generator
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        password = serializer.validated_data.get('new_password')
        if user:
            # get use with the email address and set it verified data
            user.set_password(password)
            user.save()

            refresh = RefreshToken.for_user(user)

            return Response({'detail': _('ok'),
                             'refresh': str(refresh),
                             'access': str(refresh.access_token),
                             'user': serializers.UserCompleteSerializer(user).data
                             }, status=status.HTTP_200_OK)

        raise ParseError(detail="Could not verify token",
                         code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view()
def complete_email_verification(request):
    return Response("Email account is activated")


@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)


class FacebookLogin(APIView):
    pass


class GoogleLogin(APIView):
    pass


class ChangeProfileImage(generics.CreateAPIView):
    serializer_class = ProfileImageSerializer

    def create(self, request, *args, **kwargs):
        ProfileImage.objects.filter(
            user=self.request.user).update(is_current=False)
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        return ProfileImage.objects.filter(user=self.request.user)

    def get_serializer_context(self):

        return {'user': self.request.user,
                'media': self.request.FILES.get('media')}

class SetPinView(generics.CreateAPIView):
    serializer_class = SetPinSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        pin = request.data.get('pin')
        pin_confirmation = request.data.get('pin_confirmation')
        if not pin:
            return Response({"error": "Pin is required."}, status=400)
        if not pin_confirmation:
            return Response({"error": "Pin confirmation is required."}, status=400)

        if pin != pin_confirmation:
            return Response({"error": "Pin and pin_confirmation do not match."}, status=400)

        # Check if pin is already set
        pin_exist = Pin.objects.filter(user=user, active=True).exists()
        if pin_exist:
            return Response({"error": "Pin is already set."}, status=400)
        new_pin = Pin.objects.create(user=user, code=make_password(pin))
        if not new_pin:
            return Response({"error": "Failed to set pin."}, status=400)
        return Response({"message": "Pin set successfully."})

    def get_queryset(self):
        return Pin.objects.filter(user=self.request.user)


class ChangePinView(generics.CreateAPIView):
    serializer_class = SetPinSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        old_pin = request.data.get('old_pin')
        pin = request.data.get('pin')
        pin_confirmation = request.data.get('pin_confirmation')

        if not old_pin:
            return Response({"error": "Old pin is required."}, status=400)

        if not pin:
            return Response({"error": "Pin is required."}, status=400)
        if not pin_confirmation:
            return Response({"error": "Pin confirmation is required."}, status=400)

        if pin != pin_confirmation:
            return Response({"error": "Pin and pin_confirmation do not match."}, status=400)

        active_pin = Pin.objects.filter(user=user, active=True).first()
        if not active_pin:
            return Response({"error": "Please use set pin instead."}, status=400)
        if not check_password(old_pin, active_pin.code):
            return Response({"error": "Old pin is incorrect."}, status=400)
        # lets check if user has used the pin before in last 10
        last_10_pins = Pin.objects.filter(
            user=user).order_by('-date_created')[:10]
        for p_pin in last_10_pins:
            if check_password(pin, p_pin.code):
                return Response({"error": "Pin has been used before."}, status=400)

        new_pin = Pin.objects.create(user=user, code=make_password(pin))
        if not new_pin:
            return Response({"error": "Failed to change pin."}, status=400)
        active_pin.active = False
        active_pin.save()
        return Response({"message": "Pin changed successfully."})


class VerifyPinView(generics.CreateAPIView):
    serializer_class = VerifyPinSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        pin = request.data.get('pin')
        if not pin:
            return Response({"error": "Pin is required."}, status=400)

        active_pin = Pin.objects.filter(user=user, active=True).first()
        if not active_pin:
            return Response({"error": "No pin set up."}, status=400)

        if not check_password(pin, active_pin.code):
            return Response({"error": "Pin is incorrect."}, status=400)

        return Response({"message": "Pin verified successfully."})
