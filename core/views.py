from django.shortcuts import render,HttpResponseRedirect
from .models import *
import os
from .forms import FileUploadForm

# Create your views here.
def index(request):

    # val=UploadedFile.objects.all()
    # print(type(val))

    allProds = []
    catprods = UploadedFile.objects.values('category', 'id')
    # print(catprods)
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = UploadedFile.objects.filter(category=cat)
        allProds.append([prod])
        params = {'allProds': allProds}
    # print(params)
    return render(request,'core/index.html',params)

def delete_data(request,id):
    if request.method== 'POST':
        pi=UploadedFile.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/')
    
def download_file(request,id):
    if request.method== 'POST':
        pi=UploadedFile.objects.get(pk=id)

        file_path=pi.file.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                print(response)
                return response
        else:
            return HttpResponse("File not found.", status=404)
        # pi.delete()
        # return HttpResponseRedirect('/')

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request,"core/hello.html") # Redirect to a success page
    else:
        form = FileUploadForm()
    return HttpResponseRedirect('/')