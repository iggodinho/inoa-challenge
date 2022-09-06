from django.shortcuts import render, redirect
from django.core.mail import send_mail
from base.models import Stock
from .forms import CreateUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
import requests

stock_options=[
    {'id':1,'name':'Gerdau','code':'GGB','image_file':'gerdau.png'},
    {'id':2,'name':'Microsoft','code':'MSFT','image_file':'microsoftt.png'},
    {'id':3,'name':'IBM','code':'IBM','image_file':'ibmm.png'},
    {'id':4,'name':'Apple','code':'AAPL','image_file':'apple.png'},
    {'id':5,'name':'Netflix','code':'NFLX','image_file':'netflix.png'},
    {'id':6,'name':'Opera','code':'OPRA','image_file':'opera.png'},
    {'id':7,'name':'Motorola','code':'MSI','image_file':'motorola-logo.png'},
    {'id':8,'name':'Unilever','code':'UL','image_file':'uni.svg'},
    {'id':9,'name':'Coca-Cola','code':'COKE','image_file':'coca.png'},
    {'id':10,'name':'McDonalds','code':'MCD','image_file':'mcdonaldss.png'},
    {'id':11,'name':'Amazon','code':'AMZN','image_file':'amazon.png'},
    {'id':12,'name':'Nike','code':'NKE','image_file':'nik.png'},
    {'id':13,'name':'XP','code':'XP','image_file':'xp.png'},
    {'id':14,'name':'Azul','code':'AZUL','image_file':'azul.png'},
    {'id':15,'name':'Ambev','code':'ABEV','image_file':'ambev.png'},
    {'id':16,'name':'Warner Bros','code':'WBD','image_file':'warner.png'},
    {'id':17,'name':'Uber','code':'UBER','image_file':'uberr.png'},
    {'id':18,'name':'Paramount','code':'PARAA','image_file':'paramountt.png'},
    ]

key='WJJEOQROMVPXCG9X'

@login_required(login_url='login')
def home(request):
    if 'time' not in request.session:
        request.session['time'] = '5min'
    if 'stock_list' not in request.session:
        request.session['stock_list']= []    
    context = {'stock_options':stock_options}  
    return render(request, 'base/home/home.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
                username = request.POST.get('username')
                password =request.POST.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.info(request, 'Nome de usuário ou senha incorreta')
        context = {}
    return render(request, "base/login/login.html", context)
   
def register(request):
    if request.user.is_authenticated:
        
        return redirect('home')
    else:
        form=CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Conta criada com sucesso,' + user + "!")
                return redirect('login')            
        context = {'form':form}     
    return render(request, 'base/register/register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')    
def stock(request,pk):
    selected_stock=None
    for i in stock_options:
        if i['code']==str(pk):
            selected_stock=i
    stock_code=selected_stock['code']
    time= request.session['time']
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+stock_code+'&interval='+time+'&outputsize=compact&apikey='+key 
    r = requests.get(url)
    data = r.json()
    new_stock_info=data['Time Series ('+time+')']
    values=list(new_stock_info.values())[0]
    alpha={'open':values['1. open'],'high':values['2. high'],'low':values['3. low'],'close':values['4. close']}
    time=time.replace('min','')
    if request.method == 'POST':
        if 'stock_list' in request.session:
            stock=request.POST.get('button')
            stock_list=request.session['stock_list']
            if stock in stock_list:
                stock_list.remove(stock)
                request.session['stock_list']=stock_list
            else:
                stock_list.append(stock)
                request.session['stock_list']=stock_list
        else:
            stock=request.POST.get('button')
            stock_list=[]
            stock_list.append(stock)
            request.session['stock_list']=stock_list
    stock_info={'info':selected_stock,'alpha':alpha, 'data':data, "time":time[:2], 'is_added':selected_stock['code'] in request.session['stock_list'], 'size':len(request.session['stock_list'])}
    context={"selected_stock":stock_info}
    return render(request, 'base/stock/stock.html',context)

@login_required(login_url='login')    
def config(request): 
    if request.method == 'POST':
        time = request.POST.get('select-time')
        request.session['time'] = time
    context={}
    return render(request, 'base/config/config.html',context)

@login_required(login_url='login')    
def monitored(request):
    stock_list=request.session['stock_list']
    all_stocks=stock_options
    display_list=[]
    for i in stock_list:
        for j in all_stocks:
            if i==j['code']:
                display_list.append(j) 
    if request.method == 'POST':
        stock=request.POST.get('exclude')        
        stock_list=request.session['stock_list']
        for i in stock_list:
            if i == stock:
                stock_list.remove(stock)
                request.session['stock_list']=stock_list
                return redirect('monitored')
    context={'display_list':display_list}
    return render(request, 'base/monitored/monitored.html',context)

def get_stock(request):
    time= request.session['time']
    selected_stock=None
    for code in request.session['stock_list']:
        for i in stock_options:
            if i['code']==code:
                url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+code+'&interval='+time+'&outputsize=compact&apikey='+key 
                api_request=requests.get(url)
                data = api_request.json()
                selected_stock=i
                new_stock_info=data['Time Series ('+time+')']
                values=list(new_stock_info.values())[0]
                alpha={'open':values['1. open'],'high':values['2. high'],'low':values['3. low'],'close':values['4. close']}
                register_call=Stock(
                    name=selected_stock['name'],
                    symbol=selected_stock['code'],
                    opened=alpha['open'],
                    high=alpha['high'],
                    low=alpha['low'],
                    close=alpha['close'],
                    interval=time)
                register_call.save()
    try:
        api_request.raise_for_status()
        api_request.json()
    except:
        return None

def compare_stock(price,high,low,request, name):
    #Não consegui fazer o send_email funcionar
    option=''
    option_subject=''
    name=name
    message= ('Sugestão de {option_subject}', '{option} as ações da empresa {name}!', 'iggodinho@poli.ufrj.br', [request.user.email])
    if (price > high):
        option_subject='Venda'
        option='Venda'
        #send_mail(message,fail_silently=False,)
        return print('Venda!')
    elif (price < low):
        option_subject='Compra'
        option='Compre'
        #send_mail(message,fail_silently=False,)
        return print('Compra!')
    else:
        return None

@login_required(login_url='login')    
def monitored_stock(request,pk):
    get_stock(request) #coloquei essa chamada da função aqui para simular o que seria a chamada periódica da api, já que não consegui fazer ela funcionar usando o celery
    selected_stock=None
    for i in stock_options:
        if i['code']==str(pk):
            selected_stock=i
    stock_code=selected_stock['code']
    time= request.session['time']
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+stock_code+'&interval='+time+'&outputsize=compact&apikey='+key 
    r = requests.get(url)
    data = r.json()
    new_stock_info=data['Time Series ('+time+')']
    values=list(new_stock_info.values())[0]
    alpha={'open':values['1. open'],'high':values['2. high'],'low':values['3. low'],'close':values['4. close']}
    registered=Stock.objects.filter(symbol=pk).values_list('name','symbol','opened','close','high','low','interval','created')
    reversed_list=[]
    for i in registered:
        reversed_list = [i] + reversed_list
    time=time.replace('min','')
    stock_info={'info':selected_stock,'alpha':alpha, 'data':data, "time":time[:2], 'registered':reversed_list,
    'is_added':selected_stock['code'] in request.session['stock_list'], 'size':len(request.session['stock_list'])}
    current=(list(reversed_list[0])[3])
    print(current)
    high=(list(reversed_list[1])[4])
    low=(list(reversed_list[1])[5])
    name=stock_info['info']['name']
    compare_stock(current,high,low,request,name)
    context={'stock_info':stock_info}
    return render(request, 'base/monitored_stock/monitored_stock.html',context)


