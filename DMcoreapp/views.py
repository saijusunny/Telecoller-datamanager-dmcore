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

from django.core.mail import send_mail

from django.core.files.storage import FileSystemStorage

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


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
            return redirect('hd_profile')

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
        client.smm = request.POST.get('smm',None)
        client.smm_txt = request.POST.get('smm_txt',None)
        client.smm_file = request.FILES.get('smm_file',None)
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
        return redirect("ad_create_work")
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
        client.client_files = request.FILES.get('client_files',None)
        client.seo = request.POST.get('seo',None)
        client.seo_txt = request.POST.get('seo_txt',None)
        client.seo_file = request.FILES.get('seo_file',None)
        client.smm = request.POST.get('smm',None)
        client.smm_txt = request.POST.get('smm_txt',None)
        client.smm_file = request.FILES.get('smm_file',None)
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
        client = client_information.objects.get(id=id)
        print("id")
        print(id)

        
        client = client_information.objects.get(id=client.id)
        
        labels = request.POST.getlist('label[]')
        text =request.POST.getlist('dis[]')
        
        if len(labels)==len(text):
            mapped = zip(labels,text)
            mapped=list(mapped)
            for ele in mapped:

                try:
                    
                    adiclient = addi_client_info.objects.get(client=client)
                    print("haiii")
                 
                    if ((adiclient.labels==ele[0]) or (adiclient.text==ele[1])):
                        created = addi_client_info.objects.filter(client=client,labels=ele[0],discription=ele[1]).update(labels=ele[0],discription=ele[1])
                        print("true")
                    
                    elif ((adiclient.labels!=ele[0]) or (adiclient.text!=ele[1])):
                        created = addi_client_info.objects.get_or_create(labels=ele[0],discription=ele[1],user=usr,client=client,section='client_information')
                        print("false")
                    else:
                        pass
                        
                except:
                    created = addi_client_info.objects.get_or_create(labels=ele[0],discription=ele[1],user=usr,client=client,section='client_information')


            
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
                    adiclient=addi_client_info.objects.get(client=client)
                    if ((adiclient.labels==ele[0]) or (adiclient.text==ele[1])):
                        created = addi_client_info.objects.filter(client=client,labels=ele[0],discription=ele[1]).update(labels=ele[0],discription=ele[1])
                    elif ((adiclient.labels!=ele[0]) or (adiclient.text!=ele[1])):
                        created = addi_client_info.objects.get_or_create(labels=ele[0],discription=ele[1],client=client,user=usr,section='business_details')
                    else:
                        pass
                except:
                    created = addi_client_info.objects.get_or_create(labels=ele[0],discription=ele[1],client=client,user=usr,section='business_details')

        else: 
            pass
        

            for ele in mappeds:
            
                created = addi_client_info.objects.get_or_create(labels=ele[0],discription=ele[1],user=usr,client=client,section='business_details')
      
          

        
        files_req =request.FILES.getlist('file_add[]') 
        label_req =request.POST.getlist('label_req[]')
        dis_req =request.POST.getlist('dis_req[]')

        
        if len(files_req)==len(label_req)==len(dis_req):
            mapped2 = zip(label_req,dis_req,files_req)
            mapped2=list(mapped2)

            
        
            for ele in mapped2:
                try:
       
                    adiclient=addi_client_info.objects.get(client=client)
                    if ((adiclient.labels==ele[0]) or (adiclient.text==ele[1])):
                        created = addi_client_info.objects.filter(client=client,labels=ele[0],discription=ele[1]).update(labels=ele[0],discription=ele[1],file=ele[2])
                    elif ((adiclient.labels!=ele[0]) or (adiclient.text!=ele[1])):
                        created = addi_client_info.objects.get_or_create(labels=ele[0],discription=ele[1],file=ele[2],user=usr,client=client,section='Requirments')
                    else:
                        pass
                except:
                    created = addi_client_info.objects.get_or_create(labels=ele[0],discription=ele[1],file=ele[2],user=usr,client=client,section='Requirments')
        

            for ele in mapped2:
                created = addi_client_info.objects.get_or_create(labels=ele[0],discription=ele[1],file=ele[2],user=usr,client=client,section='Requirments')

        msg_success = "Save Successfully"
        return redirect('ad_view_clint',id)
    return redirect('ad_view_clint',id)




def ad_daily_work_det(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    dl_work=daily_work.objects.filter(date=date.today())
    context={
        "usr":usr,
        "dl_work":dl_work

    }
    return render(request, 'admin/ad_daily_work_det.html',context)


def ad_work_analiz_det(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)

    dl_work=daily_work.objects.all()
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



def ad_work_progress_det(request,id):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)

    pr_work=progress_report.objects.get(id=id)
    context={
        "usr":usr,
        "pr_work":pr_work

    }
    return render(request, 'admin/ad_work_progress_det.html',context) 

def ad_warning_ex(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)

    context={
        "usr":usr,

    }
    return render(request, 'admin/ad_warning_ex.html',context)

def ad_warning_sugg_dash(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)

    context={
        "usr":usr,

    }
    return render(request, 'admin/ad_warning_sugg_dash.html',context)

def ad_warning_det(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)

    context={
        "usr":usr,

    }
    return render(request, 'admin/ad_warning_det.html',context) 

def ad_suggestions_det(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)

    context={
        "usr":usr,

    }
    return render(request, 'admin/ad_suggestions_det.html',context)

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
    client=work_asign.objects.get(exe_name=ids)
    work=Work.objects.filter(id=client.work_id)
    context={
        "usr":usr,
        "client":work
    }
    return render(request, 'executive/ex_daily_work_clint.html',context)

def ex_daily_work_det(request,id):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    
    work_as=work_asign.objects.get(exe_name=ids)
    work=Work.objects.get(id=work_as.work_id)

    daily=daily_work.objects.filter(work_id =id)
    cr_date=date.today()
    context={
        "usr":usr,
        "work":work,
        "cr_date":cr_date,
        "daily":daily
    }
    return render(request, 'executive/ex_daily_work_det.html',context)

def daily_work_done(request,id):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    work_as=work_asign.objects.get(exe_name=ids)
    work=Work.objects.get(id=work_as.work_id)
    if request.method == 'POST':
        daily = daily_work()
        daily.task=work.task
        daily.date=date.today()
        daily.workdone =request.POST.get('workdone',None)
        daily.daily_file=request.FILES.get('filed',None)
        daily.work=work
        daily.user=usr
        daily.cl_name=work.cl_name
        daily.save()
        return redirect("ex_daily_work_det",id)
    return redirect("ex_daily_work_det",id)

def ex_weekly_rep_clint(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    client=work_asign.objects.get(exe_name=ids)
    work=Work.objects.filter(id=client.work_id)
    context={
        "usr":usr,
        "client":work
    }
    return render(request, 'executive/ex_weekly_rep_clint.html',context)

def ex_weekly_rep_clint_det(request,id):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)

    work=Work.objects.filter(id=id)
    works=Work.objects.get(id=id)
    rep=progress_report.objects.filter(user=ids)
    context={
        "usr":usr,
        "work":work,
        "rep":rep,
        "works":works
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
        return redirect("ex_weekly_rep_clint_det",id)
    return redirect("ex_weekly_rep_clint_det",id)

def ex_view_work_clint(request):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    
        
    work_as=work_asign.objects.get(exe_name=ids)
    work=Work.objects.filter(id=work_as.work_id)
    
    context={
        "usr":usr,
        "client":work
    }
    return render(request, 'executive/ex_view_work_clint.html',context)

def ex_view_clint_det(request,id):
    ids=request.session['userid']
    usr = user_registration.objects.get(id=ids)
    work_as=work_asign.objects.get(exe_name=ids)
    work=Work.objects.get(id=work_as.work_id)
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


    
