from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from authentification import settings

from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from .token import generatorToken


# Create your views here.

def home(request):
    return render(request, "app/index.html")

def register(request):
    if request.method == "POST":

        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if User.objects.filter(username=username):
            messages.error(request, 'ce nom est deja utilise')
            return redirect('register')

        if User.objects.filter(email=email):
            messages.error(request, "cette email possede un compte")
            return redirect('register')

        if not username.isalnum():
            messages.error(request, 'Le nom doir etre alphanumerique')
            return redirect('register')

        if password != password1:
            messages.error(request, 'les deux password ne coincide pas')
            return redirect('register')

        mon_utilisateur = User.objects.create_user(username, email, password)
        mon_utilisateur.first_name = firstname
        mon_utilisateur.last_name = lastname
        mon_utilisateur.is_active = False
        mon_utilisateur.save()
        messages.success(request, 'Votre compte a ete cree avec succes petit venar')

        #envoir email de bienvenu
        #subject = "Bienvenu sur donald pro django system login"
        #message = "Fait pas genre tu lis "+ mon_utilisateur.first_name+" tu sais tres bien que cest le logiciel qui te parle"
        #from_email = settings.EMAIL_HOST_USER
        #to_list = [mon_utilisateur.email]
        #send_mail(subject, message, from_email, to_list, fail_silently=False)

        #email de confirmation
        #current_site = get_current_site(request)
        #email_subject = "Confirmation de l'adresse email sur donald pro"
        #messageConfirm = render_to_string("emailconfirm.html", {
        #    "name": mon_utilisateur.first_name,
        #    'domain': current_site.domain,
        #    'uid':urlsafe_base64_encode(force_bytes(mon_utilisateur.pk)),
        #    'token':generatorToken.make_token(mon_utilisateur),

        #})

        #email = EmailMessage(
        #    email_subject,
        #    messageConfirm,
        #    settings.EMAIL_HOST_USER,
        #    [mon_utilisateur.email]
        #)

        #email.fail_silently = False
        #email.send()
        return redirect('login')

    return render(request, "app/register.html")



def logIn(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            my_user = User.objects.get(username=username)
        except:
            messages.error(request, "Erreur auth")
            return redirect('login')

        if user is not None:
            login(request, user)
            try:
                firstname = user.first_name
            except:
                firstname = "User"
            firstname = user.first_name
            return render(request, 'app/perso.html', {'firstname':firstname})
            return redirect('perso')

        #elif my_user.is_active == False:
        #    messages.error(request, 'You have not confirm your account before connection merci')

        else:
            print('else')
            messages.error(request, 'Mauvaise authentification ')
            return redirect('login')
    return render(request, 'app/login.html')






def logOut(request):
    logout(request)
    messages.success(request, 'Vous avez ete bien deconnecte')
    return redirect('home')
    pass
    return render(request, "app/logout.html")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generatorToken.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Votre compte a bien ete active felicitation connectez vous mtn")
        return redirect('login')

    else:
        messages.error(request, 'activation echoue !!')
        return redirect('home')



def Perso(request):
    Perso(request)
    messages.success(request, 'Vous avez ete bien dans votre espace Personnel')
    return redirect('perso')
    pass
    return render(request, "app/perso.html")