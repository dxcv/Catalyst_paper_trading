#coding:utf-8
from src.objT.objectT import objectT
from catalyst.api import order,order_target_percent, record, symbol,order_target_value,order_value
from catalyst.api import schedule_function,date_rules
import matplotlib.pyplot as plt

def initialize(context):
    context.mailema = 0
    context.univers = ['btc_usd',
                    'eos_usd',
                    'eth_usd',
                    'etc_usd',
                    'ltc_usd',
                    'zec_usd'
    ]
    context.objects = []
    context.basePrice = {}
    context.day =0 
    context.dayday = 0
    context.Vreturn = []
    context.base = []
    for obj in context.univers:
        context.objects.append(objectT(obj,0))
        context.basePrice[obj] = None
    context.objects = dict(zip(context.univers,context.objects))
    schedule_function(everyDay,half_days=False)

def everyDay(context, data):
    base = 0
    context.dayday+=1
    for obj in context.univers:
        market = context.objects[obj]
        market.update(data)
        if context.mailema:
            if not context.basePrice[obj]:
                context.basePrice[obj] = data.current(symbol(obj),'price')
            else:
                base += data.current(symbol(obj),'price')/context.basePrice[obj] -1

    if context.mailema:
        record('Vreturn',((context.portfolio.portfolio_value/10000) - 1))
        context.Vreturn.append((context.portfolio.portfolio_value/10000) - 1)
        base /= len(context.univers)
        record('base',base)
        context.base.append(base)

    print context.dayday,'cash: ',context.portfolio.cash
    print context.dayday,'all:',context.portfolio.portfolio_value

def handle_data(context, data):
    context.day+=1
    buyList = []
    for obj in context.univers:
        market = context.objects[obj]
        if not market.ATRs:
            market.setATRs(data)
        market.updateM(data)
        oprt = market.getOperator()
        if oprt in ['entry','add']:
            if not context.mailema:
                context.mailema = 1
            allM = context.portfolio.portfolio_value
            Qvalue = market.getUnit(allM) * data.current(symbol(obj),'price')
            buyList.append([symbol(obj),Qvalue])
        elif oprt in ['outry','clean']:
            order_target_percent(symbol(obj),0.0001)

    allBuyM = 0
    for each in buyList:
        allBuyM += each[1]
    if allBuyM:
        tranRate = context.portfolio.cash/allBuyM
        for each in buyList:
            if each[1]*tranRate > 10:
                order_value(each[0],each[1]*tranRate)

def analyze(context,perf):
    line1 = context.Vreturn
    line2 = context.base
    #line3 = line1 - line2
    x=range(len(line1))
    a = plt.plot(x,line1)
    b = plt.plot(x,line2)
    #c = plt.plot(x,line3)
    plt.show()