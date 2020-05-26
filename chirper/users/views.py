import json
import requests

from django.shortcuts import render, redirect

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from requests_oauthlib import OAuth2Session

from django.contrib import messages

from .forms import UserUpdateForm, ProfileUpdateForm


# Create your views here.

client_id = r'6p7HJlFCD8cnBNBEdgMsdULS5ph0jserw1xvWfxX'
client_secret = r'E1e79KebxzAp0LBEtxcUg32b0qFP9Ap9Dxqkac6Qhci5AwXFhSfrbe7MtmGJUh6DDgxivJpGgFYNQgusfvoSraDAnsq3NnEET5DmxgfBBvvuYc2bwDq6KpeKIDQqFtwz'
redirect_uri = 'http://localhost:8000/callback/'
token_url = 'https://ion.tjhsst.edu/oauth/authorize/'
scope=["read"]

authorized_users=["2023rumareti", "Your ION_USERNAME"]
#                 Hey that's me

# Yes, I realize that this is slightly convoluted, but I couldn't get social-oauth to work,
# and OAuth2Session kept giving me nasty errors, so what I am doing below is pretty much manual OAuth

def login(request):

    # First, we get a authorization url with OAuth2Session and redirect the user to the Ion authorization page
    oauth = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = oauth.authorization_url("https://ion.tjhsst.edu/oauth/authorize/")

    return render(request,"users/login.html", {"authorization_url": authorization_url})

def callback (request):
        if request.method == "GET":
            code = request.GET.get('code')
            state = request.GET.get("state")
            # Then if we get a response from Ion with the authorization code
            if code is not None and state is not None:

                # We send it back to fetch the acess_token
                payload = {'grant_type':'authorization_code','code': code,'redirect_uri':redirect_uri,'client_id':client_id,'client_secret':client_secret, 'csrfmiddlewaretoken': state}
                token = requests.post("https://ion.tjhsst.edu/oauth/token/", data=payload).json()
                headers = {'Authorization': f"Bearer {token['access_token']}"}

                # And finally get the user's profile!
                profile = requests.get("https://ion.tjhsst.edu/api/profile", headers=headers).json()
                username = profile['ion_username']
                email = profile['tj_email']
                first_name = profile['first_name']
                last_name = profile['last_name']

                # First we need to check if this user is authoized to post, as defined in the global array above
                if username in authorized_users:
                    # Then we check if this user exists in the system, we log them in, and if not we create a user for them
                    user = authenticate(request, username=username, password=username)
                    if user is not None:
                        auth_login(request, user)
                        messages.success(request, f"Welcome back {first_name}!")
                    else:
                        user = User.objects.create_user(username=username, email=email, password=username, first_name=first_name, last_name=last_name)
                        user.save()
                        auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        messages.success(request, f"Welcome to Chirper, {first_name}, we hope you enjoy your stay!")
                    return redirect('profile')
                else:
                    messages.error(request, "Sorry, you're not an authorized Ion user!", extra_tags='danger')
                    return redirect('blog-home')

        messages.warning(request, "Invalid Callback Response")
        return redirect('blog-home')

@login_required
def logout(request):
    auth_logout(request)
    return render(request, 'users/logout.html')

@login_required
def profile(request):
    if request.method == "POST":
        userForm = UserUpdateForm(request.POST, instance=request.user)
        profileForm = ProfileUpdateForm(request.POST,
                                        request.FILES,
                                        instance=request.user.profile)

        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            messages.success(request, "Your account has been updated!")
            return redirect('profile')
    else:
        userForm = UserUpdateForm(instance=request.user)
        profileForm = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'userForm': userForm,
        'profileForm': profileForm
    }

    return render(request, 'users/profile.html', context)
