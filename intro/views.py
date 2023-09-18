from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from intro.models import MyUser,boardobject
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.contrib.auth.tokens import default_token_generator
from .tokens import account_activation_token
from django.core.mail import send_mail,BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User , auth
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.conf import settings
import django
import  datetime

from rest_framework import generics
from intro.serializers import boardSerializer
from django.db.models.query_utils import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
import uuid
from django.contrib.auth.password_validation import validate_password 
import random
import  json
def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

# Create your views here.
@login_required
def current_user(request):
    user = request.user
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        
    }
    return JsonResponse(user_data)
@api_view(('POST',))
def indexapi(request):
    

    

    if request.method=='POST':
        print(request.data)
        task=request.data
        try:
            queryset = boardobject.objects.filter(**task)
            result= boardSerializer(queryset,many=True)
            if result.data:
           
                 return Response({'status':'true','data':result.data})
            else:
                 return Response({'status':'false'})
        except Exception as e :
            print(e)
            
            return Response({'status':'false'})
    return Response({'status':'hello','demo':'hello'})
@csrf_exempt
def login(request):
    if request.user.is_authenticated:
        return redirect("/index/")
    status={"task":"logout"}
    if(request.method=='POST'):
        EMAIL=request.POST.get('username')
        password=request.POST.get('p1')
        user = auth.authenticate(username=EMAIL,password=password)
        print(user)
        if  user  is  not None:
            auth.login(request,user)
            print('invalid User')
            status={'task':"logout"}
            return redirect("/index/",{"variable":"logout",})
        else:
             messages.warning(request, 'invaild password ')
    return render(request,'login.html',{"variable":"logout",})
@csrf_exempt
@login_required
def  logout(request):
    cache.clear()
        
    auth.logout(request)
    return redirect("/")
@csrf_exempt
def activate(request, uidb64, token):  
    User = request.user
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64)) 
        print(uid) 
        user = MyUser.objects.get(pk=uid)  
        
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and  account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        messages.success(request,'Thank you for your email confirmation. Now you can login your account.')  
        return redirect("/")
    else:  
        messages.success(request,'Activation link is invalid!')
        return redirect("/signup")  
@csrf_exempt
def build (request):
  if(request.method=='POST') :
        email=request.POST.get('email')
        username=request.POST.get('user_name')
        password=request.POST.get('p1')
        password1=request.POST.get('p2')
        phone=request.POST.get('number')
        print(phone)
        if (password1==password ):
            try:
                validate_password(password)
                try:
                     user= MyUser.objects.create_user(username=username,email=email,password=password , mobile_number =phone)
                     user.is_active = False
                     user.save()
                except:
                     mail= MyUser.objects.get(email=email)
                     if mail.is_active==False:
                          mail.delete() 
                          user= MyUser.objects.create_user(username=username,email=email,password=password , mobile_number =phone)
                          user.is_active = False
                          user.save()   
                current_site = get_current_site(request)  
                mail_subject = 'Activation link has been sent to your email id'  
                message = render_to_string('acc_active_email.html', {  
                    'user': user,  
                    'domain': current_site.domain,  
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                    'token':account_activation_token.make_token(user),  
                })  
                to_email = email  
                # email = send_mail(  
                #             mail_subject, message, to=[to_email]  
                # )  
                # email.send()  
                send_mail(mail_subject, message, settings.EMAIL_HOST_USER , [to_email], fail_silently=False)
                messages.success(request,['Profile Created Successfully 😍, Please Check Your Mail To Proceed Further!!'])
            except Exception as e:
                print(e,2)
                print(e)
                
                if isinstance(e, django.core.exceptions.ValidationError):  
                    
                    # for error in e :
                    messages.warning(request, list(e))
                else:
                     messages.warning(request, [str(e)])            
        else:
            messages.warning(request, ['Invalid Credentials 😓  Try Again !! '],)
  return render(request,'base.html')
@csrf_exempt
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = MyUser.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "email/password.txt"
					c = {
					"email":user.email,
					'domain':get_current_site(request),
					'site_name': 'Wazirs gst app',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'https',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
					except BadHeaderError:
						return redirect('/index/')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password_reset_form.html", context={"password_reset_form":password_reset_form})    
@login_required
@csrf_exempt
def meet(request):
     sobj= boardobject.objects.all()
     return  render(request,'layout.html',{'data':sobj})
@login_required
@csrf_exempt
def postmeet(request):
     if(request.method=='GET') and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        name = uuid.uuid4().hex[:8] 
        passcode =random. randint(110, 1000)
        boardobject.objects.create(head_user=request.user,sessioname=str(name),sessionpassword=str(passcode)).save()
        sobj= boardobject.objects.filter(head_user=request.user)
        datas=boardSerializer(sobj,many=True).data
        return JsonResponse(datas,safe=False)
     return  HttpResponse('done') 
@login_required
@csrf_exempt
def remove(request):
     if request.method=="POST" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
         
          boardobject.objects.get(id=int(request.POST.get('uid'))).delete()
          data = boardobject.objects.filter(head_user=request.user)
          datas=boardSerializer(data,many=True).data
          return JsonResponse(datas,safe=False)
     return HttpResponse('remove')
