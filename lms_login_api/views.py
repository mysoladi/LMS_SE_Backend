from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import CustomUser  # Import your custom user model
from lms_login_api.serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from lms_login_api.serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from utils.settings import *
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import secrets
from django.core.mail.backends.smtp import EmailBackend


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def perform_create(self, serializer):
        # Encrypt the password before saving the user
        validated_data = serializer.validated_data
        user = CustomUser.objects.create_user(validated_data['email'], validated_data['password'], validated_data['first_name'], validated_data['last_name'], validated_data['sec_answer'], validated_data['username'], validated_data['user_role'])
        serializer.instance = user

class CreateUserView(APIView):
    permission_classes = [AllowAny]  # Allow any user to create a new user

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Hash the password before saving the user
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [AllowAny]  # Allow any user to login

    def post(self, request):
        username = request.data.get('username')  # Assuming 'email' is used for login
        password = request.data.get('password')

        # Authenticate user using custom user model
        
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': "user logged in"
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserInformation(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication to access this API

    def get(self, request, user_id):
        # Retrieve the user based on the user_id from the URL
        user = get_object_or_404(CustomUser, id=user_id)

        # Assuming you have serializer for your CustomUser model to serialize the user data
        serializer = UserSerializer(user)  # Replace CustomUserSerializer with your actual serializer

        return Response(serializer.data)

class PasswordRecoveryView(APIView):
    permission_classes = [AllowAny]  # Allow any user to recover password

    def post(self, request):
        if request.method == 'POST':
            email = request.data.get('email')
            security_answer = request.data.get('security_answer')

            # Query the user by email
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'User with this email does not exist'}, status=404)

            # Check if security answer matches
            if user.sec_answer == security_answer:
                # Generate reset password URL with email as query parameter
                # reset_url = reverse('confirm-password-change') + f"?email={email}"

                token = secrets.token_urlsafe(32)


                reset_url = f"http://localhost:3002/resetpassword?email={email}&token={token}"

                # Generate reset password URL (replace 'reset_password_url' with your actual URL)
                # reset_url = f"http://localhost:3002/resetpassword"

                # Return reset URL in the response
                return JsonResponse({'reset_url': reset_url})

            # If security answer doesn't match, return an error
            return JsonResponse({'error': 'Invalid security answer'}, status=400)

        # If POST method is not used, return an error
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

class EmailPasswordRecoveryView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if request.method == 'POST':
            email = request.data.get('email')

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'User with this email does not exist'}, status=404)

            # Generate token here
            token = secrets.token_urlsafe(32)

            # Send email
            subject = "Password Reset"
            message = f"Click the link below to reset your password:\n{settings.FRONTEND_URL}/resetpassword?email={email}&token={token}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return JsonResponse({'message': 'Password reset email sent successfully'})
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


class ChangePasswordView(APIView):
    permission_classes = [AllowAny]

    def put(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email:
            return Response({'error': 'Email not provided'}, status=400)

        if not password:
            return Response({'error': 'Password not provided'}, status=400)

        try:
            # Query the user by email
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=404)

        # Update the user's password
        user.set_password(password)
        user.save()

        return Response({'message': "reset successful"})
