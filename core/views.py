from django.shortcuts import render,HttpResponseRedirect
from .models import *
import os
from django.contrib import messages


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
        messages.success(request, f'File Delete successfully!')
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
                messages.success(request, f'File download successfully!')
                return response
        else:
            return HttpResponse("File not found.", status=404)

# @csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']  # Get the uploaded file

     
        file_upload = UploadedFile.objects.create( file=file)
        file_upload.save()
        messages.success(request, f'Fileuploaded successfully!')
        return HttpResponseRedirect("/")
    
  