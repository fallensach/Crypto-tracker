from django.shortcuts import render
# Create your views here.
from Cryptocurrency.apicalls import crypto_api
from json2html import *


def index(request):
    btc = crypto_api.getCrypto("btc")
    js = json2html.convert(json=btc)

    return render()