from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import RegistrationForm, ProfileForm ,LoginForm
from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users
import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserProfileSerializer, UserSerializer
from django.shortcuts import get_object_or_404



def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Saves the new user to the database
            user = form.cleaned_data.get('username')
            messages.success(request,'acount was created successfully' )
            return redirect('login_view')  # Redirect to a success page or URL
    else:
        form = RegistrationForm()

    return render(request, 'myApp/register.html', {'form': form})

@api_view(['POST'])
def register_api(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Optionally create UserProfile if needed
        UserProfile.objects.create(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Redirect to profile after login
        else:
            messages.info(request, 'Username OR Password is incorrect')

    return render(request, 'myApp/login.html')

@api_view(['POST'])
def api_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.data)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            user_profile = UserProfile.objects.get(user=user)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def profile_view(request):
    user = request.user  # Get the logged-in user object
    try:
        profile = user.userprofile  # Access the related UserProfile instance
    except UserProfile.DoesNotExist:
        profile = None
        
    if request.method == 'GET':
        form = ProfileForm(request.GET, instance=profile)
        if form.is_valid():
            if profile:
                form.save()
            else:
                # Create a new UserProfile instance linked to the user
                new_profile = form.save(commit=False)
                new_profile.user = user
                new_profile.save()
            return redirect('profile')  # Redirect to profile after updating
    else:
        form = ProfileForm(instance=profile)

    context = {'form': form}
    return render(request, 'myApp/profile.html', context)


@login_required(login_url='login')
@api_view(['GET', 'PUT'])
def api_profile_view(request):
    user = request.user
    try:
        profile = UserProfile.objects.all()  #get(user=user)
    except UserProfile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserProfileSerializer(profile, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProfileForm(request.data, instance=profile)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




def logout_view(request):
    logout(request)
    return redirect('login_view')  # Redirect to login after logout
    return render(request, 'myApp/logout.html')


@api_view(['POST'])
def api_logout_view(request):
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)





















# @api_view(['POST'])
# def api_login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.data)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             user_profile = UserProfile.objects.get(user=user)
#             serializer = UserProfileSerializer(user_profile)
#             return Response(serializer.data)
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)




# @api_view(['GET', 'PUT'])
# def profile_api(request):
#     user = request.user  # Assuming authentication is handled properly
#     profile = get_object_or_404(UserProfile, user=user)

#     if request.method == 'GET':
#         serializer = UserProfileSerializer(profile)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = UserProfileSerializer(profile, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def api_logout_view(request):
#     logout(request)
#     return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)














