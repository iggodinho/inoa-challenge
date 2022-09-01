from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
#from .models import User
#from .forms import UserForm, MyUserCreationForm
import requests


stockOptions=[
    {'id':1,'name':'Petrobras','code':'PETR4.SAO'},
    {'id':2,'name':'Microsoft','code':'MSFT34.SAO'},
    {'id':3,'name':'IBM','code':'IBMB34.SAO'},
    {'id':4,'name':'Apple','code':'AAPL34.SAO'},
    {'id':5,'name':'Netflix','code':'NFLX34.SAO'},
    {'id':6,'name':'Opera','code':'OPERA34.SAO'},
    {'id':7,'name':'Motorola','code':'M1SI34.SAO'},
    {'id':8,'name':'Unilever','code':'ULEV34.SAO'},
    {'id':9,'name':'Coca-Cola','code':'COCA34.SAO'},
    {'id':10,'name':'Smartfit','code':'SMFT3.SAO'},
    {'id':11,'name':'Bradesco','code':'BCIA11.SAO'},
    {'id':12,'name':'Nike','code':'NIKE34.SAO'},
    {'id':13,'name':'XP','code':'XPBR31.SAO'},
    {'id':14,'name':'Azul','code':'AZUL4.SAO'},
    {'id':15,'name':'Ambev','code':'ABEV3.SAO'},
    {'id':16,'name':'Magazine Luiza','code':'MGLU3.SAO'},
    {'id':17,'name':'Uber','code':'U1BE34.SAO'},
    {'id':18,'name':'Paramount','code':'C1BS34.SAO'},
    {'id':19,'name':'McDonalds','code':'MCDC34.SAO'},
    {'id':20,'name':'Gerdau','code':'GGBR3.SAO'},

    ]

key='WJJEOQROMVPXCG9X'




def home(request):
    return render(request, 'base/home/home.html', {'stockOptions':stockOptions})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in with {email}.")
                return redirect("base:home")
            else:
                messages.error(request,"Invalid email or password.")
        else:
            messages.error(request,"Invalid email or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="base/login/login.html", context={"login_form":form})
   
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            print(user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'base/register/register.html', {'form': form})

    
def selectedStock(request,pk):
    selectedStock=None
    for i in stockOptions:
        if i['code']==str(pk):
            selectedStock=i

    stockCode=selectedStock['code']
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+stockCode+'&apikey={key}' 
   
    r = requests.get(url)
    data = r.json()
    stockInfo={'info':selectedStock,'alpha':data['Global Quote']}
    newStockInfo={'symbol':stockInfo['alpha']['01. symbol'],
    'open':stockInfo['alpha']['02. open'],'high':stockInfo['alpha']['03. high'],'low':stockInfo['alpha']['04. low'],
    'price':stockInfo['alpha']['05. price'],'volume':stockInfo['alpha']['06. volume'],
    'latestTradingDay':stockInfo['alpha']['07. latest trading day'],'previousClose':stockInfo['alpha']['08. previous close'],
    'change':stockInfo['alpha']['09. change'],'changePercent':stockInfo['alpha']['10. change percent']}
    stockInfo["alpha"]=newStockInfo
    
    context={"selectedStock":stockInfo}
    return render(request, 'base/selected_stock/selectedstock.html',context)

