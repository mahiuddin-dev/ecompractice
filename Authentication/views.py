from django.views.generic import View
from django.shortcuts import render,redirect, HttpResponseRedirect
from validate_email import validate_email
from django.contrib.auth import authenticate, login,logout,get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator,PasswordResetTokenGenerator
from django.utils.encoding import DjangoUnicodeDecodeError, force_bytes,force_text
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib import messages
import threading



# Create your views here.

class EmailThread(threading.Thread):
    def __init__(self,email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)
    
    def run(self):
        self.email_message.send()


UserModel = get_user_model()

# Registration View
class RegistrationView(View):
    def get(self,request):
        return render(request,'account-create.html')
    

    def post(self,request):

        fname = request.POST.get('fname').title()
        lname = request.POST.get('lname').title()
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')

        context={
            'data':request.POST,
            'has_error': False
        }

        if not validate_email(email):
            context['msg'] = "Please provide a valid email address"
            context['color'] = 'alert-danger'
            context['has_error'] = True
        
        if password != confirmPassword:
            context['msg'] = "password don't match"
            context['color'] = 'alert-danger'
            context['has_error'] = True
        
        if User.objects.filter(email=email).exists():
            context['msg'] = "Email address already exists"
            context['color'] = 'alert-danger'
            context['has_error'] = True
        
        if context['has_error']:
            return render(request,'account-create.html',context)
        

        user = User.objects.create_user(username = email, email = email)
        user.set_password(password)
        user.is_active = False
        user.first_name = fname
        user.last_name = lname
        user.save()

        current_site = get_current_site(request)
        mail_subject = 'Verify your account'
        message = render_to_string('singUpToken.html', {
            'user': fname+" "+lname,
            'site': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user)
        })
        sent_email = EmailMessage(mail_subject,message, to=[email])

        EmailThread(sent_email).start()

        messages.info(request, 'Account created successfully. For verify your account please check your email')

        return redirect('Authentication:loginview')

# Account activate function
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user.is_active == False:
        if(user is not None and default_token_generator.check_token(user, token)):
            user.is_active = True
            user.save()
            messages.success(request, 'your account has been activated')
            
            current_site = get_current_site(request)
            mail_subject = 'Suessfully activated your account'
            message = render_to_string('Confirm.html', {
                'user': user.first_name+" "+user.last_name,
                'site': current_site,
            })
            sent_email = EmailMessage(mail_subject,message, to=[user.email])
            EmailThread(sent_email).start()

            return redirect('Authentication:loginview')

        else:
            messages.warning(request, 'Activation link is invalid')
            return redirect('Authentication:Registration')
    else:
        messages.info(request, 'This account already activated')
        return redirect('Authentication:loginview')

# Account Login views
class LoginView(View):
    def get(self,request):
        return render(request,'login.html')
    
    def post(self,request):
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            if request.GET.get('next', None):
                return HttpResponseRedirect(request.GET['next'])
            return redirect('Home:Home')
        else:
            context = {'email': username}
            messages.error(request, 'Invalid email or password')
            # return redirect('Authentication:loginview',)
            return render(request,'login.html', context)

# Account Logout views
class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('Home:Home')

# Acount update and password update
class AccountView(LoginRequiredMixin,View):

    def get(self,request):
        return render(request,'account-details.html')
    
    def post(self,request):
        user = request.user
        context = {}

        if request.method=='POST' and 'updateDetails' in request.POST:
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')            

            if user.first_name == fname and user.last_name == lname and user.email == email:
                pass
            elif user.is_authenticated:
                user.username = email
                user.first_name = fname
                user.last_name = lname

                if user.email == email:
                    pass
                else:
                    
                    pass

                user.save()

                context['msg'] = "Changed successfully"
                context['color'] = 'alert-success'

                mail_subject = 'Account information changed'
                message = 'Account information updated successfully. if you think this is wrong, please contact our support'
                sent_email = EmailMessage(mail_subject,message, to=[user.email])
                EmailThread(sent_email).start()
        
        # Password change 
        if request.method=='POST' and 'updatePassword' in request.POST:
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            check_password = user.check_password(current_password)

            if(check_password == True):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    context['msg'] = "Password changed successfully"
                    context['color'] = 'alert-success'

                    mail_subject = 'Password changed'
                    message = 'Your password has been changed successfully. if you think this is wrong, please contact our support'
                    sent_email = EmailMessage(mail_subject,message, to=[user.email])
                    EmailThread(sent_email).start()
                else:
                    context['msg'] = "Password does not match"
                    context['color'] = 'alert-danger'

            else:
                context['msg'] = "Incorrect current password"
                context['color'] = 'alert-danger'

        
        return render(request,'account-details.html', context)


class PasswordRestView(View):
    def get(self,request):
        return render(request,'password-reset.html')
    
    def post(self,request):
        email = request.POST.get('email')

        if not validate_email(email):
            messages.error(request, 'Invalid email')
            return redirect('Authentication:password-reset')

        user = User.objects.filter(email=email)
        
        if user.exists():

            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('resetToken.html', {
                'site': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0])
            })

            sent_email = EmailMessage(mail_subject,message, to=[email])

            EmailThread(sent_email).start()

            messages.success(request, 'You have sent you a email to reset your password')
            return render(request,'password-reset.html')
        else:
            messages.error(request, 'We can not find your email address')
            return redirect('Authentication:password-reset')


class SetnewPasswordView(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.error(request, 'Password reset again. This is invalid link')
                return redirect('Authentication:password-reset')

        except DjangoUnicodeDecodeError as identifiere:
            messages.error(request, 'Someting went wrong')
            
        return render(request,'new-password.html',context)

    def post(self,request,uidb64,token):
        context = {
            'uidb64': uidb64,
            'token': token,
            'has_error': False
        }
        password = request.POST.get('password')
        confirmPassword = request.POST.get('Confirmpassword')

        if password != confirmPassword:
            context['msg'] = "password don't match"
            context['color'] = 'alert-danger'
            context['has_error'] = True

        if len(password) < 6:
            context['msg'] = "Pasword shoud be at least 6 characters long"
            context['color'] = 'alert-danger'
            context['has_error'] = True

        if context['has_error']:
            return render(request,'new-password.html',context)

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            mail_subject = 'Password changed successfully'
            message = "Your password has been changed successfully. if you think you don't changed, please contact our support"
            sent_email = EmailMessage(mail_subject,message, to=[user.email])
            EmailThread(sent_email).start()
            messages.success(request, 'Password reset successfully')
            return redirect('Authentication:loginview')

        except DjangoUnicodeDecodeError as identifiere:
            messages.error(request, 'Someting went wrong')
            return render(request,'new-password.html')
