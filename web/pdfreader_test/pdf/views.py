from distutils.command.upload import upload
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import os
from .pdf_storge import pdf_test
from datetime import datetime
import re

@csrf_exempt
def upload_files(request):
      if request.method == "GET":
         today=datetime.now()
         m=int(today.strftime('%m'))
         d=int(today.strftime('%d'))
         url=str(request.build_absolute_uri())
         urls1=url.split('?')
         urls2=urls1[1].split('&')
         ap_source=urls2[0].split('=')
         ap_user=urls2[1].split('=')
         ap_ip=urls2[2].split('=') 
         ap_source=ap_source[1] 
          
         global ap_user_g
         global ap_ip_g
         ap_user_g=ap_user[1]
         ap_ip_g=ap_ip[1]  
         if ap_source == str((m+300)*(d+300)+2):
             return render(request,'test.html')
         else:
             return HttpResponse('錯誤')
      if request.method == "POST":
           #try:
               files=request.FILES.getlist('uploadedFile')
               for file_up in files:
                   suffix = file_up.name.rfind('.')
                   if suffix == -1:
                      ctx={}
                      ctx['message']='檔案錯誤'
                   file_postfix = file_up.name[suffix+1:]
                   if file_postfix not in ['pdf']:
                      ctx={}
                      ctx['message']='檔案格式錯誤'
                   else:
                      pdf_test.handle_file(file_up)
                      message=pdf_test.pdfreader(ap_user_g,ap_ip_g)
                      ctx={}
                      ctx['message']=message
               return render(request,'test.html',ctx)
           #except:
           #    ctx={}
           #    ctx['message']='上傳內容有誤或已存在'
           #    return render(request,'test.html',ctx)

