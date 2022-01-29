
from distutils.log import error
from django.urls import reverse
# Create your views here.
from django.http.response import HttpResponse
from django.shortcuts import render , redirect
from .models import *
from django.contrib.auth import authenticate , login , logout
from .forms import  RegistrationForm, AccountAuthenticationForm, AccountUpdateForm,nonRegisteredUseVoteForm
import datetime
from django.contrib.auth.admin import UserAdmin



def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('myProfile')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'evote/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')



def login_view(request):

    context = {}

    user = request.user
    if user.is_authenticated: 
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user: # bu user database de varsa login ol
                login(request, user)
               # return redirect(reverse("evote:myProfile",kwargs={'instance':str(user.id)}))
                return redirect("myProfile")  #burada da benim myProfile ın yanında user id'sini almam lazım ki o user in giriş yaptığını belirleyip oy kullanırken ona
                #göre işlem yaparım

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    # print(form)
    return render(request, "evote/login.html", context)

def account_view(request):

    if not request.user.is_authenticated:
            return redirect("login")

    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                    "email": request.POST['email'],
                    "username": request.POST['username'],
            }
            form.save()
            context['success_message'] = "Updated"
    else:
        form = AccountUpdateForm(

            initial={
                    "email": request.user.email, 
                    "username": request.user.username,
                }
            )

    context['account_form'] = form

    

    return render(request, "account/account.html", context)


# Create your views here.
def usevote(request , pk):
    if not request.user.is_authenticated:
        return redirect("pagefailed")
  	
    
    vote = Vote.objects.get(v_code = pk)
    
    candidates = vote.candidates_set.all()
    context = {'candidates':candidates , 'vote':vote}
    if request.method == 'POST':
        if request.POST.get('coursename'):
            savedata = Stat()
            savedata.value = request.POST.get('coursename')
            savedata.which_vote = request.POST.get('votename')
            savedata.l_date = request.POST.get('votedate')
            savedata.who_voted = request.POST.get('whovoted')
            savedata.save()
            return redirect('myProfile')
       
    else:        
        return render(request, 'evote/usevote.html' , context)



def viewStats(request , pk): 

    if not request.user.is_authenticated: #kayıtlı olmayanlar göremez.
        return redirect("pagefailed")

    




    vote = Vote.objects.filter(v_code = pk) 
    stat = Stat.objects.filter(which_vote = pk) #2023 seçimlerinin tüm oylarını aldık
    candidate = Candidates.objects.filter(which_vote = pk) #election2023 ün bütün candidatelerini alıyorum
    stat_counts = [] #bu arrayin içine candidate sayılarını ekleyeceğim yani akp 10 oy chp 5 oy hdp 0 oy vs
    for c in candidate:# bütün candidatelerin sayısı alındığında döngü bitecek
        a =  stat.filter(value = c.c_name).count() #seçimde değeri akp , chp , mhp ye eşit olan statlerin sayısını al
        stat_counts.append(a)#bu değerleri arraye ekle

    lastdate = vote.values('l_date') #bu bana dictionary döndürüyor  <QuerySet [{'l_date': datetime.date(2022, 1, 8)}]>
    v2 = lastdate[0]['l_date']
    
    if(datetime.date.today() < v2):  #oylama daha bitmediyse sonucu gösterme.
        return HttpResponse("Voting is not done yet so you can not view current statistics")
    
    context = {'stat':stat , 'candidate':candidate , 'stat_counts':stat_counts , 'vote':vote}
    return render(request,'evote/viewStats.html',context)


def adminviewStats(request , pk): 
    vote = Vote.objects.filter(v_code = pk) 
    stat = Stat.objects.filter(which_vote = pk) #2023 seçimlerinin tüm oylarını aldık
    candidate = Candidates.objects.filter(which_vote = pk) #election2023 ün bütün candidatelerini alıyorum
    stat_counts = [] #bu arrayin içine candidate sayılarını ekleyeceğim yani akp 10 oy chp 5 oy hdp 0 oy vs
    for c in candidate:# bütün candidatelerin sayısı alındığında döngü bitecek
        a =  stat.filter(value = c.c_name).count() #seçimde değeri akp , chp , mhp ye eşit olan statlerin sayısını al
        stat_counts.append(a)#bu değerleri arraye ekle

    

    context = {'stat':stat , 'candidate':candidate , 'stat_counts':stat_counts , 'vote':vote}
    return render(request,'evote/adminviewstats.html',context)

def myProfile(request): 

    if not request.user.is_authenticated:
        return redirect("pagefailed")

    vote = Vote.objects.all()
    
    stat = Stat.objects.filter(who_voted = request.user.username)
    context = {'vote':vote , 'stat':stat}
    return render(request,'evote/myProfile.html' , context)

def home(request):
    return render(request, 'evote/home.html')


def adminlogin(request):

    context = {}

    user = request.user
    if user.is_authenticated: 
        return redirect("adminmenu")

    if request.POST:
        
            form = AccountAuthenticationForm(request.POST)
            if form.is_valid():
               
                 email = request.POST['email']
                 password = request.POST['password']
                 #if user.is_superuser:
            user = authenticate(email=email, password=password)
            if user.is_superuser:
            # if request.user.is_superuser: # bu user database de varsa login ol
              
                login(request,user)
               # return redirect(reverse("evote:myProfile",kwargs={'instance':str(user.id)}))
                return redirect("adminmenu")  
            else:
                
                raise forms.ValidationError("Invalid login")
    else:
        form = AccountAuthenticationForm()

    context['adminlogin_form'] = form

    # print(form)
    return render(request, "evote/adminlogin.html", context)

   # return render(request, 'evote/adminlogin.html')


def adminlogout_view(request):
    logout(request)
    return redirect('adminlogin')

def adminmenu(request):
    return render(request, 'evote/adminmenu.html')

def premiumpage(request,username):
    if not request.user.is_authenticated:
        return redirect("pagefailed")

    if request.method=="POST":
        user = Account.objects.get(username=username)
        user.is_premiumuser=True
        user.save()
        print("Premium oldum olley")
        print(user.is_premiumuser)
        return redirect('home')
    return render(request, 'evote/premiumpage.html')

def adminseeelection(request):
    vote = Vote.objects.all()
    context = {'vote':vote}
    return render(request, 'evote/adminseeelection.html',context)


def adminaccounts(request):
    accounts = Account.objects.all()
    context = {'accounts':accounts}
    return render(request, 'evote/adminaccounts.html' , context)

def admincreateelection(request):


    

    return render(request, 'evote/admincreateelection.html')

def pagefailed_view(request):
    return render(request,'evote/pagefailed.html')

def admincancel(request):
    return render(request, 'evote/admincancel.html')

def usevote_nonregistered(request):
    form = nonRegisteredUseVoteForm()
    if request.method == 'POST':
        form = nonRegisteredUseVoteForm(request.POST)
        if form.is_valid():
            messages.success(request , "Successfully entered")
            #Non-registered user should go to myprofile page
            #to vote or go a new page in which there are votes
            #vote kodunu doğru girdiyse kullanıcının direk o oya gitmesi lazım
            #context = {'form':form}
            return redirect('home')
       
    context = {'form':form}    
    return render(request,'evote/usevote_nonregistered.html' ,context)