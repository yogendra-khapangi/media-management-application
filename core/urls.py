from django.urls import path
from core.views import *

urlpatterns = [
    path('',index),
    path('upload/', upload_file, name='uploadfile'),
    path('delete/<int:id>',delete_data,name='deletedata'),
    path('download/<int:id>/', download_file, name='downloadfile'),
]
