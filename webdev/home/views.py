from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
  template = loader.get_template('index.html')
  context = {}
  if(request.user.is_authenticated):
        context = {
            'user': request.user
        }
        return render(request, 'index.html',context)
  return HttpResponse(template.render(context))