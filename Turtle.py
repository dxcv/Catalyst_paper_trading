#coding:utf-8
from src.objT.objectT import objectT
from catalyst.api import order,order_target_percent, record, symbol,order_target_value,order_value
from catalyst.api import set_slippage, set_commission
import matplotlib.pyplot as plt

def initialize(context):
    context.mailema = 0
    context.univers = ['btc_usd',
                    'eos_usd',
                    'eth_usd',
                    'etc_usd',
                    'ltc_usd',
                    'zec_usd',
                    'omg_usd',
                    'rrt_usd'
    ]
    context.objects = []
    context.basePrice = {}
    context.day =0 
    for obj in context.univers:
        context.objects.append(objectT(obj,0))
        context.basePrice[obj] = None
    context.objects = dict(zip(context.univers,context.objects))
    set_slippage(0.020)
    set_commission(0.002,0.002)

def handle_data(context, data):
    value = context.portfolio.portfolio_value 
    base = 0
    context.day+=1
    buyList = []
    for obj in context.univers:
        market = context.objects[obj]
        if context.mailema:
            if not context.basePrice[obj]:
                context.basePrice[obj] = data.current(symbol(obj),'price')
            else:
                base += data.current(symbol(obj),'price')/context.basePrice[obj] -1
        if not market.ATRs:
            market.setATRs(data)
        market.update(data)
        market.updateCurrentPrice(data)
        oprt = market.getOperator()
        if oprt in ['entry','add']:
            if not context.mailema:
                context.mailema = 1
            allM = context.portfolio.portfolio_value
            Qvalue = market.getUnit(allM) * data.current(symbol(obj),'price')
            #print context.day,'cash: ',context.portfolio.cash
            #print context.day,'all:',context.portfolio.portfolio_value
            print context.day,'oder: ',Qvalue
            #order_value(symbol(obj),Qvalue)
            buyList.append([symbol(obj),Qvalue])
        elif oprt in ['outry','clean']:
            #print context.day,'cash: ',context.portfolio.cash
            #print context.day,'all:',context.portfolio.portfolio_value
            order_target_percent(symbol(obj),0.0001)
    
    allBuyM = 0
    for each in buyList:
        allBuyM += each[1]
    if allBuyM > context.portfolio.cash and allBuyM > 0:
        tranRate = context.portfolio.cash/allBuyM
        for each in buyList:
            if each[1]*tranRate > 10:
                order_value(each[0],each[1]*tranRate)
    else:
        for each in buyList:
            if each[1] > 10:
                order_value(each[0],each[1])

    Cash = context.portfolio.cash
    print context.day,'cash: ',context.portfolio.cash
    print context.day,'all:',context.portfolio.portfolio_value
    #print context.slippage


    if context.mailema:
        record('Vreturn',((context.portfolio.portfolio_value/10000) - 1))
        base /= len(context.univers)
        record('base',base)

def analyze(context,perf):
    a = plt.subplot(211)
    line1 = perf['Vreturn']
    line2 = perf['base']
    x=range(len(line1))
    line3 = [(line1[i]+1)/(line2[i]+1)-1 for i in x]
    plt.plot(x,line1)
    plt.plot(x,line2)
    b = plt.subplot(212, sharex=a)
    #print line3
    plt.plot(x,[0 for i in x])
    plt.plot(x,line3)
    plt.show()