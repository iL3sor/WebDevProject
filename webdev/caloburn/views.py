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
    template = loader.get_template('caloburned.html')
    if(request.method=='POST' and request.POST['activity']):
        activity = request.POST['activity'].split(':')[0].strip()
        minute = request.POST['activity'].split(':')[1].strip()
        api_url = 'https://api.api-ninjas.com/v1/caloriesburned?activity={}'.format(activity)
        response = requests.get(api_url, headers={'X-Api-Key': '3cYp06EjR3L15nU93CNiFA==wvSnpxPumVUIcHiE','Origin':'api-ninjas.com'})
        res = response.json()
        for i in range(len(res)):
            res[i]['total_calories'] = res[i]['total_calories']/60*int(minute)
    context = {
    'res':res,
    'user': userauth
    }
    return HttpResponse(template.render(context))
