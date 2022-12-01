from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def index(request):
    template = loader.get_template('recipe.html')
    userauth = None
    if(request.user.is_authenticated):
        userauth = request.user
    if(request.method=='POST' and request.POST['recipe']):
        data = request.POST['recipe']
        api_url = 'https://api.calorieninjas.com/v1/recipe?query='
        query = data
        response = requests.get(api_url + query, headers={'X-Api-Key': '3cYp06EjR3L15nU93CNiFA==nbMdfDFaPv8jImVt','Origin':'api.calorieninjas.com'})
        res = response.json()
        context = {
        'user': userauth,
        'title':res[0]['title'],
        'servings':res[0]['servings'],
        'ingredients':res[0]['ingredients'].split('|'),
        'instructions':res[0]['instructions']
        }
        return HttpResponse(template.render(context))
    else:
        context = {
            'user': userauth
        }
        return HttpResponse(template.render(context))
