import io

import nltk

import codecs as cs

from nltk.corpus import words

from pdfminer.converter import TextConverter as T

from pdfminer.pdfinterp import PDFPageInterpreter as PI

from pdfminer.pdfinterp import PDFResourceManager as PD

from pdfminer.pdfpage import PDFPage as PP

nltk.download('words')
from django.views.generic import TemplateView

from django.shortcuts import render

from django.core.files.storage import FileSystemStorage

import os,shutil

from django.conf import settings

from django.http import HttpResponse, Http404

from django.core.mail import EmailMessage

#import requests

class home(TemplateView):
     template_name = 'Home.html'


def extract_text_by_page(pdf_path):
    with open(pdf_path, 'rb') as fh:
        for page in PP.get_pages(fh,caching=True,check_extractable=True):
            
            resource_manager = PD()
            
            fake_file_handle = io.StringIO()
            
            converter = T(resource_manager, fake_file_handle)
            
            page_interpreter = PI(resource_manager, converter)
           
            page_interpreter.process_page(page)
            
            text = fake_file_handle.getvalue()
           
            yield text
            # close open handles
            converter.close()
            fake_file_handle.close()
    fh.close()            


def extract_text(pdf_path):
    
    text=""
    
    for page in extract_text_by_page(pdf_path):
        
        text+=page
    
    return text


def mainfun(request):
    
    data="I'M Trying My Best..."
    if request.method == 'POST':
    
        uploaded_file = request.FILES['document']
        
        fs = FileSystemStorage()
        
        if not os.path.exists(os.path.join(settings.BASE_DIR+"\media",uploaded_file.name)):
        
            fs.save(uploaded_file.name,uploaded_file)
            
        
        file = open(os.path.join(settings.BASE_DIR+"\media",uploaded_file.name))
        global x
        x=uploaded_file.name
        if os.path.exists(settings.BASE_DIR+"\Formula1.txt"):
            
            os.remove(settings.BASE_DIR+"\Formula1.txt")
            
         
        data=Formula(extract_text(file.name))

        if os.path.exists(settings.BASE_DIR+"\media\Formula1.txt"):
            
            os.remove(settings.BASE_DIR+"\media\Formula1.txt")
            
        shutil.move(settings.BASE_DIR+'\Formula1.txt',settings.BASE_DIR+"\media")
         
        
        
    else:
        data=""
        
    return render(request,'Intern/original.html',{'data':data})

def download(request):
    file_path = os.path.join(settings.MEDIA_ROOT, "Formula1.txt")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            if os.path.exists(os.path.join(settings.BASE_DIR+"\media",x)):
                os.remove(os.path.join(settings.BASE_DIR+"\media",x))
            
            return response
    raise Http404
    
def SendMail(request):
     
    if request.method == 'POST':
    
        Email = request.POST.get("emai")
        recipient = [Email]
        email = EmailMessage("Formula_File","Contains formulas",settings.EMAIL_HOST_USER,recipient)
        
        email.attach_file('media/Formula1.txt')
        
        email.send()
        
    if os.path.exists(os.path.join(settings.BASE_DIR+"\media",x)):
        os.remove(os.path.join(settings.BASE_DIR+"\media",x)) 
    data = ''    
    return render(request,'Intern/original.html',{'data':data})


def Formula(text):
    
    
    data="" 
    for c,e in enumerate(text):
         x=""
          
          
         if e == "=":
          
             if c-30<0:
                   
                 i=c+40;
                 while i<len(text) and text[i]!=chr(32) and text[i]!='.':
                     i+=1
                 x = text[:i] 
                    
                 
                  
             else:
                 
                    #x = text[c-30:c+30] 
                 j=c-28;
                 
                 while j>0 and text[j]!=chr(32):
                     
                     j-=1
                 i=c+40;
                 
                 while i<len(text) and text[i]!=chr(32) and text[i]!='.':
                     
                     i+=1
                 x = text[j:i] 
         l=1
         first = []
         second= []             
         if('+' in x or '-' in x or '*' in x or '/' in x):
              for i in x.split():
                  if l:
                     
                      first.append(i)
                  else:
                      second.append(i)
                  
                  if '=' in i:
                      
                      l=0
                       
               
              i=len(first)-1
              flag = -1
              while i > -1:
                   
                  x = first[i]
                  j=len(x)
                  p=0
                  while j-p>3:
                        if x[:j-p] in words.words() or x[:j-p].title() in words.words() or x[:j-p].lower() in words.words():
                            flag = i
                           
                            break 
                        p += 1
                  i -= 1    
                  if flag > -1:
                      break        
              c=flag+1 
              f = cs.open("Formula1.txt","a","utf8")
             
              tcs = ""
              
              #print(" \n *************************************************************** \n ")
              while c < len(first):
                  if len(first[c])==1 or first[c] not in words.words() and first[c].title() not in words.words() and first[c].lower() not in words.words():
                      #print(first[c],end="")
                      tcs += first[c]
                      
                  c += 1
              i=0
              flag = -1
              while i < len(second):
                   
                  x = second[i]
                  j=len(x)
                  p=0
                  while j-p>3:
                       
                      if x[:j-p] in words.words() or x[:j-p].title() in words.words() or x[:j-p].lower() in words.words():
                          flag = i
                           
                          break 
                      p += 1
                  i += 1    
                  if flag > -1:
                      break
              c=0
              while c < flag:
                  
                  if len(second[c])==1 or second[c] not in words.words() and second[c].title() not in words.words() and second[c].lower() not in words.words():
                      #print(second[c],end="")
                      tcs += second[c]
                      
                       
                  c += 1
              tcs += "\n\n"
              
              SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
              R = tcs[0]
              L = ['+','-','*','/']
              for i in range(1,len(tcs)):
                  if tcs[i-1] not in L and tcs[i].isdigit():
                      R+=tcs[i].translate(SUP)
                  elif  tcs[i-1]=='^' and tcs[i].isdigit():
                      R=R[:-1]+tcs[i].translate(SUP)
                  else:
                      R+=tcs[i]
              data += R 
              
              f.write(R)
              
              f.close()
              
    
    if not os.path.exists(settings.BASE_DIR+"\Formula1.txt"):
        f = cs.open("Formula1.txt","a","utf8")
        f.write("Unable to find any formula")
        data = "Unable to find any formula"
    return data         
