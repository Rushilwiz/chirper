from django.shortcuts import render, redirect
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError
from django.views.decorators.csrf import csrf_exempt
import json
import requests

# Create your views here.

client_id = r'6p7HJlFCD8cnBNBEdgMsdULS5ph0jserw1xvWfxX'
client_secret = r'E1e79KebxzAp0LBEtxcUg32b0qFP9Ap9Dxqkac6Qhci5AwXFhSfrbe7MtmGJUh6DDgxivJpGgFYNQgusfvoSraDAnsq3NnEET5DmxgfBBvvuYc2bwDq6KpeKIDQqFtwz'
redirect_uri = 'http://localhost:8000/login/'
token_url = 'https://ion.tjhsst.edu/oauth/authorize/'
scope=["read","write"]

def login(request):
    if request.method == "GET":
        code = request.GET.get('code')
        if code is not None:
            payload = {'grant_type':'authorization_code','code': code,'redirect_uri':redirect_uri,'client_id':client_id,'client_secret':client_secret, 'csrfmiddlewaretoken': request.GET.get("state")}
            token = requests.post("https://ion.tjhsst.edu/oauth/token/", data=payload)
            # profile = requests.post("https://ion.tjhsst.edu/api/profile", headers="Authorization: Bearer {token.access_token}")
            return redirect('/')


    oauth = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = oauth.authorization_url("https://ion.tjhsst.edu/oauth/authorize/")
    print(f'a_url: {authorization_url}')

    return redirect(authorization_url)
