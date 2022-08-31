from django.shortcuts import render
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
    return render(request, 'base/login/login.html')

def register(request):
    return render(request, 'base/register/register.html')

    
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

