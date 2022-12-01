from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def index(request):
    res = None
    userauth = None
    if(request.user.is_authenticated):
        userauth = request.user
    template = loader.get_template('textfud.html')
    if(request.method=='POST' and request.POST['textfood']):
        data = request.POST['textfood']
        api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
        query = data
        response = requests.get(api_url + query, headers={'X-Api-Key': '3cYp06EjR3L15nU93CNiFA==nbMdfDFaPv8jImVt','Origin':'api.calorieninjas.com'})
        res = response.json()
    context = {
    'res':res,
    'user': userauth
    }
    return HttpResponse(template.render(context))
