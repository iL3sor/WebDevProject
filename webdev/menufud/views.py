from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

# Create your views here.
# def index(request):
#     # return HttpResponse(res)
#     api_url = 'https://api.calorieninjas.com/v1/imagetextnutrition'
#     image_file_descriptor = open('menufud/test.jpg', 'rb')
#     files = {'media': image_file_descriptor}
#     r = requests.post(api_url, files=files,headers={'X-Api-Key': '3cYp06EjR3L15nU93CNiFA==nbMdfDFaPv8jImVt'})
#     res = r.json()
#     return HttpResponse(str(res))

@csrf_exempt
def index(request):
  template = loader.get_template('menufud.html')
  res = None
  if(request.method=='POST') and request.FILES['fileupload']:
    myfile = request.FILES['fileupload']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    api_url = 'https://api.calorieninjas.com/v1/imagetextnutrition'
    image_file_descriptor = open(filename, 'rb')
    files = {'media': image_file_descriptor}
    r = requests.post(api_url, files=files,headers={'X-Api-Key': '3cYp06EjR3L15nU93CNiFA==nbMdfDFaPv8jImVt'})
    res = r.json()
  context = {
    'res':res
  }
  return HttpResponse(template.render(context))