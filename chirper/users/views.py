from django.shortcuts import render, redirect
from requests_oauthlib import OAuth2Session
from django.views.decorators.csrf import csrf_exempt
import requests

# Create your views here.

client_id = r'6p7HJlFCD8cnBNBEdgMsdULS5ph0jserw1xvWfxX'
client_secret = r'E1e79KebxzAp0LBEtxcUg32b0qFP9Ap9Dxqkac6Qhci5AwXFhSfrbe7MtmGJUh6DDgxivJpGgFYNQgusfvoSraDAnsq3NnEET5DmxgfBBvvuYc2bwDq6KpeKIDQqFtwz'
redirect_uri = 'http://localhost:8000/login/callback/'
token_url = 'https://ion.tjhsst.edu/oauth/authorize/'
scope=["read","write"]

def login(request):
    client = requests.session()

    oauth = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = oauth.authorization_url("https://ion.tjhsst.edu/oauth/authorize/")
    print(f'a_url: {authorization_url}')

    return redirect(authorization_url)

# {'grant_type':'authorization_code','code':code,'redirect_uri':redirect_uri,'client_id':client_id,'client_secret':client_secret}


def callback(request):
    return render(request, 'users/callback.html')
    code = fr"{request.GET.get('code')}"
    payload = {'grant_type':'authorization_code','code':code,'redirect_uri':redirect_uri,'client_id':client_id,'client_secret':client_secret}
    token  = requests.post(token_url, data=payload)
    #print (code)
    #token = oauth.fetch_token(token_url=token_url, code=code, client_secret=client_secret)
    print(token)
