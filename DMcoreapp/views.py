from django.shortcuts import render
from venv import create
import qrcode
import random
import os, json, math
# import psycopg2
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from urllib.parse import urlencode
from django.views.decorators.csrf import csrf_exempt
from django. contrib import messages
from unicodedata import name

from django.shortcuts import render, redirect
from .models import *
from datetime import datetime,date, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from io import BytesIO
from django.core.files import File
from django.conf import settings
from django.db.models import Q
from num2words import num2words
from django.http import JsonResponse
from django.core.mail import send_mail

from django.core.files.storage import FileSystemStorage

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


from django.views.decorators.http import require_GET

import requests

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
# Create your views here.

#----------------------------------------------------------Login, Sign Up, Reset, Internshipform 
def login(request):
    return render(request, 'home/login.html')

def signin(request):
    print("function true")
    if request.method == 'POST':
        email  = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            return redirect('login')
        

        
        if user_registration.objects.filter(email=request.POST['email'], password=request.POST['password'],department="Admin",status="active").exists():
            print("function sucsess")

        if user_registration.objects.filter(email=request.POST['email'], password=request.POST['password'],department="Admin",status="active").exists():

            member = user_registration.objects.get(email=request.POST['email'],password=request.POST['password'])
            
            request.session['userid'] = member.id
            
            return redirect('ad_profile')


        elif user_registration.objects.filter(email=request.POST['email'], password=request.POST['password'],department="Digital Marketing Head",status="active").exists():
            member = user_registration.objects.get(email=request.POST['email'],password=request.POST['password'])
            request.session['userid'] = member.id
            return redirect('he_profile')

        elif user_registration.objects.filter(email=request.POST['email'], password=request.POST['password'],department="Digital Marketing Executive",status="active").exists():
            member = user_registration.objects.get(email=request.POST['email'],password=request.POST['password'])
            request.session['userid'] = member.id

            return redirect('ex_profile')
        else:
            print("function false")
            return redirect('login')


           

def signup(request):
    return render(request, 'home/signup.html')

def registration_form(request):

 
    a = user_registration()
    b = qualification()
    c = extracurricular()

    if request.method == 'POST':
        if  user_registration.objects.filter(email=request.POST['email']).exists():
            
            msg_error = "Mail id already exist"
            return render(request, 'home/signup.html',{'msg_error': msg_error})
        else:
            
            a.fullname = request.POST['fname']
            a.fathername = request.POST['fathername']
            a.mothername = request.POST['mothername']
            a.dateofbirth = request.POST['dob']
            a.gender = request.POST['gender']
            a.presentaddress1 = request.POST['address1']
            a.presentaddress2  =  request.POST['address2']
            a.presentaddress3 =  request.POST['address3']
            a.pincode = request.POST['pincode']
            a.district  =  request.POST['district']
            a.state  =  request.POST['state']
            a.country  =  request.POST['country']
            a.permanentaddress1 = request.POST['paddress1']
            a.permanentaddress2  =  request.POST['paddress2']
            a.permanentaddress3  =  request.POST['paddress3']
            a.permanentpincode = request.POST['ppincode']
            a.permanentdistrict  =  request.POST['pdistrict']
            a.permanentstate  =  request.POST['pstate']
            a.permanentcountry =  request.POST['pcountry']
            a.mobile = request.POST['mobile']
            a.alternativeno = request.POST['alternative']
            a.department = request.POST['department']
            a.email = request.POST['email']
            a.status = "active"
            a.designation = request.POST['designation']
            a.password= random.SystemRandom().randint(100000, 999999)
            
            #a.branch_id = request.POST['branch']
            a.photo = request.FILES['photo']
            a.idproof = request.FILES['idproof']
            a.save()
            
            x = user_registration.objects.get(id=a.id)
            today = date.today()
            tim = today.strftime("%m%y")
            x.employee_id = "INF"+str(tim)+''+"B"+str(x.id)
            passw=x.password
            email_id=x.email
            x.save()
            y1 = user_registration.objects.get(id=a.id)
            qr = qrcode.make("http://altoscore.in/offerletter/" + str(y1.id))
            qr.save(settings.MEDIA_ROOT + "/images"+"//" +"offer"+str(y1.id) + ".png")
            with open(settings.MEDIA_ROOT + "/images"+"//"+"offer"+ str(y1.id) +".png","rb") as reopen:
                    djangofile = File(reopen)
                    y1.offerqr = djangofile
                    y1.save()
    
            y2 = user_registration.objects.get(id=a.id)
            qr1 = qrcode.make("http://altoscore.in/relieveletter/" + str(y2.id))
            qr1.save(settings.MEDIA_ROOT + "/images"+"//"+"re" +str(y2.id) + ".png")
            with open(settings.MEDIA_ROOT + "/images"+"//"+"re" + str(y2.id) + ".png", "rb") as reopen:
                    djangofile = File(reopen)
                    y2.relieveqr = djangofile
                    y2.save()
            y3 = user_registration.objects.get(id=a.id)
            qr2 = qrcode.make("http://altoscore.in/experienceletter/" + str(y3.id))
            qr2.save(settings.MEDIA_ROOT + "/images"+"//"+"exp" +str(y3.id) + ".png")
            with open(settings.MEDIA_ROOT + "/images"+"//"+"exp" + str(y3.id) + ".png", "rb") as reopen:
                    djangofile = File(reopen)
                    y3.expqr = djangofile
                    y3.save()
           
    
            b.user_id = a.id
            b.plustwo = request.POST.get('plustwo')
            b.school = request.POST['school']
            b.schoolaggregate = request.POST['aggregate']
            if request.FILES.get('cupload') is not None:
                b.schoolcertificate = request.FILES['cupload']
            b.ugdegree = request.POST['degree']
            b.ugstream = request.POST['stream']
            b.ugpassoutyr = request.POST['passoutyear']
            b.ugaggregrate = request.POST['aggregate1']
            b.backlogs = request.POST['supply']
            if request.FILES.get('cupload1') is not None:
                b.ugcertificate = request.FILES['cupload1']
            b.pg = request.POST['pg']
            b.save()
    
            c.user_id = a.id
            c.internshipdetails = request.POST['details']
            c.internshipduration = request.POST['duration']
            c.internshipcertificate = request.POST['certificate']
            c.onlinetrainingdetails = request.POST['details1']
            c.onlinetrainingduration = request.POST['duration1']
            c.onlinetrainingcertificate= request.POST['certificate1']
            c.projecttitle = request.POST['title']
            c.projectduration = request.POST['duration2']
            c.projectdescription = request.POST['description']
            c.projecturl = request.POST['url']
            c.skill1 = request.POST['skill1']
            c.skill2 = request.POST['skill2']
            c.skill3 = request.POST['skill3']
            c.save()
            
            subject = 'Greetings from ALTOS TECHNOLOGIES'
            message = 'Congratulations,\nYou have successfully registered ALTOS TECHNOLOGIES.\nYour login credentials \n\nEmail :'+str(email_id)+'\nPassword :'+str(passw)+'\n\nNote: This is a system generated email, do not reply to this email id.'
            email_from = settings.EMAIL_HOST_USER
            
            recipient_list = [email_id, ]
            send_mail(subject,message , email_from, recipient_list, fail_silently=True)
            msg_success = "Registration successfully Check Your Registered Mail"
            return redirect('login')
        
    return redirect('login')



def reset_password(request):
    if request.method == "POST":
        email_id = request.POST.get('email')
        access_user_data = user_registration.objects.filter(email=email_id).exists()
        if access_user_data:
            _user = user_registration.objects.get(email=email_id)
            password = random.SystemRandom().randint(100000, 999999)

            _user.password = password
            subject = 'iNFOX Technologies your authentication data updated'
            message = 'Password Reset Successfully\n\nYour login details are below\n\nUsername : ' + str(email_id) + '\n\nPassword : ' + str(password) + \
                '\n\nYou can login this details\n\nNote: This is a system generated email, do not reply to this email id'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email_id, ]
            send_mail(subject, message, email_from,
                      recipient_list, fail_silently=True)

            _user.save()
            msg_success = "Password Reset successfully check your mail new password"
            return render(request, 'Reset_password.html', {'msg_success': msg_success})
        else:
            msg_error = "This email does not exist iNFOX Technologies "
            return render(request, 'Reset_password.html', {'msg_error': msg_error})

    return render(request,'home/Reset_password.html')

def internshipform(request):
    # branch = branch_registration.objects.all()
    return render(request, 'home/internship.html')

def internship_save(request):

    a = internship()
    if request.method == 'POST':
        try:
            a.fullname = request.POST['name']
            a.collegename = request.POST['college_name']
            a.reg_date = datetime.now()
            a.reg_no = request.POST['reg_no']
            a.course = request.POST['course']
            a.stream = request.POST['stream']
            a.platform = request.POST['platform']

            a.start_date =  request.POST['start_date']
            a.end_date  =  request.POST['end_date']
            a.mobile  =  request.POST['mobile']

            a.alternative_no  =  request.POST['alternative_no']

            a.email = request.POST['email']
            a.profile_pic  =  request.FILES['profile_pic']
            if (a.end_date<a.start_date):
                return render(request,'home/internship.html',{'a':a})
            else:
                a.save()
                qr = qrcode.make("https://altoscore.in/admin_code?id=" + str(a.id))
                qr.save(settings.MEDIA_ROOT + "\\" +str(a.id) + ".png")
                with open(settings.MEDIA_ROOT + "\\" + str(a.id) + ".png", "rb") as reopen:
                        djangofile = File(reopen)
                        a.qr = djangofile

                        a.save()
           
            msg_success="Your application has been sent successfully"
            Flag='True'
            return render(request, 'home/internship.html',{'msg_success':msg_success})
        except:
            message = "Enter all details !!!"
            return render(request, 'home/internship.html',{'message':message})
    else:
        
        return render(request, 'home/internship.html')



# -----------------------------------------------------------------------------Admin Section

def ad_base(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    context={
        "usr":usr,
    }
    return render(request, 'admin/ad_base.html',context)

def ad_profile(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    context={
        "usr":usr,
    }
    return render(request, 'admin/ad_profile.html',context )

def ad_dashboard(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    context={
        "usr":usr,
    }
    return render(request, 'admin/ad_dashboard.html',context)

def ad_create_work(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    context={
        "usr":usr,
    }
    return render(request, 'admin/ad_create_work.html',context)

def save_create_work(request):
    client = client_information()
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    
    if request.session.has_key('userid'):
        userid = request.session['userid']
    else:
       return redirect('/')
    if request.method == 'POST':
        client.client_name = request.POST.get('client_name')
        
        client.client_address = request.POST.get('client_address')
        client.client_mail = request.POST.get('client_mail')
        client.bs_name = request.POST.get('bs_name')
        client.bs_website = request.POST.get('bs_website',None)
       
        client.bs_location = request.POST.get('bs_location')
        client.client_files = request.FILES.get('client_files',None)
        client.seo = request.POST.get('seo',None)
        client.seo_txt = request.POST.get('seo_txt',None)
        client.seo_file = request.FILES.get('seo_file',None)

        client.on_pg = request.POST.get('onpage',None)
        client.on_pg_txt = request.POST.get('on_txt',None)
        client.on_pg_file = request.FILES.get('on_file',None)

        client.off_pg = request.POST.get('offpage',None)
        client.off_pg_txt = request.POST.get('off_txt',None)
        client.off_pg_file = request.FILES.get('off_file',None)

        client.smm = request.POST.get('smm',None)
        client.smm_txt = request.POST.get('smm_txt',None)
        client.smm_file = request.FILES.get('smm_file',None)
        client.smo = request.POST.get('smo',None)
        client.smo_txt = request.POST.get('smo_txt',None)
        client.smo_file = request.FILES.get('smo_file',None)

        client.sem = request.POST.get('sem',None)
        client.sem_txt = request.POST.get('sem_txt',None)
        client.sem_file = request.FILES.get('sem_file',None)
        client.em = request.POST.get('em',None)
        client.em_txt = request.POST.get('em_txt',None)
        client.em_file = request.FILES.get('em_file',None)
        client.cm = request.POST.get('cm',None)
        client.cm_txt = request.POST.get('cm_txt',None)
        client.cm_file = request.FILES.get('cm_file',None)
        client.am = request.POST.get('am',None)
        client.am_txt = request.POST.get('am_txt',None)
        client.am_file = request.FILES.get('am_file',None)
        client.mm = request.POST.get('mm',None)
        client.mm_txt = request.POST.get('mm_txt',None)
        client.mm_file = request.FILES.get('mm_file',None)
        client.vm = request.POST.get('vm',None)
        client.vm_txt = request.POST.get('vm_txt',None)
        client.vm_file = request.FILES.get('vm_file',None)
        client.user=usr
        client.save()
        
        client = client_information.objects.get(id=client.id)
        
        labels = request.POST.getlist('label[]')
        text =request.POST.getlist('dis[]')
        
        if len(labels)==len(text):
            mapped = zip(labels,text)
            mapped=list(mapped)
            for ele in mapped:
            
                created = addi_client_info.objects.get_or_create(labels=ele[0],discription=ele[1],user=usr,client=client,section='client_information')
        else:
            pass

        labels2 = request.POST.getlist('label2[]')
        text2 =request.POST.getlist('dis2[]')
        
        if len(labels2)==len(text2):
            mappeds = zip(labels2,text2)
            mappeds=list(mappeds)
            for ele in mappeds:
            
                created = addi_client_info.objects.get_or_create(labels=ele[0],discription=ele[1],user=usr,client=client,section='business_details')
        else: 
            pass
          
        
        files_req =request.FILES.getlist('file_add[]') 
        label_req =request.POST.getlist('label_req[]')
        dis_req =request.POST.getlist('dis_req[]')

        
        if len(files_req)==len(label_req)==len(dis_req):
            mapped2 = zip(label_req,dis_req,files_req)
            mapped2=list(mapped2)
         
            for ele in mapped2:
                created = addi_client_info.objects.get_or_create(labels=ele[0],discription=ele[1],file=ele[2],user=usr,client=client,section='requirments')

        msg_success = "Save Successfully"
        context={
            "usr":usr,
            "msg_success":msg_success,
        }
        return redirect("ad_dashboard") 
        
    return redirect("ad_create_work")


def ad_view_work(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)

    client=client_information.objects.filter(user=ids)

    context={
        "usr":usr,
        "client":client,
    }
    return render(request, 'admin/ad_view_work.html',context)

def ad_view_clint(request,id):
    client=client_information.objects.get(id=id)
    addicl=addi_client_info.objects.filter(client=client.id,section='client_information')
    addibs=addi_client_info.objects.filter(client=client.id,section='business_details')
    addirq=addi_client_info.objects.filter(client=client.id,section='requirments')
    
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    context={
        "usr":usr,
        "client":client,
        "addicl":addicl,
        "addibs":addibs,
        "addirq":addirq,
    }
    return render(request, 'admin/ad_view_clint.html',context)



def update_client(request,id):
    client = client_information.objects.get(id=id)
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    
    if request.session.has_key('userid'):
        userid = request.session['userid']
    else:
       return redirect('/')
    if request.method == 'POST':
        client.client_name = request.POST.get('client_name')
        
        client.client_address = request.POST.get('client_address')
        client.client_mail = request.POST.get('client_mail')
        client.bs_name = request.POST.get('bs_name')
        client.bs_website = request.POST.get('bs_website',None)
       
        client.bs_location = request.POST.get('bs_location')
        if request.FILES.get('client_files',None) == None:
            client.client_files=client.client_files
        else:
            client.client_files = request.FILES.get('client_files',None)
      
        client.seo = request.POST.get('seo',None)
        client.seo_txt = request.POST.get('seo_txt',None)
        if request.FILES.get('seo_file',None) == None:
            client.seo_file=client.seo_file
        else:
            client.seo_file = request.FILES.get('seo_file',None)

        client.on_pg = request.POST.get('onpage',None)
        client.on_pg_txt = request.POST.get('on_txt',None)
        if request.FILES.get('on_file',None) == None:
            client.on_pg_file=client.on_pg_file
        else:
            client.on_pg_file = request.FILES.get('on_file',None)


        client.off_pg = request.POST.get('offpage',None)
        client.off_pg_txt = request.POST.get('off_txt',None)
        if request.FILES.get('off_file',None) == None:
            client.off_pg_file=client.off_pg_file
        else:
            client.off_pg_file = request.FILES.get('off_file',None)
   


        client.smm = request.POST.get('smm',None)
        client.smm_txt = request.POST.get('smm_txt',None)
     
        if request.FILES.get('smm_file',None) == None:
            client.smm_file=client.smm_file
        else:
            client.smm_file = request.FILES.get('smm_file',None)

        client.smo = request.POST.get('smo',None)
        client.smo_txt = request.POST.get('smo_txt',None)
     
        if request.FILES.get('smo_file',None) == None:
            client.smo_file=client.smo_file
        else:
            client.smo_file = request.FILES.get('smo_file',None)

        client.sem = request.POST.get('sem',None)
        client.sem_txt = request.POST.get('sem_txt',None)
    

        if request.FILES.get('sem_file',None) == None:
            client.sem_file=client.sem_file
        else:
            client.sem_file = request.FILES.get('sem_file',None)


        client.em = request.POST.get('em',None)
        client.em_txt = request.POST.get('em_txt',None)

        if request.FILES.get('em_file',None) == None:
            client.em_file=client.em_file
        else:
            client.em_file = request.FILES.get('em_file',None)


        client.cm = request.POST.get('cm',None)
        client.cm_txt = request.POST.get('cm_txt',None)

        if request.FILES.get('cm_file',None) == None:
            client.cm_file=client.cm_file
        else:
            client.cm_file = request.FILES.get('cm_file',None)


        client.am = request.POST.get('am',None)
        client.am_txt = request.POST.get('am_txt',None)

        if request.FILES.get('am_file',None) == None:
            client.am_file=client.am_file
        else:
            client.am_file = request.FILES.get('am_file',None)


        client.mm = request.POST.get('mm',None)
        client.mm_txt = request.POST.get('mm_txt',None)

        if request.FILES.get('mm_file',None) == None:
            client.mm_file=client.mm_file
        else:
            client.mm_file = request.FILES.get('mm_file',None)


        client.vm = request.POST.get('vm',None)
        client.vm_txt = request.POST.get('vm_txt',None)

        if request.FILES.get('vm_file',None) == None:
            client.vm_file=client.vm_file
        else:
            client.vm_file = request.FILES.get('vm_file',None)


        client.user=usr
        client.save()
        client = client_information.objects.get(id=id)
       

        
        client = client_information.objects.get(id=client.id)
        
        labels = request.POST.getlist('label[]')
        text =request.POST.getlist('dis[]')
        
        if len(labels)==len(text):
            mapped = zip(labels,text)
            mapped=list(mapped)
            for ele in mapped:
                try:
                    adiclient = addi_client_info.objects.get(Q(client=client),Q(labels=ele[0])|Q(discription=ele[1]))
                    
                 
                    if ((adiclient.labels==ele[0]) or (adiclient.discription==ele[1])):
                        created = addi_client_info.objects.filter(Q(client=client),Q(labels=ele[0])|Q(discription=ele[1])).update(labels=ele[0],discription=ele[1])
                     
                    
                    elif ((adiclient.labels!=ele[0]) or (adiclient.discription!=ele[1])):
                        created = addi_client_info.objects.get_or_create(labels=ele[0],discription=ele[1],user=usr,client=client,section='client_information')
                   
                    else:
                        pass
                        
                except:
                    created = addi_client_info.objects.get_or_create(labels=ele[0],discription=ele[1],user=usr,client=client,section='client_information')



        else:
            pass

        labels2 = request.POST.getlist('label2[]')
        text2 =request.POST.getlist('dis2[]')
        
        if len(labels2)==len(text2):
            mappeds = zip(labels2,text2)
            mappeds=list(mappeds)

      
            for ele in mappeds:
                try:
                    adiclient=addi_client_info.objects.get(Q(client=client),Q(labels=ele[0])|Q(discription=ele[1]))
                    if ((adiclient.labels==ele[0]) or (adiclient.discription==ele[1])):
                        created = addi_client_info.objects.filter(Q(client=client),Q(labels=ele[0])|Q(discription=ele[1])).update(labels=ele[0],discription=ele[1])
                    elif ((adiclient.labels!=ele[0]) or (adiclient.discription!=ele[1])):
                        created = addi_client_info.objects.get_or_create(labels=ele[0],discription=ele[1],client=client,user=usr,section='business_details')
                    else:
                        pass
                except:
                    created = addi_client_info.objects.get_or_create(labels=ele[0],discription=ele[1],client=client,user=usr,section='business_details')

        else: 
            pass
        
      
          

        
        files_req =request.FILES.getlist('file_add[]') 
        label_req =request.POST.getlist('label_req[]')
        dis_req =request.POST.getlist('dis_req[]')
        
        if len(label_req)==len(dis_req):
            mapped2 = zip(label_req,dis_req,files_req)
            mapped2=list(mapped2)
            print(mapped2)
       
        
            for ele in mapped2:
                try:
                    
                    adiclient=addi_client_info.objects.get(Q(client=client),Q(labels=ele[0])|Q(discription=ele[1]))
                    if ((adiclient.labels==ele[0]) or (adiclient.discription==ele[1])):
                        crt= addi_client_info.objects.get(Q(client=client),Q(labels=ele[0])|Q(discription=ele[1]))
                        crt.labels=ele[0]
                        crt.discription=ele[1]
                        crt.file=ele[2]
                        crt.save()
                        
                       
                    elif ((adiclient.labels!=ele[0]) or (adiclient.discription!=ele[1])):
                        print("sdfsdsfd")
                        created = addi_client_info.objects.get_or_create(labels=ele[0],discription=ele[1],file=ele[2],user=usr,client=client,section='Requirments')
                    else:
                        pass
                except:
                    created = addi_client_info.objects.get_or_create(labels=ele[0],discription=ele[1],file=ele[2],user=usr,client=client,section='Requirments')
                
        else:
            pass

        msg_success = "Save Successfully"
        return redirect('ad_view_clint',id)
    return redirect('ad_view_clint',id)




def ad_daily_work_det(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    dl_work=daily_work.objects.filter(date=date.today())

    dl_sub=daily_work_sub.objects.all() 
    dl_off=daily_off_sub.objects.all()
    
    context={
        "usr":usr,
        "dl_work":dl_work

    }
    return render(request, 'admin/ad_daily_work_det.html',context)


def ad_work_analiz_det(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    dl_sub=daily_work_sub.objects.all() 
    dl_off=daily_off_sub.objects.all()

    dl_work=daily_work.objects.all()
    context={
        "usr":usr,
        "dl_work":dl_work,
        "dl_sub":dl_sub,
        "dl_off":dl_off

    }
    return render(request, 'admin/ad_work_analiz_det.html',context)

def flt_dt_analiz(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    st_dt=request.POST.get('str_dt')
    en_dt=request.POST.get('end_dt')

    dl_work=daily_work.objects.filter(date__gte=st_dt,date__lte=en_dt)
    context={
        "usr":usr,
        "dl_work":dl_work

    }
    return render(request, 'admin/ad_work_analiz_det.html',context)


def ad_work_progress(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    pr_work=progress_report.objects.all()
    context={
        "usr":usr,
        "pr_work":pr_work

    }
    return render(request, 'admin/ad_work_progress.html',context)

def flt_progress(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    st_dt=request.POST.get('str_dt')
    en_dt=request.POST.get('end_dt')
    print(en_dt)
    pr_work=progress_report.objects.filter(start_date__gte=st_dt,start_date__lte=en_dt)
    context={
        "usr":usr,
        "pr_work":pr_work

    }
    return render(request, 'admin/ad_work_progress.html',context)


def ad_work_progress_det(request,id):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    
 
    pr_work=progress_report.objects.get(id=id)
    try:
        prv_work=progress_report.objects.filter(work_id=pr_work.work_id).order_by('-end_date')[1]
    except:
        prv_work=None
    context={
        "usr":usr,
        "pr_work":pr_work,
        "prv_work":prv_work

    }
    return render(request, 'admin/ad_work_progress_det.html',context) 

# 

def ad_warning_ex(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    exe=user_registration.objects.filter(department="Digital Marketing Executive")
   
    context={
        "usr":usr,
        "exe":exe

    }
    return render(request, 'admin/ad_warning_ex.html',context)

def ad_warning_sugg_dash(request,id):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    ids=id
    context={
        "usr":usr,
        "ids":ids
        

    }
    return render(request, 'admin/ad_warning_sugg_dash.html',context)

def ad_warning_det(request,id):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    warn = Warning.objects.filter(executive=id,type="Warning")
    context={
        "usr":usr,
        "warn":warn

    }
    return render(request, 'admin/ad_warning_det.html',context) 

def ad_suggestions_det(request,id):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    warn = Warning.objects.filter(executive=id,type="Suggestion")
    context={
        "usr":usr,
        "warn":warn

    }
    return render(request, 'admin/ad_suggestions_det.html',context)


def change_pass(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    if request.session.has_key('userid'):
        devid = request.session['userid']
    else:
        return redirect('/')
    dev = user_registration.objects.filter(id=devid)

    if request.method == 'POST':
        abc = user_registration.objects.get(id=devid)
        cur = abc.password
        oldps = request.POST["currentPassword"]
        newps = request.POST["newPassword"]
        cmps = request.POST["confirmPassword"]
        if oldps == cur:
            if oldps != newps:
                if newps == cmps:
                    abc.password = request.POST.get('confirmPassword')
                    abc.save()
                    return render(request, 'admin/ch_pass.html', {'dev': dev,"usr":usr})
            elif oldps == newps:
                messages.add_message(request, messages.INFO, 'Current and New password same')
            else:
                messages.info(request, 'Incorrect password same')

            return render(request, 'admin/ch_pass.html', {'dev': dev,"usr":usr})
        else:
            messages.add_message(request, messages.INFO, 'old password wrong')
            return render(request, 'admin/ch_pass.html', {'dev': dev,"usr":usr})
    return render(request, 'admin/ch_pass.html', {'dev': dev,"usr":usr})

def ad_accountset(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    if request.session.has_key('userid'):
        devid = request.session['userid']
    else:
        return redirect('/')
    dev = user_registration.objects.filter(id=devid)
    return render(request, 'admin/ad_accountset.html', {'dev': dev,"usr":usr})

def ad_imagechange(request, id):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    if request.session.has_key('userid'):
        devid = request.session['userid']
    else:
        return redirect('/')
    dev = user_registration.objects.filter(id=devid)
    if request.method == 'POST':
        abc = user_registration.objects.get(id=id)
        abc.photo = request.FILES['filename']
        
        abc.save()
        return redirect('ad_accountset')
    return render(request, 'admin/ad_accountset.html',{'dev': dev,"usr":usr})


def get_dis(request):
    ele = request.GET.get('ele')
    warn = daily_work.objects.get(id=ele)
    
    rep =warn.workdone
 
    return JsonResponse({"status":" not","rep":rep})

def get_sub(request):
    ele = request.GET.get('ele')
    ids = request.GET.get('idss')
    try:
        warn = daily_work.objects.get(id=ids)
    except:
        pass
    if ele=="Facebook":
        hd=ele
        des=warn.fb_txt
        fl=warn.fb_file

    elif ele=="Twitter":
        hd=ele
        des=warn.tw_txt
        fl=warn.tw_file

    elif ele=="Pinterest":
        hd=ele
        des=warn.pin_txt
        fl=warn.pin_file

    elif ele=="Linkedin":
        hd=ele
        des=warn.link_txt
        fl=warn.link_file

    elif ele=="Instagram":
        hd=ele
        des=warn.insta_txt
        fl=warn.insta_file

    elif ele=="Tumber":
        hd=ele
        des=warn.tumb_txt
        fl=warn.tumb_file

    elif ele=="Directories":
        hd=ele
        des=warn.diry_txt
        fl=warn.diry_file

    elif ele=="You Tube":
        hd=ele
        des=warn.yt_txt
        fl=warn.yt_file

    elif ele=="Quora":
        hd=ele
        des=warn.qra_txt
        fl=warn.qra_file

    elif ele=="PR Submission":
        hd=ele
        des=warn.pr_txt
        fl=warn.pr_file 

    elif ele=="Article Submission":
        hd=ele
        des=warn.art_txt
        fl=warn.art_file 

    elif ele=="Blog Posting":
        hd=ele
        des=warn.blg_txt
        fl=warn.blg_file 

    elif ele=="Classified Submission":
        hd=ele
        des=warn.clss_txt
        fl=warn.clss_file

    elif ele=="Guest Blogging":
        hd=ele
        des=warn.gst_txt
        fl=warn.gst_file

    elif ele=="Bokkmarking":
        hd=ele
        des=warn.bk_txt
        fl=warn.bk_file

    elif daily_off_sub.objects.filter(id=ids,sub=ele).exists():
       
        off = daily_off_sub.objects.get(id=ids,sub=ele)
        hd=off.sub
        des=off.sub_txt
        fl=off.sub_file
    else:
        
        sm = daily_work_sub.objects.get(id=ids,sub=ele)
        hd=sm.sub
        des=sm.sub_txt
        fl=sm.sub_file
        

    return JsonResponse({"status":" not","hd":hd,"des":des,"fl":str(fl),})

# -----------------------------------------------------------------------------Executive Section

def ex_base(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    context={
        "usr":usr,
    }
    return render(request, 'executive/ex_base.html',context)

def ex_profile(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    context={
        "usr":usr,
    }
    return render(request, 'executive/ex_profile.html',context)

def ex_dashboard(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    context={
        "usr":usr
    }
    return render(request, 'executive/ex_dashboard.html',context)

def ex_daily_work_clint(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    work_as=work_asign.objects.filter(exe_name=ids).values('client_name_id').distinct()
    last=work_asign.objects.filter(exe_name=ids).last()
    work=Work.objects.all()
    cl=client_information.objects.all()

   
    context={
        "usr":usr,
        "work_as":work_as,
        "work":work,
        "cl":cl,
        "last":last
    }
    return render(request, 'executive/ex_daily_work_clint.html',context)

def ex_daily_work_det(request,id):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    work_as=work_asign.objects.filter(exe_name=ids)
    works=Work.objects.filter(client_name_id=id).order_by("-id")
    daily=daily_work.objects.filter(user=ids)
    dl_sub=daily_work_sub.objects.all() 
    dl_off=daily_off_sub.objects.all()
    cr_date=date.today()
    
    context={
        "usr":usr,
        "cr_date":cr_date,
        "daily":daily,
        "work_as":work_as,
        "works":works,
        "dl_sub":dl_sub,
        "dl_off":dl_off
        
    }
    return render(request, 'executive/ex_daily_work_det.html',context)

def daily_work_done(request,id):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)

    work=Work.objects.get(id=id)
    if request.method == 'POST':
        daily = daily_work()
        daily.task=work.task
        daily.date=date.today()
        daily.workdone =request.POST.get('workdone',None)

        daily.fb = request.POST.get('fb',None)
        daily.fb_txt = request.POST.get('fb_txt',None)
        daily.fb_file = request.FILES.get('fb_file',None)
        daily.tw = request.POST.get('tw',None)
        daily.tw_txt = request.POST.get('tw_txt',None)
        daily.tw_file = request.FILES.get('tw_file',None)
        daily.pin = request.POST.get('pin',None)
        daily.pin_txt = request.POST.get('pin_txt',None)
        daily.pin_file = request.FILES.get('pin_file',None)
        daily.link = request.POST.get('link',None)
        daily.link_txt = request.POST.get('link_txt',None)
        daily.link_file = request.FILES.get('link_file',None)
        daily.insta = request.POST.get('insta',None)
        daily.insta_txt = request.POST.get('insta_txt',None)
        daily.insta_file = request.FILES.get('insta_file',None)
        daily.tumb = request.POST.get('tumb',None)
        daily.tumb_txt = request.POST.get('tumb_txt',None)
        daily.tumb_file = request.FILES.get('tumb_file',None)
        daily.diry = request.POST.get('diry',None)
        daily.diry_txt = request.POST.get('diry_txt',None)
        daily.diry_file = request.FILES.get('diry_file',None)
        daily.yt = request.POST.get('yt',None)
        daily.yt_txt = request.POST.get('yt_txt',None)
        daily.yt_file = request.FILES.get('yt_file',None)
        daily.qra = request.POST.get('qra',None)
        daily.qra_txt = request.POST.get('qra_txt',None)
        daily.qra_file = request.FILES.get('qra_file',None)
        daily.sbms = request.POST.get('sbms',None)
        daily.sbms_txt = request.POST.get('sbms_txt',None)
        daily.sbms_file = request.FILES.get('sbms_file',None)

        daily.pr = request.POST.get('pr',None)
        daily.pr_txt = request.POST.get('pr_txt',None)
        daily.pr_file = request.FILES.get('pr_file',None)
        daily.art = request.POST.get('art',None)
        daily.art_txt = request.POST.get('art_txt',None)
        daily.art_file = request.FILES.get('art_file',None)
        daily.blg = request.POST.get('blg',None)
        daily.blg_txt = request.POST.get('blg_txt',None)
        daily.blg_file = request.FILES.get('blg_file',None)
        daily.clss = request.POST.get('cls',None)
        daily.clss_txt = request.POST.get('cls_txt',None)
        daily.clss_file = request.FILES.get('cls_file',None)
        daily.gst = request.POST.get('gst',None)
        daily.gst_txt = request.POST.get('gst_txt',None)
        daily.gst_file = request.FILES.get('gst_file',None)
        daily.bk = request.POST.get('bk',None)
        daily.bk_txt = request.POST.get('bk_txt',None)
        daily.bk_file = request.FILES.get('bk_file',None)
        
        dct_file = dict(request.FILES)
        lst_screenshot = dct_file['filed']
        lst_file = []
        for ins_screenshot in lst_screenshot:
            str_img_path = ""
            if ins_screenshot:
                img_emp = ins_screenshot
                fs = FileSystemStorage(location=settings.MEDIA_ROOT,base_url=settings.MEDIA_URL)
                str_img = fs.save(''.join(filter(str.isalnum, str(img_emp))), img_emp)
                str_img_path = fs.url(''.join(filter(str.isalnum, str_img)))
                lst_file.append('/media/'+''.join(filter(str.isalnum, str(img_emp))))
                daily.json_testerscreenshot = lst_file
        daily.work=work
        daily.user=usr
        daily.cl_name=work.cl_name
        daily.save() 
        dl = daily_work.objects.get(id=daily.id)
        
        sub_lb =request.POST.getlist('sub_lb[]') 
        sub_txt =request.POST.getlist('sub_txt[]')
        sub_file =request.FILES.getlist('sub_file[]')
        
        if len(sub_lb)==len(sub_txt)==len(sub_file):
            mapped2 = zip(sub_lb,sub_txt,sub_file)
            mapped2=list(mapped2)
            for ele in mapped2:
               
                created = daily_work_sub.objects.get_or_create(sub=ele[0],sub_txt=ele[1],sub_file=ele[2],daily=dl)
                    
        off_sub_lb =request.POST.getlist('off_sub_lb[]') 
        off_sub_txt =request.POST.getlist('off_sub_txt[]')
        off_sub_file =request.FILES.getlist('off_sub_file[]')
        
        if len(off_sub_lb)==len(off_sub_txt)==len(off_sub_file):
            mapped2 = zip(off_sub_lb,off_sub_txt,off_sub_file)
            mapped2=list(mapped2)
            for ele in mapped2:
               
                created = daily_off_sub.objects.get_or_create(sub=ele[0],sub_txt=ele[1],sub_file=ele[2],daily=dl)

        return redirect("ex_daily_work_det",work.client_name_id)
    return redirect("ex_daily_work_det",work.client_name_id)

def ex_weekly_rep_clint(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    work_as=work_asign.objects.filter(exe_name=ids).values('client_name_id').distinct()
    work=Work.objects.filter()
    last=work_asign.objects.filter(exe_name=ids).last()
    cl=client_information.objects.all()
    context={
        "usr":usr,
        "work_as":work_as,
        "work":work,
        "cl":cl,
        "last":last
    }
    return render(request, 'executive/ex_weekly_rep_clint.html',context)

def ex_weekly_rep_clint_det(request,id):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    work_as=work_asign.objects.filter(exe_name=ids)
   
    work_tb=Work.objects.filter(client_name_id=id).order_by("-id")
    rep=progress_report.objects.filter(user=usr)
    context={
        "usr":usr,
        "work_as":work_as,
      
        "rep":rep,
        "work_tb":work_tb
    }
    return render(request, 'executive/ex_weekly_rep_det.html',context)

def sv_wk_rp(request,id):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    
    work=Work.objects.get(id=id)
    if request.method == 'POST':
        pro = progress_report()
        pro.task=work.task
        pro.audit_rprt=request.FILES.get('repr_fl',None)
        pro.graph=request.FILES.get('gr_fl',None)
        pro.start_date=request.POST.get('st_dt',None)
        pro.end_date=request.POST.get('ed_dt',None)
        pro.work=work
        pro.user=usr
        pro.cl_name=work.cl_name
        pro.save()
        return redirect("ex_weekly_rep_clint_det",work.client_name_id)
    return redirect("ex_weekly_rep_clint_det",work.client_name_id)

def ex_view_work_clint(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    
    work_as=work_asign.objects.filter(exe_name=ids)
    work=Work.objects.all()
    cl=client_information.objects.all()
    last=work_asign.objects.filter(exe_name=ids).last()
    
    
    
    context={
        "usr":usr,
        "work":work,
        "work_as":work_as,
        "cl":cl,
        "last":last,
    }
    return render(request, 'executive/ex_view_work_clint.html',context)

def ex_view_clint_det(request,id):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    
    work=Work.objects.get(id=id)
    context={
        "usr":usr, 
        "client":work
    }
    return render(request, 'executive/ex_view_clint_det.html',context)

def ex_warnings_dash(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    context={
        "usr":usr
    }
    return render(request, 'executive/ex_warnings_dash.html',context) 


def ex_warning(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)

    warn=Warning.objects.filter(executive=ids,type="Warning")
    context={
        "usr":usr,
        "warn":warn
    }
    return render(request, 'executive/ex_warning.html',context)

def add_warning(request, id):
   

    if request.method == 'POST':
        warn = Warning.objects.get(id=id)
        warn.reply=request.POST.get('workdone',None)
        warn.save()
        return redirect("ex_warning")
    return redirect("ex_warning")
    
def ex_suggestions(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    warn=Warning.objects.filter(executive=ids,type="Suggestion")
    context={
        "usr":usr,
        "warn":warn
    }
    return render(request, 'executive/ex_suggestions.html',context)

def add_suggestion(request, id):
   

    if request.method == 'POST':
        warn = Warning.objects.get(id=id)
        warn.reply=request.POST.get('workdone',None)
        warn.save()
        return redirect("ex_warning")
    return redirect("ex_warning")


    
def get_warns(request):
    ele = request.GET.get('ele')
    warn = Warning.objects.get(id=ele)
    warns =warn.description
    rep =warn.reply
 
    return JsonResponse({"status":" not","warns":warns,"rep":rep})

    
def get_requ(request):
    ele = request.GET.get('ele')
    warn = addi_client_info.objects.get(id=ele)
    warns =warn.discription
    rep =warn.file
    nm =warn.labels
    vk=str(rep)
    
    return JsonResponse({"status":" not","warns":warns,"rep":vk,"nm":nm})


def logout(request):
    if 'userid' in request.session:  
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/') 


def ex_change_pass(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    if request.session.has_key('userid'):
        devid = request.session['userid']
    else:
        return redirect('/')

    dev = user_registration.objects.filter(id=devid)

    if request.method == 'POST':
        abc = user_registration.objects.get(id=devid)
        cur = abc.password
        oldps = request.POST["currentPassword"]
        newps = request.POST["newPassword"]
        cmps = request.POST["confirmPassword"]
        if oldps == cur:
            if oldps != newps:
                if newps == cmps:
                    abc.password = request.POST.get('confirmPassword')
                    abc.save()
                    return render(request, 'executive/ex_ch_pass.html', {'dev': dev,"usr":usr})
            elif oldps == newps:
                messages.add_message(request, messages.INFO, 'Current and New password same')
            else:
                messages.info(request, 'Incorrect password same')

            return render(request, 'executive/ex_ch_pass.html', {'dev': dev,"usr":usr})
        else:
            messages.add_message(request, messages.INFO, 'old password wrong')
            return render(request, 'executive/ex_ch_pass.html', {'dev': dev,"usr":usr})
    return render(request, 'executive/ex_ch_pass.html', {'dev': dev,"usr":usr})

def ex_accountset(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    if request.session.has_key('userid'):
        devid = request.session['userid']
    else:
        return redirect('/')
    dev = user_registration.objects.filter(id=devid)
    return render(request, 'executive/ex_accountset.html', {'dev': dev,"usr":usr})

def ex_imagechange(request, id):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    if request.session.has_key('userid'):
        devid = request.session['userid']
    else:
        return redirect('/')
    dev = user_registration.objects.filter(id=devid)
    if request.method == 'POST':
        abc = user_registration.objects.get(id=id)
        abc.photo = request.FILES['filename']
        
        abc.save()
        return redirect('ex_accountset')
    return render(request, 'executive/ex_accountset.html',{'dev': dev,"usr":usr})

#---------------------------------marketing section

    

def he_profile(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    return render(request, 'head/he_profile.html',{"usr":usr})

def he_project(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    return render(request,'head/he_project.html',{"usr":usr})

def he_view_works(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    client=client_information.objects.all()
    return render(request,'head/he_view_works.html',{'client':client,"usr":usr,})

def he_work_asign(request,pk):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    client=client_information.objects.get(id=pk)
    exe=user_registration.objects.filter(department='Digital Marketing Executive')
    return render(request,'head/he_work_asign.html',{'client':client,'exe':exe,"usr":usr,})

def he_view_work_asign_client(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    client=client_information.objects.all()
    return render(request,'head/he_view_work_asign_client.html',{'client':client,"usr":usr,})

def he_view_work_asign_exe(request,id):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    client=client_information.objects.get(id=id)
    work=work_asign.objects.filter(client_name=client.id)
    return render(request,'head/he_view_work_asign_exe.html',{"usr":usr,"w":work})



def he_daily_task(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    today=date.today()
    work=daily_work.objects.filter(date=today)
    return render(request,'head/he_daily_task.html',{'work':work,"usr":usr,})

def he_workprogress_executive(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    prgs=progress_report.objects.all()
    return render(request,'head/he_workprogress_executive.html',{'prgs':prgs,"usr":usr,})

def he_progress_report(request,pk):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    work=progress_report.objects.get(id=pk)
    try:
        prv_work=progress_report.objects.filter(work_id=work.id).order_by('-end_date')[0]
    except:
        prv_work=None
    return render(request,'head/he_progress_report.html',{'work':work,"usr":usr,"prv_work":prv_work})


def he_feedback(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    exe=user_registration.objects.filter(department="Digital Marketing Executive")
    return render(request,'head/he_feedback.html',{'exe':exe,"usr":usr,})


def he_feedbacke1(request,pk):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    exe=user_registration.objects.get(id=pk)
    wrng=Warning.objects.filter(executive_id=exe.id)
    return render(request,'head/he_feedback1.html',{'exe':exe,'wrng':wrng,"usr":usr,})

    
def he_feedback_submit(request,pk):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    if request.method=='POST':
        des=request.POST['des']
        typ=request.POST['option']
        warning=Warning(executive_id=pk,description=des,type=typ,)
        warning.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
def he_work_add(request,id):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    if request.method == 'POST':
        task = request.POST.get('task')
        des = request.POST.get('des')
        sdate=request.POST.get('sdate')
        edate=request.POST.get('edate')
        file=request.FILES.get('file')
        sub_tsk = request.POST.get('sub_tsk')
        client=client_information.objects.get(id=id)
        json_data = request.POST.get('array', '')
        array = json.loads(json_data)
        w=Work(task=task,description=des,start_date=sdate,end_date=edate,file_attached=file,cl_name=client.bs_name,client_name=client)
        w.save()

        if w.task=="SEO":
            w.file_2=client.seo_file
            w.save()
            if sub_tsk=="On page":
                w.sub_task="On page"
                w.sub_des=client.on_pg_txt
                w.sub_file=client.on_pg_file
                w.save()
            if sub_tsk=="Off page":
                w.sub_task="Off page"
                w.sub_des=client.off_pg_txt
                w.sub_file=client.off_pg_file
                w.save()

        if w.task=="SMM":
            w.file_2=client.smm_file
            w.save()
        if w.task=="SEM/PPC":
            w.file_2=client.sem_file
            w.save()
        if w.task=="Email Marketing":
            w.file_2=client.em_file
            w.save()   
        if w.task=="Content Marketing":
            w.file_2=client.cm_file
            w.save() 
        if w.task=="Affiliate Marketing":
            w.file_2=client.am_file
            w.save()   
        if w.task=="Mobile marketing":
            w.file_2=client.mm_file
            w.save()  
        if w.task=="Video Marketing":
            w.file_2=client.vm_file
            w.save() 
        if w.task=="SMO":
            w.file_2=client.smo_file
            w.save()     
        w=Work.objects.latest('id')
        for i in array:
            b=user_registration.objects.get(department="Digital Marketing Executive",fullname=i)
            c=work_asign(work_id=w.id,exe_name_id=b.id,client_name_id=client.id)
            c.save()
        return HttpResponse({"message": "success"})

            
    
def he_change_pass(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    if request.session.has_key('userid'):
        devid = request.session['userid']
    else:
        return redirect('/')
    dev = user_registration.objects.filter(id=devid)

    if request.method == 'POST':
        abc = user_registration.objects.get(id=devid)
        cur = abc.password
        oldps = request.POST["currentPassword"]
        newps = request.POST["newPassword"]
        cmps = request.POST["confirmPassword"]
        if oldps == cur:
            if oldps != newps:
                if newps == cmps:
                    abc.password = request.POST.get('confirmPassword')
                    abc.save()
                    return render(request, 'head/he_ch_pass.html', {'dev': dev,"usr":usr})
            elif oldps == newps:
                messages.add_message(request, messages.INFO, 'Current and New password same')
            else:
                messages.info(request, 'Incorrect password same')

            return render(request, 'head/he_ch_pass.html', {'dev': dev,"usr":usr})
        else:
            messages.add_message(request, messages.INFO, 'old password wrong')
            return render(request, 'head/he_ch_pass.html', {'dev': dev,"usr":usr})
    return render(request, 'head/he_ch_pass.html', {'dev': dev,"usr":usr})


def he_accountset(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    if request.session.has_key('userid'):
        devid = request.session['userid']
    else:
        return redirect('/')
    dev = user_registration.objects.filter(id=devid)
    return render(request, 'head/he_accountset.html', {'dev': dev,"usr":usr})

def he_imagechange(request, id):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    if request.session.has_key('userid'):
        devid = request.session['userid']
    else:
        return redirect('/')
    dev = user_registration.objects.filter(id=devid)
    if request.method == 'POST':
        abc = user_registration.objects.get(id=id)
        abc.photo = request.FILES['filename']
        abc.save()
        return redirect('he_accountset')
    return render(request, 'head/he_accountset.html',{'dev': dev,"usr":usr})


def he_flt_progress(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    st_dt=request.POST.get('str_dt')
    en_dt=request.POST.get('end_dt')
    print(en_dt)
    pr_work=progress_report.objects.filter(start_date__gte=st_dt,start_date__lte=en_dt)
    context={
        "usr":usr,
        "prgs":pr_work

    }
    return render(request, 'head/he_workprogress_executive.html',context)

#-------------------------------------------------------------------------------Smo Submission
def smo_base(request):
    ids=request.session['smo_userid']
    usr = smo_registration.objects.get(id=ids)
   
    

    context={
        "usr":usr,
      
    }
    return render(request, 'smo/publishing/smo_base.html',context)

def smo_login(request,id):
    work=Work.objects.get(id=id)
    return render(request, 'smo/index/smo_login.html', {'id':work.client_name_id})

def smo_signup(request,id):
    return render(request, 'smo/index/smo_signup.html', {'id':id})



def smo_reg(request,id):

 
    a = smo_registration()
    
    
    
    client=client_information.objects.get(id=id)
    if request.method == 'POST':
        if  smo_registration.objects.filter(email=request.POST['email']).exists():
            
            msg_error = "Mail id already exist"
            return render(request, 'smo/index/smo_signup.html',{'msg_error': msg_error})
        else:
            if request.POST['password'] == request.POST['re_password']:
                a.fullname = request.POST['fname']
                a.email = request.POST['email']
                a.password = request.POST['password']
                a.photo = request.FILES['photo']
                a.client=client
                a.save()
                return redirect('smo_login',id)
            else:
                msg_error = "Mail id already exist"
                return render(request, 'smo/index/smo_signup.html',{'msg_error': msg_error, "id": id})

def smo_signin(request,id):  
    if request.method == 'POST':
        email  = request.POST['email']
        password = request.POST['password']
        
        if smo_registration.objects.filter(email=request.POST['email'], password=request.POST['password']).exists():
            smo_ex = smo_registration.objects.get(email=request.POST['email'],password=request.POST['password'])

            #---------------------- executive session id
            ids=request.session['userid']
            usr = user_registration.objects.get(id=ids)
            request.session['userid'] = usr.id
            #---------------------- smo submission login session id
            request.session['smo_userid'] = smo_ex.id
            
            return redirect('smo_dash')
    return redirect('smo_login',id) 

def smo_dash(request):
    ids=request.session['smo_userid']
    usr = smo_registration.objects.get(id=ids)
    context={
            "usr":usr,
        }
    return render(request, 'smo/publishing/smo_dashboard.html',context)

def smo_cnt_chnl(request):
    ids=request.session['smo_userid']
    usr = smo_registration.objects.get(id=ids)
    context={
            "usr":usr,
        }
    return render(request, 'smo/publishing/connect_channel.html',context) 


def published_post(request):
    ids=request.session['smo_userid']
    usr = smo_registration.objects.get(id=ids)
    context={
            "usr":usr,
        }
    return render(request, 'smo/publishing/published_post.html',context)


def create_post(request):
    ids=request.session['smo_userid']
    usr = smo_registration.objects.get(id=ids) 
    post = smo_post.objects.filter(smo=usr)
    context={
            "usr":usr,
            "post":post
        }
    return render(request, 'smo/publishing/create_post.html',context)


def edit_post_drft(request,id):
    if request.method == 'POST':
        ids=request.session['smo_userid']
        usr = smo_registration.objects.get(id=ids)
        b=smo_post.objects.get(id=id)
        b.description = request.POST['description']
        dct_file = dict(request.FILES)
        try:
            lst_screenshot = dct_file['filed']
            lst_file = []
            for ins_screenshot in lst_screenshot:
                str_img_path = ""
                if ins_screenshot:
                    img_emp = ins_screenshot
                    fs = FileSystemStorage(location=settings.MEDIA_ROOT,base_url=settings.MEDIA_URL)
                    str_img = fs.save(''.join(filter(str.isalnum, str(img_emp))), img_emp)
                    str_img_path = fs.url(''.join(filter(str.isalnum, str_img)))
                    lst_file.append('/media/'+''.join(filter(str.isalnum, str(img_emp))))
                    b.json_testerscreenshot = lst_file
        except:
            b.json_testerscreenshot=b.json_testerscreenshot
        b.smo=usr
        b.status="save"
        b.save()
        return redirect('create_post')

    return redirect('create_post')


def save_post_drft(request):
    print("sffdfsfds")
    if request.method == 'POST':

        ids=request.session['smo_userid']
        usr = smo_registration.objects.get(id=ids)
        b=smo_post()
        b.description = request.POST['description']
        dct_file = dict(request.FILES)
        if dct_file['filed'] == None:
            lst_screenshot = dct_file['filed']
            lst_file = []
            for ins_screenshot in lst_screenshot:
                str_img_path = ""
                if ins_screenshot:
                    img_emp = ins_screenshot
                    fs = FileSystemStorage(location=settings.MEDIA_ROOT,base_url=settings.MEDIA_URL)
                    str_img = fs.save(''.join(filter(str.isalnum, str(img_emp))), img_emp)
                    str_img_path = fs.url(''.join(filter(str.isalnum, str_img)))
                    lst_file.append('/media/'+''.join(filter(str.isalnum, str(img_emp))))
                    b.json_testerscreenshot = lst_file
        b.json_testerscreenshot=b.json_testerscreenshot
        b.smo=usr
        b.status="draft"
        b.save()
        return redirect('create_post')
    return redirect('create_post')



    
def content(request):
    ids=request.session['smo_userid']
    usr = smo_registration.objects.get(id=ids) 
    post = smo_post.objects.filter(smo=usr)
    context={
            "usr":usr,
            "post":post
        }
    return render(request, 'smo/publishing/content.html',context)

#dfjhsggggggggggggggggggggggggggggggggggggggggggggggggggggggg
import facebook

def login_with_facebook(request):
    # Redirect the user to the Facebook login page
    redirect_uri = request.build_absolute_uri(reverse('facebook_login_callback'))
    login_url = 'https://www.facebook.com/v12.0/dialog/oauth?client_id={}&redirect_uri={}&scope={}'.format(
        settings.FACEBOOK_APP_ID,
        redirect_uri,
        ','.join(settings.FACEBOOK_PERMISSIONS),
    )
    return redirect(login_url)

def facebook_login_callback(request):
    # Exchange the authorization code for an access token
    code = request.GET.get('code')
    redirect_uri = request.build_absolute_uri(reverse('facebook_login_callback'))
    access_token_url = 'https://graph.facebook.com/v12.0/oauth/access_token?client_id={}&redirect_uri={}&client_secret={}&code={}'.format(
        settings.FACEBOOK_APP_ID,
        redirect_uri,
        settings.FACEBOOK_APP_SECRET,
        code,
    )
    response = requests.get(access_token_url)
    data = response.json()
    access_token = data.get('access_token')
    
    # Store the access token in the user's session
    request.session['access_token'] = access_token
    
    # Redirect the user to the home page or a success page
    return redirect('post_on_facebook')


def post_on_facebook(request):
    if request.method == 'POST':
        # Get the post message from the form
        message = request.POST.get('message')
        
        # Initialize the Facebook Graph API with the user's access token
        graph = facebook.GraphAPI(access_token=request.session['access_token'])
        
        # Publish the post on the user's Facebook account
        graph.put_object(parent_object='me', connection_name='feed', message=message)
        
        # Redirect to the home page or a success page
        return redirect('home')
    
    # If the request is not POST, render the form
    return render(request, 'post_form.html')

@require_GET
def preview(request):
    print("sdffddf")
    content = request.GET.get("content", "")
    preview = generate_linkedin_preview(content) # Replace this with your own function that generates the LinkedIn post preview
    return JsonResponse({"content": preview})


import requests
import json

def generate_linkedin_preview(content):
    # Get the access token for the authenticated user
    access_token = get_linkedin_access_token(content)

    # Create a draft post with the given content
    post_data = {
        "author": "urn:li:person:{user_id}",
        "lifecycleState": "DRAFT",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                }
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    create_post_response = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers=headers,
        data=json.dumps(post_data)
    )
    create_post_response_data = create_post_response.json()
    post_urn = create_post_response_data.get("id")

    # Generate a preview of the post
    preview_data = {
        "content": {
            "contentEntities": [
                {
                    "entityLocation": f"urn:li:ugcPost:{post_urn}",
                    "thumbnails": [
                        {
                            "resolvedUrl": settings.STATIC_URL + "images/linkedin-preview.png"
                        }
                    ]
                }
            ],
            "title": {
                "text": "LinkedIn Post Preview"
            }
        },
        "registerUploadRequest": {
            "recipes": [
                "urn:li:digitalmediaRecipe:feedshare-image"
            ],
            "supportedMimeTypes": [
                "image/jpeg",
                "image/png"
            ],
            "lifetime": {
                "durationInSeconds": 86400
            },
            "mediaType": "STILLIMAGE"
        },
        "shareMediaCategory": "NONE"
    }
    preview_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    generate_preview_response = requests.post(
        f"https://api.linkedin.com/v2/ugcPosts/{post_urn}/preview",
        headers=preview_headers,
        data=json.dumps(preview_data)
    )
    generate_preview_response_data = generate_preview_response.json()
    preview_html = generate_preview_response_data.get("data", {}).get("com.linkedin.common.VectorImage", {}).get("html")
    return preview_html


def get_linkedin_access_token(request):
 
    if isinstance(request, str):
        # If a string is passed, assume it's the redirect URI and return the authorization URL
        redirect_uri = request
        authorization_url = f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={settings.LINKEDIN_CLIENT_ID}&redirect_uri={redirect_uri}&state=xyz&scope=r_liteprofile%20w_member_social%20r_emailaddress%20w_organization_social"
        return HttpResponseRedirect(authorization_url)

    # Check if the access token is already stored in the user's session
    access_token = request.session.get('linkedin_access_token')
    if access_token:
        return access_token

    # If the access token is not in the session, redirect the user to the LinkedIn OAuth 2.0 authorization page
    redirect_uri = f"{settings.BASE_URL}/linkedin/callback"
    authorization_url = f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={settings.LINKEDIN_CLIENT_ID}&redirect_uri={redirect_uri}&state=xyz&scope=r_liteprofile%20w_member_social%20r_emailaddress%20w_organization_social"
    return HttpResponseRedirect(authorization_url)


from django.shortcuts import render, redirect
import requests

def post_to_linkedin(request):
    # Get the user's access token from the session
    access_token = request.session.get('linkedin_access_token')

    # Set the parameters for the post request

    print(access_token)
    headers = {'Authorization': f'Bearer {access_token}',
               'Content-Type': 'application/json'}
    data = {'author': f"urn:li:person:{request.user.linkedin_id}",
            'lifecycleState': 'PUBLISHED',
            'specificContent': {
                'com.linkedin.ugc.ShareContent': {
                    'shareCommentary': {
                        'text': 'Hello, world!'
                    },
                    'shareMediaCategory': 'NONE'
                }
            },
            'visibility': {
                'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
            }
           }

    # Send the post request to the LinkedIn API
    response = requests.post('https://api.linkedin.com/v2/ugcPosts', headers=headers, json=data)

    # Redirect the user back to the homepage
    return redirect('published_post')



